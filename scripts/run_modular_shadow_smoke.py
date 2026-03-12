#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.baseline import evaluate_case
from special_numbers.diagnostics import run_shadow_case
from special_numbers.selectors import smoke_selector_bank


def main() -> None:
    results_dir = ROOT / "results" / "baseline"
    results_dir.mkdir(parents=True, exist_ok=True)

    selectors = smoke_selector_bank(count=24)
    base_runs = [
        evaluate_case("rational_3_over_2", selectors["ap_2_0"]),
        evaluate_case("phi", selectors["fib_indices"]),
        evaluate_case("plastic", selectors["union_mod3_01"]),
    ]
    payload = {
        "purpose": "item_008 modular-shadow smoke run",
        "fit_length": 12,
        "runs": [run_shadow_case(run, fit_length=12, max_order=4) for run in base_runs],
    }
    out_path = results_dir / "modular_shadow_smoke.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
