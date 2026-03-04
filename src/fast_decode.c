/*
 * fast_decode.c - High-performance DEFLATE decode loop
 *
 * Key optimizations (inspired by libdeflate's architecture):
 *   1. 11-bit primary Huffman table (2048 entries) — fits in L1 cache
 *   2. Secondary subtables for codes > 11 bits (up to 15)
 *   3. Multi-literal decode: up to 3 fast literals per refill cycle
 *   4. 64-bit branchless bit buffer (see bitreader.h)
 *   5. Packed table entries: base value + extra bits + code length in one u32
 *   6. saved_bitbuf technique: extract extra bits from pre-consume snapshot
 *   7. SSE2/AVX2 SIMD match copying with tiered distance handling
 *   8. Pre-computed fixed Huffman tables (built once)
 *   9. Next-entry preload during match copy to hide latency
 *
 * Table entry layout (32-bit), libdeflate-style:
 *
 *   Literal:
 *     Bit 31:     1 (HUFFDEC_LITERAL flag — testable via sign bit)
 *     Bits 23-16: literal byte value
 *     Bits 3-0:   codeword length (bits to consume)
 *
 *   Length:
 *     Bit 31:     0 (!HUFFDEC_LITERAL)
 *     Bits 24-16: length base value (3..258)
 *     Bits 15-13: 0 (no exceptional flags)
 *     Bits 11-8:  codeword length only (for saved_bitbuf shift)
 *     Bits 4-0:   codeword length + num_extra_bits (total bits to consume)
 *
 *   End-of-block:
 *     Bit 31:     0
 *     Bit 15:     1 (HUFFDEC_EXCEPTIONAL)
 *     Bit 13:     1 (HUFFDEC_END_OF_BLOCK)
 *     Bits 3-0:   codeword length
 *
 *   Subtable pointer:
 *     Bit 31:     0
 *     Bits 30-16: subtable start index
 *     Bit 15:     1 (HUFFDEC_EXCEPTIONAL)
 *     Bit 14:     1 (HUFFDEC_SUBTABLE_POINTER)
 *     Bits 11-8:  number of subtable bits
 *     Bits 3-0:   number of primary table bits
 *
 *   Offset (distance) entries have same format as Length but with offset base.
 */

#include "fast_deflate.h"
#include "bitreader.h"
#include <string.h>
#include <immintrin.h>

/* ========================================================================== */
/*                        Table layout constants                              */
/* ========================================================================== */

#define PRIMARY_BITS      11
#define PRIMARY_SIZE      (1 << PRIMARY_BITS)    /* 2048 */
#define MAX_SUBTABLE_BITS 4                       /* 15 - 11 */
#define MAX_CODEWORD      15
#define MAX_LIT_LEN       286                     /* 0..285 literal/length symbols */
#define MAX_DIST          32                      /* 0..31 distance codes (padded) */

/* Entry flags */
#define HUFFDEC_LITERAL         0x80000000U  /* Bit 31: literal flag (sign bit) */
#define HUFFDEC_EXCEPTIONAL     0x00008000U  /* Bit 15: subtable or EOB */
#define HUFFDEC_SUBTABLE_PTR    0x00004000U  /* Bit 14: subtable pointer */
#define HUFFDEC_END_OF_BLOCK    0x00002000U  /* Bit 13: end of block */

/* Extract helpers */
#define ENTRY_LITVAL(e)      (((e) >> 16) & 0xFF)     /* literal byte */
#define ENTRY_BASEVAL(e)     ((e) >> 16)               /* length/offset base */
#define ENTRY_BITS(e)        ((e) & 0x1F)              /* total bits to consume (low 5) */
#define ENTRY_CODELEN(e)     (((e) >> 8) & 0xF)        /* code length only (bits 11-8) */
#define ENTRY_SUBTBL_IDX(e)  ((e) >> 16)               /* subtable start index */
#define ENTRY_SUBTBL_BITS(e) (((e) >> 8) & 0x3F)       /* subtable bits (bits 13-8, masked) */

#define BITMASK(n) ((1U << (n)) - 1)

/* ========================================================================== */
/*                   Litlen and Offset decode result tables                   */
/* ========================================================================== */

/*
 * Static per-symbol result templates, indexed by symbol.
 * During table build, we OR in the codeword length to produce final entries.
 */

