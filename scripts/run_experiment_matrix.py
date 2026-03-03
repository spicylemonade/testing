#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gravity_sim.scenarios import random_n_body, three_body, two_body
from gravity_sim.simulator import SimConfig, simulate


RAW_DIR = ROOT / "results" / "experiments" / "raw"
MANIFEST_PATH = RAW_DIR / "run_manifest.jsonl"


def git_commit_full() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def scenario_state(name: str, n: int, seed: int) -> dict:
    if name == "two_body":
        return two_body(seed=seed)
    if name == "three_body":
        return three_body(seed=seed)
    if name == "random":
        return random_n_body(n=n, seed=seed)
    raise ValueError(name)


def max_energy_drift_pct(frames: list[dict]) -> float:
    e0 = float(frames[0]["energy"])
    denom = max(1e-15, abs(e0))
    return max(abs(float(f["energy"]) - e0) for f in frames) / denom * 100.0


def max_angular_drift_pct(frames: list[dict]) -> float:
    l0 = float(frames[0]["angular_momentum"])
    denom = max(1e-15, abs(l0))
    return max(abs(float(f["angular_momentum"]) - l0) for f in frames) / denom * 100.0


def final_com_drift(frames: list[dict]) -> float:
    c0 = np.array(frames[0]["center_of_mass"], dtype=np.float64)
    cf = np.array(frames[-1]["center_of_mass"], dtype=np.float64)
    return float(np.linalg.norm(cf - c0))


def run_one(
    method: str,
    scenario: str,
    n: int,
    dt: float,
    steps: int,
    softening: float,
    seed: int,
    theta: float,
    leaf_size: int,
    bh_min_n: int,
) -> tuple[dict, dict]:
    state = scenario_state(scenario, n=n, seed=seed)
    config = SimConfig(
        dt=dt,
        steps=steps,
        softening=softening,
        method=method,
        snapshot_every=1,
        theta=theta,
        leaf_size=leaf_size,
        bh_min_n=bh_min_n,
    )

    t0 = time.perf_counter()
    trajectory = simulate(state["positions"], state["velocities"], state["masses"], config)
    elapsed = time.perf_counter() - t0

    frames = trajectory["frames"]
    metrics = {
        "max_energy_drift_pct": max_energy_drift_pct(frames),
        "max_angular_momentum_drift_pct": max_angular_drift_pct(frames),
        "center_of_mass_drift": final_com_drift(frames),
        "runtime_per_step_ms": elapsed / steps * 1000.0,
        "throughput_steps_per_s": steps / elapsed,
    }

    payload = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": method,
            "scenario": scenario,
            "n": n,
            "dt": dt,
            "steps": steps,
            "softening": softening,
            "seed": seed,
            "theta": theta,
            "leaf_size": leaf_size,
            "bh_min_n": bh_min_n,
        },
        "metrics": metrics,
        "trajectory": trajectory,
    }
    return payload, metrics


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    commit_hash = git_commit_full()
    py_version = sys.version.split()[0]
    plat = platform.platform()

    methods = ["baseline", "symplectic", "barnes_hut"]
    scenarios = {
        "two_body": {"n": 2, "dt": 0.002, "steps": 1200, "softening": 1e-4},
        "three_body": {"n": 3, "dt": 0.001, "steps": 1200, "softening": 1e-3},
        "random": {"n": 64, "dt": 0.001, "steps": 240, "softening": 1e-3},
    }
    seeds = [42, 43, 44, 45, 46]

    theta = 0.8
    leaf_size = 8
    bh_min_n = 64

    manifest_lines: list[str] = []
    coverage: dict[str, dict[str, list[int]]] = {m: {s: [] for s in scenarios} for m in methods}

    for method in methods:
        for scenario, spec in scenarios.items():
            for seed in seeds:
                run_id = f"{method}__{scenario}__seed{seed}"
                out_dir = RAW_DIR / method / scenario
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{run_id}.json"

                cmd = (
                    "python3 -m gravity_sim.cli run "
                    f"--method {method} --scenario {scenario} --n {spec['n']} "
                    f"--steps {spec['steps']} --dt {spec['dt']} --seed {seed} "
                    f"--softening {spec['softening']} --theta {theta} --leaf-size {leaf_size} "
                    f"--bh-min-n {bh_min_n} --out {out_path}"
                )

                payload, metrics = run_one(
                    method=method,
                    scenario=scenario,
                    n=spec["n"],
                    dt=spec["dt"],
                    steps=spec["steps"],
                    softening=spec["softening"],
                    seed=seed,
                    theta=theta,
                    leaf_size=leaf_size,
                    bh_min_n=bh_min_n,
                )

                out_path.write_text(json.dumps(payload, indent=2) + "\n")
                artifact_hash = sha256_file(out_path)

                manifest = {
                    "run_id": run_id,
                    "command": cmd,
                    "seed": seed,
                    "method": method,
                    "scenario": scenario,
                    "runtime_environment": {
                        "os": plat,
                        "arch": platform.machine(),
                        "python": py_version,
                        "simulator_version": "gravity_sim_v1",
                    },
                    "commit_hash": commit_hash,
                    "artifact_path": str(out_path.relative_to(ROOT)),
                    "artifact_sha256": artifact_hash,
                    "status": "success",
                    "metrics": metrics,
                }
                manifest_lines.append(json.dumps(manifest))
                coverage[method][scenario].append(seed)

    MANIFEST_PATH.write_text("\n".join(manifest_lines) + "\n")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit_hash": commit_hash,
        "methods": methods,
        "scenarios": list(scenarios.keys()),
        "seeds": seeds,
        "coverage": coverage,
        "total_runs": len(manifest_lines),
    }
    (RAW_DIR / "coverage_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
