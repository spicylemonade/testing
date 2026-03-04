/*
 * test_correctness.c - Verify fd_inflate produces byte-identical output to zlib.
 *
 * For each test input:
 *   1. Compress with zlib at multiple levels
 *   2. Decompress with zlib to get reference output
 *   3. Decompress with fd_inflate and compare byte-by-byte
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include "fast_deflate.h"

#define MAX_INPUT_SIZE  (4 * 1024 * 1024)  /* 4 MB max per test */
#define MAX_COMPRESSED  (MAX_INPUT_SIZE + 4096)

static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

/*
 * Compress data using raw DEFLATE (no zlib/gzip header).
 * Returns compressed size, or 0 on error.
 */
static size_t compress_raw_deflate(const uint8_t *input, size_t input_len,
                                    uint8_t *output, size_t output_cap,
                                    int level) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    /* Use negative windowBits for raw DEFLATE (no zlib header) */
    if (deflateInit2(&strm, level, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) != Z_OK) {
        return 0;
    }

    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_len;
    strm.next_out = output;
    strm.avail_out = (uInt)output_cap;

    int rc = deflate(&strm, Z_FINISH);
    if (rc != Z_STREAM_END) {
        deflateEnd(&strm);
        return 0;
    }

    size_t compressed_len = strm.total_out;
    deflateEnd(&strm);
    return compressed_len;
}

/*
 * Decompress raw DEFLATE using zlib (reference).
 * Returns decompressed size, or 0 on error.
 */
static size_t decompress_zlib_raw(const uint8_t *compressed, size_t comp_len,
                                   uint8_t *output, size_t output_cap) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    /* Negative windowBits for raw DEFLATE */
    if (inflateInit2(&strm, -15) != Z_OK) {
        return 0;
    }

    strm.next_in = (Bytef *)compressed;
    strm.avail_in = (uInt)comp_len;
    strm.next_out = output;
    strm.avail_out = (uInt)output_cap;

    int rc = inflate(&strm, Z_FINISH);
    if (rc != Z_STREAM_END) {
        inflateEnd(&strm);
        return 0;
    }

    size_t decompressed_len = strm.total_out;
    inflateEnd(&strm);
    return decompressed_len;
}

/*
 * Test: compress with zlib at given level, decompress with both zlib and
 * fd_inflate, compare outputs.
 */
static int test_roundtrip(const char *name, const uint8_t *data, size_t data_len, int level) {
    tests_run++;

    static uint8_t compressed[MAX_COMPRESSED];
    static uint8_t zlib_output[MAX_INPUT_SIZE];
    static uint8_t fd_output[MAX_INPUT_SIZE];

    /* Compress */
    size_t comp_len = compress_raw_deflate(data, data_len, compressed, sizeof(compressed), level);
    if (comp_len == 0) {
        printf("FAIL [%s level=%d]: compression failed\n", name, level);
        tests_failed++;
        return 0;
    }

    /* Decompress with zlib (reference) */
    size_t zlib_len = decompress_zlib_raw(compressed, comp_len, zlib_output, sizeof(zlib_output));
    if (zlib_len != data_len || memcmp(zlib_output, data, data_len) != 0) {
        printf("FAIL [%s level=%d]: zlib roundtrip mismatch\n", name, level);
        tests_failed++;
        return 0;
    }

    /* Decompress with fd_inflate */
    size_t fd_len = 0;
    int rc = fd_inflate(compressed, comp_len, fd_output, sizeof(fd_output), &fd_len);
    if (rc != FD_OK) {
        printf("FAIL [%s level=%d]: fd_inflate returned %d\n", name, level, rc);
        tests_failed++;
        return 0;
    }

    /* Compare */
    if (fd_len != data_len) {
        printf("FAIL [%s level=%d]: size mismatch (expected %zu, got %zu)\n",
               name, level, data_len, fd_len);
        tests_failed++;
        return 0;
    }

    if (memcmp(fd_output, data, data_len) != 0) {
        /* Find first difference */
        for (size_t i = 0; i < data_len; i++) {
            if (fd_output[i] != data[i]) {
                printf("FAIL [%s level=%d]: byte mismatch at offset %zu "
                       "(expected 0x%02x, got 0x%02x)\n",
                       name, level, i, data[i], fd_output[i]);
                break;
            }
        }
        tests_failed++;
        return 0;
    }

    tests_passed++;
    return 1;
}

/* Generate test data: all zeros */
static void fill_zeros(uint8_t *buf, size_t len) {
    memset(buf, 0, len);
}

/* Generate test data: sequential bytes */
static void fill_sequential(uint8_t *buf, size_t len) {
    for (size_t i = 0; i < len; i++) buf[i] = (uint8_t)(i & 0xFF);
}

/* Generate test data: pseudo-random */
static void fill_random(uint8_t *buf, size_t len, uint32_t seed) {
    uint32_t s = seed;
    for (size_t i = 0; i < len; i++) {
        s = s * 1103515245 + 12345;
        buf[i] = (uint8_t)(s >> 16);
    }
}

