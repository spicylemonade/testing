from __future__ import annotations

from math import atan2, pi
from pathlib import Path
import time
from typing import Any

import numpy as np

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.integrators import step_leapfrog
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.io.scenarios import SimulationConfig, load_scenario


def _wrap_delta(angle_a: float, angle_b: float) -> float:
    return (angle_b - angle_a + pi) % (2.0 * pi) - pi


def build_angular_sweep_queue(state, dt: float, encounter_radius: float) -> list[tuple[int, int]]:
    intervals = []
    drift_positions = state.positions + dt * state.velocities
    for idx in range(state.n_bodies):
        p0 = state.positions[idx]
        p1 = drift_positions[idx]
        phi0 = atan2(float(p0[1]), float(p0[0]))
        phi1 = phi0 + _wrap_delta(phi0, atan2(float(p1[1]), float(p1[0])))
        radial_scale = max(float(np.linalg.norm(p0[:2])), float(np.linalg.norm(p1[:2])), encounter_radius)
        pad = min(pi, encounter_radius / radial_scale)
        intervals.append(
            {
                "index": idx,
                "start": min(phi0, phi1) - pad,
                "end": max(phi0, phi1) + pad,
                "drift_start": p0,
                "drift_end": p1,
            }
        )

    events = []
    for interval in intervals:
        events.append((interval["start"], 0, interval))
        events.append((interval["end"], 1, interval))
    events.sort(key=lambda item: (item[0], item[1]))

    active = []
    candidates: set[tuple[int, int]] = set()
    for _, event_type, interval in events:
        if event_type == 0:
            for other in active:
                distances = [
                    float(np.linalg.norm(interval["drift_start"] - other["drift_start"])),
                    float(np.linalg.norm(interval["drift_end"] - other["drift_end"])),
                    float(
                        np.linalg.norm(
                            0.5 * (interval["drift_start"] + interval["drift_end"])
                            - 0.5 * (other["drift_start"] + other["drift_end"])
                        )
                    ),
                ]
                if min(distances) < encounter_radius:
                    candidates.add(tuple(sorted((interval["index"], other["index"]))))
            active.append(interval)
        else:
            active = [item for item in active if item["index"] != interval["index"]]

    if not candidates:
        for i in range(state.n_bodies - 1):
            for j in range(i + 1, state.n_bodies):
                midpoint_i = 0.5 * (state.positions[i] + drift_positions[i])
                midpoint_j = 0.5 * (state.positions[j] + drift_positions[j])
                distances = [
                    float(np.linalg.norm(state.positions[i] - state.positions[j])),
                    float(np.linalg.norm(drift_positions[i] - drift_positions[j])),
                    float(np.linalg.norm(midpoint_i - midpoint_j)),
                ]
                if min(distances) < encounter_radius:
                    candidates.add((i, j))
    return sorted(candidates)


def _flatten_state(state) -> np.ndarray:
    return np.concatenate([state.positions.ravel(), state.velocities.ravel()])


def _encounter_step_core(state, dt: float, force_config: ForceConfig, encounter_radius: float, micro_steps: int):
    queue = build_angular_sweep_queue(state, dt, encounter_radius)
    if queue:
        current_state = state.copy()
        current_force = None
        for _ in range(micro_steps):
            current_state, report = step_leapfrog(
                current_state,
                dt / micro_steps,
                force_config,
                start_force=current_force,
            )
            current_force = report.end_force
        end_force = current_force or compute_pairwise_forces(current_state, force_config)
        return current_state, end_force, queue, micro_steps
    next_state, report = step_leapfrog(state, dt, force_config)
    return next_state, report.end_force, queue, 1


def _one_step_roundtrip_error(state, dt: float, force_config: ForceConfig, encounter_radius: float, micro_steps: int) -> float:
    forward_state, _, _, _ = _encounter_step_core(state, dt, force_config, encounter_radius, micro_steps)
    recovered_state, _, _, _ = _encounter_step_core(
        forward_state,
        -dt,
        force_config,
        encounter_radius,
        micro_steps,
    )
    baseline_norm = max(float(np.linalg.norm(_flatten_state(state))), 1e-12)
    return float(np.linalg.norm(_flatten_state(recovered_state) - _flatten_state(state)) / baseline_norm)


def run_encounter_aware_scenario(
    config_or_path: SimulationConfig | str | Path,
    encounter_radius: float,
    micro_steps: int = 8,
    sample_every: int = 1,
) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    state = config.initial_state.copy()
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    force_report = compute_pairwise_forces(state, force_config)
    initial_snapshot = compute_invariants(state, force_report)

    diagnostics = []
    last_queue = []
    last_roundtrip = 0.0
    last_microsteps = 1
    encounter_steps = 0
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
                    "encounter_queue_size": len(last_queue),
                    "encounter_pairs": [list(pair) for pair in last_queue],
                    "encounter_roundtrip_relative_error": last_roundtrip,
                    "microstep_count": last_microsteps,
                }
            )
        if step == config.steps:
            break
        state, force_report, last_queue, last_microsteps = _encounter_step_core(
            state,
            config.dt,
            force_config,
            encounter_radius,
            micro_steps,
        )
        last_roundtrip = _one_step_roundtrip_error(state, config.dt, force_config, encounter_radius, micro_steps)
        if last_queue:
            encounter_steps += 1
    runtime_seconds = time.perf_counter() - start

    return {
        "metadata": {
            "scenario_id": config.scenario_id,
            "dt": config.dt,
            "integrator": "encounter_microstep_leapfrog",
            "encounter_radius": encounter_radius,
            "micro_steps": micro_steps,
            "encounter_steps": encounter_steps,
            "runtime_seconds": runtime_seconds,
        },
        "diagnostics": diagnostics,
    }
