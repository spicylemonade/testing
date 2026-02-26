"""Core data structures for N-body simulation: Body and System."""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class Body:
    """A single gravitational body with mass, position, and velocity."""
    mass: float
    position: np.ndarray
    velocity: np.ndarray

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        self.velocity = np.asarray(self.velocity, dtype=np.float64)


class System:
    """Collection of gravitational bodies stored as structure-of-arrays.

    Internally stores masses, positions, and velocities as contiguous
    NumPy arrays for efficient vectorized computation.
    """

    def __init__(self, bodies: list[Body], G: float = 1.0, epsilon: float = 1e-4):
        self.G = G
        self.epsilon = epsilon
        self.n = len(bodies)
        self.masses = np.array([b.mass for b in bodies], dtype=np.float64)
        self.positions = np.array([b.position for b in bodies], dtype=np.float64)
        self.velocities = np.array([b.velocity for b in bodies], dtype=np.float64)

    @property
    def dim(self) -> int:
        return self.positions.shape[1]

    def get_bodies(self) -> list[Body]:
        """Reconstruct list of Body objects from internal arrays."""
        return [
            Body(mass=self.masses[i],
                 position=self.positions[i].copy(),
                 velocity=self.velocities[i].copy())
            for i in range(self.n)
        ]
