# Verlet Position Integration

## Topic Context

The Störmer-Verlet method is one of the oldest numerical integration schemes (dating to Störmer's 1907 work on charged particles in magnetic fields and Verlet's 1967 application to molecular dynamics). Its simplicity — requiring only positions at two timesteps and accelerations — makes it ideal for minimal implementations.

The method is algebraically equivalent to the leapfrog/velocity-Verlet method, as shown by Jules Jacobs (2019). The position form has a slight advantage in memory (no velocity storage needed) but a disadvantage in that velocity must be recovered via finite differences when needed for energy computation.

### Key Ideas
- No explicit velocity storage: just current and previous positions
- Second-order accurate, symplectic, time-reversible
- Central difference formula connects to PDE finite differences
- Widely used in cloth/soft-body simulation in games

### Cross-Domain Connections
- Central difference methods in PDE solving
- FIR filter design in signal processing
- Cloth/rope physics in game engines (Jakobsen 2001)

## Implementation Backlog

- [ ] Implement position Verlet for 2D gravity
- [ ] Implement velocity Verlet for comparison
- [ ] Verify trajectory equivalence (bitwise or ULP comparison)
- [ ] Benchmark memory: 2*N*d vs 2*N*d + N*d (position vs velocity Verlet)
- [ ] Profile cache performance for large N
- [ ] Add velocity recovery for energy computation
- [ ] Test on Kepler orbit with analytical solution
- [ ] Port to GPU compute shader
