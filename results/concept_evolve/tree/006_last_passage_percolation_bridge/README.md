# Last Passage Percolation Bridge for Chvatal-Sankoff Bounds

## Topic Context

The connection between LCS and last passage percolation (LPP) is deep. Both ask for
the maximum weight of a monotone path through a 2D grid with random weights.

### The Bernoulli Matching Model
In this simplified model, the match indicator 1[x_i = y_j] is replaced by independent
Bernoulli(1/2) random variables. This model is exactly solvable:
- E[LPP]/n -> 2(sqrt(2)-1) = 0.82842...
- Fluctuations are Tracy-Widom distributed (GUE)
- This is in the KPZ universality class

### The True LCS Model
In the real model, 1[x_i = y_j] has correlations: the entries in each row/column are
correlated because they share the character x_i or y_j. These correlations can only
REDUCE the LPP value compared to the independent case.

### The Gap
0.82842 - gamma_2 ~ 0.017 represents the "price of correlations". Rigorously bounding
this gap would tighten the upper bound below Lueker's 0.826280.

## Implementation Backlog

1. [ ] Verify Bernoulli constant 2(sqrt(2)-1) by simulation (n=10000)
2. [ ] Simulate true LCS for same n values
3. [ ] Measure gap E[LPP_Bernoulli - LCS_true]/n vs n
4. [ ] Check convergence rate of the gap
5. [ ] Construct explicit coupling (FKG or Harris inequality)
6. [ ] Prove monotonicity of the coupling
7. [ ] Derive rigorous lower bound on the gap
8. [ ] Compare resulting upper bound with 0.826280
