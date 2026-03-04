#!/usr/bin/env python3
"""Standalone verification script for BB(6) search candidates.

Reads results/verified_candidates.json and independently re-simulates
each candidate from scratch, confirming step counts and sigma values.

Usage:
    python3 src/verify_candidates.py
    python3 src/verify_candidates.py --top 10
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tm_simulator import TuringMachine


def verify_all(top_n=None):
    """Re-verify all candidates from verified_candidates.json."""
    candidates_path = os.path.join(
        os.path.dirname(__file__), "..", "results", "verified_candidates.json"
    )
    with open(candidates_path) as f:
        candidates = json.load(f)

    if top_n:
        candidates = candidates[:top_n]

    print(f"Verifying {len(candidates)} candidates...")
    print("=" * 70)

    all_passed = True
    for i, c in enumerate(candidates):
        notation = c["notation"]
        expected_steps = c["steps"]
        expected_sigma = c["sigma"]

        tm = TuringMachine.from_compact(notation)
        start = time.time()
        steps, ones, tape, halted = tm.simulate(max_steps=10**7)
        elapsed = time.time() - start

        passed = (
            halted
            and steps == expected_steps
            and ones == expected_sigma
        )

        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False

        print(
            f"  [{status}] #{i+1:3d}: sigma={ones:4d}, steps={steps:6d}, "
            f"halted={halted}, time={elapsed:.3f}s — {notation}"
        )

        if not passed:
            print(f"         Expected: sigma={expected_sigma}, steps={expected_steps}")

    print("=" * 70)
    if all_passed:
        print(f"ALL {len(candidates)} CANDIDATES VERIFIED SUCCESSFULLY")
    else:
        print("SOME CANDIDATES FAILED VERIFICATION")

    return all_passed


if __name__ == "__main__":
    top_n = None
    if "--top" in sys.argv:
        idx = sys.argv.index("--top")
        top_n = int(sys.argv[idx + 1])

    success = verify_all(top_n)
    sys.exit(0 if success else 1)
