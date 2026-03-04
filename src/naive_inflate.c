/*
 * naive_inflate.c - Correct, straightforward DEFLATE decompressor (RFC 1951)
 *
 * This is the reference baseline implementation. It prioritizes correctness
 * and readability over performance. It handles all three block types:
 *   - Type 0: Non-compressed (stored) blocks
 *   - Type 1: Fixed Huffman codes
 *   - Type 2: Dynamic Huffman codes
 *
 * Back-references up to 32KB window. Fully RFC 1951 compliant.
 */

#include "fast_deflate.h"
#include <string.h>

/* Constants from RFC 1951 */
#define MAX_BITS       15
#define MAX_LIT_LEN    286  /* 0..285 literal/length symbols */
#define MAX_DIST       30   /* 0..29 distance codes */
#define MAX_CODE_LEN   19   /* Code length alphabet size */
#define WINDOW_SIZE    32768

/* Huffman table entry: symbol + bit length */
typedef struct {
    uint16_t symbol;
    uint16_t length;  /* code length in bits */
} huff_entry_t;

/* Huffman lookup table (simple flat array indexed by bit-reversed code) */
typedef struct {
    huff_entry_t *entries;
    int           table_bits;
    int           max_code;
} huff_table_t;

/* Bit reader state */
typedef struct {
    const uint8_t *data;
    size_t         data_len;
    size_t         byte_pos;
    int            bit_pos;    /* 0-7, bits consumed in current byte */
    uint32_t       buffer;     /* bit accumulator */
    int            bits_avail; /* bits available in buffer */
} bitreader_t;

static void br_init(bitreader_t *br, const uint8_t *data, size_t len) {
    br->data = data;
    br->data_len = len;
    br->byte_pos = 0;
    br->bit_pos = 0;
    br->buffer = 0;
    br->bits_avail = 0;
}

static int br_refill(bitreader_t *br) {
    while (br->bits_avail <= 24 && br->byte_pos < br->data_len) {
        br->buffer |= (uint32_t)br->data[br->byte_pos++] << br->bits_avail;
        br->bits_avail += 8;
    }
    return br->bits_avail > 0;
}

static uint32_t br_peek(bitreader_t *br, int n) {
    if (br->bits_avail < n) br_refill(br);
    return br->buffer & ((1u << n) - 1);
}

static void br_consume(bitreader_t *br, int n) {
    br->buffer >>= n;
    br->bits_avail -= n;
}

static uint32_t br_read(bitreader_t *br, int n) {
    if (n == 0) return 0;
    br_refill(br);
    uint32_t val = br->buffer & ((1u << n) - 1);
    br->buffer >>= n;
    br->bits_avail -= n;
    return val;
}

static void br_align_byte(bitreader_t *br) {
    int skip = br->bits_avail & 7;
    br->buffer >>= skip;
    br->bits_avail -= skip;
}

/* Length base values and extra bits (codes 257-285) */
static const uint16_t length_base[29] = {
    3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,
    67,83,99,115,131,163,195,227,258
};
static const uint8_t length_extra[29] = {
    0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0
};

/* Distance base values and extra bits (codes 0-29) */
static const uint16_t dist_base[30] = {
    1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,
    1025,1537,2049,3073,4097,6145,8193,12289,16385,24577
};
static const uint8_t dist_extra[30] = {
    0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13
};

/* Code length order for dynamic Huffman header */
static const uint8_t codelen_order[19] = {
    16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15
};

/*
 * Build a simple Huffman decode table from code lengths.
 * Returns allocated table on success, NULL on error.
 * Uses the canonical Huffman construction from RFC 1951 section 3.2.2.
 */
