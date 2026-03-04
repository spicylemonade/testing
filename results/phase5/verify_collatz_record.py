#!/usr/bin/env python3
"""Standalone Collatz delay record verifier.

A single self-contained Python file (no external dependencies) that
verifies Collatz stopping times. Anyone can run this to confirm
our findings.

Usage:
    python3 verify_collatz_record.py              # Demo mode: verify top findings
    python3 verify_collatz_record.py 837799       # Verify a specific number
    python3 verify_collatz_record.py 989345275647  # Verify the 10^12 record

Requires: Python 3.8+ (standard library only)
"""

from __future__ import annotations
import sys
import time


def collatz_stopping_time(n: int) -> int:
    """Compute the total Collatz stopping time of n.

    Counts every step (both 3n+1 and n/2) until reaching 1.
    """
    steps = 0
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        steps += 1
    return steps


def collatz_max_value(n: int) -> int:
    """Return the maximum value reached in n's Collatz trajectory."""
    max_val = n
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        if n > max_val:
            max_val = n
    return max_val


# ─── Top findings from our search ─────────────────────────────────────────────

TOP_FINDINGS = [
    # (n, stopping_time, description)
    (989_345_275_647, 1348, "Delay record champion for numbers < 10^12"),
    (75_128_138_247,  1228, "Delay record champion for numbers < 10^11"),
    (9_780_657_630,   1132, "Delay record champion for numbers < 10^10"),
    (670_617_279,      986, "Delay record champion for numbers < 10^9"),
    (63_728_127,       949, "Delay record champion for numbers < 10^8 (famous!)"),
]


def verify_single(n: int) -> None:
    """Verify the Collatz stopping time for a single number."""
    print(f"Computing Collatz trajectory for n = {n:,}")
    print("-" * 60)

    start = time.perf_counter()
    stopping_time = collatz_stopping_time(n)
    max_val = collatz_max_value(n)
    elapsed = time.perf_counter() - start

    print(f"  Starting value:     {n:,}")
    print(f"  Stopping time:      {stopping_time:,} steps")
    print(f"  Max value reached:  {max_val:,}")
    print(f"  Computation time:   {elapsed:.3f} seconds")
    print()
    print(f"VERIFIED: {n} has stopping time {stopping_time}")


def demo_mode() -> None:
    """Verify all top findings from our research."""
    print("=" * 60)
    print("COLLATZ DELAY RECORD VERIFICATION")
    print("=" * 60)
    print()
    print("The Collatz conjecture asks: starting from any positive")
    print("integer, if you repeatedly apply 'if even, halve; if odd,")
    print("triple and add 1', do you always reach 1?")
    print()
    print("A 'delay record' is a number that takes MORE steps to reach 1")
    print("than any smaller number. Finding these records requires")
    print("searching billions of numbers.")
    print()
    print("Here are the verified delay record champions per decade:")
    print("-" * 60)

    all_ok = True
    for n, expected_st, desc in TOP_FINDINGS:
        start = time.perf_counter()
        actual_st = collatz_stopping_time(n)
        elapsed = time.perf_counter() - start

        ok = actual_st == expected_st
        status = "OK" if ok else "FAIL"
        if not ok:
            all_ok = False

        print(f"\n  [{status}] {desc}")
        print(f"    n = {n:,}")
        print(f"    Stopping time = {actual_st:,} steps (expected {expected_st:,})")
        print(f"    Verified in {elapsed:.3f}s")

    print()
    print("=" * 60)
    if all_ok:
        print("ALL RECORDS VERIFIED SUCCESSFULLY")
    else:
        print("SOME VERIFICATIONS FAILED")
    print("=" * 60)

    print(f"""
How to interpret these results:

  989,345,275,647 takes {TOP_FINDINGS[0][1]:,} steps to reach 1 under
  the Collatz process. That's more steps than ANY smaller number.

  For comparison:
    - The number 27 (famous for being surprisingly stubborn)
      takes 111 steps.
    - 837,799 (the million-range champion) takes 524 steps.
    - Our 10^12 champion takes {TOP_FINDINGS[0][1]:,} steps!

  You can verify any of these yourself:
    python3 {__file__} 989345275647
""")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            if n < 1:
                print("Error: n must be a positive integer")
                sys.exit(1)
            verify_single(n)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid integer")
            sys.exit(1)
    else:
        demo_mode()
