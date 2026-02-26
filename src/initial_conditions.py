"""Initial condition generators for canonical test problems."""

import numpy as np
from src.bodies import Body, System


def kepler_elliptical(e=0.5, G=1.0, M=1.0, m=1e-6, a=1.0, epsilon=1e-10):
    """Create a 2-body elliptical Kepler orbit.

    Args:
        e: eccentricity (0=circular, <1=elliptical)
        G: gravitational constant
        M: central mass
        m: orbiting mass
        a: semi-major axis
        epsilon: softening length

    Returns:
        System starting at periapsis
    """
    r_peri = a * (1 - e)
    v_peri = np.sqrt(G * M * (1 + e) / (a * (1 - e)))

    bodies = [
        Body(mass=M, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=m, position=[r_peri, 0.0], velocity=[0.0, v_peri]),
    ]
    return System(bodies=bodies, G=G, epsilon=epsilon)


def figure_eight(G=1.0, epsilon=1e-10):
    """Create the Chenciner-Montgomery figure-eight 3-body choreography.

    Three equal masses follow a single figure-eight curve.
    Initial conditions from: Chenciner & Montgomery (2000)
    """
    # Precise initial conditions from the literature
    # (Simo 2001 refinement of Chenciner-Montgomery)
    x1 = 0.97000436
    y1 = -0.24308753
    vx3 = -0.93240737
    vy3 = -0.86473146

    bodies = [
        Body(mass=1.0, position=[x1, y1], velocity=[-vx3 / 2, -vy3 / 2]),
        Body(mass=1.0, position=[-x1, -y1], velocity=[-vx3 / 2, -vy3 / 2]),
        Body(mass=1.0, position=[0.0, 0.0], velocity=[vx3, vy3]),
    ]
    return System(bodies=bodies, G=G, epsilon=epsilon)


def plummer_sphere(N=500, total_mass=1.0, a=1.0, G=1.0, epsilon=0.01, seed=42):
    """Generate N bodies from a Plummer model distribution.

    The Plummer model (Plummer 1911) has density:
        rho(r) = (3M / 4*pi*a^3) * (1 + r^2/a^2)^{-5/2}

    Args:
        N: number of bodies
        total_mass: total mass of the system
        a: Plummer scale radius
        G: gravitational constant
        epsilon: softening length
        seed: random seed

    Returns:
        System in approximate virial equilibrium
    """
    rng = np.random.RandomState(seed)
    m_each = total_mass / N
    bodies = []

    for _ in range(N):
        # Sample radius from Plummer CDF: M(<r) = M * r^3 / (r^2 + a^2)^{3/2}
        # Invert: r = a / sqrt( u^{-2/3} - 1 )
        u = rng.uniform(0.01, 1.0)
        r = a / np.sqrt(u ** (-2.0 / 3.0) - 1.0)

        # Random angle in 2D
        theta = rng.uniform(0, 2 * np.pi)
        pos = np.array([r * np.cos(theta), r * np.sin(theta)])

        # Velocity from virial equilibrium (escape speed rejection sampling)
        v_esc = np.sqrt(2 * G * total_mass) * (r**2 + a**2) ** (-0.25)
        while True:
            q = rng.uniform(0, 1)
            g = q**2 * (1 - q**2) ** 3.5
            if rng.uniform(0, 0.1) < g:
                break
        v = q * v_esc
        v_theta = rng.uniform(0, 2 * np.pi)
        vel = np.array([v * np.cos(v_theta), v * np.sin(v_theta)])

        bodies.append(Body(mass=m_each, position=pos, velocity=vel))

    return System(bodies=bodies, G=G, epsilon=epsilon)
