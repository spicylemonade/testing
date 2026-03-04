#define _POSIX_C_SOURCE 199309L

/*
 * bench_main.c - Benchmarking framework for Base64 decoders
 *
 * Measures throughput (GB/s) and latency statistics (median, p95, p99)
 * across 9 payload sizes from 64B to 10MB.
 * Uses rdtsc (x86) or clock_gettime for timing.
 * Outputs JSON for machine processing.
 */

#include "../src/common/base64.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

/* --- Timing --- */

#if defined(__x86_64__) || defined(_M_X64)
static inline uint64_t rdtsc_start(void) {
    uint32_t lo, hi;
    __asm__ volatile("lfence\n\trdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
static inline uint64_t rdtsc_end(void) {
    uint32_t lo, hi;
    __asm__ volatile("rdtscp" : "=a"(lo), "=d"(hi) :: "ecx");
    __asm__ volatile("lfence");
    return ((uint64_t)hi << 32) | lo;
}
#define HAS_RDTSC 1
#elif defined(__aarch64__)
static inline uint64_t rdtsc_start(void) {
    uint64_t val;
    __asm__ volatile("isb\n\tmrs %0, cntvct_el0" : "=r"(val));
    return val;
}
static inline uint64_t rdtsc_end(void) {
    uint64_t val;
    __asm__ volatile("isb\n\tmrs %0, cntvct_el0" : "=r"(val));
    return val;
}
#define HAS_RDTSC 1
#else
#define HAS_RDTSC 0
#endif

static double wall_time_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e9 + (double)ts.tv_nsec;
}

/* --- Sorting for percentile computation --- */

static int cmp_double(const void *a, const void *b) {
    double da = *(const double *)a;
    double db = *(const double *)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

/* --- Base64 encoding (for generating test payloads) --- */

static const char B64_ENC[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

static size_t base64_encode_simple(const uint8_t *src, size_t src_len,
                                    char *dst, size_t dst_cap) {
    size_t i = 0, j = 0;
    for (; i + 3 <= src_len; i += 3) {
        if (j + 4 > dst_cap) return 0;
        uint32_t triplet = ((uint32_t)src[i] << 16) |
                           ((uint32_t)src[i+1] << 8) |
                           (uint32_t)src[i+2];
        dst[j++] = B64_ENC[(triplet >> 18) & 0x3F];
        dst[j++] = B64_ENC[(triplet >> 12) & 0x3F];
        dst[j++] = B64_ENC[(triplet >>  6) & 0x3F];
        dst[j++] = B64_ENC[triplet & 0x3F];
    }
    size_t rem = src_len - i;
    if (rem == 1) {
        if (j + 4 > dst_cap) return 0;
        dst[j++] = B64_ENC[src[i] >> 2];
        dst[j++] = B64_ENC[(src[i] & 0x3) << 4];
        dst[j++] = '=';
        dst[j++] = '=';
    } else if (rem == 2) {
        if (j + 4 > dst_cap) return 0;
        dst[j++] = B64_ENC[src[i] >> 2];
        dst[j++] = B64_ENC[((src[i] & 0x3) << 4) | (src[i+1] >> 4)];
        dst[j++] = B64_ENC[(src[i+1] & 0xF) << 2];
        dst[j++] = '=';
    }
    return j;
}

/* --- Benchmark runner --- */

typedef struct {
    const char *name;
    base64_status_t (*decode)(const uint8_t *, size_t, uint8_t *, size_t *, base64_variant_t);
} decoder_entry_t;

typedef struct {
    double median_ns;
    double p95_ns;
    double p99_ns;
    double throughput_gbps;
    double cycles_per_byte;
    size_t input_bytes;
    size_t output_bytes;
    int iterations;
} bench_result_t;

static bench_result_t benchmark_decoder(
    base64_status_t (*decode)(const uint8_t *, size_t, uint8_t *, size_t *, base64_variant_t),
    const uint8_t *input, size_t input_len,
    uint8_t *output, size_t output_cap,
    int iterations, int warmup)
{
    bench_result_t result;
    memset(&result, 0, sizeof(result));
    result.input_bytes = input_len;
    result.iterations = iterations;

    double *timings = (double *)malloc(sizeof(double) * (size_t)iterations);
    if (!timings) { result.throughput_gbps = -1; return result; }

    /* Warmup */
    for (int w = 0; w < warmup; w++) {
        size_t out_len = output_cap;
        decode(input, input_len, output, &out_len, BASE64_STANDARD);
    }

    /* Timed iterations */
    for (int i = 0; i < iterations; i++) {
        size_t out_len = output_cap;
        double t0 = wall_time_ns();
        decode(input, input_len, output, &out_len, BASE64_STANDARD);
        double t1 = wall_time_ns();
        timings[i] = t1 - t0;
        if (i == 0) result.output_bytes = out_len;
    }

    /* Sort for percentiles */
    qsort(timings, (size_t)iterations, sizeof(double), cmp_double);

    result.median_ns = timings[iterations / 2];
    result.p95_ns = timings[(int)((double)iterations * 0.95)];
    result.p99_ns = timings[(int)((double)iterations * 0.99)];

    /* Throughput: input bytes processed per second */
    if (result.median_ns > 0) {
        result.throughput_gbps = (double)input_len / result.median_ns; /* GB/s = bytes/ns */
    }

    /* Cycles per byte (rough estimate from wall clock assuming ~3 GHz) */
    /* Better: use rdtsc directly if available */
    result.cycles_per_byte = result.median_ns * 3.0 / (double)input_len; /* approx at 3GHz */

    free(timings);
    return result;
}

/* --- Main --- */

static const size_t PAYLOAD_SIZES[] = {
    64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 10485760
};
static const int NUM_SIZES = 9;

static void print_json_results(const char *decoder_name,
                               bench_result_t *results, int num_sizes) {
    printf("  {\n    \"decoder\": \"%s\",\n    \"results\": [\n", decoder_name);
    for (int i = 0; i < num_sizes; i++) {
        printf("      {\"input_bytes\": %zu, \"output_bytes\": %zu, "
               "\"median_ns\": %.1f, \"p95_ns\": %.1f, \"p99_ns\": %.1f, "
               "\"throughput_gbps\": %.4f, \"iterations\": %d}%s\n",
               results[i].input_bytes, results[i].output_bytes,
               results[i].median_ns, results[i].p95_ns, results[i].p99_ns,
               results[i].throughput_gbps, results[i].iterations,
               i < num_sizes - 1 ? "," : "");
    }
    printf("    ]\n  }");
}

int main(int argc, char **argv) {
    (void)argc; (void)argv;

    /* Seed PRNG for deterministic payloads */
    srand(42);

    printf("{\n  \"benchmark\": \"simd_base64_decode\",\n");
    printf("  \"timestamp\": \"%s %s\",\n", __DATE__, __TIME__);

    /* Detect arch */
#if defined(__x86_64__)
    printf("  \"arch\": \"x86-64\",\n");
#elif defined(__aarch64__)
    printf("  \"arch\": \"aarch64\",\n");
#else
    printf("  \"arch\": \"unknown\",\n");
#endif

    printf("  \"decoders\": [\n");

    /* Register decoders */
    decoder_entry_t decoders[] = {
        {"scalar", base64_decode_scalar},
        /* More decoders will be added as implemented */
    };
    int num_decoders = sizeof(decoders) / sizeof(decoders[0]);

    for (int d = 0; d < num_decoders; d++) {
        bench_result_t results[9];

        for (int s = 0; s < NUM_SIZES; s++) {
            size_t raw_size = PAYLOAD_SIZES[s];

            /* Generate random binary data */
            uint8_t *raw_data = (uint8_t *)malloc(raw_size);
            for (size_t j = 0; j < raw_size; j++) {
                raw_data[j] = (uint8_t)(rand() & 0xFF);
            }

            /* Encode to Base64 */
            size_t enc_cap = (raw_size / 3 + 1) * 4 + 4;
            char *encoded = (char *)malloc(enc_cap);
            size_t enc_len = base64_encode_simple(raw_data, raw_size, encoded, enc_cap);

            /* Allocate output buffer */
            size_t out_cap = raw_size + 16;
            uint8_t *output = (uint8_t *)malloc(out_cap);

            /* Determine iteration count based on payload size */
            int iters = 10000;
            if (raw_size >= 65536) iters = 1000;
            if (raw_size >= 1048576) iters = 100;

            results[s] = benchmark_decoder(
                decoders[d].decode,
                (const uint8_t *)encoded, enc_len,
                output, out_cap,
                iters, iters / 10);

            free(raw_data);
            free(encoded);
            free(output);
        }

        print_json_results(decoders[d].name, results, NUM_SIZES);
        if (d < num_decoders - 1) printf(",");
        printf("\n");
    }

    printf("  ]\n}\n");
    return 0;
}
