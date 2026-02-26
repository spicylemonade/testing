"""Tests for vectorized brute-force force computation."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force import compute_forces
from src.forces.brute_force_vec import compute_forces_vectorized


def test_vectorized_matches_loop():
    """Vectorized forces should match loop-based to machine precision."""
    np.random.seed(42)
    bodies = [Body(mass=np.random.uniform(0.5, 2.0),
                   position=np.random.randn(2),
                   velocity=[0, 0]) for _ in range(20)]
    sys = System(bodies=bodies, G=1.0, epsilon=0.01)

    acc_loop = compute_forces(sys)
    acc_vec = compute_forces_vectorized(sys)
    np.testing.assert_allclose(acc_vec, acc_loop, rtol=1e-12)


def test_vectorized_two_body():
    """Two-body force should match analytical value."""
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=2.0, position=[3.0, 0.0], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    acc = compute_forces_vectorized(sys)

    # a0 = G * m1 * r / |r|^3 = 1 * 2 * 3 / 27 = 6/27
    expected_a0x = 2.0 * 3.0 / (9.0 + 1e-20) ** 1.5
    assert abs(acc[0, 0] - expected_a0x) / expected_a0x < 1e-6
    # Newton's third: m0*a0 = -m1*a1
    np.testing.assert_allclose(1.0 * acc[0], -2.0 * acc[1], atol=1e-10)


def test_vectorized_zero_self_force():
    """Single body should have zero acceleration."""
    bodies = [Body(mass=5.0, position=[1.0, 2.0], velocity=[0, 0])]
    sys = System(bodies=bodies)
    acc = compute_forces_vectorized(sys)
    np.testing.assert_allclose(acc, 0.0, atol=1e-15)
