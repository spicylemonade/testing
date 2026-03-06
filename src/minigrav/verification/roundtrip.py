from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.integrators import step_leapfrog
from minigrav.io.scenarios import SimulationConfig, load_scenario


def _integrate(config: SimulationConfig, *, dt: float, steps: int):
    state = config.initial_state.copy()
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    force = compute_pairwise_forces(state, force_config)
    for _ in range(steps):
        state, report = step_leapfrog(state, dt, force_config, start_force=force)
        force = report.end_force
    return state


def _flatten_state(state) -> np.ndarray:
    return np.concatenate([state.positions.ravel(), state.velocities.ravel()])


def roundtrip_error(config_or_path: SimulationConfig | str | Path, horizon_steps: int | None = None) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    steps = config.steps if horizon_steps is None else int(horizon_steps)
    forward_state = _integrate(config, dt=config.dt, steps=steps)
    reverse_config = SimulationConfig(
        scenario_id=config.scenario_id,
        description=config.description,
        unit_system=config.unit_system,
        seed=config.seed,
        gravitational_constant=config.gravitational_constant,
        duration=steps * abs(config.dt),
        dt=abs(config.dt),
        steps=steps,
        expected_metrics=config.expected_metrics,
        benchmark_tags=config.benchmark_tags,
        initial_state=forward_state,
    )
    recovered_state = _integrate(reverse_config, dt=-config.dt, steps=steps)

    initial_vector = _flatten_state(config.initial_state)
    recovered_vector = _flatten_state(recovered_state)
    absolute_error = float(np.linalg.norm(recovered_vector - initial_vector))
    baseline_norm = max(float(np.linalg.norm(initial_vector)), 1e-12)
    relative_error = absolute_error / baseline_norm
    position_error = float(np.linalg.norm(recovered_state.positions - config.initial_state.positions))
    velocity_error = float(np.linalg.norm(recovered_state.velocities - config.initial_state.velocities))

    return {
        "horizon_steps": steps,
        "horizon_time": steps * config.dt,
        "absolute_state_error": absolute_error,
        "relative_state_error": relative_error,
        "position_error": position_error,
        "velocity_error": velocity_error,
    }
