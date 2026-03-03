from __future__ import annotations

import numpy as np


def two_body(seed: int = 42) -> dict:
    """Circular equal-mass two-body setup in 2D code units."""
    _ = seed
    masses = np.array([1.0, 1.0], dtype=np.float64)
    positions = np.array([[-0.5, 0.0], [0.5, 0.0]], dtype=np.float64)
    v = np.sqrt(0.5)
    velocities = np.array([[0.0, -v], [0.0, v]], dtype=np.float64)
    return {
        "name": "two_body",
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
    }


def three_body(seed: int = 42) -> dict:
    """Simple deterministic three-body setup in 2D."""
    _ = seed
    masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    positions = np.array([[-1.0, 0.0], [1.0, 0.0], [0.0, 0.3]], dtype=np.float64)
    velocities = np.array([[0.2, 0.3], [-0.2, 0.3], [0.0, -0.6]], dtype=np.float64)
    return {
        "name": "three_body",
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
    }


def random_n_body(n: int, seed: int = 42) -> dict:
    """Random N-body initialization with deterministic RNG."""
    rng = np.random.default_rng(seed)
    masses = rng.uniform(0.5, 1.5, size=n).astype(np.float64)
    positions = rng.uniform(-1.0, 1.0, size=(n, 2)).astype(np.float64)
    velocities = rng.normal(0.0, 0.12, size=(n, 2)).astype(np.float64)

    total_mass = masses.sum()
    com = (positions * masses[:, None]).sum(axis=0) / total_mass
    com_vel = (velocities * masses[:, None]).sum(axis=0) / total_mass
    positions -= com
    velocities -= com_vel

    return {
        "name": f"random_{n}",
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
    }
