#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.baseline import evaluate_case
from special_numbers.diagnostics import run_shadow_case
from special_numbers.metrics import BLOCKER_TAXONOMY, blocker_tags, modulus_consistency_score, selector_complexity, summarize_runs
from special_numbers.selectors import smoke_selector_bank


def main() -> None:
    results_dir = ROOT / "results" / "baseline"
    results_dir.mkdir(parents=True, exist_ok=True)

    selectors = smoke_selector_bank(count=24)
    plan = [
        ("main", "rational_3_over_2", selectors["ap_2_0"]),
        ("adversarial_control", "phi", selectors["fib_indices"]),
        ("adversarial_control", "plastic", selectors["union_mod3_01"]),
        ("adversarial_control", "plastic", selectors["ap_2_0"]),
    ]

    runs = []
    for role, slope_id, selector in plan:
        start = time.perf_counter()
        base = evaluate_case(slope_id, selector)
        run = run_shadow_case(base, fit_length=12, max_order=4)
        runtime = time.perf_counter() - start
        run["case_role"] = role
        run["runtime_seconds"] = runtime
        run["selector_complexity"] = selector_complexity(run)
        run["selector_density_class"] = run.get("shadow_probe", {}).get("density_class")
        run["modulus_consistency_score"] = modulus_consistency_score(run)
        run["blocker_tags"] = blocker_tags(run)
        runs.append(run)

    payload = {
        "purpose": "item_009 metrics smoke run",
        "blocker_taxonomy": BLOCKER_TAXONOMY,
        "aggregate_metrics": summarize_runs(runs),
        "runs": runs,
    }
    out_path = results_dir / "metrics_smoke.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
