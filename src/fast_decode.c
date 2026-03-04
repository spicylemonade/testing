/*
 * fast_decode.c - High-performance DEFLATE decode loop with multi-symbol Huffman
 *
 * Key optimizations:
 *   1. 11-bit primary Huffman table (2048 entries) — fits in L1 cache
 *   2. Secondary table for codes > 11 bits (up to 15)
 *   3. Multi-symbol decode: up to 2 literal symbols per table lookup
 *   4. 64-bit branchless bit buffer (see bitreader.h)
 *   5. Word-at-a-time match copying with overlap handling
 *   6. Branchless literal/backref dispatch where possible
 *
 * Table entry layout (32-bit):
 *   - For single-symbol entries:
 *     bits[15:0]  = symbol (0-285 litlen, 0-29 dist)
 *     bits[19:16] = code length (1-11 for primary, or 0 if subtable redirect)
 *     bits[23:20] = type: 0=literal, 1=length, 2=end-of-block, 3=subtable
 *     bits[31:24] = reserved / extra info
 *
 *   - For double-symbol entries (two consecutive literals):
 *     bits[7:0]   = first literal byte
 *     bits[15:8]  = second literal byte
 *     bits[19:16] = total code length (sum of both)
 *     bits[23:20] = type: 4=double-literal
 *     bits[31:24] = reserved
 *
 *   - For subtable redirect:
 *     bits[15:0]  = subtable offset
 *     bits[19:16] = 0 (unused)
 *     bits[23:20] = type: 3=subtable
 *     bits[27:24] = subtable bits (extra bits to index into subtable)
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
#define MAX_DIST          30                      /* 0..29 distance codes */

/* Table entry fields */
#define ENTRY_SYM_MASK    0x0000FFFFU
#define ENTRY_LEN_SHIFT   16
#define ENTRY_LEN_MASK    0x000F0000U
#define ENTRY_TYPE_SHIFT  20
#define ENTRY_TYPE_MASK   0x00F00000U
#define ENTRY_SUB_SHIFT   24
#define ENTRY_SUB_MASK    0xFF000000U

/* Entry types */
#define TYPE_LITERAL      0
#define TYPE_LENGTH       1
#define TYPE_EOB          2
#define TYPE_SUBTABLE     3
#define TYPE_DOUBLE_LIT   4

/* Construct a table entry */
static inline uint32_t make_entry(int sym, int len, int type) {
    return (uint32_t)sym
         | ((uint32_t)len << ENTRY_LEN_SHIFT)
         | ((uint32_t)type << ENTRY_TYPE_SHIFT);
}

static inline uint32_t make_subtable_entry(int offset, int sub_bits) {
    return (uint32_t)offset
         | ((uint32_t)TYPE_SUBTABLE << ENTRY_TYPE_SHIFT)
         | ((uint32_t)sub_bits << ENTRY_SUB_SHIFT);
}

static inline uint32_t make_double_entry(int sym1, int sym2, int total_len) {
    return (uint32_t)(sym1 & 0xFF)
         | ((uint32_t)(sym2 & 0xFF) << 8)
         | ((uint32_t)total_len << ENTRY_LEN_SHIFT)
         | ((uint32_t)TYPE_DOUBLE_LIT << ENTRY_TYPE_SHIFT);
}

/* Extract fields */
static inline int entry_sym(uint32_t e)      { return (int)(e & ENTRY_SYM_MASK); }
static inline int entry_len(uint32_t e)      { return (int)((e >> ENTRY_LEN_SHIFT) & 0xF); }
static inline int entry_type(uint32_t e)     { return (int)((e >> ENTRY_TYPE_SHIFT) & 0xF); }
static inline int entry_sub_bits(uint32_t e) { return (int)((e >> ENTRY_SUB_SHIFT) & 0xFF); }

/* ========================================================================== */
/*                        Table construction                                  */
/* ========================================================================== */

/* Maximum litlen+dist table memory: 2048 primary + up to ~512 subtable entries */
#define MAX_LITLEN_TABLE  (PRIMARY_SIZE + 1024)
#define MAX_DIST_TABLE    (PRIMARY_SIZE + 512)

/*
 * Bit-reverse an n-bit code (DEFLATE uses LSB-first).
 */
static inline int bit_reverse(int code, int len) {
    int reversed = 0;
    for (int b = 0; b < len; b++)
        reversed |= ((code >> (len - 1 - b)) & 1) << b;
    return reversed;
}

