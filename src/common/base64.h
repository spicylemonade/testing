/*
 * base64.h - Public API for SIMD-accelerated Base64 decoding
 *
 * RFC 4648 compliant decoder with support for standard Base64 and Base64url.
 * All implementations (scalar, AVX2, AVX-512, NEON, SVE) share this API.
 */
#ifndef BASE64_H
#define BASE64_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Error codes */
typedef enum {
    BASE64_OK           =  0,  /* Success */
    BASE64_ERR_INVALID  = -1,  /* Invalid character in input */
    BASE64_ERR_PADDING  = -2,  /* Invalid padding */
    BASE64_ERR_LENGTH   = -3,  /* Invalid input length (not multiple of 4, if strict) */
    BASE64_ERR_OUTPUT   = -4,  /* Output buffer too small */
    BASE64_ERR_NULL     = -5,  /* NULL pointer argument */
} base64_status_t;

/* Alphabet variant */
typedef enum {
    BASE64_STANDARD = 0,  /* A-Z, a-z, 0-9, +, /  (RFC 4648 Section 4) */
    BASE64_URL      = 1,  /* A-Z, a-z, 0-9, -, _  (RFC 4648 Section 5) */
} base64_variant_t;

/*
 * Compute the maximum decoded output size for a given Base64 input.
 * Returns the number of bytes needed for the output buffer.
 */
static inline size_t base64_decode_maxlen(size_t input_len) {
    return (input_len / 4) * 3 + 3; /* Conservative: up to 3 extra bytes */
}

/*
 * base64_decode_scalar - Decode Base64 data using scalar algorithm
 *
 * Parameters:
 *   input      - Base64-encoded input data
 *   input_len  - Length of input data in bytes
 *   output     - Buffer for decoded output (must be at least base64_decode_maxlen(input_len))
 *   output_len - [in/out] On entry: size of output buffer; on exit: bytes written
 *   variant    - BASE64_STANDARD or BASE64_URL
 *
 * Returns BASE64_OK on success, or an error code.
 * On error, *output_len is set to the number of bytes successfully decoded before the error.
 */
base64_status_t base64_decode_scalar(
    const uint8_t *input,
    size_t input_len,
    uint8_t *output,
    size_t *output_len,
    base64_variant_t variant
);

/*
 * Forward declarations for SIMD implementations (defined in respective files)
 */
base64_status_t base64_decode_avx2(
    const uint8_t *input, size_t input_len,
    uint8_t *output, size_t *output_len,
    base64_variant_t variant
);

base64_status_t base64_decode_avx512(
    const uint8_t *input, size_t input_len,
    uint8_t *output, size_t *output_len,
    base64_variant_t variant
);

base64_status_t base64_decode_neon(
    const uint8_t *input, size_t input_len,
    uint8_t *output, size_t *output_len,
    base64_variant_t variant
);

base64_status_t base64_decode_sve(
    const uint8_t *input, size_t input_len,
    uint8_t *output, size_t *output_len,
    base64_variant_t variant
);

#ifdef __cplusplus
}
#endif

#endif /* BASE64_H */
