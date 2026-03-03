# Adaptive Timestep Control

## Topic Context

Fixed-timestep integration is wasteful for gravitational systems with widely varying timescales. A binary system at perihelion passage needs tiny dt, but the same system at aphelion can use much larger steps. Adaptive timestepping allocates computational effort where it's needed.

The challenge: naively varying dt breaks symplecticity. The SQQ-PTQ integrator (2025) addresses this via time transformation, maintaining symplectic structure with adaptive steps. Block timestepping (power-of-2 time hierarchies) is a practical compromise used in production N-body codes like GADGET and AREPO.

### Key Ideas
- Timestep criterion based on dynamical timescale
- Global adaptive: one dt for all particles (simple but wasteful)
- Block timestep: per-particle dt rounded to power-of-2 fractions
- Time transformation preserves symplecticity with adaptive steps

### Cross-Domain Connections
- AMR in fluid dynamics (spatial analog of temporal adaptation)
- PID controllers (feedback-based rate adjustment)
- Variable bitrate encoding in video compression

## Implementation Backlog

- [ ] Implement fixed-step leapfrog as baseline
- [ ] Add global adaptive timestep with error estimation
- [ ] Implement Richardson extrapolation for error estimation
- [ ] Add block timestepping with power-of-2 hierarchy
- [ ] Test on eccentric Kepler orbit (e=0.99)
- [ ] Measure force evaluations saved vs fixed timestep
- [ ] Verify energy conservation is not degraded
- [ ] Implement time transformation for symplectic adaptive stepping
