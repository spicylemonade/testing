from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .forces import ForceConfig, ForceReport, compute_pairwise_forces
from .state import BodyState


@dataclass
class StepReport:
    start_force: ForceReport
    end_force: ForceReport
    acceleration_evaluations: int


def step_leapfrog(
    state: BodyState,
    dt: float,
    force_config: ForceConfig,
    start_force: ForceReport | None = None,
) -> tuple[BodyState, StepReport]:
    start = start_force or compute_pairwise_forces(state, force_config)
    half_step_velocity = state.velocities + 0.5 * dt * start.accelerations
    drifted_positions = state.positions + dt * half_step_velocity
    drifted_state = state.with_dynamics(drifted_positions, half_step_velocity)
    end = compute_pairwise_forces(drifted_state, force_config)
    completed_velocity = half_step_velocity + 0.5 * dt * end.accelerations
    next_state = state.with_dynamics(drifted_positions, completed_velocity)
    return next_state, StepReport(start_force=start, end_force=end, acceleration_evaluations=2)
