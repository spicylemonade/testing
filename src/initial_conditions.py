"""Initial condition generators for benchmark scenarios.

Provides standard test problems for validating gravity simulation:
circular orbit, figure-eight three-body, Plummer sphere, and solar system.

References:
    - Danby (1988): Kepler orbital mechanics
    - Chenciner & Montgomery (2000): Figure-eight solution
    - Plummer (1911): Plummer density model
"""

from __future__ import annotations

import numpy as np


def circular_two_body(
    M: float = 1.0,
    m: float = 1e-6,
    r: float = 1.0,
    G: float = 1.0,
) -> dict:
    """Generate circular two-body Kepler orbit.

    Central mass M at origin, orbiting mass m at radius r.

    Args:
        M: Central body mass.
        m: Orbiting body mass.
        r: Orbital radius.
        G: Gravitational constant.

    Returns:
        Dict with masses, positions, velocities, period.
    """
    v_circ = np.sqrt(G * (M + m) / r)
    period = 2 * np.pi * r / v_circ

    masses = np.array([M, m])
    positions = np.array([[0.0, 0.0], [r, 0.0]])
    velocities = np.array([[0.0, 0.0], [0.0, v_circ]])

    return {
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
        "period": period,
        "G": G,
        "epsilon": 0.0,
    }


def figure_eight(G: float = 1.0) -> dict:
    """Generate figure-eight three-body initial conditions.

    Three equal-mass bodies tracing a figure-eight path.
    Published initial conditions from Chenciner & Montgomery (2000).

    The initial conditions are given for bodies at positions:
        x1 = (-1, 0), x2 = (1, 0), x3 = (0, 0)
    with the third body at the origin and specific velocities.

    Period approximately T = 6.32591398 (for G=1, m=1).

    Args:
        G: Gravitational constant.

    Returns:
        Dict with masses, positions, velocities, period.
    """
    # Chenciner-Montgomery figure-eight initial conditions
    # From: "A remarkable periodic solution of the three-body problem
    #        in the case of equal masses"
    # Velocities from the Simo (2002) high-precision refinement
    v_x3 = 0.347111
    v_y3 = 0.532728

    masses = np.array([1.0, 1.0, 1.0])
    positions = np.array([
        [-1.0, 0.0],
        [1.0, 0.0],
        [0.0, 0.0],
    ])
    velocities = np.array([
        [v_x3, v_y3],
        [v_x3, v_y3],
        [-2.0 * v_x3, -2.0 * v_y3],
    ])

    # Period for the figure-eight solution
    period = 6.32591398

    return {
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
        "period": period,
        "G": G,
        "epsilon": 0.0,
    }


def plummer_sphere(
    N: int = 100,
    M_total: float = 1.0,
    a: float = 1.0,
    G: float = 1.0,
    seed: int = 42,
) -> dict:
    """Generate random N-body Plummer sphere initial conditions (2D projection).

    The Plummer model has density profile:
        rho(r) = (3M / 4pi a^3) * (1 + r^2/a^2)^(-5/2)

    We sample positions and velocities from the Plummer distribution
    projected onto 2D.

    Args:
        N: Number of bodies.
        M_total: Total mass.
        a: Plummer scale length.
        G: Gravitational constant.
        seed: Random seed for reproducibility.

    Returns:
        Dict with masses, positions, velocities.
    """
    rng = np.random.default_rng(seed)

    # Equal-mass particles
    masses = np.full(N, M_total / N)

    # Sample radii from Plummer distribution using inverse CDF
    # M(r) = M * r^3 / (r^2 + a^2)^(3/2)
    # Inverse: r = a / sqrt(u^(-2/3) - 1) where u ~ Uniform(0, 1)
    u = rng.uniform(0.01, 1.0, N)
    r = a / np.sqrt(u ** (-2.0 / 3.0) - 1.0)

    # Random angles for 2D positions
    theta = rng.uniform(0, 2 * np.pi, N)
    positions = np.column_stack([r * np.cos(theta), r * np.sin(theta)])

    # Velocities: use escape speed fraction for virial equilibrium
    # v_esc(r) = sqrt(2 * G * M(r) / r) where M(r) is enclosed mass
    # For Plummer: v_esc(r) = sqrt(2GM / sqrt(r^2 + a^2))
    v_esc = np.sqrt(2 * G * M_total / np.sqrt(r ** 2 + a ** 2))

    # Sample speed as fraction of escape speed (rejection sampling simplification)
    speed = 0.3 * v_esc * rng.uniform(0.2, 1.0, N)

    # Random velocity directions
    phi = rng.uniform(0, 2 * np.pi, N)
    velocities = np.column_stack([speed * np.cos(phi), speed * np.sin(phi)])

    # Center of mass correction
    total_mass = np.sum(masses)
    com_pos = np.sum(masses[:, np.newaxis] * positions, axis=0) / total_mass
    com_vel = np.sum(masses[:, np.newaxis] * velocities, axis=0) / total_mass
    positions -= com_pos
    velocities -= com_vel

    return {
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
        "G": G,
        "epsilon": 0.05 * a,  # Softening proportional to scale length
        "plummer_a": a,
    }


def solar_system_inner(G: float = 1.0) -> dict:
    """Generate approximate inner solar system initial conditions.

    Simplified 2D model with Sun, Mercury, Venus, Earth, Mars.
    Distances in AU, masses relative to Sun.

    Args:
        G: Gravitational constant (rescaled for AU units).

    Returns:
        Dict with masses, positions, velocities.
    """
    # Masses relative to Sun (Sun = 1.0)
    # Mercury: 1.66e-7, Venus: 2.45e-6, Earth: 3.0e-6, Mars: 3.23e-7
    masses = np.array([1.0, 1.66e-7, 2.45e-6, 3.0e-6, 3.23e-7])

    # Semi-major axes in AU
    a = np.array([0.0, 0.387, 0.723, 1.0, 1.524])

    # Circular orbital velocities: v = sqrt(G*M_sun/a)
    positions = np.zeros((5, 2))
    velocities = np.zeros((5, 2))

    for i in range(1, 5):
        positions[i] = [a[i], 0.0]
        v = np.sqrt(G * masses[0] / a[i])
        velocities[i] = [0.0, v]

    return {
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
        "G": G,
        "epsilon": 0.001,
    }
