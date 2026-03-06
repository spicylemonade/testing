from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .state import BodyState


@dataclass(frozen=True)
class ForceConfig:
    gravitational_constant: float
    softening_length: float = 0.0


@dataclass
class ForceReport:
    accelerations: np.ndarray
    pair_count: int
    potential_energy: float
    min_distance: float
    min_pair: tuple[str, str] | None


def compute_pairwise_forces(state: BodyState, config: ForceConfig) -> ForceReport:
    accelerations = np.zeros_like(state.positions)
    potential_energy = 0.0
    min_distance_sq = math.inf
    min_pair: tuple[str, str] | None = None
    pair_count = 0
    epsilon_sq = float(config.softening_length) ** 2

    for i in range(state.n_bodies - 1):
        for j in range(i + 1, state.n_bodies):
            displacement = state.positions[j] - state.positions[i]
            physical_distance_sq = float(np.dot(displacement, displacement))
            if physical_distance_sq < min_distance_sq:
                min_distance_sq = physical_distance_sq
                min_pair = (state.ids[i], state.ids[j])

            softened_distance_sq = physical_distance_sq + epsilon_sq
            inverse_distance = 1.0 / math.sqrt(softened_distance_sq)
            inverse_distance_cubed = inverse_distance / softened_distance_sq
            scale = config.gravitational_constant * inverse_distance_cubed
            contribution = displacement * scale

            accelerations[i] += state.masses[j] * contribution
            accelerations[j] -= state.masses[i] * contribution
            potential_energy -= (
                config.gravitational_constant * state.masses[i] * state.masses[j] * inverse_distance
            )
            pair_count += 1

    min_distance = 0.0 if min_distance_sq is math.inf else math.sqrt(min_distance_sq)
    return ForceReport(
        accelerations=accelerations,
        pair_count=pair_count,
        potential_energy=float(potential_energy),
        min_distance=min_distance,
        min_pair=min_pair,
    )
