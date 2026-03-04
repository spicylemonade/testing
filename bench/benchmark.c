/*
 * benchmark.c - Rigorous benchmarking harness for DEFLATE decompressors
 *
 * Compares throughput of:
 *   1. Our naive baseline (fd_inflate)
 *   2. System zlib (inflate)
 *   3. zlib-ng (via direct linking)
 *   4. libdeflate (libdeflate_deflate_decompress)
 *   5. Our fast decoder (fd_inflate_fast) — when available
 *
 * Statistical methodology:
 *   - Warmup iterations discarded
 *   - Reports: median, mean, p5, p95, stddev
 *   - Uses CLOCK_MONOTONIC for wall-clock timing
 *   - Supports CPU pinning via taskset (external)
 *
 * Usage: ./bench_harness <corpus_dir> <iterations> <output_json>
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <dirent.h>
#include <sys/stat.h>
#include <errno.h>
#include <zlib.h>

#include "fast_deflate.h"

/* libdeflate (built from source) */
#include "libdeflate.h"

/* ========================================================================== */
/*                          Timing infrastructure                             */
/* ========================================================================== */

static inline double time_now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

/* ========================================================================== */
/*                           Statistical helpers                              */
/* ========================================================================== */

static int cmp_double(const void *a, const void *b) {
    double da = *(const double *)a;
    double db = *(const double *)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

typedef struct {
    double median;
    double mean;
    double p5;
    double p95;
    double stddev;
    double min;
    double max;
} stats_t;

static stats_t compute_stats(double *samples, int n) {
    stats_t s = {0};
    if (n <= 0) return s;

    qsort(samples, n, sizeof(double), cmp_double);

    /* Median */
    if (n % 2 == 0)
        s.median = (samples[n/2 - 1] + samples[n/2]) / 2.0;
    else
        s.median = samples[n/2];

    /* Mean */
    double sum = 0;
    for (int i = 0; i < n; i++) sum += samples[i];
    s.mean = sum / n;

    /* Stddev */
    double sum_sq = 0;
    for (int i = 0; i < n; i++) {
        double diff = samples[i] - s.mean;
        sum_sq += diff * diff;
    }
    s.stddev = sqrt(sum_sq / n);

    /* Percentiles (nearest-rank method) */
    int p5_idx  = (int)(0.05 * n);
    int p95_idx = (int)(0.95 * n);
    if (p5_idx < 0) p5_idx = 0;
    if (p95_idx >= n) p95_idx = n - 1;
    s.p5  = samples[p5_idx];
    s.p95 = samples[p95_idx];
    s.min = samples[0];
    s.max = samples[n - 1];

    return s;
}

/* ========================================================================== */
/*                         File I/O helpers                                   */
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

/* ========================================================================== */
/*                        Decoder wrappers                                    */
/* ========================================================================== */

/* Each decoder function: returns 0 on success, -1 on failure.
 * out_len is set to actual decompressed size. */

typedef int (*decoder_fn)(const uint8_t *src, size_t src_len,
                          uint8_t *dst, size_t dst_cap, size_t *out_len);

/* 1. Our naive baseline */
static int decode_naive(const uint8_t *src, size_t src_len,
                        uint8_t *dst, size_t dst_cap, size_t *out_len) {
    int rc = fd_inflate(src, src_len, dst, dst_cap, out_len);
    return (rc == FD_OK) ? 0 : -1;
}

/* 2. System zlib */
static int decode_zlib(const uint8_t *src, size_t src_len,
                       uint8_t *dst, size_t dst_cap, size_t *out_len) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    /* -15 = raw deflate (no zlib/gzip header) */
    if (inflateInit2(&strm, -15) != Z_OK) return -1;

    strm.next_in  = (Bytef *)src;
    strm.avail_in = (uInt)src_len;
    strm.next_out = (Bytef *)dst;
    strm.avail_out = (uInt)dst_cap;

    int ret = inflate(&strm, Z_FINISH);
    *out_len = strm.total_out;
    inflateEnd(&strm);

    return (ret == Z_STREAM_END) ? 0 : -1;
}

/* 3. zlib-ng — using the same zlib-compat API but linked separately.
 *    We'll call it through function pointers loaded at init time
 *    to avoid symbol conflicts. For now, if compiled with HAVE_ZLIB_NG,
 *    we use the zlib-ng symbols directly. Otherwise, we skip it.
 *
 *    Since zlib-ng is built with --zlib-compat, its symbols are the same
 *    as zlib's. We handle this by loading it via dlopen at runtime.
 */
#include <dlfcn.h>

