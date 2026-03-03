# Symplectic Leapfrog Integrator

## Topic Context

The leapfrog method is the gold standard for gravitational N-body integration. Its symplectic property means it exactly preserves the phase-space volume of Hamiltonian dynamics, which translates to bounded energy errors over arbitrary integration times. This is in stark contrast to non-symplectic methods (Euler, RK4) where energy drifts monotonically, eventually destroying the physical fidelity of the simulation.

The method has two equivalent forms: the kick-drift-kick (KDK) and drift-kick-drift (DKD) variants. Higher-order symplectic methods (Yoshida 4th, 6th, 8th order) compose leapfrog steps with different coefficients.

### Key Ideas
- Half-step velocity and position offsets preserve symplectic structure
- One force evaluation per timestep (same cost as Euler)
- Energy error is bounded, oscillating around true value
- Trivially parallelizable: each particle's update is independent
- Equivalent to Störmer-Verlet position integration

### Cross-Domain Connections
- MAC (Marker-and-Cell) staggered grids in CFD
- Alternating direction implicit (ADI) methods in PDE solving
- Neural Symplectic Integrator combines leapfrog with learned Hamiltonians

## Implementation Backlog

- [ ] Implement KDK leapfrog for 2D gravity
- [ ] Implement DKD variant and verify equivalence
- [ ] Implement Euler and RK4 for comparison
- [ ] Benchmark energy conservation: leapfrog vs Euler vs RK4
- [ ] Implement Yoshida 4th-order composition
- [ ] Test on Kepler two-body orbit (analytical solution available)
- [ ] Test on figure-eight three-body choreography
- [ ] Profile: measure single-step cost vs accuracy gain
