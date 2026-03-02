#!/usr/bin/env python3
"""
Verify the 2-adic Linear Variance Law for Collatz stopping times.

CONJECTURE: The fraction of stopping time variance explained by n mod 2^k
grows linearly: R²(k) ≈ α·k, where α ≈ 0.012.

This script reproduces the key result in under 5 minutes.
No external dependencies beyond numpy and scipy.

Usage:
    python verify_discovery.py [max_n]

Default: max_n = 500000
"""

import sys
import time
import numpy as np
from scipy import stats


def batch_stopping_times(max_n):
    """Compute Collatz stopping times for n=1..max_n via memoization."""
    cache = {1: 0}
    results = [0] * (max_n + 1)
    for n in range(2, max_n + 1):
        seq = []
        current = n
        while current not in cache:
            seq.append(current)
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
        base = cache[current]
        for i, val in enumerate(reversed(seq)):
            cache[val] = base + i + 1
        results[n] = cache[n]
    return results


def verify(max_n=500000):
    """Verify the 2-adic linear variance law."""
    print(f"=" * 60)
    print(f"VERIFYING: 2-adic Linear Variance Law")
    print(f"  n = 1..{max_n:,}")
    print(f"=" * 60)

    t0 = time.time()

    # Step 1: Compute stopping times
    print("\n[1/3] Computing stopping times...", end=" ", flush=True)
    st = batch_stopping_times(max_n)
    st_array = np.array(st[1:], dtype=np.float64)
    ns = np.arange(1, max_n + 1)
    print(f"done ({time.time() - t0:.1f}s)")

    grand_mean = st_array.mean()
    ss_total = np.sum((st_array - grand_mean) ** 2)

    # Step 2: Compute R² for each k
    # Limit k so each group has at least ~100 observations (avoids overfitting)
    print("[2/3] Computing R² decomposition...", end=" ", flush=True)
    ks = []
    r2s = []
    max_k = 20
    min_group_size = 100
    for k in range(1, max_k + 1):
        mod = 2 ** k
        if mod > max_n // min_group_size:
            break
        residues = ns % mod
        group_means = np.zeros(mod)
        for r in range(mod):
            mask = residues == r
            if mask.any():
                group_means[r] = st_array[mask].mean()
        predicted = group_means[residues]
        ss_between = np.sum((predicted - grand_mean) ** 2)
        r2 = ss_between / ss_total
        ks.append(k)
        r2s.append(r2)
    print(f"done ({time.time() - t0:.1f}s)")

    # Step 3: Fit linear model
    print("[3/3] Fitting linear model...", end=" ", flush=True)
    slope, intercept, r_value, p_value, std_err = stats.linregress(ks, r2s)
    print(f"done ({time.time() - t0:.1f}s)")

    # Report
    print(f"\n{'=' * 60}")
    print(f"RESULTS")
    print(f"{'=' * 60}")
    print(f"\nR² by 2-adic precision level k:")
    print(f"{'k':>4s} {'mod 2^k':>10s} {'R²':>10s}")
    print(f"{'-'*4:>4s} {'-'*10:>10s} {'-'*10:>10s}")
    for k, r2 in zip(ks, r2s):
        print(f"{k:>4d} {2**k:>10,d} {r2:>10.6f}")

    print(f"\nLinear fit: R²(k) = {slope:.6f} * k + {intercept:.6f}")
    print(f"  Slope α = {slope:.6f} ± {std_err:.6f}")
    print(f"  Fit quality R² = {r_value**2:.4f}")
    print(f"  Interpretation: each additional bit of 2-adic precision")
    print(f"    explains {slope*100:.2f}% more of stopping time variance")

    # Verification checks
    print(f"\n{'=' * 60}")
    print(f"VERIFICATION CHECKS")
    print(f"{'=' * 60}")

    checks_passed = 0
    total_checks = 4

    # Check 1: Slope is positive and in expected range
    check1 = 0.005 < slope < 0.025
    checks_passed += int(check1)
    print(f"  [{'PASS' if check1 else 'FAIL'}] Slope α ∈ (0.005, 0.025): α = {slope:.6f}")

    # Check 2: Linear fit is good (R² > 0.95)
    check2 = r_value ** 2 > 0.95
    checks_passed += int(check2)
    print(f"  [{'PASS' if check2 else 'FAIL'}] Fit R² > 0.95: R² = {r_value**2:.4f}")

    # Check 3: R² at k=1 (mod 2) is small but positive
    check3 = 0.005 < r2s[0] < 0.05
    checks_passed += int(check3)
    print(f"  [{'PASS' if check3 else 'FAIL'}] R²(k=1) ∈ (0.005, 0.05): R² = {r2s[0]:.6f}")

    # Check 4: R² grows monotonically
    check4 = all(r2s[i] < r2s[i+1] for i in range(len(r2s) - 1))
    checks_passed += int(check4)
    print(f"  [{'PASS' if check4 else 'FAIL'}] R² is monotonically increasing")

    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"  {checks_passed}/{total_checks} checks passed")
    print(f"  Elapsed time: {elapsed:.1f}s")
    print(f"{'=' * 60}")

    if checks_passed == total_checks:
        print("\n  *** CONJECTURE VERIFIED ***")
        print(f"  The 2-adic linear variance law R²(k) ≈ {slope:.4f}·k")
        print(f"  holds for n = 1..{max_n:,}")
    else:
        print("\n  Some checks failed — investigate further.")

    return {
        "verified": checks_passed == total_checks,
        "slope": float(slope),
        "slope_std_err": float(std_err),
        "fit_r_squared": float(r_value ** 2),
        "r2_values": dict(zip(ks, r2s)),
        "elapsed_seconds": elapsed,
    }


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 500000
    verify(max_n)
