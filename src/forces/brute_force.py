"""Brute-force O(N^2) gravitational force computation.

Computes all pairwise Newtonian gravitational forces with Plummer
softening to prevent singularities at zero separation.

Reference: Aarseth (2003), Efstathiou et al. (1985)
"""

from __future__ import annotations

import numpy as np


def compute_forces_brute(
    masses: np.ndarray,
    positions: np.ndarray,
    G: float = 1.0,
    epsilon: float = 0.01,
) -> np.ndarray:
    """Compute gravitational accelerations via direct pairwise summation.

    Uses vectorized numpy operations with Plummer softening:
        F_ij = G * m_j * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^(3/2)

    Args:
        masses: (N,) array of body masses.
        positions: (N, 2) array of body positions.
        G: Gravitational constant.
        epsilon: Plummer softening length.

    Returns:
        (N, 2) array of accelerations for each body.
    """
    n = len(masses)
    if n == 0:
        return np.zeros((0, 2))
    if n == 1:
        return np.zeros((1, 2))

    # Vectorized pairwise displacement: diff[i, j] = positions[j] - positions[i]
    # Shape: (N, N, 2)
    diff = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]

    # Squared distances: (N, N)
    dist_sq = np.sum(diff ** 2, axis=2) + epsilon ** 2

    # Inverse cube with softening: (N, N)
    inv_dist_cube = dist_sq ** (-1.5)

    # Zero out self-interaction (i == j)
    np.fill_diagonal(inv_dist_cube, 0.0)

    # Acceleration on body i from body j:
    # a_i = G * sum_j m_j * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^(3/2)
    # Shape: (N, 2)
    accelerations = G * np.einsum("j,ijk,ij->ik", masses, diff, inv_dist_cube)

    return accelerations
