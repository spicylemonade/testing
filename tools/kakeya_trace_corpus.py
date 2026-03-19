#!/usr/bin/env python3
"""Generate exact trace artifacts for tiny arithmetic-Kakeya witnesses.

This script is intentionally narrow. It serves phase-6 theory work by:

1. Exhaustively enumerating a small exact-valid witness regime.
2. Emitting canonical synchronous trace normal forms for each witness class.
3. Exhaustively checking one-sided local strip transitions in widths 2 and 3.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
import sys

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from kakeya_ca_exact import (  # noqa: E402
    ZERO,
    Seed,
    Witness,
    normalize_witness,
    score_components,
    synchronous_trace,
    witness_to_text,
)

PALETTE = (
    (1, 0),
    (0, 1),
    (1, 1),
    (1, 2),
)
RESULTS_ROOT = Path("results/theory/forcing_traces")


@dataclass(frozen=True)
class CanonicalWitness:
    key: str
    witness: Witness
    transform: str


def sorted_seed_dicts(witness: Witness) -> list[dict[tuple[int, ...], tuple[int, int]]]:
    seeds = sorted(
        ((seed.vertex, seed.label) for seed in witness.seeds),
        key=lambda item: (item[0], item[1]),
    )
    return [{vertex: label} for vertex, label in seeds]


def witness_dict_payload(witness: Witness) -> dict[str, object]:
    return {
        "X": [list(label) for label in witness.x_labels],
        "dims": list(witness.dims),
        "f": [
            {
                str(tuple(key)): list(value)
                for key, value in sorted(mapping.items(), key=lambda item: item[0])
            }
            for mapping in witness.f_dicts
        ],
        "T": [list(vertex) for vertex in witness.initial_t],
        "R": [
            {str(tuple(vertex)): list(label)}
            for entry in sorted_seed_dicts(witness)
            for vertex, label in entry.items()
        ],
    }


def remap_vertex(vertex: tuple[int, ...], row_flip: bool, col_flip: bool) -> tuple[int, ...]:
    row, col = vertex
    if row_flip:
        row = 3 - row
    if col_flip:
        col = 3 - col
    return (row, col)


def transform_2x2_witness(witness: Witness, row_flip: bool, col_flip: bool) -> Witness:
    assert witness.dims == (2, 2)
    f1 = {}
    label = witness.f_dicts[0].get((1,), ZERO)
    if label != ZERO:
        f1[(1,)] = label
    f2 = {}
    top_label = witness.f_dicts[1].get((1, 1), ZERO)
    bottom_label = witness.f_dicts[1].get((2, 1), ZERO)
    if row_flip:
        top_label, bottom_label = bottom_label, top_label
    if top_label != ZERO:
        f2[(1, 1)] = top_label
    if bottom_label != ZERO:
        f2[(2, 1)] = bottom_label
    transformed_t = sorted(
        (remap_vertex(vertex, row_flip, col_flip) for vertex in witness.initial_t),
        key=lambda vertex: vertex,
    )
    transformed_r = [
        {
            remap_vertex(seed.vertex, row_flip, col_flip): seed.label,
        }
        for seed in sorted(
            witness.seeds,
            key=lambda seed: (seed.vertex, seed.label),
        )
    ]
    return normalize_witness(
        witness.x_labels,
        witness.dims,
        [f1, f2],
        transformed_t,
        transformed_r,
    )


def canonicalize_2x2_witness(witness: Witness) -> CanonicalWitness:
    candidates = []
    for row_flip in (False, True):
        for col_flip in (False, True):
            transformed = transform_2x2_witness(witness, row_flip=row_flip, col_flip=col_flip)
            text = witness_to_text(transformed)
            name = f"row_flip={int(row_flip)} col_flip={int(col_flip)}"
            candidates.append((text, transformed, name))
    text, transformed, name = min(candidates, key=lambda item: item[0])
    return CanonicalWitness(key=text, witness=transformed, transform=name)


def trace_signature(result) -> tuple[tuple[tuple[int, ...], ...], ...]:
    signature = []
    for layer in result.trace_layers:
        forced = tuple(sorted((tuple(item["vertex"]) for item in layer.newly_forced)))
        if forced:
            signature.append(forced)
    return tuple(signature)


def generate_2x2_full_regime() -> dict[str, object]:
    out_dir = RESULTS_ROOT / "tiny_2x2_full_seeds_le3"
    out_dir.mkdir(parents=True, exist_ok=True)

    seed_atoms = [((row, col), label) for row in (1, 2) for col in (1, 2) for label in PALETTE]
    class_entries: dict[str, dict[str, object]] = {}
    valid_count = 0
    raw_count = 0

    for edge_labels in product(PALETTE, repeat=3):
        f1 = {(1,): edge_labels[0]}
        f2 = {(1, 1): edge_labels[1], (2, 1): edge_labels[2]}
        for seed_size in range(0, 4):
            for chosen in combinations(seed_atoms, seed_size):
                raw_count += 1
                r_list = [{vertex: label} for vertex, label in chosen]
                witness = normalize_witness(
                    [ZERO, *PALETTE],
                    [2, 2],
                    [f1, f2],
                    [],
                    r_list,
                )
                result = synchronous_trace(witness)
                if not result.forced_all:
                    continue
                valid_count += 1
                canonical = canonicalize_2x2_witness(witness)
                key = canonical.key
                existing = class_entries.get(key)
                payload = {
                    "canonical_witness": witness_dict_payload(canonical.witness),
                    "canonical_witness_text": witness_to_text(canonical.witness),
                    "canonical_transform": canonical.transform,
                    "score": f"{result.score_num}/{result.score_den}",
                    "m": result.m,
                    "r": result.r,
                    "n": result.n,
                    "t": result.t,
                    "trace_signature": [[list(vertex) for vertex in layer] for layer in trace_signature(result)],
                    "trace_layers": [
                        {
                            "step": layer.step,
                            "forced_before": [list(vertex) for vertex in layer.forced_before],
                            "newly_forced": layer.newly_forced,
                        }
                        for layer in result.trace_layers
                    ],
                }
                if existing is None:
                    class_entries[key] = payload

    corpus = sorted(class_entries.values(), key=lambda item: item["canonical_witness_text"])
    for idx, payload in enumerate(corpus, start=1):
        path = out_dir / f"class_{idx:03d}.json"
        path.write_text(json.dumps(payload, indent=2) + "\n")

    signature_counts = Counter(
        tuple(tuple(tuple(vertex) for vertex in layer) for layer in entry["trace_signature"])
        for entry in corpus
    )
    scores = Counter(entry["score"] for entry in corpus)
    summary = {
        "study_regime": {
            "dims": [2, 2],
            "support": "full",
            "palette": [list(label) for label in PALETTE],
            "max_seed_atoms": 3,
            "initial_T": [],
        },
        "raw_witnesses_checked": raw_count,
        "exact_valid_witnesses": valid_count,
        "canonical_classes": len(corpus),
        "trace_signature_histogram": {
            str(k): v for k, v in sorted(signature_counts.items(), key=lambda item: str(item[0]))
        },
        "score_histogram": dict(sorted(scores.items())),
        "classes": [f"class_{idx:03d}.json" for idx in range(1, len(corpus) + 1)],
    }
    (out_dir / "corpus_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def single_column_forced_rows(height: int, vertical_labels: tuple[tuple[int, int], ...], seed_data: list[tuple[int, tuple[int, int]]]) -> tuple[int, ...]:
    f_list = [{(idx,): label for idx, label in enumerate(vertical_labels, start=1)}]
    r_list = [{(row, 1): label} for row, label in seed_data]
    witness = normalize_witness(
        [ZERO, *PALETTE],
        [height, 1],
        f_list,
        [],
        r_list,
    )
    result = synchronous_trace(witness)
    return tuple(
        row
        for row in range(1, height + 1)
        if (row, 1) in set(result.final_forced)
    )


def generate_local_transition_tables() -> dict[str, object]:
    out_dir = RESULTS_ROOT / "local_strip_states"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows2 = (1, 2)
    rows3 = (1, 2, 3)
    width2_examples = []
    width3_examples = []

    for rung in PALETTE:
        for rail_labels in product(PALETTE, repeat=2):
            for subset_size in range(3):
                for subset in combinations(rows2, subset_size):
                    seeds = [(row, rail_labels[row - 1]) for row in subset]
                    forced_rows = single_column_forced_rows(2, (rung,), seeds)
                    width2_examples.append(
                        {
                            "vertical_labels": [list(rung)],
                            "seed_rows": list(subset),
                            "seed_labels": {str(row): list(rail_labels[row - 1]) for row in subset},
                            "forced_rows": list(forced_rows),
                            "strictly_improves": len(forced_rows) > len(subset),
                        }
                    )

    for upper, lower in product(PALETTE, repeat=2):
        for rail_labels in product(PALETTE, repeat=3):
            for subset_size in range(4):
                for subset in combinations(rows3, subset_size):
                    seeds = [(row, rail_labels[row - 1]) for row in subset]
                    forced_rows = single_column_forced_rows(3, (upper, lower), seeds)
                    width3_examples.append(
                        {
                            "vertical_labels": [list(upper), list(lower)],
                            "seed_rows": list(subset),
                            "seed_labels": {str(row): list(rail_labels[row - 1]) for row in subset},
                            "forced_rows": list(forced_rows),
                            "strictly_improves": len(forced_rows) > len(subset),
                        }
                    )

    width2_summary = {
        "height": 2,
        "palette": [list(label) for label in PALETTE],
        "checked_cases": len(width2_examples),
        "strict_improvement_cases": sum(item["strictly_improves"] for item in width2_examples),
    }
    width3_summary = {
        "height": 3,
        "palette": [list(label) for label in PALETTE],
        "checked_cases": len(width3_examples),
        "strict_improvement_cases": sum(item["strictly_improves"] for item in width3_examples),
    }
    (out_dir / "width2_one_sided.json").write_text(
        json.dumps({"summary": width2_summary, "cases": width2_examples}, indent=2) + "\n"
    )
    (out_dir / "width3_one_sided.json").write_text(
        json.dumps({"summary": width3_summary, "cases": width3_examples}, indent=2) + "\n"
    )
    return {"width2": width2_summary, "width3": width3_summary}


def main() -> int:
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    tiny_summary = generate_2x2_full_regime()
    local_summary = generate_local_transition_tables()
    summary = {
        "tiny_2x2_full_seeds_le3": tiny_summary,
        "local_strip_states": local_summary,
    }
    (RESULTS_ROOT / "index.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
