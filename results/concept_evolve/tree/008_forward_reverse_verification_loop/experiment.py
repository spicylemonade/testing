#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

from minigrav.io.scenarios import load_scenario
from minigrav.verification.roundtrip import roundtrip_error


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_PATH = Path(__file__).with_name("results.json")


def evaluate(scenario_name: str, dt_values: list[float]) -> dict:
    base = load_scenario(ROOT / "scenarios" / scenario_name)
    rows = []
    for dt in dt_values:
        varied = replace(base, dt=dt, steps=int(round(base.duration / dt)), duration=int(round(base.duration / dt)) * dt)
        rows.append({"dt": dt, **roundtrip_error(varied)})
    return {"scenario_id": base.scenario_id, "rows": rows}


def main() -> int:
    payload = {
        "concept": "forward_reverse_verification_loop",
        "evaluations": [
            evaluate("circular_two_body.json", [0.02, 0.01, 0.005]),
            evaluate("star_grazing_two_body.json", [0.04, 0.02, 0.01, 0.005]),
        ],
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
