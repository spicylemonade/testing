"""Tests for initial condition generators (item_015)."""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.initial_conditions import (
    circular_two_body,
    figure_eight,
    plummer_sphere,
    solar_system_inner,
)


class TestCircularTwoBody:
    """Tests for circular orbit generator."""

    def test_correct_circular_velocity(self):
        """Circular velocity v = sqrt(GM/r)."""
        ic = circular_two_body(M=1.0, m=1e-6, r=1.0, G=1.0)
        v_expected = np.sqrt(1.0)  # sqrt(G*M/r)
        v_actual = np.linalg.norm(ic["velocities"][1])
        assert v_actual == pytest.approx(v_expected, rel=1e-6)

    def test_period(self):
        """Period T = 2*pi*sqrt(r^3/(G*M))."""
        ic = circular_two_body(M=1.0, m=1e-6, r=1.0, G=1.0)
        assert ic["period"] == pytest.approx(2 * np.pi, rel=1e-4)

    def test_positions(self):
        """Central body at origin, orbiting body at (r, 0)."""
        ic = circular_two_body(r=2.0)
        np.testing.assert_array_almost_equal(ic["positions"][0], [0.0, 0.0])
        np.testing.assert_array_almost_equal(ic["positions"][1], [2.0, 0.0])


class TestFigureEight:
    """Tests for figure-eight three-body solution."""

    def test_initial_conditions_match_published(self):
        """ICs must match Chenciner-Montgomery values within 1e-6."""
        ic = figure_eight()

        # Body positions
        np.testing.assert_array_almost_equal(ic["positions"][0], [-1.0, 0.0], decimal=6)
        np.testing.assert_array_almost_equal(ic["positions"][1], [1.0, 0.0], decimal=6)
        np.testing.assert_array_almost_equal(ic["positions"][2], [0.0, 0.0], decimal=6)

        # Equal masses
        np.testing.assert_array_almost_equal(ic["masses"], [1.0, 1.0, 1.0])

    def test_zero_total_momentum(self):
        """System must have zero total linear momentum."""
        ic = figure_eight()
        p_total = np.sum(ic["masses"][:, np.newaxis] * ic["velocities"], axis=0)
        np.testing.assert_array_almost_equal(p_total, [0.0, 0.0], decimal=10)

    def test_zero_center_of_mass(self):
        """Center of mass must be at origin."""
        ic = figure_eight()
        com = np.sum(ic["masses"][:, np.newaxis] * ic["positions"], axis=0) / np.sum(ic["masses"])
        np.testing.assert_array_almost_equal(com, [0.0, 0.0], decimal=10)


class TestPlummerSphere:
    """Tests for Plummer sphere generator."""

    def test_correct_number_of_bodies(self):
        """Generate requested number of bodies."""
        ic = plummer_sphere(N=50)
        assert len(ic["masses"]) == 50
        assert ic["positions"].shape == (50, 2)

    def test_density_profile(self):
        """Radial density should decrease with distance (statistical)."""
        ic = plummer_sphere(N=1000, a=1.0, seed=42)

        radii = np.sqrt(np.sum(ic["positions"] ** 2, axis=1))
        inner = np.sum(radii < 1.0)
        outer = np.sum(radii > 2.0)

        # More bodies should be in the inner region
        assert inner > outer

    def test_zero_center_of_mass(self):
        """COM correction should center the system."""
        ic = plummer_sphere(N=200, seed=42)
        com = np.sum(ic["masses"][:, np.newaxis] * ic["positions"], axis=0) / np.sum(ic["masses"])
        np.testing.assert_array_almost_equal(com, [0.0, 0.0], decimal=10)

    def test_reproducible_with_seed(self):
        """Same seed produces identical initial conditions."""
        ic1 = plummer_sphere(N=50, seed=42)
        ic2 = plummer_sphere(N=50, seed=42)
        np.testing.assert_array_equal(ic1["positions"], ic2["positions"])


class TestSolarSystem:
    """Tests for solar system generator."""

    def test_correct_body_count(self):
        """Should have 5 bodies (Sun + 4 inner planets)."""
        ic = solar_system_inner()
        assert len(ic["masses"]) == 5

    def test_sun_at_origin(self):
        """Sun should be at origin."""
        ic = solar_system_inner()
        np.testing.assert_array_almost_equal(ic["positions"][0], [0.0, 0.0])
