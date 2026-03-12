#!/usr/bin/env python3
"""Summarize witness and prime-support observables for record gaps."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


class PrimeTable:
    def __init__(self) -> None:
        self.limit = 1
        self.is_prime = bytearray(b"\x00\x00")

    def ensure(self, n: int) -> None:
        if n <= self.limit:
            return
        sieve = bytearray(b"\x01") * (n + 1)
        sieve[0:2] = b"\x00\x00"
        for p in range(2, int(math.isqrt(n)) + 1):
            if sieve[p]:
                start = p * p
                sieve[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
        self.limit = n
        self.is_prime = sieve

    def check(self, n: int) -> bool:
        if n < 2:
            return False
        self.ensure(n)
        return bool(self.is_prime[n])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-gaps", type=Path, required=True)
    parser.add_argument("--row-terms", type=Path, required=True)
    parser.add_argument("--column-terms", type=Path, required=True)
    parser.add_argument("--gaps", type=int, nargs="*")
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def bucket_signature(*, row_factor: int, column_factor: int, multiplicity: int) -> str:
    min_factor = min(row_factor, column_factor)
    if row_factor == 1:
        return "axis1_marker"
    if min_factor <= 10:
        return "tiny_singleton" if multiplicity == 1 else "tiny_redundant"
    if min_factor > 100:
        return "balanced_singleton" if multiplicity == 1 else "balanced_redundant"
    return "mesoscopic_singleton" if multiplicity == 1 else "mesoscopic_redundant"


def summarize_gap(
    entry: dict[str, Any],
    *,
    row_terms: list[int],
    column_terms: list[int],
    primes: PrimeTable,
) -> dict[str, Any]:
    step = int(entry["step"])
    previous_row = int(entry["previous_row_term"])
    previous_column = int(entry["previous_column_term"])
    threshold = int(math.isqrt(previous_row))

    row_support = [term for term in row_terms[:step] if term <= threshold and primes.check(term)]
    column_support = [term for term in column_terms[:step] if term <= threshold and primes.check(term)]

    multiplicities = Counter()
    signatures = Counter()
    samples: dict[str, list[dict[str, int]]] = defaultdict(list)
    axis1_values: list[int] = []
    tiny_count = 0
    balanced_count = 0
    prime_row_count = 0
    prime_column_count = 0
    prime_either_count = 0

    for skipped in entry["skipped"]:
        value = int(skipped["value"])
        multiplicity = int(skipped["multiplicity"])
        row_factor = int(skipped["witness"]["row_term"])
        column_factor = int(skipped["witness"]["column_term"])
        min_factor = min(row_factor, column_factor)

        multiplicities[multiplicity] += 1
        tiny_count += int(min_factor <= 10)
        balanced_count += int(min_factor > 100)

        row_is_prime = primes.check(row_factor)
        col_is_prime = primes.check(column_factor)
        prime_row_count += int(row_is_prime)
        prime_column_count += int(col_is_prime)
        prime_either_count += int(row_is_prime or col_is_prime)

        if row_factor == 1:
            axis1_values.append(value)

        signature = bucket_signature(
            row_factor=row_factor,
            column_factor=column_factor,
            multiplicity=multiplicity,
        )
        signatures[signature] += 1
        if len(samples[signature]) < 3:
            samples[signature].append(
                {
                    "value": value,
                    "row_term": row_factor,
                    "column_term": column_factor,
                    "multiplicity": multiplicity,
                }
            )

    skipped_count = int(entry["skipped_count"])
    singleton_count = multiplicities.get(1, 0)
    return {
        "step": step,
        "gap": int(entry["gap"]),
        "previous_row_term": previous_row,
        "next_row_term": int(entry["next_row_term"]),
        "previous_column_term": previous_column,
        "next_column_term": int(entry["next_column_term"]),
        "offset_before": int(entry["offset_before"]),
        "offset_after": int(entry["offset_after"]),
        "skipped_count": skipped_count,
        "skipped_prime_count": int(entry["skipped_prime_count"]),
        "skipped_composite_count": int(entry["skipped_composite_count"]),
        "singleton_count": singleton_count,
        "singleton_share": singleton_count / skipped_count if skipped_count else 0.0,
        "multiplicity_histogram": {str(k): multiplicities[k] for k in sorted(multiplicities)},
        "axis1_value_count": len(axis1_values),
        "axis1_values": axis1_values,
        "previous_column_inside_gap": previous_row < previous_column < int(entry["next_row_term"]),
        "min_factor_le_10_count": tiny_count,
        "min_factor_le_10_share": tiny_count / skipped_count if skipped_count else 0.0,
        "min_factor_gt_100_count": balanced_count,
        "min_factor_gt_100_share": balanced_count / skipped_count if skipped_count else 0.0,
        "signature_histogram": {key: signatures[key] for key in sorted(signatures)},
        "signature_samples": {key: samples[key] for key in sorted(samples)},
        "chosen_witness_prime_row_count": prime_row_count,
        "chosen_witness_prime_column_count": prime_column_count,
        "chosen_witness_prime_either_count": prime_either_count,
        "chosen_witness_both_composite_count": skipped_count - prime_either_count,
        "row_primes_le_sqrt_prev": len(row_support),
        "column_primes_le_sqrt_prev": len(column_support),
        "support_imbalance": len(column_support) - len(row_support),
        "row_prime_support_tail": row_support[-5:],
        "column_prime_support_tail": column_support[-5:],
    }


def main() -> int:
    args = parse_args()
    record_gaps = load_json(args.record_gaps)
    row_terms = load_json(args.row_terms)
    column_terms = load_json(args.column_terms)
    selected = set(args.gaps or [])

    primes = PrimeTable()
    summaries = [
        summarize_gap(entry, row_terms=row_terms, column_terms=column_terms, primes=primes)
        for entry in record_gaps
        if not selected or int(entry["gap"]) in selected
    ]

    payload = {
        "record_gap_count": len(summaries),
        "gaps": summaries,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2) + "\n")
    else:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
