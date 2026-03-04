/*
 * test_scalar.c - Test suite for scalar Base64 decoder
 *
 * Tests RFC 4648 compliance including edge cases, invalid inputs,
 * padding handling, and Base64url variant.
 * Target: 50+ test vectors.
 */

#include "../src/common/base64.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) do { \
    tests_run++; \
    printf("  [%3d] %-60s ", tests_run, name); \
} while(0)

#define PASS() do { tests_passed++; printf("PASS\n"); } while(0)
#define FAIL(msg) do { tests_failed++; printf("FAIL: %s\n", msg); } while(0)

/* Helper: decode and check against expected output */
static void test_decode(const char *name, const char *input,
                        const uint8_t *expected, size_t expected_len,
                        base64_status_t expected_status,
                        base64_variant_t variant)
{
    TEST(name);

    size_t input_len = strlen(input);
    uint8_t out[4096];
    size_t out_len = sizeof(out);

    base64_status_t status = base64_decode_scalar(
        (const uint8_t *)input, input_len, out, &out_len, variant);

    if (status != expected_status) {
        char msg[128];
        snprintf(msg, sizeof(msg), "status=%d, expected=%d", status, expected_status);
        FAIL(msg);
        return;
    }

    if (expected_status == BASE64_OK) {
        if (out_len != expected_len) {
            char msg[128];
            snprintf(msg, sizeof(msg), "out_len=%zu, expected=%zu", out_len, expected_len);
            FAIL(msg);
            return;
        }
        if (expected_len > 0 && memcmp(out, expected, expected_len) != 0) {
            FAIL("output mismatch");
            return;
        }
    }

    PASS();
}

/* Helper for string-based expected outputs */
static void test_decode_str(const char *name, const char *input,
                            const char *expected, base64_variant_t variant)
{
    test_decode(name, input, (const uint8_t *)expected, strlen(expected),
                BASE64_OK, variant);
}

/* Helper for error-expected tests */
static void test_decode_err(const char *name, const char *input,
                            base64_status_t expected_status,
                            base64_variant_t variant)
{
    TEST(name);

    size_t input_len = strlen(input);
    uint8_t out[4096];
    size_t out_len = sizeof(out);

    base64_status_t status = base64_decode_scalar(
        (const uint8_t *)input, input_len, out, &out_len, variant);

    if (status != expected_status) {
        char msg[128];
        snprintf(msg, sizeof(msg), "status=%d, expected=%d", status, expected_status);
        FAIL(msg);
        return;
    }
    PASS();
}

