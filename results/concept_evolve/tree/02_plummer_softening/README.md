# PLUMMER_SPHERE_BENCHMARK

The Plummer sphere as a canonical N-body benchmark: analytically known density profile, velocity distribution, and virial equilibrium. The standard testbed for N-body code validation used since Aarseth (1963).

## Mathematical Formalization

rho(r) = (3M/(4*pi*a^3)) * (1 + r^2/a^2)^(-5/2).  Velocity distribution: isotropic Maxwellian with sigma^2(r) = G*M / (6*sqrt(r^2+a^2)).  Virial ratio: 2K/|W| = 1 at equilibrium.  Dynamical time: t_dyn = (R^3/(G*M))^(1/2).

## Analogical Connections

- Plummer sphere <-> Maxwell-Boltzmann gas (thermal equilibrium with gravitational confinement)
- Virial theorem <-> equipartition theorem (energy balance between kinetic and potential modes)
- Plummer relaxation <-> thermalization in statistical mechanics (approach to equilibrium from arbitrary IC)

## Implementation Hypothesis

Generate N bodies from Plummer distribution using inverse CDF sampling. Evolve for 50 t_dyn. Monitor virial ratio and density profile stability. The standard acceptance test for any N-body code.

## Experiment Seed

Initialize N=500 Plummer sphere. Evolve with leapfrog for 50 t_dyn. Plot virial ratio vs time (should oscillate around 1.0). Plot radial density profile at t=0,10,25,50 t_dyn (should be stable). Measure energy drift.
