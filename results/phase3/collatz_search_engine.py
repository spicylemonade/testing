#!/usr/bin/env python3
"""Optimized Collatz delay record search engine.

Combines modular sieving, lookup-table acceleration, and multiprocessing
to search for delay records orders of magnitude faster than naive iteration.

Key optimizations:
1. Sieve: eliminate ~90% of candidates using mod-2^k residue analysis
2. Lookup table: precompute Collatz shortcuts for numbers < 2^k
3. Shortcut iteration: process multiple steps at once using binary tail
4. Multiprocessing: parallel search across CPU cores
5. Early termination: skip numbers that reach a value < n quickly

References:
  - Roosendaal, https://www.ericr.nl/wondrous/techpage.html
  - Angeltveit (2026), arXiv:2602.10466
  - Barina (2025), J. Supercomputing
"""

from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / "phase2"))
from collatz_baseline import collatz_stopping_time, collatz_max_value
from collatz_sieve import surviving_residues, mod9_filter


# ─── Fast Collatz Iteration with Lookup Table ─────────────────────────────────

SHORTCUT_BITS = 16  # Use 16-bit lookup table
SHORTCUT_MOD = 1 << SHORTCUT_BITS
_shortcut_table: Optional[List[Tuple[int, int, int, int]]] = None


def _build_shortcut_table() -> List[Tuple[int, int, int, int]]:
    """Build a lookup table for 16-bit shortcuts.

    For each residue r mod 2^16, precompute the result of applying
    SHORTCUT_BITS Collatz steps. After the shortcut:

        T^k(n) = (3^s * n + addend) / 2^e

    where k = SHORTCUT_BITS total steps, s = odd steps, e = even steps = k-s,
    and addend is a constant depending on the step pattern.

    We compute addend by noting:
        T^k(r) = (3^s * r + addend) / 2^e
        addend = T^k(r) * 2^e - 3^s * r

    Returns list of (multiplier_3s, addend, even_shift, total_steps) for each residue.
    """
    table = []
    k = SHORTCUT_BITS

    for r in range(1 << k):
        if r == 0:
            table.append((1, 0, k, k))
            continue

        # Simulate k steps to find T^k(r) and count odd/even steps
        n = r
        odd_count = 0
        for _ in range(k):
            if n & 1:
                n = 3 * n + 1
                odd_count += 1
            else:
                n >>= 1

        even_count = k - odd_count
        # T^k(r) = n
        # T^k(N) = (3^s * N + addend) / 2^e
        # addend = n * 2^e - 3^s * r
        three_s = 3 ** odd_count
        two_e = 1 << even_count
        addend = n * two_e - three_s * r

        table.append((three_s, addend, even_count, k))

    return table


def get_shortcut_table() -> List[Tuple[int, int, int, int]]:
    """Get or build the shortcut table (cached)."""
    global _shortcut_table
    if _shortcut_table is None:
        _shortcut_table = _build_shortcut_table()
    return _shortcut_table


def fast_stopping_time(n: int) -> int:
    """Compute Collatz stopping time using lookup table acceleration.

    Uses a 16-bit lookup table to process 16 steps at once when possible,
    falling back to single-step iteration for remaining bits.
    """
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    if n == 1:
        return 0

    table = get_shortcut_table()
    steps = 0

    while n != 1:
        if n >= SHORTCUT_MOD:
            # Use shortcut: process SHORTCUT_BITS steps at once
            r = n & (SHORTCUT_MOD - 1)
            mult, add, shift, step_count = table[r]
            n = (mult * n + add) >> shift
            steps += step_count
        else:
            # Single step for small n
            if n & 1:
                n = 3 * n + 1
            else:
                n >>= 1
            steps += 1

    return steps


def fast_max_value(n: int) -> int:
    """Compute max value in Collatz trajectory using shortcuts."""
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")

    table = get_shortcut_table()
    max_val = n

    while n != 1:
        if n >= SHORTCUT_MOD:
            r = n & (SHORTCUT_MOD - 1)
            mult, add, shift, _ = table[r]
            # Before shortcut, estimate the max value
            # The max during a shortcut is bounded by 3^s * n + add
            est_max = mult * n + add
            if est_max > max_val:
                max_val = est_max
            n = (mult * n + add) >> shift
        else:
            if n & 1:
                n = 3 * n + 1
            else:
                n >>= 1
        if n > max_val:
            max_val = n

    return max_val


# ─── Search Engine ─────────────────────────────────────────────────────────────

