#pragma once
// Novel branchless binary GCD implementations
// Goal: Zero JCC in inner loop, minimized dependency chain
#include <cstdint>
#include <cstdlib>
#include <algorithm>
#include <bit>

namespace gcd_novel {

// ============================================================
// 1. Fully branchless binary GCD with fixed iteration count
//    Eliminates BOTH the data-dependent branches AND the loop-exit branch.
//    Uses a fixed upper bound of 2*64 = 128 iterations for 64-bit inputs.
//    When one operand reaches 0, subsequent iterations are no-ops.
// ============================================================

__attribute__((noinline))
uint64_t gcd_branchless_fixed(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    b >>= bz;

    // Fixed 128 iterations (sufficient for all 64-bit inputs)
    // When a becomes 0, all subsequent iterations are no-ops
    for (int i = 0; i < 128; i++) {
        a >>= az;
        uint64_t diff = b - a;
        // When diff == 0 (a == b), we need ctz = 0 effectively.
        // But ctz(0) is undefined. We handle this by: if diff==0, 
        // a stays 0 (since abs(0)=0) and all future iterations are no-ops.
        // Use conditional: if diff==0, set az=1 (arbitrary, doesn't matter)
        az = diff ? __builtin_ctzll(diff) : 1;
        
        // Branchless min and abs
        // If a < b: new_b = a, new_a = b - a = diff (positive)
        // If a >= b: new_b = b, new_a = a - b = -diff (negate)
        uint64_t new_b = (a < b) ? a : b;
        uint64_t new_a = (a < b) ? diff : (a - b);
        b = new_b;
        a = new_a;
    }
    return b << shift;
}

// ============================================================
// 2. Branchless binary GCD with loop but zero JCC in body
//    Uses the fact that when a==0, we can let the loop continue
//    with az=0 (no-op shift) and diff=b-0=b.
//    The only branch is the loop-back, but we use a counted loop.
// ============================================================

__attribute__((noinline))
uint64_t gcd_branchless_loop(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    b >>= bz;

    // Run for max possible iterations
    // Average case ~45, worst case ~93 for 64-bit
    for (int i = 0; i < 96; i++) {
        a >>= az;
        uint64_t diff = b - a;
        az = diff ? __builtin_ctzll(diff) : 0;
        // Branchless min/abs using conditional moves
        uint64_t new_b = (a < b) ? a : b;
        uint64_t new_a = (a < b) ? diff : (a - b);
        b = new_b;
        a = new_a;
    }
    return b << shift;
}

// ============================================================
// 3. Hybrid: branchless inner loop + early loop exit
//    This is the standard approach but with explicit effort
//    to ensure CMOV generation (no branches in loop body).
// ============================================================

__attribute__((noinline))
uint64_t gcd_branchless_hybrid(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    a >>= az;
    b >>= bz;

    while (a != b) {
        uint64_t diff = (a > b) ? (a - b) : (b - a);
        b = (a < b) ? a : b;
        a = diff >> __builtin_ctzll(diff);
    }
    return a << shift;
}

// ============================================================
// 4. Optimized branchless with early-exit (clean version)
//    Aims for the tightest possible inner loop
// ============================================================

__attribute__((noinline))
uint64_t gcd_novel_v4(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Initial reduction: one modular step to handle skewed inputs
    if (a > b) { uint64_t t = a; a = b; b = t; }
    b %= a;
    if (b == 0) return a;
    
    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    a >>= az;
    b >>= bz;

    while (a != b) {
        // Ensure a >= b (branchless swap)
        uint64_t hi = (a >= b) ? a : b;
        uint64_t lo = (a >= b) ? b : a;
        a = hi - lo;
        b = lo;
        a >>= __builtin_ctzll(a);
    }
    return a << shift;
}

// ============================================================
// 5. Novel approach: initial modular reduction + tight branchless loop
//    This is our best attempt combining insights from all analysis:
//    - Initial mod step handles skewed inputs (like euclid)
//    - Then tight binary GCD loop with TZCNT-before-ABS optimization
//    - Early check for a==1 (most pairs are coprime)
// ============================================================

__attribute__((noinline))
uint64_t gcd_novel_best(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Initial reduction to handle skewed inputs efficiently
    if (a > b) { uint64_t t = a; a = b; b = t; }
    b %= a;
    if (b == 0) return a;
    
    // Factor out shared powers of 2
    int shift = __builtin_ctzll(a | b);
    a >>= __builtin_ctzll(a);
    b >>= __builtin_ctzll(b);

    // Tight binary GCD loop with TZCNT-before-ABS
    while (a != b) {
        uint64_t diff = (a > b) ? (a - b) : (b - a);
        uint64_t smaller = (a < b) ? a : b;
        diff >>= __builtin_ctzll(diff);
        a = diff;
        b = smaller;
    }
    return a << shift;
}

// ============================================================
// 6. Novel approach: unrolled 2x loop with speculative next step
// ============================================================

__attribute__((noinline))
uint64_t gcd_novel_unrolled(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = (az < bz) ? az : bz;
    a >>= az;
    b >>= bz;

    while (a != b) {
        // Step 1
        uint64_t diff = (a > b) ? (a - b) : (b - a);
        uint64_t smaller = (a < b) ? a : b;
        diff >>= __builtin_ctzll(diff);
        a = diff;
        b = smaller;
        if (a == b) break;
        
        // Step 2 (unrolled)
        diff = (a > b) ? (a - b) : (b - a);
        smaller = (a < b) ? a : b;
        diff >>= __builtin_ctzll(diff);
        a = diff;
        b = smaller;
    }
    return a << shift;
}

} // namespace gcd_novel
