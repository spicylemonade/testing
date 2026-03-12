#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.baseline import evaluate_case
from special_numbers.diagnostics import run_shadow_case
from special_numbers.selectors import (
    arithmetic_progression,
    beta_endpoint_selector,
    fibonacci_indices,
    finite_union,
    ostrowski_selector,
    padovan_indices,
    pell_indices,
    quadratic_convergent_even,
)
from special_numbers.slopes import get_slope


COUNT = 20
FIT_LENGTH = 12
MAX_ORDER = 4
FOLLOW_UP_SLOPES = ["one_plus_sqrt2"]
SELECTOR_MAX_N = 50000


def selector_bank_for_slope(slope_id: str):
    bank = [
        arithmetic_progression("ap_1_0", step=1, offset=0, count=COUNT),
        arithmetic_progression("ap_2_0", step=2, offset=0, count=COUNT),
        arithmetic_progression("ap_3_1", step=3, offset=1, count=COUNT),
        arithmetic_progression("ap_5_2", step=5, offset=2, count=COUNT),
        finite_union("union_mod3_01", modulus=3, residues=[0, 1], count=COUNT),
        finite_union("union_mod5_02", modulus=5, residues=[0, 2], count=COUNT),
        finite_union("union_mod6_013", modulus=6, residues=[0, 1, 3], count=COUNT),
        fibonacci_indices(COUNT),
        pell_indices(COUNT),
        padovan_indices(COUNT),
    ]
    irrational = not bool(get_slope(slope_id).expr.is_rational)
    if irrational:
        bank.extend(
            [
                ostrowski_selector(slope_id, "ost_single_nonzero_digit", COUNT, max_n=SELECTOR_MAX_N),
                ostrowski_selector(slope_id, "ost_suffix_01", COUNT, max_n=SELECTOR_MAX_N),
                ostrowski_selector(slope_id, "ost_suffix_001", COUNT, max_n=SELECTOR_MAX_N),
                quadratic_convergent_even(slope_id, COUNT),
            ]
        )
    return bank


def waiver_rows(slope_id: str):
    slope = get_slope(slope_id)
    waivers = []
    if bool(slope.expr.is_rational):
        for selector_id in ["ost_single_nonzero_digit", "ost_suffix_01", "ost_suffix_001", "quadratic_convergent_even"]:
            waivers.append(
                {
                    "slope_id": slope_id,
                    "slope_label": slope.label,
                    "selector_id": selector_id,
                    "status": "waived",
                    "reason": "selector requires an irrational continued-fraction or Ostrowski base",
                }
            )
    if bool(slope.expr.is_rational):
        waivers.append(
            {
                "slope_id": slope_id,
                "slope_label": slope.label,
                "selector_id": "beta_endpoint_suffix_10",
                "status": "waived",
                "reason": "beta-endpoint construction is only meaningful for irrational slopes",
            }
        )
    return waivers


def evaluate_selector(slope_id: str, selector):
    start = time.perf_counter()
    base = evaluate_case(slope_id, selector, max_order=MAX_ORDER)
    run = run_shadow_case(base, fit_length=FIT_LENGTH, max_order=MAX_ORDER)
    run["runtime_seconds"] = time.perf_counter() - start
    run["status"] = "executed"
    return run


def main() -> None:
    out_dir = ROOT / "results" / "experiments"
    out_dir.mkdir(parents=True, exist_ok=True)

    slope_ids = [
        "rational_2",
        "rational_3_over_2",
        "rational_5_over_3",
        "phi",
        "sqrt2",
        "plastic",
        "salem_quartic",
        "e",
        "half",
        "phi_minus_1",
        *FOLLOW_UP_SLOPES,
    ]

    rows = []
    for slope_id in slope_ids:
        rows.extend(waiver_rows(slope_id))
        for selector in selector_bank_for_slope(slope_id):
            rows.append(evaluate_selector(slope_id, selector))
        if not bool(get_slope(slope_id).expr.is_rational):
            rows.append(evaluate_selector(slope_id, beta_endpoint_selector(slope_id, COUNT, max_n=SELECTOR_MAX_N)))

    aggregate = {
        "executed_cases": sum(1 for row in rows if row["status"] == "executed"),
        "waived_cases": sum(1 for row in rows if row["status"] == "waived"),
        "exact_recurrence_cases": sum(
            1
            for row in rows
            if row["status"] == "executed" and row.get("shadow_probe", {}).get("classification") == "exact_recurrence"
        ),
    }

    payload = {
        "panel": {
            "count_per_selector": COUNT,
            "fit_length": FIT_LENGTH,
            "max_order": MAX_ORDER,
            "follow_up_slopes": FOLLOW_UP_SLOPES,
        },
        "aggregate": aggregate,
        "cases": rows,
    }
    json_path = out_dir / "full_panel_results.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n")

    csv_path = out_dir / "full_panel_summary.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["slope_id", "selector_id", "status", "classification", "reason"])
        for row in rows:
            writer.writerow(
                [
                    row.get("slope_id"),
                    row.get("selector_id"),
                    row.get("status"),
                    row.get("shadow_probe", {}).get("classification") if row.get("status") == "executed" else "",
                    row.get("reason", ""),
                ]
            )

    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
