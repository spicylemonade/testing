/*
 * test_adversarial.c - Comprehensive adversarial test suite for fd_inflate_fast
 *
 * Tests boundary conditions, edge cases, and adversarial DEFLATE streams.
 * All outputs are compared byte-for-byte against zlib's raw inflate as reference.
 *
 * Compile:
 *   gcc -O3 -march=native -std=c11 -g -Iinclude -o test_adversarial \
 *       tests/test_adversarial.c src/fast_decode.c -lz
 *
 * For ASAN:
 *   gcc -O1 -fsanitize=address,undefined -fno-omit-frame-pointer \
 *       -std=c11 -g -Iinclude -o test_adversarial \
 *       tests/test_adversarial.c src/fast_decode.c -lz
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <zlib.h>
#include "fast_deflate.h"

/* ========================================================================== */
/*                          Test infrastructure                               */
/* ========================================================================== */

#define MAX_INPUT_SIZE   (4 * 1024 * 1024)  /* 4 MB */
#define MAX_COMPRESSED   (MAX_INPUT_SIZE + 4096)
#define MAX_DECOMP       (MAX_INPUT_SIZE + 4096)

static int g_tests_run    = 0;
static int g_tests_passed = 0;
static int g_tests_failed = 0;

static void pass(const char *name) {
    g_tests_run++;
    g_tests_passed++;
    printf("  PASS  %s\n", name);
}

static void fail(const char *name, const char *reason) {
    g_tests_run++;
    g_tests_failed++;
    printf("  FAIL  %s: %s\n", name, reason);
}

/* ========================================================================== */
/*                      Raw DEFLATE compress / decompress helpers             */
/* ========================================================================== */

/*
 * Compress data into raw DEFLATE (windowBits=-15, no zlib/gzip wrapper).
 * Returns compressed size, or 0 on failure.
 */
static size_t compress_raw(const uint8_t *in, size_t in_len,
                           uint8_t *out, size_t out_cap, int level) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, level, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) != Z_OK)
        return 0;
    strm.next_in  = (Bytef *)in;
    strm.avail_in = (uInt)in_len;
    strm.next_out = out;
    strm.avail_out = (uInt)out_cap;
    int ret = deflate(&strm, Z_FINISH);
    size_t comp_len = strm.total_out;
    deflateEnd(&strm);
    return (ret == Z_STREAM_END) ? comp_len : 0;
}

/*
 * Compress with a specific strategy (e.g. Z_HUFFMAN_ONLY, Z_FILTERED, Z_RLE).
 */
static size_t compress_raw_strategy(const uint8_t *in, size_t in_len,
                                    uint8_t *out, size_t out_cap,
                                    int level, int strategy) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, level, Z_DEFLATED, -15, 8, strategy) != Z_OK)
        return 0;
    strm.next_in  = (Bytef *)in;
    strm.avail_in = (uInt)in_len;
    strm.next_out = out;
    strm.avail_out = (uInt)out_cap;
    int ret = deflate(&strm, Z_FINISH);
    size_t comp_len = strm.total_out;
    deflateEnd(&strm);
    return (ret == Z_STREAM_END) ? comp_len : 0;
}

/*
 * Compress using stored blocks only (level=0 forces stored blocks).
 */
static size_t compress_raw_stored(const uint8_t *in, size_t in_len,
                                  uint8_t *out, size_t out_cap) {
    return compress_raw(in, in_len, out, out_cap, 0);
}

/*
 * Decompress raw DEFLATE using zlib as reference (windowBits=-15).
 * Returns decompressed size, or 0 on failure.
 */
static size_t decompress_zlib_raw(const uint8_t *in, size_t in_len,
                                  uint8_t *out, size_t out_cap) {
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit2(&strm, -15) != Z_OK)
        return 0;
    strm.next_in  = (Bytef *)in;
    strm.avail_in = (uInt)in_len;
    strm.next_out = out;
    strm.avail_out = (uInt)out_cap;
    int ret = inflate(&strm, Z_FINISH);
    size_t dec_len = strm.total_out;
    inflateEnd(&strm);
    return (ret == Z_STREAM_END) ? dec_len : 0;
}

/*
 * Core roundtrip test: compress with zlib, decompress with both zlib and
 * fd_inflate_fast, compare byte-for-byte.
 * Returns 1 on pass, 0 on fail.
 */
static int test_roundtrip(const char *name, const uint8_t *data, size_t data_len,
                          int level) {
    uint8_t *comp = malloc(MAX_COMPRESSED);
    uint8_t *zlib_out = malloc(MAX_DECOMP);
    uint8_t *fd_out = malloc(MAX_DECOMP);
    if (!comp || !zlib_out || !fd_out) {
        fail(name, "malloc failed");
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }

    char label[256];
    snprintf(label, sizeof(label), "%s (level=%d, len=%zu)", name, level, data_len);

    size_t comp_len = compress_raw(data, data_len, comp, MAX_COMPRESSED, level);
    if (comp_len == 0 && data_len > 0) {
        /* level=0 can fail if output cap is too small for stored blocks */
        fail(label, "zlib compress failed");
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }
    if (data_len == 0 && comp_len == 0) {
        /* Empty input: zlib still produces a valid stream */
        comp_len = compress_raw(data, 0, comp, MAX_COMPRESSED, level);
        if (comp_len == 0) {
            fail(label, "zlib compress of empty data failed");
            free(comp); free(zlib_out); free(fd_out);
            return 0;
        }
    }

    /* Reference: decompress with zlib */
    size_t zlib_len = decompress_zlib_raw(comp, comp_len, zlib_out, MAX_DECOMP);
    if (zlib_len != data_len) {
        snprintf(label, sizeof(label),
                 "%s (level=%d): zlib roundtrip size mismatch (expected %zu, got %zu)",
                 name, level, data_len, zlib_len);
        fail(label, "zlib reference failed");
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }
    if (data_len > 0 && memcmp(zlib_out, data, data_len) != 0) {
        fail(label, "zlib roundtrip data mismatch");
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }

    /* Test: decompress with fd_inflate_fast */
    memset(fd_out, 0xAA, MAX_DECOMP); /* poison buffer */
    size_t fd_len = 0;
    int rc = fd_inflate_fast(comp, comp_len, fd_out, MAX_DECOMP, &fd_len);
    if (rc != FD_OK) {
        char msg[128];
        snprintf(msg, sizeof(msg), "fd_inflate_fast returned %d", rc);
        fail(label, msg);
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }

    if (fd_len != data_len) {
        char msg[128];
        snprintf(msg, sizeof(msg), "size mismatch: expected %zu, got %zu",
                 data_len, fd_len);
        fail(label, msg);
        free(comp); free(zlib_out); free(fd_out);
        return 0;
    }

    if (data_len > 0 && memcmp(fd_out, data, data_len) != 0) {
        /* Find first mismatch */
        for (size_t i = 0; i < data_len; i++) {
            if (fd_out[i] != data[i]) {
                char msg[256];
                snprintf(msg, sizeof(msg),
                         "byte mismatch at offset %zu: expected 0x%02x, got 0x%02x",
                         i, data[i], fd_out[i]);
                fail(label, msg);
                free(comp); free(zlib_out); free(fd_out);
                return 0;
            }
        }
    }

    pass(label);
    free(comp); free(zlib_out); free(fd_out);
    return 1;
}

