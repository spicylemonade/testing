"""Yoshida 4th-order symplectic integrator.

Based on: Yoshida, H. (1990) "Construction of higher order symplectic
integrators." Physics Letters A, 150, 262-268.

The 4th-order integrator composes three leapfrog (2nd-order) sub-steps
with specific coefficients to cancel the leading error terms.
"""

import numpy as np
from src.bodies import System

# Yoshida 4th-order coefficients (from the original paper)
_CBRT2 = 2.0 ** (1.0 / 3.0)
_W0 = -_CBRT2 / (2.0 - _CBRT2)
_W1 = 1.0 / (2.0 - _CBRT2)

# Drift (c) and kick (d) coefficients for the 3-substep scheme
C1 = _W1 / 2.0
C2 = (_W0 + _W1) / 2.0
C3 = C2
C4 = C1

D1 = _W1
D2 = _W0
D3 = _W1


def yoshida_step(system: System, accelerations: np.ndarray, dt: float,
                 force_func=None) -> np.ndarray:
    """Advance system by one 4th-order Yoshida step (in-place).

    Uses 3 force evaluations per step (the kick sub-steps).
    The scheme is: c1*drift, d1*kick, c2*drift, d2*kick, c3*drift, d3*kick, c4*drift

    Args:
        system: N-body system (modified in place)
        accelerations: current accelerations a(t) — only used to match interface,
                       the Yoshida scheme recomputes forces internally
        dt: timestep
        force_func: callable(system) -> accelerations (required)

    Returns:
        final accelerations after the step
    """
    # Sub-step 1: drift c1, kick d1
    system.positions += C1 * dt * system.velocities
    acc1 = force_func(system)
    system.velocities += D1 * dt * acc1

    # Sub-step 2: drift c2, kick d2
    system.positions += C2 * dt * system.velocities
    acc2 = force_func(system)
    system.velocities += D2 * dt * acc2

    # Sub-step 3: drift c3, kick d3
    system.positions += C3 * dt * system.velocities
    acc3 = force_func(system)
    system.velocities += D3 * dt * acc3

    # Final drift c4
    system.positions += C4 * dt * system.velocities

    return acc3  # return last-computed acceleration
