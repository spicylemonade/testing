# Solar System Validation

**Date:** 2026-03-03
**Rubric Item:** item_019

**Simulation:** 40000 steps, dt=0.0001 yr, total time = 4.0 years
**Integrator:** Leapfrog (KDK)
**Energy drift:** 8.78e-10

| Planet | Measured T (yr) | Known T (yr) | Error (%) |
|--------|----------------|-------------|-----------|
| Mercury | 0.2358 | 0.2408 | 2.1 |
| Venus | 0.6133 | 0.6152 | 0.3 |
| Earth | 1.0000 | 1.0000 | 0.0 |
| Mars | 1.8813 | 1.8809 | 0.0 |

## Analysis

All four inner planets show orbital periods matching known values within 2.5%.
The leapfrog integrator maintains energy conservation to ~1e-8 relative drift
over 4 years of simulated time, confirming the symplectic property.

The initial conditions use circular orbits with v = 2*pi*a/T for each planet.
The gravitational constant G = 4*pi^2 AU^3/(M_sun * yr^2) gives natural units.