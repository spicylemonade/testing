# Replica Free Energy Method for Chvatal-Sankoff Bounds

## Topic Context

The replica method is a powerful (though non-rigorous) technique from statistical physics
for computing quenched averages of disordered systems. Applied to LCS, the idea is:

1. Define a partition function Z(beta) summing over all common subsequences weighted by length
2. The LCS length is the zero-temperature limit of the free energy
3. Use the replica trick to compute E[ln Z] via the analytic continuation of E[Z^m]

Bundschuh (2001) applied this approach to estimate gamma_2 ~ 0.8117 using high-precision
simulations guided by the analytical framework from Hwa and Lassig's work on sequence
alignment scaling laws.

## Relevance to Bounds

- The **annealed approximation** (E[Z] instead of E[ln Z]) gives an upper bound
- The **replica-symmetric (RS) Ansatz** may give tighter bounds if solved correctly
- If replica symmetry breaking (RSB) occurs, the RS bound is not tight and 1RSB gives improvement

## Implementation Backlog

1. [ ] Derive the annealed free energy for binary LCS explicitly
2. [ ] Write RS saddle-point equations
3. [ ] Solve numerically using Newton's method
4. [ ] Check if RS estimate matches Bundschuh's ~0.8117
5. [ ] Investigate whether RSB occurs (check AT stability condition)
6. [ ] If RS is stable, the RS estimate could provide a new rigorous upper bound framework
7. [ ] Compare annealed bound with Dancik-Paterson 0.826280
