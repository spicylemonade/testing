"""Vectorized O(N^2) gravitational force computation using NumPy broadcasting."""

import numpy as np
from src.bodies import System


def compute_forces_vectorized(system: System) -> np.ndarray:
    """Compute gravitational acceleration via vectorized direct summation.

    Uses NumPy broadcasting to avoid Python loops over particles.
    F_i = G * sum_j(m_j * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^{3/2})
    """
    pos = system.positions  # (N, dim)
    masses = system.masses  # (N,)
    G = system.G
    eps2 = system.epsilon ** 2

    # Pairwise displacement vectors: diff[i,j] = pos[j] - pos[i]
    diff = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]  # (N, N, dim)

    # Pairwise squared distances + softening
    dist2 = np.sum(diff ** 2, axis=2) + eps2  # (N, N)

    # dist^3 for inverse cube law
    inv_dist3 = dist2 ** (-1.5)  # (N, N)

    # Zero self-interaction
    np.fill_diagonal(inv_dist3, 0.0)

    # Acceleration: a_i = G * sum_j(m_j * diff[i,j] * inv_dist3[i,j])
    acc = G * np.einsum('j,ijk,ij->ik', masses, diff, inv_dist3)

    return acc