/* Literals: HUFFDEC_LITERAL | (byte << 16) */
/* Lengths: (base << 16) | num_extra_bits */
/* EOB: HUFFDEC_EXCEPTIONAL | HUFFDEC_END_OF_BLOCK */
static const uint32_t litlen_decode_results[288] = {
    /* 0..255: literals */
#define L(v) (HUFFDEC_LITERAL | ((uint32_t)(v) << 16))
    L(0),   L(1),   L(2),   L(3),   L(4),   L(5),   L(6),   L(7),
    L(8),   L(9),   L(10),  L(11),  L(12),  L(13),  L(14),  L(15),
    L(16),  L(17),  L(18),  L(19),  L(20),  L(21),  L(22),  L(23),
    L(24),  L(25),  L(26),  L(27),  L(28),  L(29),  L(30),  L(31),
    L(32),  L(33),  L(34),  L(35),  L(36),  L(37),  L(38),  L(39),
    L(40),  L(41),  L(42),  L(43),  L(44),  L(45),  L(46),  L(47),
    L(48),  L(49),  L(50),  L(51),  L(52),  L(53),  L(54),  L(55),
    L(56),  L(57),  L(58),  L(59),  L(60),  L(61),  L(62),  L(63),
    L(64),  L(65),  L(66),  L(67),  L(68),  L(69),  L(70),  L(71),
    L(72),  L(73),  L(74),  L(75),  L(76),  L(77),  L(78),  L(79),
    L(80),  L(81),  L(82),  L(83),  L(84),  L(85),  L(86),  L(87),
    L(88),  L(89),  L(90),  L(91),  L(92),  L(93),  L(94),  L(95),
    L(96),  L(97),  L(98),  L(99),  L(100), L(101), L(102), L(103),
    L(104), L(105), L(106), L(107), L(108), L(109), L(110), L(111),
    L(112), L(113), L(114), L(115), L(116), L(117), L(118), L(119),
    L(120), L(121), L(122), L(123), L(124), L(125), L(126), L(127),
    L(128), L(129), L(130), L(131), L(132), L(133), L(134), L(135),
    L(136), L(137), L(138), L(139), L(140), L(141), L(142), L(143),
    L(144), L(145), L(146), L(147), L(148), L(149), L(150), L(151),
    L(152), L(153), L(154), L(155), L(156), L(157), L(158), L(159),
    L(160), L(161), L(162), L(163), L(164), L(165), L(166), L(167),
    L(168), L(169), L(170), L(171), L(172), L(173), L(174), L(175),
    L(176), L(177), L(178), L(179), L(180), L(181), L(182), L(183),
    L(184), L(185), L(186), L(187), L(188), L(189), L(190), L(191),
    L(192), L(193), L(194), L(195), L(196), L(197), L(198), L(199),
    L(200), L(201), L(202), L(203), L(204), L(205), L(206), L(207),
    L(208), L(209), L(210), L(211), L(212), L(213), L(214), L(215),
    L(216), L(217), L(218), L(219), L(220), L(221), L(222), L(223),
    L(224), L(225), L(226), L(227), L(228), L(229), L(230), L(231),
    L(232), L(233), L(234), L(235), L(236), L(237), L(238), L(239),
    L(240), L(241), L(242), L(243), L(244), L(245), L(246), L(247),
    L(248), L(249), L(250), L(251), L(252), L(253), L(254), L(255),
#undef L
    /* 256: end-of-block */
    HUFFDEC_EXCEPTIONAL | HUFFDEC_END_OF_BLOCK,
    /* 257..285: lengths — (base << 16) | num_extra_bits */
#define LEN(base, extra) (((uint32_t)(base) << 16) | (extra))
    LEN(3,0),   LEN(4,0),   LEN(5,0),   LEN(6,0),
    LEN(7,0),   LEN(8,0),   LEN(9,0),   LEN(10,0),
    LEN(11,1),  LEN(13,1),  LEN(15,1),  LEN(17,1),
    LEN(19,2),  LEN(23,2),  LEN(27,2),  LEN(31,2),
    LEN(35,3),  LEN(43,3),  LEN(51,3),  LEN(59,3),
    LEN(67,4),  LEN(83,4),  LEN(99,4),  LEN(115,4),
    LEN(131,5), LEN(163,5), LEN(195,5), LEN(227,5),
    LEN(258,0),
#undef LEN
    /* 286-287: unused but some encoders emit them */
    0, 0
};

static const uint32_t offset_decode_results[32] = {
#define OFF(base, extra) (((uint32_t)(base) << 16) | (extra))
    OFF(1,0),     OFF(2,0),     OFF(3,0),     OFF(4,0),
    OFF(5,1),     OFF(7,1),     OFF(9,2),     OFF(13,2),
    OFF(17,3),    OFF(25,3),    OFF(33,4),    OFF(49,4),
    OFF(65,5),    OFF(97,5),    OFF(129,6),   OFF(193,6),
    OFF(257,7),   OFF(385,7),   OFF(513,8),   OFF(769,8),
    OFF(1025,9),  OFF(1537,9),  OFF(2049,10), OFF(3073,10),
    OFF(4097,11), OFF(6145,11), OFF(8193,12), OFF(12289,12),
    OFF(16385,13),OFF(24577,13),OFF(24577,13),OFF(24577,13),
#undef OFF
};

static const uint8_t codelen_order[19] = {
    16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15
};