int main(void)
{
    printf("=== Scalar Base64 Decoder Test Suite ===\n\n");

    /* --- RFC 4648 Section 10 Test Vectors --- */
    printf("RFC 4648 test vectors:\n");
    test_decode("RFC4648: empty", "", (const uint8_t *)"", 0, BASE64_OK, BASE64_STANDARD);
    test_decode_str("RFC4648: f", "Zg==", "f", BASE64_STANDARD);
    test_decode_str("RFC4648: fo", "Zm8=", "fo", BASE64_STANDARD);
    test_decode_str("RFC4648: foo", "Zm9v", "foo", BASE64_STANDARD);
    test_decode_str("RFC4648: foob", "Zm9vYg==", "foob", BASE64_STANDARD);
    test_decode_str("RFC4648: fooba", "Zm9vYmE=", "fooba", BASE64_STANDARD);
    test_decode_str("RFC4648: foobar", "Zm9vYmFy", "foobar", BASE64_STANDARD);

    /* --- Single character outputs --- */
    printf("\nSingle byte outputs:\n");
    {
        uint8_t zero = 0;
        test_decode("Decode \\x00", "AA==", &zero, 1, BASE64_OK, BASE64_STANDARD);
    }
    {
        uint8_t ff = 0xFF;
        test_decode("Decode \\xFF", "/w==", &ff, 1, BASE64_OK, BASE64_STANDARD);
    }
    test_decode_str("Decode 'A' (0x41)", "QQ==", "A", BASE64_STANDARD);
    test_decode_str("Decode 'Z' (0x5A)", "Wg==", "Z", BASE64_STANDARD);

    /* --- Two and three byte outputs --- */
    printf("\nMulti-byte outputs:\n");
    {
        uint8_t two[] = {0x00, 0x00};
        test_decode("Decode \\x00\\x00", "AAA=", two, 2, BASE64_OK, BASE64_STANDARD);
    }
    {
        uint8_t three[] = {0x00, 0x00, 0x00};
        test_decode("Decode \\x00\\x00\\x00", "AAAA", three, 3, BASE64_OK, BASE64_STANDARD);
    }
    {
        uint8_t three[] = {0xFF, 0xFF, 0xFF};
        test_decode("Decode \\xFF\\xFF\\xFF", "////", three, 3, BASE64_OK, BASE64_STANDARD);
    }

    /* --- Padding handling --- */
    printf("\nPadding handling:\n");
    test_decode_str("No padding (3n bytes)", "Zm9v", "foo", BASE64_STANDARD);
    test_decode_str("Single pad (3n+2 bytes)", "Zm9vYmE=", "fooba", BASE64_STANDARD);
    test_decode_str("Double pad (3n+1 bytes)", "Zm9vYg==", "foob", BASE64_STANDARD);

    /* Without padding (lenient) */
    test_decode_str("No pad where == expected", "Zg", "f", BASE64_STANDARD);
    test_decode_str("No pad where = expected", "Zm8", "fo", BASE64_STANDARD);

    /* --- Base64url variant --- */
    printf("\nBase64url variant:\n");
    test_decode_str("URL: basic", "Zm9v", "foo", BASE64_URL);
    {
        /* Base64url: - is value 62 (same as + in standard), _ is value 63 (same as / in standard) */
        /* "---_" in url: 62,62,62,63 -> same as "+++/" in standard */
        /* 62=0x3E, 62=0x3E, 62=0x3E, 63=0x3F */
        /* byte0 = (62<<2)|(62>>4) = 248|3 = 0xFB */
        /* byte1 = ((62&0xF)<<4)|(62>>2) = (14<<4)|15 = 224|15 = 0xEF */
        /* byte2 = ((62&0x3)<<6)|63 = (2<<6)|63 = 128|63 = 0xBF */
        uint8_t data[] = {0xFB, 0xEF, 0xBF};
        test_decode("URL: - and _ chars", "---_", data, 3, BASE64_OK, BASE64_URL);
    }
    {
        uint8_t ff3[] = {0xFF, 0xFF, 0xFF};
        test_decode("URL: _ replaces /", "____", ff3, 3, BASE64_OK, BASE64_URL);
    }
    test_decode_str("URL: no pad", "Zg", "f", BASE64_URL);

    /* --- Invalid character detection --- */
    printf("\nInvalid character detection:\n");
    /* Tests with invalid chars in a 4-byte group (explicit length to avoid strlen issues) */
    {
        TEST("Invalid: space in group");
        uint8_t in[] = {'Z','m',' ','v'};
        uint8_t out[16]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(in, 4, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_INVALID) PASS(); else { char m[64]; snprintf(m,64,"status=%d",st); FAIL(m); }
    }
    {
        TEST("Invalid: tab in group");
        uint8_t in[] = {'Z','m','\t','v'};
        uint8_t out[16]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(in, 4, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_INVALID) PASS(); else { char m[64]; snprintf(m,64,"status=%d",st); FAIL(m); }
    }
    {
        TEST("Invalid: newline in group");
        uint8_t in[] = {'Z','m','\n','v'};
        uint8_t out[16]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(in, 4, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_INVALID) PASS(); else { char m[64]; snprintf(m,64,"status=%d",st); FAIL(m); }
    }
    {
        TEST("Invalid: byte 0x00 in group");
        uint8_t in[] = {'Z','m',0x00,'v'};
        uint8_t out[16]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(in, 4, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_INVALID) PASS(); else { char m[64]; snprintf(m,64,"status=%d",st); FAIL(m); }
    }
    test_decode_err("Invalid: byte 0x80", "Zm\x80v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Invalid: byte 0xFF", "Zm\xFFv", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Invalid: @ symbol", "Zm@v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Invalid: [ bracket", "Zm[v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Invalid: { brace", "Zm{v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Invalid: ~ tilde", "Zm~v", BASE64_ERR_INVALID, BASE64_STANDARD);

    /* Cross-variant rejection */
    test_decode_err("Std rejects URL -", "Zm-v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("Std rejects URL _", "Zm_v", BASE64_ERR_INVALID, BASE64_STANDARD);
    test_decode_err("URL rejects std +", "Zm+v", BASE64_ERR_INVALID, BASE64_URL);
    test_decode_err("URL rejects std /", "Zm/v", BASE64_ERR_INVALID, BASE64_URL);

    /* --- Padding errors --- */
    printf("\nPadding errors:\n");
    test_decode_err("Triple pad ===", "Z===", BASE64_ERR_PADDING, BASE64_STANDARD);
    test_decode_err("Quad pad ====", "====", BASE64_ERR_PADDING, BASE64_STANDARD);
    test_decode_err("Single char only", "Z", BASE64_ERR_LENGTH, BASE64_STANDARD);

    /* --- Length edge cases --- */
    printf("\nLength edge cases:\n");
    test_decode("Empty input", "", (const uint8_t *)"", 0, BASE64_OK, BASE64_STANDARD);

    /* Longer inputs */
    {
        /* "Hello, World!" = "SGVsbG8sIFdvcmxkIQ==" */
        test_decode_str("Hello, World!", "SGVsbG8sIFdvcmxkIQ==", "Hello, World!", BASE64_STANDARD);
    }
    {
        /* "The quick brown fox jumps over the lazy dog" */
        test_decode_str("Quick brown fox",
            "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZw==",
            "The quick brown fox jumps over the lazy dog", BASE64_STANDARD);
    }

    /* --- All 64 standard characters --- */
    printf("\nAlphabet coverage:\n");
    {
        /* Test that each valid Base64 character decodes correctly */
        const char *all_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        uint8_t out[256];
        size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(
            (const uint8_t *)all_chars, 64, out, &out_len, BASE64_STANDARD);
        TEST("All 64 standard chars decode OK");
        if (st == BASE64_OK && out_len == 48) PASS(); else FAIL("bad decode");
    }
    {
        const char *all_url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
        uint8_t out[256];
        size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar(
            (const uint8_t *)all_url, 64, out, &out_len, BASE64_URL);
        TEST("All 64 URL chars decode OK");
        if (st == BASE64_OK && out_len == 48) PASS(); else FAIL("bad decode");
    }

    /* --- All-same-character inputs --- */
    printf("\nAll-same-character inputs:\n");
    {
        char aaa[64]; memset(aaa, 'A', 64);
        uint8_t out[256]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar((const uint8_t *)aaa, 64, out, &out_len, BASE64_STANDARD);
        TEST("64x 'A' (all zeros)");
        if (st == BASE64_OK && out_len == 48) {
            int ok = 1;
            for (size_t j = 0; j < 48; j++) if (out[j] != 0) ok = 0;
            if (ok) PASS(); else FAIL("not all zeros");
        } else FAIL("bad status/len");
    }
    {
        char slash[64]; memset(slash, '/', 64);
        uint8_t out[256]; size_t out_len = sizeof(out);
        base64_status_t st = base64_decode_scalar((const uint8_t *)slash, 64, out, &out_len, BASE64_STANDARD);
        TEST("64x '/' (all 0xFF)");
        if (st == BASE64_OK && out_len == 48) {
            int ok = 1;
            for (size_t j = 0; j < 48; j++) if (out[j] != 0xFF) ok = 0;
            if (ok) PASS(); else FAIL("not all 0xFF");
        } else FAIL("bad status/len");
    }

    /* --- NULL pointer handling --- */
    printf("\nNULL pointer handling:\n");
    {
        TEST("NULL output_len");
        base64_status_t st = base64_decode_scalar((const uint8_t *)"Zm9v", 4, NULL, NULL, BASE64_STANDARD);
        if (st == BASE64_ERR_NULL) PASS(); else FAIL("expected NULL error");
    }
    {
        size_t out_len = 100;
        TEST("NULL input with len > 0");
        base64_status_t st = base64_decode_scalar(NULL, 10, NULL, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_NULL) PASS(); else FAIL("expected NULL error");
    }
    {
        uint8_t out[16]; size_t out_len = sizeof(out);
        TEST("NULL input with len = 0");
        base64_status_t st = base64_decode_scalar(NULL, 0, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_OK && out_len == 0) PASS(); else FAIL("expected OK/empty");
    }

    /* --- Output buffer too small --- */
    printf("\nOutput buffer capacity:\n");
    {
        uint8_t out[2]; size_t out_len = 2; /* Need 3 bytes */
        TEST("Output buffer too small");
        base64_status_t st = base64_decode_scalar((const uint8_t *)"Zm9v", 4, out, &out_len, BASE64_STANDARD);
        if (st == BASE64_ERR_OUTPUT) PASS(); else FAIL("expected OUTPUT error");
    }

    /* --- Specific byte value tests --- */
    printf("\nSpecific byte values:\n");
    {
        /* Every byte value from 0x00 to 0x0F */
        const char *hex_low = "AAECAwQFBgcICQoLDA0ODw==";
        uint8_t expected[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
        test_decode("Bytes 0x00-0x0F", hex_low, expected, 16, BASE64_OK, BASE64_STANDARD);
    }
    {
        /* Byte values 0xF0-0xFF */
        const char *hex_high = "8PHy8/T19vf4+fr7/P3+/w==";
        uint8_t expected[] = {0xF0,0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,
                              0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF};
        test_decode("Bytes 0xF0-0xFF", hex_high, expected, 16, BASE64_OK, BASE64_STANDARD);
    }

    /* --- Round-trip correctness for various lengths --- */
    printf("\nVarious output lengths (1-12 bytes):\n");
    /* Pre-encoded test vectors for lengths 1 through 12 */
    test_decode_str("1 byte: 'a'", "YQ==", "a", BASE64_STANDARD);
    test_decode_str("2 bytes: 'ab'", "YWI=", "ab", BASE64_STANDARD);
    test_decode_str("3 bytes: 'abc'", "YWJj", "abc", BASE64_STANDARD);
    test_decode_str("4 bytes: 'abcd'", "YWJjZA==", "abcd", BASE64_STANDARD);
    test_decode_str("5 bytes: 'abcde'", "YWJjZGU=", "abcde", BASE64_STANDARD);
    test_decode_str("6 bytes: 'abcdef'", "YWJjZGVm", "abcdef", BASE64_STANDARD);
    test_decode_str("7 bytes: 'abcdefg'", "YWJjZGVmZw==", "abcdefg", BASE64_STANDARD);
    test_decode_str("8 bytes: 'abcdefgh'", "YWJjZGVmZ2g=", "abcdefgh", BASE64_STANDARD);
    test_decode_str("9 bytes: 'abcdefghi'", "YWJjZGVmZ2hp", "abcdefghi", BASE64_STANDARD);
    test_decode_str("10 bytes: 'abcdefghij'", "YWJjZGVmZ2hpag==", "abcdefghij", BASE64_STANDARD);
    test_decode_str("11 bytes: 'abcdefghijk'", "YWJjZGVmZ2hpams=", "abcdefghijk", BASE64_STANDARD);
    test_decode_str("12 bytes: 'abcdefghijkl'", "YWJjZGVmZ2hpamts", "abcdefghijkl", BASE64_STANDARD);

    /* --- Summary --- */
    printf("\n=== Results: %d/%d passed, %d failed ===\n",
           tests_passed, tests_run, tests_failed);

    return tests_failed > 0 ? 1 : 0;
}
