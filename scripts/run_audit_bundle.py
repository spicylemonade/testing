#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from minigrav.io.scenarios import load_scenario
from minigrav.runner import run_scenario
from minigrav.verification.convergence import run_dt_halving_series


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios"
OUTPUT_DIR = ROOT / "results" / "audit"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(SCENARIO_DIR.glob("*.json")):
        config = load_scenario(path)
        result = run_scenario(config)
        convergence = run_dt_halving_series(config)
        audit_payload = {
            "metadata": result["metadata"],
            "expected_metrics": result["expected_metrics"],
            "terminal_diagnostics": result["diagnostics"][-1],
            "convergence": convergence,
        }
        out_path = OUTPUT_DIR / f"{config.scenario_id}_audit.json"
        out_path.write_text(json.dumps(audit_payload, indent=2) + "\n")
        print(f"wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
