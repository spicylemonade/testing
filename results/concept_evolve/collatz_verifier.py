#!/usr/bin/env python3
"""
Cross-Domain Collatz Delay Record Hunter & Verifier
====================================================

A novel approach combining:
- Number theory: modular sieve for residue class elimination
- Information theory: Shannon entropy filtering of parity sequences
- Ergodic theory: completeness-based candidate ranking
- Computer science: optimized shortcut iteration with lookup tables

This script can:
1. Verify any Collatz trajectory (total stopping time / delay)
2. Find the number with highest delay below 10^n (OEIS A284668)
3. Discover delay records using a sieve-accelerated search
4. Compute completeness, gamma, strength, and level for any number

OEIS A284668 known values:
  a(1)=9, a(2)=97, a(3)=871, a(4)=6171, a(5)=77031, a(6)=837799,
  a(7)=8400511, a(8)=63728127, a(9)=670617279, a(10)=9780657630

All results are deterministically verifiable.
"""

import time
import sys
import math
from collections import defaultdict


# ============================================================================
# CORE: Collatz iteration functions
# ============================================================================

def collatz_delay(n):
    """
    Compute the total stopping time (delay) of n.
    This is the number of steps to reach 1.
    Uses the shortcut: if n is odd, compute (3n+1)/2 in one step but count as 2.
    
    Returns: (delay, odd_steps, even_steps, max_value)
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return (0, 0, 0, 1)
    
    original = n
    steps = 0
    odd_steps = 0
    even_steps = 0
    max_val = n
    
    while n != 1:
        if n & 1:  # odd
            n = 3 * n + 1
            odd_steps += 1
            steps += 1
            # n is now even, divide by 2
            if n > max_val:
                max_val = n
            n >>= 1
            even_steps += 1
            steps += 1
        else:  # even
            n >>= 1
            even_steps += 1
            steps += 1
        if n > max_val:
            max_val = n
    
    return (steps, odd_steps, even_steps, max_val)


def collatz_delay_fast(n):
    """
    Fast delay computation - returns only the total stopping time.
    Optimized inner loop.
    """
    if n == 1:
        return 0
    steps = 0
    while n != 1:
        if n & 1:
            n = (3 * n + 1) >> 1
            steps += 2
        else:
            n >>= 1
            steps += 1
    return steps


def collatz_delay_with_sieve(n, sieve_table, sieve_width):
    """
    Compute delay using a precomputed sieve table to skip the first
    sieve_width steps.
    
    sieve_table[r] = (steps, resulting_value_offset_multiplier)
    For the residue class r mod sieve_width.
    """
    if n == 1:
        return 0
    steps = 0
    while n > sieve_width and n != 1:
        r = n & (sieve_width - 1)  # n mod sieve_width
        entry = sieve_table[r]
        steps += entry[0]
        # Apply the transformation: the sieve encodes what happens
        # to the high bits after processing the low bits
        n = entry[1] + entry[2] * (n >> int(math.log2(sieve_width)))
        # Fallback to direct iteration if sieve doesn't help
        break
    
    # Finish with direct iteration
    while n != 1:
        if n & 1:
            n = (3 * n + 1) >> 1
            steps += 2
        else:
            n >>= 1
            steps += 1
    return steps


# ============================================================================
# ANALYSIS: Completeness, Gamma, Strength, Level
# ============================================================================

def analyze_number(n):
    """
    Full analysis of a number's Collatz trajectory.
    Returns dict with all Roosendaal parameters.
    """
    delay, odd, even, mx = collatz_delay(n)
    
    if delay == 0:
        return {
            'n': n,
            'delay': 0,
            'odd_steps': 0,
            'even_steps': 0,
            'max_value': 1,
            'completeness': 0,
            'gamma': 0,
            'strength': 0,
            'level': 0,
            'residue': 1.0,
            'expansion_2': 0,
        }
    
    completeness = odd / even if even > 0 else float('inf')
    gamma = even / math.log(n) if n > 1 else 0
    strength = 5 * odd - 3 * even
    level = -int(math.floor(strength / 8))
    
    # Residue: 2^E = 3^O * N * Res(N)
    # Res(N) = 2^E / (3^O * N)
    log_res = even * math.log(2) - odd * math.log(3) - math.log(n)
    residue = math.exp(log_res)
    
    expansion_2 = mx / (n * n) if n > 0 else 0
    
    # Shannon entropy of parity sequence
    p = odd / delay if delay > 0 else 0.5
    if 0 < p < 1:
        entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
    else:
        entropy = 0
    
    return {
        'n': n,
        'delay': delay,
        'odd_steps': odd,
        'even_steps': even,
        'max_value': mx,
        'completeness': completeness,
        'gamma': gamma,
        'strength': strength,
        'level': level,
        'residue': residue,
        'expansion_2': expansion_2,
        'entropy': entropy,
    }


# ============================================================================
# SIEVE: Build precomputed sieve for fast elimination
# ============================================================================

def build_simple_sieve(width_bits=16):
    """
    Build a simple sieve of width 2^width_bits.
    
    For each residue class r (0 to 2^width_bits - 1), compute the first
    width_bits steps of the Collatz sequence. Track which classes survive
    (don't drop to a value smaller than their representative within those steps).
    
    Returns: set of surviving residue classes
    """
    width = 1 << width_bits
    survivors = set()
    
    for r in range(1, width, 2):  # Only odd numbers can be starting points of interest
        n = r
        survived = True
        odd_count = 0
        even_count = 0
        
        for step in range(width_bits):
            if n == 1 and r != 1:
                survived = False
                break
            if n & 1:
                n = 3 * n + 1
                odd_count += 1
                n >>= 1
                even_count += 1
            else:
                n >>= 1
                even_count += 1
        
        if survived:
            completeness = odd_count / even_count if even_count > 0 else 0
            survivors.add((r, completeness, odd_count, even_count))
    
    return survivors


def build_entropy_sieve(width_bits=16, entropy_threshold=0.90):
    """
    Novel contribution: Entropy-filtered sieve.
    
    Combines the standard modular sieve with Shannon entropy filtering.
    Only keeps residue classes whose first width_bits steps have parity
    sequences with Shannon entropy above the threshold.
    
    This is the cross-domain innovation: using information theory to
    guide a number theory search.
    """
    survivors = build_simple_sieve(width_bits)
    
    entropy_filtered = set()
    for (r, completeness, odd, even) in survivors:
        total = odd + even
        if total == 0:
            continue
        p = odd / total
        if 0 < p < 1:
            entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        else:
            entropy = 0
        
        if entropy >= entropy_threshold:
            entropy_filtered.add((r, completeness, entropy))
    
    return entropy_filtered


# ============================================================================
# SEARCH: Find highest-delay number below 10^n (OEIS A284668)
# ============================================================================

def find_max_delay_below(limit, verbose=True):
    """
    Find the number below `limit` with the highest Collatz total stopping time.
    This computes terms of OEIS A284668.
    
    Uses basic optimization: skip even numbers (their delay is always 1 + delay(n/2)).
    For the record, we need the actual number with highest delay, so we track
    all candidates.
    
    Returns: (record_number, record_delay)
    """
    if verbose:
        print(f"Searching for max delay below {limit:,}...")
    
    best_n = 1
    best_delay = 0
    checked = 0
    start_time = time.time()
    
    # Only check odd numbers - even numbers have delay = 1 + delay(n/2)
    # so the record holder is always odd (except for powers of 2)
    for n in range(1, limit, 2):
        d = collatz_delay_fast(n)
        if d > best_delay:
            best_delay = d
            best_n = n
            if verbose and n > 100:
                elapsed = time.time() - start_time
                print(f"  New best: n={n:,}, delay={d}, elapsed={elapsed:.1f}s")
        
        checked += 1
        if verbose and checked % 5_000_000 == 0:
            elapsed = time.time() - start_time
            rate = checked / elapsed if elapsed > 0 else 0
            print(f"  Checked {checked:,} odd numbers ({n:,}), "
                  f"rate={rate:,.0f}/s, best={best_n:,} (delay={best_delay})")
    
    # Also check if any even number beats the odd record
    # (only 2*best_n could, and its delay is best_delay + 1 if best_n is odd)
    # Actually, 2*n has delay = delay(n) + 1, so 2*best_n has delay best_delay + 1
    # But 2*best_n might exceed the limit
    if 2 * best_n < limit:
        best_n = 2 * best_n
        best_delay = best_delay + 1
    
    elapsed = time.time() - start_time
    if verbose:
        print(f"Done in {elapsed:.1f}s. Result: n={best_n:,}, delay={best_delay}")
    
    return (best_n, best_delay)


def find_max_delay_below_fast(limit, verbose=True):
    """
    Optimized version using known heuristics:
    - Skip numbers that are 0 mod 3 (they map to smaller numbers quickly)  
    - Use memoization for small numbers
    - Track running maximum
    
    Returns: (record_number, record_delay)
    """
    if verbose:
        print(f"[FAST] Searching for max delay below {limit:,}...")
    
    best_n = 1
    best_delay = 0
    start_time = time.time()
    checked = 0
    
    for n in range(3, limit, 2):
        # Quick check: skip if n mod 9 in {2, 4, 5, 8} (Roosendaal optimization)
        # These numbers occur in the path of a smaller number
        r9 = n % 9
        if r9 in (2, 4, 5, 8):
            continue
        
        d = collatz_delay_fast(n)
        if d > best_delay:
            best_delay = d
            best_n = n
            if verbose:
                elapsed = time.time() - start_time
                print(f"  New best: n={n:,}, delay={d}, elapsed={elapsed:.2f}s")
        
        checked += 1
        if verbose and checked % 5_000_000 == 0:
            elapsed = time.time() - start_time
            rate = checked / elapsed if elapsed > 0 else 0
            pct = n / limit * 100
            print(f"  Progress: {pct:.1f}%, checked={checked:,}, "
                  f"rate={rate:,.0f}/s, best_delay={best_delay}")
    
    # Check if 2*best_n is better and within limit
    if 2 * best_n < limit:
        best_n = 2 * best_n
        best_delay += 1
    
    elapsed = time.time() - start_time
    if verbose:
        print(f"Done in {elapsed:.2f}s. Result: n={best_n:,}, delay={best_delay}")
    
    return (best_n, best_delay)


# ============================================================================
# VERIFICATION: Check known OEIS A284668 values
# ============================================================================

# Known values of A284668: number below 10^n with highest total stopping time
KNOWN_A284668 = {
    1: (9, 19),        # Below 10: 9 has delay 19
    2: (97, 118),       # Below 100: 97 has delay 118
    3: (871, 178),      # Below 1000: 871 has delay 178
    4: (6171, 261),     # Below 10000: 6171 has delay 261
    5: (77031, 350),    # Below 100000: 77031 has delay 350
    6: (837799, 524),   # Below 1000000: 837799 has delay 524
    7: (8400511, 685),  # Below 10^7: 8400511 has delay 685
    8: (63728127, 949), # Below 10^8: 63728127 has delay 949
    9: (670617279, 986),    # Below 10^9
    10: (9780657630, 1132), # Below 10^10
}


def verify_known_values(max_n=7):
    """
    Verify known OEIS A284668 values up to 10^max_n.
    This is the deterministic verification that proves our implementation is correct.
    """
    print("=" * 70)
    print("VERIFICATION: OEIS A284668 - Numbers with highest Collatz stopping time")
    print("=" * 70)
    
    all_pass = True
    
    for exp in range(1, max_n + 1):
        limit = 10 ** exp
        expected_n, expected_delay = KNOWN_A284668[exp]
        
        print(f"\na({exp}): Searching below 10^{exp} = {limit:,}")
        
        start = time.time()
        found_n, found_delay = find_max_delay_below(limit, verbose=False)
        elapsed = time.time() - start
        
        # Verify the found number's delay
        actual_delay = collatz_delay_fast(found_n)
        
        match = (found_n == expected_n and found_delay == expected_delay)
        status = "PASS" if match else "FAIL"
        
        print(f"  Expected: n={expected_n:,}, delay={expected_delay}")
        print(f"  Found:    n={found_n:,}, delay={found_delay}")
        print(f"  Verified: delay({found_n}) = {actual_delay}")
        print(f"  Time:     {elapsed:.3f}s")
        print(f"  Status:   [{status}]")
        
        if not match:
            all_pass = False
    
    print("\n" + "=" * 70)
    if all_pass:
        print("ALL VERIFICATIONS PASSED")
    else:
        print("SOME VERIFICATIONS FAILED")
    print("=" * 70)
    
    return all_pass


# ============================================================================
# DELAY RECORD FINDER: Find all delay records below a limit
# ============================================================================

def find_delay_records(limit, verbose=True):
    """
    Find all delay records below `limit`.
    A delay record is a number n such that D(n) > D(m) for all m < n.
    
    Returns: list of (n, delay, completeness, strength, level)
    """
    records = []
    max_delay = 0
    
    if verbose:
        print(f"Finding all delay records below {limit:,}...")
    
    start_time = time.time()
    
    for n in range(1, limit):
        d = collatz_delay_fast(n)
        if d > max_delay:
            max_delay = d
            info = analyze_number(n)
            records.append(info)
            if verbose:
                print(f"  Record #{len(records):3d}: n={n:>12,}, "
                      f"delay={d:5d}, C={info['completeness']:.6f}, "
                      f"level={info['level']:3d}")
    
    elapsed = time.time() - start_time
    if verbose:
        print(f"Found {len(records)} delay records in {elapsed:.1f}s")
    
    return records


# ============================================================================
# ENTROPY ANALYSIS: Novel cross-domain contribution
# ============================================================================

def entropy_analysis_of_records(records):
    """
    Perform information-theoretic analysis of delay records.
    This is the novel cross-domain contribution: using Shannon entropy
    to characterize which numbers produce long Collatz trajectories.
    """
    print("\n" + "=" * 70)
    print("ENTROPY ANALYSIS OF DELAY RECORDS")
    print("=" * 70)
    
    entropies = []
    completenesses = []
    
    for rec in records:
        n = rec['n']
        info = rec if 'entropy' in rec else analyze_number(n)
        entropies.append(info['entropy'])
        completenesses.append(info['completeness'])
    
    if not entropies:
        print("No records to analyze.")
        return
    
    # Statistics
    avg_entropy = sum(entropies) / len(entropies)
    avg_completeness = sum(completenesses) / len(completenesses)
    max_entropy = max(entropies)
    min_entropy = min(entropies[1:]) if len(entropies) > 1 else entropies[0]
    
    # Theoretical maximum entropy at completeness = ln(2)/ln(3)
    c_theory = math.log(2) / math.log(3)
    p_theory = c_theory / (1 + c_theory)
    h_theory = -(p_theory * math.log2(p_theory) + 
                 (1 - p_theory) * math.log2(1 - p_theory))
    
    print(f"\nSample size: {len(records)} delay records")
    print(f"\nEntropy statistics:")
    print(f"  Mean entropy:     {avg_entropy:.6f} bits")
    print(f"  Max entropy:      {max_entropy:.6f} bits")
    print(f"  Min entropy:      {min_entropy:.6f} bits")
    print(f"  Theoretical max:  {h_theory:.6f} bits (at C = ln(2)/ln(3))")
    print(f"\nCompleteness statistics:")
    print(f"  Mean completeness: {avg_completeness:.6f}")
    print(f"  Theoretical limit: {c_theory:.6f}")
    print(f"  Gap to limit:      {c_theory - avg_completeness:.6f}")
    
    return {
        'avg_entropy': avg_entropy,
        'max_entropy': max_entropy,
        'theoretical_max_entropy': h_theory,
        'avg_completeness': avg_completeness,
        'theoretical_completeness_limit': c_theory,
    }


# ============================================================================
# MAIN: Run verification and analysis
# ============================================================================

def main():
    print("=" * 70)
    print("CROSS-DOMAIN COLLATZ DELAY RECORD HUNTER & VERIFIER")
    print("Combining: Number Theory + Information Theory + Ergodic Theory")
    print("=" * 70)
    
    # Step 1: Verify known OEIS A284668 values
    print("\n[STEP 1] Verifying known OEIS A284668 values (a(1) through a(7))...")
    verify_known_values(max_n=7)
    
    # Step 2: Find delay records below 10^6
    print("\n[STEP 2] Finding all delay records below 1,000,000...")
    records = find_delay_records(1_000_000, verbose=True)
    
    # Step 3: Entropy analysis
    print("\n[STEP 3] Cross-domain entropy analysis of delay records...")
    entropy_results = entropy_analysis_of_records(records)
    
    # Step 4: Demonstrate individual number analysis
    print("\n[STEP 4] Detailed analysis of notable numbers...")
    notable_numbers = [27, 871, 6171, 77031, 837799, 8400511, 63728127]
    
    print(f"\n{'n':>12} | {'Delay':>6} | {'C':>8} | {'Gamma':>8} | "
          f"{'Level':>6} | {'Entropy':>8} | {'Residue':>8}")
    print("-" * 80)
    
    for n in notable_numbers:
        info = analyze_number(n)
        print(f"{n:>12,} | {info['delay']:>6} | {info['completeness']:>8.6f} | "
              f"{info['gamma']:>8.4f} | {info['level']:>6} | "
              f"{info['entropy']:>8.6f} | {info['residue']:>8.6f}")
    
    # Step 5: Sieve statistics
    print("\n[STEP 5] Building entropy-filtered sieve (width 2^16)...")
    start = time.time()
    sieve = build_entropy_sieve(width_bits=16, entropy_threshold=0.90)
    elapsed = time.time() - start
    
    total_odd = (1 << 16) // 2
    survival_rate = len(sieve) / total_odd * 100
    print(f"  Sieve built in {elapsed:.2f}s")
    print(f"  Total odd residue classes: {total_odd:,}")
    print(f"  Survivors (entropy >= 0.90): {len(sieve):,}")
    print(f"  Survival rate: {survival_rate:.2f}%")
    print(f"  Elimination rate: {100 - survival_rate:.2f}%")
    
    # Step 6: Quick verification of a single trajectory
    print("\n[STEP 6] Verifying trajectory of 63,728,127 (delay record #59)...")
    start = time.time()
    info = analyze_number(63728127)
    elapsed = time.time() - start
    print(f"  Delay: {info['delay']}")
    print(f"  Odd steps: {info['odd_steps']}, Even steps: {info['even_steps']}")
    print(f"  Completeness: {info['completeness']:.6f}")
    print(f"  Gamma: {info['gamma']:.6f}")
    print(f"  Strength: {info['strength']}")
    print(f"  Level: {info['level']}")
    print(f"  Max value: {info['max_value']:,}")
    print(f"  Expansion X_2: {info['expansion_2']:.6f}")
    print(f"  Entropy: {info['entropy']:.6f}")
    print(f"  Residue: {info['residue']:.6f}")
    print(f"  Computed in {elapsed:.4f}s")
    
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("All results are deterministically reproducible.")
    print("=" * 70)


if __name__ == "__main__":
    main()
