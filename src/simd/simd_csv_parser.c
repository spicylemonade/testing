/*
 * simd_csv_parser.c — SIMD-accelerated RFC 4180 CSV parser
 *
 * Two-phase architecture:
 *   Phase 1: SIMD structural indexing (classify + quote-resolve + extract boundaries)
 *   Phase 2: Field extraction from structural index
 *
 * SIMD techniques:
 *   - AVX2 _mm256_cmpeq_epi8 for structural character classification
 *   - PCLMULQDQ for quote-state parity (prefix-XOR via carry-less multiply)
 *   - popcount + tzcnt for index extraction from bitmasks
 *
 * Build (x86-64):
 *   gcc -O2 -mavx2 -mpclmul -o simd_csv_parser simd_csv_parser.c -lm
 *
 * Usage:
 *   ./simd_csv_parser <csvfile> [--benchmark] [--validate <reference_parser>]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <immintrin.h>
#include <wmmintrin.h>  /* PCLMULQDQ */

/* ================================================================ */
/* Phase 1: SIMD Structural Indexing                                 */
/* ================================================================ */

/*
 * Structural index: arrays of byte offsets for field and record boundaries.
 * A field boundary is a comma (outside quotes) or a record-ending newline.
 * A record boundary is a newline (outside quotes).
 */
typedef struct {
    uint32_t *field_offsets;    /* byte offsets of field-separating commas */
    uint32_t *record_offsets;   /* byte offsets of record-ending newlines */
    size_t n_fields;
    size_t n_records;
    size_t capacity_fields;
    size_t capacity_records;
} structural_index;

static void si_init(structural_index *si, size_t estimated_fields, size_t estimated_records) {
    si->capacity_fields = estimated_fields + 1024;
    si->capacity_records = estimated_records + 1024;
    si->field_offsets = malloc(si->capacity_fields * sizeof(uint32_t));
    si->record_offsets = malloc(si->capacity_records * sizeof(uint32_t));
    si->n_fields = 0;
    si->n_records = 0;
}

static void si_free(structural_index *si) {
    free(si->field_offsets);
    free(si->record_offsets);
}

static inline void si_push_field(structural_index *si, uint32_t offset) {
    if (si->n_fields >= si->capacity_fields) {
        si->capacity_fields *= 2;
        si->field_offsets = realloc(si->field_offsets, si->capacity_fields * sizeof(uint32_t));
    }
    si->field_offsets[si->n_fields++] = offset;
}

static inline void si_push_record(structural_index *si, uint32_t offset) {
    if (si->n_records >= si->capacity_records) {
        si->capacity_records *= 2;
        si->record_offsets = realloc(si->record_offsets, si->capacity_records * sizeof(uint32_t));
    }
    si->record_offsets[si->n_records++] = offset;
}

/*
 * SIMD Phase 1: Process input in 64-byte blocks.
 *
 * For each block:
 * 1. Classify: find positions of , " \r \n using AVX2 cmpeq
 * 2. Quote-resolve: compute inside-quote mask using PCLMULQDQ
 * 3. Mask: remove structural chars that are inside quotes
 * 4. Extract: push field/record offsets from remaining bitmasks
 */
