#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run_cli(args: list[str]) -> None:
    full_env = os.environ.copy()
    existing = full_env.get("PYTHONPATH", "")
    full_env["PYTHONPATH"] = str(SRC) if not existing else f"{SRC}:{existing}"
    subprocess.run([sys.executable, "-m", "gravity_sim.cli", *args], cwd=ROOT, env=full_env, check=True)


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main() -> int:
    out_dir = ROOT / "results" / "baseline" / "trajectories"
    out_dir.mkdir(parents=True, exist_ok=True)

    two_a = out_dir / "two_body_seed42_run_a.json"
    two_b = out_dir / "two_body_seed42_run_b.json"
    n_a = out_dir / "random_n64_seed42_run_a.json"
    n_b = out_dir / "random_n64_seed42_run_b.json"

    run_cli([
        "run",
        "--method",
        "baseline",
        "--scenario",
        "two_body",
        "--steps",
        "400",
        "--dt",
        "0.002",
        "--seed",
        "42",
        "--out",
        str(two_a),
    ])
    run_cli([
        "run",
        "--method",
        "baseline",
        "--scenario",
        "two_body",
        "--steps",
        "400",
        "--dt",
        "0.002",
        "--seed",
        "42",
        "--out",
        str(two_b),
    ])

    run_cli([
        "run",
        "--method",
        "baseline",
        "--scenario",
        "random",
        "--n",
        "64",
        "--steps",
        "200",
        "--dt",
        "0.001",
        "--seed",
        "42",
        "--out",
        str(n_a),
    ])
    run_cli([
        "run",
        "--method",
        "baseline",
        "--scenario",
        "random",
        "--n",
        "64",
        "--steps",
        "200",
        "--dt",
        "0.001",
        "--seed",
        "42",
        "--out",
        str(n_b),
    ])

    report: dict[str, dict[str, Any]] = {
        "two_body": {
            "run_a": str(two_a),
            "run_b": str(two_b),
            "hash_a": sha256(two_a),
            "hash_b": sha256(two_b),
        },
        "random_n64": {
            "run_a": str(n_a),
            "run_b": str(n_b),
            "hash_a": sha256(n_a),
            "hash_b": sha256(n_b),
        },
    }
    report["two_body"]["deterministic"] = report["two_body"]["hash_a"] == report["two_body"]["hash_b"]
    report["random_n64"]["deterministic"] = report["random_n64"]["hash_a"] == report["random_n64"]["hash_b"]

    report_path = ROOT / "results" / "baseline" / "hash_check.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
