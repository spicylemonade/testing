"""Tests for gravitational force computation."""

import numpy as np
from src.bodies import Body, System
from src.forces.brute_force import compute_forces


def test_two_body_force():
    """Verify force between two known masses at known distance."""
    # Two unit masses at distance 1.0 apart along x-axis
    # With G=1, epsilon very small: F = G*m2/r^2 = 1.0
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[1.0, 0.0], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    acc = compute_forces(sys)

    # Body 0 should be accelerated toward body 1 (positive x)
    # a = G * m_1 / (r^2 + eps^2)^{3/2} * r ≈ G * m / r^2 for small eps
    r = 1.0
    eps = 1e-10
    expected_a = 1.0 / (r**2 + eps**2)**1.5 * r  # ≈ 1.0
    assert abs(acc[0, 0] - expected_a) / expected_a < 1e-6
    assert abs(acc[0, 1]) < 1e-10  # no y-component

    # Newton's third law: equal and opposite
    np.testing.assert_allclose(acc[0], -acc[1], atol=1e-12)


def test_three_body_symmetry():
    """Three equal masses in equilateral triangle should have symmetric forces."""
    r = 1.0
    bodies = [
        Body(mass=1.0, position=[r, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[-r/2, r*np.sqrt(3)/2], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[-r/2, -r*np.sqrt(3)/2], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    acc = compute_forces(sys)

    # All accelerations should have same magnitude (pointing inward)
    magnitudes = np.linalg.norm(acc, axis=1)
    np.testing.assert_allclose(magnitudes[0], magnitudes[1], rtol=1e-10)
    np.testing.assert_allclose(magnitudes[1], magnitudes[2], rtol=1e-10)


def test_force_with_different_masses():
    """Verify F = G*m2/r^2 for acceleration on body 0 due to body 1."""
    m1, m2 = 3.0, 5.0
    d = 2.0  # distance
    bodies = [
        Body(mass=m1, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=m2, position=[d, 0.0], velocity=[0.0, 0.0]),
    ]
    sys = System(bodies=bodies, G=1.0, epsilon=1e-10)
    acc = compute_forces(sys)

    # Acceleration on body 0: a = G * m2 * d / (d^2 + eps^2)^{3/2}
    eps = 1e-10
    expected = 1.0 * m2 * d / (d**2 + eps**2)**1.5
    rel_err = abs(acc[0, 0] - expected) / expected
    assert rel_err < 1e-6, f"Relative error {rel_err} exceeds 1e-6"
