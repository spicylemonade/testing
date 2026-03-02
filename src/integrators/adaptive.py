"""Adaptive timestep wrapper for symplectic integrators.

Detects close encounters between bodies and reduces the timestep
to maintain accuracy, restoring it when the encounter resolves.

Reference: Aarseth (2003), Rein & Spiegel (2014)
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def _min_pairwise_distance(positions: np.ndarray) -> float:
    """Compute the minimum pairwise distance between bodies.

    Args:
        positions: (N, 2) position array.

    Returns:
        Minimum pairwise distance. Returns inf for N < 2.
    """
    n = len(positions)
    if n < 2:
        return float("inf")

    diff = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    dist_sq = np.sum(diff ** 2, axis=2)
    # Set diagonal to inf to ignore self-distances
    np.fill_diagonal(dist_sq, float("inf"))
    return np.sqrt(np.min(dist_sq))


def step_adaptive(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    force_fn: Callable,
    dt_base: float,
    base_integrator: Callable,
    accelerations: np.ndarray | None = None,
    threshold: float = 0.1,
    min_factor: float = 0.1,
    reference_dist: float = 1.0,
    **force_kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Perform one adaptive timestep using close-encounter detection.

    Reduces dt when bodies approach within threshold * reference_dist,
    with dt proportional to the encounter distance. Restores dt when
    bodies separate.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.
        force_fn: Force computation callable.
        dt_base: Base (maximum) timestep.
        base_integrator: Step function (e.g., step_leapfrog, step_yoshida).
        accelerations: Optional previous accelerations.
        threshold: Distance ratio triggering dt reduction.
        min_factor: Minimum dt scaling factor.
        reference_dist: Reference distance for normalization.
        **force_kwargs: Additional args for force_fn.

    Returns:
        Tuple of (new_positions, new_velocities, new_accelerations, actual_dt).
    """
    d_min = _min_pairwise_distance(positions)

    # Compute adaptive timestep
    ratio = d_min / reference_dist
    if ratio < threshold:
        factor = max(min_factor, ratio / threshold)
    else:
        factor = 1.0

    actual_dt = dt_base * factor

    # Use the base integrator
    if accelerations is not None:
        new_pos, new_vel, new_acc = base_integrator(
            masses, positions, velocities, force_fn, actual_dt,
            accelerations=accelerations, **force_kwargs,
        )
    else:
        new_pos, new_vel, new_acc = base_integrator(
            masses, positions, velocities, force_fn, actual_dt,
            **force_kwargs,
        )

    return new_pos, new_vel, new_acc, actual_dt


def run_adaptive(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    force_fn: Callable,
    dt_base: float,
    t_end: float,
    base_integrator: Callable,
    threshold: float = 0.1,
    min_factor: float = 0.1,
    reference_dist: float = 1.0,
    **force_kwargs,
) -> dict:
    """Run simulation with adaptive timestep until t_end.

    Returns dict with trajectory, timesteps, and total step count.
    """
    pos = positions.copy()
    vel = velocities.copy()
    acc = force_fn(masses, pos, **force_kwargs)

    t = 0.0
    step_count = 0
    dt_history = []

    while t < t_end:
        remaining = t_end - t
        pos, vel, acc, actual_dt = step_adaptive(
            masses, pos, vel, force_fn,
            min(dt_base, remaining),
            base_integrator,
            accelerations=acc,
            threshold=threshold,
            min_factor=min_factor,
            reference_dist=reference_dist,
            **force_kwargs,
        )
        t += actual_dt
        step_count += 1
        dt_history.append(actual_dt)

    return {
        "positions": pos,
        "velocities": vel,
        "accelerations": acc,
        "t_final": t,
        "step_count": step_count,
        "dt_history": dt_history,
    }