static int build_huff_table(huff_entry_t *table, int table_bits,
                            const uint8_t *lengths, int num_symbols) {
    int bl_count[MAX_BITS + 1] = {0};
    int next_code[MAX_BITS + 1];
    int code;

    /* Count codes per length */
    for (int i = 0; i < num_symbols; i++) {
        if (lengths[i] > MAX_BITS) return FD_ERROR_BAD_DATA;
        bl_count[lengths[i]]++;
    }
    bl_count[0] = 0;

    /* Compute starting code for each length */
    code = 0;
    for (int bits = 1; bits <= MAX_BITS; bits++) {
        code = (code + bl_count[bits - 1]) << 1;
        next_code[bits] = code;
    }

    /* Clear table */
    int table_size = 1 << table_bits;
    for (int i = 0; i < table_size; i++) {
        table[i].symbol = 0xFFFF;
        table[i].length = 0;
    }

    /* Assign codes and fill table */
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) continue;

        int c = next_code[len]++;

        /* Bit-reverse the code for LSB-first lookup */
        int reversed = 0;
        for (int b = 0; b < len; b++) {
            reversed |= ((c >> (len - 1 - b)) & 1) << b;
        }

        if (len <= table_bits) {
            /* Fill all entries that share this prefix */
            int fill = 1 << len;
            for (int idx = reversed; idx < table_size; idx += fill) {
                table[idx].symbol = (uint16_t)sym;
                table[idx].length = (uint16_t)len;
            }
        }
        /* For codes longer than table_bits, we'd need subtables.
         * For the naive decoder, we use a sufficiently large table. */
    }

    return FD_OK;
}

/* Decode one symbol using the lookup table */
static int huff_decode(bitreader_t *br, const huff_entry_t *table, int table_bits) {
    br_refill(br);
    uint32_t idx = br_peek(br, table_bits);
    huff_entry_t entry = table[idx];

    if (entry.length == 0 || entry.symbol == 0xFFFF) {
        return -1;  /* Invalid code */
    }

    br_consume(br, entry.length);
    return entry.symbol;
}

/* Fixed Huffman code lengths for literal/length alphabet (RFC 1951 section 3.2.6) */
static void build_fixed_litlen_lengths(uint8_t *lengths) {
    int i;
    for (i = 0;   i <= 143; i++) lengths[i] = 8;
    for (i = 144; i <= 255; i++) lengths[i] = 9;
    for (i = 256; i <= 279; i++) lengths[i] = 7;
    for (i = 280; i <= 287; i++) lengths[i] = 8;
}

/* Fixed Huffman code lengths for distance alphabet */
static void build_fixed_dist_lengths(uint8_t *lengths) {
    for (int i = 0; i < 32; i++) lengths[i] = 5;
}

/*
 * Decode dynamic Huffman table header (BTYPE=10)
 */
static int decode_dynamic_tables(bitreader_t *br,
                                  huff_entry_t *litlen_table, int litlen_bits,
                                  huff_entry_t *dist_table, int dist_bits) {
    int hlit  = br_read(br, 5) + 257;
    int hdist = br_read(br, 5) + 1;
    int hclen = br_read(br, 4) + 4;

    if (hlit > 286 || hdist > 30) return FD_ERROR_BAD_DATA;

    /* Read code-length code lengths */
    uint8_t codelen_lengths[MAX_CODE_LEN] = {0};
    for (int i = 0; i < hclen; i++) {
        codelen_lengths[codelen_order[i]] = (uint8_t)br_read(br, 3);
    }

    /* Build code-length Huffman table (max 7 bits) */
    huff_entry_t codelen_table[128]; /* 2^7 entries */
    int rc = build_huff_table(codelen_table, 7, codelen_lengths, MAX_CODE_LEN);
    if (rc != FD_OK) return rc;

    /* Decode literal/length + distance code lengths */
    int total = hlit + hdist;
    uint8_t all_lengths[MAX_LIT_LEN + MAX_DIST];
    memset(all_lengths, 0, sizeof(all_lengths));

    int i = 0;
    while (i < total) {
        int sym = huff_decode(br, codelen_table, 7);
        if (sym < 0) return FD_ERROR_BAD_DATA;

        if (sym <= 15) {
            all_lengths[i++] = (uint8_t)sym;
        } else if (sym == 16) {
            /* Repeat previous 3-6 times */
            if (i == 0) return FD_ERROR_BAD_DATA;
            int repeat = br_read(br, 2) + 3;
            uint8_t prev = all_lengths[i - 1];
            for (int j = 0; j < repeat && i < total; j++)
                all_lengths[i++] = prev;
        } else if (sym == 17) {
            /* Repeat 0 for 3-10 times */
            int repeat = br_read(br, 3) + 3;
            for (int j = 0; j < repeat && i < total; j++)
                all_lengths[i++] = 0;
        } else if (sym == 18) {
            /* Repeat 0 for 11-138 times */
            int repeat = br_read(br, 7) + 11;
            for (int j = 0; j < repeat && i < total; j++)
                all_lengths[i++] = 0;
        } else {
            return FD_ERROR_BAD_DATA;
        }
    }

    /* Build litlen and dist tables */
    rc = build_huff_table(litlen_table, litlen_bits, all_lengths, hlit);
    if (rc != FD_OK) return rc;

    rc = build_huff_table(dist_table, dist_bits, all_lengths + hlit, hdist);
    if (rc != FD_OK) return rc;

    return FD_OK;
}

