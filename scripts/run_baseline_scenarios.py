#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from minigrav.runner import run_scenario


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios"
OUTPUT_DIR = ROOT / "results" / "baseline"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scenario_paths = sorted(SCENARIO_DIR.glob("*.json"))
    for path in scenario_paths:
        result = run_scenario(path)
        scenario_id = result["metadata"]["scenario_id"]
        out_path = OUTPUT_DIR / f"{scenario_id}.json"
        out_path.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