/* ========================================================================== */
/*                        Table construction                                  */
/* ========================================================================== */

/* Maximum litlen+dist table memory: 2048 primary + up to ~512 subtable entries */
#define MAX_LITLEN_TABLE  (PRIMARY_SIZE + 1024)
#define MAX_DIST_TABLE    (PRIMARY_SIZE + 512)

/* Bit-reverse LUT */
static const uint8_t bit_reverse_lut[256] = {
    0x00,0x80,0x40,0xC0,0x20,0xA0,0x60,0xE0,0x10,0x90,0x50,0xD0,0x30,0xB0,0x70,0xF0,
    0x08,0x88,0x48,0xC8,0x28,0xA8,0x68,0xE8,0x18,0x98,0x58,0xD8,0x38,0xB8,0x78,0xF8,
    0x04,0x84,0x44,0xC4,0x24,0xA4,0x64,0xE4,0x14,0x94,0x54,0xD4,0x34,0xB4,0x74,0xF4,
    0x0C,0x8C,0x4C,0xCC,0x2C,0xAC,0x6C,0xEC,0x1C,0x9C,0x5C,0xDC,0x3C,0xBC,0x7C,0xFC,
    0x02,0x82,0x42,0xC2,0x22,0xA2,0x62,0xE2,0x12,0x92,0x52,0xD2,0x32,0xB2,0x72,0xF2,
    0x0A,0x8A,0x4A,0xCA,0x2A,0xAA,0x6A,0xEA,0x1A,0x9A,0x5A,0xDA,0x3A,0xBA,0x7A,0xFA,
    0x06,0x86,0x46,0xC6,0x26,0xA6,0x66,0xE6,0x16,0x96,0x56,0xD6,0x36,0xB6,0x76,0xF6,
    0x0E,0x8E,0x4E,0xCE,0x2E,0xAE,0x6E,0xEE,0x1E,0x9E,0x5E,0xDE,0x3E,0xBE,0x7E,0xFE,
    0x01,0x81,0x41,0xC1,0x21,0xA1,0x61,0xE1,0x11,0x91,0x51,0xD1,0x31,0xB1,0x71,0xF1,
    0x09,0x89,0x49,0xC9,0x29,0xA9,0x69,0xE9,0x19,0x99,0x59,0xD9,0x39,0xB9,0x79,0xF9,
    0x05,0x85,0x45,0xC5,0x25,0xA5,0x65,0xE5,0x15,0x95,0x55,0xD5,0x35,0xB5,0x75,0xF5,
    0x0D,0x8D,0x4D,0xCD,0x2D,0xAD,0x6D,0xED,0x1D,0x9D,0x5D,0xDD,0x3D,0xBD,0x7D,0xFD,
    0x03,0x83,0x43,0xC3,0x23,0xA3,0x63,0xE3,0x13,0x93,0x53,0xD3,0x33,0xB3,0x73,0xF3,
    0x0B,0x8B,0x4B,0xCB,0x2B,0xAB,0x6B,0xEB,0x1B,0x9B,0x5B,0xDB,0x3B,0xBB,0x7B,0xFB,
    0x07,0x87,0x47,0xC7,0x27,0xA7,0x67,0xE7,0x17,0x97,0x57,0xD7,0x37,0xB7,0x77,0xF7,
    0x0F,0x8F,0x4F,0xCF,0x2F,0xAF,0x6F,0xEF,0x1F,0x9F,0x5F,0xDF,0x3F,0xBF,0x7F,0xFF,
};

static inline int bit_reverse(int code, int len) {
    int r = (bit_reverse_lut[code & 0xFF] << 8) | bit_reverse_lut[(code >> 8) & 0xFF];
    return r >> (16 - len);
}

/*
 * Build a packed Huffman lookup table from code lengths.
 *
 * For litlen tables, uses litlen_decode_results[] to pack base+extra into entry.
 * For offset tables, uses offset_decode_results[].
 *
 * Entry format for length/offset codes:
 *   bits[31:16] = base value
 *   bits[15:13] = flags (exceptional, subtable_ptr, eob)
 *   bits[11:8]  = codeword length (for saved_bitbuf extraction)
 *   bits[4:0]   = codeword length + extra bits (total bits to consume)
 *
 * Returns total table size, or -1 on error.
 */
