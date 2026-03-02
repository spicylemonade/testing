"""Tests for Barnes-Hut tree code (item_012)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.forces.brute_force import compute_forces_brute
from src.forces.barnes_hut import (
    build_quadtree,
    compute_forces_barnes_hut,
    QuadTreeNode,
)


class TestQuadTree:
    """Tests for quadtree construction."""

    def test_four_body_tree_structure(self):
        """Four bodies in known positions create correct tree structure."""
        masses = np.array([1.0, 1.0, 1.0, 1.0])
        positions = np.array([
            [-1.0, 1.0],   # NW
            [1.0, 1.0],    # NE
            [-1.0, -1.0],  # SW
            [1.0, -1.0],   # SE
        ])

        root = build_quadtree(masses, positions)

        # Root should be an internal node with all 4 children populated
        assert not root.is_leaf()
        assert root.mass == pytest.approx(4.0)
        # Center of mass should be at origin
        np.testing.assert_array_almost_equal(root.com, [0.0, 0.0])

    def test_single_body_tree(self):
        """Single body creates a leaf node."""
        masses = np.array([5.0])
        positions = np.array([[3.0, 4.0]])

        root = build_quadtree(masses, positions)
        assert root.is_leaf()
        assert root.mass == pytest.approx(5.0)
        assert root.body_index == 0

    def test_tree_total_mass(self):
        """Root node mass equals sum of all body masses."""
        rng = np.random.default_rng(42)
        n = 50
        masses = rng.uniform(0.1, 2.0, n)
        positions = rng.uniform(-10, 10, (n, 2))

        root = build_quadtree(masses, positions)
        assert root.mass == pytest.approx(np.sum(masses), rel=1e-10)


class TestBarnesHutForce:
    """Tests for Barnes-Hut force computation."""

    def test_accuracy_vs_brute_force(self):
        """Barnes-Hut with theta=0.5 matches brute-force within 1% for N=100."""
        rng = np.random.default_rng(42)
        n = 100
        masses = rng.uniform(0.5, 2.0, n)
        positions = rng.uniform(-5, 5, (n, 2))

        acc_brute = compute_forces_brute(masses, positions, G=1.0, epsilon=0.1)
        acc_bh = compute_forces_barnes_hut(
            masses, positions, G=1.0, epsilon=0.1, theta=0.5
        )

        # Relative force error per body
        force_mag_brute = np.sqrt(np.sum(acc_brute ** 2, axis=1))
        diff = np.sqrt(np.sum((acc_bh - acc_brute) ** 2, axis=1))

        # Ignore bodies with near-zero force
        mask = force_mag_brute > 1e-10
        rel_errors = diff[mask] / force_mag_brute[mask]

        max_rel_error = np.max(rel_errors)
        assert max_rel_error < 0.01, f"Max relative error {max_rel_error:.4f} exceeds 1%"

    def test_convergence_to_brute_force(self):
        """As theta -> 0, Barnes-Hut converges to brute-force."""
        rng = np.random.default_rng(42)
        n = 20
        masses = rng.uniform(0.5, 2.0, n)
        positions = rng.uniform(-5, 5, (n, 2))

        acc_brute = compute_forces_brute(masses, positions, G=1.0, epsilon=0.1)
        acc_bh = compute_forces_barnes_hut(
            masses, positions, G=1.0, epsilon=0.1, theta=0.01
        )

        np.testing.assert_array_almost_equal(acc_bh, acc_brute, decimal=4)

    def test_two_body_force(self):
        """Barnes-Hut reproduces exact two-body force."""
        masses = np.array([1.0, 2.0])
        positions = np.array([[0.0, 0.0], [3.0, 0.0]])

        acc_brute = compute_forces_brute(masses, positions, G=1.0, epsilon=0.0)
        acc_bh = compute_forces_barnes_hut(
            masses, positions, G=1.0, epsilon=0.0, theta=0.5
        )

        np.testing.assert_array_almost_equal(acc_bh, acc_brute, decimal=10)

    def test_empty_system(self):
        """Empty system returns empty array."""
        masses = np.array([])
        positions = np.zeros((0, 2))
        acc = compute_forces_barnes_hut(masses, positions)
        assert acc.shape == (0, 2)

    def test_single_body(self):
        """Single body has zero acceleration."""
        masses = np.array([1.0])
        positions = np.array([[0.0, 0.0]])
        acc = compute_forces_barnes_hut(masses, positions)
        np.testing.assert_array_almost_equal(acc[0], [0.0, 0.0])
