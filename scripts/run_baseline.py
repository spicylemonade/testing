#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.harness import SearchConfig, run_harness
from hadamard_ca.search import METHODS, load_sequence_pair


def _load_config(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"baseline config at {path} must be a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Hadamard q/s baseline method")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--seed-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--q-key", default="q")
    parser.add_argument("--s-key", default="s")
    args = parser.parse_args()

    config_payload = _load_config(args.config)
    method_name = str(config_payload["method"])
    method = METHODS[method_name]
    q, s = load_sequence_pair(args.seed_file, q_key=args.q_key, s_key=args.s_key)
    config = SearchConfig(
        method_name=method_name,
        evaluation_budget=int(config_payload["evaluation_budget"]),
        restart_count=int(config_payload.get("restart_count", 1)),
        seed=int(config_payload.get("seed", 0)),
        metadata=dict(config_payload.get("metadata", {})),
    )
    result = run_harness(method, q, s, config)
    result["config"] = config_payload
    result["seed_file"] = str(args.seed_file)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
