#!/usr/bin/env python3
"""Exact search utilities for width-2 arithmetic Kakeya corridor certificates.

The search space here is intentionally narrow:

- constructible graphs with `d = [2, W]`
- one constant vertical label across columns
- arbitrary top and bottom horizontal labels
- arbitrary singleton seeds and optional initial solved vertices

This is enough to evaluate the frozen H1 corridor family and matched controls.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_decomp


Vector = Tuple[int, int]
Vertex = Tuple[int, int]


def same_sum_labels(sum_value: int, count: int) -> List[Vector]:
    return [(i, sum_value - i) for i in range(count)]


def format_pair(v: Vector) -> str:
    return f"({v[0]},{v[1]})"


def format_vertex(v: Vertex) -> str:
    return f"[{v[0]},{v[1]}]"


def index_vertices(width: int) -> List[Vertex]:
    return [(r, c) for r in range(1, 3) for c in range(1, width + 1)]


def vertex_index_map(width: int) -> Dict[Vertex, int]:
    return {vertex: idx for idx, vertex in enumerate(index_vertices(width))}


def zero_vector(dim: int) -> List[int]:
    return [0] * dim


def singleton_generator(width: int, vertex: Vertex, label: Vector) -> List[int]:
    n = 2 * width
    out = zero_vector(2 * n // 1)
    index = vertex_index_map(width)[vertex]
    out[2 * index] = label[0]
    out[2 * index + 1] = label[1]
    return out


def edge_generator(width: int, u: Vertex, v: Vertex, label: Vector) -> List[int]:
    n = 2 * width
    out = zero_vector(2 * n // 1)
    u_index = vertex_index_map(width)[u]
    v_index = vertex_index_map(width)[v]
    out[2 * u_index] = label[0]
    out[2 * u_index + 1] = label[1]
    out[2 * v_index] = -label[0]
    out[2 * v_index + 1] = -label[1]
    return out


def project_vector(width: int, vector: Sequence[int], unsolved: Sequence[Vertex]) -> List[int]:
    idx = vertex_index_map(width)
    out: List[int] = []
    for vertex in unsolved:
        base = 2 * idx[vertex]
        out.extend([vector[base], vector[base + 1]])
    return out


def target_vector(unsolved: Sequence[Vertex], target: Vertex, weight: int = 1) -> List[int]:
    out = [0] * (2 * len(unsolved))
    pos = unsolved.index(target)
    out[2 * pos] = weight
    out[2 * pos + 1] = -weight
    return out


@dataclass(frozen=True)
class CorridorInstance:
    width: int
    x_labels: Tuple[Vector, ...]
    vertical: Vector
    top: Tuple[Vector, ...]
    bottom: Tuple[Vector, ...]
    seeds: Tuple[Tuple[Vertex, Vector], ...]
    initial_t: Tuple[Vertex, ...]

    @property
    def vertices(self) -> List[Vertex]:
        return index_vertices(self.width)

    @property
    def n(self) -> int:
        return 2 * self.width

    @property
    def m(self) -> int:
        count = self.width if self.vertical != (0, 0) else 0
        count += sum(1 for label in self.top if label != (0, 0))
        count += sum(1 for label in self.bottom if label != (0, 0))
        return count

    @property
    def r(self) -> int:
        return len(self.seeds)

    @property
    def t(self) -> int:
        return len(self.initial_t)

    @property
    def score(self) -> float:
        return (self.m + self.r) / (self.n - self.t)

    def generators(self) -> List[List[int]]:
        out: List[List[int]] = []
        for column in range(1, self.width + 1):
            if self.vertical != (0, 0):
                out.append(edge_generator(self.width, (1, column), (2, column), self.vertical))
        for column, label in enumerate(self.top, start=1):
            if label != (0, 0):
                out.append(edge_generator(self.width, (1, column), (1, column + 1), label))
        for column, label in enumerate(self.bottom, start=1):
            if label != (0, 0):
                out.append(edge_generator(self.width, (2, column), (2, column + 1), label))
        for vertex, label in self.seeds:
            out.append(singleton_generator(self.width, vertex, label))
        return out

    def forcing_order(self) -> Optional[List[Vertex]]:
        solved = list(self.initial_t)
        order = list(self.initial_t)
        generators = self.generators()
        remaining = [vertex for vertex in self.vertices if vertex not in solved]
        while remaining:
            progress = False
            for vertex in list(remaining):
                unsolved = [v for v in self.vertices if v not in solved]
                if lattice_membership(
                    [project_vector(self.width, g, unsolved) for g in generators],
                    target_vector(unsolved, vertex),
                ):
                    solved.append(vertex)
                    order.append(vertex)
                    remaining.remove(vertex)
                    progress = True
                    break
            if not progress:
                return None
        return order

    def is_forcing(self) -> bool:
        return self.forcing_order() is not None

    def to_certificate_lines(self) -> List[str]:
        numerator = self.m + self.r
        denominator = self.n - self.t
        score_line = (
            f"{numerator}/{denominator} m={self.m} r={self.r} n={self.n} t={self.t}"
        )
        x_line = "[" + ", ".join(format_pair(v) for v in self.x_labels) + "]"
        d_line = f"[2,{self.width}]"
        f1 = "{1:" + format_pair(self.vertical) + "}" if self.vertical != (0, 0) else "{}"
        top_entries = [
            f"(1,{column}):{format_pair(label)}"
            for column, label in enumerate(self.top, start=1)
            if label != (0, 0)
        ]
        bottom_entries = [
            f"(2,{column}):{format_pair(label)}"
            for column, label in enumerate(self.bottom, start=1)
            if label != (0, 0)
        ]
        f2 = "{" + ", ".join(top_entries + bottom_entries) + "}"
        functions_line = f"[{f1}, {f2}]"
        t_line = "[" + ", ".join(format_vertex(v) for v in self.initial_t) + "]"
        r_items = []
        for vertex, label in self.seeds:
            r_items.append("{" + f"{format_vertex(vertex)}:{format_pair(label)}" + "}")
        r_line = "[" + ", ".join(r_items) + "]"
        return [score_line, x_line, d_line, functions_line, t_line, r_line]


def lattice_membership(generators: Sequence[Sequence[int]], target: Sequence[int]) -> bool:
    if not generators:
        return all(v == 0 for v in target)
    matrix = Matrix(list(zip(*generators)))
    target_matrix = Matrix(target)
    diagonal, left, _right = smith_normal_decomp(matrix, domain=ZZ)
    transformed = left * target_matrix
    rows, cols = diagonal.shape
    rank = min(rows, cols)
    for i in range(rank):
        d = diagonal[i, i]
        value = transformed[i, 0]
        if d == 0:
            if value != 0:
                return False
        else:
            if value % d != 0:
                return False
    for i in range(rank, rows):
        if transformed[i, 0] != 0:
            return False
    return True


def all_label_patterns(labels: Sequence[Vector], width: int) -> Iterable[Tuple[Tuple[Vector, ...], Tuple[Vector, ...], Vector]]:
    for vertical in labels:
        for top in itertools.product(labels, repeat=width - 1):
            for bottom in itertools.product(labels, repeat=width - 1):
                yield tuple(top), tuple(bottom), vertical


def greedy_seed_search(
    width: int,
    x_labels: Sequence[Vector],
    vertical: Vector,
    top: Sequence[Vector],
    bottom: Sequence[Vector],
    seed_budget: int,
    initial_t_budget: int = 0,
) -> Optional[CorridorInstance]:
    vertices = index_vertices(width)
    seed_candidates = [(vertex, label) for vertex in vertices for label in x_labels if label != (0, 0)]
    best: Optional[CorridorInstance] = None

    for initial_t in itertools.combinations(vertices, initial_t_budget):
        chosen: List[Tuple[Vertex, Vector]] = []
        current = CorridorInstance(
            width=width,
            x_labels=tuple(x_labels),
            vertical=vertical,
            top=tuple(top),
            bottom=tuple(bottom),
            seeds=tuple(chosen),
            initial_t=tuple(initial_t),
        )
        if current.is_forcing():
            return current
        for _ in range(seed_budget):
            best_local = None
            best_closure = -1
            for candidate in seed_candidates:
                if candidate in chosen:
                    continue
                trial = CorridorInstance(
                    width=width,
                    x_labels=tuple(x_labels),
                    vertical=vertical,
                    top=tuple(top),
                    bottom=tuple(bottom),
                    seeds=tuple(chosen + [candidate]),
                    initial_t=tuple(initial_t),
                )
                order = trial.forcing_order()
                closure = len(order) if order else len(initial_t)
                if order:
                    if best is None or trial.score < best.score:
                        best = trial
                    return trial
                if closure > best_closure:
                    best_closure = closure
                    best_local = candidate
            if best_local is None:
                break
            chosen.append(best_local)
            current = CorridorInstance(
                width=width,
                x_labels=tuple(x_labels),
                vertical=vertical,
                top=tuple(top),
                bottom=tuple(bottom),
                seeds=tuple(chosen),
                initial_t=tuple(initial_t),
            )
            if current.is_forcing():
                if best is None or current.score < best.score:
                    best = current
                return current
    return best


def same_sum_palette(sum_value: int, nonzero_count: int) -> List[Vector]:
    return [(0, 0)] + [(i, sum_value - i) for i in range(nonzero_count)]


def random_search(
    width_min: int,
    width_max: int,
    trials: int,
    nonzero_count: int,
    seed_budget: int,
    initial_t_budget: int,
    rng_seed: int,
    output_path: Optional[Path],
) -> Dict[str, object]:
    rng = random.Random(rng_seed)
    x_labels = same_sum_palette(1, nonzero_count)
    nonzero_labels = [label for label in x_labels if label != (0, 0)]
    best: Optional[CorridorInstance] = None
    history: List[Dict[str, object]] = []
    for trial_index in range(1, trials + 1):
        width = rng.randint(width_min, width_max)
        vertical = rng.choice(nonzero_labels)
        top = tuple(rng.choice(nonzero_labels) for _ in range(width - 1))
        bottom = tuple(rng.choice(nonzero_labels) for _ in range(width - 1))
        instance = greedy_seed_search(
            width=width,
            x_labels=x_labels,
            vertical=vertical,
            top=top,
            bottom=bottom,
            seed_budget=seed_budget,
            initial_t_budget=initial_t_budget,
        )
        if instance and instance.is_forcing():
            if best is None or instance.score < best.score:
                best = instance
        history.append(
            {
                "trial": trial_index,
                "width": width,
                "vertical": vertical,
                "top": list(top),
                "bottom": list(bottom),
                "best_score_so_far": best.score if best else None,
            }
        )
        if best and best.score <= 1.675:
            break
    payload: Dict[str, object] = {
        "rng_seed": rng_seed,
        "width_min": width_min,
        "width_max": width_max,
        "trials": len(history),
        "x_labels": x_labels,
        "history": history[-100:],
        "best": None,
    }
    if best:
        payload["best"] = {
            "score": best.score,
            "m": best.m,
            "r": best.r,
            "n": best.n,
            "t": best.t,
            "vertical": best.vertical,
            "top": list(best.top),
            "bottom": list(best.bottom),
            "seeds": [[list(vertex), list(label)] for vertex, label in best.seeds],
            "initial_t": [list(vertex) for vertex in best.initial_t],
            "forcing_order": [list(vertex) for vertex in best.forcing_order() or []],
            "certificate_lines": best.to_certificate_lines(),
        }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2))
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    random_parser = subparsers.add_parser("random-search")
    random_parser.add_argument("--width-min", type=int, default=8)
    random_parser.add_argument("--width-max", type=int, default=16)
    random_parser.add_argument("--trials", type=int, default=200)
    random_parser.add_argument("--nonzero-count", type=int, default=3)
    random_parser.add_argument("--seed-budget", type=int, default=8)
    random_parser.add_argument("--initial-t-budget", type=int, default=0)
    random_parser.add_argument("--rng-seed", type=int, default=0)
    random_parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "random-search":
        payload = random_search(
            width_min=args.width_min,
            width_max=args.width_max,
            trials=args.trials,
            nonzero_count=args.nonzero_count,
            seed_budget=args.seed_budget,
            initial_t_budget=args.initial_t_budget,
            rng_seed=args.rng_seed,
            output_path=args.output,
        )
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
