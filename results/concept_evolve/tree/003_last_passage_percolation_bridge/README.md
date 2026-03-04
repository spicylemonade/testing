# Last Passage Percolation Bridge to LCS

## Topic Context

The longest common subsequence (LCS) of two strings has an exact reformulation as a last-passage percolation (LPP) problem. Given strings a, b of length n, define a grid where cell (i,j) has weight 1 if a_i = b_j and 0 otherwise. The LCS length equals the maximum total weight over all up-right lattice paths from (0,0) to (n,n).

For random binary strings, this becomes LPP with i.i.d. Bernoulli(1/2) weights. The constant γ₂ is the LPP constant for this specific weight distribution.

## Key Connections

- **Exactly solvable LPP**: For geometric and exponential weights, the LPP constant and fluctuation distribution are known exactly (Tracy-Widom). Binary Bernoulli weights are NOT exactly solvable, but universality suggests similar fluctuation behavior.
- **Busemann functions**: These characterize the geodesic structure and competition interfaces in LPP, providing geometric insight into the alignment structure.
- **Shape theorems**: The LPP shape function g(s,t) = lim E[LPP(⌊sn⌋, ⌊tn⌋)]/n exists and is concave.

## Implementation Backlog

1. **Monte Carlo LPP simulation** (Priority: HIGH)
   - Direct simulation of Bernoulli(1/2) LPP on n×n grid
   - Measure LPP(n,n)/n and fluctuations
   - Compare with KPZ predictions

2. **Shape function computation** (Priority: MEDIUM)
   - Compute g(s,1) for s ∈ [0,2] to map the full shape function
   - Relate curvature of g to fluctuation exponents

3. **Busemann function analysis** (Priority: MEDIUM)
   - Compute Busemann functions numerically for finite systems
   - Characterize the competition interface structure
   - Relate to optimal alignment uniqueness/multiplicity

4. **Comparison with solvable models** (Priority: LOW)
   - Compare Bernoulli LPP statistics with geometric LPP (exactly solvable)
   - Test universality of fluctuation distribution
