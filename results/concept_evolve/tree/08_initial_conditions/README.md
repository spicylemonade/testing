# INITIAL_CONDITIONS_GALLERY

A library of analytically-motivated starting configurations: Kepler two-body, circular N-ring, Plummer sphere, Pythagorean three-body, figure-eight choreography. Each tests a different regime of the simulator.

## Mathematical Formalization

Kepler: v_circular = sqrt(G*M/r), e in [0,1).  Plummer: rho(r) = (3M/4pi*a^3)(1 + r^2/a^2)^(-5/2).  Figure-eight: x1(0) = -x3(0) = (0.97, -0.24), v1(0) = v2(0)/2, periodic solution of 3-body problem.

## Analogical Connections

- Initial conditions <-> dataset splits in ML (each IC tests a different failure mode)
- Plummer sphere <-> Gaussian mixture model (smooth density profile, analytically tractable)
- Pythagorean 3-body <-> chaotic time series benchmark (sensitive dependence on initial conditions)

## Implementation Hypothesis

Factory functions: kepler_orbit(m1,m2,a,e), plummer_sphere(N,M,a), ring(N,R), figure_eight(). Each returns (positions, velocities, masses) arrays. ~50 lines total.

## Experiment Seed

Run all 5 initial conditions for 100 time units. For Kepler: verify period. For ring: measure time to instability. For figure-eight: measure how many periods before numerical chaos breaks the choreography.
