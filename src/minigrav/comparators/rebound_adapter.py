from __future__ import annotations

from pathlib import Path
import time
from typing import Any

import numpy as np
import rebound

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.io.scenarios import SimulationConfig, load_scenario
from minigrav.core.state import BodyState
from minigrav.verification.reproducibility import terminal_state_fingerprint, trajectory_fingerprint


def run_rebound_scenario(
    config_or_path: SimulationConfig | str | Path,
    sample_every: int = 1,
    integrator: str = "ias15",
    internal_dt: float | None = None,
) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    sim = rebound.Simulation()
    sim.G = config.gravitational_constant
    sim.integrator = integrator
    if internal_dt is not None:
        sim.dt = internal_dt
    for idx, body_id in enumerate(config.initial_state.ids):
        sim.add(
            m=float(config.initial_state.masses[idx]),
            x=float(config.initial_state.positions[idx, 0]),
            y=float(config.initial_state.positions[idx, 1]),
            z=float(config.initial_state.positions[idx, 2]),
            vx=float(config.initial_state.velocities[idx, 0]),
            vy=float(config.initial_state.velocities[idx, 1]),
            vz=float(config.initial_state.velocities[idx, 2]),
            hash=body_id,
        )

    diagnostics = []
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    masses = config.initial_state.masses.copy()
    radii = config.initial_state.radii.copy()
    ids = tuple(config.initial_state.ids)

    def current_state() -> BodyState:
        positions = np.asarray([[p.x, p.y, p.z] for p in sim.particles], dtype=float)
        velocities = np.asarray([[p.vx, p.vy, p.vz] for p in sim.particles], dtype=float)
        return BodyState(ids=ids, masses=masses, radii=radii, positions=positions, velocities=velocities)

    initial_state = current_state()
    initial_force = compute_pairwise_forces(initial_state, force_config)
    initial_snapshot = compute_invariants(initial_state, initial_force)

    sample_steps = list(range(0, config.steps + 1, sample_every))
    if sample_steps[-1] != config.steps:
        sample_steps.append(config.steps)

    start = time.perf_counter()
    for step in sample_steps:
        if step > 0:
            sim.integrate(step * config.dt, exact_finish_time=1)
        state = current_state()
        force_report = compute_pairwise_forces(state, force_config)
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
    runtime_seconds = time.perf_counter() - start

    result = {
        "metadata": {
            "scenario_id": config.scenario_id,
            "dt": config.dt,
            "integrator": f"rebound_{integrator}",
            "runtime_seconds": runtime_seconds,
        },
        "diagnostics": diagnostics,
    }
    result["metadata"]["terminal_state_fingerprint"] = terminal_state_fingerprint(result)
    result["metadata"]["trajectory_fingerprint"] = trajectory_fingerprint(result)
    return result