/*
 * Roundtrip using a pre-compressed raw DEFLATE stream (for hand-crafted tests).
 * Compares fd_inflate_fast output against zlib inflate output.
 */
static int test_precompressed(const char *name,
                              const uint8_t *comp, size_t comp_len,
                              const uint8_t *expected, size_t expected_len) {
    uint8_t *zlib_out = malloc(MAX_DECOMP);
    uint8_t *fd_out = malloc(MAX_DECOMP);
    if (!zlib_out || !fd_out) {
        fail(name, "malloc failed");
        free(zlib_out); free(fd_out);
        return 0;
    }

    /* Reference: decompress with zlib */
    size_t zlib_len = decompress_zlib_raw(comp, comp_len, zlib_out, MAX_DECOMP);

    /* Decompress with fd_inflate_fast */
    memset(fd_out, 0xBB, MAX_DECOMP);
    size_t fd_len = 0;
    int rc = fd_inflate_fast(comp, comp_len, fd_out, MAX_DECOMP, &fd_len);

    /* Both should succeed or both should fail identically */
    if (zlib_len == 0) {
        /* zlib couldn't decompress - this is testing that fd also rejects it */
        if (rc != FD_OK) {
            pass(name);
        } else {
            fail(name, "fd_inflate_fast succeeded but zlib failed");
        }
        free(zlib_out); free(fd_out);
        return (rc != FD_OK) ? 1 : 0;
    }

    if (rc != FD_OK) {
        char msg[128];
        snprintf(msg, sizeof(msg), "fd_inflate_fast returned %d but zlib succeeded", rc);
        fail(name, msg);
        free(zlib_out); free(fd_out);
        return 0;
    }

    /* Compare sizes */
    if (fd_len != zlib_len) {
        char msg[128];
        snprintf(msg, sizeof(msg), "size mismatch: zlib=%zu, fd=%zu", zlib_len, fd_len);
        fail(name, msg);
        free(zlib_out); free(fd_out);
        return 0;
    }

    /* Compare bytes against zlib reference */
    if (memcmp(fd_out, zlib_out, zlib_len) != 0) {
        for (size_t i = 0; i < zlib_len; i++) {
            if (fd_out[i] != zlib_out[i]) {
                char msg[256];
                snprintf(msg, sizeof(msg),
                         "byte mismatch at %zu: zlib=0x%02x, fd=0x%02x",
                         i, zlib_out[i], fd_out[i]);
                fail(name, msg);
                free(zlib_out); free(fd_out);
                return 0;
            }
        }
    }

    /* Also check against expected if provided */
    if (expected && expected_len > 0) {
        if (fd_len != expected_len || memcmp(fd_out, expected, expected_len) != 0) {
            fail(name, "output does not match expected data");
            free(zlib_out); free(fd_out);
            return 0;
        }
    }

    pass(name);
    free(zlib_out); free(fd_out);
    return 1;
}

/* ========================================================================== */
/*                         Pseudo-random number generator                     */
/* ========================================================================== */

static uint32_t prng_state;

static void prng_seed(uint32_t s) { prng_state = s; }

static uint32_t prng_next(void) {
    prng_state = prng_state * 1103515245u + 12345u;
    return prng_state;
}

static uint8_t prng_byte(void) {
    return (uint8_t)(prng_next() >> 16);
}

static void prng_fill(uint8_t *buf, size_t len) {
    for (size_t i = 0; i < len; i++)
        buf[i] = prng_byte();
}

/* ========================================================================== */
/*                      (a) Empty DEFLATE stream                              */
/* ========================================================================== */

static void test_empty_stream(void) {
    printf("\n--- (a) Empty DEFLATE stream ---\n");

    /* Empty input compressed to a single end-of-block marker */
    uint8_t empty[0];
    test_roundtrip("empty_L1", empty, 0, 1);
    test_roundtrip("empty_L6", empty, 0, 6);
    test_roundtrip("empty_L9", empty, 0, 9);
}

/* ========================================================================== */
/*                    (b) Stored (uncompressed) blocks only                   */
/* ========================================================================== */

static void test_stored_blocks(void) {
    printf("\n--- (b) Stored (uncompressed) blocks ---\n");

    /* Empty stored block */
    uint8_t empty[0];
    test_roundtrip("stored_empty", empty, 0, 0);

    /* Tiny stored block: 1 byte */
    uint8_t one = 0x42;
    test_roundtrip("stored_1byte", &one, 1, 0);

    /* Small stored block: 16 bytes */
    uint8_t small[16];
    for (int i = 0; i < 16; i++) small[i] = (uint8_t)(i + 0x30);
    test_roundtrip("stored_16bytes", small, 16, 0);

    /* 256 bytes */
    uint8_t med[256];
    for (int i = 0; i < 256; i++) med[i] = (uint8_t)i;
    test_roundtrip("stored_256bytes", med, 256, 0);

    /* Exactly 65535 bytes (max stored block size) */
    uint8_t *maxblk = malloc(65535);
    if (maxblk) {
        prng_seed(100);
        prng_fill(maxblk, 65535);
        test_roundtrip("stored_65535bytes", maxblk, 65535, 0);
        free(maxblk);
    }

    /* Larger than single stored block (forces multiple stored blocks) */
    uint8_t *big = malloc(131072);
    if (big) {
        prng_seed(200);
        prng_fill(big, 131072);
        test_roundtrip("stored_128k", big, 131072, 0);
        free(big);
    }

    /* Random data at level 0 (zlib uses stored blocks for random data at L0) */
    uint8_t *rnd = malloc(4096);
    if (rnd) {
        prng_seed(300);
        prng_fill(rnd, 4096);
        test_roundtrip("stored_random_4k", rnd, 4096, 0);
        free(rnd);
    }
}

/* ========================================================================== */
/*                (c) Maximum back-reference distance (32768 bytes)           */
/* ========================================================================== */