typedef int (*zlibng_inflateInit2_fn)(z_streamp, int, const char *, int);
typedef int (*zlibng_inflate_fn)(z_streamp, int);
typedef int (*zlibng_inflateEnd_fn)(z_streamp);

static void *zlibng_handle = NULL;
static zlibng_inflateInit2_fn zlibng_inflateInit2_ = NULL;
static zlibng_inflate_fn      zlibng_inflate      = NULL;
static zlibng_inflateEnd_fn   zlibng_inflateEnd   = NULL;

static int init_zlibng(const char *sopath) {
    zlibng_handle = dlopen(sopath, RTLD_NOW | RTLD_LOCAL);
    if (!zlibng_handle) {
        fprintf(stderr, "Warning: cannot load zlib-ng from %s: %s\n",
                sopath, dlerror());
        return -1;
    }
    zlibng_inflateInit2_ = (zlibng_inflateInit2_fn)dlsym(zlibng_handle, "inflateInit2_");
    zlibng_inflate       = (zlibng_inflate_fn)dlsym(zlibng_handle, "inflate");
    zlibng_inflateEnd    = (zlibng_inflateEnd_fn)dlsym(zlibng_handle, "inflateEnd");
    if (!zlibng_inflateInit2_ || !zlibng_inflate || !zlibng_inflateEnd) {
        fprintf(stderr, "Warning: missing symbols in zlib-ng .so\n");
        dlclose(zlibng_handle);
        zlibng_handle = NULL;
        return -1;
    }
    return 0;
}

static int decode_zlibng(const uint8_t *src, size_t src_len,
                         uint8_t *dst, size_t dst_cap, size_t *out_len) {
    if (!zlibng_handle) return -1;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    int rc = zlibng_inflateInit2_(&strm, -15, ZLIB_VERSION, (int)sizeof(z_stream));
    if (rc != Z_OK) return -1;

    strm.next_in  = (Bytef *)src;
    strm.avail_in = (uInt)src_len;
    strm.next_out = (Bytef *)dst;
    strm.avail_out = (uInt)dst_cap;

    int ret = zlibng_inflate(&strm, Z_FINISH);
    *out_len = strm.total_out;
    zlibng_inflateEnd(&strm);

    return (ret == Z_STREAM_END) ? 0 : -1;
}

/* 4. libdeflate */
static struct libdeflate_decompressor *ld_decompressor = NULL;

static int decode_libdeflate(const uint8_t *src, size_t src_len,
                             uint8_t *dst, size_t dst_cap, size_t *out_len) {
    if (!ld_decompressor) return -1;

    enum libdeflate_result r =
        libdeflate_deflate_decompress(ld_decompressor,
                                      src, src_len,
                                      dst, dst_cap,
                                      out_len);
    return (r == LIBDEFLATE_SUCCESS) ? 0 : -1;
}

/* 5. Our fast decoder */
static int decode_fast(const uint8_t *src, size_t src_len,
                       uint8_t *dst, size_t dst_cap, size_t *out_len) {
    int rc = fd_inflate_fast(src, src_len, dst, dst_cap, out_len);
    return (rc == FD_OK) ? 0 : -1;
}

/* ========================================================================== */
/*                          Benchmark core                                    */
/* ========================================================================== */

typedef struct {
    char name[64];
    decoder_fn fn;
    int available;
} decoder_entry_t;

#define MAX_DECODERS 5

static decoder_entry_t decoders[MAX_DECODERS] = {
    { "naive",      decode_naive,      1 },
    { "zlib",       decode_zlib,       1 },
    { "zlib-ng",    decode_zlibng,     0 },  /* set at init */
    { "libdeflate", decode_libdeflate, 0 },  /* set at init */
    { "fast",       decode_fast,       1 },  /* enabled: fd_inflate_fast */
};

#define MAX_CORPUS_FILES 100
#define WARMUP_ITERS     5

typedef struct {
    char filename[256];
    char basename[256];
    int  level;
    size_t compressed_size;
    size_t original_size;
} corpus_file_t;

typedef struct {
    char decoder_name[64];
    char filename[256];
    int  level;
    size_t original_size;
    size_t compressed_size;
    stats_t throughput_stats;  /* MB/s of decompressed output */
    int valid;                 /* correctness check passed */
} bench_result_t;

