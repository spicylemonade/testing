from __future__ import annotations

from pathlib import Path
from typing import Any

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.integrators import step_leapfrog
from minigrav.diagnostics.invariants import compute_invariants, compute_relative_drift
from minigrav.io.scenarios import SimulationConfig, load_scenario
from minigrav.verification.reproducibility import terminal_state_fingerprint, trajectory_fingerprint
from minigrav.verification.roundtrip import roundtrip_error


def _record_state(time: float, state, snapshot, drift) -> dict[str, Any]:
    return {
        "time": time,
        "positions": state.positions.tolist(),
        "velocities": state.velocities.tolist(),
        "kinetic_energy": snapshot.kinetic_energy,
        "potential_energy": snapshot.potential_energy,
        "total_energy": snapshot.total_energy,
        "angular_momentum": snapshot.angular_momentum.tolist(),
        "angular_momentum_norm": snapshot.angular_momentum_norm,
        "center_of_mass": snapshot.center_of_mass.tolist(),
        "center_of_mass_velocity": snapshot.center_of_mass_velocity.tolist(),
        "energy_rel_drift": drift["energy_rel"],
        "angular_momentum_rel_drift": drift["angular_momentum_rel"],
        "center_of_mass_abs_drift": drift["center_of_mass_abs"],
        "center_of_mass_velocity_abs_drift": drift["center_of_mass_velocity_abs"],
        "min_distance": snapshot.min_distance,
        "min_pair": list(snapshot.min_pair) if snapshot.min_pair else None,
    }


def run_scenario(config_or_path: SimulationConfig | str | Path) -> dict[str, Any]:
    config = load_scenario(config_or_path) if isinstance(config_or_path, (str, Path)) else config_or_path
    state = config.initial_state.copy()
    force_config = ForceConfig(gravitational_constant=config.gravitational_constant)
    force_report = compute_pairwise_forces(state, force_config)
    initial_snapshot = compute_invariants(state, force_report)

    diagnostics: list[dict[str, Any]] = []
    for step in range(config.steps + 1):
        snapshot = compute_invariants(state, force_report)
        drift = compute_relative_drift(snapshot, initial_snapshot)
        diagnostics.append(_record_state(step * config.dt, state, snapshot, drift))
        if step == config.steps:
            break
        state, step_report = step_leapfrog(state, config.dt, force_config, start_force=force_report)
        force_report = step_report.end_force

    result = {
        "metadata": {
            "scenario_id": config.scenario_id,
            "description": config.description,
            "seed": config.seed,
            "unit_system": config.unit_system,
            "gravitational_constant": config.gravitational_constant,
            "dt": config.dt,
            "duration": config.duration,
            "steps": config.steps,
            "integrator": "leapfrog_kdk",
            "force_model": "direct_sum_newtonian",
            "benchmark_tags": list(config.benchmark_tags),
            "body_ids": list(config.initial_state.ids),
            "claim_map": {
                "invariant_tracking": "results/problem_statement.md :: Add audit surfaces that ordinary toy simulators omit: energy and angular-momentum drift, center-of-mass drift, round-trip reversibility diagnostics, timestep-halving convergence, and scenario-level benchmark metadata.",
                "timestep_halving_convergence": "results/problem_statement.md :: Long-horizon invariant drift and timestep-halving behavior are measured rather than assumed.",
                "reproducibility_hooks": "results/problem_statement.md :: The same scenario bundle can be replayed across at least two runtimes or numeric targets with documented tolerances and failure cases.",
                "scenario_benchmark_metadata": "results/problem_statement.md :: Make the benchmark pack part of the contribution, not supporting material."
            },
        },
        "expected_metrics": config.expected_metrics,
        "diagnostics": diagnostics,
    }
    result["metadata"]["roundtrip"] = roundtrip_error(config)
    result["metadata"]["terminal_state_fingerprint"] = terminal_state_fingerprint(result)
    result["metadata"]["trajectory_fingerprint"] = trajectory_fingerprint(result)
    return result
