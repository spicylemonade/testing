#pragma once
// LUT-based GCD: precomputed table for small operands + hybrid approach
#include <cstdint>
#include <cstdlib>

namespace gcd_novel {

// ============================================================
// Precomputed GCD lookup table for 8-bit operands
// Size: 256 * 256 = 65536 bytes = 64KB (fits in L1 cache)
// ============================================================

struct GcdLut {
    uint8_t table[256][256];
    
    constexpr GcdLut() : table{} {
        for (int a = 0; a < 256; a++) {
            for (int b = 0; b < 256; b++) {
                // Compute gcd using Euclidean
                int x = a, y = b;
                while (y) { int t = y; y = x % y; x = t; }
                table[a][b] = static_cast<uint8_t>(x);
            }
        }
    }
};

// Runtime-initialized lookup table (constexpr may exceed step limit)
static const GcdLut gcd_lut_8bit{};

// ============================================================
// Hybrid binary GCD with LUT early termination
// When both operands fit in 8 bits, use O(1) table lookup
// ============================================================

__attribute__((noinline))
uint64_t gcd_lut_hybrid(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Fast path: both small
    if (a < 256 && b < 256) {
        return gcd_lut_8bit.table[a][b];
    }

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    a >>= az;
    b >>= bz;

    while (a != b) {
        // Check if both fit in LUT (after stripping trailing zeros, they're odd and possibly small)
        if (a < 256 && b < 256) {
            uint64_t g = gcd_lut_8bit.table[a][b];
            return g << shift;
        }
        uint64_t diff = (a > b) ? (a - b) : (b - a);
        b = (a < b) ? a : b;
        a = diff >> __builtin_ctzll(diff);
    }
    return a << shift;
}

// ============================================================
// LUT hybrid with initial modular reduction for skewed inputs
// ============================================================

__attribute__((noinline))
uint64_t gcd_lut_hybrid_mod(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Initial reduction
    if (a > b) { uint64_t t = a; a = b; b = t; }
    b %= a;
    if (b == 0) return a;
    
    // Fast path: both small
    if (a < 256 && b < 256) {
        return gcd_lut_8bit.table[a][b];
    }

    int shift = __builtin_ctzll(a | b);
    a >>= __builtin_ctzll(a);
    b >>= __builtin_ctzll(b);

    while (a != b) {
        if (a < 256 && b < 256) {
            return gcd_lut_8bit.table[a][b] << shift;
        }
        uint64_t diff = (a > b) ? (a - b) : (b - a);
        b = (a < b) ? a : b;
        a = diff >> __builtin_ctzll(diff);
    }
    return a << shift;
}

} // namespace gcd_novel
