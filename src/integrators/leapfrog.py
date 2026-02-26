"""Velocity-Verlet (leapfrog) integrator — 2nd order, symplectic."""

import numpy as np
from src.bodies import System


def leapfrog_step(system: System, accelerations: np.ndarray, dt: float,
                  force_func=None) -> np.ndarray:
    """Advance system by one velocity-Verlet step (in-place).

    1. v(t + dt/2) = v(t) + a(t) * dt/2        (half kick)
    2. x(t + dt)   = x(t) + v(t + dt/2) * dt   (drift)
    3. a(t + dt)   = F(x(t + dt)) / m           (force eval)
    4. v(t + dt)   = v(t + dt/2) + a(t+dt)*dt/2 (half kick)

    Args:
        system: the N-body system (modified in place)
        accelerations: current accelerations a(t)
        dt: timestep
        force_func: callable(system) -> accelerations. If None, must
                    be called externally and returned acc used for next step.

    Returns:
        new_accelerations: a(t+dt) if force_func provided, else None
    """
    # Half kick
    system.velocities += 0.5 * accelerations * dt
    # Drift
    system.positions += system.velocities * dt

    if force_func is not None:
        # Force evaluation at new positions
        new_acc = force_func(system)
        # Half kick
        system.velocities += 0.5 * new_acc * dt
        return new_acc
    else:
        # Caller must provide the next acceleration
        system.velocities += 0.5 * accelerations * dt
        return None