static void phase1_simd_index(const char *input, size_t input_len, structural_index *si) {
    const __m256i comma_vec = _mm256_set1_epi8(',');
    const __m256i quote_vec = _mm256_set1_epi8('"');
    const __m256i cr_vec    = _mm256_set1_epi8('\r');
    const __m256i lf_vec    = _mm256_set1_epi8('\n');

    /* CLMUL constant: multiply by all-ones to compute prefix XOR */
    const __m128i clmul_const = _mm_set_epi64x(0, 0xFFFFFFFFFFFFFFFFULL);

    uint64_t prev_in_string = 0;  /* carry bit from previous block */

    size_t i = 0;
    for (; i + 64 <= input_len; i += 64) {
        /* Load two 32-byte chunks */
        __m256i chunk_lo = _mm256_loadu_si256((const __m256i *)(input + i));
        __m256i chunk_hi = _mm256_loadu_si256((const __m256i *)(input + i + 32));

        /* Classify: produce 32-bit masks for each structural character */
        uint32_t comma_lo = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_lo, comma_vec));
        uint32_t comma_hi = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_hi, comma_vec));
        uint32_t quote_lo = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_lo, quote_vec));
        uint32_t quote_hi = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_hi, quote_vec));
        uint32_t cr_lo    = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_lo, cr_vec));
        uint32_t cr_hi    = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_hi, cr_vec));
        uint32_t lf_lo    = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_lo, lf_vec));
        uint32_t lf_hi    = (uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk_hi, lf_vec));

        /* Combine into 64-bit masks */
        uint64_t comma_bits = ((uint64_t)comma_hi << 32) | comma_lo;
        uint64_t quote_bits = ((uint64_t)quote_hi << 32) | quote_lo;
        uint64_t cr_bits    = ((uint64_t)cr_hi << 32)    | cr_lo;
        uint64_t lf_bits    = ((uint64_t)lf_hi << 32)    | lf_lo;

        /* ---- Quote-state resolution via PCLMULQDQ ---- */
        /*
         * Prefix-XOR of quote_bits gives us an in_string mask:
         * where bit i is 1 if an odd number of quotes precede position i.
         * CLMUL(quote_bits, 0xFFFFFFFFFFFFFFFF) computes this in one instruction.
         * We XOR with the carry from the previous block.
         */
        __m128i quote_128 = _mm_set_epi64x(0, (long long)quote_bits);
        __m128i clmul_result = _mm_clmulepi64_si128(quote_128, clmul_const, 0x00);
        uint64_t in_string = (uint64_t)_mm_extract_epi64(clmul_result, 0);
        in_string ^= prev_in_string;

        /* Update carry: if odd number of quotes in this block, flip carry */
        prev_in_string = (uint64_t)((int64_t)in_string >> 63);  /* broadcast MSB */

        /*
         * Handle escaped quotes (doubled ""):
         * Adjacent quote pairs should not flip the in_string state.
         * The CLMUL approach handles this naturally: "" produces two
         * toggles that cancel out. However, we need to ensure that
         * quote characters inside strings are not treated as structural.
         * The in_string mask already handles this: quotes inside strings
         * are part of the string content.
         */

        /* ---- Mask structural characters inside quotes ---- */
        uint64_t structural_commas = comma_bits & ~in_string;
        uint64_t structural_lf     = lf_bits & ~in_string;
        uint64_t structural_cr     = cr_bits & ~in_string;

        /* Handle CRLF: if CR is followed by LF, treat the LF as the record end */
        /* Remove CR positions where CR is immediately followed by LF */
        uint64_t crlf_pairs = structural_cr & (structural_lf >> 1);
        /* The newline mask is: LF positions (including those after CR) */
        uint64_t newline_bits = structural_lf;
        /* For standalone CR (not followed by LF), add as newline */
        uint64_t standalone_cr = structural_cr & ~(structural_lf >> 1);
        newline_bits |= standalone_cr;

        /* ---- Extract structural positions ---- */
        /* Field boundaries: commas */
        uint64_t fc = structural_commas;
        while (fc) {
            uint64_t bit = fc & (-fc);  /* lowest set bit */
            uint32_t pos = (uint32_t)(i + __builtin_ctzll(fc));
            si_push_field(si, pos);
            fc &= fc - 1;  /* clear lowest set bit */
        }

        /* Record boundaries: newlines */
        uint64_t nl = newline_bits;
        while (nl) {
            uint64_t bit = nl & (-nl);
            uint32_t pos = (uint32_t)(i + __builtin_ctzll(nl));
            si_push_record(si, pos);
            nl &= nl - 1;
        }
    }

    /* ---- Scalar tail processing for remaining bytes ---- */
    /* Simple state machine for bytes not covered by SIMD blocks */
    int in_q = (prev_in_string != 0);  /* carry from SIMD */
    for (; i < input_len; i++) {
        char c = input[i];
        if (c == '"') {
            in_q = !in_q;
        } else if (!in_q) {
            if (c == ',') {
                si_push_field(si, (uint32_t)i);
            } else if (c == '\n') {
                si_push_record(si, (uint32_t)i);
            } else if (c == '\r') {
                if (i + 1 < input_len && input[i + 1] == '\n') {
                    /* CRLF: record boundary at LF position */
                    si_push_record(si, (uint32_t)(i + 1));
                    i++;  /* skip LF */
                } else {
                    si_push_record(si, (uint32_t)i);
                }
            }
        }
    }
}