static int build_packed_table(uint32_t *table, int primary_bits,
                              const uint8_t *lengths, int num_symbols,
                              const uint32_t *decode_results) {
    int bl_count[MAX_CODEWORD + 1] = {0};
    int next_code[MAX_CODEWORD + 1] = {0};
    int reversed_codes[288 + 32]; /* enough for litlen or dist */
    int primary_size = 1 << primary_bits;

    /* Count codes per bit length */
    int max_len = 0;
    for (int i = 0; i < num_symbols; i++) {
        if (lengths[i] > MAX_CODEWORD) return -1;
        bl_count[lengths[i]]++;
        if (lengths[i] > max_len) max_len = lengths[i];
    }
    bl_count[0] = 0;

    if (max_len == 0) {
        memset(table, 0, primary_size * sizeof(uint32_t));
        return primary_size;
    }

    /* Compute starting code for each bit length */
    int code = 0;
    for (int bits = 1; bits <= MAX_CODEWORD; bits++) {
        code = (code + bl_count[bits - 1]) << 1;
        next_code[bits] = code;
    }

    /* Assign canonical codes and bit-reverse */
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) { reversed_codes[sym] = -1; continue; }
        int c = next_code[len]++;
        reversed_codes[sym] = bit_reverse(c, len);
    }

    /* Clear primary table */
    memset(table, 0, primary_size * sizeof(uint32_t));

    /* Pass 1: Determine max subtable bits per primary index */
    int8_t max_sub_bits[PRIMARY_SIZE];
    memset(max_sub_bits, 0, sizeof(max_sub_bits));
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len <= primary_bits || len == 0) continue;
        int reversed = reversed_codes[sym];
        int primary_idx = reversed & (primary_size - 1);
        int extra = len - primary_bits;
        if (extra > max_sub_bits[primary_idx])
            max_sub_bits[primary_idx] = (int8_t)extra;
    }

    /* Allocate subtables */
    int subtable_offset = primary_size;
    int sub_offsets[PRIMARY_SIZE];
    memset(sub_offsets, -1, sizeof(sub_offsets));

    for (int idx = 0; idx < primary_size; idx++) {
        if (max_sub_bits[idx] > 0) {
            sub_offsets[idx] = subtable_offset;
            int sub_size = 1 << max_sub_bits[idx];
            /* Write subtable redirect in primary table:
             * bits[30:16] = subtable start index
             * bit 15 = HUFFDEC_EXCEPTIONAL
             * bit 14 = HUFFDEC_SUBTABLE_PTR
             * bits[11:8] = subtable bits
             * bits[3:0] = primary_bits
             */
            table[idx] = ((uint32_t)subtable_offset << 16)
                       | HUFFDEC_EXCEPTIONAL
                       | HUFFDEC_SUBTABLE_PTR
                       | ((uint32_t)max_sub_bits[idx] << 8)
                       | (uint32_t)primary_bits;
            memset(&table[subtable_offset], 0, sub_size * sizeof(uint32_t));
            subtable_offset += sub_size;
        }
    }

    /* Pass 2: Fill all entries with packed format */
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) continue;
        int reversed = reversed_codes[sym];

        /* Get the result template for this symbol */
        uint32_t result = decode_results[sym];

        if (len <= primary_bits) {
            /*
             * Build the final packed entry:
             *   For literals:  result already has HUFFDEC_LITERAL | (byte << 16)
             *                  OR in codelen as bits[3:0]
             *   For lengths:   result has (base << 16) | extra_bits
             *                  Final entry = result | (codelen << 8) | codelen
             *                  But bits[4:0] should be codelen + extra_bits
             *   For EOB:       result has HUFFDEC_EXCEPTIONAL | HUFFDEC_END_OF_BLOCK
             *                  OR in codelen as bits[3:0]
             */
            uint32_t entry;
            if (result & HUFFDEC_LITERAL) {
                /* Literal: just add codelen to low bits */
                entry = result | (uint32_t)len;
            } else if (result & HUFFDEC_EXCEPTIONAL) {
                /* EOB: add codelen to low bits */
                entry = result | (uint32_t)len;
            } else {
                /* Length/offset: extra_bits is in result low bits */
                int extra_bits = result & 0x1F;
                entry = (result & 0xFFFF0000U)  /* base value in high 16 */
                      | ((uint32_t)len << 8)     /* codelen in bits[11:8] */
                      | (uint32_t)(len + extra_bits); /* total bits in [4:0] */
            }

            /* Fill primary table slots */
            int fill = 1 << len;
            for (int idx = reversed; idx < primary_size; idx += fill) {
                if (sub_offsets[idx] < 0)
                    table[idx] = entry;
            }
        } else {
            /* Subtable entries */
            int primary_idx = reversed & (primary_size - 1);
            int sub_off = sub_offsets[primary_idx];
            if (sub_off < 0) return -1;
            int sub_bits = max_sub_bits[primary_idx];
            int sub_size = 1 << sub_bits;
            int extra_code_bits = len - primary_bits;
            int extra_code = reversed >> primary_bits;

            /* Build entry — for subtable entries, codelen is the FULL length */
            uint32_t entry;
            if (result & HUFFDEC_LITERAL) {
                entry = result | (uint32_t)len;
            } else if (result & HUFFDEC_EXCEPTIONAL) {
                entry = result | (uint32_t)len;
            } else {
                int extra_bits = result & 0x1F;
                entry = (result & 0xFFFF0000U)
                      | ((uint32_t)len << 8)
                      | (uint32_t)(len + extra_bits);
            }

            int sub_fill = 1 << extra_code_bits;
            for (int si = extra_code; si < sub_size; si += sub_fill)
                table[sub_off + si] = entry;
        }
    }

    return subtable_offset;
}

