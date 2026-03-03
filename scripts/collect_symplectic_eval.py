#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gravity_sim.scenarios import random_n_body, three_body, two_body
from gravity_sim.simulator import SimConfig, simulate


ENERGY_IMPROVEMENT_MIN_PCT = 20.0
RUNTIME_RATIO_MAX = 1.5
MIN_SCENARIOS_PASSING = 2
EPS = 1e-15


@dataclass(frozen=True)
class ScenarioSpec:
    label: str
    scenario: str
    n: int
    dt: float
    steps: int
    softening: float


def git_commit() -> str:
    try:
        value = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    return value.strip() or "unknown"


def build_case(spec: ScenarioSpec, seed: int) -> dict:
    if spec.scenario == "two_body":
        return two_body(seed=seed)
    if spec.scenario == "three_body":
        return three_body(seed=seed)
    if spec.scenario == "random":
        return random_n_body(n=spec.n, seed=seed)
    raise ValueError(f"Unsupported scenario: {spec.scenario}")


def max_energy_drift_pct(frames: list[dict]) -> float:
    e0 = float(frames[0]["energy"])
    denom = max(EPS, abs(e0))
    max_abs_delta = 0.0
    for frame in frames:
        e = float(frame["energy"])
        max_abs_delta = max(max_abs_delta, abs(e - e0))
    return max_abs_delta / denom * 100.0


def run_method(spec: ScenarioSpec, method: str, seeds: list[int]) -> dict:
    runs: list[dict] = []
    for seed in seeds:
        case = build_case(spec, seed)
        t0 = time.perf_counter()
        trajectory = simulate(
            case["positions"],
            case["velocities"],
            case["masses"],
            SimConfig(
                dt=spec.dt,
                steps=spec.steps,
                softening=spec.softening,
                method=method,
                snapshot_every=1,
            ),
        )
        elapsed = time.perf_counter() - t0
        energy_drift_pct = max_energy_drift_pct(trajectory["frames"])
        runtime_per_step_ms = elapsed / spec.steps * 1000.0
        runs.append(
            {
                "seed": seed,
                "max_energy_drift_pct": energy_drift_pct,
                "runtime_per_step_ms": runtime_per_step_ms,
            }
        )

    energy_values = [run["max_energy_drift_pct"] for run in runs]
    runtime_values = [run["runtime_per_step_ms"] for run in runs]
    return {
        "runs": runs,
        "median_max_energy_drift_pct": float(median(energy_values)),
        "median_runtime_per_step_ms": float(median(runtime_values)),
    }


def evaluate_scenario(spec: ScenarioSpec, seeds: list[int]) -> dict:
    baseline = run_method(spec, method="baseline", seeds=seeds)
    symplectic = run_method(spec, method="symplectic", seeds=seeds)

    baseline_energy = baseline["median_max_energy_drift_pct"]
    symplectic_energy = symplectic["median_max_energy_drift_pct"]
    baseline_runtime = baseline["median_runtime_per_step_ms"]
    symplectic_runtime = symplectic["median_runtime_per_step_ms"]

    improvement_pct = (baseline_energy - symplectic_energy) / max(EPS, baseline_energy) * 100.0
    runtime_ratio = symplectic_runtime / max(EPS, baseline_runtime)

    energy_improvement_pass = improvement_pct >= ENERGY_IMPROVEMENT_MIN_PCT
    runtime_ratio_pass = runtime_ratio <= RUNTIME_RATIO_MAX
    scenario_pass = energy_improvement_pass and runtime_ratio_pass

    return {
        "scenario": spec.label,
        "config": {
            "scenario": spec.scenario,
            "n": spec.n,
            "dt": spec.dt,
            "steps": spec.steps,
            "softening": spec.softening,
            "seeds": seeds,
        },
        "medians": {
            "baseline_max_energy_drift_pct": baseline_energy,
            "symplectic_max_energy_drift_pct": symplectic_energy,
            "baseline_runtime_per_step_ms": baseline_runtime,
            "symplectic_runtime_per_step_ms": symplectic_runtime,
        },
        "improvement_pct": improvement_pct,
        "runtime_ratio": runtime_ratio,
        "flags": {
            "energy_improvement_pass": energy_improvement_pass,
            "runtime_ratio_pass": runtime_ratio_pass,
            "scenario_pass": scenario_pass,
        },
        "runs": {
            "baseline": baseline["runs"],
            "symplectic": symplectic["runs"],
        },
    }


def evaluate_acceptance(scenarios: list[dict]) -> dict:
    energy_pass_count = sum(1 for row in scenarios if row["flags"]["energy_improvement_pass"])
    runtime_pass_count = sum(1 for row in scenarios if row["flags"]["runtime_ratio_pass"])
    scenario_pass_count = sum(1 for row in scenarios if row["flags"]["scenario_pass"])

    return {
        "thresholds": {
            "energy_improvement_min_pct": ENERGY_IMPROVEMENT_MIN_PCT,
            "runtime_ratio_max": RUNTIME_RATIO_MAX,
            "min_scenarios_passing": MIN_SCENARIOS_PASSING,
        },
        "counts": {
            "scenarios_evaluated": len(scenarios),
            "energy_improvement_pass": energy_pass_count,
            "runtime_ratio_pass": runtime_pass_count,
            "scenario_pass": scenario_pass_count,
        },
        "flags": {
            "energy_requirement_pass": energy_pass_count >= MIN_SCENARIOS_PASSING,
            "runtime_requirement_all_scenarios_pass": runtime_pass_count == len(scenarios),
            "rubric_acceptance_pass": scenario_pass_count >= MIN_SCENARIOS_PASSING,
        },
    }


def main() -> int:
    out_path = ROOT / "results" / "research" / "symplectic_eval.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seeds = [42, 43, 44, 45, 46]
    scenarios = [
        ScenarioSpec(label="two_body", scenario="two_body", n=2, dt=0.002, steps=1200, softening=1e-4),
        ScenarioSpec(label="three_body", scenario="three_body", n=3, dt=0.001, steps=1200, softening=1e-3),
        ScenarioSpec(label="random_n64", scenario="random", n=64, dt=0.001, steps=300, softening=1e-3),
    ]

    scenario_results = [evaluate_scenario(spec, seeds) for spec in scenarios]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": git_commit(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "acceptance": evaluate_acceptance(scenario_results),
        "scenarios": scenario_results,
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
