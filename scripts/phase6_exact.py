#!/usr/bin/env python3
"""Exact grid-based utilities for Phase 6 arithmetic Kakeya experiments.

This module extends the width-2 corridor search from ``scripts/ca_kakeya_search``
to low-height ``H x W`` product geometries while keeping the same exact forcing
semantics used by the verifier-facing certificates.
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import numpy as np
except Exception:  # pragma: no cover - optional acceleration only
    np = None

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ca_kakeya_search import FAST_PRIMES, ModSpanOracle, SpanOracle


Vector = Tuple[int, int]
Vertex = Tuple[int, int]


def format_pair(v: Vector) -> str:
    return f"({v[0]},{v[1]})"


def format_vertex(v: Vertex) -> str:
    return f"[{v[0]},{v[1]}]"


def grid_vertices(height: int, width: int) -> List[Vertex]:
    return [(row, col) for row in range(1, height + 1) for col in range(1, width + 1)]


def vertex_index_map(height: int, width: int) -> Dict[Vertex, int]:
    return {vertex: idx for idx, vertex in enumerate(grid_vertices(height, width))}


def zero_vector(length: int) -> List[int]:
    return [0] * length


def singleton_generator(height: int, width: int, vertex: Vertex, label: Vector) -> List[int]:
    n = height * width
    out = zero_vector(2 * n)
    index = vertex_index_map(height, width)[vertex]
    out[2 * index] = label[0]
    out[2 * index + 1] = label[1]
    return out


def edge_generator(
    height: int,
    width: int,
    u: Vertex,
    v: Vertex,
    label: Vector,
) -> List[int]:
    n = height * width
    out = zero_vector(2 * n)
    index = vertex_index_map(height, width)
    u_index = index[u]
    v_index = index[v]
    out[2 * u_index] = label[0]
    out[2 * u_index + 1] = label[1]
    out[2 * v_index] = -label[0]
    out[2 * v_index + 1] = -label[1]
    return out


def project_vector(
    height: int,
    width: int,
    vector: Sequence[int],
    unsolved: Sequence[Vertex],
) -> List[int]:
    index = vertex_index_map(height, width)
    out: List[int] = []
    for vertex in unsolved:
        base = 2 * index[vertex]
        out.extend([vector[base], vector[base + 1]])
    return out


def coordinate_height(x_labels: Sequence[Vector]) -> int:
    return max((max(abs(a), abs(b)) for a, b in x_labels if (a, b) != (0, 0)), default=0)


def serialize_horizontal(horizontal: Sequence[Sequence[Vector]]) -> List[List[List[int]]]:
    return [[list(label) for label in row] for row in horizontal]


@dataclass(frozen=True)
class GridInstance:
    height: int
    width: int
    x_labels: Tuple[Vector, ...]
    vertical: Tuple[Vector, ...]
    horizontal: Tuple[Tuple[Vector, ...], ...]
    seeds: Tuple[Tuple[Vertex, Vector], ...]
    initial_t: Tuple[Vertex, ...]

    @property
    def vertices(self) -> List[Vertex]:
        return grid_vertices(self.height, self.width)

    @property
    def n(self) -> int:
        return self.height * self.width

    @property
    def m(self) -> int:
        count = self.width * sum(1 for label in self.vertical if label != (0, 0))
        count += sum(
            1
            for row in self.horizontal
            for label in row
            if label != (0, 0)
        )
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

    @property
    def distinct_nonzero_labels(self) -> Tuple[Vector, ...]:
        used = {
            label
            for label in self.vertical
            if label != (0, 0)
        }
        used |= {
            label
            for row in self.horizontal
            for label in row
            if label != (0, 0)
        }
        used |= {
            label
            for _, label in self.seeds
            if label != (0, 0)
        }
        return tuple(sorted(used))

    def grammar_length(self) -> int:
        return (
            sum(1 for label in self.vertical if label != (0, 0))
            + sum(1 for row in self.horizontal for label in row if label != (0, 0))
            + len(self.seeds)
            + len(self.initial_t)
        )

    def generators(self) -> List[List[int]]:
        out: List[List[int]] = []
        for col in range(1, self.width + 1):
            for row, label in enumerate(self.vertical, start=1):
                if label != (0, 0):
                    out.append(
                        edge_generator(
                            self.height,
                            self.width,
                            (row, col),
                            (row + 1, col),
                            label,
                        )
                    )
        for row in range(1, self.height + 1):
            for col, label in enumerate(self.horizontal[row - 1], start=1):
                if label != (0, 0):
                    out.append(
                        edge_generator(
                            self.height,
                            self.width,
                            (row, col),
                            (row, col + 1),
                            label,
                        )
                    )
        for vertex, label in self.seeds:
            out.append(singleton_generator(self.height, self.width, vertex, label))
        return out

    def forcing_order(self) -> Optional[List[Vertex]]:
        generators = self.generators()
        solved = set(self.initial_t)
        order = list(self.initial_t)
        oracle_cache: Dict[Tuple[Vertex, ...], SpanOracle] = {}

        def oracle_for(unsolved: Tuple[Vertex, ...]) -> SpanOracle:
            if unsolved not in oracle_cache:
                projected = [
                    project_vector(self.height, self.width, generator, unsolved)
                    for generator in generators
                ]
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
        oracle_cache: Dict[Tuple[object, ...], object] = {}

        def numpy_oracle_for(unsolved: Tuple[Vertex, ...]):
            if unsolved not in oracle_cache:
                projected = [
                    project_vector(self.height, self.width, generator, unsolved)
                    for generator in generators
                ]
                if projected:
                    matrix = np.array(projected, dtype=float).T
                else:
                    matrix = np.zeros((2 * len(unsolved), 0), dtype=float)
                oracle_cache[unsolved] = (matrix, int(np.linalg.matrix_rank(matrix)))
            return oracle_cache[unsolved]

        def oracle_for(unsolved: Tuple[Vertex, ...], modulus: int) -> ModSpanOracle:
            key = (unsolved, modulus)
            if key not in oracle_cache:
                projected = [
                    project_vector(self.height, self.width, generator, unsolved)
                    for generator in generators
                ]
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

    def closure_size_fast(self) -> int:
        return len(self.forcing_order_fast())

    def is_forcing(self) -> bool:
        return self.forcing_order() is not None

    def to_certificate_lines(self) -> List[str]:
        numerator = self.m + self.r
        denominator = self.n - self.t
        score_line = f"{numerator}/{denominator} m={self.m} r={self.r} n={self.n} t={self.t}"
        x_line = "[" + ", ".join(format_pair(v) for v in self.x_labels) + "]"
        d_line = f"[{self.height},{self.width}]"
        vertical_entries = [
            f"{row}:{format_pair(label)}"
            for row, label in enumerate(self.vertical, start=1)
            if label != (0, 0)
        ]
        horizontal_entries = [
            f"({row},{col}):{format_pair(label)}"
            for row, row_labels in enumerate(self.horizontal, start=1)
            for col, label in enumerate(row_labels, start=1)
            if label != (0, 0)
        ]
        functions_line = (
            "[" + "{" + ", ".join(vertical_entries) + "}, "
            + "{" + ", ".join(horizontal_entries) + "}" + "]"
        )
        t_line = "[" + ", ".join(format_vertex(vertex) for vertex in self.initial_t) + "]"
        r_entries = [
            "{" + f"{format_vertex(vertex)}:{format_pair(label)}" + "}"
            for vertex, label in self.seeds
        ]
        r_line = "[" + ", ".join(r_entries) + "]"
        return [score_line, x_line, d_line, functions_line, t_line, r_line]


def boundary_vertices(height: int, width: int, boundary_band: int) -> List[Vertex]:
    vertices = grid_vertices(height, width)
    if boundary_band <= 0:
        return vertices
    return [
        vertex
        for vertex in vertices
        if vertex[1] <= boundary_band or vertex[1] > width - boundary_band
    ]


def greedy_seed_search_grid(
    height: int,
    width: int,
    x_labels: Sequence[Vector],
    vertical: Sequence[Vector],
    horizontal: Sequence[Sequence[Vector]],
    seed_budget: int,
    initial_t_budget: int = 0,
    boundary_band: int = 0,
) -> Optional[GridInstance]:
    candidate_vertices = boundary_vertices(height, width, boundary_band)
    seed_candidates = [
        (vertex, label)
        for vertex in candidate_vertices
        for label in x_labels
        if label != (0, 0)
    ]
    best: Optional[GridInstance] = None

    for initial_t in itertools.combinations(candidate_vertices, initial_t_budget):
        chosen: List[Tuple[Vertex, Vector]] = []
        current = GridInstance(
            height=height,
            width=width,
            x_labels=tuple(x_labels),
            vertical=tuple(vertical),
            horizontal=tuple(tuple(row) for row in horizontal),
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
                trial = GridInstance(
                    height=height,
                    width=width,
                    x_labels=tuple(x_labels),
                    vertical=tuple(vertical),
                    horizontal=tuple(tuple(row) for row in horizontal),
                    seeds=tuple(chosen + [candidate]),
                    initial_t=tuple(initial_t),
                )
                closure = trial.closure_size_fast()
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
            current = GridInstance(
                height=height,
                width=width,
                x_labels=tuple(x_labels),
                vertical=tuple(vertical),
                horizontal=tuple(tuple(row) for row in horizontal),
                seeds=tuple(chosen),
                initial_t=tuple(initial_t),
            )
            if current.closure_size_fast() == current.n and current.is_forcing():
                if best is None or current.score < best.score:
                    best = current
                return current
    return best


def build_payload(
    instance: Optional[GridInstance],
    *,
    candidate_count: int,
    x_labels: Sequence[Vector],
    height: int,
    width: int,
    seed_budget: int,
    initial_t_budget: int,
    boundary_band: int,
    grammar_length: Optional[int] = None,
    active_state_count: Optional[int] = None,
    extractor_complexity: int = 1,
) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "height": height,
        "width": width,
        "x_labels": [list(label) for label in x_labels],
        "candidate_count": candidate_count,
        "seed_budget": seed_budget,
        "initial_t_budget": initial_t_budget,
        "boundary_band": boundary_band,
        "coordinate_height": coordinate_height(x_labels),
        "best": None,
    }
    if instance is None or not instance.is_forcing():
        return payload
    payload["best"] = {
        "score": instance.score,
        "m": instance.m,
        "r": instance.r,
        "n": instance.n,
        "t": instance.t,
        "vertical": [list(label) for label in instance.vertical],
        "horizontal": serialize_horizontal(instance.horizontal),
        "seeds": [[list(vertex), list(label)] for vertex, label in instance.seeds],
        "initial_t": [list(vertex) for vertex in instance.initial_t],
        "forcing_order": [list(vertex) for vertex in instance.forcing_order() or []],
        "certificate_lines": instance.to_certificate_lines(),
        "grammar_length": grammar_length if grammar_length is not None else instance.grammar_length(),
        "active_state_count": (
            active_state_count
            if active_state_count is not None
            else len(instance.distinct_nonzero_labels)
        ),
        "extractor_complexity": extractor_complexity,
    }
    return payload


def random_search_grid(
    *,
    height: int,
    width: int,
    x_labels: Sequence[Vector],
    trials: int,
    seed_budget: int,
    initial_t_budget: int,
    boundary_band: int,
    allow_zero_horizontal: bool,
    rng_seed: int,
) -> Dict[str, object]:
    rng = random.Random(rng_seed)
    nonzero_labels = [label for label in x_labels if label != (0, 0)]
    horizontal_labels = list(x_labels) if allow_zero_horizontal else nonzero_labels
    best: Optional[GridInstance] = None
    history: List[Dict[str, object]] = []
    for trial_index in range(1, trials + 1):
        vertical = tuple(rng.choice(nonzero_labels) for _ in range(height - 1))
        horizontal = tuple(
            tuple(rng.choice(horizontal_labels) for _ in range(width - 1))
            for _ in range(height)
        )
        instance = greedy_seed_search_grid(
            height=height,
            width=width,
            x_labels=x_labels,
            vertical=vertical,
            horizontal=horizontal,
            seed_budget=seed_budget,
            initial_t_budget=initial_t_budget,
            boundary_band=boundary_band,
        )
        forcing = instance is not None and instance.is_forcing()
        if forcing and (best is None or instance.score < best.score):
            best = instance
        history.append(
            {
                "trial": trial_index,
                "forcing": forcing,
                "score": None if not forcing else instance.score,
                "closure_size": 0 if instance is None else instance.closure_size_fast(),
                "best_score_so_far": None if best is None else best.score,
            }
        )
    payload = build_payload(
        best,
        candidate_count=trials,
        x_labels=x_labels,
        height=height,
        width=width,
        seed_budget=seed_budget,
        initial_t_budget=initial_t_budget,
        boundary_band=boundary_band,
    )
    payload["rng_seed"] = rng_seed
    payload["trials"] = trials
    payload["history"] = history
    return payload


def dump_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False))

