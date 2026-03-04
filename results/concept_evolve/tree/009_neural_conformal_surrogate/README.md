# Neural Conformal Surrogate

## Topic Context

Machine learning approaches to mathematical optimization have shown remarkable success in discovering patterns and accelerating search. For the Bloch constant, the search space is infinite-dimensional (all univalent functions), but truncation to degree N gives a manageable N-dimensional coefficient space.

## Key Idea

Train a neural network as a surrogate for the expensive computation f ↦ B_f. Then use the surrogate to:
1. Rapidly scan the coefficient space for near-extremal functions
2. Identify structural patterns (e.g., coefficient decay rates) of near-extremals
3. Provide warm-start guesses for rigorous optimization methods

## Implementation Backlog

1. **[P0]** Sample random univalent polynomials (rejection sampling on Grunsky)
2. **[P0]** Compute B_f for each sample (numerical conformal mapping)
3. **[P1]** Train surrogate network
4. **[P1]** Use gradient descent on surrogate to find approximate minimizer
5. **[P2]** Validate minimizer with exact B_f computation
6. **[P2]** Analyze coefficient patterns of near-extremals
7. **[P3]** Feed results into SDP (concept 004) and certification (concept 008)
