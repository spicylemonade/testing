#!/usr/bin/env python3
"""Optimized Collatz iteration with standard acceleration tricks.

Implements:
1. Binary shortcut (process trailing zeros at once via bit operations)
2. Combined step ((3n+1)/2 in one operation since 3n+1 is always even)
3. Lookup table for small values (precompute steps for n < 2^20)
4. Tail optimization (stop when below verified threshold)
"""

import json
import time
import random
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "baselines"

# Precompute delay for all n < LOOKUP_LIMIT
LOOKUP_BITS = 20
LOOKUP_LIMIT = 1 << LOOKUP_BITS  # 2^20 = 1,048,576


def build_lookup_table():
    """Build delay lookup table for n < 2^20."""
    table = [0] * LOOKUP_LIMIT
    # table[0] undefined, table[1] = 0
    for n in range(2, LOOKUP_LIMIT):
        x = n
        steps = 0
        while x >= n:
            # Combined step: if odd, do (3x+1)/2; if even, do x/2
            if x & 1:
                x = (3 * x + 1) >> 1
                steps += 2  # count both the 3x+1 and the /2
            else:
                x >>= 1
                steps += 1
        # x is now < n, so table[x] is already computed
        table[n] = steps + table[x]
    return table


def delay_optimized(n: int, lookup: list) -> int:
    """Compute delay using combined steps and lookup table."""
    x = n
    steps = 0
    while x >= LOOKUP_LIMIT:
        if x & 1:
            x = (3 * x + 1) >> 1
            steps += 2
        else:
            # Count trailing zeros for batch shift
            tz = (x & -x).bit_length() - 1
            x >>= tz
            steps += tz
    return steps + lookup[x]


def delay_no_lookup(n: int) -> int:
    """Optimized delay without lookup table (for comparison)."""
    x = n
    steps = 0
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
            steps += 2
        else:
            tz = (x & -x).bit_length() - 1
            x >>= tz
            steps += tz
    return steps


# Import known records for validation
from baseline import A284668_KNOWN


def verify_known_records(lookup, max_k=14):
    """Verify known records with optimized function."""
    results = []
    for k in range(1, max_k + 1):
        n, expected_delay = A284668_KNOWN[k]
        t0 = time.perf_counter()
        actual_delay = delay_optimized(n, lookup)
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
              f"{'OK' if match else 'MISMATCH'} ({elapsed:.6f}s)")
    return results


def benchmark_sampled(lookup, limit=10**9, sample_size=10000, seed=42):
    """Benchmark on random sample."""
    rng = random.Random(seed)
    samples = sorted(rng.randint(1, limit) for _ in range(sample_size))

    t0 = time.perf_counter()
    max_delay = 0
    max_n = 1
    for n in samples:
        d = delay_optimized(n, lookup)
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


def benchmark_range_scan(lookup, limit=10**7):
    """Scan all numbers up to limit, find max delay."""
    t0 = time.perf_counter()
    max_delay = 0
    max_n = 1
    for n in range(2, limit + 1):
        d = delay_optimized(n, lookup)
        if d > max_delay:
            max_delay = d
            max_n = n
    elapsed = time.perf_counter() - t0
    return {
        "limit": limit,
        "total_time_seconds": round(elapsed, 4),
        "numbers_per_second": round(limit / elapsed, 1),
        "max_delay": max_delay,
        "max_delay_number": max_n,
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Optimized Collatz Benchmark ===\n")

    print("Building lookup table (2^20 entries)...")
    t0 = time.perf_counter()
    lookup = build_lookup_table()
    lookup_time = time.perf_counter() - t0
    print(f"  Lookup table built in {lookup_time:.3f}s\n")

    # Verify known records
    print("Verifying known A284668 records:")
    verification = verify_known_records(lookup, max_k=14)

    # Sampled benchmark
    print("\nBenchmarking on random sample up to 10^9:")
    bench_sample = benchmark_sampled(lookup, limit=10**9, sample_size=10000)
    print(f"  {bench_sample['numbers_per_second']:.0f} numbers/s")

    # Range scan benchmark
    print("\nScanning all numbers up to 10^7:")
    bench_range = benchmark_range_scan(lookup, limit=10**7)
    print(f"  {bench_range['numbers_per_second']:.0f} numbers/s")
    print(f"  Max delay: {bench_range['max_delay']} at n={bench_range['max_delay_number']}")

    # Compare with naive baseline
    from baseline import delay_time as naive_delay
    print("\nSpeedup comparison (10000 random numbers up to 10^9):")
    rng = random.Random(42)
    samples = [rng.randint(1, 10**9) for _ in range(10000)]

    t0 = time.perf_counter()
    for n in samples:
        naive_delay(n)
    naive_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for n in samples:
        delay_optimized(n, lookup)
    opt_time = time.perf_counter() - t0

    speedup = naive_time / opt_time if opt_time > 0 else float('inf')
    print(f"  Naive: {naive_time:.4f}s, Optimized: {opt_time:.4f}s, Speedup: {speedup:.1f}x")

    results = {
        "benchmark_type": "optimized",
        "lookup_bits": LOOKUP_BITS,
        "lookup_build_time_seconds": round(lookup_time, 3),
        "verification_results": verification,
        "sampled_benchmark": bench_sample,
        "range_scan_benchmark": bench_range,
        "speedup_vs_naive": round(speedup, 1),
        "all_verifications_passed": all(r["match"] for r in verification),
    }

    out_path = RESULTS_DIR / "optimized_benchmark.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {out_path}")
    return results


if __name__ == "__main__":
    main()
