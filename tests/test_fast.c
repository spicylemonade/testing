/*
 * test_fast.c - Verify fd_inflate_fast produces byte-identical output to zlib.
 *
 * Same test methodology as test_correctness.c but tests the optimized decoder.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include "fast_deflate.h"

#define MAX_INPUT_SIZE  (4 * 1024 * 1024)
#define MAX_COMPRESSED  (MAX_INPUT_SIZE + 4096)

static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

static size_t compress_raw_deflate(const uint8_t *input, size_t input_len,
                                    uint8_t *output, size_t output_cap,
                                    int level) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, level, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) != Z_OK)
        return 0;
    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_len;
    strm.next_out = output;
    strm.avail_out = (uInt)output_cap;
    int ret = deflate(&strm, Z_FINISH);
    size_t comp_len = strm.total_out;
    deflateEnd(&strm);
    if (ret != Z_STREAM_END) return 0;
    return comp_len;
}

static size_t decompress_zlib_raw(const uint8_t *input, size_t input_len,
                                   uint8_t *output, size_t output_cap) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit2(&strm, -15) != Z_OK) return 0;
    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_len;
    strm.next_out = output;
    strm.avail_out = (uInt)output_cap;
    int ret = inflate(&strm, Z_FINISH);
    size_t len = strm.total_out;
    inflateEnd(&strm);
    if (ret != Z_STREAM_END) return 0;
    return len;
}

static int test_roundtrip(const char *name, const uint8_t *data, size_t data_len, int level) {
    tests_run++;

    static uint8_t compressed[MAX_COMPRESSED];
    static uint8_t zlib_output[MAX_INPUT_SIZE];
    static uint8_t fd_output[MAX_INPUT_SIZE];

    size_t comp_len = compress_raw_deflate(data, data_len, compressed, sizeof(compressed), level);
    if (comp_len == 0) {
        printf("FAIL [%s level=%d]: compression failed\n", name, level);
        tests_failed++;
        return 0;
    }

    size_t zlib_len = decompress_zlib_raw(compressed, comp_len, zlib_output, sizeof(zlib_output));
    if (zlib_len != data_len || memcmp(zlib_output, data, data_len) != 0) {
        printf("FAIL [%s level=%d]: zlib roundtrip mismatch\n", name, level);
        tests_failed++;
        return 0;
    }

    /* Decompress with fd_inflate_fast */
    size_t fd_len = 0;
    int rc = fd_inflate_fast(compressed, comp_len, fd_output, sizeof(fd_output), &fd_len);
    if (rc != FD_OK) {
        printf("FAIL [%s level=%d]: fd_inflate_fast returned %d\n", name, level, rc);
        tests_failed++;
        return 0;
    }

    if (fd_len != data_len) {
        printf("FAIL [%s level=%d]: size mismatch (expected %zu, got %zu)\n",
               name, level, data_len, fd_len);
        tests_failed++;
        return 0;
    }

    if (memcmp(fd_output, data, data_len) != 0) {
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

/* Data generators */
static void fill_zeros(uint8_t *buf, size_t len) { memset(buf, 0, len); }

static void fill_sequential(uint8_t *buf, size_t len) {
    for (size_t i = 0; i < len; i++) buf[i] = (uint8_t)(i & 0xFF);
}

static void fill_random(uint8_t *buf, size_t len, uint32_t seed) {
    uint32_t s = seed;
    for (size_t i = 0; i < len; i++) {
        s = s * 1103515245 + 12345;
        buf[i] = (uint8_t)(s >> 16);
    }
}

static void fill_text_like(uint8_t *buf, size_t len, uint32_t seed) {
    const char *words[] = {
        "the ", "quick ", "brown ", "fox ", "jumps ", "over ", "lazy ", "dog ",
        "hello ", "world ", "foo ", "bar ", "baz ", "qux ", "test ", "data ",
        "compress ", "deflate ", "huffman ", "lz77 ",
    };
    uint32_t s = seed;
    size_t pos = 0;
    while (pos < len) {
        s = s * 1103515245 + 12345;
        int widx = (int)((s >> 16) % 20);
        const char *w = words[widx];
        size_t wlen = strlen(w);
        if (pos + wlen > len) wlen = len - pos;
        memcpy(buf + pos, w, wlen);
        pos += wlen;
    }
}

static void fill_repetitive(uint8_t *buf, size_t len) {
    const char *pattern = "ABCDEFGHIJKLMNOP";
    size_t plen = 16;
    for (size_t i = 0; i < len; i++) buf[i] = (uint8_t)pattern[i % plen];
}

static void fill_mixed_entropy(uint8_t *buf, size_t len, uint32_t seed) {
    uint32_t s = seed;
    for (size_t i = 0; i < len; i++) {
        if ((i / 256) % 2 == 0) {
            s = s * 1103515245 + 12345;
            buf[i] = (uint8_t)(s >> 16);
        } else {
            buf[i] = (uint8_t)(i & 0xFF);
        }
    }
}

#define RUN_TEST(name, fill_fn, size, ...) do { \
    uint8_t *buf = malloc(size); \
    if (!buf) { printf("FAIL: malloc failed\n"); tests_failed++; break; } \
    fill_fn(buf, size, ##__VA_ARGS__); \
    test_roundtrip(name " L1", buf, size, 1); \
    test_roundtrip(name " L6", buf, size, 6); \
    test_roundtrip(name " L9", buf, size, 9); \
    free(buf); \
} while(0)

int main(void) {
    printf("=== Fast Decoder (fd_inflate_fast) Correctness Tests ===\n\n");

    /* Basic tests */
    RUN_TEST("zeros_1k",        fill_zeros, 1024);
    RUN_TEST("zeros_64k",       fill_zeros, 65536);
    RUN_TEST("zeros_256k",      fill_zeros, 262144);
    RUN_TEST("sequential_1k",   fill_sequential, 1024);
    RUN_TEST("sequential_64k",  fill_sequential, 65536);
    RUN_TEST("sequential_256k", fill_sequential, 262144);
    RUN_TEST("random_1k",       fill_random, 1024, 42);
    RUN_TEST("random_64k",      fill_random, 65536, 42);
    RUN_TEST("random_256k",     fill_random, 262144, 42);
    RUN_TEST("text_1k",         fill_text_like, 1024, 42);
    RUN_TEST("text_4k",         fill_text_like, 4096, 42);
    RUN_TEST("text_16k",        fill_text_like, 16384, 42);
    RUN_TEST("text_64k",        fill_text_like, 65536, 42);
    RUN_TEST("text_256k",       fill_text_like, 262144, 42);
    RUN_TEST("text_1m",         fill_text_like, 1048576, 42);
    RUN_TEST("repetitive_1k",   fill_repetitive, 1024);
    RUN_TEST("repetitive_64k",  fill_repetitive, 65536);
    RUN_TEST("repetitive_256k", fill_repetitive, 262144);
    RUN_TEST("mixed_1k",        fill_mixed_entropy, 1024, 42);
    RUN_TEST("mixed_64k",       fill_mixed_entropy, 65536, 42);
    RUN_TEST("mixed_256k",      fill_mixed_entropy, 262144, 42);

    /* Tiny inputs */
    {
        uint8_t tiny[] = {0x41};
        test_roundtrip("tiny_1byte L1", tiny, 1, 1);
        test_roundtrip("tiny_1byte L6", tiny, 1, 6);
    }
    {
        uint8_t tiny2[] = {0x41, 0x42};
        test_roundtrip("tiny_2byte L1", tiny2, 2, 1);
        test_roundtrip("tiny_2byte L6", tiny2, 2, 6);
    }
    {
        uint8_t tiny16[16];
        memset(tiny16, 'X', 16);
        test_roundtrip("tiny_16byte L1", tiny16, 16, 1);
        test_roundtrip("tiny_16byte L6", tiny16, 16, 6);
    }

    /* Multiple random seeds */
    for (uint32_t seed = 1; seed <= 10; seed++) {
        char name[64];
        snprintf(name, sizeof(name), "random_seed%u_16k", seed);
        uint8_t *buf = malloc(16384);
        fill_random(buf, 16384, seed);
        test_roundtrip(name, buf, 16384, 6);
        free(buf);
    }

    printf("\n=== Results: %d/%d passed, %d failed ===\n",
           tests_passed, tests_run, tests_failed);

    return tests_failed > 0 ? 1 : 0;
}
