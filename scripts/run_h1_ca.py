#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.h1_ca import defect_syndrome_ca_search, load_h1_seed
from hadamard_ca.harness import SearchConfig, run_harness


def _load_config(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"H1 config at {path} must be a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the H1 defect-syndrome CA on a q/s seed")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--seed-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--q-key", default="q")
    parser.add_argument("--s-key", default="s")
    args = parser.parse_args()

    config_payload = _load_config(args.config)
    q, s = load_h1_seed(args.seed_file, q_key=args.q_key, s_key=args.s_key)
    config = SearchConfig(
        method_name="H1_defect_syndrome_ca_64m",
        evaluation_budget=int(config_payload["evaluation_budget"]),
        restart_count=int(config_payload.get("restart_count", 1)),
        seed=int(config_payload.get("seed", 0)),
        metadata=dict(config_payload.get("metadata", {})),
    )
    result = run_harness(defect_syndrome_ca_search, q, s, config)
    result["config"] = config_payload
    result["seed_file"] = str(args.seed_file)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
