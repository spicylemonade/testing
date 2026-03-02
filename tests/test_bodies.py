"""Tests for the bodies module (item_006)."""

import numpy as np
import pytest

from src.bodies import System, kepler_orbit, circular_ring, plummer_sphere, G


class TestSystem:
    def test_system_properties(self):
        """Test System n and dim properties."""
        sys = System(
            pos=np.zeros((5, 2)),
            vel=np.zeros((5, 2)),
            mass=np.ones(5),
        )
        assert sys.n == 5
        assert sys.dim == 2

    def test_system_copy(self):
        """Test that copy produces an independent deep copy."""
        sys = kepler_orbit()
        copy = sys.copy()
        copy.pos[0, 0] = 999.0
        assert sys.pos[0, 0] != 999.0


class TestKeplerOrbit:
    def test_two_bodies(self):
        """Kepler orbit produces exactly 2 bodies."""
        sys = kepler_orbit()
        assert sys.n == 2

    def test_center_of_mass_at_origin(self):
        """Center of mass is at the origin."""
        sys = kepler_orbit(m1=1.0, m2=2.0, a=1.0, e=0.3)
        com = np.average(sys.pos, weights=sys.mass, axis=0)
        np.testing.assert_allclose(com, 0.0, atol=1e-14)

    def test_com_velocity_zero(self):
        """Center of mass velocity is zero."""
        sys = kepler_orbit(m1=1.0, m2=2.0, a=1.0, e=0.5)
        com_vel = np.average(sys.vel, weights=sys.mass, axis=0)
        np.testing.assert_allclose(com_vel, 0.0, atol=1e-14)

    def test_circular_velocity(self):
        """For e=0, velocity matches circular orbit formula."""
        sys = kepler_orbit(m1=1.0, m2=1.0, a=1.0, e=0.0)
        v_expected = np.sqrt(G * 2.0 / 1.0 * 1.0)  # v_circ = sqrt(GM/a)
        v_actual = np.sqrt(np.sum(sys.vel**2, axis=1))
        # Each body has v = (m_other/M_total) * v_circ
        np.testing.assert_allclose(v_actual, v_expected / 2.0, rtol=1e-10)

    def test_eccentricity_raises(self):
        """Invalid eccentricity raises ValueError."""
        with pytest.raises(ValueError):
            kepler_orbit(e=1.5)

    def test_3d_kepler(self):
        """Kepler orbit in 3D produces correct shape."""
        sys = kepler_orbit(d=3)
        assert sys.pos.shape == (2, 3)
        assert sys.vel.shape == (2, 3)


class TestCircularRing:
    def test_correct_count(self):
        """Ring has correct number of bodies."""
        sys = circular_ring(n=10)
        assert sys.n == 10

    def test_radii(self):
        """All bodies are at the specified radius."""
        R = 2.0
        sys = circular_ring(n=8, R=R)
        radii = np.sqrt(np.sum(sys.pos**2, axis=1))
        np.testing.assert_allclose(radii, R, rtol=1e-10)

    def test_equal_masses(self):
        """All bodies have the specified mass."""
        sys = circular_ring(n=5, m=3.0)
        np.testing.assert_allclose(sys.mass, 3.0)


class TestPlummerSphere:
    def test_correct_count(self):
        """Plummer sphere has correct number of bodies."""
        sys = plummer_sphere(n=50)
        assert sys.n == 50

    def test_total_mass(self):
        """Total mass matches specification."""
        M = 10.0
        sys = plummer_sphere(n=100, M=M)
        np.testing.assert_allclose(np.sum(sys.mass), M, rtol=1e-10)

    def test_com_at_origin(self):
        """Center of mass is at origin (after centering)."""
        sys = plummer_sphere(n=200)
        com = np.average(sys.pos, weights=sys.mass, axis=0)
        np.testing.assert_allclose(com, 0.0, atol=1e-13)

    def test_reproducible_seed(self):
        """Same seed produces identical results."""
        s1 = plummer_sphere(n=50, seed=42)
        s2 = plummer_sphere(n=50, seed=42)
        np.testing.assert_array_equal(s1.pos, s2.pos)

    def test_3d_plummer(self):
        """3D Plummer sphere has correct shape."""
        sys = plummer_sphere(n=30, d=3)
        assert sys.pos.shape == (30, 3)
        assert sys.vel.shape == (30, 3)
