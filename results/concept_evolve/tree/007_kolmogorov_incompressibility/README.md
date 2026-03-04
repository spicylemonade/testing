# Kolmogorov Incompressibility Upper Bounds

## Topic Context

The Kolmogorov complexity approach to bounding LCS works as follows:

1. Random binary strings have K(x) ~ n (incompressible)
2. If LCS(x,y) = ell, then x can be described given y using:
   - The LCS positions in x: choose(n, ell) possibilities ~ exp(n * H(ell/n)) descriptions
   - The LCS positions in y: another choose(n, ell) possibilities
   - The non-LCS bits of x: n - ell additional bits
3. Total description: 2 * n * H(ell/n) + (n - ell) bits must be >= n (incompressibility)
4. This gives: H(ell/n) + (1 - ell/n)/2 >= 1/2, yielding ell/n <= 0.8325...

Baeza-Yates et al. refined this with Markov chains. Further refinements are possible by
encoding the alignment structure more efficiently.

## Key Opportunity

The naive encoding treats the two sets of LCS positions as independent choices. But they
are not: they must form a monotone matching. The number of monotone matchings is much smaller
than choose(n,ell)^2, which should improve the bound.

## Implementation Backlog

1. [ ] Verify the basic incompressibility bound: gamma_2 <= 0.8325
2. [ ] Count monotone matchings for small n (relates to Catalan/ballot numbers)
3. [ ] Compute refined encoding length using monotone matching count
4. [ ] Derive improved upper bound
5. [ ] Combine with Markov chain refinement a la Baeza-Yates
6. [ ] Compare with Lueker's 0.826280
