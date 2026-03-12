from __future__ import annotations

import sympy as sp

from special_numbers.slopes import get_slope


def rounded_power_basis(slope_id: str, max_terms: int = 18) -> list[int]:
    expr = get_slope(slope_id).expr
    values: list[int] = []
    for power in range(1, max_terms + 1):
        raw = sp.N(expr**power, 80)
        candidate = int(sp.Integer(raw.round()))
        if candidate <= 0:
            continue
        if values and candidate <= values[-1]:
            continue
        values.append(candidate)
    return values


def greedy_digits(slope_id: str, n: int, max_terms: int = 18) -> list[int]:
    basis = rounded_power_basis(slope_id, max_terms=max_terms)
    expr = get_slope(slope_id).expr
    max_digit = int(sp.floor(expr))
    digits = [0] * len(basis)
    remaining = n
    for idx in range(len(basis) - 1, -1, -1):
        weight = basis[idx]
        digit = min(max_digit, remaining // weight)
        digits[idx] = int(digit)
        remaining -= int(digit) * weight
    return digits


def endpoint_indices(slope_id: str, *, suffix: str, count: int, max_n: int) -> list[int]:
    suffix_digits = [int(ch) for ch in suffix][::-1]
    indices: list[int] = []
    for n in range(1, max_n + 1):
        digits = greedy_digits(slope_id, n)
        if len(digits) >= len(suffix_digits) and digits[: len(suffix_digits)] == suffix_digits:
            indices.append(n)
        if len(indices) >= count:
            break
    return indices
