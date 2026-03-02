# LEAPFROG_CORE

Kick-drift-kick symplectic integrator as the heartbeat of the simulation. Second-order, time-reversible, and energy-conserving over arbitrary time horizons. The minimal viable physics engine.

## Mathematical Formalization

v(t+dt/2) = v(t) + a(x(t)) * dt/2;  x(t+dt) = x(t) + v(t+dt/2) * dt;  v(t+dt) = v(t+dt/2) + a(x(t+dt)) * dt/2.  Symplectic map preserving the 2-form dp ^ dq on phase space.

## Analogical Connections

- Leapfrog <-> BFGS momentum in optimization (half-step velocity update)
- Leapfrog <-> staggered-grid FDTD in electromagnetics (E and H fields offset by half a time step)
- Symplecticity <-> area-preservation in Hamiltonian flow (Liouville's theorem)

## Implementation Hypothesis

A single function `leapfrog_step(pos, vel, mass, dt, force_fn)` operating on Float64Arrays. Expected: energy drift < 1e-10 per orbit for Keplerian two-body. ~15 lines of Python/TS.

## Experiment Seed

Compare energy drift of Euler vs leapfrog vs RK4 on a two-body Kepler orbit (e=0.5) over 1000 periods. Plot |dE/E| vs time. Leapfrog should show bounded oscillation while Euler/RK4 show secular drift.
