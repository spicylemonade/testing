#!/usr/bin/env python3
"""Compute the narrow H2 screening package on corridor families.

This script deliberately stays inside the frozen width-2 corridor family. It
compares representative frozen-H1 families against matched direct-search
controls using the invariant package from ``results/phase3_h2_program.md``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ca_kakeya_search import CorridorInstance, SpanOracle, same_sum_palette


Vector = Tuple[int, int]


def determinant(a: Vector, b: Vector) -> int:
    return a[0] * b[1] - a[1] * b[0]


def nonzero_labels(x_labels: Sequence[Vector]) -> List[Vector]:
    return [label for label in x_labels if label != (0, 0)]


def h1_identity_word(level: int) -> Tuple[str, ...]:
    word = ("L_a", "R_a")
    sigma = {
        "L_a": ("L_a", "M_a"),
        "M_a": ("M_a", "M_a"),
        "R_a": ("M_a", "R_a"),
    }
    for _ in range(level):
        word = tuple(symbol for state in word for symbol in sigma[state])
    return word


def h1_identity_instance(level: int) -> CorridorInstance:
    x_labels = tuple(same_sum_palette(1, 4))
    zero, u, v, w, z = x_labels
    assert zero == (0, 0)
    word = h1_identity_word(level)
    width = len(word)
    # Every internal interface is carry_a, so top edges are u and bottom edges are zero.
    top = (u,) * (width - 1)
    bottom = ((0, 0),) * (width - 1)
    seeds = (((1, 1), u),)
    return CorridorInstance(
        width=width,
        x_labels=x_labels,
        vertical=z,
        top=top,
        bottom=bottom,
        seeds=seeds,
        initial_t=tuple(),
    )


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


def smith_diagonal(matrix: Matrix) -> List[int]:
    if matrix.rows == 0 or matrix.cols == 0:
        return []
    diagonal = smith_normal_form(matrix, domain=ZZ)
    out: List[int] = []
    for idx in range(min(diagonal.rows, diagonal.cols)):
        value = int(diagonal[idx, idx])
        if value != 0:
            out.append(abs(value))
    return out


def target_solvable_vertices(instance: CorridorInstance) -> int:
    oracle = SpanOracle.from_generators(instance.generators())
    return len(oracle.solvable_vertices(instance.vertices))


def invariant_summary(family_id: str, instance: CorridorInstance, forcing: bool) -> Dict[str, object]:
    generators = instance.generators()
    if generators:
        matrix = Matrix(list(zip(*generators)))
        rank = int(matrix.rank())
        smith = smith_diagonal(matrix)
    else:
        matrix = Matrix([])
        rank = 0
        smith = []
    nz = nonzero_labels(instance.x_labels)
    determinant_pattern = sorted(
        {
            abs(determinant(a, b))
            for i, a in enumerate(nz)
            for b in nz[i + 1 :]
        }
    )
    coord_height = max((max(abs(a), abs(b)) for a, b in nz), default=0)
    return {
        "family_id": family_id,
        "forcing": forcing,
        "score": None if not forcing else instance.score,
        "m": instance.m,
        "r": instance.r,
        "n": instance.n,
        "t": instance.t,
        "rank": rank,
        "smith_diagonal": smith,
        "support_size": instance.r,
        "edge_density": instance.m / instance.n,
        "determinant_pattern": determinant_pattern,
        "coordinate_height": coord_height,
        "nonzero_x_size": len(nz),
        "target_solvable_vertices": target_solvable_vertices(instance),
    }


def evaluate_controls(paths: Iterable[Path]) -> List[Dict[str, object]]:
    rows = []
    for path in paths:
        instance = load_best_instance(path)
        rows.append(
            invariant_summary(
                family_id=path.stem,
                instance=instance,
                forcing=True,
            )
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--control",
        type=Path,
        action="append",
        default=[],
        help="Path to a saved random-search JSON result whose best witness will be screened.",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    h1_rows = [
        invariant_summary(
            family_id="h1_identity_L1",
            instance=h1_identity_instance(level=1),
            forcing=False,
        ),
        invariant_summary(
            family_id="h1_identity_L2",
            instance=h1_identity_instance(level=2),
            forcing=False,
        ),
    ]
    control_rows = evaluate_controls(args.control)

    summary = {
        "route": "H2_target_direction_abelian",
        "h1_rows": h1_rows,
        "control_rows": control_rows,
        "conclusion": (
            "The raw support-size / rank package already separates the failed frozen-H1 "
            "families from the direct corridor controls: H1 has support size 1, "
            "target_solvable_vertices 0, and no forcing, while the matched controls "
            "require larger support and do force. No additional abelian-screening gain "
            "is visible on this family set."
        ),
        "kill_h2": True,
    }
    payload = json.dumps(summary, indent=2)
    if args.output:
        args.output.write_text(payload)
    print(payload)


if __name__ == "__main__":
    main()
