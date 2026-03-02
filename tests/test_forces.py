"""Tests for brute-force gravitational force computation (item_007)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.forces.brute_force import compute_forces_brute


class TestBruteForce:
    """Tests for O(N^2) direct force computation."""

    def test_two_body_analytical_force(self):
        """Two equal masses at unit separation: known analytical force."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        G = 1.0
        epsilon = 0.0  # No softening for analytical comparison

        acc = compute_forces_brute(masses, positions, G=G, epsilon=epsilon)

        # Force on body 0 from body 1: G*m1*(r1-r0)/|r1-r0|^3
        # = 1.0 * 1.0 * [1,0] / 1.0 = [1, 0]
        expected_acc0 = np.array([1.0, 0.0])
        np.testing.assert_array_almost_equal(acc[0], expected_acc0)

    def test_force_symmetry(self):
        """Newton's third law: F_ij = -F_ji (momentum conservation)."""
        masses = np.array([2.0, 3.0])
        positions = np.array([[0.0, 0.0], [1.0, 1.0]])

        acc = compute_forces_brute(masses, positions, G=1.0, epsilon=0.0)

        # m_0 * a_0 = -m_1 * a_1
        force_0 = masses[0] * acc[0]
        force_1 = masses[1] * acc[1]
        np.testing.assert_array_almost_equal(force_0 + force_1, [0.0, 0.0])

    def test_zero_self_force(self):
        """Self-interaction must be zero (no body exerts force on itself)."""
        masses = np.array([1.0])
        positions = np.array([[5.0, 3.0]])

        acc = compute_forces_brute(masses, positions, G=1.0, epsilon=0.01)
        np.testing.assert_array_almost_equal(acc[0], [0.0, 0.0])

    def test_softening_prevents_singularity(self):
        """With epsilon > 0, coincident bodies produce finite force."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [0.0, 0.0]])  # Same position

        acc = compute_forces_brute(masses, positions, G=1.0, epsilon=0.1)

        # Should be finite (not inf/nan)
        assert np.all(np.isfinite(acc))
        # Both should be zero since diff is zero
        np.testing.assert_array_almost_equal(acc[0], [0.0, 0.0])

    def test_inverse_square_law_scaling(self):
        """Force scales as 1/r^2 (for eps=0)."""
        masses = np.array([1.0, 1.0])

        pos_r1 = np.array([[0.0, 0.0], [1.0, 0.0]])
        pos_r2 = np.array([[0.0, 0.0], [2.0, 0.0]])

        acc_r1 = compute_forces_brute(masses, pos_r1, G=1.0, epsilon=0.0)
        acc_r2 = compute_forces_brute(masses, pos_r2, G=1.0, epsilon=0.0)

        # a(2r) / a(r) should be 1/4
        ratio = np.linalg.norm(acc_r2[0]) / np.linalg.norm(acc_r1[0])
        assert ratio == pytest.approx(0.25, rel=1e-10)

    def test_three_body_superposition(self):
        """Force on body 0 from bodies 1 and 2 is the vector sum."""
        masses = np.array([1.0, 1.0, 1.0])
        positions = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ])

        acc = compute_forces_brute(masses, positions, G=1.0, epsilon=0.0)

        # Force from body 1: [1, 0]
        # Force from body 2: [0, 1]
        # Total on body 0: [1, 1]
        expected = np.array([1.0, 1.0])
        np.testing.assert_array_almost_equal(acc[0], expected)

    def test_configurable_G(self):
        """Changing G scales all forces linearly."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])

        acc_G1 = compute_forces_brute(masses, positions, G=1.0, epsilon=0.0)
        acc_G2 = compute_forces_brute(masses, positions, G=2.0, epsilon=0.0)

        np.testing.assert_array_almost_equal(acc_G2, 2.0 * acc_G1)

    def test_empty_system(self):
        """Empty system returns empty array."""
        masses = np.array([])
        positions = np.zeros((0, 2))
        acc = compute_forces_brute(masses, positions)
        assert acc.shape == (0, 2)
