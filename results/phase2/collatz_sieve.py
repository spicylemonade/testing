#!/usr/bin/env python3
"""Collatz modular sieving filter for candidate elimination.

Uses the key insight that the lowest k bits of n completely determine
the first k Collatz steps. This allows pre-computing which residue
classes mod 2^k have short guaranteed stopping times and eliminating them.

Additionally implements the mod-9 filter: numbers congruent to
2, 4, 5, or 8 mod 9 lie on the trajectory of a smaller number.

References:
  - Roosendaal, https://www.ericr.nl/wondrous/techpage.html
  - Angeltveit (2026), arXiv:2602.10466
  - Dutta (2025), EJMAA
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from collatz_baseline import collatz_stopping_time


def simulate_k_steps(residue: int, k: int) -> Tuple[int, int]:
    """Simulate k Collatz steps on a residue class.

    Given a number n ≡ residue (mod 2^k), the first k steps are
    completely determined by the residue. We track:
    - The number of steps actually executed (may be < k if we reach 1)
    - Whether the trajectory "descended" below the starting value

    Returns (steps_executed, min_ratio_numerator) where min_ratio indicates
    the minimum value of n_i / n_0 achieved (as integer ratio * 2^k for precision).
    """
    # Simulate on the actual residue value to determine the step pattern
    n = residue
    if n == 0:
        return (0, 0)

    steps = 0
    for _ in range(k):
        if n == 0:
            break
        if n & 1:  # odd
            n = 3 * n + 1
        else:       # even
            n >>= 1
        steps += 1

    return (steps, n)


def compute_sieve_table(k: int) -> Dict[int, int]:
    """Compute the sieve lookup table for mod 2^k.

    For each residue r in [0, 2^k), simulate k Collatz steps.
    The result after k steps is: n' = a * n + b where a, b depend only on r.

    We track the "shortcut multiplier" and offset so that:
      T^k(n) = (a * n + b) / 2^k  (where a, b are determined by residue mod 2^k)

    Returns dict mapping residue -> guaranteed_min_steps.
    """
    mod = 1 << k
    table = {}

    for r in range(mod):
        if r == 0:
            table[r] = 0
            continue

        # Track how the Collatz map transforms r symbolically
        # For n ≡ r (mod 2^k), the first k bit-decisions are fixed
        n = r
        odd_steps = 0
        even_steps = 0

        for step in range(k):
            if n & 1:  # odd: n -> 3n+1
                n = 3 * n + 1
                odd_steps += 1
            else:       # even: n -> n/2
                n >>= 1
                even_steps += 1

        # The number of guaranteed steps is k
        # After k steps, the "effective multiplier" is 3^odd_steps / 2^k
        # If 3^odd_steps < 2^k, the value definitely decreased
        table[r] = odd_steps  # Store odd step count for analysis

    return table


def surviving_residues(k: int, min_steps: int = 0, search_min: int = 10**9) -> Set[int]:
    """Return residue classes mod 2^k that survive the delay-record sieve.

    Standard Roosendaal-style sieve adapted for delay record search:

    For each residue r mod 2^k, simulate k Collatz steps symbolically.
    At step j, T^j(n) = (a_j * n + b_j) / 2^{e_j} where the step pattern
    (odd/even decisions) is determined entirely by r.

    A residue is ELIMINATED if T^j(n) < n for all n >= search_min at any step
    j in [1..k]. This means: a_j / 2^{e_j} < 1 AND n > b_j / (2^{e_j} - a_j).

    The search_min parameter determines the minimum n we care about.
    For searching range [10^10, 10^13], set search_min=10^10.

    Additionally applies mod-9 filter (eliminates 44.4% of numbers).
    """
    mod = 1 << k
    survivors = set()

    for r in range(1, mod, 2):  # Only odd numbers
        # Apply mod-9 filter
        if r % 9 in (2, 4, 5, 8):
            continue

        # Simulate k steps symbolically
        current = r
        a = 1       # numerator coefficient of n
        b = 0       # constant offset (numerator)
        e = 0       # denominator is 2^e

        descended = False

        for step in range(k):
            if current & 1:
                a = 3 * a
                b = 3 * b + (1 << e)
                current = 3 * current + 1
            else:
                e += 1
                current >>= 1

            # T^j(n) = (a*n + b) / 2^e
            # T^j(n) < n iff a*n + b < 2^e * n iff b < (2^e - a) * n
            denom = 1 << e
            if a < denom:
                gap = denom - a
                # n > b / gap means T^j(n) < n
                crossover = b // gap + 1 if gap > 0 else 10**18
                if search_min >= crossover:
                    descended = True
                    break

        if not descended:
            survivors.add(r)

    return survivors


def build_sieve_bitset(k: int, min_odd_ratio: float = 0.35) -> bytearray:
    """Build a compact bitset sieve for residues mod 2^k.

    Returns a bytearray where bit i is set if residue i should be tested.
    Only odd residues can be set (all even residues are skipped by default
    since they map to n/2 which is smaller).
    """
    mod = 1 << k
    bitset = bytearray(mod // 8 + 1)

    for r in range(1, mod, 2):
        # Simulate k steps
        n = r
        odd_count = 0
        for _ in range(k):
            if n & 1:
                n = 3 * n + 1
                odd_count += 1
            else:
                n >>= 1

        odd_ratio = odd_count / k if k > 0 else 0
        if odd_ratio >= min_odd_ratio:
            byte_idx = r >> 3
            bit_idx = r & 7
            bitset[byte_idx] |= (1 << bit_idx)

    return bitset


def mod9_filter(n: int) -> bool:
    """Return True if n should be tested (not on a smaller number's path).

    Numbers congruent to 2, 4, 5, or 8 mod 9 occur on the path of a
    smaller number and can be skipped for delay record search.
    """
    r = n % 9
    return r not in (2, 4, 5, 8)


def sieved_scan(start: int, end: int, k: int = 16,
                min_stopping_time: int = 200) -> List[Tuple[int, int]]:
    """Scan range [start, end) using sieve to find numbers with high stopping times.

    Returns list of (n, stopping_time) for numbers exceeding min_stopping_time.
    """
    mod = 1 << k
    # Pre-compute surviving residues
    survivors = surviving_residues(k, min_steps=min(k, 30))

    results = []
    candidates_tested = 0
    candidates_skipped = 0

    for n in range(start | 1, end, 2):  # Only odd numbers
        r = n % mod
        if r not in survivors:
            candidates_skipped += 1
            continue
        if not mod9_filter(n):
            candidates_skipped += 1
            continue

        candidates_tested += 1
        t = collatz_stopping_time(n)
        if t >= min_stopping_time:
            results.append((n, t))

    return results


def benchmark_sieve():
    """Benchmark sieve effectiveness at various depths."""
    print("Sieve Effectiveness Benchmark")
    print("=" * 70)

    test_range = 1_000_000  # Test on first million odd numbers

    # Naive baseline
    print("\n--- Naive scan (no sieve) ---")
    start_t = time.perf_counter()
    naive_count = 0
    naive_high = 0
    for n in range(1, test_range + 1, 2):
        t = collatz_stopping_time(n)
        naive_count += 1
        if t >= 200:
            naive_high += 1
    naive_time = time.perf_counter() - start_t
    print(f"  Numbers tested: {naive_count:,}")
    print(f"  Numbers with stopping time >= 200: {naive_high:,}")
    print(f"  Time: {naive_time:.2f}s")

    # Sieved scans at different depths
    for k in [10, 15, 20]:
        print(f"\n--- Sieve depth k={k} (mod 2^{k} = {1<<k:,}) ---")
        # Test with different search_min values
        for smin in [1, 10**6, 10**9]:
            survivors = surviving_residues(k, search_min=smin)
            mod = 1 << k
            survival_rate = len(survivors) / (mod // 2)
            elim = 1 - survival_rate
            print(f"  search_min={smin:>12}: survivors={len(survivors):>6}, rate={survival_rate*100:.1f}%, elimination={elim*100:.1f}%")

        # Actual scan with search_min=1 (conservative for small range)
        survivors = surviving_residues(k, search_min=1)
        mod = 1 << k
        start_t = time.perf_counter()
        sieve_tested = 0
        sieve_high = 0
        sieve_skipped = 0
        for n in range(1, test_range + 1, 2):
            r = n % mod
            if r not in survivors:
                sieve_skipped += 1
                continue
            sieve_tested += 1
            t = collatz_stopping_time(n)
            if t >= 200:
                sieve_high += 1
        sieve_time = time.perf_counter() - start_t

        actual_elim = sieve_skipped / naive_count

        print(f"  Actual scan (smin=1): tested={sieve_tested:,}, skipped={sieve_skipped:,}, elim={actual_elim*100:.1f}%")
        print(f"  Time: {sieve_time:.2f}s, Speedup: {naive_time/sieve_time:.1f}x")

    # Summary
    results = {
        "test_range": test_range,
        "naive_count": naive_count,
        "naive_high_count": naive_high,
        "naive_time_seconds": round(naive_time, 2),
        "sieve_results": {}
    }

    for k in [10, 15, 20]:
        survivors = surviving_residues(k, search_min=10**9)
        mod = 1 << k
        survival_rate = len(survivors) / (mod // 2)
        results["sieve_results"][f"k={k}"] = {
            "mod": mod,
            "surviving_residues": len(survivors),
            "survival_rate": round(survival_rate, 4),
            "elimination_rate": round(1 - survival_rate, 4),
        }

    outpath = Path(__file__).parent / "sieve_benchmark.json"
    outpath.write_text(json.dumps(results, indent=2))
    print(f"\nBenchmark saved to {outpath}")


if __name__ == "__main__":
    benchmark_sieve()
