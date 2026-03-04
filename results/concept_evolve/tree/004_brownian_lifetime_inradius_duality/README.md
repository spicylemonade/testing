# 004: Brownian Lifetime and Inradius Duality

## Topic Context

The connection between Brownian motion exit times and conformal mapping constants was established by Banuelos and Carroll. For a simply connected planar domain D with inradius R_D, the expected exit time E_z[tau_D] of Brownian motion starting at z is bounded by a universal constant times R_D^2.

The key duality: domains that maximize normalized Brownian exit time are related to domains that are extremal for the Bloch-Landau constant. The torsion function u (solution of Delta u = -2 with u=0 on the boundary) integrates to the expected exit time.

## Key Inequalities

- lambda_1(D) >= pi^2 / (4 * R_D^2) — Banuelos-Carroll
- E_z[tau_D] <= R_D^2 / lambda_1(D)
- Connection to B_u via inradius of the conformal image

## Implementation Backlog

1. [ ] Implement 2D Brownian motion simulator with boundary detection
2. [ ] Compute E_z[tau_D] via Monte Carlo for strip, disk, slit domains
3. [ ] Solve torsion equation via FEM for comparison
4. [ ] Optimize domain shape to maximize normalized exit time
5. [ ] Compare extremal domain shapes with known Bloch candidates
6. [ ] Estimate convergence rate of Monte Carlo estimator
