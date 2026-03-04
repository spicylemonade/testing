/*
 * fast_deflate.h - High-performance DEFLATE decompressor
 *
 * Public API for the fast DEFLATE decompression library.
 * Drop-in replacement for zlib inflate, targeting >=2x throughput
 * over zlib-ng on modern x86-64 hardware.
 *
 * RFC 1951 compliant.
 */

#ifndef FAST_DEFLATE_H
#define FAST_DEFLATE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Return codes */
#define FD_OK              0
#define FD_ERROR_BAD_DATA  (-1)
#define FD_ERROR_SHORT_BUF (-2)
#define FD_ERROR_BAD_BLOCK (-3)
#define FD_ERROR_INTERNAL  (-4)

/*
 * Decompress a raw DEFLATE stream (RFC 1951).
 *
 * Parameters:
 *   src       - pointer to compressed data
 *   src_len   - length of compressed data in bytes
 *   dst       - pointer to output buffer (must be pre-allocated)
 *   dst_len   - capacity of output buffer in bytes
 *   out_len   - on success, set to the actual decompressed size
 *
 * Returns:
 *   FD_OK on success, or a negative error code.
 */
int fd_inflate(const uint8_t *src, size_t src_len,
               uint8_t *dst, size_t dst_len,
               size_t *out_len);

/*
 * Decompress using the optimized fast decoder.
 * Same API as fd_inflate but uses all optimizations.
 */
int fd_inflate_fast(const uint8_t *src, size_t src_len,
                    uint8_t *dst, size_t dst_len,
                    size_t *out_len);

#ifdef __cplusplus
}
#endif

#endif /* FAST_DEFLATE_H */
