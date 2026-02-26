"""Conservation diagnostics: energy, linear momentum, angular momentum."""

import numpy as np
from src.bodies import System


def kinetic_energy(system: System) -> float:
    """Total kinetic energy: sum of 0.5 * m_i * |v_i|^2."""
    v2 = np.sum(system.velocities ** 2, axis=1)
    return 0.5 * np.sum(system.masses * v2)


def potential_energy(system: System) -> float:
    """Total gravitational potential energy: sum over pairs -G*m_i*m_j / r_ij.

    Uses softening to match force computation.
    """
    n = system.n
    pos = system.positions
    masses = system.masses
    G = system.G
    eps2 = system.epsilon ** 2
    pe = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            rij = pos[j] - pos[i]
            dist = np.sqrt(np.dot(rij, rij) + eps2)
            pe -= G * masses[i] * masses[j] / dist
    return pe


def total_energy(system: System) -> float:
    """Total energy = kinetic + potential."""
    return kinetic_energy(system) + potential_energy(system)


def linear_momentum(system: System) -> np.ndarray:
    """Total linear momentum vector: sum of m_i * v_i."""
    return np.sum(system.masses[:, np.newaxis] * system.velocities, axis=0)


def angular_momentum(system: System) -> float:
    """Total angular momentum (scalar for 2D, z-component of cross product).

    L = sum of m_i * (x_i * vy_i - y_i * vx_i)
    """
    m = system.masses
    x = system.positions[:, 0]
    y = system.positions[:, 1]
    vx = system.velocities[:, 0]
    vy = system.velocities[:, 1]
    return np.sum(m * (x * vy - y * vx))