/* ================================================================ */
/* Phase 2: Field Extraction from Structural Index                   */
/* ================================================================ */

typedef struct {
    size_t total_rows;
    size_t total_fields;
    size_t max_field_len;
    size_t total_field_bytes;
} simd_count_ctx;

/*
 * Phase 2: Walk the structural index to count rows and fields.
 * For benchmarking, we just count; production would extract field data.
 */
static void phase2_extract(const char *input, size_t input_len,
                           const structural_index *si, simd_count_ctx *ctx) {
    ctx->total_rows = 0;
    ctx->total_fields = 0;
    ctx->max_field_len = 0;
    ctx->total_field_bytes = 0;

    /* Merge field and record offsets into a sorted stream */
    size_t fi = 0, ri = 0;
    uint32_t prev_offset = 0;  /* start of current field */
    int field_idx = 0;

    while (fi < si->n_fields || ri < si->n_records) {
        uint32_t next_field = (fi < si->n_fields) ? si->field_offsets[fi] : UINT32_MAX;
        uint32_t next_record = (ri < si->n_records) ? si->record_offsets[ri] : UINT32_MAX;

        if (next_field <= next_record) {
            /* Comma: end of field */
            uint32_t field_len = next_field - prev_offset;
            /* Adjust for quoted fields */
            const char *fstart = input + prev_offset;
            if (field_len > 0 && *fstart == '"') {
                fstart++;
                field_len -= 2;  /* remove opening and closing quotes */
            }
            ctx->total_fields++;
            ctx->total_field_bytes += field_len;
            if (field_len > ctx->max_field_len) ctx->max_field_len = field_len;
            prev_offset = next_field + 1;  /* skip comma */
            field_idx++;
            fi++;
        } else {
            /* Newline: end of field AND end of record */
            uint32_t field_len = next_record - prev_offset;
            /* Handle CRLF: if byte before newline is CR, exclude it */
            if (field_len > 0 && next_record > 0 && input[next_record - 1] == '\r') {
                field_len--;
            }
            const char *fstart = input + prev_offset;
            if (field_len > 0 && *fstart == '"') {
                fstart++;
                field_len -= 2;
            }
            ctx->total_fields++;
            ctx->total_field_bytes += field_len;
            if (field_len > ctx->max_field_len) ctx->max_field_len = field_len;
            field_idx++;
            ctx->total_rows++;
            prev_offset = next_record + 1;  /* skip newline */
            field_idx = 0;
            ri++;
        }
    }

    /* Handle trailing field (no final newline) */
    if (prev_offset < input_len) {
        uint32_t field_len = (uint32_t)(input_len - prev_offset);
        if (field_len > 0) {
            const char *fstart = input + prev_offset;
            if (field_len > 0 && *fstart == '"') {
                field_len -= 2;
            }
            ctx->total_fields++;
            ctx->total_field_bytes += field_len;
            if (field_len > ctx->max_field_len) ctx->max_field_len = field_len;
            ctx->total_rows++;
        }
    }
}

/* ================================================================ */
/* Memory-mapped I/O                                                 */
/* ================================================================ */

static char *mmap_file(const char *path, size_t *out_size) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) { perror("open"); return NULL; }
    struct stat st;
    if (fstat(fd, &st) < 0) { perror("fstat"); close(fd); return NULL; }
    *out_size = (size_t)st.st_size;
    if (*out_size == 0) { close(fd); return (char *)calloc(1, 1); }
    /* Allocate extra 64 bytes for SIMD overread safety */
    char *data = mmap(NULL, *out_size + 64, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    if (data == MAP_FAILED) { perror("mmap"); return NULL; }
    return data;
}

