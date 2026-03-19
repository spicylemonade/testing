#!/usr/bin/env python3
"""Phase 6 experiment runners for exact CA-style arithmetic Kakeya tests."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phase6_exact import (
    GridInstance,
    build_payload,
    coordinate_height,
    dump_json,
    greedy_seed_search_grid,
    random_search_grid,
)


Vector = Tuple[int, int]

RESULTS = ROOT / "results"

LOW_HEIGHT_X_FAMILIES: Dict[str, Tuple[Vector, ...]] = {
    "asym_a": ((0, 0), (1, 0), (0, 1), (1, 1), (2, -1)),
    "asym_b": ((0, 0), (1, 0), (0, 1), (2, -1), (2, 1)),
    "asym_c": ((0, 0), (1, 0), (0, 1), (1, 2), (2, -1)),
}

ROW_SWAP = {
    "closed": "closed",
    "top": "bottom",
    "bottom": "top",
    "gate_up": "gate_down",
    "gate_down": "gate_up",
}


@dataclass(frozen=True)
class H4Grammar:
    family_id: str
    x_labels: Tuple[Vector, ...]
    interface_alphabet: Tuple[str, ...]
    horizontal_map_h2: Dict[str, Tuple[Vector, Vector]]
    vertical_h2: Tuple[Vector, ...]
    symmetry_quotient: str
    extractor_note: str


def make_h4_grammar(family_id: str, x_labels: Sequence[Vector]) -> H4Grammar:
    zero, a, b, c, d = x_labels
    return H4Grammar(
        family_id=family_id,
        x_labels=tuple(x_labels),
        interface_alphabet=("closed", "top", "bottom", "gate_up", "gate_down"),
        horizontal_map_h2={
            "closed": (zero, zero),
            "top": (a, zero),
            "bottom": (zero, b),
            "gate_up": (c, d),
            "gate_down": (d, c),
        },
        vertical_h2=(c,),
        symmetry_quotient=(
            "canonicalize width-4 interface words by horizontal reversal and the row-swap "
            "involution top<->bottom, gate_up<->gate_down"
        ),
        extractor_note=(
            "Each interface symbol maps to a fixed two-row connector pattern over the frozen X: "
            "closed->(0,0), top->(a,0), bottom->(0,b), gate_up->(c,d), gate_down->(d,c). "
            "The vertical profile is fixed to c on every column."
        ),
    )


def canonical_word(word: Sequence[str]) -> Tuple[str, ...]:
    base = tuple(word)
    swapped = tuple(ROW_SWAP[symbol] for symbol in base)
    variants = (
        base,
        tuple(reversed(base)),
        swapped,
        tuple(reversed(swapped)),
    )
    return min(variants)


def canonical_words(alphabet: Sequence[str], length: int) -> List[Tuple[str, ...]]:
    return sorted({canonical_word(word) for word in itertools.product(alphabet, repeat=length)})


def word_to_horizontal(
    word: Sequence[str],
    symbol_map: Dict[str, Sequence[Vector]],
) -> Tuple[Tuple[Vector, ...], ...]:
    rows: List[List[Vector]] = [[] for _ in range(len(next(iter(symbol_map.values()))))]
    for symbol in word:
        labels = symbol_map[symbol]
        for row, label in enumerate(labels):
            rows[row].append(label)
    return tuple(tuple(row) for row in rows)


def serialize_word(word: Sequence[str]) -> str:
    return "".join(symbol[0].upper() for symbol in word)


def evaluate_level1_words(
    grammar: H4Grammar,
    *,
    seed_budget: int,
    initial_t_budget: int,
    boundary_band: int,
) -> Dict[str, object]:
    words = canonical_words(grammar.interface_alphabet, length=3)
    rows: List[Dict[str, object]] = []
    forcing_rows: List[Dict[str, object]] = []
    for word in words:
        horizontal = word_to_horizontal(word, grammar.horizontal_map_h2)
        instance = greedy_seed_search_grid(
            height=2,
            width=4,
            x_labels=grammar.x_labels,
            vertical=grammar.vertical_h2,
            horizontal=horizontal,
            seed_budget=seed_budget,
            initial_t_budget=initial_t_budget,
            boundary_band=boundary_band,
        )
        forcing = instance is not None and instance.is_forcing()
        row = {
            "word": list(word),
            "word_id": serialize_word(word),
            "forcing": forcing,
            "score": None if not forcing else instance.score,
            "grammar_length": 3,
            "active_state_count": len(set(word)),
            "seed_count": 0 if instance is None else instance.r,
            "initial_t_count": 0 if instance is None else instance.t,
            "certificate_lines": None if not forcing else instance.to_certificate_lines(),
            "instance": None,
        }
        if forcing:
            row["instance"] = {
                "vertical": [list(label) for label in instance.vertical],
                "horizontal": [
                    [list(label) for label in horizontal_row]
                    for horizontal_row in instance.horizontal
                ],
                "seeds": [[list(vertex), list(label)] for vertex, label in instance.seeds],
                "initial_t": [list(vertex) for vertex in instance.initial_t],
            }
            forcing_rows.append(row)
        rows.append(row)
    rows.sort(key=lambda row: (row["score"] is None, row["score"] or 999.0, row["word_id"]))
    forcing_rows.sort(key=lambda row: (row["score"], row["word_id"]))
    return {
        "candidate_words": rows,
        "forcing_words": forcing_rows,
    }


def shift_vertices(entries: Sequence[Tuple[Tuple[int, int], Tuple[int, int]]], delta: int):
    return tuple((((row, col + delta), label) for (row, col), label in entries))


def shift_points(entries: Sequence[Tuple[int, int]], delta: int):
    return tuple((row, col + delta) for row, col in entries)


def compose_level1_instances(
    grammar: H4Grammar,
    left_row: Dict[str, object],
    right_row: Dict[str, object],
    bridge_symbol: str,
) -> GridInstance:
    left = left_row["instance"]
    right = right_row["instance"]
    if left is None or right is None:
        raise ValueError("composition requires forcing level-1 rows")
    bridge = grammar.horizontal_map_h2[bridge_symbol]
    left_horizontal = tuple(tuple(tuple(label) for label in row) for row in left["horizontal"])
    right_horizontal = tuple(tuple(tuple(label) for label in row) for row in right["horizontal"])
    horizontal = []
    for row_idx in range(2):
        horizontal.append(left_horizontal[row_idx] + (bridge[row_idx],) + right_horizontal[row_idx])
    left_seeds = tuple((tuple(vertex), tuple(label)) for vertex, label in left["seeds"])
    right_seeds = tuple((tuple(vertex), tuple(label)) for vertex, label in right["seeds"])
    left_t = tuple(tuple(vertex) for vertex in left["initial_t"])
    right_t = tuple(tuple(vertex) for vertex in right["initial_t"])
    return GridInstance(
        height=2,
        width=8,
        x_labels=grammar.x_labels,
        vertical=grammar.vertical_h2,
        horizontal=tuple(tuple(row) for row in horizontal),
        seeds=left_seeds + tuple(((row, col + 4), label) for (row, col), label in right_seeds),
        initial_t=left_t + tuple((row, col + 4) for row, col in right_t),
    )


def evaluate_level2_compositions(
    grammar: H4Grammar,
    level1_forcing_rows: Sequence[Dict[str, object]],
) -> Dict[str, object]:
    rows: List[Dict[str, object]] = []
    best_instance = None
    forcing_count = 0
    for left_row in level1_forcing_rows:
        for right_row in level1_forcing_rows:
            for bridge_symbol in grammar.interface_alphabet:
                instance = compose_level1_instances(grammar, left_row, right_row, bridge_symbol)
                closure_size = instance.closure_size_fast()
                forcing = closure_size == instance.n and instance.is_forcing()
                if forcing:
                    forcing_count += 1
                    if best_instance is None or instance.score < best_instance.score:
                        best_instance = instance
                rows.append(
                    {
                        "left_word": left_row["word"],
                        "right_word": right_row["word"],
                        "bridge_symbol": bridge_symbol,
                        "closure_size": closure_size,
                        "forcing": forcing,
                        "score": None if not forcing else instance.score,
                        "grammar_length": 7,
                        "active_state_count": len(
                            set(left_row["word"]) | set(right_row["word"]) | {bridge_symbol}
                        ),
                        "certificate_lines": None if not forcing else instance.to_certificate_lines(),
                    }
                )
    rows.sort(key=lambda row: (row["score"] is None, row["score"] or 999.0))
    return {
        "candidate_count": len(rows),
        "forcing_count": forcing_count,
        "hit_rate": 0.0 if not rows else forcing_count / len(rows),
        "best": None
        if best_instance is None
        else build_payload(
            best_instance,
            candidate_count=len(rows),
            x_labels=grammar.x_labels,
            height=2,
            width=8,
            seed_budget=0,
            initial_t_budget=0,
            boundary_band=0,
            grammar_length=7,
            active_state_count=len(best_instance.distinct_nonzero_labels),
            extractor_complexity=len(grammar.interface_alphabet),
        )["best"],
        "rows": rows,
    }


def aggregate_direct_search(
    grammar: H4Grammar,
    *,
    trials: int,
    seed_budget: int,
    initial_t_budget: int,
    boundary_band: int,
    seeds: Sequence[int],
) -> Dict[str, object]:
    runs = []
    best = None
    forcing_trials = 0
    for rng_seed in seeds:
        payload = random_search_grid(
            height=2,
            width=8,
            x_labels=grammar.x_labels,
            trials=trials,
            seed_budget=seed_budget,
            initial_t_budget=initial_t_budget,
            boundary_band=boundary_band,
            allow_zero_horizontal=True,
            rng_seed=rng_seed,
        )
        run_forcing = sum(1 for row in payload["history"] if row["forcing"])
        forcing_trials += run_forcing
        if payload["best"] is not None:
            if best is None or payload["best"]["score"] < best["score"]:
                best = payload["best"]
        runs.append(
            {
                "rng_seed": rng_seed,
                "forcing_trials": run_forcing,
                "trial_count": trials,
                "best_score": None if payload["best"] is None else payload["best"]["score"],
                "payload": payload,
            }
        )
    total_trials = trials * len(seeds)
    hit_rate = 0.0 if total_trials == 0 else forcing_trials / total_trials
    return {
        "total_trials": total_trials,
        "forcing_trials": forcing_trials,
        "hit_rate": hit_rate,
        "best": best,
        "runs": runs,
    }


def choose_best_family() -> Tuple[H4Grammar, Dict[str, object]]:
    family_id = "asym_a"
    grammar = make_h4_grammar(family_id, LOW_HEIGHT_X_FAMILIES[family_id])
    level1 = evaluate_level1_words(
        grammar,
        seed_budget=4,
        initial_t_budget=1,
        boundary_band=1,
    )
    return grammar, level1


def write_typed_residue_results() -> Dict[str, object]:
    grammar, level1 = choose_best_family()
    best_level1_score = None if not level1["forcing_words"] else level1["forcing_words"][0]["score"]
    level1_summaries = [
        row
        for row in level1["forcing_words"]
        if row["score"] == best_level1_score
    ]
    level2 = evaluate_level2_compositions(grammar, level1_summaries)
    direct_seed_count = 2
    direct_total_budget = max(60, min(level2["candidate_count"], 240))
    direct = aggregate_direct_search(
        grammar,
        trials=max(math.ceil(direct_total_budget / direct_seed_count), 30),
        seed_budget=4,
        initial_t_budget=1,
        boundary_band=1,
        seeds=(3101, 3102),
    )
    route_best = None if level2["best"] is None else level2["best"]["score"]
    direct_best = None if direct["best"] is None else direct["best"]["score"]
    pass_score = (
        route_best is not None
        and direct_best is not None
        and route_best < direct_best
    )
    pass_hit_rate = level2["hit_rate"] > direct["hit_rate"]
    passed = pass_score or pass_hit_rate
    if level1["forcing_words"]:
        reason = (
            "The fixed-alphabet route composes without repair but fails to beat matched direct width-8 search "
            "on best exact score or hit rate."
        )
    else:
        reason = (
            "The frozen interface grammar produces no width-4 forcing word under the matched boundary-seed budget, "
            "so the route never reaches a nontrivial no-repair level-2 comparison."
        )
    decision = {
        "passed": passed,
        "reason": (
            "The fixed-alphabet route composes width-4 forcing witnesses into width-8 legal certificates "
            "with no new interface symbols or repair."
            if passed
            else reason
        ),
        "beat_direct_on_score": pass_score,
        "beat_direct_on_hit_rate": pass_hit_rate,
    }
    payload = {
        "route": "H4_typed_residue_interfaces",
        "frozen_family": {
            "family_id": grammar.family_id,
            "x_labels": [list(label) for label in grammar.x_labels],
            "coordinate_height": coordinate_height(grammar.x_labels),
        },
        "interface_alphabet": list(grammar.interface_alphabet),
        "symmetry_quotient": grammar.symmetry_quotient,
        "extractor": {
            "note": grammar.extractor_note,
            "vertical_h2": [list(label) for label in grammar.vertical_h2],
            "horizontal_map_h2": {
                symbol: [list(label) for label in labels]
                for symbol, labels in grammar.horizontal_map_h2.items()
            },
        },
        "level1": {
            "candidate_count": len(level1["candidate_words"]),
            "forcing_count": len(level1["forcing_words"]),
            "forcing_hit_rate": 0.0
            if not level1["candidate_words"]
            else len(level1["forcing_words"]) / len(level1["candidate_words"]),
            "best_score": None
            if not level1["forcing_words"]
            else level1["forcing_words"][0]["score"],
            "summary_count_used_for_level2": len(level1_summaries),
            "forcing_words": level1["forcing_words"],
        },
        "level2": level2,
        "matched_direct_width8": direct,
        "decision": decision,
        "novelty_note": (
            "The current prior-art gap log covers bootstrap-percolation and macrocell folklore only at the "
            "metaphor level. It does not contain an exact verifier-backed audit where a fixed finite interface "
            "alphabet is frozen first, actual width-4 legal certificates are composed without repair, and the "
            "composed width-8 family is then benchmarked against matched direct no-CA search."
        ),
    }
    dump_json(RESULTS / "phase6_h4_typed_residue_interfaces.json", payload)
    write_typed_residue_markdown(payload)
    return payload


def write_typed_residue_markdown(payload: Dict[str, object]) -> None:
    path = RESULTS / "phase6_h4_typed_residue_interfaces.md"
    level1 = payload["level1"]
    level2 = payload["level2"]
    direct = payload["matched_direct_width8"]
    decision = payload["decision"]
    best_level2 = "none" if level2["best"] is None else level2["best"]["certificate_lines"][0]
    best_direct = "none" if direct["best"] is None else direct["best"]["certificate_lines"][0]
    lines = [
        "# Phase 6 H4 Typed Residue Interfaces",
        "",
        "## Protocol",
        "",
        f"- Frozen low-height asymmetric family: `{payload['frozen_family']['family_id']}` with `X = {payload['frozen_family']['x_labels']}`.",
        f"- Frozen interface alphabet: `{payload['interface_alphabet']}`.",
        f"- Symmetry quotient: {payload['symmetry_quotient']}.",
        f"- Unchanged extractor: {payload['extractor']['note']}",
        "- Level-1 search space: canonical width-4 interface words of length 3, exact forcing check with the same extractor and no repair.",
        "- Level-2 composition rule: concatenate two forcing width-4 witnesses with one bridge symbol from the same alphabet; seeds and initial solved vertices are copied verbatim into the left and right halves with no new symbols and no repair pass.",
        "",
        "## Results",
        "",
        f"- Level-1 canonical words checked: `{level1['candidate_count']}`.",
        f"- Level-1 forcing words: `{level1['forcing_count']}`.",
        f"- Level-2 compositions checked: `{level2['candidate_count']}`.",
        f"- Level-2 forcing hit rate: `{level2['hit_rate']:.4f}`.",
        f"- Matched direct width-8 hit rate: `{direct['hit_rate']:.4f}` over `{direct['total_trials']}` exact trials.",
        f"- Best composed level-2 certificate: `{best_level2}`.",
        f"- Best matched direct width-8 certificate: `{best_direct}`.",
        "",
        "## Decision",
        "",
        f"- Passed: `{decision['passed']}`.",
        f"- Reason: {decision['reason']}",
        "",
        "## Novelty Position",
        "",
        f"- {payload['novelty_note']}",
        "- This is not bootstrap-percolation folklore in new words because the object under test is an exact verifier-facing certificate family, not an infection threshold or fill time.",
        "- It is not just macrocell folklore in new words because the experiment freezes the interface alphabet first and then asks whether exact legal witnesses compose across levels without any repair or hidden extractor change.",
    ]
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("typed-residue",),
    )
    args = parser.parse_args()
    if args.command == "typed-residue":
        payload = write_typed_residue_results()
        print(json.dumps(payload["decision"], indent=2))


if __name__ == "__main__":
    main()
