"""Tests for initial condition generators."""

import numpy as np
from src.initial_conditions import kepler_elliptical, figure_eight, plummer_sphere


def test_kepler_elliptical_basic():
    sys = kepler_elliptical(e=0.5)
    assert sys.n == 2
    assert sys.masses[0] == 1.0  # central mass
    # Periapsis distance = a*(1-e) = 0.5
    assert abs(sys.positions[1, 0] - 0.5) < 1e-10
    assert abs(sys.positions[1, 1]) < 1e-10


def test_kepler_circular():
    sys = kepler_elliptical(e=0.0)
    # For circular: r_peri = a = 1.0, v = sqrt(G*M/a) = 1.0
    assert abs(sys.positions[1, 0] - 1.0) < 1e-10
    assert abs(sys.velocities[1, 1] - 1.0) < 1e-10


def test_figure_eight_three_bodies():
    sys = figure_eight()
    assert sys.n == 3
    # All equal masses
    np.testing.assert_allclose(sys.masses, [1.0, 1.0, 1.0])
    # Total momentum should be zero (center of mass frame)
    total_p = np.sum(sys.masses[:, None] * sys.velocities, axis=0)
    np.testing.assert_allclose(total_p, [0.0, 0.0], atol=1e-10)


def test_figure_eight_com_at_origin():
    sys = figure_eight()
    com = np.sum(sys.masses[:, None] * sys.positions, axis=0) / np.sum(sys.masses)
    np.testing.assert_allclose(com, [0.0, 0.0], atol=1e-10)


def test_plummer_sphere():
    sys = plummer_sphere(N=100, seed=42)
    assert sys.n == 100
    assert abs(np.sum(sys.masses) - 1.0) < 1e-10  # total mass = 1.0


def test_plummer_sphere_reproducible():
    sys1 = plummer_sphere(N=50, seed=123)
    sys2 = plummer_sphere(N=50, seed=123)
    np.testing.assert_array_equal(sys1.positions, sys2.positions)
    np.testing.assert_array_equal(sys1.velocities, sys2.velocities)
