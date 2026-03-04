#!/usr/bin/env python3
"""Windowed DP heuristic for LCS (Bukh-Cox style).

Instead of full O(n²) DP, compute LCS using a diagonal band of width
T = c·√n. This reduces complexity to O(nT) = O(cn^{3/2}) while
providing a close approximation to the true LCS for random strings.

References:
  - [BukhCox2022] Bukh & Cox 2022
"""

import json
import time
import numpy as np
from pathlib import Path
import ctypes

RESULTS_DIR = Path(__file__).parent
SEED = 42

_lib_path = RESULTS_DIR / "lcs_fast.so"
_lib = None
if _lib_path.exists():
    _lib = ctypes.CDLL(str(_lib_path))
    _lib.lcs_dp.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int
    ]
    _lib.lcs_dp.restype = ctypes.c_int
    _lib.lcs_windowed.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
        ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
        ctypes.c_int
    ]
    _lib.lcs_windowed.restype = ctypes.c_int


def lcs_full(a, b):
    n, m = len(a), len(b)
    if _lib is not None:
        a_c = a.astype(np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        b_c = b.astype(np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        return _lib.lcs_dp(a_c, n, b_c, m)
    prev = [0] * (m + 1)
    for i in range(n):
        curr = [0] * (m + 1)
        for j in range(m):
            if a[i] == b[j]:
                curr[j+1] = prev[j] + 1
            else:
                curr[j+1] = max(curr[j], prev[j+1])
        prev = curr
    return prev[m]


def lcs_windowed(a, b, window):
    """Compute LCS using a diagonal band of width 2*window (C-accelerated)."""
    n, m = len(a), len(b)
    if _lib is not None:
        a_c = a.astype(np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        b_c = b.astype(np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        return _lib.lcs_windowed(a_c, n, b_c, m, window)
    # Python fallback
    prev = np.zeros(m + 1, dtype=np.int32)
    curr = np.zeros(m + 1, dtype=np.int32)
    for i in range(n):
        j_min = max(0, i - window)
        j_max = min(m - 1, i + window)
        curr[:] = 0
        if j_min > 0:
            curr[j_min] = prev[j_min]
        for j in range(j_min, j_max + 1):
            if a[i] == b[j]:
                curr[j + 1] = prev[j] + 1
            else:
                curr[j + 1] = max(curr[j], prev[j + 1])
        prev, curr = curr, prev
        curr[:] = 0
    return int(prev[m])


def compare_windowed_vs_full(n, c_values, trials, rng):
    """Compare windowed LCS against full DP for given n."""
    results = []
    
    for c in c_values:
        window = int(c * np.sqrt(n))
        
        full_scores = np.zeros(trials)
        wind_scores = np.zeros(trials)
        
        t0 = time.time()
        for t in range(trials):
            a = rng.integers(0, 2, size=n, dtype=np.uint8)
            b = rng.integers(0, 2, size=n, dtype=np.uint8)
            full_scores[t] = lcs_full(a, b)
            wind_scores[t] = lcs_windowed(a, b, window)
        elapsed = time.time() - t0
        
        full_gamma = float(np.mean(full_scores) / n)
        wind_gamma = float(np.mean(wind_scores) / n)
        diff = full_gamma - wind_gamma
        
        results.append({
            "n": n,
            "c": c,
            "window": window,
            "trials": trials,
            "full_gamma": round(full_gamma, 6),
            "windowed_gamma": round(wind_gamma, 6),
            "difference": round(diff, 6),
            "runtime_seconds": round(elapsed, 3)
        })
    
    return results


def windowed_large_n(n, c, trials, rng):
    """Run windowed DP for large n."""
    window = int(c * np.sqrt(n))
    scores = np.zeros(trials)
    
    t0 = time.time()
    for t in range(trials):
        a = rng.integers(0, 2, size=n, dtype=np.uint8)
        b = rng.integers(0, 2, size=n, dtype=np.uint8)
        scores[t] = lcs_windowed(a, b, window)
    elapsed = time.time() - t0
    
    gamma = float(np.mean(scores) / n)
    se = float(np.std(scores, ddof=1) / (n * np.sqrt(trials)))
    
    return {
        "n": n,
        "c": c,
        "window": window,
        "trials": trials,
        "gamma_estimate": round(gamma, 6),
        "gamma_se": round(se, 6),
        "ci_95": [round(gamma - 1.96*se, 6), round(gamma + 1.96*se, 6)],
        "runtime_seconds": round(elapsed, 3)
    }


def main():
    rng = np.random.default_rng(SEED)
    
    # Part 1: Compare windowed vs full for n=10000
    print("=== Windowed vs Full DP (n=10000) ===")
    print(f"{'c':>4} {'window':>7} {'full_γ':>8} {'wind_γ':>8} {'diff':>8}")
    print("-" * 45)
    
    comparison = compare_windowed_vs_full(10000, [1, 2, 4, 8], 50, rng)
    for r in comparison:
        print(f"{r['c']:>4} {r['window']:>7} {r['full_gamma']:>8.6f} "
              f"{r['windowed_gamma']:>8.6f} {r['difference']:>8.6f}")
    
    # Part 2: Large n estimates with c=4
    print("\n=== Large-n windowed estimates (c=4) ===")
    large_n_results = []
    for n in [10000, 50000, 100000]:
        trials = max(50, 200000 // n)
        r = windowed_large_n(n, 4, trials, rng)
        large_n_results.append(r)
        print(f"  n={n:>7}: γ≈{r['gamma_estimate']:.6f} ± {r['gamma_se']:.6f} "
              f"(window={r['window']}, {r['runtime_seconds']:.1f}s)")
    
    output = {
        "description": "Windowed DP heuristic for LCS estimation (Bukh-Cox style)",
        "method": "Diagonal band DP with width T = c·√n",
        "comparison_n10000": comparison,
        "large_n_estimates": large_n_results
    }
    
    outpath = RESULTS_DIR / "windowed_estimates.json"
    outpath.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {outpath}")
    
    # Check acceptance: windowed matches full to within 0.001 for c≥4
    for r in comparison:
        if r["c"] >= 4 and abs(r["difference"]) < 0.001:
            print(f"✓ c={r['c']}: difference={r['difference']:.6f} < 0.001")
        elif r["c"] >= 4:
            print(f"! c={r['c']}: difference={r['difference']:.6f} ≥ 0.001")


if __name__ == "__main__":
    main()
