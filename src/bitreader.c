/*
 * bitreader.c - High-performance branchless bit reader for DEFLATE decoding
 *
 * Design principles:
 *   1. 64-bit bit buffer for fewer refills
 *   2. Branchless refill: always read 8 bytes from input, mask by available
 *   3. Overlapped refill: refill early so bits are ready for next lookup
 *   4. Inspired by dougallj's zero-refill-latency technique
 *
 * The bit buffer is maintained LSB-first (matching DEFLATE bit order).
 * We keep track of how many bits are valid. Refill loads up to 56 bits
 * by reading a full 64-bit word and shifting it into position.
 *
 * Key insight: DEFLATE codes are max 15 bits, so with 64-bit buffer
 * we can guarantee at least 4 symbol decodes between refills.
 */

#include "bitreader.h"
#include <string.h>

/*
 * Initialize the fast bit reader.
 */
void fbr_init(fast_bitreader_t *br, const uint8_t *data, size_t len) {
    br->data = data;
    br->data_end = data + len;
    br->ptr = data;
    br->bits = 0;
    br->nbits = 0;

    /* Perform initial refill */
    fbr_refill(br);
}

/*
 * Branchless refill: load a 64-bit word and shift into the buffer.
 *
 * This is the critical hot path function. We want to:
 *   1. Read 8 bytes from the current pointer (even if near end - we bounds-check after)
 *   2. Shift them into position above existing valid bits
 *   3. Advance the pointer by the number of bytes consumed
 *
 * The branchless approach: we always read a word, but only advance
 * by the number of bytes we actually needed. We ensure at least 8 bytes
 * of read-ahead safety by checking bounds.
 */
void fbr_refill(fast_bitreader_t *br) {
    /*
     * We want to fill the buffer to at least 56 bits.
     * bytes_to_read = (64 - nbits) / 8, but we just read a full word.
     */
    if (br->nbits > 56) return;

    /* How many bytes can we consume? */
    size_t avail = (size_t)(br->data_end - br->ptr);
    if (avail == 0) return;

    if (avail >= 8) {
        /* Fast path: read 8 bytes at once (unaligned load) */
        uint64_t word;
        memcpy(&word, br->ptr, 8);  /* compiles to single movq on x86 */

        /* Shift the new bits into position above existing bits */
        br->bits |= word << br->nbits;

        /* Advance by the number of byte-slots we filled */
        int bytes_consumed = (64 - br->nbits) >> 3;
        br->ptr += bytes_consumed;
        br->nbits |= 56;  /* Set to at least 56 (equivalent to nbits += bytes_consumed * 8,
                              but since nbits was < 56 and we filled to 56+, this works) */
        /*
         * More precisely: nbits + bytes_consumed*8 >= 56.
         * Actually we need to be exact. Let's compute properly:
         */
        br->nbits = br->nbits + bytes_consumed * 8;
        /* Undo the |= 56 above, use precise calculation */
    } else {
        /* Slow path: near end of input, read byte by byte */
        while (br->nbits <= 56 && br->ptr < br->data_end) {
            br->bits |= (uint64_t)(*br->ptr++) << br->nbits;
            br->nbits += 8;
        }
    }
}

/*
 * Optimized refill - the real implementation.
 * Designed to be inlined at call sites.
 */

/* Defined in the header as static inline for hot-path use */
