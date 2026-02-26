"""Tests for Yoshida 4th-order symplectic integrator."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force_vec import compute_forces_vectorized
from src.integrators.yoshida import yoshida_step, C1, C2, C3, C4, D1, D2, D3
from src.metrics import total_energy


def test_yoshida_coefficients_sum():
    """Drift coefficients should sum to 1 (full step)."""
    assert abs(C1 + C2 + C3 + C4 - 1.0) < 1e-14
    assert abs(D1 + D2 + D3 - 1.0) < 1e-14


def test_yoshida_kepler_energy():
    """Yoshida should conserve energy much better than leapfrog on Kepler orbit."""
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1e-6, position=[1.0, 0.0], velocity=[0.0, 1.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    E0 = total_energy(sys)

    acc = compute_forces_vectorized(sys)
    dt = 0.01
    for _ in range(1000):
        acc = yoshida_step(sys, acc, dt, force_func=compute_forces_vectorized)

    E_final = total_energy(sys)
    drift = abs((E_final - E0) / E0)
    assert drift < 1e-8, f"Yoshida energy drift {drift:.2e} too large"


def test_yoshida_returns_acceleration():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[1.0, 0.0], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    acc = compute_forces_vectorized(sys)
    result = yoshida_step(sys, acc, 0.001, force_func=compute_forces_vectorized)
    assert result.shape == (2, 2)
