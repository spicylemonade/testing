from __future__ import annotations

from math import gcd
from typing import Any

import sympy as sp

from special_numbers.recurrence import find_exact_relation
from special_numbers.selectors import SelectorInstance
from special_numbers.slopes import floor_value, get_slope


def _selector_gap_pattern(selector: SelectorInstance) -> list[int] | None:
    if selector.family == "arithmetic_progression":
        return [int(selector.metadata["step"])]
    if selector.family == "finite_union_of_arithmetic_progressions":
        gap_pattern = selector.metadata.get("gap_pattern")
        if isinstance(gap_pattern, list) and gap_pattern:
            return [int(value) for value in gap_pattern]
    return None


def _difference_period_coefficients(period: int) -> list[int]:
    coefficients = [0] * (period + 2)
    coefficients[0] += 1
    coefficients[1] -= 1
    coefficients[period] -= 1
    coefficients[period + 1] += 1
    return coefficients


def _rational_periodic_gap_certificate(slope_id: str, selector: SelectorInstance) -> dict[str, Any] | None:
    slope = get_slope(slope_id)
    if not slope.expr.is_rational:
        return None
    ratio = sp.Rational(slope.expr)
    denominator = int(sp.denom(ratio))
    gap_pattern = _selector_gap_pattern(selector)
    if gap_pattern is None:
        return None
    gap_period = len(gap_pattern)
    period_drift = sum(gap_pattern)
    difference_period = gap_period * denominator // gcd(denominator, period_drift)
    coefficients = _difference_period_coefficients(difference_period)
    return {
        "status": "proved_exact",
        "method": "rational_periodic_gap_identity",
        "proof": (
            f"Write r = p/q with q={denominator}. The selector gaps repeat with period {gap_period} "
            f"and total drift {period_drift}. After {difference_period} selector steps the gap phase repeats "
            f"and the index advances by a multiple of q, so the first-difference sequence Delta b_k is periodic "
            f"with period {difference_period}. Therefore (T^(L+1)-T^L-T+1)b = 0 for L={difference_period}."
        ),
        "certified_coefficients": coefficients,
        "difference_period": difference_period,
    }


def _named_quadratic_convergent_certificate(slope_id: str, selector: SelectorInstance) -> dict[str, Any] | None:
    if selector.selector_id != "quadratic_convergent_even":
        return None
    certificates = {
        "phi": ([1, -3, 1], "Every second convergent denominator of phi is a Fibonacci-type selector, and floor(q_{2k} * phi) satisfies x_k - 3 x_(k+1) + x_(k+2) = 0."),
        "phi_minus_1": ([1, -3, 1], "Every second convergent denominator of phi - 1 is the same Fibonacci selector as for phi, and floor(q_{2k} * (phi - 1)) satisfies x_k - 3 x_(k+1) + x_(k+2) = 0."),
        "one_plus_sqrt2": ([1, -6, 1], "Every second convergent denominator of 1+sqrt(2) is a Pell-type selector, and floor(q_{2k} * (1+sqrt(2))) satisfies x_k - 6 x_(k+1) + x_(k+2) = 0."),
        "sqrt2": ([1, -6, 1], "Every second convergent denominator of sqrt(2) is a Pell-type selector, and floor(q_{2k} * sqrt(2)) satisfies x_k - 6 x_(k+1) + x_(k+2) = 0."),
    }
    if slope_id not in certificates:
        return None
    coeffs, proof = certificates[slope_id]
    return {
        "status": "proved_exact",
        "method": "named_quadratic_convergent_identity",
        "proof": proof,
        "certified_coefficients": coeffs,
    }


def evaluate_case(slope_id: str, selector: SelectorInstance, *, max_order: int = 4) -> dict[str, Any]:
    values = [floor_value(slope_id, n) for n in selector.indices]
    recurrence = find_exact_relation(values, max_order=max_order)
    certificate = _rational_periodic_gap_certificate(slope_id, selector) or _named_quadratic_convergent_certificate(slope_id, selector)
    if certificate is not None:
        classification = "exact_recurrence"
    elif recurrence is not None:
        classification = "finite_prefix_fit_insufficient"
    else:
        classification = "no_exact_relation_detected"
    return {
        "slope_id": slope_id,
        "slope_label": get_slope(slope_id).label,
        "selector_id": selector.selector_id,
        "selector_family": selector.family,
        "indices": selector.indices,
        "values": values,
        "candidate_recurrence": recurrence,
        "certificate": certificate,
        "classification": classification,
    }
