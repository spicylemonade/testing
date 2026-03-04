#!/usr/bin/env python3
"""Verify known Collatz delay records and establish benchmarks.

Cross-references OEIS A006877 and Roosendaal's tables.
Produces known_records.json with verified entries.

References:
  - Roosendaal, https://www.ericr.nl/wondrous/delrecs.html
  - OEIS A006877
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Import baseline functions
sys.path.insert(0, str(Path(__file__).parent))
from collatz_baseline import collatz_stopping_time, collatz_max_value

# Known delay records from OEIS A006877 + A006884 (Roosendaal / Pfoertner)
# Format: (record_number, n, stopping_time)
KNOWN_DELAY_RECORDS = [
    (1, 1, 0),
    (2, 2, 1),
    (3, 3, 7),
    (4, 6, 8),
    (5, 7, 16),
    (6, 9, 19),
    (7, 18, 20),
    (8, 25, 23),
    (9, 27, 111),
    (10, 54, 112),
    (11, 73, 115),
    (12, 97, 118),
    (13, 129, 121),
    (14, 171, 124),
    (15, 231, 127),
    (16, 313, 130),
    (17, 327, 143),
    (18, 649, 144),
    (19, 703, 170),
    (20, 871, 178),
    (21, 1161, 181),
    (22, 2223, 182),
    (23, 2463, 208),
    (24, 2919, 216),
    (25, 3711, 237),
    (26, 6171, 261),
    (27, 10971, 267),
    (28, 13255, 275),
    (29, 17647, 278),
    (30, 23529, 281),
    (31, 26623, 307),
    (32, 34239, 310),
    (33, 35655, 323),
    (34, 52527, 339),
    (35, 77031, 350),
    (36, 106239, 353),
    (37, 142587, 374),
    (38, 156159, 382),
    (39, 216367, 385),
    (40, 230631, 442),
    (41, 410011, 448),
    (42, 511935, 469),
    (43, 626331, 508),
    (44, 837799, 524),
    (45, 1117065, 527),
    (46, 1501353, 530),
    (47, 1723519, 556),
    (48, 2298025, 559),
    (49, 3064033, 562),
    (50, 3542887, 583),
    (51, 3732423, 596),
    (52, 5649499, 612),
    (53, 6649279, 664),
    (54, 8400511, 685),
    (55, 11200681, 688),
    (56, 14934241, 691),
    (57, 15733191, 704),
    (58, 31466382, 705),
    (59, 36791535, 744),
    (60, 63728127, 949),
    (61, 127456254, 950),
    (62, 169941673, 953),
    (63, 226588897, 956),
    (64, 268549803, 964),
    (65, 537099606, 965),
    (66, 670617279, 986),
    (67, 1341234558, 987),
    (68, 1412987847, 1000),
    (69, 2825975694, 1001),
]

# A284668: best record per decade
RECORDS_PER_DECADE = {
    1: (9, 19),
    2: (97, 118),
    3: (871, 178),
    4: (6171, 261),
    5: (77031, 350),
    6: (837799, 524),
    7: (8400511, 685),
    8: (63728127, 949),
    9: (670617279, 986),
}


def verify_all_records():
    """Verify all known delay records and save results."""
    print("Verifying known Collatz delay records...")
    print("=" * 60)

    results = []
    failures = 0

    for rec_num, n, expected_time in KNOWN_DELAY_RECORDS:
        actual_time = collatz_stopping_time(n)
        max_val = collatz_max_value(n)
        verified = actual_time == expected_time

        if not verified:
            print(f"  FAIL: Record #{rec_num}: n={n}, expected={expected_time}, got={actual_time}")
            failures += 1
        else:
            print(f"  OK: Record #{rec_num}: n={n:>15,}, stopping_time={actual_time}, max_val={max_val:,}")

        results.append({
            "record_number": rec_num,
            "n": n,
            "stopping_time": actual_time,
            "expected_stopping_time": expected_time,
            "max_value": max_val,
            "verified": verified,
            "source": "OEIS A006877 / Roosendaal",
        })

    # Verify per-decade records
    print("\n--- Per-Decade Records (A284668) ---")
    for decade, (n, expected_time) in sorted(RECORDS_PER_DECADE.items()):
        actual = collatz_stopping_time(n)
        ok = actual == expected_time
        status = "OK" if ok else "FAIL"
        print(f"  {status}: 10^{decade}: n={n:>15,}, stopping_time={actual}")
        if not ok:
            failures += 1

    # Benchmark: naive scan up to 10^7
    print("\n--- Benchmark: naive scan up to 10^7 ---")
    start = time.perf_counter()
    max_time_seen = 0
    for i in range(1, 10_000_001):
        t = collatz_stopping_time(i)
        if t > max_time_seen:
            max_time_seen = t
    elapsed = time.perf_counter() - start
    speed = 10_000_000 / elapsed
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Speed: {speed:,.0f} numbers/sec")
    print(f"  Max stopping time found: {max_time_seen}")

    # Save results
    output = {
        "records": results,
        "per_decade_records": {str(k): {"n": v[0], "stopping_time": v[1]}
                               for k, v in RECORDS_PER_DECADE.items()},
        "benchmark": {
            "range": "1 to 10^7",
            "elapsed_seconds": round(elapsed, 2),
            "speed_numbers_per_second": round(speed),
            "max_stopping_time_in_range": max_time_seen,
        },
        "total_records_verified": len(results),
        "all_verified": failures == 0,
    }

    outpath = Path(__file__).parent / "known_records.json"
    outpath.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {outpath}")

    if failures:
        print(f"\n{failures} verification(s) FAILED")
        return False
    else:
        print(f"\nAll {len(results)} records VERIFIED ✓")
        return True


if __name__ == "__main__":
    success = verify_all_records()
    sys.exit(0 if success else 1)
