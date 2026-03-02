"""Conservation metrics for N-body simulation diagnostics.

Computes total energy, linear momentum, and angular momentum (2D scalar)
with support for relative error tracking.

Reference: Hairer, Lubich & Wanner (2006), Chapter IX
"""

from __future__ import annotations

import numpy as np


def kinetic_energy(masses: np.ndarray, velocities: np.ndarray) -> float:
    """Total kinetic energy: T = sum(0.5 * m_i * |v_i|^2).

    Args:
        masses: (N,) mass array.
        velocities: (N, 2) velocity array.

    Returns:
        Scalar total kinetic energy.
    """
    v_sq = np.sum(velocities ** 2, axis=1)
    return 0.5 * np.sum(masses * v_sq)


def potential_energy(
    masses: np.ndarray,
    positions: np.ndarray,
    G: float = 1.0,
    epsilon: float = 0.01,
) -> float:
    """Total gravitational potential energy with Plummer softening.

    V = -sum_{i<j} G * m_i * m_j / sqrt(|r_ij|^2 + eps^2)

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        G: Gravitational constant.
        epsilon: Plummer softening length.

    Returns:
        Scalar total potential energy (negative for bound systems).
    """
    n = len(masses)
    if n < 2:
        return 0.0

    pe = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            rij = positions[j] - positions[i]
            dist = np.sqrt(np.dot(rij, rij) + epsilon ** 2)
            pe -= G * masses[i] * masses[j] / dist
    return pe


def total_energy(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    G: float = 1.0,
    epsilon: float = 0.01,
) -> float:
    """Total energy E = T + V.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.
        G: Gravitational constant.
        epsilon: Plummer softening length.

    Returns:
        Scalar total energy.
    """
    T = kinetic_energy(masses, velocities)
    V = potential_energy(masses, positions, G, epsilon)
    return T + V


def linear_momentum(masses: np.ndarray, velocities: np.ndarray) -> np.ndarray:
    """Total linear momentum vector: p = sum(m_i * v_i).

    Args:
        masses: (N,) mass array.
        velocities: (N, 2) velocity array.

    Returns:
        (2,) total momentum vector.
    """
    return np.sum(masses[:, np.newaxis] * velocities, axis=0)


def angular_momentum(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
) -> float:
    """Total angular momentum (2D scalar): L = sum(m_i * (x_i * vy_i - y_i * vx_i)).

    In 2D, angular momentum is a scalar (z-component of r x v).

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        velocities: (N, 2) velocity array.

    Returns:
        Scalar total angular momentum.
    """
    cross = positions[:, 0] * velocities[:, 1] - positions[:, 1] * velocities[:, 0]
    return np.sum(masses * cross)


def relative_energy_error(E: float, E0: float) -> float:
    """Relative energy error: (E - E0) / |E0|.

    Args:
        E: Current energy.
        E0: Initial energy.

    Returns:
        Relative energy error. Returns 0.0 if E0 is zero.
    """
    if abs(E0) < 1e-30:
        return 0.0
    return (E - E0) / abs(E0)


def relative_momentum_error(p: np.ndarray, p0: np.ndarray) -> float:
    """Relative momentum error: |p - p0| / |p0|.

    Args:
        p: Current momentum vector.
        p0: Initial momentum vector.

    Returns:
        Relative momentum magnitude error. Returns 0.0 if |p0| is zero.
    """
    p0_mag = np.linalg.norm(p0)
    if p0_mag < 1e-30:
        return np.linalg.norm(p - p0)
    return np.linalg.norm(p - p0) / p0_mag
