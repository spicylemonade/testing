#!/usr/bin/env python3
"""Nearby-rule perturbations for the prime separator array."""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prime_separator import (
    PrimeSeparatorGenerator,
    table_preview,
    write_json,
)


class VariantGenerator(PrimeSeparatorGenerator):
    def generate_variant(self, steps: int, variant: str) -> dict[str, Any]:
        record_gaps: list[dict[str, Any]] = []
        best_gap = 0
        while len(self.row_terms) < steps:
            step = len(self.row_terms)
            previous_row = self.row_terms[-1]
            previous_column = self.column_terms[-1]

            if variant == "row_immediate":
                next_row = self._next_row_term(previous_row + 1)
                record = self._record_gap_entry(
                    step=step,
                    previous_row=previous_row,
                    next_row=next_row,
                    previous_column=previous_column,
                    next_column=-1,
                    current_record=best_gap,
                )
                self.row_terms.append(next_row)
                self._mark_new_column(next_row)
                next_column = self._next_column_term(next_row + 1, next_row)
                if record is not None:
                    record["next_column_term"] = next_column
                    record["offset_after"] = next_column - next_row
                self.column_terms.append(next_column)
                self._mark_new_row(next_column)

            elif variant == "column_immediate":
                next_column = self._next_row_term(previous_row + 1)
                self.column_terms.append(next_column)
                self._mark_new_row(next_column)
                next_row = self._next_column_term(next_column + 1, next_column)
                record = self._record_gap_entry(
                    step=step,
                    previous_row=previous_row,
                    next_row=next_row,
                    previous_column=previous_column,
                    next_column=next_column,
                    current_record=best_gap,
                )
                self.row_terms.append(next_row)
                self._mark_new_column(next_row)

            else:
                raise ValueError(f"unknown variant: {variant}")

            if record is not None:
                best_gap = int(record["gap"])
                record_gaps.append(record)

        return {
            "variant": variant,
            "row_terms": self.row_terms,
            "column_terms": self.column_terms,
            "record_gaps": record_gaps,
        }


def contract_payload(
    *,
    variant: str,
    steps: int,
    row_terms: list[int],
    column_terms: list[int],
    record_gaps: list[dict[str, Any]],
) -> dict[str, Any]:
    gap_locations = [
        {
            "step": entry["step"],
            "previous_row_term": entry["previous_row_term"],
            "next_row_term": entry["next_row_term"],
            "gap": entry["gap"],
        }
        for entry in record_gaps
    ]
    digest_input = {
        "variant": variant,
        "steps": steps,
        "row_terms": row_terms,
        "column_terms": column_terms,
        "gap_locations": gap_locations,
    }
    digest = hashlib.sha256(
        json.dumps(digest_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "variant": variant,
        "steps": steps,
        "row_last": row_terms[-1],
        "column_last": column_terms[-1],
        "record_gap_count": len(record_gaps),
        "largest_record_gap": max((entry["gap"] for entry in record_gaps), default=0),
        "gap_locations": gap_locations,
        "structural_digest_sha256": digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["row_immediate", "column_immediate"], required=True)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--initial-limit", type=int, default=128)
    parser.add_argument("--preview-rows", type=int, default=5)
    parser.add_argument("--preview-cols", type=int, default=11)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    generator = VariantGenerator(initial_limit=args.initial_limit)
    result = generator.generate_variant(args.steps, args.variant)
    elapsed = time.perf_counter() - started

    row_terms = result["row_terms"]
    column_terms = result["column_terms"]
    contract = contract_payload(
        variant=args.variant,
        steps=args.steps,
        row_terms=row_terms,
        column_terms=column_terms,
        record_gaps=result["record_gaps"],
    )
    preview = table_preview(
        row_terms,
        column_terms,
        min(args.preview_rows, len(column_terms)),
        min(args.preview_cols, len(row_terms)),
    )
    performance = {
        "variant": args.variant,
        "steps": args.steps,
        "runtime_seconds": elapsed,
        "max_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }

    write_json(args.out_dir / "contract.json", contract)
    write_json(args.out_dir / "performance.json", performance)
    write_json(args.out_dir / "row_terms.json", row_terms)
    write_json(args.out_dir / "column_terms.json", column_terms)
    write_json(args.out_dir / "table_preview.json", preview)
    write_json(args.out_dir / "record_gaps.json", result["record_gaps"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
