"""Tests for Body and System data structures."""

import numpy as np
from src.bodies import Body, System


def test_body_creation():
    b = Body(mass=1.0, position=[1.0, 2.0], velocity=[0.1, -0.2])
    assert b.mass == 1.0
    np.testing.assert_array_equal(b.position, [1.0, 2.0])
    np.testing.assert_array_equal(b.velocity, [0.1, -0.2])
    assert b.position.dtype == np.float64


def test_system_3body():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.5]),
        Body(mass=2.0, position=[1.0, 0.0], velocity=[0.0, -0.25]),
        Body(mass=0.5, position=[0.5, 0.866], velocity=[-0.3, 0.0]),
    ]
    sys = System(bodies=bodies)

    assert sys.n == 3
    assert sys.dim == 2
    np.testing.assert_array_equal(sys.masses, [1.0, 2.0, 0.5])
    assert sys.positions.shape == (3, 2)
    assert sys.velocities.shape == (3, 2)
    np.testing.assert_array_almost_equal(sys.positions[1], [1.0, 0.0])


def test_system_get_bodies():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.5]),
        Body(mass=2.0, position=[1.0, 0.0], velocity=[0.0, -0.25]),
    ]
    sys = System(bodies=bodies)
    recovered = sys.get_bodies()
    assert len(recovered) == 2
    assert recovered[0].mass == 1.0
    np.testing.assert_array_equal(recovered[1].position, [1.0, 0.0])
