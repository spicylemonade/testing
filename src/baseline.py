#!/usr/bin/env python3
"""Naive Collatz iteration baseline with timing benchmarks.

Implements basic Collatz functions and benchmarks them against known records.
"""

import json
import time
import random
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "baselines"


def collatz_step(n: int) -> int:
    """Single Collatz step: n/2 if even, 3n+1 if odd."""
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def delay_time(n: int) -> int:
    """Total stopping time: number of steps to reach 1."""
    steps = 0
    x = n
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        steps += 1
    return steps


def glide_time(n: int) -> int:
    """Steps to first drop below starting value n."""
    if n <= 1:
        return 0
    steps = 0
    x = n
    while True:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        steps += 1
        if x < n:
            return steps


def max_excursion(n: int) -> int:
    """Highest value reached in trajectory from n to 1."""
    peak = n
    x = n
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        if x > peak:
            peak = x
    return peak


def trajectory(n: int) -> list:
    """Full trajectory from n to 1."""
    path = [n]
    x = n
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        path.append(x)
    return path


# Known A284668 records for validation
A284668_KNOWN = {
    1: (9, 19),
    2: (97, 118),
    3: (871, 178),
    4: (6171, 261),
    5: (77031, 350),
    6: (837799, 524),
    7: (8400511, 685),
    8: (63728127, 949),
    9: (670617279, 986),
    10: (9780657630, 1132),
    11: (75128138247, 1228),
    12: (989345275647, 1348),
    13: (7887663552367, 1563),
    14: (80867137596217, 1662),
    15: (942488749153153, 1862),
    16: (7579309213675935, 1958),
    17: (93571393692802302, 2091),
    18: (931386509544713451, 2283),
}


def verify_known_records(max_k=10):
    """Verify known A284668 records up to a(max_k)."""
    results = []
    for k in range(1, max_k + 1):
        n, expected_delay = A284668_KNOWN[k]
        t0 = time.perf_counter()
        actual_delay = delay_time(n)
        elapsed = time.perf_counter() - t0
        match = actual_delay == expected_delay
        results.append({
            "k": k,
            "n": n,
            "expected_delay": expected_delay,
            "actual_delay": actual_delay,
            "match": match,
            "time_seconds": round(elapsed, 6),
        })
        print(f"  a({k}) = {n}: delay={actual_delay} "
              f"{'OK' if match else 'MISMATCH'} ({elapsed:.4f}s)")
    return results


def benchmark_sampled(limit=10**9, sample_size=10000, seed=42):
    """Benchmark delay computation on random sample up to limit."""
    rng = random.Random(seed)
    samples = sorted(rng.randint(1, limit) for _ in range(sample_size))

    t0 = time.perf_counter()
    max_delay = 0
    max_n = 1
    for n in samples:
        d = delay_time(n)
        if d > max_delay:
            max_delay = d
            max_n = n
    elapsed = time.perf_counter() - t0

    return {
        "limit": limit,
        "sample_size": sample_size,
        "seed": seed,
        "total_time_seconds": round(elapsed, 4),
        "numbers_per_second": round(sample_size / elapsed, 1),
        "max_delay_in_sample": max_delay,
        "max_delay_number": max_n,
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Naive Collatz Baseline Benchmark ===\n")

    # Verify known records
    print("Verifying known A284668 records (a(1) through a(10)):")
    verification = verify_known_records(max_k=10)

    # Benchmark sampled computation
    print("\nBenchmarking on random sample up to 10^9:")
    bench = benchmark_sampled(limit=10**9, sample_size=10000)
    print(f"  {bench['sample_size']} numbers in {bench['total_time_seconds']}s "
          f"({bench['numbers_per_second']:.0f}/s)")
    print(f"  Max delay in sample: {bench['max_delay_in_sample']} "
          f"at n={bench['max_delay_number']}")

    # Also verify a few large records
    print("\nVerifying large records (a(11) through a(14)):")
    large_verification = []
    for k in range(11, 15):
        n, expected_delay = A284668_KNOWN[k]
        t0 = time.perf_counter()
        actual_delay = delay_time(n)
        elapsed = time.perf_counter() - t0
        match = actual_delay == expected_delay
        large_verification.append({
            "k": k,
            "n": n,
            "expected_delay": expected_delay,
            "actual_delay": actual_delay,
            "match": match,
            "time_seconds": round(elapsed, 6),
        })
        print(f"  a({k}) = {n}: delay={actual_delay} "
              f"{'OK' if match else 'MISMATCH'} ({elapsed:.4f}s)")

    results = {
        "benchmark_type": "naive_baseline",
        "python_version": "3.10",
        "verification_results": verification,
        "large_verification_results": large_verification,
        "sampled_benchmark": bench,
        "all_verifications_passed": all(r["match"] for r in verification + large_verification),
    }

    out_path = RESULTS_DIR / "naive_benchmark.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {out_path}")
    return results


if __name__ == "__main__":
    main()