static void test_max_distance(void) {
    printf("\n--- (c) Maximum back-reference distance (32768) ---\n");

    /*
     * Create data that forces maximum distance references:
     * Write a unique pattern at the start, fill 32768 bytes of different data,
     * then repeat the pattern. When compressed, zlib should create a
     * back-reference at distance ~32768.
     */
    size_t total = 32768 + 1024;
    uint8_t *data = malloc(total);
    if (!data) return;

    /* First 512 bytes: unique repeating pattern */
    for (int i = 0; i < 512; i++)
        data[i] = (uint8_t)(i * 7 + 3);

    /* Next 32768 - 512 bytes: sequential but different */
    for (size_t i = 512; i < 32768; i++)
        data[i] = (uint8_t)(i & 0xFF);

    /* Last 1024 bytes: repeat first 512 bytes twice to force far back-reference */
    memcpy(data + 32768, data, 512);
    memcpy(data + 32768 + 512, data, 512);

    test_roundtrip("maxdist_32768", data, total, 1);
    test_roundtrip("maxdist_32768", data, total, 6);
    test_roundtrip("maxdist_32768", data, total, 9);

    /* Exactly 32769 bytes with repeat at the very end */
    size_t total2 = 32769 + 258;
    uint8_t *data2 = malloc(total2);
    if (data2) {
        prng_seed(500);
        prng_fill(data2, 32769);
        /* Copy a chunk from the very beginning to the end */
        memcpy(data2 + 32769, data2, 258);
        test_roundtrip("maxdist_32769+258", data2, total2, 6);
        test_roundtrip("maxdist_32769+258", data2, total2, 9);
        free(data2);
    }

    /* Large buffer where the pattern repeats at exact distance 32768 */
    size_t total3 = 65536;
    uint8_t *data3 = malloc(total3);
    if (data3) {
        /* Fill first 32768 bytes with a pattern */
        for (size_t i = 0; i < 32768; i++)
            data3[i] = (uint8_t)((i * 13 + 7) & 0xFF);
        /* Copy to second half: same content at distance 32768 */
        memcpy(data3 + 32768, data3, 32768);
        test_roundtrip("maxdist_exact_dup_64k", data3, total3, 1);
        test_roundtrip("maxdist_exact_dup_64k", data3, total3, 9);
        free(data3);
    }

    free(data);
}

/* ========================================================================== */
/*          (d) Exercise all 286 literal/length codes                         */
/* ========================================================================== */

static void test_all_litlen_codes(void) {
    printf("\n--- (d) All 286 literal/length codes ---\n");

    /*
     * Strategy: include all 256 literal byte values plus enough match patterns
     * to exercise length codes 257..285 (lengths 3..258).
     *
     * Build data that contains:
     *   1. All 256 byte values (literals 0..255)
     *   2. Repeated patterns at various match lengths to trigger each length code
     */
    size_t cap = 256 + 30 * 300 + 4096;
    uint8_t *data = malloc(cap);
    if (!data) return;

    size_t pos = 0;

    /* All 256 literal byte values */
    for (int i = 0; i < 256; i++)
        data[pos++] = (uint8_t)i;

    /*
     * For each length code (lengths 3..258), create a pattern:
     *   - Write a marker pattern
     *   - Write some filler
     *   - Repeat the marker at the target match length
     *
     * This forces the compressor to emit length/distance pairs spanning
     * all length codes.
     */
    static const int target_lengths[] = {
        3, 4, 5, 6, 7, 8, 9, 10,       /* codes 257-264, 0 extra bits */
        11, 12, 13, 14, 15, 16, 17, 18, /* codes 265-268, 1 extra bit */
        19, 22, 23, 26, 27, 30, 31, 34, /* codes 269-272, 2 extra bits */
        35, 42, 43, 50, 51, 58, 59, 66, /* codes 273-276, 3 extra bits */
        67, 82, 83, 98, 99, 114, 115,   /* codes 277-280, 4 extra bits */
        130, 131, 162, 163, 194, 195, 226, 227, 258 /* codes 281-285, 5 extra bits + special 258 */
    };
    int n_lengths = sizeof(target_lengths) / sizeof(target_lengths[0]);

    for (int li = 0; li < n_lengths; li++) {
        int len = target_lengths[li];
        /* Write a unique marker of this length */
        for (int j = 0; j < len && pos < cap; j++)
            data[pos++] = (uint8_t)(0xA0 + (j % 32));
        /* Some filler to separate */
        for (int j = 0; j < 4 && pos < cap; j++)
            data[pos++] = (uint8_t)(0xF0 + li);
        /* Repeat the marker (creates a match of exactly `len` bytes) */
        for (int j = 0; j < len && pos < cap; j++)
            data[pos++] = (uint8_t)(0xA0 + (j % 32));
    }

    test_roundtrip("all_litlen_codes", data, pos, 1);
    test_roundtrip("all_litlen_codes", data, pos, 6);
    test_roundtrip("all_litlen_codes", data, pos, 9);

    free(data);
}

/* ========================================================================== */
/*            (e) Maximum Huffman code length (15 bits)                       */
/* ========================================================================== */

