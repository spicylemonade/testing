"""Tests for Euler and Leapfrog integrators on Kepler 2-body problem."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force import compute_forces
from src.integrators.euler import euler_step
from src.integrators.leapfrog import leapfrog_step


def make_circular_kepler(G=1.0, M=1.0, m=1e-6, r=1.0):
    """Create a 2-body system with a circular orbit.

    Central mass M at origin, test mass m in circular orbit at radius r.
    Circular velocity: v = sqrt(G*M/r)
    Orbital period: T = 2*pi*r / v = 2*pi*sqrt(r^3/(G*M))
    """
    v_circ = np.sqrt(G * M / r)
    bodies = [
        Body(mass=M, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=m, position=[r, 0.0], velocity=[0.0, v_circ]),
    ]
    return System(bodies=bodies, G=G, epsilon=1e-10)


def test_euler_circular_orbit_10_orbits():
    """Forward Euler should complete 10 orbits with < 10% position error."""
    sys = make_circular_kepler()
    r0 = sys.positions[1].copy()

    T = 2 * np.pi  # period for G=M=r=1
    dt = 0.001
    n_steps = int(10 * T / dt)

    for _ in range(n_steps):
        acc = compute_forces(sys)
        euler_step(sys, acc, dt)

    # Check position error after 10 orbits
    r_final = sys.positions[1]
    pos_error = np.linalg.norm(r_final - r0) / np.linalg.norm(r0)
    assert pos_error < 0.10, f"Euler position error {pos_error:.4f} >= 10%"


def test_leapfrog_circular_orbit_10_orbits():
    """Leapfrog should complete 10 orbits with < 1% position error."""
    sys = make_circular_kepler()
    r0 = sys.positions[1].copy()

    T = 2 * np.pi
    dt = 0.001
    n_steps = int(10 * T / dt)

    acc = compute_forces(sys)
    for _ in range(n_steps):
        acc = leapfrog_step(sys, acc, dt, force_func=compute_forces)

    r_final = sys.positions[1]
    pos_error = np.linalg.norm(r_final - r0) / np.linalg.norm(r0)
    assert pos_error < 0.01, f"Leapfrog position error {pos_error:.4f} >= 1%"
