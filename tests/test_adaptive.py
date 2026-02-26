"""Tests for adaptive timestep controller."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force_vec import compute_forces_vectorized
from src.integrators.adaptive import compute_adaptive_dt, adaptive_leapfrog_step


def make_two_body():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1e-6, position=[1.0, 0.0], velocity=[0.0, 1.0]),
    ]
    return System(bodies=bodies, G=1.0, epsilon=0.01)


def test_adaptive_dt_within_bounds():
    sys = make_two_body()
    acc = compute_forces_vectorized(sys)
    dt = compute_adaptive_dt(sys, acc, eta=0.1, dt_min=1e-6, dt_max=0.1)
    assert 1e-6 <= dt <= 0.1


def test_adaptive_dt_clamp_max():
    """With zero acceleration and velocity, dt should clamp to dt_max."""
    bodies = [Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0])]
    sys = System(bodies=bodies, epsilon=0.01)
    acc = np.zeros((1, 2))
    dt = compute_adaptive_dt(sys, acc, eta=1.0, dt_max=0.05)
    assert dt == 0.05


def test_adaptive_leapfrog_step():
    sys = make_two_body()
    acc = compute_forces_vectorized(sys)
    pos_before = sys.positions.copy()
    new_acc, dt_used = adaptive_leapfrog_step(
        sys, acc, compute_forces_vectorized, eta=0.1
    )
    assert dt_used > 0
    assert new_acc.shape == (2, 2)
    # Positions should have changed
    assert not np.allclose(sys.positions, pos_before)


def test_adaptive_conserves_energy():
    """Adaptive leapfrog should conserve energy reasonably."""
    from src.metrics import total_energy
    sys = make_two_body()
    E0 = total_energy(sys)
    acc = compute_forces_vectorized(sys)

    for _ in range(100):
        acc, dt = adaptive_leapfrog_step(sys, acc, compute_forces_vectorized, eta=0.1)

    E_final = total_energy(sys)
    drift = abs((E_final - E0) / E0)
    assert drift < 0.01, f"Adaptive energy drift {drift:.2e} too large"
