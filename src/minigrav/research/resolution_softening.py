from __future__ import annotations

from pathlib import Path
import time
from typing import Any

import numpy as np

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.integrators import step_leapfrog
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.io.scenarios import SimulationConfig, load_scenario


def estimate_local_cell_size(state) -> float:
    distances = []
    for i in range(state.n_bodies):
        nearest = None
        for j in range(state.n_bodies):
            if i == j:
                continue
            distance = float(np.linalg.norm(state.positions[i] - state.positions[j]))
            nearest = distance if nearest is None else min(nearest, distance)
        if nearest is not None:
            distances.append(nearest)
    return float(np.median(distances)) if distances else 0.0


def run_resolution_coupled_scenario(
    config_or_path: SimulationConfig | str | Path,
    k_cell: float,
    physical_epsilon: float = 0.0,
    sample_every: int = 1,
) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    state = config.initial_state.copy()
    initial_force = compute_pairwise_forces(state, ForceConfig(config.gravitational_constant, 0.0))
    initial_snapshot = compute_invariants(state, initial_force)

    diagnostics = []
    start = time.perf_counter()
    for step in range(config.steps + 1):
        local_cell_size = estimate_local_cell_size(state)
        effective_epsilon = max(physical_epsilon, k_cell * local_cell_size)
        force_config = ForceConfig(config.gravitational_constant, effective_epsilon)
        force_report = compute_pairwise_forces(state, force_config)
        if step % sample_every == 0 or step == config.steps:
            snapshot = compute_invariants(state, force_report)
            drift = compute_relative_drift(snapshot, initial_snapshot)
            diagnostics.append(
                {
                    "time": step * config.dt,
                    "positions": state.positions.tolist(),
                    "velocities": state.velocities.tolist(),
                    "kinetic_energy": snapshot.kinetic_energy,
                    "potential_energy": snapshot.potential_energy,
                    "total_energy": snapshot.total_energy,
                    "angular_momentum_norm": snapshot.angular_momentum_norm,
                    "energy_rel_drift": drift["energy_rel"],
                    "angular_momentum_rel_drift": drift["angular_momentum_rel"],
                    "center_of_mass_abs_drift": drift["center_of_mass_abs"],
                    "center_of_mass_velocity_abs_drift": drift["center_of_mass_velocity_abs"],
                    "effective_epsilon": effective_epsilon,
                    "local_cell_size": local_cell_size,
                }
            )
        if step == config.steps:
            break
        state, _ = step_leapfrog(state, config.dt, force_config)
    runtime_seconds = time.perf_counter() - start
    return {
        "metadata": {
            "scenario_id": config.scenario_id,
            "dt": config.dt,
            "integrator": "resolution_coupled_leapfrog",
            "k_cell": k_cell,
            "physical_epsilon": physical_epsilon,
            "runtime_seconds": runtime_seconds,
        },
        "diagnostics": diagnostics,
    }
