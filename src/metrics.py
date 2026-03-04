#!/usr/bin/env python3
"""Metrics framework for Collatz computation.

Defines all metrics and verification functions used throughout the project.
"""

import json
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "metrics"


def delay_time(n: int) -> int:
    """Total stopping time: number of steps to reach 1."""
    steps = 0
    x = n
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
            steps += 2
        else:
            x >>= 1
            steps += 1
    return steps


def glide_time(n: int) -> int:
    """Steps to first drop below starting value n."""
    if n <= 1:
        return 0
    steps = 0
    x = n
    while True:
        if x & 1:
            x = (3 * x + 1) >> 1
            steps += 2
        else:
            x >>= 1
            steps += 1
        if x < n:
            return steps


def max_excursion(n: int) -> int:
    """Highest value reached in trajectory from n to 1."""
    peak = n
    x = n
    while x != 1:
        if x & 1:
            x = (3 * x + 1) >> 1
        else:
            x >>= 1
        if x > peak:
            peak = x
    return peak


def compression_ratio(n: int) -> float:
    """Ratio of bit-length of n to delay time."""
    d = delay_time(n)
    if d == 0:
        return 0.0
    return n.bit_length() / d


def verify_record(n: int, claimed_delay: int) -> dict:
    """Verify a claimed delay record. Returns detailed result."""
    actual = delay_time(n)
    return {
        "n": n,
        "claimed_delay": claimed_delay,
        "actual_delay": actual,
        "match": actual == claimed_delay,
        "glide_time": glide_time(n),
        "max_excursion": max_excursion(n),
        "bit_length": n.bit_length(),
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    definitions = {
        "metrics": [
            {
                "name": "delay_time",
                "description": "Total stopping time: number of steps to reach 1 using combined steps ((3n+1)/2 for odd, n/2 for even)",
                "unit": "steps",
                "example": {"n": 63728127, "value": 949}
            },
            {
                "name": "glide_time",
                "description": "Number of combined steps until trajectory first drops below starting value",
                "unit": "steps",
                "example": {"n": 63728127, "value": None}
            },
            {
                "name": "max_excursion",
                "description": "Highest value reached during trajectory from n to 1",
                "unit": "integer",
                "example": {"n": 63728127, "value": None}
            },
            {
                "name": "compression_ratio",
                "description": "Ratio of bit-length of n to delay time. Lower = more 'efficient' trajectory",
                "unit": "dimensionless",
                "example": {"n": 63728127, "value": None}
            },
        ],
        "verification_protocol": {
            "description": "Given (n, claimed_delay), compute delay_time(n) and check equality. Also compute glide_time, max_excursion for completeness.",
            "deterministic": True,
            "independent_of_search_method": True,
        }
    }

    # Compute examples
    for m in definitions["metrics"]:
        n = m["example"]["n"]
        if m["name"] == "delay_time":
            m["example"]["value"] = delay_time(n)
        elif m["name"] == "glide_time":
            m["example"]["value"] = glide_time(n)
        elif m["name"] == "max_excursion":
            m["example"]["value"] = max_excursion(n)
        elif m["name"] == "compression_ratio":
            m["example"]["value"] = round(compression_ratio(n), 6)

    out_path = RESULTS_DIR / "metric_definitions.json"
    out_path.write_text(json.dumps(definitions, indent=2))
    print(f"Metric definitions saved to {out_path}")
    print(json.dumps(definitions, indent=2))


if __name__ == "__main__":
    main()
