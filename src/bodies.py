"""Particle data structures and initial condition generators.

Uses Structure-of-Arrays (SoA) layout with numpy arrays for maximum
cache coherence and vectorized performance. All state is stored as:
  - pos: (N, d) array of positions
  - vel: (N, d) array of velocities
  - mass: (N,) array of masses

References:
  - Plummer (1911) for the Plummer sphere model
  - Rein & Liu (2012) for initial condition conventions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

# Gravitational constant (set to 1 in natural units)
G = 1.0


@dataclass
class System:
    """N-body system state in SoA layout.

    Attributes:
        pos: Positions array, shape (N, d).
        vel: Velocities array, shape (N, d).
        mass: Masses array, shape (N,).
    """

    pos: np.ndarray
    vel: np.ndarray
    mass: np.ndarray

    @property
    def n(self) -> int:
        """Number of bodies."""
        return self.mass.shape[0]

    @property
    def dim(self) -> int:
        """Spatial dimensionality."""
        return self.pos.shape[1]

    def copy(self) -> "System":
        """Return a deep copy of this system."""
        return System(
            pos=self.pos.copy(),
            vel=self.vel.copy(),
            mass=self.mass.copy(),
        )


def kepler_orbit(
    m1: float = 1.0,
    m2: float = 1.0,
    a: float = 1.0,
    e: float = 0.0,
    d: int = 2,
) -> System:
    """Create a two-body Kepler orbit.

    Bodies are placed at apoapsis with the center of mass at the origin.

    Args:
        m1: Mass of body 1.
        m2: Mass of body 2.
        a: Semi-major axis.
        e: Eccentricity (0 = circular, <1 = elliptical).
        d: Spatial dimensionality (default 2).

    Returns:
        System with 2 bodies on a Keplerian orbit.
    """
    if not (0.0 <= e < 1.0):
        raise ValueError(f"Eccentricity must be in [0, 1), got {e}")

    M = m1 + m2
    # Apoapsis distance
    r_apo = a * (1.0 + e)

    # Positions at apoapsis along x-axis, COM at origin
    r1 = -m2 / M * r_apo
    r2 = m1 / M * r_apo

    # Velocity at apoapsis (vis-viva equation): v_apo = sqrt(G*M/a * (1-e)/(1+e))
    v_apo = np.sqrt(G * M / a * (1.0 - e) / (1.0 + e))
    v1_y = -m2 / M * v_apo
    v2_y = m1 / M * v_apo

    pos = np.zeros((2, d))
    vel = np.zeros((2, d))
    mass = np.array([m1, m2])

    pos[0, 0] = r1
    pos[1, 0] = r2
    vel[0, 1] = v1_y
    vel[1, 1] = v2_y

    return System(pos=pos, vel=vel, mass=mass)


def circular_ring(
    n: int = 8,
    R: float = 1.0,
    m: float = 1.0,
    d: int = 2,
) -> System:
    """Create N equal-mass bodies in a circular ring.

    Bodies are evenly spaced on a circle of radius R. Each body has velocity
    directed tangentially to maintain a circular configuration (approximate
    for N >= 3).

    Args:
        n: Number of bodies.
        R: Ring radius.
        m: Mass per body.
        d: Spatial dimensionality (>= 2).

    Returns:
        System with N bodies on a ring.
    """
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)

    pos = np.zeros((n, d))
    vel = np.zeros((n, d))
    mass = np.full(n, m)

    pos[:, 0] = R * np.cos(angles)
    pos[:, 1] = R * np.sin(angles)

    # Approximate circular velocity: sum of forces from all other bodies
    # For a symmetric ring, the net inward force on one body can be computed.
    # Use virial estimate: v ~ sqrt(G * M_total / R) * correction
    M_total = n * m
    # More accurate: sum pairwise forces for one body
    force_inward = 0.0
    for k in range(1, n):
        theta = 2 * np.pi * k / n
        dist = 2 * R * np.sin(theta / 2)
        # Component of force toward center
        force_inward += G * m * m / dist**2 * np.sin(theta / 2)

    v_circ = np.sqrt(force_inward * R / m) if force_inward > 0 else 0.0

    # Tangential velocity (perpendicular to radius)
    vel[:, 0] = -v_circ * np.sin(angles)
    vel[:, 1] = v_circ * np.cos(angles)

    return System(pos=pos, vel=vel, mass=mass)


def plummer_sphere(
    n: int = 100,
    M: float = 1.0,
    a: float = 1.0,
    d: int = 2,
    seed: int = 42,
) -> System:
    """Generate an N-body realization of a Plummer sphere.

    Uses inverse CDF sampling for positions and rejection sampling for
    velocities following the Plummer distribution function.

    In 2D, the surface density follows Sigma(R) ~ (1 + R^2/a^2)^{-2}.
    In 3D, the density follows rho(r) ~ (1 + r^2/a^2)^{-5/2}.

    Args:
        n: Number of bodies.
        M: Total mass.
        a: Plummer scale radius.
        d: Spatial dimensionality (2 or 3).
        seed: Random seed for reproducibility.

    Returns:
        System in approximate virial equilibrium.
    """
    rng = np.random.default_rng(seed)

    mass = np.full(n, M / n)

    # --- Position sampling via inverse CDF ---
    if d == 2:
        # 2D Plummer: cumulative mass M(R) = M * R^2 / (R^2 + a^2)
        # Inverse: R = a * sqrt(u / (1 - u)) where u ~ U(0,1)
        u = rng.uniform(0, 0.999, n)  # avoid R -> infinity
        r = a * np.sqrt(u / (1.0 - u))
    elif d == 3:
        # 3D Plummer: cumulative mass M(r) = M * r^3 / (r^2 + a^2)^{3/2}
        # Inverse: r = a / sqrt(u^{-2/3} - 1)
        u = rng.uniform(0.001, 1.0, n)
        r = a / np.sqrt(u ** (-2.0 / 3) - 1.0)
    else:
        raise ValueError(f"Plummer sphere only supports d=2 or d=3, got {d}")

    # Random angles
    if d == 2:
        theta = rng.uniform(0, 2 * np.pi, n)
        pos = np.zeros((n, d))
        pos[:, 0] = r * np.cos(theta)
        pos[:, 1] = r * np.sin(theta)
    else:
        phi = rng.uniform(0, 2 * np.pi, n)
        cos_theta = rng.uniform(-1, 1, n)
        sin_theta = np.sqrt(1 - cos_theta**2)
        pos = np.zeros((n, d))
        pos[:, 0] = r * sin_theta * np.cos(phi)
        pos[:, 1] = r * sin_theta * np.sin(phi)
        pos[:, 2] = r * cos_theta

    # --- Velocity sampling ---
    # Escape velocity at radius r: v_esc = sqrt(2 * |Phi(r)|)
    # Phi(r) = -G*M / sqrt(r^2 + a^2)
    phi_r = -G * M / np.sqrt(r**2 + a**2)
    v_esc = np.sqrt(-2.0 * phi_r)

    # Simplified isotropic velocity assignment:
    # Use velocity dispersion sigma^2 = G*M / (6*sqrt(r^2+a^2)) (3D)
    # For 2D: sigma^2 ~ G*M / (4*sqrt(r^2+a^2))
    if d == 2:
        sigma = np.sqrt(G * M / (4.0 * np.sqrt(r**2 + a**2)))
    else:
        sigma = np.sqrt(G * M / (6.0 * np.sqrt(r**2 + a**2)))

    vel = np.zeros((n, d))
    for i in range(d):
        vel[:, i] = rng.normal(0, sigma)

    # Ensure velocities don't exceed escape velocity
    v_mag = np.sqrt(np.sum(vel**2, axis=1))
    too_fast = v_mag > 0.95 * v_esc
    if np.any(too_fast):
        scale = 0.95 * v_esc[too_fast] / v_mag[too_fast]
        vel[too_fast] *= scale[:, np.newaxis]

    # Center on COM
    com_pos = np.average(pos, weights=mass, axis=0)
    com_vel = np.average(vel, weights=mass, axis=0)
    pos -= com_pos
    vel -= com_vel

    return System(pos=pos, vel=vel, mass=mass)