static int run_single_bench(decoder_fn fn,
                            const uint8_t *compressed, size_t comp_len,
                            const uint8_t *expected, size_t orig_len,
                            int iterations,
                            stats_t *out_stats, int *out_valid) {
    uint8_t *outbuf = malloc(orig_len + 64);  /* small padding */
    if (!outbuf) return -1;

    double *throughputs = malloc(sizeof(double) * iterations);
    if (!throughputs) { free(outbuf); return -1; }

    *out_valid = 1;

    /* Warmup */
    for (int i = 0; i < WARMUP_ITERS; i++) {
        size_t out_len = 0;
        int rc = fn(compressed, comp_len, outbuf, orig_len + 64, &out_len);
        if (rc != 0 || out_len != orig_len) {
            *out_valid = 0;
            free(outbuf);
            free(throughputs);
            return -1;
        }
    }

    /* Verify correctness once */
    {
        size_t out_len = 0;
        fn(compressed, comp_len, outbuf, orig_len + 64, &out_len);
        if (out_len != orig_len || memcmp(outbuf, expected, orig_len) != 0) {
            *out_valid = 0;
            free(outbuf);
            free(throughputs);
            return -1;
        }
    }

    /* Timed iterations */
    for (int i = 0; i < iterations; i++) {
        size_t out_len = 0;
        double t0 = time_now();
        fn(compressed, comp_len, outbuf, orig_len + 64, &out_len);
        double t1 = time_now();
        double elapsed = t1 - t0;
        if (elapsed < 1e-9) elapsed = 1e-9;  /* avoid div-by-zero */
        throughputs[i] = ((double)orig_len / (1024.0 * 1024.0)) / elapsed;
    }

    *out_stats = compute_stats(throughputs, iterations);
    free(outbuf);
    free(throughputs);
    return 0;
}

/* ========================================================================== */
/*                          Corpus scanning                                   */
/* ========================================================================== */

/* Find .deflate.lN files and their originals */
static int scan_corpus(const char *dir, corpus_file_t *files, int max_files) {
    DIR *d = opendir(dir);
    if (!d) {
        fprintf(stderr, "Cannot open corpus dir: %s\n", dir);
        return 0;
    }

    int count = 0;
    struct dirent *ent;
    while ((ent = readdir(d)) != NULL && count < max_files) {
        /* Look for .deflate.l{1,6,9} files */
        const char *name = ent->d_name;
        char *deflate_pos = strstr(name, ".deflate.l");
        if (!deflate_pos) continue;

        /* Extract level */
        int level = atoi(deflate_pos + 10);
        if (level != 1 && level != 6 && level != 9) continue;

        /* Extract base name */
        size_t base_len = (size_t)(deflate_pos - name);
        if (base_len >= sizeof(files[0].basename)) continue;

        corpus_file_t *cf = &files[count];
        snprintf(cf->filename, sizeof(cf->filename), "%s/%s", dir, name);
        memcpy(cf->basename, name, base_len);
        cf->basename[base_len] = '\0';
        cf->level = level;

        /* Get compressed size */
        struct stat st;
        if (stat(cf->filename, &st) != 0) continue;
        cf->compressed_size = (size_t)st.st_size;

        /* Get original size */
        char orig_path[512];
        snprintf(orig_path, sizeof(orig_path), "%s/%s", dir, cf->basename);
        if (stat(orig_path, &st) != 0) continue;
        cf->original_size = (size_t)st.st_size;

        count++;
    }
    closedir(d);
    return count;
}

/* ========================================================================== */
/*                           JSON output                                      */
/* ========================================================================== */

static void write_results_json(const char *path,
                                bench_result_t *results, int nresults,
                                int iterations) {
    FILE *f = fopen(path, "w");
    if (!f) {
        fprintf(stderr, "Cannot write results to %s\n", path);
        return;
    }

    fprintf(f, "{\n");
    fprintf(f, "  \"benchmark_config\": {\n");
    fprintf(f, "    \"iterations\": %d,\n", iterations);
    fprintf(f, "    \"warmup_iterations\": %d,\n", WARMUP_ITERS);

    /* Get timestamp */
    time_t now = time(NULL);
    char timebuf[64];
    strftime(timebuf, sizeof(timebuf), "%Y-%m-%dT%H:%M:%SZ", gmtime(&now));
    fprintf(f, "    \"timestamp\": \"%s\"\n", timebuf);
    fprintf(f, "  },\n");

    fprintf(f, "  \"results\": [\n");
    for (int i = 0; i < nresults; i++) {
        bench_result_t *r = &results[i];
        fprintf(f, "    {\n");
        fprintf(f, "      \"decoder\": \"%s\",\n", r->decoder_name);
        fprintf(f, "      \"file\": \"%s\",\n", r->filename);
        fprintf(f, "      \"compression_level\": %d,\n", r->level);
        fprintf(f, "      \"original_size\": %zu,\n", r->original_size);
        fprintf(f, "      \"compressed_size\": %zu,\n", r->compressed_size);
        fprintf(f, "      \"correct\": %s,\n", r->valid ? "true" : "false");
        fprintf(f, "      \"throughput_MBps\": {\n");
        fprintf(f, "        \"median\": %.2f,\n", r->throughput_stats.median);
        fprintf(f, "        \"mean\": %.2f,\n", r->throughput_stats.mean);
        fprintf(f, "        \"p5\": %.2f,\n", r->throughput_stats.p5);
        fprintf(f, "        \"p95\": %.2f,\n", r->throughput_stats.p95);
        fprintf(f, "        \"stddev\": %.2f,\n", r->throughput_stats.stddev);
        fprintf(f, "        \"min\": %.2f,\n", r->throughput_stats.min);
        fprintf(f, "        \"max\": %.2f\n", r->throughput_stats.max);
        fprintf(f, "      }\n");
        fprintf(f, "    }%s\n", (i < nresults - 1) ? "," : "");
    }
    fprintf(f, "  ]\n");
    fprintf(f, "}\n");
    fclose(f);
}

