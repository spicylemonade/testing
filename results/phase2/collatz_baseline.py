#!/usr/bin/env python3
"""Collatz conjecture baseline implementation with verification.

Provides naive iteration for computing stopping times, full trajectories,
and delay record verification. Used as ground truth for all optimized variants.

References:
  - Lagarias (1985), "The 3x+1 problem and its generalizations"
  - Roosendaal, https://www.ericr.nl/wondrous/delrecs.html
  - OEIS A006877, A006577
"""

from __future__ import annotations

import sys
import time
from typing import List, Tuple


def collatz_stopping_time(n: int) -> int:
    """Return the total stopping time of n (steps to reach 1).

    Both halving and tripling steps are counted.
    For n=1, returns 0.

    >>> collatz_stopping_time(1)
    0
    >>> collatz_stopping_time(27)
    111
    >>> collatz_stopping_time(9663)
    184
    """
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")
    steps = 0
    while n != 1:
        if n & 1:  # odd
            n = 3 * n + 1
        else:       # even
            n >>= 1
        steps += 1
    return steps


def collatz_path(n: int) -> List[int]:
    """Return the full Collatz trajectory from n down to 1.

    >>> collatz_path(6)
    [6, 3, 10, 5, 16, 8, 4, 2, 1]
    """
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")
    path = [n]
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        path.append(n)
    return path


def collatz_max_value(n: int) -> int:
    """Return the maximum value reached in the Collatz trajectory of n.

    >>> collatz_max_value(27)
    9232
    """
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")
    max_val = n
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        if n > max_val:
            max_val = n
    return max_val


def verify_delay_record(n: int, claimed_time: int) -> bool:
    """Verify that n has exactly the claimed stopping time.

    >>> verify_delay_record(27, 111)
    True
    >>> verify_delay_record(27, 100)
    False
    """
    return collatz_stopping_time(n) == claimed_time


def find_delay_records(up_to: int) -> List[Tuple[int, int]]:
    """Find all delay record holders up to `up_to`.

    Returns list of (n, stopping_time) where n has a longer stopping time
    than all numbers less than n.
    """
    records: List[Tuple[int, int]] = []
    max_time = -1
    for n in range(1, up_to + 1):
        t = collatz_stopping_time(n)
        if t > max_time:
            max_time = t
            records.append((n, t))
    return records


def benchmark_naive(limit: int) -> float:
    """Benchmark naive iteration speed. Returns numbers/second."""
    start = time.perf_counter()
    for n in range(1, limit + 1):
        collatz_stopping_time(n)
    elapsed = time.perf_counter() - start
    return limit / elapsed


# ─── Unit Tests ───────────────────────────────────────────────────────────────

def run_tests():
    """Run all unit tests. Exit with code 1 on failure."""
    failures = 0

    # Test 1: Known stopping times
    known = {
        1: 0,
        2: 1,
        3: 7,
        6: 8,
        7: 16,
        9: 19,
        27: 111,
        97: 118,
        871: 178,
        6171: 261,
        9663: 184,
        77031: 350,
        113383: 247,
        837799: 524,
    }
    for n, expected in known.items():
        actual = collatz_stopping_time(n)
        if actual != expected:
            print(f"FAIL: collatz_stopping_time({n}) = {actual}, expected {expected}")
            failures += 1
        else:
            print(f"  OK: collatz_stopping_time({n}) = {actual}")

    # Test 2: Path correctness
    path_27 = collatz_path(27)
    if path_27[0] != 27 or path_27[-1] != 1 or len(path_27) != 112:
        print(f"FAIL: collatz_path(27) length={len(path_27)}, expected 112")
        failures += 1
    else:
        print(f"  OK: collatz_path(27) has {len(path_27)} elements")

    # Test 3: Max value
    mv27 = collatz_max_value(27)
    if mv27 != 9232:
        print(f"FAIL: collatz_max_value(27) = {mv27}, expected 9232")
        failures += 1
    else:
        print(f"  OK: collatz_max_value(27) = {mv27}")

    # Test 4: Verify delay record
    if not verify_delay_record(27, 111):
        print("FAIL: verify_delay_record(27, 111) returned False")
        failures += 1
    else:
        print("  OK: verify_delay_record(27, 111) = True")

    if verify_delay_record(27, 100):
        print("FAIL: verify_delay_record(27, 100) returned True")
        failures += 1
    else:
        print("  OK: verify_delay_record(27, 100) = False")

    # Test 5: Delay records up to 1000
    records = find_delay_records(1000)
    expected_records_in_range = [(1, 0), (2, 1), (3, 7), (6, 8), (7, 16), (9, 19),
                                  (18, 20), (25, 23), (27, 111), (54, 112),
                                  (73, 115), (97, 118), (129, 121), (171, 124),
                                  (231, 127), (313, 130), (327, 143), (649, 144),
                                  (703, 170), (871, 178)]
    for n, t in expected_records_in_range:
        if (n, t) not in records:
            print(f"FAIL: delay record ({n}, {t}) not found in find_delay_records(1000)")
            failures += 1

    if len(records) == len(expected_records_in_range):
        print(f"  OK: find_delay_records(1000) found {len(records)} records (matches expected)")
    else:
        print(f"  INFO: find_delay_records(1000) found {len(records)} records, expected {len(expected_records_in_range)}")

    # Benchmark
    print("\n--- Benchmark ---")
    speed = benchmark_naive(100_000)
    print(f"  Naive iteration speed: {speed:,.0f} numbers/sec (range 1..100,000)")

    if failures:
        print(f"\n{failures} test(s) FAILED")
        sys.exit(1)
    else:
        print(f"\nAll tests PASSED")


if __name__ == "__main__":
    run_tests()
