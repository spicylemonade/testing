"""Tests for integrators module (item_008)."""

import numpy as np
import pytest

from src.bodies import G
from src.forces import compute_forces_vectorized
from src.integrators import euler_step, leapfrog_step, yoshida4_step


def _simple_harmonic_force(pos, mass):
    """Simple harmonic oscillator: a = -omega^2 * x (omega=1)."""
    return -pos


def _gravity_force(eps=0.01):
    """Return a gravity force function with given softening."""
    def force_fn(pos, mass):
        return compute_forces_vectorized(pos, mass, eps=eps)
    return force_fn


class TestEulerStep:
    def test_free_particle(self):
        """Free particle moves in a straight line."""
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[1.0, 0.0]])
        mass = np.array([1.0])

        def zero_force(pos, mass):
            return np.zeros_like(pos)

        new_pos, new_vel = euler_step(pos, vel, mass, dt=0.1, force_fn=zero_force)
        np.testing.assert_allclose(new_pos, [[0.1, 0.0]], atol=1e-14)
        np.testing.assert_allclose(new_vel, [[1.0, 0.0]], atol=1e-14)

    def test_constant_acceleration(self):
        """Constant force produces correct motion."""
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[0.0, 0.0]])
        mass = np.array([1.0])

        def const_force(pos, mass):
            return np.array([[1.0, 0.0]])

        new_pos, new_vel = euler_step(pos, vel, mass, dt=0.1, force_fn=const_force)
        np.testing.assert_allclose(new_vel, [[0.1, 0.0]], atol=1e-14)
        np.testing.assert_allclose(new_pos, [[0.0, 0.0]], atol=1e-14)  # pos doesn't feel new vel


class TestLeapfrogStep:
    def test_free_particle(self):
        """Free particle moves in a straight line."""
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[1.0, 0.0]])
        mass = np.array([1.0])

        def zero_force(pos, mass):
            return np.zeros_like(pos)

        new_pos, new_vel = leapfrog_step(pos, vel, mass, dt=0.1, force_fn=zero_force)
        np.testing.assert_allclose(new_pos, [[0.1, 0.0]], atol=1e-14)

    def test_harmonic_oscillator_energy(self):
        """Leapfrog conserves energy for simple harmonic oscillator."""
        pos = np.array([[1.0, 0.0]])
        vel = np.array([[0.0, 0.0]])
        mass = np.array([1.0])
        dt = 0.01

        def energy(p, v):
            return 0.5 * np.sum(v**2) + 0.5 * np.sum(p**2)

        E0 = energy(pos, vel)
        for _ in range(10000):
            pos, vel = leapfrog_step(pos, vel, mass, dt, _simple_harmonic_force)

        E_final = energy(pos, vel)
        # Leapfrog should conserve energy to < 1e-4 relative error
        assert abs(E_final - E0) / abs(E0) < 1e-4

    def test_time_reversibility(self):
        """Leapfrog is time-reversible: integrating forward then backward returns to start."""
        pos0 = np.array([[1.0, 0.0]])
        vel0 = np.array([[0.0, 1.0]])
        mass = np.array([1.0])
        dt = 0.05

        pos, vel = pos0.copy(), vel0.copy()
        for _ in range(100):
            pos, vel = leapfrog_step(pos, vel, mass, dt, _simple_harmonic_force)

        # Reverse time
        for _ in range(100):
            pos, vel = leapfrog_step(pos, vel, mass, -dt, _simple_harmonic_force)

        np.testing.assert_allclose(pos, pos0, atol=1e-10)
        np.testing.assert_allclose(vel, vel0, atol=1e-10)


class TestYoshida4Step:
    def test_higher_accuracy_than_leapfrog(self):
        """Yoshida4 has lower energy error than leapfrog at same dt."""
        pos0 = np.array([[1.0, 0.0]])
        vel0 = np.array([[0.0, 1.0]])
        mass = np.array([1.0])
        dt = 0.1

        def energy(p, v):
            return 0.5 * np.sum(v**2) + 0.5 * np.sum(p**2)

        E0 = energy(pos0, vel0)

        # Leapfrog
        pos_lf, vel_lf = pos0.copy(), vel0.copy()
        for _ in range(1000):
            pos_lf, vel_lf = leapfrog_step(pos_lf, vel_lf, mass, dt, _simple_harmonic_force)
        err_lf = abs(energy(pos_lf, vel_lf) - E0) / abs(E0)

        # Yoshida4
        pos_y4, vel_y4 = pos0.copy(), vel0.copy()
        for _ in range(1000):
            pos_y4, vel_y4 = yoshida4_step(pos_y4, vel_y4, mass, dt, _simple_harmonic_force)
        err_y4 = abs(energy(pos_y4, vel_y4) - E0) / abs(E0)

        # Yoshida4 should be significantly better
        assert err_y4 < err_lf * 0.1, f"Yoshida4 error {err_y4} not much better than leapfrog {err_lf}"

    def test_fourth_order_convergence(self):
        """Yoshida4 shows 4th-order convergence: error ~ dt^4."""
        pos0 = np.array([[1.0, 0.0]])
        vel0 = np.array([[0.0, 1.0]])
        mass = np.array([1.0])

        def energy(p, v):
            return 0.5 * np.sum(v**2) + 0.5 * np.sum(p**2)

        E0 = energy(pos0, vel0)
        T = 10.0  # total time
        errors = []
        dts = [0.1, 0.05, 0.025]

        for dt in dts:
            n_steps = int(T / dt)
            pos, vel = pos0.copy(), vel0.copy()
            for _ in range(n_steps):
                pos, vel = yoshida4_step(pos, vel, mass, dt, _simple_harmonic_force)
            err = abs(energy(pos, vel) - E0) / abs(E0)
            errors.append(err)

        # Check convergence rate: log(err1/err2) / log(dt1/dt2) should be ~4
        for i in range(len(errors) - 1):
            if errors[i + 1] > 0 and errors[i] > 0:
                rate = np.log(errors[i] / errors[i + 1]) / np.log(dts[i] / dts[i + 1])
                assert rate > 3.0, f"Expected ~4th order, got rate={rate:.1f}"
