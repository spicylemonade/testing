# Tropical Geometry of LCS for Chvatal-Sankoff Bounds

## Topic Context

The LCS dynamic programming recurrence uses max and plus operations, which are the basic
operations of the tropical (max-plus) semiring. This means the LCS problem is inherently a
tropical algebraic problem.

The anti-diagonal of the DP table evolves via multiplication by a random max-plus matrix
determined by the next pair of characters (x_i, y_j). The LCS of length-n strings is the
top entry of the product of n such random matrices. By Kingman's subadditive ergodic theorem,
the growth rate (Lyapunov exponent) of this product equals gamma_2.

## Key Insight

The tropical polytope of feasible LCS paths encodes ALL possible optimal alignments.
The vertices of this polytope correspond to distinct alignment types. The number of such
types grows polynomially (not exponentially) in n for fixed string length, which constrains
the optimization landscape.

## Implementation Backlog

1. [ ] Compute the 2^n x 2^n max-plus transition matrices for binary LCS
2. [ ] Implement Lyapunov exponent computation for random matrix products
3. [ ] Measure convergence rate of the exponent (should be O(1/sqrt(n)))
4. [ ] Analyze the tropical eigenspaces of the average transition matrix
5. [ ] Use tropical convexity to bound the exponent from above and below
6. [ ] Connect to Tiskin's semi-local LCS framework
7. [ ] Explore tropical Plucker coordinates of the LCS Grassmannian
