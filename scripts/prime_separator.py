#!/usr/bin/env python3
"""Baseline generator for Kimberling's prime separator array."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import time
from array import array
from bisect import bisect_right
from pathlib import Path
from typing import Any


ROW_PREFIX = [1, 2, 4, 7, 9, 13, 15, 18, 23, 25, 29]
COLUMN_PREFIX = [1, 3, 5, 8, 11]
TABLE_PREFIX = [
    [1, 2, 4, 7, 9, 13, 15, 18, 23, 25, 29],
    [3, 6, 12, 21, 27, 39, 45, 54, 69, 75, 87],
    [5, 10, 20, 35, 45, 65, 75, 90, 115, 125, 145],
    [8, 16, 32, 56, 72, 104, 120, 144, 184, 200, 232],
    [11, 22, 44, 77, 99, 143, 165, 198, 253, 275, 319],
]


class PrimeTable:
    def __init__(self) -> None:
        self.limit = 1
        self.is_prime = bytearray(b"\x00\x00")

    def ensure(self, n: int) -> None:
        if n <= self.limit:
            return
        sieve = bytearray(b"\x01") * (n + 1)
        sieve[0:2] = b"\x00\x00"
        bound = int(math.isqrt(n))
        for p in range(2, bound + 1):
            if sieve[p]:
                start = p * p
                sieve[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
        self.limit = n
        self.is_prime = sieve

    def check(self, n: int) -> bool:
        self.ensure(n)
        return bool(self.is_prime[n])


class ProductCoverage:
    def __init__(self, limit: int) -> None:
        self.limit = 0
        self.counts = array("I", [0])
        self.witness_row = array("Q", [0])
        self.witness_col = array("Q", [0])
        self.extend(limit)

    def extend(self, new_limit: int) -> None:
        if new_limit <= self.limit:
            return
        extra = new_limit - self.limit
        self.counts.extend(array("I", [0]) * extra)
        self.witness_row.extend(array("Q", [0]) * extra)
        self.witness_col.extend(array("Q", [0]) * extra)
        self.limit = new_limit

    def mark(self, value: int, row_term: int, column_term: int) -> None:
        self.counts[value] += 1
        if self.witness_row[value] == 0:
            self.witness_row[value] = row_term
            self.witness_col[value] = column_term

    def is_covered(self, value: int) -> bool:
        return self.counts[value] > 0

    def multiplicity(self, value: int) -> int:
        return int(self.counts[value])

    def witness(self, value: int) -> tuple[int, int]:
        return int(self.witness_row[value]), int(self.witness_col[value])


class PrimeSeparatorGenerator:
    def __init__(self, *, initial_limit: int = 128) -> None:
        self.row_terms = [1]
        self.column_terms = [1]
        self.coverage = ProductCoverage(max(8, initial_limit))
        self.coverage.mark(1, 1, 1)
        self.primes = PrimeTable()

    def _mark_new_column(self, row_term: int) -> None:
        row_limit = self.coverage.limit // row_term
        stop = bisect_right(self.column_terms, row_limit)
        for column_term in self.column_terms[:stop]:
            self.coverage.mark(row_term * column_term, row_term, column_term)

    def _mark_new_row(self, column_term: int) -> None:
        col_limit = self.coverage.limit // column_term
        stop = bisect_right(self.row_terms, col_limit)
        for row_term in self.row_terms[:stop]:
            self.coverage.mark(row_term * column_term, row_term, column_term)

    def _extend_coverage(self, new_limit: int) -> None:
        old_limit = self.coverage.limit
        self.coverage.extend(new_limit)
        for row_term in self.row_terms:
            low = old_limit // row_term
            high = new_limit // row_term
            if high <= low:
                continue
            start = bisect_right(self.column_terms, low)
            stop = bisect_right(self.column_terms, high)
            for column_term in self.column_terms[start:stop]:
                self.coverage.mark(row_term * column_term, row_term, column_term)

    def _ensure_candidate_room(self, candidate: int) -> None:
        while candidate > self.coverage.limit:
            grown = max(candidate + 64, self.coverage.limit * 2)
            self._extend_coverage(grown)

    def _next_row_term(self, start: int) -> int:
        candidate = start
        while True:
            self._ensure_candidate_room(candidate)
            if not self.coverage.is_covered(candidate):
                return candidate
            candidate += 1

    def _next_column_term(self, start: int, forbidden: int) -> int:
        candidate = start
        while True:
            self._ensure_candidate_room(candidate)
            if candidate != forbidden and not self.coverage.is_covered(candidate):
                return candidate
            candidate += 1

    def _record_gap_entry(
        self,
        *,
        step: int,
        previous_row: int,
        next_row: int,
        previous_column: int,
        next_column: int,
        current_record: int,
    ) -> dict[str, Any] | None:
        gap = next_row - previous_row
        if gap <= current_record:
            return None

        skipped: list[dict[str, Any]] = []
        prime_count = 0
        composite_count = 0
        self.primes.ensure(next_row)
        for value in range(previous_row + 1, next_row):
            if not self.coverage.is_covered(value):
                raise RuntimeError(f"uncovered skipped value at step {step}: {value}")
            row_factor, column_factor = self.coverage.witness(value)
            is_prime = self.primes.check(value)
            prime_count += int(is_prime)
            composite_count += int(not is_prime)
            skipped.append(
                {
                    "value": value,
                    "is_prime": is_prime,
                    "is_composite": not is_prime,
                    "multiplicity": self.coverage.multiplicity(value),
                    "witness": {
                        "row_term": row_factor,
                        "column_term": column_factor,
                    },
                }
            )

        return {
            "step": step,
            "previous_row_term": previous_row,
            "next_row_term": next_row,
            "previous_column_term": previous_column,
            "next_column_term": next_column,
            "gap": gap,
            "skipped_count": gap - 1,
            "skipped_prime_count": prime_count,
            "skipped_composite_count": composite_count,
            "offset_before": previous_column - previous_row,
            "offset_after": next_column - next_row,
            "skipped": skipped,
        }

    def generate(self, steps: int) -> dict[str, Any]:
        record_gaps: list[dict[str, Any]] = []
        best_gap = 0
        while len(self.row_terms) < steps:
            step = len(self.row_terms)
            previous_row = self.row_terms[-1]
            previous_column = self.column_terms[-1]
            next_row = self._next_row_term(previous_row + 1)
            next_column = self._next_column_term(next_row + 1, next_row)

            record = self._record_gap_entry(
                step=step,
                previous_row=previous_row,
                next_row=next_row,
                previous_column=previous_column,
                next_column=next_column,
                current_record=best_gap,
            )
            if record is not None:
                best_gap = int(record["gap"])
                record_gaps.append(record)

            self.row_terms.append(next_row)
            self._mark_new_column(next_row)
            self.column_terms.append(next_column)
            self._mark_new_row(next_column)

        return {
            "row_terms": self.row_terms,
            "column_terms": self.column_terms,
            "record_gaps": record_gaps,
        }


def table_preview(row_terms: list[int], column_terms: list[int], rows: int, cols: int) -> list[list[int]]:
    return [
        [column_terms[i] * row_terms[j] for j in range(cols)]
        for i in range(rows)
    ]


def validate_prefix(row_terms: list[int], column_terms: list[int]) -> dict[str, bool]:
    preview = table_preview(row_terms, column_terms, len(COLUMN_PREFIX), len(ROW_PREFIX))
    return {
        "row_prefix_matches": row_terms[: len(ROW_PREFIX)] == ROW_PREFIX,
        "column_prefix_matches": column_terms[: len(COLUMN_PREFIX)] == COLUMN_PREFIX,
        "table_prefix_matches": preview == TABLE_PREFIX,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def contract_payload(
    *,
    steps: int,
    row_terms: list[int],
    column_terms: list[int],
    record_gaps: list[dict[str, Any]],
    validation: dict[str, bool],
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
        "steps": steps,
        "row_terms": row_terms,
        "column_terms": column_terms,
        "gap_locations": gap_locations,
    }
    digest = hashlib.sha256(
        json.dumps(digest_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "steps": steps,
        "row_last": row_terms[-1],
        "column_last": column_terms[-1],
        "record_gap_count": len(record_gaps),
        "largest_record_gap": max((entry["gap"] for entry in record_gaps), default=0),
        "validation": validation,
        "gap_locations": gap_locations,
        "structural_digest_sha256": digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--initial-limit", type=int, default=128)
    parser.add_argument("--preview-rows", type=int, default=5)
    parser.add_argument("--preview-cols", type=int, default=11)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()

    started = time.perf_counter()
    generator = PrimeSeparatorGenerator(initial_limit=args.initial_limit)
    result = generator.generate(args.steps)
    elapsed = time.perf_counter() - started

    row_terms = result["row_terms"]
    column_terms = result["column_terms"]
    validation = validate_prefix(row_terms, column_terms)
    contract = contract_payload(
        steps=args.steps,
        row_terms=row_terms,
        column_terms=column_terms,
        record_gaps=result["record_gaps"],
        validation=validation,
    )
    preview = table_preview(
        row_terms,
        column_terms,
        min(args.preview_rows, len(column_terms)),
        min(args.preview_cols, len(row_terms)),
    )
    performance = {
        "steps": args.steps,
        "runtime_seconds": elapsed,
        "max_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }

    payload = {
        "contract": contract,
        "performance": performance,
        "row_terms": row_terms,
        "column_terms": column_terms,
        "table_preview": preview,
        "record_gaps": result["record_gaps"],
    }

    if args.out_dir:
        write_json(args.out_dir / "contract.json", contract)
        write_json(args.out_dir / "performance.json", performance)
        write_json(args.out_dir / "row_terms.json", row_terms)
        write_json(args.out_dir / "column_terms.json", column_terms)
        write_json(args.out_dir / "table_preview.json", preview)
        write_json(args.out_dir / "record_gaps.json", result["record_gaps"])
    else:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
