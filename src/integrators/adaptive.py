"""Adaptive timestep controller for leapfrog integration."""

import numpy as np
from src.bodies import System


def compute_adaptive_dt(system: System, accelerations: np.ndarray,
                        eta: float = 0.1, dt_min: float = 1e-6,
                        dt_max: float = 0.1) -> float:
    """Compute adaptive timestep based on particle dynamics.

    Uses the standard Aarseth criterion:
        dt = eta * min_i( sqrt(epsilon / |a_i|) )

    Combined with a velocity-based CFL criterion:
        dt_v = eta * min_i( epsilon / |v_i| )

    The minimum of both is used, clamped to [dt_min, dt_max].

    Args:
        system: N-body system
        accelerations: current accelerations (N, dim)
        eta: safety factor (smaller = more conservative)
        dt_min: minimum allowed timestep
        dt_max: maximum allowed timestep

    Returns:
        dt: adaptive timestep
    """
    eps = system.epsilon

    # Acceleration criterion: dt_a = sqrt(eps / |a|) per particle
    a_mag = np.linalg.norm(accelerations, axis=1)
    max_a = np.max(a_mag)
    dt_a = np.sqrt(eps / max_a) if max_a > 1e-30 else dt_max

    # Velocity criterion: dt_v = eps / |v| per particle
    v_mag = np.linalg.norm(system.velocities, axis=1)
    max_v = np.max(v_mag)
    dt_v = eps / max_v if max_v > 1e-30 else dt_max

    dt = eta * min(dt_a, dt_v)
    return np.clip(dt, dt_min, dt_max)


def adaptive_leapfrog_step(system: System, accelerations: np.ndarray,
                           force_func, eta: float = 0.1,
                           dt_min: float = 1e-6,
                           dt_max: float = 0.1) -> tuple:
    """One adaptive leapfrog step.

    Returns:
        (new_accelerations, dt_used)
    """
    dt = compute_adaptive_dt(system, accelerations, eta, dt_min, dt_max)

    # Velocity-Verlet with adaptive dt
    system.velocities += 0.5 * accelerations * dt
    system.positions += system.velocities * dt
    new_acc = force_func(system)
    system.velocities += 0.5 * new_acc * dt

    return new_acc, dt
