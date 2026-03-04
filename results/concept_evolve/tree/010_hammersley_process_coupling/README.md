# Hammersley Process Coupling for Chvatal-Sankoff Bounds

## Topic Context

The Hammersley process is a classical particle system where points are placed randomly in a
square and the longest increasing path through them determines the LPP time. For uniformly
random points in [0,1]^2, the LPP time scales as 2*sqrt(n), connecting to the Ulam problem.

For the discrete version with Bernoulli(1/2) point placement (the Bernoulli matching model),
the LPP constant is exactly 2(sqrt(2)-1) = 0.82842...

The true LCS model introduces correlations (the match indicators 1[x_i=y_j] in a given row
or column are correlated). Georgiou and Ortmann (2018) introduced an "exploration penalty"
that smoothly interpolates between independent and correlated models.

## Proposed Bound Approach

1. At zero penalty: LPP constant = 0.82842 (Bernoulli model)
2. Increase penalty to match correlation structure of true LCS
3. The LPP constant decreases monotonically with penalty
4. The value at the correct penalty equals gamma_2
5. Any intermediate penalty gives a rigorous upper bound

## Implementation Backlog

1. [ ] Implement Bernoulli LPP simulation and verify constant 0.82842
2. [ ] Implement discrete Hammersley process with tunable penalty
3. [ ] Measure E[T_n]/n for penalty = 0, 0.01, 0.02, ..., 0.20
4. [ ] Characterize the correlation structure of true LCS model
5. [ ] Find penalty value matching the true model's correlations
6. [ ] Prove the coupling is monotone (FKG/Harris inequality)
7. [ ] Report resulting upper bound