/* ========================================================================== */
/*                         Copy with overlap handling                         */
/* ========================================================================== */

static inline void fast_copy(uint8_t *dst, size_t dst_pos,
                             uint32_t distance, uint32_t length) {
    uint8_t *out = dst + dst_pos;
    const uint8_t *src = out - distance;

    if (__builtin_expect(distance >= 16, 1)) {
#ifdef __AVX2__
        if (distance >= 32 && length >= 32) {
            uint8_t *end = out + length;
            do {
                __m256i chunk = _mm256_loadu_si256((const __m256i *)src);
                _mm256_storeu_si256((__m256i *)out, chunk);
                src += 32;
                out += 32;
            } while (out < end);
            return;
        }
#endif
        if (length >= 16) {
            uint8_t *end = out + length;
            do {
                __m128i chunk = _mm_loadu_si128((const __m128i *)src);
                _mm_storeu_si128((__m128i *)out, chunk);
                src += 16;
                out += 16;
            } while (out < end);
            return;
        }
        {
            uint64_t chunk;
            memcpy(&chunk, src, 8);
            memcpy(out, &chunk, 8);
            if (length > 8) {
                memcpy(&chunk, src + 8, 8);
                memcpy(out + 8, &chunk, 8);
            }
        }
    } else if (distance >= 8) {
        uint8_t *end = out + length;
        do {
            uint64_t chunk;
            memcpy(&chunk, src, 8);
            memcpy(out, &chunk, 8);
            src += 8;
            out += 8;
        } while (out < end);
    } else if (distance == 1) {
        memset(out, *src, length);
    } else if (distance >= 4) {
        uint8_t *end = out + length;
        do {
            uint32_t chunk;
            memcpy(&chunk, src, 4);
            memcpy(out, &chunk, 4);
            src += 4;
            out += 4;
        } while (out < end);
    } else {
        if (distance == 2) {
            uint16_t pat;
            memcpy(&pat, src, 2);
            uint8_t *end = out + length;
            while (out < end) {
                memcpy(out, &pat, 2);
                out += 2;
            }
        } else { /* distance == 3 */
            for (uint32_t i = 0; i < length; i++)
                out[i] = src[i];
        }
    }
}

/* ========================================================================== */
/*                         Fixed Huffman tables                               */
/* ========================================================================== */

static void build_fixed_litlen_lengths(uint8_t *lengths) {
    for (int i = 0;   i <= 143; i++) lengths[i] = 8;
    for (int i = 144; i <= 255; i++) lengths[i] = 9;
    for (int i = 256; i <= 279; i++) lengths[i] = 7;
    for (int i = 280; i <= 287; i++) lengths[i] = 8;
}

static void build_fixed_dist_lengths(uint8_t *lengths) {
    for (int i = 0; i < 32; i++) lengths[i] = 5;
}

static uint32_t fixed_litlen_table[MAX_LITLEN_TABLE];
static uint32_t fixed_dist_table[MAX_DIST_TABLE];
static int fixed_tables_built = 0;

static void ensure_fixed_tables(void) {
    if (__builtin_expect(fixed_tables_built, 1)) return;
    uint8_t ll[288], dl[32];
    build_fixed_litlen_lengths(ll);
    build_fixed_dist_lengths(dl);
    build_packed_table(fixed_litlen_table, PRIMARY_BITS, ll, 288, litlen_decode_results);
    build_packed_table(fixed_dist_table, PRIMARY_BITS, dl, 32, offset_decode_results);
    fixed_tables_built = 1;
}

/* ========================================================================== */
/*                    Dynamic Huffman table decode                            */
/* ========================================================================== */

/* Code-length codes use a simple 7-bit table (not packed format) */
#define CL_TABLE_BITS 7
#define CL_TABLE_SIZE (1 << CL_TABLE_BITS)

/* Simple code-length table entry: sym in bits[15:4], len in bits[3:0] */
static int build_cl_table(uint32_t *table, const uint8_t *lengths, int count) {
    int bl_count[16] = {0};
    int next_code[16] = {0};
    int tsize = CL_TABLE_SIZE;

    int max_len = 0;
    for (int i = 0; i < count; i++) {
        bl_count[lengths[i]]++;
        if (lengths[i] > max_len) max_len = lengths[i];
    }
    bl_count[0] = 0;

    if (max_len == 0) {
        memset(table, 0, tsize * sizeof(uint32_t));
        return 0;
    }

    int code = 0;
    for (int b = 1; b <= 15; b++) {
        code = (code + bl_count[b-1]) << 1;
        next_code[b] = code;
    }

    memset(table, 0, tsize * sizeof(uint32_t));

    for (int sym = 0; sym < count; sym++) {
        int len = lengths[sym];
        if (len == 0) continue;
        int c = next_code[len]++;
        int rev = bit_reverse(c, len);
        /* Pack: sym in bits[15:4], len in bits[3:0] */
        uint32_t entry = ((uint32_t)sym << 4) | (uint32_t)len;
        int fill = 1 << len;
        for (int idx = rev; idx < tsize; idx += fill)
            table[idx] = entry;
    }
    return 0;
}

