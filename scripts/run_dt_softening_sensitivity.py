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


def max_energy_drift_pct(frames: list[dict]) -> float:
    e0 = float(frames[0]["energy"])
    denom = max(1e-15, abs(e0))
    return max(abs(float(f["energy"]) - e0) for f in frames) / denom * 100.0


def max_angular_drift_pct(frames: list[dict]) -> float:
    l0 = float(frames[0]["angular_momentum"])
    denom = max(1e-15, abs(l0))
    return max(abs(float(f["angular_momentum"]) - l0) for f in frames) / denom * 100.0


def main() -> int:
    out = ROOT / "results" / "experiments" / "sensitivity_dt_softening.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    dt_values = [0.0005, 0.001, 0.002]
    softening_values = [0.0005, 0.001, 0.002]
    seeds = [42, 43, 44, 45, 46]
    horizon = 0.12
    n = 64

    rows = []
    for dt in dt_values:
        steps = max(1, int(round(horizon / dt)))
        for softening in softening_values:
            for seed in seeds:
                case = random_n_body(n=n, seed=seed)
                t0 = time.perf_counter()
                trajectory = simulate(
                    case["positions"],
                    case["velocities"],
                    case["masses"],
                    SimConfig(
                        dt=dt,
                        steps=steps,
                        softening=softening,
                        method="baseline",
                        snapshot_every=1,
                    ),
                )
                elapsed = time.perf_counter() - t0
                frames = trajectory["frames"]
                rows.append(
                    {
                        "method": "baseline",
                        "scenario": "random",
                        "n": n,
                        "seed": seed,
                        "dt": dt,
                        "softening": softening,
                        "steps": steps,
                        "max_energy_drift_pct": max_energy_drift_pct(frames),
                        "max_angular_momentum_drift_pct": max_angular_drift_pct(frames),
                        "runtime_per_step_ms": elapsed / steps * 1000.0,
                    }
                )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": git_commit(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "horizon": horizon,
        "dt_values": dt_values,
        "softening_values": softening_values,
        "seeds": seeds,
        "rows": rows,
    }
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "output": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