static void test_max_huffman_length(void) {
    printf("\n--- (e) Maximum Huffman code length (15 bits) ---\n");

    /*
     * To get long Huffman codes, we need a heavily skewed frequency
     * distribution. Create data where one byte value dominates and many
     * values appear just once or very rarely.
     *
     * With 256 different symbols and highly skewed frequencies,
     * the Huffman tree can reach depth 15.
     */

    /* Approach 1: One dominant symbol + many rare ones */
    size_t len1 = 100000;
    uint8_t *data1 = malloc(len1);
    if (data1) {
        size_t pos = 0;
        /* 99% of data is byte 0x00 */
        memset(data1, 0x00, len1);
        /* Sprinkle in all 256 byte values very sparsely */
        for (int v = 1; v < 256; v++) {
            /* Place each rare value a few times at random-ish positions */
            size_t step = len1 / 256;
            size_t off = (size_t)v * step;
            if (off < len1)
                data1[off] = (uint8_t)v;
        }
        test_roundtrip("max_huff_skewed", data1, len1, 6);
        test_roundtrip("max_huff_skewed", data1, len1, 9);
        free(data1);
    }

    /* Approach 2: Fibonacci-like frequency distribution (guarantees max depth) */
    size_t len2 = 200000;
    uint8_t *data2 = malloc(len2);
    if (data2) {
        /*
         * Build a distribution where symbol i has frequency proportional to
         * 2^(-i). This forces the Huffman coder into deep trees.
         */
        size_t pos = 0;
        int nsym = 200; /* use 200 different symbols */
        for (int sym = 0; sym < nsym && pos < len2; sym++) {
            /* Higher-numbered symbols get exponentially fewer occurrences */
            size_t count;
            if (sym == 0)
                count = len2 / 2;
            else if (sym < 10)
                count = (len2 / 2) >> sym;
            else
                count = 1;
            if (count == 0) count = 1;
            for (size_t j = 0; j < count && pos < len2; j++)
                data2[pos++] = (uint8_t)(sym & 0xFF);
        }
        /* Fill remaining with dominant symbol */
        while (pos < len2)
            data2[pos++] = 0;

        /* Shuffle to make it more realistic for the compressor */
        prng_seed(42);
        for (size_t i = pos - 1; i > 0; i--) {
            size_t j = prng_next() % (i + 1);
            uint8_t tmp = data2[i];
            data2[i] = data2[j];
            data2[j] = tmp;
        }

        test_roundtrip("max_huff_fibonacci", data2, pos, 6);
        test_roundtrip("max_huff_fibonacci", data2, pos, 9);
        free(data2);
    }

    /* Approach 3: Use Z_HUFFMAN_ONLY strategy to force purely Huffman-coded output */
    size_t len3 = 50000;
    uint8_t *data3 = malloc(len3);
    uint8_t *comp3 = malloc(MAX_COMPRESSED);
    if (data3 && comp3) {
        prng_seed(777);
        /* Skewed: 240 of byte 0x00, rest spread across rare symbols */
        memset(data3, 0x00, len3);
        for (size_t i = 0; i < 256 && i < len3; i++)
            data3[i * (len3 / 256)] = (uint8_t)i;

        size_t comp_len = compress_raw_strategy(data3, len3, comp3, MAX_COMPRESSED,
                                                9, Z_HUFFMAN_ONLY);
        if (comp_len > 0)
            test_precompressed("max_huff_huffonly", comp3, comp_len, data3, len3);

        free(data3);
        free(comp3);
    } else {
        free(data3);
        free(comp3);
    }
}

/* ========================================================================== */
/*     (f) 100+ random valid DEFLATE streams at various compression levels   */
/* ========================================================================== */

static void test_random_streams(void) {
    printf("\n--- (f) 100+ random DEFLATE streams ---\n");

    static const size_t sizes[] = {
        0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64,
        127, 128, 255, 256, 511, 512, 1023, 1024,
        2048, 4096, 8192, 16384, 32768, 65536, 131072
    };
    int nsizes = sizeof(sizes) / sizeof(sizes[0]);

    int count = 0;

    for (int si = 0; si < nsizes; si++) {
        size_t sz = sizes[si];
        if (sz > MAX_INPUT_SIZE) continue;

        uint8_t *data = malloc(sz > 0 ? sz : 1);
        if (!data) continue;

        for (uint32_t seed = 1; seed <= 5; seed++) {
            prng_seed(seed * 1000 + (uint32_t)si);
            prng_fill(data, sz);

            char name[128];
            int level = 1 + (int)((seed + si) % 9);  /* levels 1-9 */
            snprintf(name, sizeof(name), "rand_sz%zu_seed%u", sz, seed);
            test_roundtrip(name, data, sz, level);
            count++;
        }
        free(data);
    }

    /* Additional random streams with varied patterns to reach 100+ total */
    for (uint32_t trial = 0; trial < 60; trial++) {
        prng_seed(10000 + trial);
        size_t sz = (prng_next() % 65536) + 1;
        uint8_t *data = malloc(sz);
        if (!data) continue;

        /* Vary the data pattern */
        switch (trial % 6) {
        case 0: /* Pure random */
            prng_fill(data, sz);
            break;
        case 1: /* Mostly zeros with random spikes */
            memset(data, 0, sz);
            for (size_t i = 0; i < sz / 10; i++)
                data[prng_next() % sz] = prng_byte();
            break;
        case 2: /* Repeating 4-byte pattern with noise */
            for (size_t i = 0; i < sz; i++)
                data[i] = (uint8_t)((i * 3 + 17) & 0xFF);
            for (size_t i = 0; i < sz / 20; i++)
                data[prng_next() % sz] = prng_byte();
            break;
        case 3: /* Two-value alternating */
            for (size_t i = 0; i < sz; i++)
                data[i] = (i & 1) ? 0xAA : 0x55;
            break;
        case 4: /* Ascending then descending */
            for (size_t i = 0; i < sz; i++) {
                size_t half = sz / 2;
                data[i] = (i < half) ? (uint8_t)(i & 0xFF)
                                     : (uint8_t)((sz - i) & 0xFF);
            }
            break;
        case 5: /* Low entropy: only 4 distinct values */
            for (size_t i = 0; i < sz; i++)
                data[i] = (uint8_t)((prng_next() >> 16) & 3);
            break;
        }

        char name[128];
        int level = 1 + (int)(trial % 9);
        snprintf(name, sizeof(name), "rand_trial%u", trial);
        test_roundtrip(name, data, sz, level);
        count++;
        free(data);
    }

    printf("  [%d random stream tests executed]\n", count);
}

/* ========================================================================== */
/*             (g) Very small inputs: 0, 1, 2 bytes                          */
/* ========================================================================== */

static void test_tiny_inputs(void) {
    printf("\n--- (g) Very small inputs ---\n");

    /* 0 bytes (empty) */
    uint8_t empty[1] = {0};
    test_roundtrip("tiny_0bytes", empty, 0, 1);
    test_roundtrip("tiny_0bytes", empty, 0, 6);
    test_roundtrip("tiny_0bytes", empty, 0, 9);

    /* 1 byte: all values */
    for (int v = 0; v < 256; v++) {
        uint8_t b = (uint8_t)v;
        char name[64];
        snprintf(name, sizeof(name), "tiny_1byte_0x%02x", v);
        test_roundtrip(name, &b, 1, 6);
    }

    /* 2 bytes: selected pairs */
    uint8_t pairs[][2] = {
        {0x00, 0x00}, {0xFF, 0xFF}, {0x00, 0xFF}, {0xFF, 0x00},
        {0x41, 0x42}, {0x80, 0x7F}, {0x01, 0xFE}, {0xDE, 0xAD},
    };
    int npairs = sizeof(pairs) / sizeof(pairs[0]);
    for (int i = 0; i < npairs; i++) {
        char name[64];
        snprintf(name, sizeof(name), "tiny_2bytes_%02x%02x", pairs[i][0], pairs[i][1]);
        test_roundtrip(name, pairs[i], 2, 1);
        test_roundtrip(name, pairs[i], 2, 9);
    }
}

/* ========================================================================== */
/*                   (h) Many short blocks                                    */
/* ========================================================================== */

