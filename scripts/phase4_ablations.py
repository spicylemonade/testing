#!/usr/bin/env python3
"""Run the required ablations on an exact corridor witness."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ca_kakeya_search import CorridorInstance, greedy_seed_search


Vector = Tuple[int, int]
Vertex = Tuple[int, int]


def load_best_instance(path: Path) -> CorridorInstance:
    payload = json.loads(path.read_text())
    best = payload["best"]
    return CorridorInstance(
        width=best["n"] // 2,
        x_labels=tuple(tuple(label) for label in payload["x_labels"]),
        vertical=tuple(best["vertical"]),
        top=tuple(tuple(label) for label in best["top"]),
        bottom=tuple(tuple(label) for label in best["bottom"]),
        seeds=tuple((tuple(vertex), tuple(label)) for vertex, label in best["seeds"]),
        initial_t=tuple(tuple(vertex) for vertex in best["initial_t"]),
    )


def summarize_instance(name: str, instance: CorridorInstance | None) -> Dict[str, object]:
    if instance is None:
        return {
            "name": name,
            "forcing": False,
            "score": None,
            "m": None,
            "r": None,
            "n": None,
            "t": None,
        }
    forcing = instance.is_forcing()
    return {
        "name": name,
        "forcing": forcing,
        "score": None if not forcing else instance.score,
        "m": instance.m,
        "r": instance.r,
        "n": instance.n,
        "t": instance.t,
    }


def isotropic_variants(base: CorridorInstance) -> List[Dict[str, object]]:
    return [
        summarize_instance(
            "isotropic_top_to_bottom",
            CorridorInstance(
                width=base.width,
                x_labels=base.x_labels,
                vertical=base.vertical,
                top=base.top,
                bottom=base.top,
                seeds=base.seeds,
                initial_t=base.initial_t,
            ),
        ),
        summarize_instance(
            "isotropic_bottom_to_top",
            CorridorInstance(
                width=base.width,
                x_labels=base.x_labels,
                vertical=base.vertical,
                top=base.bottom,
                bottom=base.bottom,
                seeds=base.seeds,
                initial_t=base.initial_t,
            ),
        ),
    ]


def boundary_seed_removal(base: CorridorInstance) -> Dict[str, object]:
    seeds = tuple(
        seed for seed in base.seeds if seed[0][1] not in {1, base.width}
    )
    initial_t = tuple(vertex for vertex in base.initial_t if vertex[1] not in {1, base.width})
    inst = CorridorInstance(
        width=base.width,
        x_labels=base.x_labels,
        vertical=base.vertical,
        top=base.top,
        bottom=base.bottom,
        seeds=seeds,
        initial_t=initial_t,
    )
    row = summarize_instance("boundary_seed_removal", inst)
    row["seed_count_after"] = len(seeds)
    row["t_count_after"] = len(initial_t)
    return row


def shuffled_labels(labels: Sequence[Vector], rng: random.Random) -> Dict[Vector, Vector]:
    nonzero = [label for label in labels if label != (0, 0)]
    shuffled = nonzero[:]
    rng.shuffle(shuffled)
    mapping = {(0, 0): (0, 0)}
    mapping.update({old: new for old, new in zip(nonzero, shuffled)})
    return mapping


def random_label_set(base: CorridorInstance, rng: random.Random) -> Tuple[Vector, ...]:
    nonzero_old = [label for label in base.x_labels if label != (0, 0)]
    coord_height = max(max(abs(a), abs(b)) for a, b in nonzero_old)
    pool = [
        (a, b)
        for a in range(-coord_height, coord_height + 1)
        for b in range(-coord_height, coord_height + 1)
        if (a, b) != (0, 0) and a + b != 0
    ]
    rng.shuffle(pool)
    chosen = tuple(pool[: len(nonzero_old)])
    return ((0, 0),) + chosen


def remap_instance(base: CorridorInstance, mapping: Dict[Vector, Vector], x_labels: Tuple[Vector, ...] | None = None) -> CorridorInstance:
    return CorridorInstance(
        width=base.width,
        x_labels=base.x_labels if x_labels is None else x_labels,
        vertical=mapping[base.vertical],
        top=tuple(mapping[label] for label in base.top),
        bottom=tuple(mapping[label] for label in base.bottom),
        seeds=tuple((vertex, mapping[label]) for vertex, label in base.seeds),
        initial_t=base.initial_t,
    )


def randomized_trials(base: CorridorInstance, rng_seed: int) -> Dict[str, object]:
    rng = random.Random(rng_seed)
    vertices = base.vertices
    seed_labels = [label for _, label in base.seeds]
    rows: Dict[str, List[Dict[str, object]]] = {
        "randomize_R": [],
        "randomize_T": [],
        "randomize_X": [],
    }
    for trial in range(4):
        seed_vertices = rng.sample(vertices, len(base.seeds))
        r_inst = CorridorInstance(
            width=base.width,
            x_labels=base.x_labels,
            vertical=base.vertical,
            top=base.top,
            bottom=base.bottom,
            seeds=tuple(zip(seed_vertices, seed_labels)),
            initial_t=base.initial_t,
        )
        rows["randomize_R"].append(summarize_instance(f"randomize_R_trial_{trial}", r_inst))

        t_vertices = tuple(sorted(rng.sample(vertices, len(base.initial_t))))
        t_inst = CorridorInstance(
            width=base.width,
            x_labels=base.x_labels,
            vertical=base.vertical,
            top=base.top,
            bottom=base.bottom,
            seeds=base.seeds,
            initial_t=t_vertices,
        )
        rows["randomize_T"].append(summarize_instance(f"randomize_T_trial_{trial}", t_inst))

        new_x = random_label_set(base, rng)
        old_nonzero = [label for label in base.x_labels if label != (0, 0)]
        new_nonzero = [label for label in new_x if label != (0, 0)]
        mapping = {(0, 0): (0, 0)}
        mapping.update({old: new for old, new in zip(old_nonzero, new_nonzero)})
        x_inst = remap_instance(base, mapping, x_labels=new_x)
        rows["randomize_X"].append(summarize_instance(f"randomize_X_trial_{trial}", x_inst))
    return rows


def periodic(motif: Sequence[Vector], length: int) -> Tuple[Vector, ...]:
    return tuple(motif[i % len(motif)] for i in range(length))


def scale_rows(base: CorridorInstance) -> List[Dict[str, object]]:
    rows = []
    for width in (6, 8):
        inst = greedy_seed_search(
            width=width,
            x_labels=base.x_labels,
            vertical=base.vertical,
            top=periodic(base.top, width - 1),
            bottom=periodic(base.bottom, width - 1),
            seed_budget=6,
            initial_t_budget=len(base.initial_t),
            boundary_band=2,
        )
        rows.append(summarize_instance(f"freeze_X_scale_width_{width}", inst))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rng-seed", type=int, default=1901)
    args = parser.parse_args()

    base = load_best_instance(args.base)
    payload = {
        "base": summarize_instance("base_exact", base),
        "exact_elimination_replacement": "all rows use the exact verifier; no surrogate score is reported",
        "isotropic": isotropic_variants(base),
        "boundary_seed_removal": boundary_seed_removal(base),
        "randomized": randomized_trials(base, args.rng_seed),
        "freeze_X_scale_n": scale_rows(base),
        "stage_order_perturbation": {
            "status": "not_applicable",
            "reason": (
                "No grammar-mediated H1 family survived. The remaining objects are direct corridor "
                "controls, so there is no substitution-stage order to swap without leaving the exact family."
            ),
        },
    }
    text = json.dumps(payload, indent=2)
    args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
