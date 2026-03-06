from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from minigrav.core.forces import ForceReport
from minigrav.core.state import BodyState


@dataclass
class InvariantSnapshot:
    kinetic_energy: float
    potential_energy: float
    total_energy: float
    angular_momentum: np.ndarray
    angular_momentum_norm: float
    center_of_mass: np.ndarray
    center_of_mass_velocity: np.ndarray
    min_distance: float
    min_pair: tuple[str, str] | None


def compute_invariants(state: BodyState, force_report: ForceReport) -> InvariantSnapshot:
    kinetic_energy = 0.5 * float(np.sum(state.masses[:, None] * state.velocities**2))
    angular_momentum = np.sum(
        np.cross(state.positions, state.masses[:, None] * state.velocities),
        axis=0,
    )
    center_of_mass = np.sum(state.masses[:, None] * state.positions, axis=0) / state.total_mass
    center_of_mass_velocity = np.sum(state.masses[:, None] * state.velocities, axis=0) / state.total_mass
    total_energy = kinetic_energy + force_report.potential_energy
    return InvariantSnapshot(
        kinetic_energy=kinetic_energy,
        potential_energy=force_report.potential_energy,
        total_energy=total_energy,
        angular_momentum=angular_momentum,
        angular_momentum_norm=float(np.linalg.norm(angular_momentum)),
        center_of_mass=center_of_mass,
        center_of_mass_velocity=center_of_mass_velocity,
        min_distance=force_report.min_distance,
        min_pair=force_report.min_pair,
    )


def _relative_error(value: float, reference: float) -> float:
    scale = max(abs(reference), 1e-12)
    return float(abs(value - reference) / scale)


def compute_relative_drift(current: InvariantSnapshot, initial: InvariantSnapshot) -> dict[str, float]:
    return {
        "energy_rel": _relative_error(current.total_energy, initial.total_energy),
        "angular_momentum_rel": _relative_error(
            current.angular_momentum_norm, initial.angular_momentum_norm
        ),
        "center_of_mass_abs": float(np.linalg.norm(current.center_of_mass - initial.center_of_mass)),
        "center_of_mass_velocity_abs": float(
            np.linalg.norm(current.center_of_mass_velocity - initial.center_of_mass_velocity)
        ),
    }
