from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class BodyState:
    ids: tuple[str, ...]
    masses: np.ndarray
    radii: np.ndarray
    positions: np.ndarray
    velocities: np.ndarray

    def __post_init__(self) -> None:
        n = len(self.ids)
        if self.masses.shape != (n,):
            raise ValueError("masses must have shape (n,)")
        if self.radii.shape != (n,):
            raise ValueError("radii must have shape (n,)")
        if self.positions.shape != (n, 3):
            raise ValueError("positions must have shape (n, 3)")
        if self.velocities.shape != (n, 3):
            raise ValueError("velocities must have shape (n, 3)")

    @property
    def n_bodies(self) -> int:
        return len(self.ids)

    @property
    def total_mass(self) -> float:
        return float(np.sum(self.masses))

    def copy(self) -> "BodyState":
        return BodyState(
            ids=tuple(self.ids),
            masses=self.masses.copy(),
            radii=self.radii.copy(),
            positions=self.positions.copy(),
            velocities=self.velocities.copy(),
        )

    def with_dynamics(self, positions: np.ndarray, velocities: np.ndarray) -> "BodyState":
        return BodyState(
            ids=tuple(self.ids),
            masses=self.masses.copy(),
            radii=self.radii.copy(),
            positions=np.asarray(positions, dtype=float),
            velocities=np.asarray(velocities, dtype=float),
        )