static int decode_dynamic_tables(fast_bitreader_t *br,
                                 uint32_t *litlen_table,
                                 uint32_t *dist_table) {
    fbr_refill(br);
    int hlit  = (int)fbr_read_fast(br, 5) + 257;
    int hdist = (int)fbr_read_fast(br, 5) + 1;
    int hclen = (int)fbr_read_fast(br, 4) + 4;

    if (hlit > 286 || hdist > 30) return FD_ERROR_BAD_DATA;

    uint8_t cl_lengths[19] = {0};
    for (int i = 0; i < hclen; i++) {
        fbr_ensure(br, 3);
        cl_lengths[codelen_order[i]] = (uint8_t)fbr_read_fast(br, 3);
    }

    uint32_t cl_table[CL_TABLE_SIZE];
    build_cl_table(cl_table, cl_lengths, 19);

    int total = hlit + hdist;
    uint8_t all_lengths[286 + 30];
    memset(all_lengths, 0, sizeof(all_lengths));

    int i = 0;
    while (i < total) {
        fbr_refill(br);
        uint32_t idx = (uint32_t)fbr_peek(br, CL_TABLE_BITS);
        uint32_t entry = cl_table[idx];
        int len = (int)(entry & 0xF);
        int sym = (int)(entry >> 4);
        if (len == 0) return FD_ERROR_BAD_DATA;
        fbr_consume(br, len);

        if (sym <= 15) {
            all_lengths[i++] = (uint8_t)sym;
        } else if (sym == 16) {
            if (i == 0) return FD_ERROR_BAD_DATA;
            int rep = (int)fbr_read(br, 2) + 3;
            uint8_t prev = all_lengths[i - 1];
            for (int j = 0; j < rep && i < total; j++)
                all_lengths[i++] = prev;
        } else if (sym == 17) {
            int rep = (int)fbr_read(br, 3) + 3;
            for (int j = 0; j < rep && i < total; j++)
                all_lengths[i++] = 0;
        } else if (sym == 18) {
            int rep = (int)fbr_read(br, 7) + 11;
            for (int j = 0; j < rep && i < total; j++)
                all_lengths[i++] = 0;
        } else {
            return FD_ERROR_BAD_DATA;
        }
    }

    if (build_packed_table(litlen_table, PRIMARY_BITS, all_lengths, hlit,
                           litlen_decode_results) < 0)
        return FD_ERROR_BAD_DATA;
    if (build_packed_table(dist_table, PRIMARY_BITS, all_lengths + hlit, hdist,
                           offset_decode_results) < 0)
        return FD_ERROR_BAD_DATA;

    return FD_OK;
}

/* ========================================================================== */
/*                          Fast decode loop                                  */
/* ========================================================================== */