static void munmap_file(char *data, size_t size) {
    if (data && size > 0) munmap(data, size + 64);
}

static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/* ================================================================ */
/* Main                                                              */
/* ================================================================ */

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <csvfile> [--benchmark] [--phase1-only]\n", argv[0]);
        return 1;
    }

    const char *filepath = argv[1];
    int benchmark = 0, phase1_only = 0;
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--benchmark") == 0) benchmark = 1;
        if (strcmp(argv[i], "--phase1-only") == 0) phase1_only = 1;
    }

    size_t file_size;
    char *data = mmap_file(filepath, &file_size);
    if (!data) return 1;

    int n_runs = benchmark ? 5 : 1;

    /* Phase 1 benchmark */
    double best_phase1 = 1e30;
    structural_index si;

    for (int run = 0; run < n_runs; run++) {
        si_init(&si, file_size / 8, file_size / 80);
        double t0 = now_sec();
        phase1_simd_index(data, file_size, &si);
        double elapsed = now_sec() - t0;
        if (elapsed < best_phase1) best_phase1 = elapsed;
        if (run < n_runs - 1) si_free(&si);
    }

    double phase1_mbs = (file_size / (1024.0 * 1024.0)) / best_phase1;

    if (phase1_only) {
        printf("{\"parser\":\"simd_phase1\",\"file\":\"%s\","
               "\"file_size_bytes\":%zu,\"field_boundaries\":%zu,"
               "\"record_boundaries\":%zu,"
               "\"best_time_sec\":%.6f,\"throughput_mb_per_sec\":%.2f}\n",
               filepath, file_size, si.n_fields, si.n_records,
               best_phase1, phase1_mbs);
        si_free(&si);
        munmap_file(data, file_size);
        return 0;
    }

    /* Phase 2 benchmark */
    double best_total = 1e30;
    simd_count_ctx ctx = {0};

    for (int run = 0; run < n_runs; run++) {
        structural_index si2;
        si_init(&si2, file_size / 8, file_size / 80);

        double t0 = now_sec();
        phase1_simd_index(data, file_size, &si2);
        phase2_extract(data, file_size, &si2, &ctx);
        double elapsed = now_sec() - t0;

        if (elapsed < best_total) best_total = elapsed;
        si_free(&si2);
    }

    double total_mbs = (file_size / (1024.0 * 1024.0)) / best_total;
    double rows_per_sec = ctx.total_rows / best_total;

    if (benchmark) {
        printf("{\"parser\":\"simd_csv\",\"file\":\"%s\","
               "\"file_size_bytes\":%zu,\"rows\":%zu,\"fields\":%zu,"
               "\"phase1_time_sec\":%.6f,\"phase1_throughput_mb_per_sec\":%.2f,"
               "\"total_time_sec\":%.6f,\"throughput_mb_per_sec\":%.2f,"
               "\"rows_per_sec\":%.0f,\"max_field_len\":%zu,"
               "\"avg_field_bytes\":%.1f}\n",
               filepath, file_size, ctx.total_rows, ctx.total_fields,
               best_phase1, phase1_mbs,
               best_total, total_mbs, rows_per_sec,
               ctx.max_field_len,
               ctx.total_fields > 0 ? (double)ctx.total_field_bytes / ctx.total_fields : 0);
    } else {
        printf("File: %s\n", filepath);
        printf("Size: %.2f MB\n", file_size / (1024.0 * 1024.0));
        printf("Phase 1 (indexing): %.4f sec, %.2f MB/s\n", best_phase1, phase1_mbs);
        printf("  Field boundaries: %zu\n", si.n_fields);
        printf("  Record boundaries: %zu\n", si.n_records);
        printf("Total (Phase 1 + 2): %.4f sec, %.2f MB/s\n", best_total, total_mbs);
        printf("Rows: %zu\n", ctx.total_rows);
        printf("Fields: %zu\n", ctx.total_fields);
        printf("Rows/sec: %.0f\n", rows_per_sec);
    }

    si_free(&si);
    munmap_file(data, file_size);
    return 0;
}