class CollatzSearchEngine:
    """High-performance Collatz delay record search engine.

    Combines sieving, lookup table acceleration, and multiprocessing.
    """

    def __init__(self, sieve_depth: int = 15, num_workers: int = 0):
        """Initialize the search engine.

        Args:
            sieve_depth: Depth k for modular sieve (mod 2^k)
            num_workers: Number of parallel workers (0 = auto-detect)
        """
        self.sieve_depth = sieve_depth
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        self._sieve: Optional[Set[int]] = None

    def _get_sieve(self, search_min: int) -> Set[int]:
        """Get or build the sieve for the given search range."""
        if self._sieve is None:
            self._sieve = surviving_residues(self.sieve_depth, search_min=search_min)
        return self._sieve

    def search(self, range_start: int, range_end: int,
               min_stopping_time: int = 0) -> List[Dict]:
        """Search for numbers with high stopping times in [range_start, range_end).

        Returns list of {n, stopping_time, max_value} for all numbers
        exceeding min_stopping_time threshold.
        """
        sieve = self._get_sieve(range_start)
        sieve_mod = 1 << self.sieve_depth

        # Build shortcut table
        get_shortcut_table()

        results = []
        tested = 0
        skipped = 0

        # Only test odd numbers
        start = range_start | 1
        for n in range(start, range_end, 2):
            r = n & (sieve_mod - 1)
            if r not in sieve:
                skipped += 1
                continue

            tested += 1
            st = fast_stopping_time(n)
            if st >= min_stopping_time:
                results.append({
                    "n": n,
                    "stopping_time": st,
                })

        return results

    def search_parallel(self, range_start: int, range_end: int,
                        min_stopping_time: int = 0) -> List[Dict]:
        """Parallel version of search using multiprocessing."""
        # Split range into chunks for each worker
        total = range_end - range_start
        chunk_size = max(1000, total // (self.num_workers * 4))

        chunks = []
        current = range_start
        while current < range_end:
            chunk_end = min(current + chunk_size, range_end)
            chunks.append((current, chunk_end, min_stopping_time, self.sieve_depth))
            current = chunk_end

        with mp.Pool(self.num_workers) as pool:
            chunk_results = pool.starmap(_search_chunk, chunks)

        # Merge results
        all_results = []
        for chunk in chunk_results:
            all_results.extend(chunk)

        return sorted(all_results, key=lambda x: x["stopping_time"], reverse=True)

    def find_delay_records(self, range_start: int, range_end: int,
                            known_max_time: int = 0) -> List[Dict]:
        """Find delay records in range: numbers with stopping time > known_max_time.

        This is more targeted than search(): it only returns potential
        record-holders whose stopping time exceeds the best known record
        for any number less than range_start.
        """
        results = self.search(range_start, range_end,
                              min_stopping_time=known_max_time)
        return results


def _search_chunk(start: int, end: int, min_st: int, sieve_depth: int) -> List[Dict]:
    """Worker function for parallel search (must be at module level for pickling)."""
    # Build local sieve and shortcut table
    sieve = surviving_residues(sieve_depth, search_min=start)
    sieve_mod = 1 << sieve_depth
    get_shortcut_table()

    results = []
    s = start | 1  # Start with odd number
    for n in range(s, end, 2):
        r = n & (sieve_mod - 1)
        if r not in sieve:
            continue
        st = fast_stopping_time(n)
        if st >= min_st:
            results.append({"n": n, "stopping_time": st})

    return results


# ─── Benchmark ─────────────────────────────────────────────────────────────────

def benchmark():
    """Benchmark the search engine against naive iteration."""
    print("Collatz Search Engine Benchmark")
    print("=" * 60)

    # First verify correctness
    print("\n--- Correctness Check ---")
    test_numbers = [27, 97, 871, 6171, 77031, 837799, 8400511]
    all_correct = True
    for n in test_numbers:
        naive = collatz_stopping_time(n)
        fast = fast_stopping_time(n)
        ok = naive == fast
        if not ok:
            all_correct = False
        print(f"  n={n:>10}: naive={naive:>5}, fast={fast:>5}, {'OK' if ok else 'FAIL'}")

    if not all_correct:
        print("\nFAILED: fast_stopping_time does not match naive!")
        return

    # Benchmark range
    test_range = 10_000_000

    # Naive baseline
    print(f"\n--- Naive scan [1, {test_range:,}] ---")
    start_t = time.perf_counter()
    max_naive = 0
    for n in range(1, test_range + 1):
        t = collatz_stopping_time(n)
        if t > max_naive:
            max_naive = t
    naive_time = time.perf_counter() - start_t
    naive_speed = test_range / naive_time
    print(f"  Time: {naive_time:.1f}s ({naive_speed:,.0f} numbers/sec)")
    print(f"  Max stopping time: {max_naive}")

    # Fast scan (no sieve)
    print(f"\n--- Fast scan (lookup table) [1, {test_range:,}] ---")
    start_t = time.perf_counter()
    max_fast = 0
    for n in range(1, test_range + 1):
        t = fast_stopping_time(n)
        if t > max_fast:
            max_fast = t
    fast_time = time.perf_counter() - start_t
    fast_speed = test_range / fast_time
    print(f"  Time: {fast_time:.1f}s ({fast_speed:,.0f} numbers/sec)")
    print(f"  Max stopping time: {max_fast}")
    print(f"  Speedup vs naive: {naive_time/fast_time:.1f}x")

    # Sieved + fast scan
    print(f"\n--- Sieved + fast scan [1, {test_range:,}] ---")
    engine = CollatzSearchEngine(sieve_depth=15)
    start_t = time.perf_counter()
    results = engine.search(1, test_range + 1, min_stopping_time=500)
    sieved_time = time.perf_counter() - start_t
    print(f"  Time: {sieved_time:.1f}s")
    print(f"  Numbers with st >= 500: {len(results)}")
    if results:
        best = max(results, key=lambda x: x["stopping_time"])
        print(f"  Best: n={best['n']:,}, stopping_time={best['stopping_time']}")
    print(f"  Speedup vs naive: {naive_time/sieved_time:.1f}x")

    # Save benchmark results
    bench = {
        "test_range": test_range,
        "naive": {"time_s": round(naive_time, 2), "speed": round(naive_speed)},
        "fast": {"time_s": round(fast_time, 2), "speed": round(fast_speed),
                 "speedup": round(naive_time / fast_time, 1)},
        "sieved_fast": {"time_s": round(sieved_time, 2),
                        "speedup": round(naive_time / sieved_time, 1),
                        "candidates_above_500": len(results)},
    }
    outpath = Path(__file__).parent / "search_benchmarks.json"
    outpath.write_text(json.dumps(bench, indent=2))
    print(f"\nBenchmark saved to {outpath}")


if __name__ == "__main__":
    benchmark()
