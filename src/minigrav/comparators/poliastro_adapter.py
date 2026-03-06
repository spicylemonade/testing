from __future__ import annotations

from pathlib import Path
import time
from typing import Any

from astropy import units as u
import numpy as np
from poliastro.bodies import Body
from poliastro.twobody import Orbit

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.state import BodyState
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.benchmarks.orbits import orbital_elements_from_relative_state
from minigrav.io.scenarios import SimulationConfig, load_scenario


def run_poliastro_two_body(config_or_path: SimulationConfig | str | Path, sample_every: int = 1) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    if config.initial_state.n_bodies != 2:
        raise ValueError("poliastro adapter only supports two-body scenarios")

    relative_position = config.initial_state.positions[1] - config.initial_state.positions[0]
    relative_velocity = config.initial_state.velocities[1] - config.initial_state.velocities[0]
    mu = config.gravitational_constant * float(np.sum(config.initial_state.masses))
    attractor = Body(None, k=mu * u.km**3 / u.s**2, name="MuReference")
    orbit = Orbit.from_vectors(attractor, relative_position * u.km, relative_velocity * u.km / u.s)
    diagnostics = []
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    initial_state = config.initial_state.copy()
    initial_force = compute_pairwise_forces(initial_state, force_config)
    initial_snapshot = compute_invariants(initial_state, initial_force)
    sample_steps = list(range(0, config.steps + 1, sample_every))
    if sample_steps[-1] != config.steps:
        sample_steps.append(config.steps)
    start = time.perf_counter()
    for step in sample_steps:
        propagated = orbit.propagate(step * config.dt * u.s)
        r = propagated.r.to_value(u.km)
        v = propagated.v.to_value(u.km / u.s)
        positions = np.asarray([(-0.5 * r).tolist(), (0.5 * r).tolist()], dtype=float)
        velocities = np.asarray([(-0.5 * v).tolist(), (0.5 * v).tolist()], dtype=float)
        state = BodyState(
            ids=tuple(config.initial_state.ids),
            masses=config.initial_state.masses.copy(),
            radii=config.initial_state.radii.copy(),
            positions=positions,
            velocities=velocities,
        )
        force_report = compute_pairwise_forces(state, force_config)
        snapshot = compute_invariants(state, force_report)
        drift = compute_relative_drift(snapshot, initial_snapshot)
        diagnostics.append(
            {
                "time": step * config.dt,
                "positions": positions.tolist(),
                "velocities": velocities.tolist(),
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
    return {
        "metadata": {
            "scenario_id": config.scenario_id,
            "dt": config.dt,
            "integrator": "poliastro_two_body",
            "runtime_seconds": runtime_seconds,
        },
        "diagnostics": diagnostics,
    }
