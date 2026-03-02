"""Comprehensive verification checker for all 7 integer conditions of a perfect cuboid.

Verifies edges (3), face diagonals (3), and space diagonal (1) for exact integrality
using integer square root checks — no floating point involved in the integrality test.
"""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.cuboid import is_perfect_square, isqrt


def verify_cuboid(a: int, b: int, c: int) -> dict:
    """Verify all 7 integer conditions for a potential perfect cuboid.

    Args:
        a, b, c: Positive integer edge lengths.

    Returns:
        Dict with detailed report:
        - values: dict of all 7 values and whether each is integer
        - is_euler_brick: bool
        - is_perfect_cuboid: bool
        - summary: human-readable summary string
    """
    a2, b2, c2 = a * a, b * b, c * c

    # Face diagonal squared values
    d_ab_sq = a2 + b2
    d_ac_sq = a2 + c2
    d_bc_sq = b2 + c2

    # Space diagonal squared
    d_s_sq = a2 + b2 + c2

    # Check each for perfect square
    d_ab_is_int = is_perfect_square(d_ab_sq)
    d_ac_is_int = is_perfect_square(d_ac_sq)
    d_bc_is_int = is_perfect_square(d_bc_sq)
    d_s_is_int = is_perfect_square(d_s_sq)

    # Compute actual values
    d_ab_val = isqrt(d_ab_sq) if d_ab_is_int else math.sqrt(d_ab_sq)
    d_ac_val = isqrt(d_ac_sq) if d_ac_is_int else math.sqrt(d_ac_sq)
    d_bc_val = isqrt(d_bc_sq) if d_bc_is_int else math.sqrt(d_bc_sq)
    d_s_val = isqrt(d_s_sq) if d_s_is_int else math.sqrt(d_s_sq)

    # Residual errors (0 if integer, else fractional part)
    def residual(sq_val, is_int):
        if is_int:
            return 0.0
        v = math.sqrt(sq_val)
        frac = v - math.floor(v)
        return min(frac, 1.0 - frac)

    is_euler = d_ab_is_int and d_ac_is_int and d_bc_is_int
    is_perfect = is_euler and d_s_is_int

    values = {
        "a": {"value": a, "is_integer": True, "residual": 0.0},
        "b": {"value": b, "is_integer": True, "residual": 0.0},
        "c": {"value": c, "is_integer": True, "residual": 0.0},
        "d_ab": {
            "value": d_ab_val,
            "squared": d_ab_sq,
            "is_integer": d_ab_is_int,
            "residual": residual(d_ab_sq, d_ab_is_int),
        },
        "d_ac": {
            "value": d_ac_val,
            "squared": d_ac_sq,
            "is_integer": d_ac_is_int,
            "residual": residual(d_ac_sq, d_ac_is_int),
        },
        "d_bc": {
            "value": d_bc_val,
            "squared": d_bc_sq,
            "is_integer": d_bc_is_int,
            "residual": residual(d_bc_sq, d_bc_is_int),
        },
        "d_s": {
            "value": d_s_val,
            "squared": d_s_sq,
            "is_integer": d_s_is_int,
            "residual": residual(d_s_sq, d_s_is_int),
        },
    }

    int_count = 3 + sum([d_ab_is_int, d_ac_is_int, d_bc_is_int, d_s_is_int])

    summary = (
        f"Cuboid({a}, {b}, {c}): "
        f"{int_count}/7 integers. "
        f"{'EULER BRICK' if is_euler else 'Not Euler brick'}. "
        f"{'PERFECT CUBOID!' if is_perfect else 'Not perfect cuboid.'}"
    )

    return {
        "edges": [a, b, c],
        "values": values,
        "is_euler_brick": is_euler,
        "is_perfect_cuboid": is_perfect,
        "integer_count": int_count,
        "summary": summary,
    }


def batch_verify(candidates: list) -> list:
    """Verify a list of (a, b, c) triples.

    Args:
        candidates: List of (a, b, c) tuples.

    Returns:
        List of verification reports.
    """
    return [verify_cuboid(a, b, c) for a, b, c in candidates]


if __name__ == "__main__":
    # Demo verification of known Euler bricks
    known_euler_bricks = [
        (44, 117, 240),
        (240, 252, 275),
        (85, 132, 720),
        (140, 480, 693),
        (160, 231, 792),
    ]

    print("Verification of known Euler bricks:")
    print("=" * 60)
    for a, b, c in known_euler_bricks:
        report = verify_cuboid(a, b, c)
        print(report["summary"])
        if report["is_euler_brick"]:
            sd = report["values"]["d_s"]
            print(f"  Space diagonal: {sd['value']:.10f} (residual: {sd['residual']:.10f})")
    print()
