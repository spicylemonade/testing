from __future__ import annotations

from pathlib import Path
import time
from typing import Any

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.io.scenarios import SimulationConfig, load_scenario
from minigrav.verification.reproducibility import terminal_state_fingerprint, trajectory_fingerprint


def run_euler_scenario(config_or_path: SimulationConfig | str | Path, sample_every: int = 1) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    state = config.initial_state.copy()
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    force_report = compute_pairwise_forces(state, force_config)
    initial_snapshot = compute_invariants(state, force_report)
    diagnostics = []
    start = time.perf_counter()
    for step in range(config.steps + 1):
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
                }
            )
        if step == config.steps:
            break
        next_positions = state.positions + config.dt * state.velocities
        next_velocities = state.velocities + config.dt * force_report.accelerations
        state = state.with_dynamics(next_positions, next_velocities)
        force_report = compute_pairwise_forces(state, force_config)
    runtime_seconds = time.perf_counter() - start
    result = {
        "metadata": {
            "scenario_id": config.scenario_id,
            "dt": config.dt,
            "integrator": "explicit_euler_classroom",
            "runtime_seconds": runtime_seconds,
        },
        "diagnostics": diagnostics,
    }
    result["metadata"]["terminal_state_fingerprint"] = terminal_state_fingerprint(result)
    result["metadata"]["trajectory_fingerprint"] = trajectory_fingerprint(result)
    return result