/* Generate test data: English-like text */
static void fill_text(uint8_t *buf, size_t len) {
    const char *words[] = {
        "the ", "quick ", "brown ", "fox ", "jumps ", "over ", "lazy ", "dog ",
        "and ", "cat ", "sat ", "on ", "mat ", "in ", "a ", "big ", "red ",
        "house ", "with ", "green ", "door ", "hello ", "world ", "test ",
        "data ", "compression ", "deflate ", "huffman ", "coding ", "algorithm "
    };
    int nwords = sizeof(words) / sizeof(words[0]);
    size_t pos = 0;
    uint32_t seed = 42;
    while (pos < len) {
        seed = seed * 1103515245 + 12345;
        const char *w = words[(seed >> 16) % nwords];
        size_t wlen = strlen(w);
        if (pos + wlen > len) wlen = len - pos;
        memcpy(buf + pos, w, wlen);
        pos += wlen;
    }
}

/* Generate test data: highly repetitive (tests overlapping matches) */
static void fill_repetitive(uint8_t *buf, size_t len) {
    const char *pattern = "ABCDEFGH";
    size_t plen = strlen(pattern);
    for (size_t i = 0; i < len; i++) {
        buf[i] = (uint8_t)pattern[i % plen];
    }
}

/* Generate test data: single byte repeated (tests distance=1 RLE) */
static void fill_single_byte(uint8_t *buf, size_t len) {
    memset(buf, 'X', len);
}

/* Test with a file loaded from disk */
static int test_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return 0;

    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (fsize <= 0 || (size_t)fsize > MAX_INPUT_SIZE) {
        fclose(f);
        return 0;
    }

    uint8_t *data = malloc((size_t)fsize);
    if (!data) { fclose(f); return 0; }

    size_t nread = fread(data, 1, (size_t)fsize, f);
    fclose(f);

    if (nread != (size_t)fsize) { free(data); return 0; }

    int ok = 1;
    for (int level = 1; level <= 9; level++) {
        if (!test_roundtrip(path, data, (size_t)fsize, level)) ok = 0;
    }

    free(data);
    return ok;
}

int main(int argc, char **argv) {
    static uint8_t test_buf[MAX_INPUT_SIZE];

    printf("=== DEFLATE Correctness Tests ===\n\n");

    /* Size variants to test */
    size_t sizes[] = {0, 1, 2, 10, 100, 1000, 4096, 16384, 65536, 262144, 1048576};
    int nsizes = sizeof(sizes) / sizeof(sizes[0]);

    /* Test empty input */
    printf("--- Empty input ---\n");
    test_roundtrip("empty", test_buf, 0, 1);

    /* Test various data patterns at multiple sizes and compression levels */
    struct {
        const char *name;
        void (*fill)(uint8_t *, size_t);
    } patterns[] = {
        {"zeros",      (void(*)(uint8_t*,size_t))fill_zeros},
        {"sequential", (void(*)(uint8_t*,size_t))fill_sequential},
        {"text",       (void(*)(uint8_t*,size_t))fill_text},
        {"repetitive", (void(*)(uint8_t*,size_t))fill_repetitive},
        {"single_byte",(void(*)(uint8_t*,size_t))fill_single_byte},
    };
    int npatterns = sizeof(patterns) / sizeof(patterns[0]);

    for (int p = 0; p < npatterns; p++) {
        printf("--- Pattern: %s ---\n", patterns[p].name);
        for (int s = 0; s < nsizes; s++) {
            if (sizes[s] == 0) continue;
            if (sizes[s] > MAX_INPUT_SIZE) continue;

            patterns[p].fill(test_buf, sizes[s]);

            for (int level = 1; level <= 9; level += 4) { /* Test levels 1, 5, 9 */
                char label[128];
                snprintf(label, sizeof(label), "%s_%zu", patterns[p].name, sizes[s]);
                test_roundtrip(label, test_buf, sizes[s], level);
            }
        }
    }

    /* Random data at various seeds */
    printf("--- Random data ---\n");
    for (int seed = 0; seed < 10; seed++) {
        fill_random(test_buf, 65536, 42 + seed);
        char label[64];
        snprintf(label, sizeof(label), "random_seed%d_64k", seed);
        for (int level = 1; level <= 9; level += 4) {
            test_roundtrip(label, test_buf, 65536, level);
        }
    }

    /* Test with corpus files if provided */
    if (argc > 1) {
        printf("\n--- File tests ---\n");
        for (int i = 1; i < argc; i++) {
            printf("Testing file: %s\n", argv[i]);
            test_file(argv[i]);
        }
    }

    /* Summary */
    printf("\n=== Results ===\n");
    printf("Tests run:    %d\n", tests_run);
    printf("Tests passed: %d\n", tests_passed);
    printf("Tests failed: %d\n", tests_failed);

    return tests_failed > 0 ? 1 : 0;
}
