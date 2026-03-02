"""Symplectic Euler integrator.

First-order symplectic method that updates velocity before position.
Also known as the semi-implicit Euler method.

Reference: Hairer, Lubich & Wanner (2006), Chapter VI
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def step_euler(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    force_fn: Callable,
    dt: float,
    **force_kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform one symplectic Euler step.

    Update order (symplectic):
        1. Compute accelerations from current positions
        2. Update velocities: v += dt * a
        3. Update positions: x += dt * v  (using NEW velocities)

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.
        force_fn: Callable(masses, positions, **kwargs) -> (N, 2) accelerations.
        dt: Timestep.
        **force_kwargs: Additional args passed to force_fn.

    Returns:
        Tuple of (new_positions, new_velocities, accelerations).
    """
    acc = force_fn(masses, positions, **force_kwargs)
    new_vel = velocities + dt * acc
    new_pos = positions + dt * new_vel
    return new_pos, new_vel, acc
