#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.baseline import evaluate_case
from special_numbers.selectors import smoke_selector_bank


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results_dir = root / "results" / "baseline"
    results_dir.mkdir(parents=True, exist_ok=True)

    selectors = smoke_selector_bank(count=16)
    runs = [
        evaluate_case("rational_3_over_2", selectors["ap_2_0"]),
        evaluate_case("rational_5_over_3", selectors["ap_3_1"]),
        evaluate_case("phi", selectors["ap_2_0"]),
        evaluate_case("phi", selectors["fib_indices"]),
        evaluate_case("sqrt2", selectors["union_mod3_01"]),
    ]

    payload = {
        "purpose": "item_007 baseline smoke run",
        "max_order": 4,
        "runs": runs,
    }
    out_path = results_dir / "baseline_smoke.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