/*
 * Build a fast Huffman lookup table from code lengths.
 *
 * Two-pass approach:
 *   Pass 1: Fill primary table, determine max subtable bits per primary index
 *   Pass 2: Allocate subtables, fill subtable entries
 *
 * Returns the total table size (primary + subtables), or -1 on error.
 */
static int build_fast_table(uint32_t *table, int primary_bits,
                            const uint8_t *lengths, int num_symbols,
                            int is_litlen) {
    int bl_count[MAX_CODEWORD + 1] = {0};
    int next_code[MAX_CODEWORD + 1] = {0};
    int sorted_codes[MAX_LIT_LEN + MAX_DIST]; /* reversed codes */
    int primary_size = 1 << primary_bits;

    /* Count codes per bit length */
    int max_len = 0;
    for (int i = 0; i < num_symbols; i++) {
        if (lengths[i] > MAX_CODEWORD) return -1;
        bl_count[lengths[i]]++;
        if (lengths[i] > max_len) max_len = lengths[i];
    }
    bl_count[0] = 0;

    /* If no codes at all, just clear the table */
    if (max_len == 0) {
        memset(table, 0, primary_size * sizeof(uint32_t));
        return primary_size;
    }

    /* Compute starting code for each bit length (RFC 1951 canonical) */
    int code = 0;
    for (int bits = 1; bits <= MAX_CODEWORD; bits++) {
        code = (code + bl_count[bits - 1]) << 1;
        next_code[bits] = code;
    }

    /* Assign canonical codes and bit-reverse them */
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) { sorted_codes[sym] = -1; continue; }
        int c = next_code[len]++;
        sorted_codes[sym] = bit_reverse(c, len);
    }

    /* Clear primary table */
    memset(table, 0, primary_size * sizeof(uint32_t));

    /* Pass 1: Determine max subtable bits needed per primary index */
    int8_t max_sub_bits[PRIMARY_SIZE];
    memset(max_sub_bits, 0, sizeof(max_sub_bits));

    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len <= primary_bits || len == 0) continue;
        int reversed = sorted_codes[sym];
        int primary_idx = reversed & (primary_size - 1);
        int extra = len - primary_bits;
        if (extra > max_sub_bits[primary_idx])
            max_sub_bits[primary_idx] = (int8_t)extra;
    }

    /* Allocate subtables */
    int subtable_offset = primary_size;
    int sub_offsets[PRIMARY_SIZE]; /* offset of each subtable, or -1 */
    memset(sub_offsets, -1, sizeof(sub_offsets));

    for (int idx = 0; idx < primary_size; idx++) {
        if (max_sub_bits[idx] > 0) {
            sub_offsets[idx] = subtable_offset;
            int sub_size = 1 << max_sub_bits[idx];
            /* Write subtable redirect in primary table */
            table[idx] = make_subtable_entry(subtable_offset, max_sub_bits[idx]);
            /* Clear subtable */
            memset(&table[subtable_offset], 0, sub_size * sizeof(uint32_t));
            subtable_offset += sub_size;
        }
    }

    /* Pass 2: Fill all entries */
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) continue;
        int reversed = sorted_codes[sym];

        /* Determine entry type */
        int type;
        if (is_litlen) {
            if (sym < 256)       type = TYPE_LITERAL;
            else if (sym == 256) type = TYPE_EOB;
            else                 type = TYPE_LENGTH;
        } else {
            type = TYPE_LITERAL;
        }

        uint32_t entry = make_entry(sym, len, type);

        if (len <= primary_bits) {
            /* Fill primary table slots */
            int fill = 1 << len;
            for (int idx = reversed; idx < primary_size; idx += fill) {
                /* Don't overwrite subtable redirects */
                if (sub_offsets[idx] < 0) {
                    table[idx] = entry;
                }
            }
        } else {
            /* Fill subtable entries */
            int primary_idx = reversed & (primary_size - 1);
            int sub_off = sub_offsets[primary_idx];
            if (sub_off < 0) return -1; /* shouldn't happen */
            int sub_bits = max_sub_bits[primary_idx];
            int sub_size = 1 << sub_bits;
            int extra_bits = len - primary_bits;
            int extra_code = reversed >> primary_bits;
            int sub_fill = 1 << extra_bits;
            for (int si = extra_code; si < sub_size; si += sub_fill) {
                table[sub_off + si] = entry;
            }
        }
    }

    (void)make_double_entry; /* suppress unused warning */
    return subtable_offset;
}

