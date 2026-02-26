"""Ray: parameterized ray for voxel grid traversal."""

import numpy as np


class Ray:
    """Ray defined by origin and direction: P(t) = origin + t * direction.

    Direction is stored as-is (not normalized) to preserve t-parameter semantics.
    """

    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = np.asarray(origin, dtype=np.float64)
        self.direction = np.asarray(direction, dtype=np.float64)
        assert self.origin.shape == (3,)
        assert self.direction.shape == (3,)

    def at(self, t: float) -> np.ndarray:
        """Evaluate point along ray at parameter t."""
        return self.origin + t * self.direction

    @property
    def inv_direction(self) -> np.ndarray:
        """1/direction with safe handling of zero components."""
        with np.errstate(divide='ignore'):
            inv = 1.0 / self.direction
        return inv

    def __repr__(self):
        return f"Ray(origin={self.origin}, direction={self.direction})"
