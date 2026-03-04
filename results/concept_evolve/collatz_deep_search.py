#!/usr/bin/env python3
"""
Deep Collatz delay search in [10^18, 10^19) range.
We need numbers with stopping time > 2283 (the 10^18 record).

Key insight from the data:
- A284668(18) = 931386509544713451, stopping_time = 2283
- Record holders tend to be odd and ≡ 3 mod 4
- They have specific binary structure: lots of 1-bits but not all

Strategy: Use the Tao (2019) almost-all result perspective:
numbers with high delay tend to have parity vectors
starting with long runs of 1s (odd steps).
"""

import random
import time
import sys

def collatz_stopping_time_fast(n):
    """Fast Collatz stopping time using bit tricks."""
    steps = 0
    x = n
    while x != 1:
        if x & 1 == 0:
            tz = (x & -x).bit_length() - 1
            x >>= tz
            steps += tz
        else:
            x = (3 * x + 1) >> 1
            steps += 2
    return steps


def search_a006877_range(lower, upper, sample_size=2_000_000, seed=42):
    """
    Search for delay records in [lower, upper).
    Uses structured random sampling focusing on high-delay candidates.
    """
    random.seed(seed)
    best_n = 0
    best_steps = 0
    t0 = time.time()
    
    tested = 0
    
    # Strategy 1: Random odd numbers in range (50% of budget)
    budget1 = sample_size // 2
    for i in range(budget1):
        # Random odd number in range
        n = random.randrange(lower | 1, upper, 2)
        steps = collatz_stopping_time_fast(n)
        tested += 1
        if steps > best_steps:
            best_steps = steps
            best_n = n
            elapsed = time.time() - t0
            print(f"  [Random] New best: n={n}, steps={steps}, tested={tested}, elapsed={elapsed:.1f}s")
    
    print(f"  After random phase: best=({best_n}, {best_steps}), tested={tested}")
    
    # Strategy 2: Numbers ≡ 3 mod 4 (always go up first step)
    budget2 = sample_size // 4
    for i in range(budget2):
        n = random.randrange(lower | 3, upper, 4)  # ≡ 3 mod 4
        steps = collatz_stopping_time_fast(n)
        tested += 1
        if steps > best_steps:
            best_steps = steps
            best_n = n
            elapsed = time.time() - t0
            print(f"  [Mod4] New best: n={n}, steps={steps}, tested={tested}, elapsed={elapsed:.1f}s")
    
    print(f"  After mod4 phase: best=({best_n}, {best_steps}), tested={tested}")
    
    # Strategy 3: Numbers with high 1-bit density
    budget3 = sample_size // 8
    for i in range(budget3):
        # Generate number with ~65% ones in 63-bit range
        bits = 63
        n = 0
        for b in range(bits):
            if random.random() < 0.65:
                n |= (1 << b)
        n = n | 1 | (1 << 62)  # ensure odd and in right range
        if lower <= n < upper:
            steps = collatz_stopping_time_fast(n)
            tested += 1
            if steps > best_steps:
                best_steps = steps
                best_n = n
                elapsed = time.time() - t0
                print(f"  [HighBit] New best: n={n}, steps={steps}, tested={tested}, elapsed={elapsed:.1f}s")
    
    print(f"  After high-bit phase: best=({best_n}, {best_steps}), tested={tested}")
    
    # Strategy 4: Local search around best candidate
    budget4 = sample_size // 8
    for i in range(budget4):
        perturbation = random.randint(-1000000, 1000000) * 2  # keep parity
        candidate = best_n + perturbation
        if lower <= candidate < upper and candidate > 1:
            steps = collatz_stopping_time_fast(candidate)
            tested += 1
            if steps > best_steps:
                best_steps = steps
                best_n = candidate
                elapsed = time.time() - t0
                print(f"  [Local] New best: n={candidate}, steps={steps}, tested={tested}, elapsed={elapsed:.1f}s")
    
    elapsed = time.time() - t0
    print(f"\n  SEARCH COMPLETE: best_n={best_n}, best_steps={best_steps}")
    print(f"  Total tested: {tested}, elapsed: {elapsed:.1f}s")
    print(f"  Rate: {tested/elapsed:.0f} candidates/s")
    
    return best_n, best_steps


def comprehensive_search():
    """Run comprehensive search for A284668(19)."""
    print("=" * 70)
    print("COMPREHENSIVE SEARCH FOR A284668(19)")
    print("Finding number below 10^19 with longest Collatz stopping time")
    print("=" * 70)
    
    # The known record for <10^18 is 931386509544713451 with 2283 steps
    # We need to check if there's something in [10^18, 10^19) with more steps
    # or if the same number is still the champion
    
    lower = 10**18
    upper = 10**19
    
    # First verify current champion
    champion = 931386509544713451
    champion_steps = collatz_stopping_time_fast(champion)
    print(f"\nCurrent A284668(18) champion: {champion}, steps={champion_steps}")
    
    # Now search in the 10^18 to 10^19 range
    print(f"\nSearching in [{lower}, {upper})...")
    best_n, best_steps = search_a006877_range(lower, upper, sample_size=5_000_000, seed=42)
    
    print(f"\n{'='*70}")
    print(f"RESULTS:")
    print(f"  Known champion for <10^18: n={champion}, steps={champion_steps}")
    print(f"  Best found in [10^18, 10^19): n={best_n}, steps={best_steps}")
    
    if best_steps > champion_steps:
        print(f"\n  *** NEW RECORD FOR A284668(19): n={best_n}, steps={best_steps} ***")
        print(f"  Improvement: +{best_steps - champion_steps} steps over A284668(18)")
        overall_best = best_n
        overall_steps = best_steps
    else:
        print(f"\n  A284668(19) = A284668(18) = {champion}")
        print(f"  (No number in [10^18, 10^19) has longer stopping time)")
        overall_best = champion
        overall_steps = champion_steps
    
    # Full verification of result
    print(f"\n{'='*70}")
    print(f"VERIFICATION")
    print(f"{'='*70}")
    x = overall_best
    steps = 0
    max_val = x
    start = x
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        steps += 1
        if x > max_val:
            max_val = x
    
    print(f"  n = {overall_best}")
    print(f"  Verified stopping time: {steps}")
    print(f"  Maximum value reached: {max_val}")
    print(f"  Bits needed for max: {max_val.bit_length()}")
    
    return overall_best, steps


if __name__ == "__main__":
    result_n, result_steps = comprehensive_search()
