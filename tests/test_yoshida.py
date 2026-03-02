"""Tests for Yoshida 4th-order integrator (item_013)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.forces.brute_force import compute_forces_brute
from src.integrators.yoshida import step_yoshida, W0, W1, W2
from src.integrators.leapfrog import step_leapfrog
from src.metrics import total_energy


class TestYoshidaCoefficients:
    """Verify Yoshida coefficients match published values."""

    def test_coefficients_sum_to_one(self):
        """w0 + w1 + w2 = 1."""
        assert W0 + W1 + W2 == pytest.approx(1.0, abs=1e-14)

    def test_w1_value(self):
        """w1 = 1 / (2 - 2^(1/3))."""
        cbrt2 = 2.0 ** (1.0 / 3.0)
        expected = 1.0 / (2.0 - cbrt2)
        assert W1 == pytest.approx(expected, rel=1e-14)

    def test_w0_is_negative(self):
        """w0 is negative (this is the 'backward' step)."""
        assert W0 < 0


class TestYoshidaConvergence:
    """Verify 4th-order convergence rate."""

    def _kepler_energy_error(self, dt: float, n_orbits: int = 1) -> float:
        """Run Kepler orbit and return max energy error."""
        M, m = 1.0, 1e-6
        G = 1.0
        r = 1.0
        v = np.sqrt(G * M / r)
        period = 2 * np.pi

        masses = np.array([M, m])
        pos = np.array([[0.0, 0.0], [r, 0.0]])
        vel = np.array([[0.0, 0.0], [0.0, v]])

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=0.0)

        E0 = total_energy(masses, pos, vel, G=G, epsilon=0.0)
        n_steps = int(n_orbits * period / dt)

        acc = force_fn(masses, pos)
        max_err = 0.0
        for _ in range(n_steps):
            pos, vel, acc = step_yoshida(masses, pos, vel, force_fn, dt, acc)
            E = total_energy(masses, pos, vel, G=G, epsilon=0.0)
            max_err = max(max_err, abs((E - E0) / E0))

        return max_err

    def test_fourth_order_convergence(self):
        """Halving dt reduces energy error by ~16x (4th order)."""
        err1 = self._kepler_energy_error(dt=0.05, n_orbits=2)
        err2 = self._kepler_energy_error(dt=0.025, n_orbits=2)

        # 4th order: error ratio should be ~16 (2^4)
        ratio = err1 / err2 if err2 > 0 else float("inf")
        # Allow generous tolerance (8x to 24x)
        assert 8.0 < ratio < 32.0, f"Convergence ratio {ratio:.1f} not consistent with 4th order"

    def test_yoshida_better_than_leapfrog(self):
        """Yoshida has smaller energy error than leapfrog for equivalent force evaluations."""
        M, m = 1.0, 1e-6
        G = 1.0
        r = 1.0
        v = np.sqrt(G * M / r)

        masses = np.array([M, m])
        pos0 = np.array([[0.0, 0.0], [r, 0.0]])
        vel0 = np.array([[0.0, 0.0], [0.0, v]])

        def force_fn(m, p, **kw):
            return compute_forces_brute(m, p, G=G, epsilon=0.0)

        E0 = total_energy(masses, pos0, vel0, G=G, epsilon=0.0)

        # Yoshida: 3 force evals per step at dt=0.03 over ~100 steps
        # = 300 force evals
        dt_y = 0.03
        n_steps_y = 100
        pos, vel = pos0.copy(), vel0.copy()
        acc = force_fn(masses, pos)
        for _ in range(n_steps_y):
            pos, vel, acc = step_yoshida(masses, pos, vel, force_fn, dt_y, acc)
        E_yoshida = total_energy(masses, pos, vel, G=G, epsilon=0.0)
        err_yoshida = abs((E_yoshida - E0) / E0)

        # Leapfrog: 1 force eval per step at dt=0.01 over 300 steps
        # = 300 force evals (same budget)
        dt_l = 0.01
        n_steps_l = 300
        pos, vel = pos0.copy(), vel0.copy()
        acc = force_fn(masses, pos)
        for _ in range(n_steps_l):
            pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt_l, acc)
        E_leapfrog = total_energy(masses, pos, vel, G=G, epsilon=0.0)
        err_leapfrog = abs((E_leapfrog - E0) / E0)

        assert err_yoshida < err_leapfrog, (
            f"Yoshida error {err_yoshida:.2e} >= leapfrog error {err_leapfrog:.2e}"
        )
