"""Optimized force computation: vectorized symmetric pairs.

Exploits Newton's third law in a fully vectorized manner, computing
each pair (i, j) with j > i exactly once. Uses numpy advanced indexing
and scatter-accumulation via np.add.at.

Achieves ~2x speedup and ~2x memory reduction over the full N^2 approach.

References:
  - Concept card NEWTONS_THIRD_EXPLOIT
  - Concept card SOA_STATE
"""

from __future__ import annotations

import numpy as np

from .bodies import G


def compute_forces_symmetric(
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> np.ndarray:
    """Compute gravitational accelerations using vectorized symmetric pairs.

    Only computes forces for the upper triangle of pairs (j > i), then
    applies Newton's third law (F_ij = -F_ji) via scatter accumulation.

    Args:
        pos: Positions array, shape (N, d).
        mass: Masses array, shape (N,).
        eps: Plummer softening length.

    Returns:
        Accelerations array, shape (N, d).
    """
    n = pos.shape[0]
    d = pos.shape[1]

    if n <= 1:
        return np.zeros_like(pos)

    # Pre-compute upper-triangular pair indices
    idx_i, idx_j = np.triu_indices(n, k=1)
    n_pairs = len(idx_i)

    # Displacement vectors for each pair: r_ij = pos[j] - pos[i]
    rij = pos[idx_j] - pos[idx_i]  # shape (n_pairs, d)

    # Squared distances + softening
    r2 = np.sum(rij**2, axis=1) + eps**2  # shape (n_pairs,)

    # Inverse cube
    r_inv3 = r2 ** (-1.5)  # shape (n_pairs,)

    # Force vectors: f_ij = G * rij / |rij|^3 (force per unit mass product)
    fij = G * rij * r_inv3[:, np.newaxis]  # shape (n_pairs, d)

    # Accumulate accelerations using scatter-add
    acc = np.zeros((n, d))

    # a_i += m_j * f_ij (force on i from j)
    weighted_fij_j = fij * mass[idx_j, np.newaxis]  # m_j * f_ij
    weighted_fij_i = fij * mass[idx_i, np.newaxis]  # m_i * f_ij

    np.add.at(acc, idx_i, weighted_fij_j)    # body i gains force from j
    np.add.at(acc, idx_j, -weighted_fij_i)   # body j gains -force from i (Newton's 3rd)

    return acc
