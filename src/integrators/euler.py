"""Symplectic Euler integrator — 1st order, symplectic."""

import numpy as np
from src.bodies import System


def euler_step(system: System, accelerations: np.ndarray, dt: float):
    """Advance system by one symplectic Euler step (in-place).

    v(t+dt) = v(t) + a(t) * dt   (kick)
    x(t+dt) = x(t) + v(t+dt) * dt  (drift using NEW velocity)

    This is a 1st-order symplectic integrator (also called semi-implicit
    Euler or Euler-Cromer). Unlike forward Euler, it preserves a modified
    Hamiltonian and does not exhibit secular energy drift.
    """
    system.velocities += accelerations * dt
    system.positions += system.velocities * dt