static void test_many_short_blocks(void) {
    printf("\n--- (h) Many short blocks ---\n");

    /*
     * Use zlib's Z_SYNC_FLUSH / Z_FULL_FLUSH between small chunks to force
     * multiple blocks in the output stream.
     */
    uint8_t *input = malloc(65536);
    uint8_t *comp = malloc(MAX_COMPRESSED);
    if (!input || !comp) {
        free(input); free(comp);
        return;
    }

    /* Fill with recognizable pattern */
    for (size_t i = 0; i < 65536; i++)
        input[i] = (uint8_t)((i * 7 + 13) & 0xFF);

    /* Compress with many small flushes to create many blocks */
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, 6, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) != Z_OK) {
        free(input); free(comp);
        return;
    }

    strm.next_out = comp;
    strm.avail_out = (uInt)MAX_COMPRESSED;

    /* Write in small 64-byte chunks with sync flush */
    size_t chunk_size = 64;
    size_t total_in = 65536;
    size_t written = 0;

    for (size_t off = 0; off < total_in; off += chunk_size) {
        size_t this_chunk = (off + chunk_size <= total_in) ? chunk_size : (total_in - off);
        strm.next_in = input + off;
        strm.avail_in = (uInt)this_chunk;
        int flush = (off + this_chunk >= total_in) ? Z_FINISH : Z_SYNC_FLUSH;
        int ret = deflate(&strm, flush);
        if (ret == Z_STREAM_END) break;
        if (ret != Z_OK) {
            fail("many_short_blocks_sync", "deflate with Z_SYNC_FLUSH failed");
            deflateEnd(&strm);
            free(input); free(comp);
            return;
        }
    }
    size_t comp_len = strm.total_out;
    deflateEnd(&strm);

    if (comp_len > 0)
        test_precompressed("many_short_blocks_sync64", comp, comp_len, input, total_in);

    /* Also test with full flush (creates independent blocks) */
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, 4, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) == Z_OK) {
        strm.next_out = comp;
        strm.avail_out = (uInt)MAX_COMPRESSED;

        for (size_t off = 0; off < total_in; off += 128) {
            size_t this_chunk = (off + 128 <= total_in) ? 128 : (total_in - off);
            strm.next_in = input + off;
            strm.avail_in = (uInt)this_chunk;
            int flush = (off + this_chunk >= total_in) ? Z_FINISH : Z_FULL_FLUSH;
            int ret = deflate(&strm, flush);
            if (ret == Z_STREAM_END) break;
            if (ret != Z_OK) break;
        }
        comp_len = strm.total_out;
        deflateEnd(&strm);

        if (comp_len > 0)
            test_precompressed("many_short_blocks_full128", comp, comp_len, input, total_in);
    }

    /* Very small chunks: 8 bytes each with sync flush */
    memset(&strm, 0, sizeof(strm));
    size_t small_total = 4096;
    if (deflateInit2(&strm, 1, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) == Z_OK) {
        strm.next_out = comp;
        strm.avail_out = (uInt)MAX_COMPRESSED;

        for (size_t off = 0; off < small_total; off += 8) {
            size_t this_chunk = (off + 8 <= small_total) ? 8 : (small_total - off);
            strm.next_in = input + off;
            strm.avail_in = (uInt)this_chunk;
            int flush = (off + this_chunk >= small_total) ? Z_FINISH : Z_SYNC_FLUSH;
            int ret = deflate(&strm, flush);
            if (ret == Z_STREAM_END) break;
            if (ret != Z_OK) break;
        }
        comp_len = strm.total_out;
        deflateEnd(&strm);

        if (comp_len > 0)
            test_precompressed("many_short_blocks_tiny8", comp, comp_len, input, small_total);
    }

    /* Mix of stored + compressed blocks: alternate between level 0 and level 6 */
    /* We achieve this by using Z_SYNC_FLUSH with different data patterns */
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, 6, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) == Z_OK) {
        strm.next_out = comp;
        strm.avail_out = (uInt)MAX_COMPRESSED;

        size_t mixed_total = 8192;
        for (size_t off = 0; off < mixed_total; off += 32) {
            size_t this_chunk = (off + 32 <= mixed_total) ? 32 : (mixed_total - off);
            strm.next_in = input + off;
            strm.avail_in = (uInt)this_chunk;
            int flush = (off + this_chunk >= mixed_total) ? Z_FINISH : Z_SYNC_FLUSH;
            int ret = deflate(&strm, flush);
            if (ret == Z_STREAM_END) break;
            if (ret != Z_OK) break;
        }
        comp_len = strm.total_out;
        deflateEnd(&strm);

        if (comp_len > 0)
            test_precompressed("many_short_blocks_mixed32", comp, comp_len, input, mixed_total);
    }

    free(input);
    free(comp);
}

/* ========================================================================== */
/*       (i) Single-byte and two-byte repeated patterns (RLE-heavy)          */
/* ========================================================================== */

