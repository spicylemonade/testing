"""Tests for conservation metrics (item_009)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.metrics import (
    kinetic_energy,
    potential_energy,
    total_energy,
    linear_momentum,
    angular_momentum,
    relative_energy_error,
    relative_momentum_error,
)


class TestKineticEnergy:
    """Tests for kinetic energy computation."""

    def test_stationary_body(self):
        """Stationary body has zero kinetic energy."""
        masses = np.array([5.0])
        velocities = np.array([[0.0, 0.0]])
        assert kinetic_energy(masses, velocities) == 0.0

    def test_known_value(self):
        """T = 0.5 * m * v^2 for single body."""
        masses = np.array([2.0])
        velocities = np.array([[3.0, 4.0]])
        # 0.5 * 2 * (9 + 16) = 25
        assert kinetic_energy(masses, velocities) == pytest.approx(25.0)


class TestPotentialEnergy:
    """Tests for gravitational potential energy."""

    def test_two_body_analytical(self):
        """V = -G*m1*m2 / r for two bodies (eps=0)."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [2.0, 0.0]])
        V = potential_energy(masses, positions, G=1.0, epsilon=0.0)
        assert V == pytest.approx(-0.5)  # -1*1/2

    def test_single_body(self):
        """Single body has zero potential energy."""
        masses = np.array([1.0])
        positions = np.array([[0.0, 0.0]])
        assert potential_energy(masses, positions) == 0.0


class TestLinearMomentum:
    """Tests for linear momentum computation."""

    def test_zero_momentum(self):
        """Equal opposite velocities give zero momentum."""
        masses = np.array([1.0, 1.0])
        velocities = np.array([[1.0, 0.0], [-1.0, 0.0]])
        p = linear_momentum(masses, velocities)
        np.testing.assert_array_almost_equal(p, [0.0, 0.0])

    def test_known_momentum(self):
        """p = m*v for single body."""
        masses = np.array([3.0])
        velocities = np.array([[2.0, -1.0]])
        p = linear_momentum(masses, velocities)
        np.testing.assert_array_almost_equal(p, [6.0, -3.0])


class TestAngularMomentum:
    """Tests for angular momentum (2D scalar)."""

    def test_circular_orbit(self):
        """Circular orbit at r=1, v=1: L = m*r*v = m."""
        masses = np.array([1.0])
        positions = np.array([[1.0, 0.0]])
        velocities = np.array([[0.0, 1.0]])
        L = angular_momentum(masses, positions, velocities)
        assert L == pytest.approx(1.0)

    def test_radial_motion_zero_angular_momentum(self):
        """Radial motion has zero angular momentum."""
        masses = np.array([1.0])
        positions = np.array([[1.0, 0.0]])
        velocities = np.array([[1.0, 0.0]])  # Radial
        L = angular_momentum(masses, positions, velocities)
        assert L == pytest.approx(0.0)


class TestRelativeErrors:
    """Tests for relative error functions."""

    def test_zero_initial_energy(self):
        """Zero initial energy returns 0."""
        assert relative_energy_error(1.0, 0.0) == 0.0

    def test_relative_energy(self):
        """Known relative error."""
        assert relative_energy_error(-0.99, -1.0) == pytest.approx(0.01)

    def test_momentum_error(self):
        """Known momentum error."""
        p = np.array([1.01, 0.0])
        p0 = np.array([1.0, 0.0])
        assert relative_momentum_error(p, p0) == pytest.approx(0.01)
