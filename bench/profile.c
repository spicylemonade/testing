/*
 * profile.c - Instrumented profiler for naive DEFLATE decoder
 *
 * Measures time breakdown across decoding phases:
 *   - Table construction (Huffman table build)
 *   - Huffman symbol decoding (the hot loop)
 *   - LZ77 back-reference copies
 *   - Bit reader refills
 *   - Literal output
 *
 * Also counts key events: symbols decoded, branches, refills, etc.
 *
 * Usage: ./profiler <deflate_file> <original_size> [iterations]
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

/* ========================================================================== */
/*  Instrumented copy of the naive decoder with timing hooks                  */
/* ========================================================================== */

#define MAX_BITS       15
#define MAX_LIT_LEN    286
#define MAX_DIST       30
#define MAX_CODE_LEN   19

typedef struct {
    uint16_t symbol;
    uint16_t length;
} huff_entry_t;

typedef struct {
    const uint8_t *data;
    size_t         data_len;
    size_t         byte_pos;
    int            bit_pos;
    uint32_t       buffer;
    int            bits_avail;
} bitreader_t;

/* Profiling counters */
typedef struct {
    /* Time accumulators (nanoseconds) */
    uint64_t time_table_build_ns;
    uint64_t time_huff_decode_ns;
    uint64_t time_lz77_copy_ns;
    uint64_t time_bitreader_ns;
    uint64_t time_total_ns;

    /* Event counters */
    uint64_t n_symbols_decoded;
    uint64_t n_literals;
    uint64_t n_backrefs;
    uint64_t n_backref_bytes;
    uint64_t n_refills;
    uint64_t n_table_builds;
    uint64_t n_blocks;
    uint64_t n_dynamic_blocks;
    uint64_t n_fixed_blocks;
    uint64_t n_stored_blocks;

    /* Branch stats */
    uint64_t n_literal_branches;
    uint64_t n_eof_branches;
    uint64_t n_backref_branches;

    /* Derived (computed after) */
    double   cycles_per_symbol;    /* estimated */
    double   pct_table_build;
    double   pct_huff_decode;
    double   pct_lz77_copy;
    double   pct_bitreader;
} profile_counters_t;

static inline uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

/* ---- Bit reader ---- */
static void br_init(bitreader_t *br, const uint8_t *data, size_t len) {
    br->data = data;
    br->data_len = len;
    br->byte_pos = 0;
    br->bit_pos = 0;
    br->buffer = 0;
    br->bits_avail = 0;
}

static int br_refill(bitreader_t *br, profile_counters_t *pc) {
    pc->n_refills++;
    while (br->bits_avail <= 24 && br->byte_pos < br->data_len) {
        br->buffer |= (uint32_t)br->data[br->byte_pos++] << br->bits_avail;
        br->bits_avail += 8;
    }
    return br->bits_avail > 0;
}

static uint32_t br_peek(bitreader_t *br, int n, profile_counters_t *pc) {
    if (br->bits_avail < n) br_refill(br, pc);
    return br->buffer & ((1u << n) - 1);
}

static void br_consume(bitreader_t *br, int n) {
    br->buffer >>= n;
    br->bits_avail -= n;
}

