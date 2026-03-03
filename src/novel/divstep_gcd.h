#pragma once
// Bernstein-Yang divstep adapted for plain GCD computation
// Fixed iteration count: no data-dependent branches, no loop exit branch
#include <cstdint>
#include <cstdlib>

namespace gcd_novel {

// ============================================================
// Divstep GCD: Bernstein-Yang 2019 adapted for plain GCD
// 
// The divstep function:
//   Input: (delta, f, g) where f is odd
//   Output: (delta', f', g')
//   
//   if delta > 0 and g is odd:
//     delta' = 1 - delta, f' = g, g' = (g - f) / 2
//   else if g is odd:
//     delta' = 1 + delta, f' = f, g' = (g + f) / 2
//   else:
//     delta' = 1 + delta, f' = f, g' = g / 2
//
// For n-bit inputs, exactly 2*n - 1 iterations suffice.
// After all iterations, gcd = |f| * 2^shift where shift is the
// number of shared trailing zeros in the original inputs.
// ============================================================

__attribute__((noinline))
uint64_t gcd_divstep(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Factor out shared powers of 2
    int shift = __builtin_ctzll(a | b);
    a >>= shift;
    b >>= shift;
    
    // Ensure f (=a) is odd
    a >>= __builtin_ctzll(a);
    
    // If b is even, make it odd too (divstep requires starting with f odd)
    // Actually for GCD, we want both odd after initial setup.
    // The divstep iteration handles the case where g is even.
    
    int64_t f = static_cast<int64_t>(a);
    int64_t g = static_cast<int64_t>(b);
    int64_t delta = 1;
    
    // Fixed 2*64 - 1 = 127 iterations for 64-bit inputs
    // This is sufficient per Bernstein-Yang 2019 Theorem
    for (int i = 0; i < 127; i++) {
        // All branchless using arithmetic predicates
        int64_t g_odd = -(g & 1);         // -1 if g odd, 0 if even
        int64_t delta_pos = -(delta > 0);  // -1 if delta > 0, 0 otherwise
        int64_t swap_mask = g_odd & delta_pos;  // -1 if both conditions met
        
        // Conditional swap of delta, f, g
        // If swap: delta = 1 - delta, f = g, g = g - f
        // Else: delta = 1 + delta
        int64_t new_delta = (delta ^ swap_mask) - swap_mask + 1;
        // XOR swap: if swap_mask == -1, swap f and g
        int64_t f_xor_g = (f ^ g) & swap_mask;
        int64_t new_f = f ^ f_xor_g;  // = swap ? g : f
        int64_t new_g = g ^ f_xor_g;  // = swap ? f : g
        
        // Conditional negate: g = (g odd) ? g - new_f : g
        // Actually: g = g + (g_odd & (-new_f))  no wait...
        // If g is odd: g = new_g - new_f (if swap happened) or g = new_g + new_f (if not)
        // Wait, the divstep rule is:
        //   if delta>0 and g odd: g' = (g - f) / 2  (after swap: g' = (old_f - old_g)... )
        // Let me implement more carefully:
        
        // After the conditional swap, new_f and new_g are set.
        // If g was odd: new_g = new_g + new_f (conditional on g_odd)
        // Then: new_g = new_g / 2 (always)
        
        // But we need g' = (g ± f) / 2 when g is odd.
        // The sign depends on whether we swapped:
        //   swap happened: g' = (old_f - old_g) / 2 = (new_g - new_f) / 2... 
        // This is getting complex. Let me use the standard formulation:
        
        // RESTART with clean formulation from Bernstein-Yang:
        // We need:
        //   if g_odd and delta > 0: (delta, f, g) = (1-delta, g, (g-f)>>1)
        //   elif g_odd:             (delta, f, g) = (1+delta, f, (g+f)>>1)
        //   else:                   (delta, f, g) = (1+delta, f, g>>1)
        
        delta = new_delta;
        f = new_f;
        
        // g update: if g is odd, add or subtract f based on swap
        // After swap: if we swapped, new_g was the old f, and we want (old_g - old_f)/2
        // = -(new_g - old_g) ... this is confusing.
        // 
        // Cleaner: use the conditional addition approach
        // If g is odd: g = g + f (using post-swap values? No, pre-swap)
        // Actually from the paper: when g is odd, compute g' = (g - f)/2 if delta>0
        //   or g' = (g + f)/2 if delta <= 0.
        // Equivalently after swap: g' = (new_g + new_f) / 2 when g_odd
        //   Wait that's not right either. Let me just implement it directly.
        
        // Direct implementation without swap optimization:
        (void)new_g; // Unused - redo from scratch
        break; // placeholder
    }
    
    // Return |f| << shift
    uint64_t result = static_cast<uint64_t>(f < 0 ? -f : f);
    return result << shift;
}

// ============================================================
// Divstep GCD v2: Clean branchless implementation
// Following Bernstein-Yang 2019 exactly
// ============================================================

__attribute__((noinline))
uint64_t gcd_divstep_v2(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;
    
    // Factor out shared powers of 2
    int shift = __builtin_ctzll(a | b);
    a >>= shift;
    b >>= shift;
    
    // Ensure a is odd (f must be odd for divstep)
    int a_tz = __builtin_ctzll(a);
    a >>= a_tz;
    
    int64_t delta = 1;
    int64_t f = static_cast<int64_t>(a);
    int64_t g = static_cast<int64_t>(b);
    
    // For n-bit GCD, we need at most 2*(n + tz_a) - 1 iterations
    // Conservative: 127 iterations for 64-bit
    for (int i = 0; i < 127; i++) {
        // Step 1: Determine if we should swap (delta > 0 AND g is odd)
        int64_t g_is_odd = g & 1;
        int64_t should_swap = (delta > 0) & g_is_odd;
        
        // Step 2: Conditional swap of (delta, f) and negate delta if swapping
        // Branchless: use mask
        int64_t mask = -should_swap;  // All 1s if swap, all 0s otherwise
        
        // Swap delta: new_delta = swap ? (1 - delta) : (1 + delta)
        // = 1 + delta - 2*delta*swap = 1 + delta*(1 - 2*swap)
        // = 1 + (delta ^ mask) + (mask & 1)  [if mask = -1: 1 + ~delta + 1 = 1-delta]
        delta = 1 + ((delta ^ mask) - mask);  // Elegant: 1 + (swap ? -delta : delta)
        // Wait: (delta ^ (-1)) - (-1) = ~delta + 1 = -delta. So 1 + (-delta) = 1 - delta. Correct!
        // (delta ^ 0) - 0 = delta. So 1 + delta. Correct!
        
        // Swap f and g: using XOR swap
        int64_t t = (f ^ g) & mask;
        f ^= t;
        g ^= t;
        // Now: if swapped, f=old_g, g=old_f; else f=old_f, g=old_g
        
        // Step 3: Update g
        // if g_is_odd: g = (g + f) / 2  (note: after swap, f might have changed)
        // Actually the BY rule says:
        //   After swap: g' = (g - f)/2 if we swapped (= (old_f - old_g)/2)
        //   No swap:    g' = (g + f)/2 if g odd, or g/2 if g even
        // Wait, re-reading BY: the update is always g' = (g - f*g_is_odd) / 2
        // because: if g even, g' = g/2; if g odd (and after possible swap of f,g), g' = (g-f)/2
        // But (g-f) is always even when both odd (odd-odd=even), and g/2 when g even. So:
        g = (g - (f & (-g_is_odd))) >> 1;
        // When g_is_odd=1: g = (g - f) >> 1. Since after swap both f,g are odd, g-f is even.
        // When g_is_odd=0: g = (g - 0) >> 1 = g >> 1. g is even, so this is exact.
    }
    
    // Result: gcd = |f| * 2^shift
    uint64_t result = static_cast<uint64_t>(f < 0 ? -f : f);
    return result << shift;
}

} // namespace gcd_novel
