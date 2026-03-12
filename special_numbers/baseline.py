from __future__ import annotations

from typing import Any

import sympy as sp

from special_numbers.recurrence import find_exact_relation
from special_numbers.selectors import SelectorInstance
from special_numbers.slopes import floor_value, get_slope


def _rational_ap_certificate(slope_id: str, selector: SelectorInstance) -> dict[str, Any] | None:
    slope = get_slope(slope_id)
    if selector.family != "arithmetic_progression" or not slope.expr.is_rational:
        return None
    ratio = sp.Rational(slope.expr)
    step = int(selector.metadata["step"])
    if step % ratio.q != 0:
        return None
    return {
        "status": "proved_exact",
        "method": "rational_ap_identity",
        "proof": f"q={ratio.q} divides step={step}, so floor((step*k+offset)*r) is an arithmetic progression and satisfies x_k-2x_(k+1)+x_(k+2)=0.",
        "certified_coefficients": [1, -2, 1],
    }


def _named_quadratic_convergent_certificate(slope_id: str, selector: SelectorInstance) -> dict[str, Any] | None:
    if selector.selector_id != "quadratic_convergent_even":
        return None
    certificates = {
        "phi": ([1, -3, 1], "Every second convergent denominator of phi is a Fibonacci-type selector, and floor(q_{2k} * phi) satisfies x_k - 3 x_(k+1) + x_(k+2) = 0."),
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
    certificate = _rational_ap_certificate(slope_id, selector) or _named_quadratic_convergent_certificate(slope_id, selector)
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
