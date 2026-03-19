#!/usr/bin/env python3
"""Exact witness tooling for the arithmetic-Kakeya CA search lane.

This module serves three roles:

1. Parse and verify six-line witnesses `(X, G, R, T)`.
2. Emit a canonical synchronous forcing trace normal form.
3. Search bounded product-grid geometries with Z3 over a reduced but exact
   proof-state cellular-automaton semantics.

The key reduction is that only the projective line of a nonzero label matters.
Within a fixed line class, edge differences propagate a label through the
monochromatic component; a vertex becomes forced exactly when it acquires two
distinct line classes.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from z3 import (
    And,
    Bool,
    BoolVal,
    If,
    Int,
    Optimize,
    Or,
    Solver,
    Sum,
    sat,
)

ZERO = (0, 0)
DIAGONAL = (1, -1)
CANONICAL_LABELS = [
    (1, 0),
    (0, 1),
    (1, 1),
    (1, 2),
    (2, 1),
    (1, 3),
    (3, 1),
    (1, 4),
    (4, 1),
]


def gcd2(a: int, b: int) -> int:
    return math.gcd(abs(a), abs(b))


def normalize_line(label: tuple[int, int]) -> tuple[int, int]:
    a, b = label
    if a == 0 and b == 0:
        raise ValueError("zero label has no projective line")
    g = gcd2(a, b)
    a //= g
    b //= g
    if a < 0 or (a == 0 and b < 0):
        a = -a
        b = -b
    return (a, b)


def canonical_label_for_line(line: tuple[int, int]) -> tuple[int, int]:
    if line == normalize_line(DIAGONAL):
        raise ValueError("diagonal line is forbidden for X")
    return line


def parse_ratio(text: str) -> tuple[int, int]:
    if "/" in text:
        a, b = text.split("/", 1)
        return (int(a), int(b))
    value = Fraction(text)
    return (value.numerator, value.denominator)


def literal_eval_line(text: str):
    return ast.literal_eval(text.strip())


def vertex_sort_key(vertex: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(vertex)


@dataclass(frozen=True)
class PrefixSlot:
    stage: int
    key: tuple[int, ...]
    weight: int
    edges: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]


@dataclass(frozen=True)
class Seed:
    vertex: tuple[int, ...]
    label: tuple[int, int]


@dataclass
class Witness:
    x_labels: tuple[tuple[int, int], ...]
    dims: tuple[int, ...]
    f_dicts: tuple[dict[tuple[int, ...], tuple[int, int]], ...]
    initial_t: tuple[tuple[int, ...], ...]
    seeds: tuple[Seed, ...]

    @property
    def n(self) -> int:
        total = 1
        for dim in self.dims:
            total *= dim
        return total


@dataclass
class TraceLayer:
    step: int
    forced_before: list[tuple[int, ...]]
    available_lines: dict[str, list[tuple[int, ...]]]
    newly_forced: list[dict[str, object]]


@dataclass
class VerificationResult:
    valid: bool
    forced_all: bool
    score_num: int
    score_den: int
    m: int
    r: int
    n: int
    t: int
    lines: dict[tuple[int, int], int]
    trace_layers: list[TraceLayer]
    final_forced: list[tuple[int, ...]]
    errors: list[str]


def all_vertices(dims: Sequence[int]) -> list[tuple[int, ...]]:
    return [tuple(p) for p in product(*(range(1, dim + 1) for dim in dims))]


def build_vertex_index(dims: Sequence[int]) -> dict[tuple[int, ...], int]:
    return {vertex: idx for idx, vertex in enumerate(all_vertices(dims))}


def prefix_domains(dims: Sequence[int], stage: int) -> list[tuple[int, ...]]:
    ranges = [range(1, dims[i] + 1) for i in range(stage - 1)]
    ranges.append(range(1, dims[stage - 1]))
    if not ranges:
        return [tuple()]
    return [tuple(p) for p in product(*ranges)]


def build_prefix_slots(dims: Sequence[int]) -> list[PrefixSlot]:
    slots: list[PrefixSlot] = []
    suffix_cache: dict[int, list[tuple[int, ...]]] = {}
    k = len(dims)
    for stage in range(1, k + 1):
        if stage not in suffix_cache:
            if stage == k:
                suffix_cache[stage] = [tuple()]
            else:
                suffix_cache[stage] = [
                    tuple(s)
                    for s in product(
                        *(range(1, dims[j] + 1) for j in range(stage, k))
                    )
                ]
        suffixes = suffix_cache[stage]
        weight = len(suffixes)
        for key in prefix_domains(dims, stage):
            edges = []
            for suffix in suffixes:
                left = key[:-1] + (key[-1],) + suffix
                right = key[:-1] + (key[-1] + 1,) + suffix
                edges.append((left, right))
            slots.append(
                PrefixSlot(
                    stage=stage,
                    key=key,
                    weight=weight,
                    edges=tuple(edges),
                )
            )
    return slots


def normalize_witness(
    x_labels: Sequence[Sequence[int]],
    dims: Sequence[int],
    f_list: Sequence[dict],
    t_list: Sequence[Sequence[int]],
    r_list: Sequence[dict],
) -> Witness:
    labels = tuple(tuple(map(int, pair)) for pair in x_labels)
    dims_t = tuple(int(v) for v in dims)
    f_dicts: list[dict[tuple[int, ...], tuple[int, int]]] = []
    for stage, mapping in enumerate(f_list, start=1):
        normalized: dict[tuple[int, ...], tuple[int, int]] = {}
        for raw_key, raw_value in mapping.items():
            key = tuple(int(x) for x in raw_key)
            value = tuple(int(x) for x in raw_value)
            normalized[key] = value
        f_dicts.append(normalized)
    seeds: list[Seed] = []
    for mapping in r_list:
        items = list(mapping.items())
        if len(items) != 1:
            raise ValueError("each R entry must be singleton-supported")
        raw_key, raw_value = items[0]
        seeds.append(
            Seed(
                vertex=tuple(int(x) for x in raw_key),
                label=tuple(int(x) for x in raw_value),
            )
        )
    initial_t = tuple(tuple(int(x) for x in vertex) for vertex in t_list)
    return Witness(
        x_labels=labels,
        dims=dims_t,
        f_dicts=tuple(f_dicts),
        initial_t=initial_t,
        seeds=tuple(seeds),
    )


def parse_witness_text(text: str) -> Witness:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 6:
        raise ValueError("witness text must contain at least six non-empty lines")
    x_labels = literal_eval_line(lines[1])
    dims = literal_eval_line(lines[2])
    f_list = literal_eval_line(lines[3])
    t_list = literal_eval_line(lines[4])
    r_list = literal_eval_line(lines[5])
    return normalize_witness(x_labels, dims, f_list, t_list, r_list)


def witness_to_text(witness: Witness, score_header: str | None = None) -> str:
    lines = []
    if score_header is None:
        lines.append("generated witness")
    else:
        lines.append(score_header)
    lines.append(repr(list(witness.x_labels)))
    lines.append(repr(list(witness.dims)))
    f_out = []
    for mapping in witness.f_dicts:
        out = {tuple(key): tuple(value) for key, value in sorted(mapping.items())}
        f_out.append(out)
    lines.append(repr(f_out))
    lines.append(repr(list(witness.initial_t)))
    r_out = [{seed.vertex: seed.label} for seed in witness.seeds]
    lines.append(repr(r_out))
    return "\n".join(lines)


def line_palette_from_witness(witness: Witness) -> dict[tuple[int, int], int]:
    lines: dict[tuple[int, int], int] = {}
    for label in witness.x_labels:
        if label == ZERO:
            continue
        line = normalize_line(label)
        if line == normalize_line(DIAGONAL):
            raise ValueError("X contains the forbidden diagonal line")
        if line not in lines:
            lines[line] = len(lines) + 1
    return lines


def validate_witness(witness: Witness) -> list[str]:
    errors: list[str] = []
    if ZERO not in witness.x_labels:
        errors.append("X must contain (0, 0)")
    label_set = set(witness.x_labels)
    if len(witness.f_dicts) != len(witness.dims):
        errors.append("number of f_i dictionaries must match len(dims)")
    vertices = set(all_vertices(witness.dims))
    for label in witness.x_labels:
        if label == ZERO:
            continue
        if label[0] + label[1] == 0:
            errors.append(f"forbidden diagonal label in X: {label}")
    for stage, mapping in enumerate(witness.f_dicts, start=1):
        for key, value in mapping.items():
            if value not in label_set:
                errors.append(f"f_{stage}{key} uses label outside X: {value}")
            if len(key) != stage:
                errors.append(f"f_{stage}{key} has wrong key length")
                continue
            for idx in range(stage - 1):
                if not (1 <= key[idx] <= witness.dims[idx]):
                    errors.append(f"f_{stage}{key} is out of range")
            if stage > 0 and not (1 <= key[-1] <= witness.dims[stage - 1] - 1):
                errors.append(f"f_{stage}{key} uses invalid edge coordinate")
    for vertex in witness.initial_t:
        if vertex not in vertices:
            errors.append(f"T contains invalid vertex {vertex}")
    for seed in witness.seeds:
        if seed.vertex not in vertices:
            errors.append(f"R contains invalid vertex {seed.vertex}")
        if seed.label not in label_set:
            errors.append(f"R contains label outside X: {seed.label}")
        if seed.label == ZERO:
            errors.append("R entries must be nonzero")
    return errors


def actual_edges_with_lines(
    witness: Witness,
    line_ids: dict[tuple[int, int], int],
) -> list[tuple[tuple[int, ...], tuple[int, ...], int]]:
    edges: list[tuple[tuple[int, ...], tuple[int, ...], int]] = []
    slot_lookup = {
        (slot.stage, slot.key): slot for slot in build_prefix_slots(witness.dims)
    }
    for stage, mapping in enumerate(witness.f_dicts, start=1):
        for key, label in mapping.items():
            if label == ZERO:
                continue
            line = line_ids[normalize_line(label)]
            slot = slot_lookup[(stage, key)]
            for edge in slot.edges:
                edges.append((edge[0], edge[1], line))
    return edges


def score_components(witness: Witness) -> tuple[int, int, int, int]:
    slots = build_prefix_slots(witness.dims)
    mapping = {
        (slot.stage, slot.key): slot for slot in slots
    }
    m = 0
    for stage, f_dict in enumerate(witness.f_dicts, start=1):
        for key, label in f_dict.items():
            if label != ZERO:
                m += mapping[(stage, key)].weight
    r = len(witness.seeds)
    n = witness.n
    t = len(witness.initial_t)
    return (m, r, n, t)


def dense_vector(size: int, updates: Sequence[tuple[int, int]]) -> list[int]:
    vec = [0] * size
    for idx, value in updates:
        vec[idx] += value
    return vec


def exact_generators(
    witness: Witness,
) -> tuple[list[dict[str, object]], list[list[int]], list[tuple[int, ...]], dict[tuple[int, ...], int]]:
    vertices = all_vertices(witness.dims)
    vertex_index = {vertex: idx for idx, vertex in enumerate(vertices)}
    size = 2 * len(vertices)
    descriptors: list[dict[str, object]] = []
    vectors: list[list[int]] = []
    for seed_idx, seed in enumerate(witness.seeds):
        v_idx = vertex_index[seed.vertex]
        descriptors.append(
            {
                "kind": "seed",
                "seed_index": seed_idx,
                "vertex": seed.vertex,
                "label": seed.label,
            }
        )
        vectors.append(
            dense_vector(
                size,
                [
                    (2 * v_idx, seed.label[0]),
                    (2 * v_idx + 1, seed.label[1]),
                ],
            )
        )
    slot_lookup = {
        (slot.stage, slot.key): slot for slot in build_prefix_slots(witness.dims)
    }
    for stage, mapping in enumerate(witness.f_dicts, start=1):
        for key, label in sorted(mapping.items()):
            if label == ZERO:
                continue
            slot = slot_lookup[(stage, key)]
            for edge_idx, (left, right) in enumerate(slot.edges):
                left_idx = vertex_index[left]
                right_idx = vertex_index[right]
                descriptors.append(
                    {
                        "kind": "edge",
                        "stage": stage,
                        "key": key,
                        "edge_index": edge_idx,
                        "u": left,
                        "v": right,
                        "label": label,
                    }
                )
                vectors.append(
                    dense_vector(
                        size,
                        [
                            (2 * left_idx, label[0]),
                            (2 * left_idx + 1, label[1]),
                            (2 * right_idx, -label[0]),
                            (2 * right_idx + 1, -label[1]),
                        ],
                    )
                )
    return descriptors, vectors, vertices, vertex_index


def solve_linear_system(
    columns: Sequence[Sequence[int]],
    target: Sequence[int],
) -> list[Fraction] | None:
    rows = len(target)
    cols = len(columns)
    matrix = [
        [Fraction(columns[c][r]) for c in range(cols)] + [Fraction(target[r])]
        for r in range(rows)
    ]
    pivot_cols: list[int] = []
    pivot_row = 0
    for pivot_col in range(cols):
        found = None
        for row in range(pivot_row, rows):
            if matrix[row][pivot_col] != 0:
                found = row
                break
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        scale = matrix[pivot_row][pivot_col]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or matrix[row][pivot_col] == 0:
                continue
            factor = matrix[row][pivot_col]
            matrix[row] = [
                matrix[row][idx] - factor * matrix[pivot_row][idx]
                for idx in range(cols + 1)
            ]
        pivot_cols.append(pivot_col)
        pivot_row += 1
        if pivot_row == rows:
            break
    for row in matrix:
        if all(value == 0 for value in row[:-1]) and row[-1] != 0:
            return None
    solution = [Fraction(0) for _ in range(cols)]
    for row_idx, pivot_col in enumerate(pivot_cols):
        solution[pivot_col] = matrix[row_idx][-1]
    return solution


def exact_trace(witness: Witness) -> VerificationResult:
    errors = validate_witness(witness)
    m, r, n, t = score_components(witness)
    if n - t <= 0:
        errors.append("score denominator n - |T| must be positive")
    if errors:
        return VerificationResult(
            valid=False,
            forced_all=False,
            score_num=m + r,
            score_den=n - t,
            m=m,
            r=r,
            n=n,
            t=t,
            lines={},
            trace_layers=[],
            final_forced=[],
            errors=errors,
        )

    descriptors, vectors, vertices, vertex_index = exact_generators(witness)
    forced = set(witness.initial_t)
    line_map = line_palette_from_witness(witness)
    trace_layers: list[TraceLayer] = []
    step = 0
    while True:
        active_vertices = [vertex for vertex in vertices if vertex not in forced]
        active_indices = [
            index
            for vertex in active_vertices
            for index in (2 * vertex_index[vertex], 2 * vertex_index[vertex] + 1)
        ]
        projected = [vector_support_projection(vec, active_indices) for vec in vectors]
        newly: list[dict[str, object]] = []
        for vertex in active_vertices:
            target = [0] * len(active_indices)
            offset = active_indices.index(2 * vertex_index[vertex])
            target[offset] = 1
            target[offset + 1] = -1
            coeffs = solve_linear_system(projected, target)
            if coeffs is None:
                continue
            support = []
            used_lines = set()
            for idx, coeff in enumerate(coeffs):
                if coeff == 0:
                    continue
                desc = descriptors[idx]
                if "label" in desc and desc["label"] != ZERO:
                    used_lines.add(normalize_line(desc["label"]))
                support.append(
                    {
                        "generator_index": idx,
                        "coefficient": [coeff.numerator, coeff.denominator],
                        "descriptor": desc,
                    }
                )
            newly.append(
                {
                    "vertex": vertex,
                    "support_size": len(support),
                    "support": support,
                    "line_support": sorted(used_lines),
                }
            )
        trace_layers.append(
            TraceLayer(
                step=step,
                forced_before=sorted(forced, key=vertex_sort_key),
                available_lines={},
                newly_forced=newly,
            )
        )
        if not newly:
            break
        for record in newly:
            forced.add(tuple(record["vertex"]))
        step += 1
        if step > n:
            errors.append("forcing trace exceeded n layers without stabilizing")
            break

    return VerificationResult(
        valid=not errors,
        forced_all=len(forced) == n and not errors,
        score_num=m + r,
        score_den=n - t,
        m=m,
        r=r,
        n=n,
        t=t,
        lines={line: idx for line, idx in sorted(line_map.items(), key=lambda item: item[1])},
        trace_layers=trace_layers,
        final_forced=sorted(forced, key=vertex_sort_key),
        errors=errors,
    )


def adjacency_by_line(
    witness: Witness,
    line_ids: dict[tuple[int, int], int],
) -> tuple[dict[int, dict[tuple[int, ...], set[tuple[int, ...]]]], dict[tuple[int, ...], set[int]]]:
    adj: dict[int, dict[tuple[int, ...], set[tuple[int, ...]]]] = defaultdict(
        lambda: defaultdict(set)
    )
    incident_lines: dict[tuple[int, ...], set[int]] = defaultdict(set)
    for u, v, line in actual_edges_with_lines(witness, line_ids):
        adj[line][u].add(v)
        adj[line][v].add(u)
        incident_lines[u].add(line)
        incident_lines[v].add(line)
    return adj, incident_lines


def synchronous_trace(witness: Witness) -> VerificationResult:
    return exact_trace(witness)


def reduced_synchronous_trace(witness: Witness) -> VerificationResult:
    errors = validate_witness(witness)
    if errors:
        m, r, n, t = score_components(witness)
        return VerificationResult(
            valid=False,
            forced_all=False,
            score_num=m + r,
            score_den=n - t,
            m=m,
            r=r,
            n=n,
            t=t,
            lines={},
            trace_layers=[],
            final_forced=[],
            errors=errors,
        )

    line_map = line_palette_from_witness(witness)
    reverse_line = {idx: line for line, idx in line_map.items()}
    adj, _ = adjacency_by_line(witness, line_map)
    seeds_by_line: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for seed in witness.seeds:
        seeds_by_line[line_map[normalize_line(seed.label)]].add(seed.vertex)
    forced = set(witness.initial_t)
    vertices = sorted(all_vertices(witness.dims), key=vertex_sort_key)
    layers: list[TraceLayer] = []
    step = 0
    while True:
        available: dict[int, set[tuple[int, ...]]] = {}
        for line_id in reverse_line:
            seen = set(forced) | set(seeds_by_line[line_id])
            queue = deque(seen)
            while queue:
                vertex = queue.popleft()
                for neighbor in adj[line_id].get(vertex, ()):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            available[line_id] = seen
        newly = []
        for vertex in vertices:
            if vertex in forced:
                continue
            active_lines = [line for line in sorted(reverse_line) if vertex in available[line]]
            if len(active_lines) >= 2:
                newly.append(
                    {
                        "vertex": vertex,
                        "line_pair": [reverse_line[active_lines[0]], reverse_line[active_lines[1]]],
                        "line_ids": [active_lines[0], active_lines[1]],
                    }
                )
        layers.append(
            TraceLayer(
                step=step,
                forced_before=sorted(forced, key=vertex_sort_key),
                available_lines={
                    str(reverse_line[line]): sorted(available[line], key=vertex_sort_key)
                    for line in sorted(reverse_line)
                },
                newly_forced=newly,
            )
        )
        if not newly:
            break
        for record in newly:
            forced.add(tuple(record["vertex"]))
        step += 1
        if step > witness.n:
            errors.append("forcing trace exceeded n layers without stabilizing")
            break
    m, r, n, t = score_components(witness)
    if n - t <= 0:
        errors.append("score denominator n - |T| must be positive")
    return VerificationResult(
        valid=not errors,
        forced_all=len(forced) == witness.n and not errors,
        score_num=m + r,
        score_den=n - t,
        m=m,
        r=r,
        n=n,
        t=t,
        lines={line: idx for line, idx in sorted(line_map.items(), key=lambda item: item[1])},
        trace_layers=layers,
        final_forced=sorted(forced, key=vertex_sort_key),
        errors=errors,
    )


def vector_support_projection(
    vec: Sequence[int],
    active_indices: Sequence[int],
) -> list[int]:
    return [vec[i] for i in active_indices]


def solve_in_rational_span(columns: Sequence[Sequence[int]], target: Sequence[int]) -> bool:
    if not columns:
        return False
    rows = len(target)
    cols = len(columns)
    matrix = [
        [Fraction(columns[c][r]) for c in range(cols)] + [Fraction(target[r])]
        for r in range(rows)
    ]
    pivot_row = 0
    for pivot_col in range(cols):
        found = None
        for row in range(pivot_row, rows):
            if matrix[row][pivot_col] != 0:
                found = row
                break
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        scale = matrix[pivot_row][pivot_col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or matrix[row][pivot_col] == 0:
                continue
            factor = matrix[row][pivot_col]
            matrix[row] = [
                matrix[row][idx] - factor * matrix[pivot_row][idx]
                for idx in range(cols + 1)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    for row in matrix:
        if all(value == 0 for value in row[:-1]) and row[-1] != 0:
            return False
    return True


def linear_crosscheck_path(
    colors: Sequence[tuple[int, int]],
    n: int,
    edge_labels: Sequence[int],
    seed_specs: Sequence[tuple[int, int]],
    initial_t: Sequence[int],
) -> bool:
    total_vertices = n
    generators: list[list[int]] = []
    for vertex, color_idx in seed_specs:
        label = colors[color_idx]
        vec = [0] * (2 * total_vertices)
        vec[2 * vertex] = label[0]
        vec[2 * vertex + 1] = label[1]
        generators.append(vec)
    for edge_idx, color_idx in enumerate(edge_labels):
        if color_idx < 0:
            continue
        label = colors[color_idx]
        vec = [0] * (2 * total_vertices)
        vec[2 * edge_idx] = label[0]
        vec[2 * edge_idx + 1] = label[1]
        vec[2 * (edge_idx + 1)] = -label[0]
        vec[2 * (edge_idx + 1) + 1] = -label[1]
        generators.append(vec)
    forced = set(initial_t)
    while True:
        changed = False
        active_indices = [
            idx
            for vertex in range(total_vertices)
            if vertex not in forced
            for idx in (2 * vertex, 2 * vertex + 1)
        ]
        if not active_indices:
            return True
        columns = [vector_support_projection(vec, active_indices) for vec in generators]
        for vertex in range(total_vertices):
            if vertex in forced:
                continue
            target = [0] * len(active_indices)
            pos = active_indices.index(2 * vertex)
            target[pos] = 1
            target[pos + 1] = -1
            if solve_in_rational_span(columns, target):
                forced.add(vertex)
                changed = True
        if not changed:
            return len(forced) == total_vertices


def run_crosscheck_random(samples: int, max_n: int) -> dict[str, int]:
    import random

    colors = [(1, 0), (0, 1), (1, 1)]
    checked = 0
    for n in range(2, max_n + 1):
        for _ in range(samples):
            edge_labels = [random.randrange(len(colors)) for _ in range(n - 1)]
            seed_specs = []
            for vertex in range(n):
                for color_idx in range(len(colors)):
                    if random.random() < 0.15:
                        seed_specs.append((vertex, color_idx))
            initial_t = [vertex for vertex in range(n) if random.random() < 0.05]
            if len(initial_t) == n:
                initial_t = initial_t[:-1]
            linear_ok = linear_crosscheck_path(colors, n, edge_labels, seed_specs, initial_t)
            edges = [colors[idx] for idx in edge_labels]
            reduced_witness = normalize_witness(
                [ZERO, *colors],
                [n],
                [{(idx + 1,): edge for idx, edge in enumerate(edges)}],
                [[vertex + 1] for vertex in initial_t],
                [{(vertex + 1,): colors[color]} for vertex, color in seed_specs],
            )
            reduced_ok = synchronous_trace(reduced_witness).forced_all
            if linear_ok != reduced_ok:
                raise RuntimeError(
                    "linear/reduced mismatch "
                    f"n={n} edges={edge_labels} seeds={seed_specs} T={initial_t}"
                )
            checked += 1
    return {"checked_samples": checked}


def color_symbol(color_id: int) -> str:
    return f"c{color_id}"


@dataclass(frozen=True)
class SearchConfig:
    dims: tuple[int, ...]
    colors: int
    threshold_num: int
    threshold_den: int
    max_force_layers: int
    max_prop_rounds: int
    allow_initial_t: bool
    require_connected_support: bool
    optimize: bool


def z3_bool_sum(items: Iterable) -> object:
    return Sum([If(item, 1, 0) for item in items])


def search_geometry(config: SearchConfig) -> Witness | None:
    dims = config.dims
    vertices = all_vertices(dims)
    vertex_to_idx = {vertex: idx for idx, vertex in enumerate(vertices)}
    slots = build_prefix_slots(dims)
    solver = Optimize() if config.optimize else Solver()

    color_vars = {
        (slot.stage, slot.key): Int(f"slot_{slot.stage}_{'_'.join(map(str, slot.key))}")
        for slot in slots
    }
    for var in color_vars.values():
        solver.add(var >= 0, var <= config.colors)

    force0 = {
        vertex: Bool(f"force0_{'_'.join(map(str, vertex))}")
        for vertex in vertices
    }
    if not config.allow_initial_t:
        for var in force0.values():
            solver.add(var == BoolVal(False))

    seed = {
        (vertex, color): Bool(f"seed_{'_'.join(map(str, vertex))}_{color}")
        for vertex in vertices
        for color in range(1, config.colors + 1)
    }

    neighbors_for_slot: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    actual_edges = []
    for slot in slots:
        for left, right in slot.edges:
            actual_edges.append((left, right, color_vars[(slot.stage, slot.key)]))
            neighbors_for_slot[left].append(right)
            neighbors_for_slot[right].append(left)

    max_layers = config.max_force_layers
    max_rounds = config.max_prop_rounds
    forced = {
        (layer, vertex): Bool(f"forced_{layer}_{'_'.join(map(str, vertex))}")
        for layer in range(max_layers + 1)
        for vertex in vertices
    }
    avail = {
        (layer, round_idx, color, vertex): Bool(
            f"avail_{layer}_{round_idx}_{color}_{'_'.join(map(str, vertex))}"
        )
        for layer in range(max_layers)
        for round_idx in range(max_rounds + 1)
        for color in range(1, config.colors + 1)
        for vertex in vertices
    }

    for vertex in vertices:
        solver.add(forced[(0, vertex)] == force0[vertex])

    for layer in range(max_layers):
        for color in range(1, config.colors + 1):
            for vertex in vertices:
                solver.add(
                    avail[(layer, 0, color, vertex)]
                    == Or(forced[(layer, vertex)], seed[(vertex, color)])
                )
            for round_idx in range(max_rounds):
                for vertex in vertices:
                    propagated = [avail[(layer, round_idx, color, vertex)]]
                    for left, right, slot_color in actual_edges:
                        if left == vertex:
                            propagated.append(
                                And(slot_color == color, avail[(layer, round_idx, color, right)])
                            )
                        elif right == vertex:
                            propagated.append(
                                And(slot_color == color, avail[(layer, round_idx, color, left)])
                            )
                    solver.add(
                        avail[(layer, round_idx + 1, color, vertex)] == Or(*propagated)
                    )
        for vertex in vertices:
            active_colors = [
                avail[(layer, max_rounds, color, vertex)]
                for color in range(1, config.colors + 1)
            ]
            solver.add(
                forced[(layer + 1, vertex)]
                == Or(
                    forced[(layer, vertex)],
                    z3_bool_sum(active_colors) >= 2,
                )
            )

    for vertex in vertices:
        solver.add(forced[(max_layers, vertex)])

    m_terms = []
    for slot in slots:
        m_terms.append(
            If(color_vars[(slot.stage, slot.key)] == 0, 0, slot.weight)
        )
    r_terms = [If(seed_key, 1, 0) for seed_key in seed.values()]
    t_terms = [If(force0[vertex], 1, 0) for vertex in vertices]
    m_expr = Sum(m_terms)
    r_expr = Sum(r_terms)
    t_expr = Sum(t_terms)
    n_value = len(vertices)
    solver.add(
        config.threshold_den * (m_expr + r_expr)
        <= config.threshold_num * (n_value - t_expr)
    )
    solver.add(t_expr <= n_value - 1)

    if config.require_connected_support:
        # A light connectivity proxy: every non-forced vertex must touch at least one
        # nonzero edge or carry a seed; this avoids trivially isolated junk.
        for vertex in vertices:
            incident_nonzero = []
            for left, right, slot_color in actual_edges:
                if left == vertex or right == vertex:
                    incident_nonzero.append(slot_color != 0)
            seed_here = [seed[(vertex, color)] for color in range(1, config.colors + 1)]
            solver.add(
                Or(force0[vertex], Or(*(incident_nonzero + seed_here)))
            )

    if config.optimize:
        solver.minimize(m_expr + r_expr)
        solver.minimize(t_expr)

    if solver.check() != sat:
        return None

    model = solver.model()
    used_colors = sorted(
        {
            model.eval(var).as_long()
            for var in color_vars.values()
            if model.eval(var).as_long() != 0
        }
        | {
            color
            for vertex in vertices
            for color in range(1, config.colors + 1)
            if model.eval(seed[(vertex, color)])
        }
    )
    color_remap = {old: new for new, old in enumerate(used_colors, start=1)}
    label_pool = [ZERO] + CANONICAL_LABELS
    if len(used_colors) > len(CANONICAL_LABELS):
        raise ValueError("not enough canonical labels for remapped colors")
    x_labels = [ZERO] + [label_pool[idx] for idx in range(1, len(used_colors) + 1)]
    f_dicts = [dict() for _ in dims]
    for slot in slots:
        raw_color = model.eval(color_vars[(slot.stage, slot.key)]).as_long()
        if raw_color == 0:
            continue
        mapped = color_remap[raw_color]
        f_dicts[slot.stage - 1][slot.key] = label_pool[mapped]
    t_list = [
        vertex
        for vertex in vertices
        if model.eval(force0[vertex])
    ]
    seeds_out = []
    for vertex in vertices:
        for color in range(1, config.colors + 1):
            if model.eval(seed[(vertex, color)]):
                seeds_out.append({vertex: label_pool[color_remap[color]]})
    return normalize_witness(
        x_labels,
        dims,
        f_dicts,
        t_list,
        seeds_out,
    )


def geometry_list_from_text(text: str) -> tuple[int, ...]:
    separators = ["x", "X", ",", " "]
    chunks = [text]
    for sep in separators:
        next_chunks = []
        for chunk in chunks:
            next_chunks.extend(part for part in chunk.split(sep) if part)
        chunks = next_chunks
    return tuple(int(chunk) for chunk in chunks)


def run_search(args: argparse.Namespace) -> int:
    dims = geometry_list_from_text(args.dims)
    num, den = parse_ratio(args.threshold)
    config = SearchConfig(
        dims=dims,
        colors=args.colors,
        threshold_num=num,
        threshold_den=den,
        max_force_layers=args.max_force_layers or math.prod(dims),
        max_prop_rounds=args.max_prop_rounds or math.prod(dims),
        allow_initial_t=args.allow_initial_t,
        require_connected_support=not args.allow_disconnected,
        optimize=args.optimize,
    )
    witness = search_geometry(config)
    if witness is None:
        print(json.dumps({"status": "unsat", "dims": dims, "colors": args.colors}))
        return 1
    result = synchronous_trace(witness)
    score_header = (
        f"{result.score_num}/{result.score_den} "
        f"(m={result.m}, r={result.r}, n={result.n}, t={result.t})"
    )
    if args.output:
        Path(args.output).write_text(witness_to_text(witness, score_header) + "\n")
    print(witness_to_text(witness, score_header))
    return 0


def run_verify(args: argparse.Namespace) -> int:
    text = Path(args.path).read_text() if args.path else args.text
    witness = parse_witness_text(text)
    result = synchronous_trace(witness)
    payload = {
        "valid": result.valid,
        "forced_all": result.forced_all,
        "score": f"{result.score_num}/{result.score_den}",
        "m": result.m,
        "r": result.r,
        "n": result.n,
        "t": result.t,
        "lines": {str(line): idx for line, idx in result.lines.items()},
        "final_forced": result.final_forced,
        "errors": result.errors,
    }
    if args.trace_json:
        trace_payload = {
            "score": payload["score"],
            "m": result.m,
            "r": result.r,
            "n": result.n,
            "t": result.t,
            "lines": {str(line): idx for line, idx in result.lines.items()},
            "layers": [
                {
                    "step": layer.step,
                    "forced_before": layer.forced_before,
                    "available_lines": layer.available_lines,
                    "newly_forced": layer.newly_forced,
                }
                for layer in result.trace_layers
            ],
            "final_forced": result.final_forced,
            "errors": result.errors,
        }
        Path(args.trace_json).write_text(json.dumps(trace_payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0 if result.valid and result.forced_all else 1


def run_crosscheck(args: argparse.Namespace) -> int:
    payload = run_crosscheck_random(args.samples, args.max_n)
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    verify = sub.add_parser("verify", help="verify a witness and emit JSON")
    verify.add_argument("--path", type=str, help="path to a six-line witness file")
    verify.add_argument("--text", type=str, help="inline six-line witness text")
    verify.add_argument("--trace-json", type=str, help="optional path for trace JSON")
    verify.set_defaults(func=run_verify)

    search = sub.add_parser("search", help="search a bounded geometry with Z3")
    search.add_argument("--dims", required=True, help="geometry, e.g. 8 or 2x3x4")
    search.add_argument("--colors", type=int, default=3, help="number of search colors")
    search.add_argument("--threshold", default="67/40", help="score threshold")
    search.add_argument("--max-force-layers", type=int)
    search.add_argument("--max-prop-rounds", type=int)
    search.add_argument("--allow-initial-t", action="store_true")
    search.add_argument("--allow-disconnected", action="store_true")
    search.add_argument("--optimize", action="store_true")
    search.add_argument("--output", type=str)
    search.set_defaults(func=run_search)

    cross = sub.add_parser("crosscheck", help="random linear/reduced agreement checks")
    cross.add_argument("--samples", type=int, default=200)
    cross.add_argument("--max-n", type=int, default=6)
    cross.set_defaults(func=run_crosscheck)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "verify" and not args.path and not args.text:
        parser.error("verify requires --path or --text")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