static void test_rle_patterns(void) {
    printf("\n--- (i) RLE-heavy patterns ---\n");

    /* Single-byte repeat: all zeros */
    for (size_t sz = 1; sz <= 65536; sz *= 4) {
        uint8_t *data = malloc(sz);
        if (!data) continue;
        memset(data, 0x00, sz);
        char name[64];
        snprintf(name, sizeof(name), "rle_zeros_%zu", sz);
        test_roundtrip(name, data, sz, 1);
        test_roundtrip(name, data, sz, 9);
        free(data);
    }

    /* Single-byte repeat: 0xFF */
    for (size_t sz = 1; sz <= 65536; sz *= 4) {
        uint8_t *data = malloc(sz);
        if (!data) continue;
        memset(data, 0xFF, sz);
        char name[64];
        snprintf(name, sizeof(name), "rle_0xFF_%zu", sz);
        test_roundtrip(name, data, sz, 1);
        test_roundtrip(name, data, sz, 9);
        free(data);
    }

    /* Single-byte repeat: 0x80 */
    {
        size_t sz = 100000;
        uint8_t *data = malloc(sz);
        if (data) {
            memset(data, 0x80, sz);
            test_roundtrip("rle_0x80_100k", data, sz, 6);
            free(data);
        }
    }

    /* Two-byte alternating: 0xAA 0x55 */
    for (size_t sz = 2; sz <= 65536; sz *= 4) {
        uint8_t *data = malloc(sz);
        if (!data) continue;
        for (size_t i = 0; i < sz; i++)
            data[i] = (i & 1) ? 0x55 : 0xAA;
        char name[64];
        snprintf(name, sizeof(name), "rle_alt_aa55_%zu", sz);
        test_roundtrip(name, data, sz, 1);
        test_roundtrip(name, data, sz, 9);
        free(data);
    }

    /* Two-byte pattern: 0x12 0x34 */
    {
        size_t sz = 100000;
        uint8_t *data = malloc(sz);
        if (data) {
            for (size_t i = 0; i < sz; i++)
                data[i] = (i & 1) ? 0x34 : 0x12;
            test_roundtrip("rle_1234_100k", data, sz, 6);
            test_roundtrip("rle_1234_100k", data, sz, 9);
            free(data);
        }
    }

    /* Three-byte pattern: stress distance=3 copy */
    {
        size_t sz = 30000;
        uint8_t *data = malloc(sz);
        if (data) {
            for (size_t i = 0; i < sz; i++)
                data[i] = (uint8_t)("ABC"[i % 3]);
            test_roundtrip("rle_abc_30k", data, sz, 1);
            test_roundtrip("rle_abc_30k", data, sz, 9);
            free(data);
        }
    }

    /* Four-byte pattern: stress distance=4 copy */
    {
        size_t sz = 30000;
        uint8_t *data = malloc(sz);
        if (data) {
            for (size_t i = 0; i < sz; i++)
                data[i] = (uint8_t)("WXYZ"[i % 4]);
            test_roundtrip("rle_wxyz_30k", data, sz, 1);
            test_roundtrip("rle_wxyz_30k", data, sz, 9);
            free(data);
        }
    }

    /* Short period patterns for distances 5..16 */
    for (int period = 5; period <= 16; period++) {
        size_t sz = 10000;
        uint8_t *data = malloc(sz);
        if (!data) continue;
        for (size_t i = 0; i < sz; i++)
            data[i] = (uint8_t)((i % period) * 17 + period);
        char name[64];
        snprintf(name, sizeof(name), "rle_period%d_10k", period);
        test_roundtrip(name, data, sz, 6);
        free(data);
    }

    /* RLE with Z_RLE strategy */
    {
        size_t sz = 50000;
        uint8_t *data = malloc(sz);
        uint8_t *comp = malloc(MAX_COMPRESSED);
        if (data && comp) {
            memset(data, 'X', sz);
            size_t comp_len = compress_raw_strategy(data, sz, comp, MAX_COMPRESSED,
                                                    9, Z_RLE);
            if (comp_len > 0)
                test_precompressed("rle_strategy_X_50k", comp, comp_len, data, sz);

            /* RLE with alternating pattern */
            for (size_t i = 0; i < sz; i++)
                data[i] = (i & 1) ? 0xCD : 0xEF;
            comp_len = compress_raw_strategy(data, sz, comp, MAX_COMPRESSED, 9, Z_RLE);
            if (comp_len > 0)
                test_precompressed("rle_strategy_cdef_50k", comp, comp_len, data, sz);
        }
        free(data);
        free(comp);
    }
}

/* ========================================================================== */
/*                  (j) Maximum match length (258 bytes)                      */
/* ========================================================================== */

static void test_max_match_length(void) {
    printf("\n--- (j) Maximum match length (258 bytes) ---\n");

    /*
     * Create data that forces 258-byte matches. The simplest way is to
     * have long runs of identical data, then the compressor will emit
     * length-258 matches.
     */

    /* Single byte repeated: guaranteed to produce max-length matches */
    {
        size_t sz = 258 * 100; /* many max-length matches */
        uint8_t *data = malloc(sz);
        if (data) {
            memset(data, 'A', sz);
            test_roundtrip("maxmatch_single_25800", data, sz, 1);
            test_roundtrip("maxmatch_single_25800", data, sz, 6);
            test_roundtrip("maxmatch_single_25800", data, sz, 9);
            free(data);
        }
    }

    /* Pattern repeat: 258-byte pattern repeated exactly */
    {
        uint8_t pattern[258];
        prng_seed(999);
        prng_fill(pattern, 258);

        size_t reps = 50;
        size_t sz = 258 * reps;
        uint8_t *data = malloc(sz);
        if (data) {
            for (size_t r = 0; r < reps; r++)
                memcpy(data + r * 258, pattern, 258);
            test_roundtrip("maxmatch_pattern258_x50", data, sz, 1);
            test_roundtrip("maxmatch_pattern258_x50", data, sz, 6);
            test_roundtrip("maxmatch_pattern258_x50", data, sz, 9);
            free(data);
        }
    }

    /* Match of exactly 258 bytes followed by a mismatch, repeated */
    {
        size_t block = 258 + 1; /* 258 match + 1 different */
        size_t reps = 100;
        size_t sz = block * reps * 2 + 258;
        uint8_t *data = malloc(sz);
        if (data) {
            /* First block: the pattern to match against */
            prng_seed(1234);
            prng_fill(data, 258);
            size_t pos = 258;

            /* Add a separator byte */
            data[pos++] = 0xFF;

            /* Repeat: copy the 258-byte pattern + different separator each time */
            for (size_t r = 0; r < reps && pos + 259 <= sz; r++) {
                memcpy(data + pos, data, 258);
                pos += 258;
                data[pos++] = (uint8_t)(r & 0xFF);
            }

            test_roundtrip("maxmatch_258_with_sep", data, pos, 6);
            test_roundtrip("maxmatch_258_with_sep", data, pos, 9);
            free(data);
        }
    }

    /* Edge case: exactly 258 bytes total, all same */
    {
        uint8_t data[258];
        memset(data, 'Z', 258);
        test_roundtrip("maxmatch_exact_258", data, 258, 1);
        test_roundtrip("maxmatch_exact_258", data, 258, 9);
    }

    /* Edge case: 259 bytes (258 match + 1 literal) */
    {
        uint8_t data[259];
        memset(data, 'M', 258);
        data[258] = 'N';
        test_roundtrip("maxmatch_259", data, 259, 1);
        test_roundtrip("maxmatch_259", data, 259, 9);
    }

    /* Long run forcing many consecutive 258-byte matches */
    {
        size_t sz = 258 * 1000;
        uint8_t *data = malloc(sz);
        if (data) {
            memset(data, 0xBB, sz);
            test_roundtrip("maxmatch_run_258k", data, sz, 1);
            test_roundtrip("maxmatch_run_258k", data, sz, 9);
            free(data);
        }
    }
}

/* ========================================================================== */
/*              Additional adversarial tests                                  */
/* ========================================================================== */

