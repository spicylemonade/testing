"""Exact computation of E[L_n] for small n by exhaustive enumeration.

For each n, enumerate all 2^n x 2^n pairs of binary strings, compute LCS length
for each pair, and average. By superadditivity, max_n E[L_n]/n is a rigorous
lower bound on gamma_2.

Uses C-optimized LCS via numpy for speed, with multi-processing for larger n.
"""

import numpy as np
import json
import time
from pathlib import Path
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed


def lcs_length(x, y, n):
    """Compute LCS length of two binary strings represented as integers."""
    # Convert integers to bit arrays
    xbits = [(x >> i) & 1 for i in range(n)]
    ybits = [(y >> i) & 1 for i in range(n)]
    
    # Standard DP with 1D array
    prev = [0] * (n + 1)
    for i in range(n):
        curr = [0] * (n + 1)
        for j in range(n):
            if xbits[i] == ybits[j]:
                curr[j+1] = prev[j] + 1
            else:
                curr[j+1] = max(prev[j+1], curr[j])
        prev = curr
    return prev[n]


def compute_chunk(args):
    """Compute sum of LCS lengths for a chunk of x values."""
    n, x_start, x_end = args
    total = 0
    num_y = 1 << n
    for x in range(x_start, x_end):
        for y in range(num_y):
            total += lcs_length(x, y, n)
    return total


def exact_expected_lcs(n, num_workers=None):
    """Compute exact E[L_n] by averaging over all 2^n x 2^n binary string pairs."""
    num_pairs = (1 << n) * (1 << n)
    num_x = 1 << n
    
    if n <= 10:
        # Single-threaded for small n
        total = 0
        for x in range(num_x):
            for y in range(num_x):
                total += lcs_length(x, y, n)
        return total / num_pairs
    else:
        # Multi-threaded for larger n
        import os
        if num_workers is None:
            num_workers = min(os.cpu_count() or 4, 8)
        
        chunk_size = max(1, num_x // (num_workers * 4))
        chunks = []
        for start in range(0, num_x, chunk_size):
            end = min(start + chunk_size, num_x)
            chunks.append((n, start, end))
        
        total = 0
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(compute_chunk, chunk) for chunk in chunks]
            for future in as_completed(futures):
                total += future.result()
        
        return total / num_pairs


def main():
    print("Exact E[L_n] Computation")
    print("=" * 60)
    
    results = {}
    max_ratio = 0.0
    max_ratio_n = 0
    
    # Compute for n = 1 through 14 (or as far as feasible)
    # n=14: 2^14 * 2^14 = 2^28 ≈ 268M pairs -- may be slow but feasible
    for n in range(1, 15):
        t0 = time.time()
        num_pairs = (1 << n) * (1 << n)
        print(f"n={n}: {num_pairs} pairs...", end=" ", flush=True)
        
        expected_lcs = exact_expected_lcs(n)
        ratio = expected_lcs / n
        elapsed = time.time() - t0
        
        results[str(n)] = {
            "n": n,
            "E_L_n": round(expected_lcs, 10),
            "E_L_n_over_n": round(ratio, 10),
            "num_pairs": num_pairs,
            "elapsed_seconds": round(elapsed, 2)
        }
        
        if ratio > max_ratio:
            max_ratio = ratio
            max_ratio_n = n
        
        print(f"E[L_{n}] = {expected_lcs:.6f}, E[L_{n}]/n = {ratio:.8f} ({elapsed:.1f}s)")
        
        # Stop if taking too long (budget ~2 hours total)
        if elapsed > 3600:  # if a single n took > 1 hour
            print(f"  Stopping: n={n} took {elapsed:.0f}s")
            break
    
    # The rigorous lower bound from superadditivity
    print(f"\nRigorous lower bound (superadditivity): gamma_2 >= {max_ratio:.10f} (at n={max_ratio_n})")
    
    # Verification
    assert abs(results.get("1", {}).get("E_L_n_over_n", 0) - 0.5) < 1e-10, "E[L_1]/1 should be 0.5"
    assert abs(results.get("2", {}).get("E_L_n_over_n", 0) - 0.625) < 1e-10, "E[L_2]/2 should be 0.625"
    print("Verification passed: E[L_1]/1 = 0.5, E[L_2]/2 = 0.625")
    
    output = {
        "description": "Exact expected LCS lengths for binary strings of length n",
        "method": "exhaustive enumeration over all 2^n x 2^n string pairs",
        "rigorous_lower_bound": round(max_ratio, 10),
        "rigorous_lower_bound_n": max_ratio_n,
        "note": "By superadditivity of LCS, max_n E[L_n]/n is a rigorous lower bound on gamma_2",
        "results": results
    }
    
    outpath = Path(__file__).parent / "exact_expectations.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