/* ========================================================================== */
/*                              Main                                          */
/* ========================================================================== */

static void print_usage(const char *prog) {
    fprintf(stderr, "Usage: %s <corpus_dir> <iterations> <output_json>\n", prog);
    fprintf(stderr, "\nExample: %s bench/corpus 100 results/baseline_results.json\n", prog);
}

int main(int argc, char **argv) {
    if (argc < 4) {
        print_usage(argv[0]);
        return 1;
    }

    const char *corpus_dir = argv[1];
    int iterations = atoi(argv[2]);
    const char *output_path = argv[3];

    if (iterations < 10) {
        fprintf(stderr, "Warning: iterations=%d is very low, using 10 minimum\n",
                iterations);
        iterations = 10;
    }

    printf("=== DEFLATE Benchmark Harness ===\n");
    printf("Corpus: %s\n", corpus_dir);
    printf("Iterations: %d (+ %d warmup)\n", iterations, WARMUP_ITERS);
    printf("Output: %s\n\n", output_path);

    /* Initialize optional decoders */

    /* zlib-ng via dlopen */
    {
        /* Try relative path first, then absolute */
        const char *zng_paths[] = {
            "third_party/zlib-ng/libz.so.1.3.1.zlib-ng",
            "./third_party/zlib-ng/libz.so.1.3.1.zlib-ng",
            NULL
        };
        for (int i = 0; zng_paths[i]; i++) {
            if (init_zlibng(zng_paths[i]) == 0) {
                decoders[2].available = 1;
                printf("[OK] zlib-ng loaded from %s\n", zng_paths[i]);
                break;
            }
        }
        if (!decoders[2].available) {
            /* Try to find it with a glob */
            char trypath[512];
            snprintf(trypath, sizeof(trypath),
                     "%s/../../third_party/zlib-ng/libz.so.1.3.1.zlib-ng",
                     corpus_dir);
            if (init_zlibng(trypath) == 0) {
                decoders[2].available = 1;
                printf("[OK] zlib-ng loaded from %s\n", trypath);
            }
        }
        if (!decoders[2].available) {
            printf("[--] zlib-ng not available\n");
        }
    }

    /* libdeflate */
    ld_decompressor = libdeflate_alloc_decompressor();
    if (ld_decompressor) {
        decoders[3].available = 1;
        printf("[OK] libdeflate initialized\n");
    } else {
        printf("[--] libdeflate not available\n");
    }

    /* Count available decoders */
    int n_decoders = 0;
    for (int i = 0; i < MAX_DECODERS; i++) {
        if (decoders[i].available) n_decoders++;
    }
    printf("\nActive decoders: %d\n", n_decoders);

    /* Scan corpus */
    corpus_file_t corpus[MAX_CORPUS_FILES];
    int n_files = scan_corpus(corpus_dir, corpus, MAX_CORPUS_FILES);
    if (n_files == 0) {
        fprintf(stderr, "No .deflate files found in %s\n", corpus_dir);
        return 1;
    }
    printf("Corpus files: %d\n\n", n_files);

    /* Allocate results */
    int max_results = n_files * MAX_DECODERS;
    bench_result_t *results = calloc(max_results, sizeof(bench_result_t));
    if (!results) {
        fprintf(stderr, "Out of memory for results\n");
        return 1;
    }
    int n_results = 0;

    /* Run benchmarks */
    printf("%-30s %-12s %5s %10s ", "File", "Decoder", "Level", "Size(KB)");
    printf("%10s %10s %10s %10s\n",
           "Med(MB/s)", "Mean", "P5", "P95");
    printf("%-30s %-12s %5s %10s ", "----", "-------", "-----", "--------");
    printf("%10s %10s %10s %10s\n",
           "---------", "----", "--", "---");

    for (int fi = 0; fi < n_files; fi++) {
        corpus_file_t *cf = &corpus[fi];

        /* Load compressed data */
        size_t comp_len = 0;
        uint8_t *compressed = read_file(cf->filename, &comp_len);
        if (!compressed) {
            fprintf(stderr, "Cannot read %s\n", cf->filename);
            continue;
        }

        /* Load original data for correctness verification */
        char orig_path[512];
        snprintf(orig_path, sizeof(orig_path), "%s/%s", corpus_dir, cf->basename);
        size_t orig_len = 0;
        uint8_t *original = read_file(orig_path, &orig_len);
        if (!original) {
            fprintf(stderr, "Cannot read original %s\n", orig_path);
            free(compressed);
            continue;
        }

        for (int di = 0; di < MAX_DECODERS; di++) {
            if (!decoders[di].available) continue;

            bench_result_t *r = &results[n_results];
            strncpy(r->decoder_name, decoders[di].name, sizeof(r->decoder_name) - 1);
            strncpy(r->filename, cf->basename, sizeof(r->filename) - 1);
            r->level = cf->level;
            r->original_size = orig_len;
            r->compressed_size = comp_len;

            int valid = 0;
            stats_t st = {0};
            int rc = run_single_bench(decoders[di].fn,
                                      compressed, comp_len,
                                      original, orig_len,
                                      iterations, &st, &valid);

            if (rc == 0 && valid) {
                r->throughput_stats = st;
                r->valid = 1;
                printf("%-30s %-12s %5d %10.1f %10.1f %10.1f %10.1f %10.1f\n",
                       cf->basename, decoders[di].name, cf->level,
                       (double)orig_len / 1024.0,
                       st.median, st.mean, st.p5, st.p95);
            } else {
                r->valid = 0;
                printf("%-30s %-12s %5d %10.1f %10s\n",
                       cf->basename, decoders[di].name, cf->level,
                       (double)orig_len / 1024.0,
                       "FAIL");
            }
            n_results++;
        }

        free(compressed);
        free(original);
    }

    /* Write JSON results */
    write_results_json(output_path, results, n_results, iterations);
    printf("\n=== Results written to %s ===\n", output_path);

    /* Print summary: geometric mean speedup over zlib for each decoder */
    printf("\n=== Geometric Mean Throughput (MB/s) ===\n");
    for (int di = 0; di < MAX_DECODERS; di++) {
        if (!decoders[di].available) continue;

        double log_sum = 0;
        int count = 0;
        for (int ri = 0; ri < n_results; ri++) {
            if (strcmp(results[ri].decoder_name, decoders[di].name) == 0
                && results[ri].valid && results[ri].throughput_stats.median > 0) {
                log_sum += log(results[ri].throughput_stats.median);
                count++;
            }
        }
        if (count > 0) {
            double geomean = exp(log_sum / count);
            printf("  %-12s: %8.1f MB/s (%d files)\n",
                   decoders[di].name, geomean, count);
        }
    }

    /* Print speedup ratios over zlib */
    printf("\n=== Geometric Mean Speedup vs. zlib ===\n");
    for (int di = 0; di < MAX_DECODERS; di++) {
        if (!decoders[di].available || di == 1 /* skip zlib vs zlib */) continue;

        double log_speedup_sum = 0;
        int count = 0;
        for (int ri = 0; ri < n_results; ri++) {
            if (strcmp(results[ri].decoder_name, decoders[di].name) != 0
                || !results[ri].valid)
                continue;

            /* Find matching zlib result */
            for (int rj = 0; rj < n_results; rj++) {
                if (strcmp(results[rj].decoder_name, "zlib") == 0
                    && strcmp(results[rj].filename, results[ri].filename) == 0
                    && results[rj].level == results[ri].level
                    && results[rj].valid
                    && results[rj].throughput_stats.median > 0) {
                    double speedup = results[ri].throughput_stats.median /
                                     results[rj].throughput_stats.median;
                    log_speedup_sum += log(speedup);
                    count++;
                    break;
                }
            }
        }
        if (count > 0) {
            double geomean_speedup = exp(log_speedup_sum / count);
            printf("  %-12s: %.2fx (%d files)\n",
                   decoders[di].name, geomean_speedup, count);
        }
    }

    /* Cleanup */
    free(results);
    if (ld_decompressor) libdeflate_free_decompressor(ld_decompressor);
    if (zlibng_handle) dlclose(zlibng_handle);

    return 0;
}
