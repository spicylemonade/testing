from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


X = sp.Symbol("x")


@dataclass(frozen=True)
class SlopeSpec:
    slope_id: str
    label: str
    kind: str
    expr: sp.Expr


SLOPES = {
    "rational_2": SlopeSpec("rational_2", "2", "rational", sp.Integer(2)),
    "rational_3_over_2": SlopeSpec("rational_3_over_2", "3/2", "rational", sp.Rational(3, 2)),
    "rational_5_over_3": SlopeSpec("rational_5_over_3", "5/3", "rational", sp.Rational(5, 3)),
    "phi": SlopeSpec("phi", "phi", "quadratic_pisot", (sp.Integer(1) + sp.sqrt(5)) / 2),
    "sqrt2": SlopeSpec("sqrt2", "sqrt(2)", "quadratic_non_pisot", sp.sqrt(2)),
    "plastic": SlopeSpec("plastic", "plastic constant", "cubic_pisot", sp.RootOf(X**3 - X - 1, 0)),
    "salem_quartic": SlopeSpec(
        "salem_quartic",
        "Salem quartic root",
        "salem",
        sp.RootOf(X**4 - X**3 - X**2 - X + 1, 1),
    ),
    "e": SlopeSpec("e", "e", "transcendental", sp.E),
    "half": SlopeSpec("half", "1/2", "rational", sp.Rational(1, 2)),
    "phi_minus_1": SlopeSpec(
        "phi_minus_1",
        "phi - 1",
        "quadratic_pisot_inverse",
        (sp.sqrt(5) - 1) / 2,
    ),
}


def get_slope(slope_id: str) -> SlopeSpec:
    return SLOPES[slope_id]


def floor_value(slope_id: str, n: int) -> int:
    expr = get_slope(slope_id).expr
    return int(sp.floor(sp.Integer(n) * expr))
