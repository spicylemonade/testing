#!/usr/bin/env python3
"""Independently verify all candidate delay records from search.

Reads search_results.json and verifies every candidate by computing
the full Collatz trajectory from scratch (no sieving shortcuts).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path


def collatz_stopping_time_verify(n: int) -> int:
    """Compute Collatz stopping time by naive iteration (no shortcuts)."""
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")
    steps = 0
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        steps += 1
    return steps


def collatz_max_value_verify(n: int) -> int:
    """Compute max intermediate value by naive iteration."""
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


def main():
    results_path = Path(__file__).parent / "search_results.json"
    if not results_path.exists():
        print("ERROR: search_results.json not found. Run run_search.py first.")
        sys.exit(1)

    data = json.loads(results_path.read_text())

    # Get all unique candidates to verify
    candidates = {}
    for result in data.get("top_results", []):
        n = result["n"]
        candidates[n] = result["stopping_time"]

    for result in data.get("all_results_above_threshold", []):
        n = result["n"]
        if n not in candidates:
            candidates[n] = result["stopping_time"]

    print(f"Verifying {len(candidates)} candidates...")
    print("=" * 70)

    verified_records = []
    all_passed = True

    for n, claimed_st in sorted(candidates.items()):
        start = time.perf_counter()
        actual_st = collatz_stopping_time_verify(n)
        max_val = collatz_max_value_verify(n)
        elapsed = time.perf_counter() - start

        ok = actual_st == claimed_st
        status = "VERIFIED" if ok else "MISMATCH"
        if not ok:
            all_passed = False

        print(f"  {status}: n={n:>20,}, claimed_st={claimed_st:>5}, actual_st={actual_st:>5}, "
              f"max_val={max_val:,}, time={elapsed:.2f}s")

        verified_records.append({
            "n": n,
            "claimed_stopping_time": claimed_st,
            "verified_stopping_time": actual_st,
            "max_value": max_val,
            "verified": ok,
            "verification_time_seconds": round(elapsed, 3),
        })

    output = {
        "total_candidates": len(candidates),
        "all_verified": all_passed,
        "verified_records": verified_records,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    outpath = Path(__file__).parent / "verified_records.json"
    outpath.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {outpath}")
    print(f"ALL VERIFIED: {all_passed}")


if __name__ == "__main__":
    main()
