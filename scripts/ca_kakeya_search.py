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

from sympy import Matrix
try:
    import numpy as np
except Exception:  # pragma: no cover - optional acceleration only
    np = None


Vector = Tuple[int, int]
Vertex = Tuple[int, int]
FAST_PRIMES = (1_000_003, 1_000_033)


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


def nullspace_mod_p(rows: Sequence[Sequence[int]], cols: int, modulus: int) -> List[List[int]]:
    if not rows:
        return [[1 if i == j else 0 for i in range(cols)] for j in range(cols)]
    mat = [[entry % modulus for entry in row] for row in rows]
    row_count = len(mat)
    pivot_cols: List[int] = []
    pivot_row = 0
    for col in range(cols):
        pivot = None
        for row in range(pivot_row, row_count):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[pivot_row], mat[pivot] = mat[pivot], mat[pivot_row]
        inv = pow(mat[pivot_row][col], -1, modulus)
        mat[pivot_row] = [(value * inv) % modulus for value in mat[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or mat[row][col] % modulus == 0:
                continue
            factor = mat[row][col] % modulus
            mat[row] = [
                (mat[row][j] - factor * mat[pivot_row][j]) % modulus
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free_cols = [col for col in range(cols) if col not in pivot_cols]
    basis: List[List[int]] = []
    for free_col in free_cols:
        vector = [0] * cols
        vector[free_col] = 1
        for row_index, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-mat[row_index][free_col]) % modulus
        basis.append(vector)
    return basis


@dataclass
class SpanOracle:
    left_nullspace: Tuple[Matrix, ...]
    has_generators: bool

    @classmethod
    def from_generators(cls, generators: Sequence[Sequence[int]]) -> "SpanOracle":
        if not generators:
            return cls(left_nullspace=tuple(), has_generators=False)
        matrix = Matrix(list(zip(*generators)))
        return cls(left_nullspace=tuple(matrix.transpose().nullspace()), has_generators=True)

    def solvable_vertices(self, unsolved: Sequence[Vertex]) -> List[Vertex]:
        if not self.has_generators:
            return []
        if not self.left_nullspace:
            return list(unsolved)
        out: List[Vertex] = []
        for pos, vertex in enumerate(unsolved):
            if all(vector[2 * pos, 0] == vector[2 * pos + 1, 0] for vector in self.left_nullspace):
                out.append(vertex)
        return out


@dataclass
class ModSpanOracle:
    left_nullspace: Tuple[Tuple[int, ...], ...]
    has_generators: bool
    modulus: int

    @classmethod
    def from_generators(cls, generators: Sequence[Sequence[int]], rows: int, modulus: int) -> "ModSpanOracle":
        if not generators:
            return cls(left_nullspace=tuple(), has_generators=False, modulus=modulus)
        basis = nullspace_mod_p(generators, rows, modulus)
        return cls(
            left_nullspace=tuple(tuple(vector) for vector in basis),
            has_generators=True,
            modulus=modulus,
        )

    def solvable_vertices(self, unsolved: Sequence[Vertex]) -> List[Vertex]:
        if not self.has_generators:
            return []
        if not self.left_nullspace:
            return list(unsolved)
        out: List[Vertex] = []
        for pos, vertex in enumerate(unsolved):
            if all(
                (vector[2 * pos] - vector[2 * pos + 1]) % self.modulus == 0
                for vector in self.left_nullspace
            ):
                out.append(vertex)
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
        generators = self.generators()
        solved = set(self.initial_t)
        order = list(self.initial_t)
        oracle_cache: Dict[Tuple[Vertex, ...], SpanOracle] = {}

        def oracle_for(unsolved: Tuple[Vertex, ...]) -> SpanOracle:
            if unsolved not in oracle_cache:
                projected = [project_vector(self.width, g, unsolved) for g in generators]
                oracle_cache[unsolved] = SpanOracle.from_generators(projected)
            return oracle_cache[unsolved]

        while len(solved) < len(self.vertices):
            unsolved = tuple(vertex for vertex in self.vertices if vertex not in solved)
            oracle = oracle_for(unsolved)
            candidates = oracle.solvable_vertices(unsolved)
            if not candidates:
                return None
            candidates.sort(key=lambda vertex: (vertex[1], vertex[0]))
            chosen = candidates[0]
            solved.add(chosen)
            order.append(chosen)
        return order

    def forcing_order_fast(self) -> List[Vertex]:
        generators = self.generators()
        solved = set(self.initial_t)
        order = list(self.initial_t)
        oracle_cache: Dict[Tuple[Vertex, ...], object] = {}

        def numpy_oracle_for(unsolved: Tuple[Vertex, ...]):
            if unsolved not in oracle_cache:
                projected = [project_vector(self.width, g, unsolved) for g in generators]
                if projected:
                    matrix = np.array(projected, dtype=float).T
                else:
                    matrix = np.zeros((2 * len(unsolved), 0), dtype=float)
                oracle_cache[unsolved] = (matrix, int(np.linalg.matrix_rank(matrix)))
            return oracle_cache[unsolved]

        def oracle_for(unsolved: Tuple[Vertex, ...], modulus: int) -> ModSpanOracle:
            key = (unsolved, modulus)
            if key not in oracle_cache:
                projected = [project_vector(self.width, g, unsolved) for g in generators]
                oracle_cache[key] = ModSpanOracle.from_generators(
                    projected,
                    rows=2 * len(unsolved),
                    modulus=modulus,
                )
            return oracle_cache[key]

        while len(solved) < len(self.vertices):
            unsolved = tuple(vertex for vertex in self.vertices if vertex not in solved)
            if np is not None:
                matrix, rank = numpy_oracle_for(unsolved)
                candidates = []
                for pos, vertex in enumerate(unsolved):
                    target = np.zeros((2 * len(unsolved), 1), dtype=float)
                    target[2 * pos, 0] = 1.0
                    target[2 * pos + 1, 0] = -1.0
                    augmented = np.concatenate((matrix, target), axis=1)
                    if int(np.linalg.matrix_rank(augmented)) == rank:
                        candidates.append(vertex)
                if not candidates:
                    return order
            else:
                candidates = set(unsolved)
                for modulus in FAST_PRIMES:
                    candidates &= set(oracle_for(unsolved, modulus).solvable_vertices(unsolved))
                    if not candidates:
                        return order
                candidates = sorted(candidates, key=lambda vertex: (vertex[1], vertex[0]))
            chosen = sorted(candidates, key=lambda vertex: (vertex[1], vertex[0]))[0]
            solved.add(chosen)
            order.append(chosen)
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
    oracle = SpanOracle.from_generators(generators)
    unsolved = tuple((1, i + 1) for i in range(len(target) // 2))
    target_index = next(
        idx for idx in range(len(target) // 2) if target[2 * idx] != 0 or target[2 * idx + 1] != 0
    )
    return unsolved[target_index] in oracle.solvable_vertices(unsolved)


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
    boundary_band: int = 0,
) -> Optional[CorridorInstance]:
    vertices = index_vertices(width)
    if boundary_band > 0:
        candidate_vertices = [
            vertex
            for vertex in vertices
            if vertex[1] <= boundary_band or vertex[1] > width - boundary_band
        ]
    else:
        candidate_vertices = vertices
    seed_candidates = [
        (vertex, label)
        for vertex in candidate_vertices
        for label in x_labels
        if label != (0, 0)
    ]
    best: Optional[CorridorInstance] = None

    for initial_t in itertools.combinations(candidate_vertices, initial_t_budget):
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
                approx_order = trial.forcing_order_fast()
                closure = len(approx_order)
                if closure == trial.n:
                    order = trial.forcing_order()
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
            if len(current.forcing_order_fast()) == current.n and current.is_forcing():
                if best is None or current.score < best.score:
                    best = current
                return current
    return best


def same_sum_palette(sum_value: int, nonzero_count: int) -> List[Vector]:
    return [(0, 0)] + [(i, sum_value - i) for i in range(nonzero_count)]


def frozen_h1_obstruction(sum_value: int, nonzero_count: int) -> Dict[str, object]:
    """Return the exact one-seed obstruction for the frozen H1 corridor pilot.

    The frozen H1 template list in ``results/phase3_h1_program.md`` has exactly
    one seeded boundary state (either ``L_a`` or ``L_b``), no seeded middle or
    right states, and no initial solved vertices. Edge generators contribute
    zero total label over all vertices, so any singleton relation produced from
    one seed has total label in ``Z * x`` for the chosen seed label ``x``.
    Operation 2 would require a singleton anti-diagonal ``(a,-a)``, whose total
    coordinate sum is zero; this is impossible when ``x_1 + x_2 = sum_value != 0``.
    """

    x_labels = same_sum_palette(sum_value, nonzero_count)
    nonzero = [label for label in x_labels if label != (0, 0)]
    if not nonzero:
        raise ValueError("frozen H1 obstruction requires at least one nonzero label")
    sample_seed = nonzero[0]
    return {
        "route": "H1_macrocell_substitution",
        "frozen_height": 2,
        "template_seed_structure": {
            "seeded_templates": ["L_a", "L_b"],
            "unseeded_templates": ["M_a", "M_b", "M_g", "M_ab", "R_a", "R_b"],
            "initial_t_templates": [],
        },
        "level_invariant": {
            "seed_count": 1,
            "initial_t_count": 0,
            "seed_label": list(sample_seed),
            "seed_label_coordinate_sum": sample_seed[0] + sample_seed[1],
            "edge_generator_total_label": [0, 0],
            "required_operation_2_total_label_form": [1, -1],
            "required_operation_2_coordinate_sum": 0,
        },
        "conclusion": (
            "Every extracted frozen-H1 level has exactly one singleton seed and no "
            "initial solved vertices, so no nonzero anti-diagonal singleton can be "
            "generated. The exact verifier therefore fails at every level before any "
            "score comparison is meaningful."
        ),
    }


def random_search(
    width_min: int,
    width_max: int,
    trials: int,
    nonzero_count: int,
    seed_budget: int,
    initial_t_budget: int,
    boundary_band: int,
    allow_zero_horizontal: bool,
    rng_seed: int,
    output_path: Optional[Path],
) -> Dict[str, object]:
    rng = random.Random(rng_seed)
    x_labels = same_sum_palette(1, nonzero_count)
    nonzero_labels = [label for label in x_labels if label != (0, 0)]
    horizontal_labels = list(x_labels) if allow_zero_horizontal else nonzero_labels
    best: Optional[CorridorInstance] = None
    history: List[Dict[str, object]] = []
    for trial_index in range(1, trials + 1):
        width = rng.randint(width_min, width_max)
        vertical = rng.choice(nonzero_labels)
        top = tuple(rng.choice(horizontal_labels) for _ in range(width - 1))
        bottom = tuple(rng.choice(horizontal_labels) for _ in range(width - 1))
        instance = greedy_seed_search(
            width=width,
            x_labels=x_labels,
            vertical=vertical,
            top=top,
            bottom=bottom,
            seed_budget=seed_budget,
            initial_t_budget=initial_t_budget,
            boundary_band=boundary_band,
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
        "boundary_band": boundary_band,
        "allow_zero_horizontal": allow_zero_horizontal,
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
    random_parser.add_argument("--boundary-band", type=int, default=0)
    random_parser.add_argument("--allow-zero-horizontal", action="store_true")
    random_parser.add_argument("--rng-seed", type=int, default=0)
    random_parser.add_argument("--output", type=Path, default=None)

    h1_obstruction_parser = subparsers.add_parser("h1-obstruction")
    h1_obstruction_parser.add_argument("--sum-value", type=int, default=1)
    h1_obstruction_parser.add_argument("--nonzero-count", type=int, default=4)
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
            boundary_band=args.boundary_band,
            allow_zero_horizontal=args.allow_zero_horizontal,
            rng_seed=args.rng_seed,
            output_path=args.output,
        )
        print(json.dumps(payload, indent=2))
    elif args.command == "h1-obstruction":
        payload = frozen_h1_obstruction(
            sum_value=args.sum_value,
            nonzero_count=args.nonzero_count,
        )
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
