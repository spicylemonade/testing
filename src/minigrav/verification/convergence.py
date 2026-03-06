from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from minigrav.io.scenarios import SimulationConfig, load_scenario
from minigrav.runner import run_scenario


def _final_state_vector(result: dict[str, Any]) -> np.ndarray:
    terminal = result["diagnostics"][-1]
    return np.asarray(terminal["positions"] + terminal["velocities"], dtype=float).ravel()


def run_dt_halving_series(
    config_or_path: SimulationConfig | str | Path,
    levels: int = 3,
) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    runs: list[dict[str, Any]] = []

    for level in range(levels):
        dt = config.dt / (2**level)
        steps = int(round(config.duration / dt))
        varied = replace(config, dt=dt, steps=steps, duration=steps * dt)
        result = run_scenario(varied)
        terminal = result["diagnostics"][-1]
        runs.append(
            {
                "dt": dt,
                "steps": steps,
                "terminal_state_norm": float(np.linalg.norm(_final_state_vector(result))),
                "max_energy_rel_drift": max(row["energy_rel_drift"] for row in result["diagnostics"]),
                "max_angular_momentum_rel_drift": max(
                    row["angular_momentum_rel_drift"] for row in result["diagnostics"]
                ),
                "trajectory_fingerprint": result["metadata"]["trajectory_fingerprint"],
                "terminal_state_fingerprint": result["metadata"]["terminal_state_fingerprint"],
            }
        )

    deltas = []
    for coarse, fine in zip(runs, runs[1:]):
        coarse_norm = max(coarse["terminal_state_norm"], 1e-12)
        deltas.append(
            {
                "from_dt": coarse["dt"],
                "to_dt": fine["dt"],
                "terminal_norm_ratio": fine["terminal_state_norm"] / coarse_norm,
                "energy_drift_ratio": fine["max_energy_rel_drift"]
                / max(coarse["max_energy_rel_drift"], 1e-12),
                "angular_momentum_drift_ratio": fine["max_angular_momentum_rel_drift"]
                / max(coarse["max_angular_momentum_rel_drift"], 1e-12),
            }
        )

    return {
        "scenario_id": config.scenario_id,
        "levels": levels,
        "runs": runs,
        "pairwise_deltas": deltas,
    }
