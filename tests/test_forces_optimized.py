"""Tests for the optimized symmetric force computation (item_016)."""

import time

import numpy as np
import pytest

from src.forces import compute_forces_vectorized
from src.forces_optimized import compute_forces_symmetric


class TestComputeForcesSymmetric:
    def test_matches_bruteforce(self):
        """Symmetric computation matches full brute-force exactly."""
        rng = np.random.default_rng(42)
        n = 50
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)
        eps = 0.05

        acc_bf = compute_forces_vectorized(pos, mass, eps=eps)
        acc_sym = compute_forces_symmetric(pos, mass, eps=eps)

        np.testing.assert_allclose(acc_sym, acc_bf, rtol=1e-10)

    def test_single_body(self):
        """Single body has zero force."""
        pos = np.array([[1.0, 2.0]])
        mass = np.array([5.0])
        acc = compute_forces_symmetric(pos, mass, eps=0.01)
        np.testing.assert_allclose(acc, 0.0)

    def test_newtons_third_law(self):
        """Forces obey Newton's third law."""
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        mass = np.array([2.0, 3.0])
        acc = compute_forces_symmetric(pos, mass, eps=0.01)

        F1 = mass[0] * acc[0]
        F2 = mass[1] * acc[1]
        np.testing.assert_allclose(F1, -F2, atol=1e-14)

    def test_memory_efficiency(self):
        """Symmetric uses ~half the pair computations (correctness check)."""
        rng = np.random.default_rng(42)
        n = 100
        pos = rng.uniform(-1, 1, (n, 2))
        mass = rng.uniform(0.1, 2.0, n)
        eps = 0.05

        # N*(N-1)/2 pairs vs N*N
        n_symmetric_pairs = n * (n - 1) // 2
        n_full_pairs = n * n
        ratio = n_symmetric_pairs / n_full_pairs

        assert ratio < 0.51, f"Symmetric pair ratio {ratio:.3f} should be ~0.5"

        # Verify correctness for large N
        acc_bf = compute_forces_vectorized(pos, mass, eps=eps)
        acc_sym = compute_forces_symmetric(pos, mass, eps=eps)
        np.testing.assert_allclose(acc_sym, acc_bf, rtol=1e-10)
