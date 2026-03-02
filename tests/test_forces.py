"""Tests for the forces module (item_007)."""

import numpy as np
import pytest

from src.bodies import G
from src.forces import compute_forces, compute_forces_vectorized, pairwise_force


class TestPairwiseForce:
    def test_inverse_square_law(self):
        """Force matches F = G*m1*m2/r^2 for r >> eps."""
        pos1 = np.array([0.0, 0.0])
        pos2 = np.array([10.0, 0.0])
        m1, m2 = 1.0, 1.0

        F = pairwise_force(pos1, pos2, m1, m2, eps=0.0)
        r = 10.0
        F_analytical = G * m1 * m2 / r**2

        # Force should be in +x direction
        assert F[0] > 0
        np.testing.assert_allclose(F[0], F_analytical, rtol=0.01)
        np.testing.assert_allclose(F[1], 0.0, atol=1e-15)

    def test_softened_force_finite_at_zero(self):
        """Softened force is finite when bodies are at the same position."""
        pos = np.array([0.0, 0.0])
        F = pairwise_force(pos, pos, 1.0, 1.0, eps=0.1)
        assert np.all(np.isfinite(F))
        # Force should be zero at same position (rij = 0)
        np.testing.assert_allclose(F, 0.0, atol=1e-15)

    def test_softening_reduces_close_force(self):
        """Softening reduces force at close range vs unsoftened."""
        pos1 = np.array([0.0, 0.0])
        pos2 = np.array([0.01, 0.0])

        F_hard = pairwise_force(pos1, pos2, 1.0, 1.0, eps=0.0)
        F_soft = pairwise_force(pos1, pos2, 1.0, 1.0, eps=0.1)

        assert np.linalg.norm(F_soft) < np.linalg.norm(F_hard)


class TestComputeForces:
    def test_newtons_third_law(self):
        """F_ij = -F_ji: forces are equal and opposite."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        mass = np.array([1.0, 2.0])

        acc = compute_forces(pos, mass, eps=0.01)

        # m1*a1 should equal -m2*a2 (Newton's third law)
        F1 = mass[0] * acc[0]
        F2 = mass[1] * acc[1]
        np.testing.assert_allclose(F1, -F2, atol=1e-14)

    def test_two_body_analytical(self):
        """Two-body force matches analytical F=Gm1m2/r^2 within 1% for r >> eps."""
        r = 5.0
        pos = np.array([[0.0, 0.0], [r, 0.0]])
        mass = np.array([3.0, 4.0])
        eps = 0.01

        acc = compute_forces(pos, mass, eps=eps)

        # Analytical acceleration on body 0
        r_soft = np.sqrt(r**2 + eps**2)
        a_analytical = G * mass[1] * r / r_soft**3
        np.testing.assert_allclose(acc[0, 0], a_analytical, rtol=0.01)

    def test_vectorized_matches_loop(self):
        """Vectorized computation matches loop-based computation."""
        rng = np.random.default_rng(42)
        n = 20
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)

        acc_loop = compute_forces(pos, mass, eps=0.05)
        acc_vec = compute_forces_vectorized(pos, mass, eps=0.05)

        np.testing.assert_allclose(acc_loop, acc_vec, rtol=1e-10)

    def test_three_body_conservation(self):
        """Total force (sum of F=ma) is zero for an isolated system."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.866]])
        mass = np.array([1.0, 1.0, 1.0])

        acc = compute_forces(pos, mass, eps=0.01)
        total_force = np.sum(mass[:, np.newaxis] * acc, axis=0)
        np.testing.assert_allclose(total_force, 0.0, atol=1e-14)

    def test_single_body_zero_force(self):
        """A single body has zero acceleration."""
        pos = np.array([[1.0, 2.0]])
        mass = np.array([5.0])
        acc = compute_forces(pos, mass, eps=0.01)
        np.testing.assert_allclose(acc, 0.0)
