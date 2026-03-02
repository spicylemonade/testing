"""Yoshida 4th-order symplectic integrator.

Implements the triple-jump composition method from Yoshida (1990).
Achieves 4th-order accuracy using three leapfrog stages with
specific coefficients.

Reference: Yoshida (1990), Physics Letters A 150, 262-268
"""

from __future__ import annotations

from typing import Callable

import numpy as np

# Yoshida 4th-order coefficients
# w1 = 1 / (2 - 2^(1/3))
# w0 = -2^(1/3) / (2 - 2^(1/3))
# w2 = w1
_CBRT2 = 2.0 ** (1.0 / 3.0)
W1 = 1.0 / (2.0 - _CBRT2)  # ~1.3512
W0 = -_CBRT2 / (2.0 - _CBRT2)  # ~-1.7024
W2 = W1

# Verify: w0 + w1 + w2 = 1
assert abs(W0 + W1 + W2 - 1.0) < 1e-14


def _leapfrog_substep(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    accelerations: np.ndarray,
    force_fn: Callable,
    dt: float,
    **force_kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One leapfrog substep (KDK)."""
    vel_half = velocities + 0.5 * dt * accelerations
    new_pos = positions + dt * vel_half
    new_acc = force_fn(masses, new_pos, **force_kwargs)
    new_vel = vel_half + 0.5 * dt * new_acc
    return new_pos, new_vel, new_acc


def step_yoshida(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    force_fn: Callable,
    dt: float,
    accelerations: np.ndarray | None = None,
    **force_kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform one 4th-order Yoshida step.

    Composition of three leapfrog substeps with Yoshida coefficients:
        Phi(dt) = Phi_leapfrog(w1*dt) o Phi_leapfrog(w0*dt) o Phi_leapfrog(w2*dt)

    Requires 3 force evaluations per step.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.
        force_fn: Callable(masses, positions, **kwargs) -> (N, 2) accelerations.
        dt: Timestep.
        accelerations: Optional (N, 2) from previous step.
        **force_kwargs: Additional args passed to force_fn.

    Returns:
        Tuple of (new_positions, new_velocities, new_accelerations).
    """
    if accelerations is None:
        accelerations = force_fn(masses, positions, **force_kwargs)

    # Stage 1: leapfrog with w1*dt
    pos, vel, acc = _leapfrog_substep(
        masses, positions, velocities, accelerations,
        force_fn, W1 * dt, **force_kwargs,
    )

    # Stage 2: leapfrog with w0*dt
    pos, vel, acc = _leapfrog_substep(
        masses, pos, vel, acc,
        force_fn, W0 * dt, **force_kwargs,
    )

    # Stage 3: leapfrog with w2*dt
    pos, vel, acc = _leapfrog_substep(
        masses, pos, vel, acc,
        force_fn, W2 * dt, **force_kwargs,
    )

    return pos, vel, acc
