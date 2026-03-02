"""Tests for symplectic Euler and leapfrog integrators (item_008)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.forces.brute_force import compute_forces_brute
from src.integrators.euler import step_euler
from src.integrators.leapfrog import step_leapfrog
from src.metrics import total_energy


def _kepler_setup(G=1.0, epsilon=0.0):
    """Set up a circular two-body Kepler orbit.

    Body 0 at origin with mass M=1, Body 1 in circular orbit at r=1.
    Circular velocity: v = sqrt(G*M/r) = 1.0
    Period: T = 2*pi*r/v = 2*pi
    """
    M = 1.0
    m = 1e-6  # Test particle (nearly massless)
    r = 1.0
    v_circ = np.sqrt(G * M / r)

    masses = np.array([M, m])
    positions = np.array([[0.0, 0.0], [r, 0.0]])
    velocities = np.array([[0.0, 0.0], [0.0, v_circ]])

    return masses, positions, velocities, G, epsilon


class TestEuler:
    """Tests for symplectic Euler integrator."""

    def test_single_step_known_force(self):
        """Single Euler step with constant force produces correct update."""
        masses = np.array([1.0])
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[1.0, 0.0]])

        # Constant downward acceleration
        def const_force(m, p, **kw):
            return np.array([[0.0, -1.0]])

        new_pos, new_vel, acc = step_euler(masses, pos, vel, const_force, dt=0.1)

        # v_new = v + dt * a = [1, 0] + 0.1 * [0, -1] = [1, -0.1]
        np.testing.assert_array_almost_equal(new_vel, [[1.0, -0.1]])
        # x_new = x + dt * v_new = [0,0] + 0.1 * [1, -0.1] = [0.1, -0.01]
        np.testing.assert_array_almost_equal(new_pos, [[0.1, -0.01]])

    def test_euler_returns_accelerations(self):
        """Euler step returns the computed accelerations."""
        masses = np.array([1.0])
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[0.0, 0.0]])

        def const_force(m, p, **kw):
            return np.array([[1.0, 2.0]])

        _, _, acc = step_euler(masses, pos, vel, const_force, dt=0.1)
        np.testing.assert_array_almost_equal(acc, [[1.0, 2.0]])


class TestLeapfrog:
    """Tests for leapfrog (Stormer-Verlet) integrator."""

    def test_single_step_known_force(self):
        """Single leapfrog step with constant force."""
        masses = np.array([1.0])
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[1.0, 0.0]])

        def const_force(m, p, **kw):
            return np.array([[0.0, -1.0]])

        new_pos, new_vel, new_acc = step_leapfrog(
            masses, pos, vel, const_force, dt=0.1
        )

        # Half-kick: v_half = [1, 0] + 0.05*[0,-1] = [1, -0.05]
        # Drift: x_new = [0,0] + 0.1*[1, -0.05] = [0.1, -0.005]
        # a_new = [0, -1] (constant)
        # Full-kick: v_new = [1, -0.05] + 0.05*[0,-1] = [1, -0.1]
        np.testing.assert_array_almost_equal(new_pos, [[0.1, -0.005]])
        np.testing.assert_array_almost_equal(new_vel, [[1.0, -0.1]])

    def test_leapfrog_energy_conservation_kepler(self):
        """Leapfrog conserves energy within 1% over 100 orbits for Kepler problem."""
        masses, positions, velocities, G, epsilon = _kepler_setup()

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=epsilon)

        E0 = total_energy(masses, positions, velocities, G=G, epsilon=epsilon)
        dt = 0.01
        period = 2.0 * np.pi  # Approximate for test particle
        n_steps = int(100 * period / dt)

        pos, vel = positions.copy(), velocities.copy()
        acc = force_fn(masses, pos)

        max_rel_error = 0.0
        for _ in range(n_steps):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt, acc)
            E = total_energy(masses, pos, vel, G=G, epsilon=epsilon)
            rel_err = abs((E - E0) / E0)
            max_rel_error = max(max_rel_error, rel_err)

        assert max_rel_error < 0.01, f"Energy error {max_rel_error:.6f} exceeds 1%"

    def test_leapfrog_time_reversibility(self):
        """Leapfrog is time-reversible: forward then backward returns to start."""
        masses = np.array([1.0, 1.0])
        pos0 = np.array([[0.0, 0.0], [1.0, 0.0]])
        vel0 = np.array([[0.0, 0.1], [0.0, -0.1]])

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=1.0, epsilon=0.01)

        dt = 0.01
        pos, vel = pos0.copy(), vel0.copy()
        acc = force_fn(masses, pos)

        # Forward 100 steps
        for _ in range(100):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt, acc)

        # Reverse velocity
        vel = -vel

        # Backward 100 steps
        acc = force_fn(masses, pos)
        for _ in range(100):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt, acc)

        # Should return to start (reverse velocity again)
        vel = -vel
        np.testing.assert_array_almost_equal(pos, pos0, decimal=8)
        np.testing.assert_array_almost_equal(vel, vel0, decimal=8)

    def test_leapfrog_reuses_accelerations(self):
        """Providing previous accelerations avoids redundant force computation."""
        masses = np.array([1.0, 1.0])
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        vel = np.array([[0.0, 0.0], [0.0, 1.0]])

        call_count = [0]

        def counting_force(m, p, **kw):
            call_count[0] += 1
            return compute_forces_brute(m, p, G=1.0, epsilon=0.01)

        # First step: 2 calls (initial + after drift) if no acc provided
        # With acc provided: 1 call (after drift only)
        acc0 = counting_force(masses, pos)
        call_count[0] = 0

        step_leapfrog(masses, pos, vel, counting_force, 0.01, acc0)
        assert call_count[0] == 1  # Only one force eval needed

    def test_leapfrog_correct_kepler_period(self):
        """Leapfrog reproduces Kepler orbital period within 1%."""
        masses, positions, velocities, G, epsilon = _kepler_setup()

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=epsilon)

        dt = 0.001
        pos, vel = positions.copy(), velocities.copy()
        acc = force_fn(masses, pos)

        # Track when body 1 crosses the positive x-axis (y changes sign)
        analytical_period = 2.0 * np.pi
        prev_y = pos[1, 1]
        crossings = []

        for step in range(int(3 * analytical_period / dt)):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt, acc)
            curr_y = pos[1, 1]
            # Detect positive x-axis crossing (y goes from negative to positive)
            if prev_y < 0 and curr_y >= 0:
                crossings.append(step * dt)
            prev_y = curr_y

        # Period is time between successive crossings
        assert len(crossings) >= 2, f"Only {len(crossings)} crossings detected"
        measured_period = crossings[1] - crossings[0]
        rel_error = abs(measured_period - analytical_period) / analytical_period
        assert rel_error < 0.01, f"Period error {rel_error:.4f} exceeds 1%"
