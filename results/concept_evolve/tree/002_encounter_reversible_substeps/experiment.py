#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REGIME_PATH = ROOT / "results" / "verification" / "close_encounter_regimes.json"
OUTPUT_PATH = Path(__file__).with_name("results.json")


def main() -> int:
    rows = json.loads(REGIME_PATH.read_text())["rows"]
    direct = {row["dt"]: row for row in rows if row["mode"] == "direct"}
    encounter = {row["dt"]: row for row in rows if row["mode"] == "encounter_microstep"}
    summary = []
    for dt in sorted(encounter):
        summary.append(
            {
                "dt": dt,
                "direct_error": direct[dt]["final_state_rel_error_vs_rebound"],
                "encounter_error": encounter[dt]["final_state_rel_error_vs_rebound"],
                "error_reduction_factor": direct[dt]["final_state_rel_error_vs_rebound"] / max(encounter[dt]["final_state_rel_error_vs_rebound"], 1e-12),
                "direct_safe": direct[dt]["safe"],
                "encounter_safe": encounter[dt]["safe"],
            }
        )
    payload = {
        "concept": "encounter_reversible_substeps",
        "source": str(REGIME_PATH.relative_to(ROOT)),
        "summary": summary,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
