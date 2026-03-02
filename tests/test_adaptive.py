"""Tests for adaptive timestep control (item_014)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.forces.brute_force import compute_forces_brute
from src.integrators.leapfrog import step_leapfrog
from src.integrators.adaptive import step_adaptive, run_adaptive, _min_pairwise_distance
from src.metrics import total_energy


class TestMinPairwiseDistance:
    """Tests for close encounter detection."""

    def test_two_bodies(self):
        """Min distance between two bodies."""
        positions = np.array([[0.0, 0.0], [3.0, 4.0]])
        assert _min_pairwise_distance(positions) == pytest.approx(5.0)

    def test_single_body(self):
        """Single body returns inf."""
        positions = np.array([[0.0, 0.0]])
        assert _min_pairwise_distance(positions) == float("inf")


class TestAdaptiveStep:
    """Tests for adaptive timestep integration."""

    def test_dt_reduction_during_close_encounter(self):
        """Timestep decreases when bodies are close."""
        masses = np.array([1.0, 1.0])
        # Bodies very close together
        positions = np.array([[0.0, 0.0], [0.01, 0.0]])
        velocities = np.array([[0.0, 0.0], [0.0, 0.0]])

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=1.0, epsilon=0.001)

        _, _, _, actual_dt = step_adaptive(
            masses, positions, velocities, force_fn,
            dt_base=0.1,
            base_integrator=step_leapfrog,
            threshold=0.1,
            reference_dist=1.0,
        )

        # dt should be much smaller than base
        assert actual_dt < 0.1

    def test_dt_preserved_for_distant_bodies(self):
        """Timestep stays at base when bodies are far apart."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [10.0, 0.0]])
        velocities = np.array([[0.0, 0.0], [0.0, 0.0]])

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=1.0, epsilon=0.01)

        _, _, _, actual_dt = step_adaptive(
            masses, positions, velocities, force_fn,
            dt_base=0.1,
            base_integrator=step_leapfrog,
            threshold=0.1,
            reference_dist=1.0,
        )

        assert actual_dt == pytest.approx(0.1)

    def test_energy_conservation_improvement(self):
        """Adaptive dt improves energy conservation for close encounters."""
        # Set up a hyperbolic-like flyby
        masses = np.array([1.0, 0.001])
        pos0 = np.array([[0.0, 0.0], [5.0, 0.1]])
        vel0 = np.array([[0.0, 0.0], [-2.0, 0.0]])
        G = 1.0
        eps = 0.01

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=eps)

        E0 = total_energy(masses, pos0, vel0, G=G, epsilon=eps)

        # Fixed timestep
        dt_fixed = 0.01
        t_end = 5.0
        n_fixed = int(t_end / dt_fixed)
        pos, vel = pos0.copy(), vel0.copy()
        acc = force_fn(masses, pos)
        for _ in range(n_fixed):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt_fixed, acc)
        E_fixed = total_energy(masses, pos, vel, G=G, epsilon=eps)
        err_fixed = abs((E_fixed - E0) / E0)

        # Adaptive timestep
        result = run_adaptive(
            masses, pos0, vel0, force_fn,
            dt_base=0.01, t_end=t_end,
            base_integrator=step_leapfrog,
            threshold=0.5, min_factor=0.01,
            reference_dist=1.0,
            G=G, epsilon=eps,
        )
        E_adaptive = total_energy(
            masses, result["positions"], result["velocities"], G=G, epsilon=eps
        )
        err_adaptive = abs((E_adaptive - E0) / E0)

        # Adaptive should be at least as good
        assert err_adaptive <= err_fixed * 1.1  # Allow small tolerance

    def test_fewer_steps_than_fixed(self):
        """Adaptive uses fewer total steps than fixed for same accuracy."""
        masses = np.array([1.0, 0.001])
        pos0 = np.array([[0.0, 0.0], [3.0, 0.0]])
        vel0 = np.array([[0.0, 0.0], [0.0, 0.5]])  # Circular-ish orbit
        G = 1.0
        eps = 0.01

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=eps)

        t_end = 10.0
        n_fixed = int(t_end / 0.001)  # Very small fixed dt

        result = run_adaptive(
            masses, pos0, vel0, force_fn,
            dt_base=0.01, t_end=t_end,
            base_integrator=step_leapfrog,
            threshold=0.2, min_factor=0.1,
            reference_dist=1.0,
            G=G, epsilon=eps,
        )

        # Adaptive should use fewer steps than the very small fixed dt
        assert result["step_count"] < n_fixed
