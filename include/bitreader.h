/*
 * bitreader.h - High-performance branchless bit reader for DEFLATE decoding
 *
 * 64-bit bit buffer, LSB-first (DEFLATE bit order).
 * Branchless refill via unaligned 64-bit loads.
 *
 * All hot-path functions are static inline for maximum performance.
 */

#ifndef BITREADER_H
#define BITREADER_H

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    const uint8_t *data;      /* start of input */
    const uint8_t *data_end;  /* end of input */
    const uint8_t *ptr;       /* current read position */
    uint64_t       bits;      /* bit accumulator (LSB-first) */
    int            nbits;     /* number of valid bits in accumulator */
} fast_bitreader_t;

/*
 * Initialize the bit reader.
 */
static inline void fbr_init(fast_bitreader_t *br, const uint8_t *data, size_t len) {
    br->data = data;
    br->data_end = data + len;
    br->ptr = data;
    br->bits = 0;
    br->nbits = 0;
}

/*
 * Branchless refill: ensure at least 56 bits are in the buffer.
 *
 * Uses a single unaligned 64-bit load when possible.
 * After refill, nbits >= 56 (unless near end of input).
 *
 * This is the critical hot-path function, called once per 1-4 symbol decodes.
 */
static inline void fbr_refill(fast_bitreader_t *br) {
    /*
     * Key insight: we can always load 8 bytes as long as we have >= 8 bytes
     * remaining. This avoids byte-at-a-time refill loops entirely.
     *
     * We need to refill (64 - nbits) / 8 bytes. Rather than computing this,
     * we just load a full 64-bit word shifted into position, then advance
     * the pointer by exactly the bytes consumed.
     */
    if (__builtin_expect(br->ptr + 8 <= br->data_end, 1)) {
        /* Fast path: plenty of input remaining */
        uint64_t word;
        memcpy(&word, br->ptr, 8);  /* compiles to movq on x86-64 */

        br->bits |= word << br->nbits;

        /* Advance by number of bytes we can consume (fill remaining slots) */
        unsigned bytes = (unsigned)(63 - br->nbits) >> 3;
        br->ptr += bytes;
        br->nbits += (int)(bytes << 3);
    } else {
        /* Slow path: near end of input, byte-at-a-time */
        while (br->nbits <= 56 && br->ptr < br->data_end) {
            br->bits |= (uint64_t)(*br->ptr++) << br->nbits;
            br->nbits += 8;
        }
    }
}

/*
 * Ensure we have at least `n` bits available.
 * Call this before peek/consume sequences.
 */
static inline void fbr_ensure(fast_bitreader_t *br, int n) {
    if (__builtin_expect(br->nbits < n, 0)) {
        fbr_refill(br);
    }
}

/*
 * Peek at the bottom `n` bits without consuming them.
 * Caller must ensure nbits >= n (via fbr_refill or fbr_ensure).
 */
static inline uint64_t fbr_peek(fast_bitreader_t *br, int n) {
    return br->bits & ((1ULL << n) - 1);
}

/*
 * Consume `n` bits from the buffer. Caller must ensure nbits >= n.
 */
static inline void fbr_consume(fast_bitreader_t *br, int n) {
    br->bits >>= n;
    br->nbits -= n;
}

/*
 * Read `n` bits: refill if needed, peek, consume, return.
 * For the hot path, prefer separate refill/peek/consume.
 */
static inline uint64_t fbr_read(fast_bitreader_t *br, int n) {
    if (n == 0) return 0;
    fbr_ensure(br, n);
    uint64_t val = fbr_peek(br, n);
    fbr_consume(br, n);
    return val;
}

/*
 * Peek + consume in one call (for use after fbr_refill).
 * Slightly more efficient than separate calls.
 */
static inline uint64_t fbr_read_fast(fast_bitreader_t *br, int n) {
    uint64_t val = br->bits & ((1ULL << n) - 1);
    br->bits >>= n;
    br->nbits -= n;
    return val;
}

/*
 * Align to byte boundary (discard remaining bits in current byte).
 */
static inline void fbr_align_byte(fast_bitreader_t *br) {
    int skip = br->nbits & 7;
    br->bits >>= skip;
    br->nbits -= skip;
}

/*
 * Check if we've consumed all input.
 */
static inline int fbr_done(fast_bitreader_t *br) {
    return br->ptr >= br->data_end && br->nbits <= 0;
}

/*
 * Get remaining bytes in input (approximate, for bounds checking).
 */
static inline size_t fbr_remaining(fast_bitreader_t *br) {
    return (size_t)(br->data_end - br->ptr) + (size_t)(br->nbits >> 3);
}

#ifdef __cplusplus
}
#endif

#endif /* BITREADER_H */