/*
 * fd_inflate - Decompress a raw DEFLATE stream.
 */
int fd_inflate(const uint8_t *src, size_t src_len,
               uint8_t *dst, size_t dst_len,
               size_t *out_len) {
    bitreader_t br;
    br_init(&br, src, src_len);

    size_t out_pos = 0;
    int bfinal;

    /* Table sizes: 15 bits for litlen (32768 entries), 15 bits for dist */
    /* Using 15 bits ensures no subtable is needed */
    static const int LITLEN_BITS = 15;
    static const int DIST_BITS = 15;
    huff_entry_t litlen_table[1 << 15];
    huff_entry_t dist_table[1 << 15];

    do {
        /* Read block header */
        bfinal = br_read(&br, 1);
        int btype = br_read(&br, 2);

        if (btype == 3) {
            return FD_ERROR_BAD_BLOCK;  /* Reserved block type */
        }

        if (btype == 0) {
            /* Non-compressed block */
            br_align_byte(&br);
            uint32_t len  = br_read(&br, 16);
            uint32_t nlen = br_read(&br, 16);

            if ((len ^ nlen) != 0xFFFF) {
                return FD_ERROR_BAD_DATA;
            }

            if (out_pos + len > dst_len) {
                return FD_ERROR_SHORT_BUF;
            }

            for (uint32_t i = 0; i < len; i++) {
                dst[out_pos++] = (uint8_t)br_read(&br, 8);
            }
            continue;
        }

        /* Compressed block (btype 1 or 2) */
        if (btype == 1) {
            /* Fixed Huffman codes */
            uint8_t litlen_lengths[288];
            uint8_t dist_lengths[32];
            build_fixed_litlen_lengths(litlen_lengths);
            build_fixed_dist_lengths(dist_lengths);
            build_huff_table(litlen_table, LITLEN_BITS, litlen_lengths, 288);
            build_huff_table(dist_table, DIST_BITS, dist_lengths, 32);
        } else {
            /* Dynamic Huffman codes (btype == 2) */
            int rc = decode_dynamic_tables(&br, litlen_table, LITLEN_BITS,
                                           dist_table, DIST_BITS);
            if (rc != FD_OK) return rc;
        }

        /* Decode block data */
        for (;;) {
            int sym = huff_decode(&br, litlen_table, LITLEN_BITS);
            if (sym < 0) return FD_ERROR_BAD_DATA;

            if (sym < 256) {
                /* Literal byte */
                if (out_pos >= dst_len) return FD_ERROR_SHORT_BUF;
                dst[out_pos++] = (uint8_t)sym;
            } else if (sym == 256) {
                /* End of block */
                break;
            } else {
                /* Length-distance pair (back-reference) */
                int len_idx = sym - 257;
                if (len_idx >= 29) return FD_ERROR_BAD_DATA;

                uint32_t length = length_base[len_idx] + br_read(&br, length_extra[len_idx]);

                int dist_sym = huff_decode(&br, dist_table, DIST_BITS);
                if (dist_sym < 0 || dist_sym >= 30) return FD_ERROR_BAD_DATA;

                uint32_t distance = dist_base[dist_sym] + br_read(&br, dist_extra[dist_sym]);

                if (distance > out_pos) return FD_ERROR_BAD_DATA;
                if (out_pos + length > dst_len) return FD_ERROR_SHORT_BUF;

                /* Copy from output history (byte-by-byte for overlapping support) */
                size_t src_pos = out_pos - distance;
                for (uint32_t i = 0; i < length; i++) {
                    dst[out_pos++] = dst[src_pos++];
                }
            }
        }

    } while (!bfinal);

    if (out_len) *out_len = out_pos;
    return FD_OK;
}

/* fd_inflate_fast is now in src/fast_decode.c */
