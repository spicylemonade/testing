"""Gravitational force computation with Plummer softening.

Brute-force O(N^2) pairwise force calculation exploiting Newton's third law
(F_ij = -F_ji) for a 2x speedup.

References:
  - Plummer (1911) for softening
  - Barnes & Hut (1986) for the tree-based alternative (see tree.py)
"""

from __future__ import annotations

import numpy as np

from .bodies import G


def compute_forces(
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> np.ndarray:
    """Compute gravitational accelerations using brute-force O(N^2).

    Exploits Newton's third law: compute each pair (i, j) with j > i once,
    apply equal and opposite forces.

    Args:
        pos: Positions array, shape (N, d).
        mass: Masses array, shape (N,).
        eps: Plummer softening length.

    Returns:
        Accelerations array, shape (N, d).
    """
    n = pos.shape[0]
    acc = np.zeros_like(pos)

    for i in range(n):
        for j in range(i + 1, n):
            rij = pos[j] - pos[i]
            r2 = np.dot(rij, rij) + eps**2
            r_inv3 = r2 ** (-1.5)

            # Force on i due to j: F = G * mi * mj * rij / |rij|^3
            # Acceleration: a_i += G * mj * rij / |rij|^3
            fij = G * rij * r_inv3
            acc[i] += mass[j] * fij
            acc[j] -= mass[i] * fij  # Newton's third law

    return acc


def compute_forces_vectorized(
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> np.ndarray:
    """Compute gravitational accelerations using vectorized O(N^2).

    Fully vectorized with numpy broadcasting. Faster than the loop version
    for N > ~20, but uses O(N^2) memory for the displacement matrix.

    Args:
        pos: Positions array, shape (N, d).
        mass: Masses array, shape (N,).
        eps: Plummer softening length.

    Returns:
        Accelerations array, shape (N, d).
    """
    # Displacement vectors: rij[i, j] = pos[j] - pos[i], shape (N, N, d)
    rij = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]

    # Squared distances + softening, shape (N, N)
    r2 = np.sum(rij**2, axis=2) + eps**2

    # Inverse cube: 1 / |r|^3, shape (N, N)
    r_inv3 = r2 ** (-1.5)

    # Zero self-interaction
    np.fill_diagonal(r_inv3, 0.0)

    # Acceleration: a_i = G * sum_j(m_j * rij / |rij|^3)
    # Shape: (N, N, d) * (N, N, 1) -> sum over j -> (N, d)
    acc = G * np.sum(rij * r_inv3[:, :, np.newaxis] * mass[np.newaxis, :, np.newaxis], axis=1)

    return acc


def pairwise_force(
    pos1: np.ndarray,
    pos2: np.ndarray,
    m1: float,
    m2: float,
    eps: float = 0.0,
) -> np.ndarray:
    """Compute the gravitational force on body 1 due to body 2.

    Args:
        pos1: Position of body 1, shape (d,).
        pos2: Position of body 2, shape (d,).
        m1: Mass of body 1.
        m2: Mass of body 2.
        eps: Plummer softening length.

    Returns:
        Force vector on body 1 due to body 2, shape (d,).
    """
    r = pos2 - pos1
    r2 = np.dot(r, r) + eps**2
    return G * m1 * m2 * r * r2 ** (-1.5)
