"""Time integration schemes for N-body simulation.

Implements:
  - Forward Euler (1st order, non-symplectic)
  - Leapfrog / Störmer-Verlet (2nd order, symplectic)
  - Yoshida 4th-order (4th order, symplectic, composed from leapfrog)
  - Adaptive leapfrog with acceleration-based time-step control

References:
  - Verlet (1967) for the leapfrog method
  - Yoshida (1990) for higher-order symplectic construction
  - Forest & Ruth (1990) for the equivalent 4th-order scheme
"""

from __future__ import annotations

from typing import Callable, Tuple

import numpy as np

# Type alias for force function: (pos, mass) -> accelerations
ForceFunc = Callable[[np.ndarray, np.ndarray], np.ndarray]


def euler_step(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    dt: float,
    force_fn: ForceFunc,
) -> Tuple[np.ndarray, np.ndarray]:
    """Forward Euler integration step.

    First-order, non-symplectic. Included as baseline for comparison only.
    Shows secular energy drift.

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).
        dt: Time step.
        force_fn: Function computing accelerations from (pos, mass).

    Returns:
        Updated (pos, vel) tuple.
    """
    acc = force_fn(pos, mass)
    new_pos = pos + vel * dt
    new_vel = vel + acc * dt
    return new_pos, new_vel


def leapfrog_step(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    dt: float,
    force_fn: ForceFunc,
) -> Tuple[np.ndarray, np.ndarray]:
    """Leapfrog (kick-drift-kick) integration step.

    Second-order, symplectic, time-reversible. The standard integrator for
    N-body simulations. Energy error is bounded (oscillating) rather than
    drifting secularly.

    Implementation: KDK (kick-drift-kick) variant:
      1. Half-kick:  v_{1/2} = v + a(x) * dt/2
      2. Drift:      x' = x + v_{1/2} * dt
      3. Half-kick:  v' = v_{1/2} + a(x') * dt/2

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).
        dt: Time step.
        force_fn: Function computing accelerations from (pos, mass).

    Returns:
        Updated (pos, vel) tuple.
    """
    acc = force_fn(pos, mass)
    vel_half = vel + acc * (dt / 2.0)
    new_pos = pos + vel_half * dt
    acc_new = force_fn(new_pos, mass)
    new_vel = vel_half + acc_new * (dt / 2.0)
    return new_pos, new_vel


# Yoshida 4th-order coefficients
# w1 = 1 / (2 - 2^{1/3})
# w0 = -2^{1/3} * w1
_CBRT2 = 2.0 ** (1.0 / 3.0)
_W1 = 1.0 / (2.0 - _CBRT2)
_W0 = -_CBRT2 * _W1


def yoshida4_step(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    dt: float,
    force_fn: ForceFunc,
) -> Tuple[np.ndarray, np.ndarray]:
    """Yoshida 4th-order symplectic integration step.

    Composes three leapfrog steps with specific time-step weights that cancel
    the third-order error term:
      Yoshida4(dt) = Leapfrog(w1*dt) . Leapfrog(w0*dt) . Leapfrog(w1*dt)

    Fourth-order accuracy at 3x the cost per step of leapfrog.

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).
        dt: Time step.
        force_fn: Function computing accelerations from (pos, mass).

    Returns:
        Updated (pos, vel) tuple.

    References:
        Yoshida, H. (1990). Construction of higher order symplectic integrators.
        Physics Letters A, 150(5-7), 262-268.
    """
    pos, vel = leapfrog_step(pos, vel, mass, _W1 * dt, force_fn)
    pos, vel = leapfrog_step(pos, vel, mass, _W0 * dt, force_fn)
    pos, vel = leapfrog_step(pos, vel, mass, _W1 * dt, force_fn)
    return pos, vel


def adaptive_leapfrog(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    dt_max: float,
    force_fn: ForceFunc,
    eps: float = 0.01,
    eta: float = 0.01,
) -> Tuple[np.ndarray, np.ndarray, float]:
    """Adaptive leapfrog with acceleration-based time-step control.

    Computes dt = eta * sqrt(eps / |a_max|) where |a_max| is the maximum
    acceleration magnitude. The actual dt used is min(dt_adaptive, dt_max).

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).
        dt_max: Maximum allowed time step.
        force_fn: Function computing accelerations from (pos, mass).
        eps: Softening length (used in criterion).
        eta: Safety parameter (smaller = more conservative).

    Returns:
        Tuple of (new_pos, new_vel, dt_used).
    """
    acc = force_fn(pos, mass)
    a_max = np.max(np.sqrt(np.sum(acc**2, axis=1)))

    if a_max > 0:
        dt = min(eta * np.sqrt(eps / a_max), dt_max)
    else:
        dt = dt_max

    # KDK leapfrog with computed dt
    vel_half = vel + acc * (dt / 2.0)
    new_pos = pos + vel_half * dt
    acc_new = force_fn(new_pos, mass)
    new_vel = vel_half + acc_new * (dt / 2.0)

    return new_pos, new_vel, dt