__attribute__((flatten))
int fd_inflate_fast(const uint8_t *src, size_t src_len,
                    uint8_t *dst, size_t dst_len,
                    size_t *out_len) {
    fast_bitreader_t br;
    fbr_init(&br, src, src_len);

    size_t out_pos = 0;
    int bfinal;

    uint32_t litlen_table[MAX_LITLEN_TABLE];
    uint32_t dist_table[MAX_DIST_TABLE];

    do {
        fbr_refill(&br);

        bfinal = (int)fbr_read_fast(&br, 1);
        int btype = (int)fbr_read_fast(&br, 2);

        if (btype == 3) return FD_ERROR_BAD_BLOCK;

        if (btype == 0) {
            /* Stored block */
            fbr_align_byte(&br);
            fbr_refill(&br);
            uint32_t len  = (uint32_t)fbr_read_fast(&br, 16);
            uint32_t nlen = (uint32_t)fbr_read_fast(&br, 16);
            if ((len ^ nlen) != 0xFFFF) return FD_ERROR_BAD_DATA;
            if (out_pos + len > dst_len) return FD_ERROR_SHORT_BUF;

            while (br.nbits >= 8 && len > 0) {
                dst[out_pos++] = (uint8_t)(br.bits & 0xFF);
                br.bits >>= 8;
                br.nbits -= 8;
                len--;
            }
            if (len > 0) {
                if (br.ptr + len > br.data_end) return FD_ERROR_BAD_DATA;
                memcpy(dst + out_pos, br.ptr, len);
                br.ptr += len;
                out_pos += len;
            }
            br.bits = 0;
            br.nbits = 0;
            continue;
        }

        const uint32_t *ll_tbl;
        const uint32_t *dt_tbl;

        if (btype == 1) {
            ensure_fixed_tables();
            ll_tbl = fixed_litlen_table;
            dt_tbl = fixed_dist_table;
        } else {
            int rc = decode_dynamic_tables(&br, litlen_table, dist_table);
            if (rc != FD_OK) return rc;
            ll_tbl = litlen_table;
            dt_tbl = dist_table;
        }

        /*
         * Fast decode loop using packed entries and saved_bitbuf.
         *
         * Key technique: before consuming bits for a length/offset code,
         * we save the bitbuf. The extra bits follow the codeword bits
         * in the saved buffer, so we can extract them with:
         *   extra_val = (saved_bitbuf & mask) >> codelen
         * where mask = (1 << (codelen + extra_bits)) - 1
         *
         * The packed entry has:
         *   bits[4:0]  = codelen + extra_bits (total bits to consume)
         *   bits[11:8] = codelen (for the shift amount)
         *   bits[31:16] = base value
         *
         * So: value = base + ((saved_bitbuf & BITMASK(total)) >> codelen)
         * Which is: ENTRY_BASEVAL(entry) + (EXTRACT(saved, entry) >> ENTRY_CODELEN(entry))
         */
        {
            const size_t safe_end = (dst_len > 274) ? dst_len - 274 : 0;
            uint32_t match_length = 0; /* shared between primary/subtable length paths */

            fbr_refill(&br);
            uint32_t entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];

            for (;;) {
                uint64_t saved_bitbuf;

                /*
                 * Save bitbuf before consuming. For literals, the codelen
                 * is in bits[3:0]. For lengths, total_bits is in bits[4:0].
                 */
                saved_bitbuf = br.bits;
                br.bits >>= (uint8_t)entry;
                br.nbits -= (uint8_t)entry;

                if (__builtin_expect((int32_t)entry < 0, 1)) {
                    /* HUFFDEC_LITERAL (bit 31 set = negative as signed).
                     * Literal value is in bits[23:16]. */
                    dst[out_pos++] = (uint8_t)(entry >> 16);

                    /* Try 2nd fast literal without refill */
                    if (__builtin_expect(br.nbits >= PRIMARY_BITS, 1)) {
                        entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                        if (__builtin_expect((int32_t)entry < 0, 1)) {
                            saved_bitbuf = br.bits;
                            br.bits >>= (uint8_t)entry;
                            br.nbits -= (uint8_t)entry;
                            dst[out_pos++] = (uint8_t)(entry >> 16);

                            /* Try 3rd fast literal */
                            if (__builtin_expect(br.nbits >= PRIMARY_BITS, 1)) {
                                entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                                if ((int32_t)entry < 0) {
                                    br.bits >>= (uint8_t)entry;
                                    br.nbits -= (uint8_t)entry;
                                    dst[out_pos++] = (uint8_t)(entry >> 16);
                                    /* Preload next entry after refill */
                                    fbr_refill(&br);
                                    entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                                    if (__builtin_expect(out_pos >= safe_end, 0)) {
                                        if (out_pos >= dst_len)
                                            return FD_ERROR_SHORT_BUF;
                                    }
                                    continue;
                                }
                                /* Non-literal: fall through to handle it */
                            } else {
                                /* Need refill, then preload */
                                fbr_refill(&br);
                                entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                                if (__builtin_expect(out_pos >= safe_end, 0)) {
                                    if (out_pos >= dst_len)
                                        return FD_ERROR_SHORT_BUF;
                                }
                                continue;
                            }
                        }
                        /* Non-literal from 2nd: entry already loaded, fall through */
                    } else {
                        /* Need refill */
                        fbr_refill(&br);
                        entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                        if (__builtin_expect(out_pos >= safe_end, 0)) {
                            if (out_pos >= dst_len)
                                return FD_ERROR_SHORT_BUF;
                        }
                        continue;
                    }

                    /* Fall through: entry contains a non-literal from a
                     * subsequent literal attempt. Re-save and consume. */
                    saved_bitbuf = br.bits;
                    br.bits >>= (uint8_t)entry;
                    br.nbits -= (uint8_t)entry;
                }

                /* Not a literal. Check for exceptional (EOB or subtable). */
                if (__builtin_expect(entry & HUFFDEC_EXCEPTIONAL, 0)) {
                    if (entry & HUFFDEC_END_OF_BLOCK)
                        break;

                    /* Subtable pointer */
                    uint32_t sub_idx = ENTRY_SUBTBL_IDX(entry);
                    int sub_bits = ENTRY_SUBTBL_BITS(entry);
                    /* We already consumed primary_bits via the entry shift.
                     * Now index into subtable with the next sub_bits. */
                    /* Actually, we consumed (uint8_t)entry bits which is
                     * primary_bits (stored in bits[3:0] of subtable ptr entry). */
                    if (__builtin_expect(br.nbits < (int)sub_bits, 0))
                        fbr_refill(&br);
                    entry = ll_tbl[sub_idx + (br.bits & BITMASK(sub_bits))];

                    /* The subtable entry could be literal, length, or EOB */
                    if ((int32_t)entry < 0) {
                        /* Literal from subtable */
                        int sub_codelen = ENTRY_BITS(entry) - PRIMARY_BITS;
                        br.bits >>= sub_codelen;
                        br.nbits -= sub_codelen;
                        dst[out_pos++] = (uint8_t)(entry >> 16);
                        fbr_refill(&br);
                        entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                        continue;
                    }
                    if (entry & HUFFDEC_END_OF_BLOCK) {
                        int sub_codelen = ENTRY_BITS(entry) - PRIMARY_BITS;
                        br.bits >>= sub_codelen;
                        br.nbits -= sub_codelen;
                        break;
                    }
                    /* Length from subtable: consume remaining bits and extract
                     * extra bits. The entry has full codelen in bits[11:8] and
                     * full total_bits in bits[4:0]. We need to consume
                     * total_bits - primary_bits from current buffer. */
                    {
                        int total_bits = ENTRY_BITS(entry);
                        int remaining = total_bits - PRIMARY_BITS;
                        saved_bitbuf = br.bits;
                        br.bits >>= remaining;
                        br.nbits -= remaining;
                        int codelen_remaining = ENTRY_CODELEN(entry) - PRIMARY_BITS;
                        match_length = ENTRY_BASEVAL(entry)
                            + (uint32_t)((saved_bitbuf & BITMASK(remaining)) >> codelen_remaining);
                        goto decode_distance;
                    }
                }

                /* Length entry (not exceptional, not literal).
                 * saved_bitbuf was captured before consume.
                 * Extract length = base + extra_bits_value. */
                match_length = ENTRY_BASEVAL(entry)
                    + (uint32_t)((saved_bitbuf & BITMASK((uint8_t)entry))
                                 >> (uint8_t)(entry >> 8));

            decode_distance:
                /* Decode distance */
                if (__builtin_expect(br.nbits < PRIMARY_BITS, 0))
                    fbr_refill(&br);

                entry = dt_tbl[br.bits & BITMASK(PRIMARY_BITS)];

                if (__builtin_expect(entry & HUFFDEC_EXCEPTIONAL, 0)) {
                    /* Subtable for distance */
                    uint32_t sub_idx = ENTRY_SUBTBL_IDX(entry);
                    int sub_bits = ENTRY_SUBTBL_BITS(entry);
                    br.bits >>= PRIMARY_BITS;
                    br.nbits -= PRIMARY_BITS;
                    if (br.nbits < sub_bits) fbr_refill(&br);
                    entry = dt_tbl[sub_idx + (br.bits & BITMASK(sub_bits))];
                    /* Consume remaining bits for this entry */
                    int remaining = ENTRY_BITS(entry) - PRIMARY_BITS;
                    saved_bitbuf = br.bits;
                    br.bits >>= remaining;
                    br.nbits -= remaining;
                    int codelen_remaining = ENTRY_CODELEN(entry) - PRIMARY_BITS;
                    uint32_t dist_sub = ENTRY_BASEVAL(entry)
                        + (uint32_t)((saved_bitbuf & BITMASK(remaining)) >> codelen_remaining);

                    if (__builtin_expect(dist_sub > out_pos, 0))
                        return FD_ERROR_BAD_DATA;
                    if (__builtin_expect(out_pos + match_length > dst_len, 0))
                        return FD_ERROR_SHORT_BUF;

                    fast_copy(dst, out_pos, dist_sub, match_length);
                    out_pos += match_length;

                    fbr_refill(&br);
                    entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
                    continue;
                }

                /* Common case: distance from primary table */
                saved_bitbuf = br.bits;
                br.bits >>= (uint8_t)entry;
                br.nbits -= (uint8_t)entry;

                {
                    uint32_t distance = ENTRY_BASEVAL(entry)
                        + (uint32_t)((saved_bitbuf & BITMASK((uint8_t)entry))
                                     >> (uint8_t)(entry >> 8));

                    if (__builtin_expect(distance > out_pos, 0))
                        return FD_ERROR_BAD_DATA;
                    if (__builtin_expect(out_pos + match_length > dst_len, 0))
                        return FD_ERROR_SHORT_BUF;

                    fast_copy(dst, out_pos, distance, match_length);
                    out_pos += match_length;
                }

                /* Preload next litlen entry (overlaps with copy latency) */
                fbr_refill(&br);
                entry = ll_tbl[br.bits & BITMASK(PRIMARY_BITS)];
            }
        }
    } while (!bfinal);

    if (out_len) *out_len = out_pos;
    return FD_OK;
}