static void test_boundary_sizes(void) {
    printf("\n--- Additional: boundary sizes ---\n");

    /* Powers of 2 and nearby values */
    static const size_t boundary_sizes[] = {
        1, 2, 3, 4, 7, 8, 9, 15, 16, 17,
        31, 32, 33, 63, 64, 65,
        127, 128, 129, 255, 256, 257,
        511, 512, 513, 1023, 1024, 1025,
        2047, 2048, 2049, 4095, 4096, 4097,
        8191, 8192, 8193, 16383, 16384, 16385,
        32767, 32768, 32769, 65534, 65535, 65536, 65537,
    };
    int n = sizeof(boundary_sizes) / sizeof(boundary_sizes[0]);

    for (int i = 0; i < n; i++) {
        size_t sz = boundary_sizes[i];
        uint8_t *data = malloc(sz);
        if (!data) continue;
        prng_seed((uint32_t)(sz * 7 + 31));
        prng_fill(data, sz);
        char name[64];
        snprintf(name, sizeof(name), "boundary_%zu", sz);
        test_roundtrip(name, data, sz, 6);
        free(data);
    }
}

static void test_all_strategies(void) {
    printf("\n--- Additional: all zlib strategies ---\n");

    size_t sz = 32768;
    uint8_t *data = malloc(sz);
    uint8_t *comp = malloc(MAX_COMPRESSED);
    if (!data || !comp) {
        free(data); free(comp);
        return;
    }

    /* Fill with text-like data */
    prng_seed(555);
    const char *words[] = {
        "the ", "quick ", "brown ", "fox ", "jumps ", "over ", "the ", "lazy ",
        "dog ", "and ", "sphinx ", "of ", "black ", "quartz ", "judge ", "my ", "vow "
    };
    int nw = sizeof(words) / sizeof(words[0]);
    size_t pos = 0;
    while (pos < sz) {
        const char *w = words[prng_next() % nw];
        size_t wl = strlen(w);
        if (pos + wl > sz) wl = sz - pos;
        memcpy(data + pos, w, wl);
        pos += wl;
    }

    int strategies[] = { Z_DEFAULT_STRATEGY, Z_FILTERED, Z_HUFFMAN_ONLY, Z_RLE, Z_FIXED };
    const char *snames[] = { "default", "filtered", "huffman_only", "rle", "fixed" };
    int nstrat = sizeof(strategies) / sizeof(strategies[0]);

    for (int si = 0; si < nstrat; si++) {
        for (int level = 1; level <= 9; level += 4) {
            size_t comp_len = compress_raw_strategy(data, sz, comp, MAX_COMPRESSED,
                                                    level, strategies[si]);
            if (comp_len > 0) {
                char name[128];
                snprintf(name, sizeof(name), "strategy_%s_L%d", snames[si], level);
                test_precompressed(name, comp, comp_len, data, sz);
            }
        }
    }

    free(data);
    free(comp);
}

static void test_fixed_huffman(void) {
    printf("\n--- Additional: fixed Huffman blocks ---\n");

    /* Z_FIXED forces fixed Huffman tables (btype=1) */
    static const size_t sizes[] = { 1, 10, 100, 1000, 10000, 65536 };
    int nsz = sizeof(sizes) / sizeof(sizes[0]);

    for (int i = 0; i < nsz; i++) {
        size_t sz = sizes[i];
        uint8_t *data = malloc(sz);
        uint8_t *comp = malloc(MAX_COMPRESSED);
        if (!data || !comp) { free(data); free(comp); continue; }

        prng_seed((uint32_t)(sz + 42));
        prng_fill(data, sz);

        size_t comp_len = compress_raw_strategy(data, sz, comp, MAX_COMPRESSED,
                                                6, Z_FIXED);
        if (comp_len > 0) {
            char name[64];
            snprintf(name, sizeof(name), "fixed_huffman_%zu", sz);
            test_precompressed(name, comp, comp_len, data, sz);
        }

        free(data);
        free(comp);
    }
}

static void test_mixed_block_types(void) {
    printf("\n--- Additional: mixed block types via flush ---\n");

    /*
     * Create a stream that mixes dynamic, fixed, and stored blocks by
     * alternating flush strategies. zlib may choose different block types
     * for different data.
     */
    size_t total = 32768;
    uint8_t *input = malloc(total);
    uint8_t *comp = malloc(MAX_COMPRESSED);
    if (!input || !comp) {
        free(input); free(comp);
        return;
    }

    /* Segments: zeros (stored-friendly), random (dynamic), repetitive (fixed-friendly) */
    size_t seg = total / 4;
    memset(input, 0, seg);
    prng_seed(666);
    prng_fill(input + seg, seg);
    for (size_t i = 2 * seg; i < 3 * seg; i++)
        input[i] = (uint8_t)("ABCDEF"[i % 6]);
    for (size_t i = 3 * seg; i < total; i++)
        input[i] = (uint8_t)(i & 0xFF);

    /* Compress with sync flushes between segments */
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (deflateInit2(&strm, 6, Z_DEFLATED, -15, 8, Z_DEFAULT_STRATEGY) == Z_OK) {
        strm.next_out = comp;
        strm.avail_out = (uInt)MAX_COMPRESSED;

        for (size_t off = 0; off < total; off += seg) {
            size_t chunk = (off + seg <= total) ? seg : (total - off);
            strm.next_in = input + off;
            strm.avail_in = (uInt)chunk;
            int flush = (off + chunk >= total) ? Z_FINISH : Z_SYNC_FLUSH;
            int ret = deflate(&strm, flush);
            if (ret == Z_STREAM_END) break;
            if (ret != Z_OK) break;
        }
        size_t comp_len = strm.total_out;
        deflateEnd(&strm);

        if (comp_len > 0)
            test_precompressed("mixed_block_types", comp, comp_len, input, total);
    }

    free(input);
    free(comp);
}

static void test_worst_case_compression(void) {
    printf("\n--- Additional: worst-case (incompressible) data ---\n");

    /* Truly random data: incompressible, exercises literal-heavy paths */
    static const size_t sizes[] = { 1, 100, 1000, 10000, 65536, 131072 };
    int nsz = sizeof(sizes) / sizeof(sizes[0]);

    for (int i = 0; i < nsz; i++) {
        size_t sz = sizes[i];
        uint8_t *data = malloc(sz);
        if (!data) continue;
        prng_seed((uint32_t)(sz * 13 + 7));
        prng_fill(data, sz);
        char name[64];
        snprintf(name, sizeof(name), "incompressible_%zu", sz);
        test_roundtrip(name, data, sz, 1);
        test_roundtrip(name, data, sz, 9);
        free(data);
    }
}