static uint32_t br_read(bitreader_t *br, int n, profile_counters_t *pc) {
    if (n == 0) return 0;
    br_refill(br, pc);
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

static int build_huff_table(huff_entry_t *table, int table_bits,
                            const uint8_t *lengths, int num_symbols) {
    int bl_count[MAX_BITS + 1] = {0};
    int next_code[MAX_BITS + 1];
    int code;
    for (int i = 0; i < num_symbols; i++) {
        if (lengths[i] > MAX_BITS) return -1;
        bl_count[lengths[i]]++;
    }
    bl_count[0] = 0;
    code = 0;
    for (int bits = 1; bits <= MAX_BITS; bits++) {
        code = (code + bl_count[bits - 1]) << 1;
        next_code[bits] = code;
    }
    int table_size = 1 << table_bits;
    for (int i = 0; i < table_size; i++) {
        table[i].symbol = 0xFFFF;
        table[i].length = 0;
    }
    for (int sym = 0; sym < num_symbols; sym++) {
        int len = lengths[sym];
        if (len == 0) continue;
        int c = next_code[len]++;
        int reversed = 0;
        for (int b = 0; b < len; b++)
            reversed |= ((c >> (len - 1 - b)) & 1) << b;
        if (len <= table_bits) {
            int fill = 1 << len;
            for (int idx = reversed; idx < table_size; idx += fill) {
                table[idx].symbol = (uint16_t)sym;
                table[idx].length = (uint16_t)len;
            }
        }
    }
    return 0;
}

static void build_fixed_litlen_lengths(uint8_t *lengths) {
    for (int i = 0;   i <= 143; i++) lengths[i] = 8;
    for (int i = 144; i <= 255; i++) lengths[i] = 9;
    for (int i = 256; i <= 279; i++) lengths[i] = 7;
    for (int i = 280; i <= 287; i++) lengths[i] = 8;
}
static void build_fixed_dist_lengths(uint8_t *lengths) {
    for (int i = 0; i < 32; i++) lengths[i] = 5;
}

static int profiled_inflate(const uint8_t *src, size_t src_len,
                            uint8_t *dst, size_t dst_len,
                            size_t *out_len,
                            profile_counters_t *pc) {
    memset(pc, 0, sizeof(*pc));
    uint64_t t_total_start = now_ns();

    bitreader_t br;
    br_init(&br, src, src_len);
    size_t out_pos = 0;
    int bfinal;

    static const int LITLEN_BITS = 15;
    static const int DIST_BITS = 15;
    huff_entry_t litlen_table[1 << 15];
    huff_entry_t dist_table[1 << 15];

    do {
        bfinal = br_read(&br, 1, pc);
        int btype = br_read(&br, 2, pc);
        pc->n_blocks++;

        if (btype == 3) return -1;

        if (btype == 0) {
            pc->n_stored_blocks++;
            br_align_byte(&br);
            uint32_t len  = br_read(&br, 16, pc);
            uint32_t nlen = br_read(&br, 16, pc);
            if ((len ^ nlen) != 0xFFFF) return -1;
            if (out_pos + len > dst_len) return -1;
            for (uint32_t i = 0; i < len; i++)
                dst[out_pos++] = (uint8_t)br_read(&br, 8, pc);
            continue;
        }

        /* Table build timing */
        uint64_t t_tb = now_ns();
        if (btype == 1) {
            pc->n_fixed_blocks++;
            uint8_t ll[288], dl[32];
            build_fixed_litlen_lengths(ll);
            build_fixed_dist_lengths(dl);
            build_huff_table(litlen_table, LITLEN_BITS, ll, 288);
            build_huff_table(dist_table, DIST_BITS, dl, 32);
        } else {
            pc->n_dynamic_blocks++;
            /* Inline dynamic table decode */
            int hlit  = br_read(&br, 5, pc) + 257;
            int hdist = br_read(&br, 5, pc) + 1;
            int hclen = br_read(&br, 4, pc) + 4;
            if (hlit > 286 || hdist > 30) return -1;
            uint8_t cl_lengths[MAX_CODE_LEN] = {0};
            for (int i = 0; i < hclen; i++)
                cl_lengths[codelen_order[i]] = (uint8_t)br_read(&br, 3, pc);
            huff_entry_t cl_table[128];
            if (build_huff_table(cl_table, 7, cl_lengths, MAX_CODE_LEN) != 0) return -1;
            int total = hlit + hdist;
            uint8_t all_lengths[MAX_LIT_LEN + MAX_DIST];
            memset(all_lengths, 0, sizeof(all_lengths));
            int i = 0;
            while (i < total) {
                br_refill(&br, pc);
                uint32_t idx = br_peek(&br, 7, pc);
                huff_entry_t e = cl_table[idx];
                if (e.length == 0 || e.symbol == 0xFFFF) return -1;
                br_consume(&br, e.length);
                int sym = e.symbol;
                if (sym <= 15) {
                    all_lengths[i++] = (uint8_t)sym;
                } else if (sym == 16) {
                    if (i == 0) return -1;
                    int rep = br_read(&br, 2, pc) + 3;
                    uint8_t prev = all_lengths[i-1];
                    for (int j = 0; j < rep && i < total; j++)
                        all_lengths[i++] = prev;
                } else if (sym == 17) {
                    int rep = br_read(&br, 3, pc) + 3;
                    for (int j = 0; j < rep && i < total; j++)
                        all_lengths[i++] = 0;
                } else if (sym == 18) {
                    int rep = br_read(&br, 7, pc) + 11;
                    for (int j = 0; j < rep && i < total; j++)
                        all_lengths[i++] = 0;
                } else return -1;
            }
            if (build_huff_table(litlen_table, LITLEN_BITS, all_lengths, hlit) != 0) return -1;
            if (build_huff_table(dist_table, DIST_BITS, all_lengths + hlit, hdist) != 0) return -1;
        }
        pc->n_table_builds++;
        pc->time_table_build_ns += now_ns() - t_tb;

        /* Decode block data */
        for (;;) {
            /* Huffman decode */
            uint64_t t_hd = now_ns();
            br_refill(&br, pc);
            uint32_t idx = br_peek(&br, LITLEN_BITS, pc);
            huff_entry_t entry = litlen_table[idx];
            if (entry.length == 0 || entry.symbol == 0xFFFF) return -1;
            br_consume(&br, entry.length);
            int sym = entry.symbol;
            pc->n_symbols_decoded++;
            pc->time_huff_decode_ns += now_ns() - t_hd;

            if (sym < 256) {
                pc->n_literals++;
                pc->n_literal_branches++;
                if (out_pos >= dst_len) return -1;
                dst[out_pos++] = (uint8_t)sym;
            } else if (sym == 256) {
                pc->n_eof_branches++;
                break;
            } else {
                pc->n_backrefs++;
                pc->n_backref_branches++;
                int len_idx = sym - 257;
                if (len_idx >= 29) return -1;

                uint64_t t_br = now_ns();
                uint32_t length = length_base[len_idx] + br_read(&br, length_extra[len_idx], pc);
                pc->time_bitreader_ns += now_ns() - t_br;

                /* Decode distance */
                t_hd = now_ns();
                br_refill(&br, pc);
                idx = br_peek(&br, DIST_BITS, pc);
                huff_entry_t dentry = dist_table[idx];
                if (dentry.length == 0 || dentry.symbol == 0xFFFF) return -1;
                br_consume(&br, dentry.length);
                int dist_sym = dentry.symbol;
                pc->time_huff_decode_ns += now_ns() - t_hd;

                if (dist_sym >= 30) return -1;

                t_br = now_ns();
                uint32_t distance = dist_base[dist_sym] + br_read(&br, dist_extra[dist_sym], pc);
                pc->time_bitreader_ns += now_ns() - t_br;

                if (distance > out_pos || out_pos + length > dst_len) return -1;

                /* LZ77 copy */
                uint64_t t_copy = now_ns();
                size_t src_pos = out_pos - distance;
                for (uint32_t ci = 0; ci < length; ci++)
                    dst[out_pos++] = dst[src_pos++];
                pc->time_lz77_copy_ns += now_ns() - t_copy;
                pc->n_backref_bytes += length;
            }
        }
    } while (!bfinal);

    pc->time_total_ns = now_ns() - t_total_start;
    if (out_len) *out_len = out_pos;

    /* Compute derived metrics */
    if (pc->time_total_ns > 0) {
        pc->pct_table_build = 100.0 * pc->time_table_build_ns / pc->time_total_ns;
        pc->pct_huff_decode = 100.0 * pc->time_huff_decode_ns / pc->time_total_ns;
        pc->pct_lz77_copy   = 100.0 * pc->time_lz77_copy_ns / pc->time_total_ns;
        pc->pct_bitreader   = 100.0 * pc->time_bitreader_ns / pc->time_total_ns;
    }

    return 0;
}

/* ========================================================================== */
/*                              Main                                          */
/* ========================================================================== */

static uint8_t *read_file(const char *path, size_t *len) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    if (sz <= 0) { fclose(f); return NULL; }
    fseek(f, 0, SEEK_SET);
    uint8_t *buf = malloc((size_t)sz);
    if (!buf) { fclose(f); return NULL; }
    size_t rd = fread(buf, 1, (size_t)sz, f);
    fclose(f);
    if (rd != (size_t)sz) { free(buf); return NULL; }
    *len = (size_t)sz;
    return buf;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <deflate_file> <original_size> [iterations]\n", argv[0]);
        return 1;
    }

    const char *filepath = argv[1];
    size_t orig_size = (size_t)atol(argv[2]);
    int iterations = argc >= 4 ? atoi(argv[3]) : 10;

    size_t comp_len = 0;
    uint8_t *compressed = read_file(filepath, &comp_len);
    if (!compressed) {
        fprintf(stderr, "Cannot read %s\n", filepath);
        return 1;
    }

    uint8_t *output = malloc(orig_size + 64);
    if (!output) { free(compressed); return 1; }

    printf("=== DEFLATE Decoder Profile ===\n");
    printf("File: %s\n", filepath);
    printf("Compressed: %zu bytes, Original: %zu bytes (ratio: %.1f%%)\n",
           comp_len, orig_size, 100.0 * comp_len / orig_size);
    printf("Iterations: %d\n\n", iterations);

    /* Accumulate profiling across iterations */
    profile_counters_t total;
    memset(&total, 0, sizeof(total));

    for (int iter = 0; iter < iterations; iter++) {
        profile_counters_t pc;
        size_t out_len = 0;
        int rc = profiled_inflate(compressed, comp_len, output, orig_size + 64,
                                  &out_len, &pc);
        if (rc != 0) {
            fprintf(stderr, "Decode error at iteration %d\n", iter);
            free(compressed); free(output);
            return 1;
        }

        total.time_table_build_ns += pc.time_table_build_ns;
        total.time_huff_decode_ns += pc.time_huff_decode_ns;
        total.time_lz77_copy_ns   += pc.time_lz77_copy_ns;
        total.time_bitreader_ns   += pc.time_bitreader_ns;
        total.time_total_ns       += pc.time_total_ns;
        total.n_symbols_decoded   += pc.n_symbols_decoded;
        total.n_literals          += pc.n_literals;
        total.n_backrefs          += pc.n_backrefs;
        total.n_backref_bytes     += pc.n_backref_bytes;
        total.n_refills           += pc.n_refills;
        total.n_table_builds      += pc.n_table_builds;
        total.n_blocks            += pc.n_blocks;
        total.n_dynamic_blocks    += pc.n_dynamic_blocks;
        total.n_fixed_blocks      += pc.n_fixed_blocks;
        total.n_stored_blocks     += pc.n_stored_blocks;
        total.n_literal_branches  += pc.n_literal_branches;
        total.n_eof_branches      += pc.n_eof_branches;
        total.n_backref_branches  += pc.n_backref_branches;
    }

    /* Print per-iteration averages */
    double div = (double)iterations;
    printf("=== Time Breakdown (per iteration average) ===\n");
    printf("  Total time:      %10.3f ms\n",  total.time_total_ns / div / 1e6);
    printf("  Table build:     %10.3f ms  (%5.1f%%)\n",
           total.time_table_build_ns / div / 1e6,
           100.0 * total.time_table_build_ns / total.time_total_ns);
    printf("  Huffman decode:  %10.3f ms  (%5.1f%%)\n",
           total.time_huff_decode_ns / div / 1e6,
           100.0 * total.time_huff_decode_ns / total.time_total_ns);
    printf("  LZ77 copy:       %10.3f ms  (%5.1f%%)\n",
           total.time_lz77_copy_ns / div / 1e6,
           100.0 * total.time_lz77_copy_ns / total.time_total_ns);
    printf("  Extra bit reads: %10.3f ms  (%5.1f%%)\n",
           total.time_bitreader_ns / div / 1e6,
           100.0 * total.time_bitreader_ns / total.time_total_ns);
    double accounted = total.time_table_build_ns + total.time_huff_decode_ns +
                       total.time_lz77_copy_ns + total.time_bitreader_ns;
    double overhead = total.time_total_ns - accounted;
    printf("  Overhead/other:  %10.3f ms  (%5.1f%%)\n",
           overhead / div / 1e6,
           100.0 * overhead / total.time_total_ns);

    printf("\n=== Event Counters (per iteration average) ===\n");
    printf("  Symbols decoded: %12.0f\n", total.n_symbols_decoded / div);
    printf("  Literals:        %12.0f  (%5.1f%% of symbols)\n",
           total.n_literals / div,
           100.0 * total.n_literals / total.n_symbols_decoded);
    printf("  Back-references: %12.0f  (%5.1f%% of symbols)\n",
           total.n_backrefs / div,
           100.0 * total.n_backrefs / total.n_symbols_decoded);
    printf("  Backref bytes:   %12.0f  (avg len: %.1f)\n",
           total.n_backref_bytes / div,
           total.n_backrefs > 0 ? (double)total.n_backref_bytes / total.n_backrefs : 0);
    printf("  Bit refills:     %12.0f  (%.1f per symbol)\n",
           total.n_refills / div,
           (double)total.n_refills / total.n_symbols_decoded);
    printf("  Table builds:    %12.0f\n", total.n_table_builds / div);
    printf("  Blocks:          %12.0f  (dyn=%0.f, fixed=%0.f, stored=%0.f)\n",
           total.n_blocks / div,
           total.n_dynamic_blocks / div,
           total.n_fixed_blocks / div,
           total.n_stored_blocks / div);

    printf("\n=== Performance ===\n");
    double throughput = ((double)orig_size / (1024.0*1024.0)) /
                        (total.time_total_ns / div / 1e9);
    printf("  Throughput:     %8.1f MB/s\n", throughput);
    double ns_per_sym = (double)total.time_total_ns / total.n_symbols_decoded;
    printf("  Time/symbol:    %8.1f ns\n", ns_per_sym);

    /* Estimate cycles at ~3.5 GHz (typical) */
    double est_ghz = 3.5;
    double cycles_per_sym = ns_per_sym * est_ghz;
    printf("  Cycles/symbol:  %8.1f (est @ %.1f GHz)\n", cycles_per_sym, est_ghz);
    double ns_per_huff = (double)total.time_huff_decode_ns / total.n_symbols_decoded;
    printf("  Huff ns/symbol: %8.1f ns  (%.1f est cycles)\n",
           ns_per_huff, ns_per_huff * est_ghz);

    free(compressed);
    free(output);
    return 0;
}
