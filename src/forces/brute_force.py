"""Brute-force O(N^2) gravitational force computation using Python loops."""

import numpy as np
from src.bodies import System


def compute_forces(system: System) -> np.ndarray:
    """Compute gravitational acceleration on each body via direct summation.

    Uses pairwise force calculation F = G*m1*m2 * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^{3/2}
    with softening parameter epsilon to avoid singularities.

    Returns:
        accelerations: array of shape (N, dim) with acceleration for each body
    """
    n = system.n
    pos = system.positions
    masses = system.masses
    G = system.G
    eps2 = system.epsilon ** 2

    acc = np.zeros_like(pos)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            rij = pos[j] - pos[i]
            dist2 = np.dot(rij, rij) + eps2
            dist3 = dist2 ** 1.5
            acc[i] += G * masses[j] * rij / dist3

    return acc
