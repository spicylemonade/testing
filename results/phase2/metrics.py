#!/usr/bin/env python3
"""Delay record metrics and comparison framework.

Defines data structures for tracking delay records and comparing
against literature values.

References:
  - Roosendaal (2025), https://www.ericr.nl/wondrous/delrecs.html
  - OEIS A006877 (delay record holders)
  - Lagarias (1985), "The 3x+1 problem and its generalizations"
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from collatz_baseline import collatz_stopping_time, collatz_max_value


@dataclass
class DelayRecord:
    """A Collatz delay record: a number whose stopping time exceeds all smaller numbers."""
    n: int
    stopping_time: int
    max_value: int
    path_length: int  # = stopping_time + 1 (includes start)
    discovery_timestamp: str
    source: str = "this_project"
    verified: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_computation(cls, n: int, timestamp: str = "") -> "DelayRecord":
        """Create a DelayRecord by computing all metrics for n."""
        st = collatz_stopping_time(n)
        mv = collatz_max_value(n)
        if not timestamp:
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return cls(
            n=n,
            stopping_time=st,
            max_value=mv,
            path_length=st + 1,
            discovery_timestamp=timestamp,
            verified=True,
        )


def is_new_record(n: int, stopping_time: int, known_records: List[DelayRecord]) -> bool:
    """Check if (n, stopping_time) beats all known records for numbers <= n.

    A number is a delay record if its stopping time exceeds the stopping
    time of ALL numbers less than it.

    Args:
        n: The candidate number
        stopping_time: Its stopping time
        known_records: List of known delay records sorted by n

    Returns:
        True if this is a new record (stopping_time > all known records with n' < n)
    """
    max_known_time = 0
    for rec in known_records:
        if rec.n < n:
            max_known_time = max(max_known_time, rec.stopping_time)
        elif rec.n == n:
            return False  # Already known
    return stopping_time > max_known_time


def record_summary(records: List[DelayRecord]) -> Dict:
    """Produce a JSON-serializable summary of a list of delay records."""
    if not records:
        return {"count": 0, "records": []}

    records_sorted = sorted(records, key=lambda r: r.n)
    return {
        "count": len(records_sorted),
        "min_n": records_sorted[0].n,
        "max_n": records_sorted[-1].n,
        "min_stopping_time": min(r.stopping_time for r in records_sorted),
        "max_stopping_time": max(r.stopping_time for r in records_sorted),
        "max_intermediate_value": max(r.max_value for r in records_sorted),
        "all_verified": all(r.verified for r in records_sorted),
        "records": [r.to_dict() for r in records_sorted],
    }


# Known records from Roosendaal/OEIS for comparison
LITERATURE_RECORDS = [
    (9, 19), (27, 111), (97, 118), (871, 178), (6171, 261),
    (77031, 350), (837799, 524), (8400511, 685), (63728127, 949),
    (670617279, 986),
]

# Per-decade champions from OEIS A284668
DECADE_CHAMPIONS = {
    10: (9780657630, 1132),
    11: (75128138247, 1228),
    12: (989345275647, 1348),
    13: (7887663552367, 1563),
    14: (80867137596217, 1662),
    15: (942488749153153, 1862),
}


def compare_against_literature(our_records: List[DelayRecord]) -> Dict:
    """Compare our findings against literature records."""
    comparison = {
        "our_max_stopping_time": max((r.stopping_time for r in our_records), default=0),
        "our_max_n": max((r.n for r in our_records), default=0),
        "literature_matches": [],
        "new_records": [],
        "missed_records": [],
    }

    our_dict = {r.n: r for r in our_records}

    for n, st in LITERATURE_RECORDS:
        if n in our_dict and our_dict[n].stopping_time == st:
            comparison["literature_matches"].append({"n": n, "stopping_time": st})
        elif n in our_dict:
            comparison["literature_matches"].append({
                "n": n,
                "expected": st,
                "found": our_dict[n].stopping_time,
                "match": False,
            })

    # Check for new records not in literature
    lit_ns = {n for n, _ in LITERATURE_RECORDS}
    lit_ns.update(n for n, _ in DECADE_CHAMPIONS.values())
    for rec in our_records:
        if rec.n not in lit_ns:
            # Check if this is genuinely a new record
            max_lit_time = max(st for n, st in LITERATURE_RECORDS if n < rec.n)
            if rec.stopping_time > max_lit_time:
                comparison["new_records"].append(rec.to_dict())

    return comparison


if __name__ == "__main__":
    # Demo: create records for known champions
    print("Metrics Framework Demo")
    print("=" * 50)

    records = []
    for n, expected_st in LITERATURE_RECORDS:
        rec = DelayRecord.from_computation(n)
        records.append(rec)
        match = "OK" if rec.stopping_time == expected_st else "MISMATCH"
        print(f"  {match}: n={n:>12,} st={rec.stopping_time:>5} max_val={rec.max_value:,}")

    summary = record_summary(records)
    print(f"\nSummary: {summary['count']} records, max stopping time = {summary['max_stopping_time']}")
    print(f"All verified: {summary['all_verified']}")

    outpath = Path(__file__).parent / "metrics_demo.json"
    outpath.write_text(json.dumps(summary, indent=2))
    print(f"Saved to {outpath}")
