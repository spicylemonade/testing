"""Core data structures for N-body gravity simulation.

Provides Body (single particle) and System (collection manager) classes
with JSON serialization and vectorized bulk accessors.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class Body:
    """A single gravitational body in 2D.

    Attributes:
        mass: Scalar mass (positive).
        position: 2D position vector [x, y].
        velocity: 2D velocity vector [vx, vy].
        acceleration: 2D acceleration vector [ax, ay].
    """

    mass: float
    position: np.ndarray = field(default_factory=lambda: np.zeros(2))
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(2))
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(2))

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        self.velocity = np.asarray(self.velocity, dtype=np.float64)
        self.acceleration = np.asarray(self.acceleration, dtype=np.float64)
        if self.mass <= 0:
            raise ValueError(f"Mass must be positive, got {self.mass}")
        if self.position.shape != (2,):
            raise ValueError(f"Position must be 2D, got shape {self.position.shape}")
        if self.velocity.shape != (2,):
            raise ValueError(f"Velocity must be 2D, got shape {self.velocity.shape}")
        if self.acceleration.shape != (2,):
            raise ValueError(f"Acceleration must be 2D, got shape {self.acceleration.shape}")

    def kinetic_energy(self) -> float:
        """Return kinetic energy 0.5 * m * |v|^2."""
        return 0.5 * self.mass * np.dot(self.velocity, self.velocity)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mass": self.mass,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "acceleration": self.acceleration.tolist(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Body:
        """Deserialize from dictionary."""
        return cls(
            mass=data["mass"],
            position=np.array(data["position"]),
            velocity=np.array(data["velocity"]),
            acceleration=np.array(data.get("acceleration", [0.0, 0.0])),
        )


class System:
    """A collection of gravitational bodies with vectorized accessors.

    Manages body state and provides bulk numpy array views for
    efficient force computation and integration.
    """

    def __init__(self, G: float = 1.0, epsilon: float = 0.01):
        """Initialize an empty system.

        Args:
            G: Gravitational constant.
            epsilon: Plummer softening length.
        """
        self.G = G
        self.epsilon = epsilon
        self._bodies: List[Body] = []

    @property
    def n(self) -> int:
        """Number of bodies in the system."""
        return len(self._bodies)

    @property
    def bodies(self) -> List[Body]:
        """List of bodies (read-only reference)."""
        return self._bodies

    def add(self, body: Body) -> None:
        """Add a body to the system."""
        self._bodies.append(body)

    def remove(self, index: int) -> Body:
        """Remove and return the body at the given index."""
        return self._bodies.pop(index)

    def get(self, index: int) -> Body:
        """Get body by index."""
        return self._bodies[index]

    # --- Vectorized bulk accessors ---

    def masses(self) -> np.ndarray:
        """Return masses as (N,) array."""
        return np.array([b.mass for b in self._bodies])

    def positions(self) -> np.ndarray:
        """Return positions as (N, 2) array."""
        return np.array([b.position for b in self._bodies])

    def velocities(self) -> np.ndarray:
        """Return velocities as (N, 2) array."""
        return np.array([b.velocity for b in self._bodies])

    def accelerations(self) -> np.ndarray:
        """Return accelerations as (N, 2) array."""
        return np.array([b.acceleration for b in self._bodies])

    def set_positions(self, pos: np.ndarray) -> None:
        """Update all body positions from (N, 2) array."""
        for i, b in enumerate(self._bodies):
            b.position = pos[i].copy()

    def set_velocities(self, vel: np.ndarray) -> None:
        """Update all body velocities from (N, 2) array."""
        for i, b in enumerate(self._bodies):
            b.velocity = vel[i].copy()

    def set_accelerations(self, acc: np.ndarray) -> None:
        """Update all body accelerations from (N, 2) array."""
        for i, b in enumerate(self._bodies):
            b.acceleration = acc[i].copy()

    # --- Serialization ---

    def to_dict(self) -> Dict[str, Any]:
        """Serialize system to dictionary."""
        return {
            "G": self.G,
            "epsilon": self.epsilon,
            "bodies": [b.to_dict() for b in self._bodies],
        }

    def to_json(self, path: Optional[str] = None) -> str:
        """Serialize to JSON string, optionally saving to file."""
        s = json.dumps(self.to_dict(), indent=2)
        if path is not None:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(s)
        return s

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> System:
        """Deserialize from dictionary."""
        sys = cls(G=data.get("G", 1.0), epsilon=data.get("epsilon", 0.01))
        for bd in data.get("bodies", []):
            sys.add(Body.from_dict(bd))
        return sys

    @classmethod
    def from_json(cls, json_str_or_path: str) -> System:
        """Deserialize from JSON string or file path."""
        p = Path(json_str_or_path)
        if p.exists():
            json_str_or_path = p.read_text()
        data = json.loads(json_str_or_path)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        return f"System(n={self.n}, G={self.G}, eps={self.epsilon})"
