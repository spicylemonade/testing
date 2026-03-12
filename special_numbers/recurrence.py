from __future__ import annotations

from math import gcd

import sympy as sp


def _normalize_integer_relation(vector: list[sp.Rational | sp.Integer]) -> list[int]:
    denoms = [int(term.q) if isinstance(term, sp.Rational) else 1 for term in vector]
    lcm = 1
    for denom in denoms:
        lcm = sp.ilcm(lcm, denom)
    numerators = [int(sp.Rational(term) * lcm) for term in vector]
    divisor = 0
    for value in numerators:
        divisor = gcd(divisor, abs(value))
    if divisor == 0:
        return numerators
    numerators = [value // divisor for value in numerators]
    if numerators[-1] < 0:
        numerators = [-value for value in numerators]
    return numerators


def find_exact_relation(sequence: list[int], max_order: int) -> dict[str, object] | None:
    if len(sequence) < 3:
        return None
    for order in range(1, max_order + 1):
        if len(sequence) <= order:
            break
        rows = [sequence[start : start + order + 1] for start in range(len(sequence) - order)]
        matrix = sp.Matrix(rows)
        basis = matrix.nullspace()
        if not basis:
            continue
        for candidate in basis:
            if candidate[-1] == 0:
                continue
            coeffs = _normalize_integer_relation(list(candidate))
            verified = []
            exact = True
            for start in range(len(sequence) - order):
                lhs = sum(coeffs[idx] * sequence[start + idx] for idx in range(order + 1))
                verified.append(start)
                if lhs != 0:
                    exact = False
                    break
            if not exact:
                continue
            return {
                "order": order,
                "coefficients": coeffs,
                "verified_windows": verified,
            }
    return None
