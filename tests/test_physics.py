"""
Physics correctness test suite for the N-body gravity simulator.
================================================================

Tests:
1. Two-body Keplerian orbit period within 5% of analytical solution
2. Momentum conservation within tolerance
3. Energy computation correctness against hand-calculated values
4. Force symmetry (F_ij = -F_ji)
5. Zero force for single body
6. Leapfrog energy conservation (bounded oscillation)
"""

import sys
import os
import numpy as np
import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gravity_sim import (
    compute_forces_direct,
    compute_forces_vectorized,
    compute_kinetic_energy,
    compute_potential_energy,
    compute_potential_energy_vectorized,
    compute_total_energy,
    compute_momentum,
    step_euler,
    step_verlet,
    step_leapfrog,
    run_simulation,
)


class TestForceSymmetry:
    """Test 4: Force symmetry F_ij = -F_ji."""

    def test_force_symmetry_direct(self):
        """Direct force computation must satisfy Newton's third law."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2) * 5
        masses = np.random.uniform(0.5, 2.0, N)
        G = 1.0
        softening = 0.01

        # Compute forces using the loop version
        acc = compute_forces_direct(positions, masses, G, softening)

        # Total force on system should be zero (Newton's third law)
        total_force = np.sum(acc * masses[:, np.newaxis], axis=0)
        np.testing.assert_allclose(total_force, [0.0, 0.0], atol=1e-10)

    def test_force_symmetry_vectorized(self):
        """Vectorized force computation must satisfy Newton's third law."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2) * 5
        masses = np.random.uniform(0.5, 2.0, N)

        acc = compute_forces_vectorized(positions, masses, G=1.0, softening=0.01)

        total_force = np.sum(acc * masses[:, np.newaxis], axis=0)
        np.testing.assert_allclose(total_force, [0.0, 0.0], atol=1e-10)

    def test_direct_vs_vectorized_consistency(self):
        """Direct and vectorized force computations must agree."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2) * 5
        masses = np.random.uniform(0.5, 2.0, N)

        acc_direct = compute_forces_direct(positions, masses)
        acc_vec = compute_forces_vectorized(positions, masses)

        np.testing.assert_allclose(acc_direct, acc_vec, rtol=1e-10)


class TestZeroForce:
    """Test 5: Zero force for single body."""

    def test_single_body_zero_force(self):
        """A single body should experience zero gravitational force."""
        positions = np.array([[1.0, 2.0]])
        masses = np.array([5.0])

        acc = compute_forces_vectorized(positions, masses)
        np.testing.assert_array_equal(acc, [[0.0, 0.0]])

    def test_single_body_zero_force_direct(self):
        """Direct computation: single body has zero force."""
        positions = np.array([[1.0, 2.0]])
        masses = np.array([5.0])

        acc = compute_forces_direct(positions, masses)
        np.testing.assert_array_equal(acc, [[0.0, 0.0]])


class TestEnergyComputation:
    """Test 3: Energy computation correctness against hand-calculated values."""

    def test_kinetic_energy(self):
        """KE = 0.5 * m * v^2 for known values."""
        # Body 1: m=2, v=(3,4) => KE = 0.5 * 2 * (9+16) = 25
        # Body 2: m=1, v=(0,0) => KE = 0
        velocities = np.array([[3.0, 4.0], [0.0, 0.0]])
        masses = np.array([2.0, 1.0])
        ke = compute_kinetic_energy(velocities, masses)
        assert abs(ke - 25.0) < 1e-12

    def test_potential_energy_two_bodies(self):
        """PE = -G * m1 * m2 / r for two bodies at known separation."""
        # Two bodies: m1=1, m2=1, separation=1.0, G=1, softening=0
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        masses = np.array([1.0, 1.0])
        # With softening=0: PE = -1*1*1/1 = -1
        pe = compute_potential_energy(positions, masses, G=1.0, softening=0.0)
        assert abs(pe - (-1.0)) < 1e-12

    def test_potential_energy_vectorized_matches_loop(self):
        """Vectorized and loop PE must agree."""
        np.random.seed(42)
        positions = np.random.randn(5, 2)
        masses = np.random.uniform(0.5, 2.0, 5)

        pe_loop = compute_potential_energy(positions, masses, G=1.0, softening=0.1)
        pe_vec = compute_potential_energy_vectorized(positions, masses, G=1.0, softening=0.1)

        np.testing.assert_allclose(pe_loop, pe_vec, rtol=1e-10)

    def test_total_energy_hand_calculated(self):
        """Total energy for a simple two-body system."""
        # Two unit masses at distance 2 with no velocity
        positions = np.array([[0.0, 0.0], [2.0, 0.0]])
        velocities = np.array([[0.0, 0.0], [0.0, 0.0]])
        masses = np.array([1.0, 1.0])

        te, ke, pe = compute_total_energy(positions, velocities, masses,
                                          G=1.0, softening=0.0)
        assert abs(ke - 0.0) < 1e-12
        assert abs(pe - (-0.5)) < 1e-12
        assert abs(te - (-0.5)) < 1e-12


class TestMomentumConservation:
    """Test 2: Momentum conservation within tolerance."""

    def test_momentum_conservation_leapfrog(self):
        """Leapfrog integrator should conserve total momentum to machine precision."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2)
        velocities = np.random.randn(N, 2) * 0.1
        masses = np.random.uniform(0.5, 2.0, N)

        p_initial = compute_momentum(velocities, masses)

        results = run_simulation(
            positions, velocities, masses,
            n_steps=200, dt=0.01,
            integrator="leapfrog",
            G=1.0, softening=0.1,
            track_energy=False,
        )

        # Get final velocities
        final_vel = results["velocities"][-1]
        p_final = compute_momentum(final_vel, masses)

        np.testing.assert_allclose(p_initial, p_final, atol=1e-10)

    def test_momentum_conservation_verlet(self):
        """Verlet integrator should conserve total momentum."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2)
        velocities = np.random.randn(N, 2) * 0.1
        masses = np.random.uniform(0.5, 2.0, N)

        p_initial = compute_momentum(velocities, masses)

        results = run_simulation(
            positions, velocities, masses,
            n_steps=200, dt=0.01,
            integrator="verlet",
            G=1.0, softening=0.1,
            track_energy=False,
        )

        final_vel = results["velocities"][-1]
        p_final = compute_momentum(final_vel, masses)

        np.testing.assert_allclose(p_initial, p_final, atol=1e-10)


class TestKeplerianOrbit:
    """Test 1: Two-body Keplerian orbit period within 5% of analytical solution."""

    def test_circular_orbit_period(self):
        """
        Set up a circular orbit and verify the period matches Kepler's third law.

        For a circular orbit with G=1, M_total=2 (unit masses), radius a:
            T = 2*pi*sqrt(a^3 / (G * M_total))

        We use the center-of-mass frame with equal masses.
        """
        G = 1.0
        m1, m2 = 1.0, 1.0
        M = m1 + m2

        # Semi-major axis (separation / 2 for equal masses)
        a = 2.0  # total separation
        # Orbital velocity for circular orbit in CM frame
        # v = sqrt(G * M / (4 * a)) for each body (equal mass, each at a/2)
        v_orb = np.sqrt(G * M / (4 * a))

        positions = np.array([[-a / 2, 0.0], [a / 2, 0.0]])
        velocities = np.array([[0.0, -v_orb], [0.0, v_orb]])
        masses = np.array([m1, m2])

        # Analytical period: T = 2*pi*sqrt(a^3 / (G*M)) where a is separation
        # Actually for two equal mass bodies in CM:
        # Each orbits at distance a/2 from center
        # T = 2*pi * a^(3/2) / sqrt(G*M)
        T_analytical = 2 * np.pi * a ** (3 / 2) / np.sqrt(G * M)

        # Simulate for 2.5 periods with small dt
        dt = 0.001
        n_steps = int(2.5 * T_analytical / dt)

        results = run_simulation(
            positions, velocities, masses,
            n_steps=n_steps, dt=dt,
            integrator="leapfrog",
            G=G, softening=0.0001,  # very small softening
            track_energy=False,
        )

        # Find the period by detecting when body 0 completes one orbit
        # (returns to starting x position with positive y velocity)
        pos_history = results["positions"]
        x0_values = [p[0, 0] for p in pos_history]

        # Find zero-crossings of x from negative to positive
        crossings = []
        for i in range(1, len(x0_values)):
            if x0_values[i - 1] < -a / 2 + 0.01 and x0_values[i] >= -a / 2 + 0.01:
                # Approximate time
                crossings.append(i * dt)

        # Alternative: track y-position sign changes (crossing y=0 upward)
        y0_values = [p[0, 1] for p in pos_history]
        y_crossings = []
        for i in range(1, len(y0_values)):
            if y0_values[i - 1] < 0 and y0_values[i] >= 0:
                # Linear interpolation for better accuracy
                frac = -y0_values[i - 1] / (y0_values[i] - y0_values[i - 1] + 1e-30)
                y_crossings.append((i - 1 + frac) * dt)

        assert len(y_crossings) >= 2, \
            f"Expected at least 2 zero-crossings, got {len(y_crossings)}"

        T_measured = y_crossings[1] - y_crossings[0]
        relative_error = abs(T_measured - T_analytical) / T_analytical

        assert relative_error < 0.05, \
            f"Period error {relative_error*100:.2f}% exceeds 5%. " \
            f"T_analytical={T_analytical:.4f}, T_measured={T_measured:.4f}"


class TestLeapfrogEnergyConservation:
    """Bonus test: Leapfrog should have bounded energy oscillation."""

    def test_leapfrog_bounded_energy(self):
        """Leapfrog energy drift should remain bounded (no secular drift)."""
        np.random.seed(42)
        N = 10
        positions = np.random.randn(N, 2) * 2
        velocities = np.random.randn(N, 2) * 0.1
        masses = np.random.uniform(0.5, 2.0, N)

        results = run_simulation(
            positions, velocities, masses,
            n_steps=500, dt=0.01,
            integrator="leapfrog",
            G=1.0, softening=0.5,
            track_energy=True,
        )

        energies = [e["total"] for e in results["energy"]]
        e0 = energies[0]
        max_drift = max(abs(e - e0) / abs(e0) for e in energies)

        # Leapfrog should keep energy within a few percent for well-softened system
        assert max_drift < 0.05, \
            f"Leapfrog energy drift {max_drift*100:.2f}% exceeds 5% bound"