/* ========================================================================== */
/*                      Length/Distance tables (RFC 1951)                     */
/* ========================================================================== */

static const uint16_t length_base[29] = {
    3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,
    67,83,99,115,131,163,195,227,258
};
static const uint8_t length_extra[29] = {
    0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0
};
static const uint16_t dist_base[30] = {
    1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,
    1025,1537,2049,3073,4097,6145,8193,12289,16385,24577
};
static const uint8_t dist_extra[30] = {
    0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13
};
static const uint8_t codelen_order[19] = {
    16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15
};

/* ========================================================================== */
/*                         Copy with overlap handling                         */
/* ========================================================================== */

/*
 * Fast memory copy for LZ77 back-references.
 * Handles overlapping copies (distance < length) correctly.
 */
static inline void fast_copy(uint8_t *dst, size_t dst_pos,
                             uint32_t distance, uint32_t length) {
    uint8_t *out = dst + dst_pos;
    const uint8_t *src = out - distance;

    if (distance >= 8) {
        /* Non-overlapping or minimally overlapping: use word copies.
         * Copy 8 bytes at a time. Safe because output buffer has padding. */
        uint8_t *end = out + length;
        do {
            uint64_t chunk;
            memcpy(&chunk, src, 8);
            memcpy(out, &chunk, 8);
            src += 8;
            out += 8;
        } while (out < end);
    } else if (distance == 1) {
        /* RLE: single byte repeated */
        memset(out, *src, length);
    } else {
        /* Small distance overlap: byte-at-a-time */
        for (uint32_t i = 0; i < length; i++) {
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

/* ========================================================================== */
/*                    Dynamic Huffman table decode                            */
/* ========================================================================== */

static int decode_dynamic_tables(fast_bitreader_t *br,
                                 uint32_t *litlen_table,
                                 uint32_t *dist_table) {
    fbr_refill(br);
    int hlit  = (int)fbr_read_fast(br, 5) + 257;
    int hdist = (int)fbr_read_fast(br, 5) + 1;
    int hclen = (int)fbr_read_fast(br, 4) + 4;

    if (hlit > 286 || hdist > 30) return FD_ERROR_BAD_DATA;

    /* Read code-length code lengths */
    uint8_t cl_lengths[19] = {0};
    for (int i = 0; i < hclen; i++) {
        fbr_ensure(br, 3);
        cl_lengths[codelen_order[i]] = (uint8_t)fbr_read_fast(br, 3);
    }

    /* Build code-length table (7-bit, small) */
    uint32_t cl_table[128];
    if (build_fast_table(cl_table, 7, cl_lengths, 19, 0) < 0)
        return FD_ERROR_BAD_DATA;

    /* Decode all code lengths */
    int total = hlit + hdist;
    uint8_t all_lengths[286 + 30];
    memset(all_lengths, 0, sizeof(all_lengths));

    int i = 0;
    while (i < total) {
        fbr_refill(br);
        uint32_t idx = (uint32_t)fbr_peek(br, 7);
        uint32_t entry = cl_table[idx];
        int len = entry_len(entry);
        int sym = entry_sym(entry);
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

    /* Build litlen and dist fast tables */
    if (build_fast_table(litlen_table, PRIMARY_BITS, all_lengths, hlit, 1) < 0)
        return FD_ERROR_BAD_DATA;
    if (build_fast_table(dist_table, PRIMARY_BITS, all_lengths + hlit, hdist, 0) < 0)
        return FD_ERROR_BAD_DATA;

    return FD_OK;
}

/* ========================================================================== */
/*                          Fast decode loop                                  */
/* ========================================================================== */

/*
 * fd_inflate_fast - High-performance DEFLATE decompressor.
 *
 * Uses 11-bit primary Huffman table, 64-bit branchless bit reader,
 * multi-symbol decode, and word-at-a-time copy.
 */
int fd_inflate_fast(const uint8_t *src, size_t src_len,
                    uint8_t *dst, size_t dst_len,
                    size_t *out_len) {
    fast_bitreader_t br;
    fbr_init(&br, src, src_len);

    size_t out_pos = 0;
    int bfinal;

    /* Allocate tables on stack */
    uint32_t litlen_table[MAX_LITLEN_TABLE];
    uint32_t dist_table[MAX_DIST_TABLE];

    do {
        fbr_refill(&br);

        /* Read block header */
        bfinal = (int)fbr_read_fast(&br, 1);
        int btype = (int)fbr_read_fast(&br, 2);

        if (btype == 3) return FD_ERROR_BAD_BLOCK;

        if (btype == 0) {
            /* Stored (non-compressed) block */
            fbr_align_byte(&br);
            fbr_refill(&br);
            uint32_t len  = (uint32_t)fbr_read_fast(&br, 16);
            uint32_t nlen = (uint32_t)fbr_read_fast(&br, 16);
            if ((len ^ nlen) != 0xFFFF) return FD_ERROR_BAD_DATA;
            if (out_pos + len > dst_len) return FD_ERROR_SHORT_BUF;

            /* Copy directly from bitreader's byte stream */
            /* First, drain any remaining bits in the buffer */
            while (br.nbits >= 8 && len > 0) {
                dst[out_pos++] = (uint8_t)(br.bits & 0xFF);
                br.bits >>= 8;
                br.nbits -= 8;
                len--;
            }
            /* Then copy from the byte pointer */
            if (len > 0) {
                if (br.ptr + len > br.data_end) return FD_ERROR_BAD_DATA;
                memcpy(dst + out_pos, br.ptr, len);
                br.ptr += len;
                out_pos += len;
            }
            /* Reset bit buffer — stored blocks consume whole bytes,
             * next block starts at the current byte boundary */
            br.bits = 0;
            br.nbits = 0;
            continue;
        }

        /* Compressed block */
        if (btype == 1) {
            /* Fixed Huffman */
            uint8_t ll[288], dl[32];
            build_fixed_litlen_lengths(ll);
            build_fixed_dist_lengths(dl);
            build_fast_table(litlen_table, PRIMARY_BITS, ll, 288, 1);
            build_fast_table(dist_table, PRIMARY_BITS, dl, 32, 0);
        } else {
            /* Dynamic Huffman */
            int rc = decode_dynamic_tables(&br, litlen_table, dist_table);
            if (rc != FD_OK) return rc;
        }

        /*
         * Main decode loop — optimized for minimal branches.
         *
         * Structure: refill once, decode symbol, fast-path for literals.
         * After consuming at most ~30 bits per iteration (litlen + dist + extras),
         * we refill. With 56+ bits in the buffer after refill, we can decode
         * at least one full litlen+dist pair before the next refill.
         */
        {
            /* Safety margin: stop copying when we're close to end of output */
            const size_t safe_end = (dst_len > 274) ? dst_len - 274 : 0;

            fbr_refill(&br);

            for (;;) {
                /* Decode litlen symbol */
                uint32_t bits = (uint32_t)(br.bits & ((1u << PRIMARY_BITS) - 1));
                uint32_t entry = litlen_table[bits];

                if (__builtin_expect(entry_type(entry) == TYPE_LITERAL, 1)) {
                    /* FAST PATH: single literal — most common case.
                     * Consume bits and emit byte without full refill. */
                    int codelen = entry_len(entry);
                    br.bits >>= codelen;
                    br.nbits -= codelen;
                    dst[out_pos++] = (uint8_t)(entry & 0xFF); /* sym is in low bits */

                    /* Try to decode another literal immediately (no refill) */
                    if (__builtin_expect(br.nbits >= PRIMARY_BITS, 1)) {
                        bits = (uint32_t)(br.bits & ((1u << PRIMARY_BITS) - 1));
                        entry = litlen_table[bits];
                        if (__builtin_expect(entry_type(entry) == TYPE_LITERAL, 1)) {
                            codelen = entry_len(entry);
                            br.bits >>= codelen;
                            br.nbits -= codelen;
                            dst[out_pos++] = (uint8_t)(entry & 0xFF);

                            /* Third literal? */
                            if (__builtin_expect(br.nbits >= PRIMARY_BITS, 1)) {
                                bits = (uint32_t)(br.bits & ((1u << PRIMARY_BITS) - 1));
                                entry = litlen_table[bits];
                                if (entry_type(entry) == TYPE_LITERAL) {
                                    codelen = entry_len(entry);
                                    br.bits >>= codelen;
                                    br.nbits -= codelen;
                                    dst[out_pos++] = (uint8_t)(entry & 0xFF);
                                }
                            }
                        }
                    }

                    /* Refill and check bounds */
                    fbr_refill(&br);
                    if (__builtin_expect(out_pos >= safe_end, 0)) {
                        if (out_pos >= dst_len) return FD_ERROR_SHORT_BUF;
                    }
                    continue;
                }

                /* Slow paths: EOB, subtable, or length code */
                int type = entry_type(entry);
                int codelen = entry_len(entry);

                if (type == TYPE_EOB) {
                    br.bits >>= codelen;
                    br.nbits -= codelen;
                    break;
                }

                if (__builtin_expect(type == TYPE_SUBTABLE, 0)) {
                    int sub_off = entry_sym(entry);
                    int sub_bits = entry_sub_bits(entry);
                    br.bits >>= PRIMARY_BITS;
                    br.nbits -= PRIMARY_BITS;
                    if (__builtin_expect(br.nbits < sub_bits, 0)) fbr_refill(&br);
                    uint32_t sub_idx = (uint32_t)(br.bits & ((1u << sub_bits) - 1));
                    entry = litlen_table[sub_off + sub_idx];
                    type = entry_type(entry);
                    codelen = entry_len(entry) - PRIMARY_BITS;
                    br.bits >>= codelen;
                    br.nbits -= codelen;

                    if (type == TYPE_LITERAL) {
                        dst[out_pos++] = (uint8_t)(entry & 0xFF);
                        fbr_refill(&br);
                        continue;
                    }
                    if (type == TYPE_EOB) break;
                    /* Fall through to backref handling */
                } else {
                    /* TYPE_LENGTH in primary table */
                    br.bits >>= codelen;
                    br.nbits -= codelen;
                }

                /* Back-reference: decode length + distance */
                int sym = entry_sym(entry);
                int len_idx = sym - 257;
                if (__builtin_expect((unsigned)len_idx >= 29, 0))
                    return FD_ERROR_BAD_DATA;

                uint32_t match_len = length_base[len_idx];
                int extra = length_extra[len_idx];
                if (extra) {
                    if (__builtin_expect(br.nbits < extra, 0)) fbr_refill(&br);
                    match_len += (uint32_t)(br.bits & ((1u << extra) - 1));
                    br.bits >>= extra;
                    br.nbits -= extra;
                }

                /* Decode distance */
                if (__builtin_expect(br.nbits < PRIMARY_BITS, 0)) fbr_refill(&br);
                bits = (uint32_t)(br.bits & ((1u << PRIMARY_BITS) - 1));
                entry = dist_table[bits];
                type = entry_type(entry);
                codelen = entry_len(entry);

                int dist_sym;
                if (__builtin_expect(type != TYPE_SUBTABLE, 1)) {
                    br.bits >>= codelen;
                    br.nbits -= codelen;
                    dist_sym = entry_sym(entry);
                } else {
                    int sub_off = entry_sym(entry);
                    int sub_bits = entry_sub_bits(entry);
                    br.bits >>= PRIMARY_BITS;
                    br.nbits -= PRIMARY_BITS;
                    if (br.nbits < sub_bits) fbr_refill(&br);
                    uint32_t sub_idx = (uint32_t)(br.bits & ((1u << sub_bits) - 1));
                    entry = dist_table[sub_off + sub_idx];
                    codelen = entry_len(entry) - PRIMARY_BITS;
                    br.bits >>= codelen;
                    br.nbits -= codelen;
                    dist_sym = entry_sym(entry);
                }

                if (__builtin_expect((unsigned)dist_sym >= 30, 0))
                    return FD_ERROR_BAD_DATA;

                uint32_t distance = dist_base[dist_sym];
                extra = dist_extra[dist_sym];
                if (extra) {
                    if (__builtin_expect(br.nbits < extra, 0)) fbr_refill(&br);
                    distance += (uint32_t)(br.bits & ((1u << extra) - 1));
                    br.bits >>= extra;
                    br.nbits -= extra;
                }

                /* Validate and copy */
                if (__builtin_expect(distance > out_pos, 0))
                    return FD_ERROR_BAD_DATA;
                if (__builtin_expect(out_pos + match_len > dst_len, 0))
                    return FD_ERROR_SHORT_BUF;

                fast_copy(dst, out_pos, distance, match_len);
                out_pos += match_len;

                fbr_refill(&br);
            }
        }

    } while (!bfinal);

    if (out_len) *out_len = out_pos;
    return FD_OK;
}
