# Stochastic Particle Duality for Chvatal-Sankoff Bounds

## Topic Context

The LCS problem on random binary strings can be mapped to an interacting particle system
on the integer lattice. Tiskin (2022) constructed a specific stochastic particle process whose
parameters encode the Chvatal-Sankoff constant gamma_2. Amsalu, Matzinger, and Vachkovskaia
(2008) independently established an equivalent interacting particle model in random media,
proving that the average speed of particles converges uniformly.

The key insight is that the LCS growth rate corresponds to the flux of particles in the
hydrodynamic limit. The flux function f(rho) = rho * v(rho) relates particle density rho to
particle velocity v(rho). Bounding this function yields bounds on gamma_2.

## Connection to Bounds

- **Upper bound**: If f(rho) <= f_upper(rho) for a concave function f_upper, then
  gamma_2 <= max_rho f_upper(rho). The Bernoulli matching model provides such an
  upper envelope.
- **Lower bound**: Constructing explicit particle configurations with provable minimum
  velocity gives lower bounds.

## Implementation Backlog

1. [ ] Reproduce Tiskin's particle process construction from arXiv:2212.01582
2. [ ] Implement Monte Carlo simulation of particle system (N=10000 particles)
3. [ ] Measure flux function f(rho) at 100 density points
4. [ ] Fit convex/concave envelopes to empirical flux data
5. [ ] Derive rigorous bounds from the envelopes
6. [ ] Compare with known bounds (lower: 0.792666, upper: 0.826280)
7. [ ] Investigate connection to TASEP and exact solvability
8. [ ] Study finite-size corrections to the flux function
