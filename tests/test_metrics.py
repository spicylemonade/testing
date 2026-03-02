"""Tests for metrics module (item_009)."""

import numpy as np
import pytest

from src.bodies import G
from src.metrics import (
    kinetic_energy,
    potential_energy,
    potential_energy_vectorized,
    total_energy,
    total_momentum,
    angular_momentum,
    virial_ratio,
)


class TestKineticEnergy:
    def test_formula(self):
        """KE = 1/2 * m * v^2."""
        vel = np.array([[3.0, 4.0]])  # |v| = 5
        mass = np.array([2.0])
        ke = kinetic_energy(vel, mass)
        np.testing.assert_allclose(ke, 0.5 * 2.0 * 25.0)

    def test_zero_velocity(self):
        """Zero velocity gives zero KE."""
        vel = np.zeros((5, 2))
        mass = np.ones(5)
        assert kinetic_energy(vel, mass) == 0.0

    def test_multiple_bodies(self):
        """KE sums correctly over multiple bodies."""
        vel = np.array([[1.0, 0.0], [0.0, 2.0]])
        mass = np.array([1.0, 3.0])
        ke = kinetic_energy(vel, mass)
        expected = 0.5 * 1.0 * 1.0 + 0.5 * 3.0 * 4.0
        np.testing.assert_allclose(ke, expected)


class TestPotentialEnergy:
    def test_two_body(self):
        """PE for two bodies matches analytical formula."""
        r = 2.0
        pos = np.array([[0.0, 0.0], [r, 0.0]])
        mass = np.array([1.0, 1.0])
        eps = 0.0
        pe = potential_energy(pos, mass, eps=eps)
        expected = -G * 1.0 * 1.0 / r
        np.testing.assert_allclose(pe, expected, rtol=1e-10)

    def test_symmetry(self):
        """PE is the same regardless of body ordering."""
        pos = np.array([[0.0, 0.0], [1.0, 1.0]])
        mass = np.array([2.0, 3.0])
        pe1 = potential_energy(pos, mass, eps=0.01)

        pos_rev = pos[::-1]
        mass_rev = mass[::-1]
        pe2 = potential_energy(pos_rev, mass_rev, eps=0.01)
        np.testing.assert_allclose(pe1, pe2, rtol=1e-14)

    def test_vectorized_matches_loop(self):
        """Vectorized PE matches loop-based PE."""
        rng = np.random.default_rng(42)
        pos = rng.uniform(-1, 1, (15, 2))
        mass = rng.uniform(0.1, 2.0, 15)
        pe_loop = potential_energy(pos, mass, eps=0.05)
        pe_vec = potential_energy_vectorized(pos, mass, eps=0.05)
        np.testing.assert_allclose(pe_loop, pe_vec, rtol=1e-10)

    def test_negative_for_bound(self):
        """PE is negative for bound systems."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        mass = np.array([1.0, 1.0])
        pe = potential_energy(pos, mass, eps=0.01)
        assert pe < 0


class TestTotalMomentum:
    def test_zero_for_symmetric(self):
        """Total momentum is zero for symmetric configuration."""
        vel = np.array([[1.0, 0.0], [-1.0, 0.0]])
        mass = np.array([1.0, 1.0])
        p = total_momentum(vel, mass)
        np.testing.assert_allclose(p, 0.0, atol=1e-14)

    def test_correct_sum(self):
        """Total momentum equals sum of individual momenta."""
        vel = np.array([[1.0, 2.0], [3.0, 4.0]])
        mass = np.array([2.0, 3.0])
        p = total_momentum(vel, mass)
        expected = np.array([2.0 * 1.0 + 3.0 * 3.0, 2.0 * 2.0 + 3.0 * 4.0])
        np.testing.assert_allclose(p, expected)


class TestAngularMomentum:
    def test_circular_orbit(self):
        """Circular orbit has non-zero angular momentum."""
        pos = np.array([[1.0, 0.0]])
        vel = np.array([[0.0, 1.0]])
        mass = np.array([1.0])
        L = angular_momentum(pos, vel, mass)
        np.testing.assert_allclose(L, 1.0)  # L = m * r * v = 1*1*1

    def test_radial_motion_zero_L(self):
        """Radial motion has zero angular momentum."""
        pos = np.array([[1.0, 0.0]])
        vel = np.array([[1.0, 0.0]])  # velocity parallel to position
        mass = np.array([1.0])
        L = angular_momentum(pos, vel, mass)
        np.testing.assert_allclose(L, 0.0, atol=1e-15)


class TestConservationInvariant:
    def test_trivial_invariant(self):
        """For stationary bodies, energy, momentum, and angular momentum are trivially conserved."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        vel = np.zeros((2, 2))
        mass = np.array([1.0, 1.0])

        E = total_energy(pos, vel, mass, eps=0.01)
        P = total_momentum(vel, mass)
        L = angular_momentum(pos, vel, mass)

        # These should be exactly reproducible
        E2 = total_energy(pos, vel, mass, eps=0.01)
        P2 = total_momentum(vel, mass)
        L2 = angular_momentum(pos, vel, mass)

        np.testing.assert_allclose(E, E2)
        np.testing.assert_allclose(P, P2)
        np.testing.assert_allclose(L, L2)
