#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.baseline import evaluate_case
from special_numbers.beta_numeration import endpoint_indices, greedy_digits
from special_numbers.diagnostics import run_shadow_case
from special_numbers.selectors import SelectorInstance
from special_numbers.slopes import get_slope


PISOT_SLOPES = ["phi", "one_plus_sqrt2", "plastic"]
CONTROL_SLOPES = ["sqrt2", "salem_quartic", "e"]
COUNT = 20
MAX_N = 200000


def random_digit_control(slope_id: str, count: int, max_n: int) -> list[int]:
    rng = random.Random(42)
    pool = list(range(1, max_n + 1))
    rng.shuffle(pool)
    selected = []
    for n in pool:
        digits = greedy_digits(slope_id, n)
        if len(digits) >= 2 and digits[0] == 0 and digits[1] == 1:
            continue
        selected.append(n)
        if len(selected) >= count:
            break
    selected.sort()
    return selected


def run_case(slope_id: str) -> dict[str, object]:
    endpoint = endpoint_indices(slope_id, suffix="10", count=COUNT, max_n=MAX_N)
    endpoint_selector = SelectorInstance("beta_endpoint_suffix_10", "linear_recursive", endpoint, {"slope_id": slope_id, "suffix": "10"})
    random_selector = SelectorInstance("beta_random_control", "linear_recursive", random_digit_control(slope_id, COUNT, MAX_N), {"slope_id": slope_id})
    endpoint_run = run_shadow_case(evaluate_case(slope_id, endpoint_selector), fit_length=12, max_order=4)
    control_run = run_shadow_case(evaluate_case(slope_id, random_selector), fit_length=12, max_order=4)
    return {
        "slope_id": slope_id,
        "label": get_slope(slope_id).label,
        "kind": get_slope(slope_id).kind,
        "endpoint_run": endpoint_run,
        "random_control_run": control_run,
    }


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    payload = {
        "concept": "009_pisot_beta_endpoint_sampler",
        "basis_note": "G_n is implemented as the rounded-power beta basis induced by the named slope; endpoint selectors use the greedy suffix 10 in that basis.",
        "runs": [run_case(slope_id) for slope_id in PISOT_SLOPES + CONTROL_SLOPES],
    }
    out_path = out_dir / "results.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
