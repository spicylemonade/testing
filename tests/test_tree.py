"""Tests for the Barnes-Hut tree module (item_012)."""

import time

import numpy as np
import pytest

from src.tree import (
    build_tree,
    compute_forces_tree,
    tree_depth,
    tree_node_count,
)
from src.forces import compute_forces_vectorized


class TestBuildTree:
    def test_single_body(self):
        """Tree with a single body has depth 1."""
        pos = np.array([[0.5, 0.5]])
        mass = np.array([1.0])
        root = build_tree(pos, mass)
        assert root.is_leaf
        assert root.total_mass == 1.0

    def test_two_bodies(self):
        """Tree with two bodies has correct total mass."""
        pos = np.array([[0.0, 0.0], [1.0, 1.0]])
        mass = np.array([1.0, 2.0])
        root = build_tree(pos, mass)
        np.testing.assert_allclose(root.total_mass, 3.0)

    def test_100_bodies_partition(self):
        """Tree correctly partitions >= 100 bodies."""
        rng = np.random.default_rng(42)
        n = 100
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)

        root = build_tree(pos, mass)

        # Total mass should be preserved
        np.testing.assert_allclose(root.total_mass, np.sum(mass), rtol=1e-10)

        # Tree should have non-trivial depth
        depth = tree_depth(root)
        assert depth >= 2, f"Tree depth {depth} too shallow for 100 bodies"

        # Node count should be reasonable
        n_nodes = tree_node_count(root)
        assert n_nodes >= n, f"Expected at least {n} nodes, got {n_nodes}"

    def test_500_bodies(self):
        """Tree handles 500 bodies correctly."""
        rng = np.random.default_rng(42)
        pos = rng.uniform(-10, 10, (500, 2))
        mass = rng.uniform(0.1, 2.0, 500)
        root = build_tree(pos, mass)
        np.testing.assert_allclose(root.total_mass, np.sum(mass), rtol=1e-10)


class TestComputeForcesTree:
    def test_force_error_theta_05(self):
        """Force error vs brute-force < 2% for theta=0.5 (typical accuracy)."""
        rng = np.random.default_rng(42)
        n = 100
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)
        eps = 0.05

        acc_bf = compute_forces_vectorized(pos, mass, eps=eps)
        acc_bh = compute_forces_tree(pos, mass, theta=0.5, eps=eps)

        # RMS relative error
        force_mag_bf = np.sqrt(np.sum(acc_bf**2, axis=1))
        error_mag = np.sqrt(np.sum((acc_bh - acc_bf)**2, axis=1))
        # Avoid division by zero
        mask = force_mag_bf > 1e-10
        rel_errors = error_mag[mask] / force_mag_bf[mask]
        rms_error = np.sqrt(np.mean(rel_errors**2))

        # theta=0.5 gives ~1-2% RMS error for random distributions
        assert rms_error < 0.02, f"RMS relative force error {rms_error:.4f} exceeds 2%"

    def test_force_error_theta_03(self):
        """Force error vs brute-force < 1% for theta=0.3 (tighter criterion)."""
        rng = np.random.default_rng(42)
        n = 100
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)
        eps = 0.05

        acc_bf = compute_forces_vectorized(pos, mass, eps=eps)
        acc_bh = compute_forces_tree(pos, mass, theta=0.3, eps=eps)

        force_mag_bf = np.sqrt(np.sum(acc_bf**2, axis=1))
        error_mag = np.sqrt(np.sum((acc_bh - acc_bf)**2, axis=1))
        mask = force_mag_bf > 1e-10
        rel_errors = error_mag[mask] / force_mag_bf[mask]
        rms_error = np.sqrt(np.mean(rel_errors**2))

        assert rms_error < 0.01, f"RMS relative force error {rms_error:.4f} exceeds 1%"

    def test_theta_zero_matches_bruteforce(self):
        """theta=0 should give exact results (tree degenerates to brute-force)."""
        rng = np.random.default_rng(42)
        n = 20
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)
        eps = 0.05

        acc_bf = compute_forces_vectorized(pos, mass, eps=eps)
        acc_bh = compute_forces_tree(pos, mass, theta=0.0, eps=eps)

        np.testing.assert_allclose(acc_bh, acc_bf, rtol=1e-10)

    def test_single_body_zero_force(self):
        """Single body has zero force."""
        pos = np.array([[0.0, 0.0]])
        mass = np.array([1.0])
        acc = compute_forces_tree(pos, mass, theta=0.5, eps=0.01)
        np.testing.assert_allclose(acc, 0.0)

    def test_two_body_symmetry(self):
        """Two-body forces are equal and opposite."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        mass = np.array([1.0, 1.0])
        acc = compute_forces_tree(pos, mass, theta=0.5, eps=0.01)

        F1 = mass[0] * acc[0]
        F2 = mass[1] * acc[1]
        # Newton's third law may not hold exactly for tree due to asymmetric opening
        # but for two bodies it should be exact
        np.testing.assert_allclose(F1, -F2, atol=1e-10)


class TestScaling:
    def test_nlogn_scaling(self):
        """Demonstrate O(N log N) scaling with timing data."""
        rng = np.random.default_rng(42)
        sizes = [100, 500, 1000, 2000]
        times_list = []

        for n in sizes:
            pos = rng.uniform(-1, 1, (n, 2))
            mass = rng.uniform(0.1, 2.0, n)

            # Warm up
            compute_forces_tree(pos, mass, theta=0.5, eps=0.05)

            start = time.perf_counter()
            for _ in range(3):
                compute_forces_tree(pos, mass, theta=0.5, eps=0.05)
            elapsed = (time.perf_counter() - start) / 3
            times_list.append(elapsed)

        # Check scaling: t(N) ~ N log N
        # Ratio of t(2N)/t(N) should be roughly 2*log(2N)/log(N) ~ 2.x
        # Not 4.0 (which would indicate O(N^2))
        for i in range(len(sizes) - 1):
            ratio = times_list[i + 1] / max(times_list[i], 1e-10)
            n_ratio = sizes[i + 1] / sizes[i]
            # For O(N^2), ratio would be n_ratio^2
            # For O(N log N), ratio would be n_ratio * log(n2)/log(n1) ~ n_ratio * 1.x
            # We verify it's sub-quadratic: ratio < n_ratio^1.7
            max_expected = n_ratio ** 1.7
            assert ratio < max_expected, (
                f"N={sizes[i]}->{sizes[i+1]}: time ratio {ratio:.1f} "
                f"exceeds sub-quadratic bound {max_expected:.1f}"
            )
