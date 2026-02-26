"""Tests for energy and momentum conservation metrics."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force import compute_forces
from src.integrators.leapfrog import leapfrog_step
from src.metrics import (
    kinetic_energy, potential_energy, total_energy,
    linear_momentum, angular_momentum,
)


def make_circular_kepler(G=1.0, M=1.0, m=1e-6, r=1.0):
    """2-body circular orbit."""
    v_circ = np.sqrt(G * M / r)
    bodies = [
        Body(mass=M, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=m, position=[r, 0.0], velocity=[0.0, v_circ]),
    ]
    return System(bodies=bodies, G=G, epsilon=1e-10)


def test_kinetic_energy():
    bodies = [
        Body(mass=2.0, position=[0.0, 0.0], velocity=[3.0, 4.0]),
    ]
    sys = System(bodies=bodies)
    # KE = 0.5 * 2.0 * (9 + 16) = 25.0
    assert abs(kinetic_energy(sys) - 25.0) < 1e-10


def test_potential_energy_two_body():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[1.0, 0.0], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    pe = potential_energy(sys)
    # PE ≈ -G*m1*m2/r = -1.0
    assert abs(pe - (-1.0)) < 1e-6


def test_linear_momentum():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[1.0, 0.0]),
        Body(mass=2.0, position=[1.0, 0.0], velocity=[-0.5, 1.0]),
    ]
    sys = System(bodies=bodies)
    p = linear_momentum(sys)
    # p = [1*1 + 2*(-0.5), 1*0 + 2*1] = [0, 2]
    np.testing.assert_allclose(p, [0.0, 2.0])


def test_leapfrog_energy_conservation_100_orbits():
    """Leapfrog should conserve energy to < 0.1% over 100 orbits."""
    sys = make_circular_kepler()
    E0 = total_energy(sys)

    T = 2 * np.pi
    dt = 0.01
    n_steps = int(100 * T / dt)

    acc = compute_forces(sys)
    max_dE = 0.0
    for step in range(n_steps):
        acc = leapfrog_step(sys, acc, dt, force_func=compute_forces)
        if (step + 1) % 1000 == 0:
            E = total_energy(sys)
            dE = abs((E - E0) / E0)
            max_dE = max(max_dE, dE)

    E_final = total_energy(sys)
    final_dE = abs((E_final - E0) / E0)
    assert final_dE < 0.001, f"|dE/E0| = {final_dE:.6e} >= 0.1%"
    assert max_dE < 0.001, f"max |dE/E0| = {max_dE:.6e} >= 0.1%"
