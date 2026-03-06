#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REGIME_PATH = ROOT / "results" / "verification" / "close_encounter_regimes.json"
OUTPUT_PATH = Path(__file__).with_name("results.json")


def main() -> int:
    rows = json.loads(REGIME_PATH.read_text())["rows"]
    softened = [row for row in rows if row["mode"] == "resolution_coupled"]
    payload = {
        "concept": "resolution_coupled_softening",
        "source": str(REGIME_PATH.relative_to(ROOT)),
        "safe_dt_values": [row["dt"] for row in softened if row["safe"]],
        "rows": softened,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
