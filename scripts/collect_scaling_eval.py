#!/usr/bin/env python3
from __future__ import annotations

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

from gravity_sim.scenarios import random_n_body
from gravity_sim.simulator import SimConfig, simulate


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def run_case(method: str, n: int, steps: int, dt: float, softening: float, theta: float, seed: int) -> dict:
    case = random_n_body(n=n, seed=seed)
    t0 = time.perf_counter()
    result = simulate(
        case["positions"],
        case["velocities"],
        case["masses"],
        SimConfig(
            dt=dt,
            steps=steps,
            softening=softening,
            method=method,
            snapshot_every=steps,
            theta=theta,
            leaf_size=8,
            bh_min_n=64,
        ),
    )
    elapsed = time.perf_counter() - t0
    frames = result["frames"]
    final_positions = np.array(frames[-1]["positions"], dtype=np.float64)
    return {
        "method": method,
        "n": n,
        "steps": steps,
        "dt": dt,
        "softening": softening,
        "theta": theta,
        "seed": seed,
        "elapsed_s": elapsed,
        "step_time_ms": elapsed / steps * 1000.0,
        "throughput_steps_per_s": steps / elapsed,
        "final_positions": final_positions,
    }


def final_position_error_pct(ref: np.ndarray, approx: np.ndarray) -> float:
    diff = approx - ref
    rms_diff = np.sqrt(np.mean(np.sum(diff * diff, axis=1)))
    rms_ref = np.sqrt(np.mean(np.sum(ref * ref, axis=1)))
    return float(100.0 * rms_diff / max(1e-15, rms_ref))


def main() -> int:
    out = ROOT / "results" / "research" / "scaling_eval.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    seed = 42
    dt = 8e-4
    softening = 1e-3
    n_specs = {
        256: 12,
        512: 8,
        1024: 4,
    }
    theta_values = [0.5, 0.8, 1.2]

    per_n = {}
    tradeoff_points = []

    for n, steps in n_specs.items():
        baseline = run_case(
            method="baseline",
            n=n,
            steps=steps,
            dt=dt,
            softening=softening,
            theta=0.0,
            seed=seed,
        )

        bh_runs = []
        for theta in theta_values:
            bh = run_case(
                method="barnes_hut",
                n=n,
                steps=steps,
                dt=dt,
                softening=softening,
                theta=theta,
                seed=seed,
            )
            error_pct = final_position_error_pct(baseline["final_positions"], bh["final_positions"])
            speedup = baseline["throughput_steps_per_s"] / max(1e-15, bh["throughput_steps_per_s"])
            throughput_improvement_pct = (
                (bh["throughput_steps_per_s"] - baseline["throughput_steps_per_s"])
                / max(1e-15, baseline["throughput_steps_per_s"])
                * 100.0
            )
            point = {
                "n": n,
                "theta": theta,
                "baseline_step_time_ms": baseline["step_time_ms"],
                "barnes_hut_step_time_ms": bh["step_time_ms"],
                "baseline_throughput_steps_per_s": baseline["throughput_steps_per_s"],
                "barnes_hut_throughput_steps_per_s": bh["throughput_steps_per_s"],
                "throughput_improvement_pct": throughput_improvement_pct,
                "speedup_vs_baseline": bh["throughput_steps_per_s"] / max(1e-15, baseline["throughput_steps_per_s"]),
                "final_position_error_pct": error_pct,
            }
            bh_runs.append(point)
            tradeoff_points.append(point)

        best_throughput = max(bh_runs, key=lambda p: p["barnes_hut_throughput_steps_per_s"])
        best_accuracy = min(bh_runs, key=lambda p: p["final_position_error_pct"])
        per_n[str(n)] = {
            "baseline": {
                "step_time_ms": baseline["step_time_ms"],
                "throughput_steps_per_s": baseline["throughput_steps_per_s"],
            },
            "barnes_hut_runs": bh_runs,
            "best_throughput_theta": best_throughput["theta"],
            "best_throughput_improvement_pct": best_throughput["throughput_improvement_pct"],
            "best_accuracy_theta": best_accuracy["theta"],
            "best_accuracy_error_pct": best_accuracy["final_position_error_pct"],
        }

    n_ge_512 = [k for k in per_n.keys() if int(k) >= 512]
    throughput_pass = True
    for n in n_ge_512:
        if per_n[n]["best_throughput_improvement_pct"] <= 0.0:
            throughput_pass = False
            break

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": git_commit(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "config": {
            "seed": seed,
            "dt": dt,
            "softening": softening,
            "n_specs": n_specs,
            "theta_values": theta_values,
        },
        "throughput_requirement": {
            "rule": "best Barnes-Hut throughput improvement must be >0 for every N>=512",
            "n_ge_512": n_ge_512,
            "pass": throughput_pass,
        },
        "per_n": per_n,
        "error_speed_tradeoff_curve": tradeoff_points,
    }

    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
