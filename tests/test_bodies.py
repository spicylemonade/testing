"""Tests for Body and System data structures (item_006)."""

import json
import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.bodies import Body, System


class TestBody:
    """Tests for the Body dataclass."""

    def test_body_creation_defaults(self):
        """Body with just mass gets zero position/velocity/acceleration."""
        b = Body(mass=1.0)
        assert b.mass == 1.0
        np.testing.assert_array_equal(b.position, [0.0, 0.0])
        np.testing.assert_array_equal(b.velocity, [0.0, 0.0])
        np.testing.assert_array_equal(b.acceleration, [0.0, 0.0])

    def test_body_creation_with_values(self):
        """Body with explicit position and velocity."""
        b = Body(mass=5.0, position=[1.0, 2.0], velocity=[-1.0, 0.5])
        assert b.mass == 5.0
        np.testing.assert_array_almost_equal(b.position, [1.0, 2.0])
        np.testing.assert_array_almost_equal(b.velocity, [-1.0, 0.5])

    def test_body_negative_mass_raises(self):
        """Negative mass should raise ValueError."""
        with pytest.raises(ValueError, match="Mass must be positive"):
            Body(mass=-1.0)

    def test_body_kinetic_energy(self):
        """Kinetic energy = 0.5 * m * |v|^2."""
        b = Body(mass=2.0, velocity=[3.0, 4.0])
        # 0.5 * 2 * (9 + 16) = 25
        assert b.kinetic_energy() == pytest.approx(25.0)

    def test_body_serialization_roundtrip(self):
        """Body -> dict -> Body preserves all fields."""
        original = Body(mass=3.0, position=[1.5, -2.5], velocity=[0.1, 0.2])
        data = original.to_dict()
        restored = Body.from_dict(data)
        assert restored.mass == original.mass
        np.testing.assert_array_almost_equal(restored.position, original.position)
        np.testing.assert_array_almost_equal(restored.velocity, original.velocity)


class TestSystem:
    """Tests for the System collection class."""

    def test_empty_system(self):
        """New system has zero bodies."""
        sys = System()
        assert sys.n == 0

    def test_add_and_query(self):
        """Add bodies and query by index."""
        sys = System(G=1.0, epsilon=0.01)
        sys.add(Body(mass=1.0, position=[0.0, 0.0]))
        sys.add(Body(mass=2.0, position=[1.0, 0.0]))
        assert sys.n == 2
        assert sys.get(1).mass == 2.0

    def test_remove(self):
        """Remove body reduces count."""
        sys = System()
        sys.add(Body(mass=1.0))
        sys.add(Body(mass=2.0))
        removed = sys.remove(0)
        assert removed.mass == 1.0
        assert sys.n == 1

    def test_vectorized_accessors(self):
        """Bulk accessors return correct shapes and values."""
        sys = System()
        sys.add(Body(mass=1.0, position=[1.0, 2.0], velocity=[0.1, 0.2]))
        sys.add(Body(mass=3.0, position=[3.0, 4.0], velocity=[0.3, 0.4]))

        masses = sys.masses()
        positions = sys.positions()
        velocities = sys.velocities()

        assert masses.shape == (2,)
        assert positions.shape == (2, 2)
        assert velocities.shape == (2, 2)
        np.testing.assert_array_almost_equal(masses, [1.0, 3.0])
        np.testing.assert_array_almost_equal(positions[1], [3.0, 4.0])

    def test_json_roundtrip(self):
        """System -> JSON -> System preserves all state."""
        sys = System(G=2.0, epsilon=0.05)
        sys.add(Body(mass=1.0, position=[1.0, 0.0], velocity=[0.0, 1.0]))
        sys.add(Body(mass=2.0, position=[-1.0, 0.0], velocity=[0.0, -0.5]))

        json_str = sys.to_json()
        restored = System.from_json(json_str)

        assert restored.G == 2.0
        assert restored.epsilon == 0.05
        assert restored.n == 2
        np.testing.assert_array_almost_equal(
            restored.positions(), sys.positions()
        )
