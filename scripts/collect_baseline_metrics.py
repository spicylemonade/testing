#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gravity_sim.scenarios import random_n_body
from gravity_sim.simulator import SimConfig, simulate


def maxrss_mb() -> float:
    # Linux ru_maxrss is in kilobytes.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def run_case(n: int, seed: int, dt: float, steps: int, softening: float) -> dict:
    case = random_n_body(n=n, seed=seed)
    process = psutil.Process(os.getpid())
    rss_before_mb = process.memory_info().rss / (1024.0 * 1024.0)

    t0 = time.perf_counter()
    result = simulate(
        case["positions"],
        case["velocities"],
        case["masses"],
        SimConfig(dt=dt, steps=steps, softening=softening, method="baseline", snapshot_every=1),
    )
    elapsed = time.perf_counter() - t0
    rss_after_mb = process.memory_info().rss / (1024.0 * 1024.0)
    maxrss_after = maxrss_mb()

    first = result["frames"][0]
    last = result["frames"][-1]

    e0 = first["energy"]
    ef = last["energy"]
    l0 = first["angular_momentum"]
    lf = last["angular_momentum"]
    c0 = np.array(first["center_of_mass"], dtype=np.float64)
    cf = np.array(last["center_of_mass"], dtype=np.float64)

    energy_drift_pct = abs(ef - e0) / max(1e-15, abs(e0)) * 100.0
    ang_drift_pct = abs(lf - l0) / max(1e-15, abs(l0)) * 100.0
    com_drift = float(np.linalg.norm(cf - c0))
    mean_step_time_ms = elapsed / steps * 1000.0
    memory_usage_mb = max(rss_before_mb, rss_after_mb, maxrss_after)

    return {
        "n": n,
        "seed": seed,
        "dt": dt,
        "steps": steps,
        "softening": softening,
        "energy_drift_pct": energy_drift_pct,
        "angular_momentum_drift_pct": ang_drift_pct,
        "center_of_mass_drift": com_drift,
        "mean_step_time_ms": mean_step_time_ms,
        "memory_usage_mb": memory_usage_mb,
    }


def write_markdown(path: Path, payload: dict) -> None:
    lines = [
        "# Baseline Metrics",
        "",
        f"Generated at: {payload['generated_at']}",
        f"Commit: {payload['commit']}",
        "",
        "## Definitions",
        "",
        "- Energy drift %: `|E_final-E_0|/|E_0|*100`",
        "- Angular momentum drift %: `|L_final-L_0|/|L_0|*100`",
        "- Center-of-mass drift: `||COM_final - COM_0||`",
        "- Mean step time: wall-clock simulation time divided by step count",
        "- Memory usage: process RSS/peak memory footprint during run (MB)",
        "",
        "## Results",
        "",
        "| N | Energy drift % | Angular momentum drift % | COM drift | Mean step time (ms) | Memory usage (MB) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["results"]:
        lines.append(
            f"| {row['n']} | {row['energy_drift_pct']:.6f} | {row['angular_momentum_drift_pct']:.6f} | {row['center_of_mass_drift']:.6e} | {row['mean_step_time_ms']:.6f} | {row['memory_usage_mb']:.3f} |"
        )

    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    out_json = ROOT / "results" / "baseline" / "metrics.json"
    out_md = ROOT / "results" / "baseline" / "metrics.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)

    commit = os.popen("git rev-parse --short HEAD").read().strip() or "unknown"

    results = [run_case(n=n, seed=42, dt=0.001, steps=500, softening=1e-3) for n in (16, 64, 256)]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": commit,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n")
    write_markdown(out_md, payload)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
