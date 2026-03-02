"""Conservation law metrics for N-body simulation validation.

Computes total kinetic energy, gravitational potential energy, linear
momentum, and angular momentum. These are the primary correctness signals:
a simulation that doesn't conserve energy is wrong.

References:
  - Noether's theorem: every continuous symmetry yields a conserved quantity
  - Time translation symmetry -> energy conservation
  - Spatial translation symmetry -> momentum conservation
  - Rotational symmetry -> angular momentum conservation
"""

from __future__ import annotations

import numpy as np

from .bodies import G


def kinetic_energy(vel: np.ndarray, mass: np.ndarray) -> float:
    """Compute total kinetic energy.

    K = sum_i (1/2 * m_i * |v_i|^2)

    Args:
        vel: Velocities (N, d).
        mass: Masses (N,).

    Returns:
        Total kinetic energy (scalar).
    """
    v2 = np.sum(vel**2, axis=1)
    return 0.5 * np.sum(mass * v2)


def potential_energy(
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> float:
    """Compute total gravitational potential energy.

    W = sum_{i<j} (-G * m_i * m_j / sqrt(|r_ij|^2 + eps^2))

    Args:
        pos: Positions (N, d).
        mass: Masses (N,).
        eps: Plummer softening length.

    Returns:
        Total potential energy (scalar, negative for bound systems).
    """
    n = pos.shape[0]
    pe = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            rij = pos[j] - pos[i]
            r2 = np.dot(rij, rij) + eps**2
            pe -= G * mass[i] * mass[j] / np.sqrt(r2)
    return pe


def potential_energy_vectorized(
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> float:
    """Vectorized potential energy computation.

    Uses O(N^2) memory but much faster for large N.

    Args:
        pos: Positions (N, d).
        mass: Masses (N,).
        eps: Plummer softening length.

    Returns:
        Total potential energy.
    """
    rij = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
    r2 = np.sum(rij**2, axis=2) + eps**2
    np.fill_diagonal(r2, np.inf)  # Avoid self-interaction

    r_inv = 1.0 / np.sqrt(r2)
    # Mass product matrix
    mm = mass[:, np.newaxis] * mass[np.newaxis, :]
    # Sum upper triangle only (i < j)
    pe = -G * np.sum(np.triu(mm * r_inv, k=1))
    return pe


def total_energy(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> float:
    """Compute total energy E = K + W.

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).
        eps: Plummer softening length.

    Returns:
        Total energy.
    """
    return kinetic_energy(vel, mass) + potential_energy(pos, mass, eps)


def total_momentum(vel: np.ndarray, mass: np.ndarray) -> np.ndarray:
    """Compute total linear momentum vector.

    P = sum_i (m_i * v_i)

    Args:
        vel: Velocities (N, d).
        mass: Masses (N,).

    Returns:
        Total momentum vector, shape (d,).
    """
    return np.sum(mass[:, np.newaxis] * vel, axis=0)


def angular_momentum(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
) -> float:
    """Compute total angular momentum (2D: scalar, 3D: z-component).

    L = sum_i m_i * (r_i x v_i)

    In 2D: L = sum_i m_i * (x_i * vy_i - y_i * vx_i)

    Args:
        pos: Positions (N, d).
        vel: Velocities (N, d).
        mass: Masses (N,).

    Returns:
        Total angular momentum (scalar for 2D).
    """
    d = pos.shape[1]
    if d == 2:
        # L_z = sum(m * (x*vy - y*vx))
        return np.sum(mass * (pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]))
    elif d == 3:
        cross = np.cross(pos, vel)
        return np.sum(mass[:, np.newaxis] * cross, axis=0)
    else:
        raise ValueError(f"Angular momentum only supported for d=2 or d=3, got {d}")


def virial_ratio(
    vel: np.ndarray,
    pos: np.ndarray,
    mass: np.ndarray,
    eps: float = 0.01,
) -> float:
    """Compute the virial ratio 2K/|W|.

    For a system in virial equilibrium, 2K/|W| = 1.

    Args:
        vel: Velocities (N, d).
        pos: Positions (N, d).
        mass: Masses (N,).
        eps: Plummer softening length.

    Returns:
        Virial ratio (should be ~1.0 for equilibrium).
    """
    K = kinetic_energy(vel, mass)
    W = potential_energy(pos, mass, eps)
    if abs(W) < 1e-30:
        return float("inf")
    return 2.0 * K / abs(W)
