"""Leapfrog (Stormer-Verlet) integrator.

Second-order symplectic, time-reversible integrator using the
Kick-Drift-Kick (KDK) formulation. The workhorse of gravitational
N-body simulation.

Reference: Verlet (1967), Hairer et al. (2006) Chapter I.1
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def step_leapfrog(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    force_fn: Callable,
    dt: float,
    accelerations: np.ndarray | None = None,
    **force_kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform one leapfrog (KDK) step.

    Kick-Drift-Kick form:
        1. Half-kick:  v_{1/2} = v_0 + (dt/2) * a_0
        2. Drift:      x_1     = x_0 + dt * v_{1/2}
        3. Compute a_1 from x_1
        4. Half-kick:  v_1     = v_{1/2} + (dt/2) * a_1

    Requires one force evaluation per step. If accelerations from the
    previous step are provided, reuses them (avoids redundant computation).

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.
        force_fn: Callable(masses, positions, **kwargs) -> (N, 2) accelerations.
        dt: Timestep.
        accelerations: Optional (N, 2) accelerations from previous step.
        **force_kwargs: Additional args passed to force_fn.

    Returns:
        Tuple of (new_positions, new_velocities, new_accelerations).
    """
    if accelerations is None:
        accelerations = force_fn(masses, positions, **force_kwargs)

    # Half-kick
    vel_half = velocities + 0.5 * dt * accelerations

    # Drift
    new_pos = positions + dt * vel_half

    # Compute new accelerations
    new_acc = force_fn(masses, new_pos, **force_kwargs)

    # Half-kick
    new_vel = vel_half + 0.5 * dt * new_acc

    return new_pos, new_vel, new_acc
