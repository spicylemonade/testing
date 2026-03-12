#!/usr/bin/env python3
"""Export full witness hypergraphs for selected record gaps."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-gaps", type=Path, required=True)
    parser.add_argument("--row-terms", type=Path, required=True)
    parser.add_argument("--column-terms", type=Path, required=True)
    parser.add_argument("--gaps", type=int, nargs="+", required=True)
    parser.add_argument(
        "--variant",
        choices=["original", "column_immediate"],
        default="original",
    )
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def divisors(n: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    for d in range(1, int(math.isqrt(n)) + 1):
        if n % d == 0:
            small.append(d)
            q = n // d
            if q != d:
                large.append(q)
    return small + large[::-1]


def export_gap(
    entry: dict[str, Any],
    *,
    row_terms: list[int],
    column_terms: list[int],
    variant: str,
) -> dict[str, Any]:
    step = int(entry["step"])
    row_set = set(row_terms[:step])
    column_prefix = step + 1 if variant == "column_immediate" else step
    column_set = set(column_terms[:column_prefix])

    pair_hist = Counter()
    row_factor_hist = Counter()
    column_factor_hist = Counter()
    multiplicity_mismatches = 0
    skipped_export: list[dict[str, Any]] = []

    for skipped in entry["skipped"]:
        value = int(skipped["value"])
        all_pairs: list[dict[str, int]] = []
        for row_factor in divisors(value):
            column_factor = value // row_factor
            if row_factor in row_set and column_factor in column_set:
                all_pairs.append(
                    {
                        "row_term": row_factor,
                        "column_term": column_factor,
                    }
                )

        all_pairs.sort(key=lambda pair: (pair["row_term"], pair["column_term"]))
        pair_count = len(all_pairs)
        stored_multiplicity = int(skipped["multiplicity"])
        multiplicity_mismatches += int(pair_count != stored_multiplicity)
        pair_hist[pair_count] += 1
        for pair in all_pairs:
            row_factor_hist[pair["row_term"]] += 1
            column_factor_hist[pair["column_term"]] += 1

        skipped_export.append(
            {
                "value": value,
                "is_prime": bool(skipped["is_prime"]),
                "stored_multiplicity": stored_multiplicity,
                "full_pair_count": pair_count,
                "multiplicity_matches": pair_count == stored_multiplicity,
                "all_pairs": all_pairs,
            }
        )

    return {
        "gap": int(entry["gap"]),
        "step": step,
        "previous_row_term": int(entry["previous_row_term"]),
        "next_row_term": int(entry["next_row_term"]),
        "previous_column_term": int(entry["previous_column_term"]),
        "next_column_term": int(entry["next_column_term"]),
        "offset_before": int(entry["offset_before"]),
        "offset_after": int(entry["offset_after"]),
        "skipped_count": int(entry["skipped_count"]),
        "skipped_prime_count": int(entry["skipped_prime_count"]),
        "skipped_composite_count": int(entry["skipped_composite_count"]),
        "multiplicity_mismatch_count": multiplicity_mismatches,
        "pair_count_histogram": {str(k): pair_hist[k] for k in sorted(pair_hist)},
        "total_full_pairs": sum(pair_hist[k] * k for k in pair_hist),
        "distinct_row_factors_used": len(row_factor_hist),
        "distinct_column_factors_used": len(column_factor_hist),
        "top_row_factors": [
            {"row_term": factor, "hits": count}
            for factor, count in row_factor_hist.most_common(10)
        ],
        "top_column_factors": [
            {"column_term": factor, "hits": count}
            for factor, count in column_factor_hist.most_common(10)
        ],
        "skipped": skipped_export,
    }


def main() -> int:
    args = parse_args()
    record_gaps = load_json(args.record_gaps)
    row_terms = load_json(args.row_terms)
    column_terms = load_json(args.column_terms)
    target_gaps = set(args.gaps)

    exported = [
        export_gap(
            entry,
            row_terms=row_terms,
            column_terms=column_terms,
            variant=args.variant,
        )
        for entry in record_gaps
        if int(entry["gap"]) in target_gaps
    ]
    payload = {
        "requested_gaps": sorted(target_gaps),
        "exported_gap_count": len(exported),
        "gaps": exported,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