static void test_distance_edge_cases(void) {
    printf("\n--- Additional: distance edge cases ---\n");

    /* Distance = 1 (RLE): byte repeated many times */
    {
        size_t sz = 100000;
        uint8_t *data = malloc(sz);
        if (data) {
            memset(data, 'Q', sz);
            test_roundtrip("dist1_rle_100k", data, sz, 9);
            free(data);
        }
    }

    /* Distance = 2 */
    {
        size_t sz = 50000;
        uint8_t *data = malloc(sz);
        if (data) {
            for (size_t i = 0; i < sz; i++)
                data[i] = (i & 1) ? 0xBB : 0xCC;
            test_roundtrip("dist2_alt_50k", data, sz, 9);
            free(data);
        }
    }

    /* All 30 distance codes: create matches at various distances */
    {
        /* Distance codes cover: 1,2,3,4, 5-6, 7-8, 9-12, 13-16, ..., 24577-32768 */
        static const int target_distances[] = {
            1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193,
            257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145,
            8193, 12289, 16385, 24577
        };
        int nd = sizeof(target_distances) / sizeof(target_distances[0]);

        /* Build data with matches at each target distance */
        size_t sz = 32768 + 4096;
        uint8_t *data = malloc(sz);
        if (data) {
            prng_seed(42);
            prng_fill(data, sz);

            /* For each target distance, copy a 10-byte chunk from that distance */
            size_t pos = 32768;
            for (int di = 0; di < nd && pos + 16 < sz; di++) {
                int dist = target_distances[di];
                if ((size_t)dist > pos) continue;
                memmove(data + pos, data + pos - dist, 10);
                pos += 10;
                /* Add separator to prevent merging */
                data[pos++] = prng_byte();
                data[pos++] = prng_byte();
            }

            test_roundtrip("all_distance_codes", data, pos, 6);
            test_roundtrip("all_distance_codes", data, pos, 9);
            free(data);
        }
    }
}

static void test_output_buffer_exact(void) {
    printf("\n--- Additional: exact output buffer size ---\n");

    /*
     * Test with output buffer exactly the right size (no headroom).
     * This stresses bounds checking in the decoder.
     */
    size_t data_len = 4096;
    uint8_t *data = malloc(data_len);
    uint8_t *comp = malloc(MAX_COMPRESSED);
    uint8_t *out = malloc(data_len);
    if (!data || !comp || !out) {
        free(data); free(comp); free(out);
        return;
    }

    prng_seed(888);
    prng_fill(data, data_len);

    size_t comp_len = compress_raw(data, data_len, comp, MAX_COMPRESSED, 6);
    if (comp_len > 0) {
        /* Decompress into exact-size buffer */
        size_t fd_len = 0;
        int rc = fd_inflate_fast(comp, comp_len, out, data_len, &fd_len);
        if (rc == FD_OK && fd_len == data_len && memcmp(out, data, data_len) == 0) {
            pass("exact_buffer_size_4096");
        } else if (rc == FD_ERROR_SHORT_BUF) {
            /* Some decoders may need a few extra bytes for safety margin - still note it */
            fail("exact_buffer_size_4096", "FD_ERROR_SHORT_BUF (needs larger buffer)");
        } else {
            char msg[128];
            snprintf(msg, sizeof(msg), "rc=%d fd_len=%zu", rc, fd_len);
            fail("exact_buffer_size_4096", msg);
        }
    }

    /* Undersized buffer should return FD_ERROR_SHORT_BUF */
    if (comp_len > 0 && data_len > 10) {
        size_t fd_len = 0;
        int rc = fd_inflate_fast(comp, comp_len, out, data_len / 2, &fd_len);
        if (rc == FD_ERROR_SHORT_BUF) {
            pass("short_buffer_returns_error");
        } else {
            char msg[128];
            snprintf(msg, sizeof(msg), "expected FD_ERROR_SHORT_BUF, got %d", rc);
            fail("short_buffer_returns_error", msg);
        }
    }

    free(data); free(comp); free(out);
}

static void test_large_data(void) {
    printf("\n--- Additional: large data ---\n");

    /* 1 MB of text-like data */
    {
        size_t sz = 1024 * 1024;
        uint8_t *data = malloc(sz);
        if (data) {
            prng_seed(7777);
            const char *words[] = {
                "the ", "quick ", "brown ", "fox ", "jumps ", "over ", "lazy ", "dog ",
                "hello ", "world ", "compress ", "deflate ", "test "
            };
            int nw = 13;
            size_t pos = 0;
            while (pos < sz) {
                const char *w = words[prng_next() % nw];
                size_t wl = strlen(w);
                if (pos + wl > sz) wl = sz - pos;
                memcpy(data + pos, w, wl);
                pos += wl;
            }
            test_roundtrip("large_text_1mb", data, sz, 1);
            test_roundtrip("large_text_1mb", data, sz, 6);
            test_roundtrip("large_text_1mb", data, sz, 9);
            free(data);
        }
    }

    /* 1 MB all zeros */
    {
        size_t sz = 1024 * 1024;
        uint8_t *data = calloc(sz, 1);
        if (data) {
            test_roundtrip("large_zeros_1mb", data, sz, 1);
            test_roundtrip("large_zeros_1mb", data, sz, 9);
            free(data);
        }
    }

    /* 1 MB random (incompressible) */
    {
        size_t sz = 1024 * 1024;
        uint8_t *data = malloc(sz);
        if (data) {
            prng_seed(9876);
            prng_fill(data, sz);
            test_roundtrip("large_random_1mb", data, sz, 1);
            test_roundtrip("large_random_1mb", data, sz, 6);
            free(data);
        }
    }
}

/* ========================================================================== */
/*                              Main                                          */
/* ========================================================================== */

int main(void) {
    printf("======================================================\n");
    printf("  Adversarial DEFLATE Test Suite for fd_inflate_fast\n");
    printf("======================================================\n");

    /* (a) Empty DEFLATE stream */
    test_empty_stream();

    /* (b) Stored blocks */
    test_stored_blocks();

    /* (c) Maximum back-reference distance */
    test_max_distance();

    /* (d) All 286 literal/length codes */
    test_all_litlen_codes();

    /* (e) Maximum Huffman code length */
    test_max_huffman_length();

    /* (f) 100+ random streams */
    test_random_streams();

    /* (g) Very small inputs */
    test_tiny_inputs();

    /* (h) Many short blocks */
    test_many_short_blocks();

    /* (i) RLE-heavy patterns */
    test_rle_patterns();

    /* (j) Maximum match length */
    test_max_match_length();

    /* Additional adversarial tests */
    test_boundary_sizes();
    test_all_strategies();
    test_fixed_huffman();
    test_mixed_block_types();
    test_worst_case_compression();
    test_distance_edge_cases();
    test_output_buffer_exact();
    test_large_data();

    /* Summary */
    printf("\n======================================================\n");
    printf("  RESULTS: %d / %d passed, %d failed\n",
           g_tests_passed, g_tests_run, g_tests_failed);
    printf("======================================================\n");

    return g_tests_failed > 0 ? 1 : 0;
}
