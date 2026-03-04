# Information-Theoretic Upper Bounds on γ₂: Mathematical Arguments

## 1. Basic Kolmogorov Complexity Bound

**Theorem 1.** γ₂ ≤ c* where c* ≈ 0.9051 is the unique solution of c = 2H(c) in (0.5, 1).

**Proof sketch.** Let X, Y ∈ {0,1}^n be independent uniform random strings. Let L = LCS(X,Y).

An alignment of length L is specified by:
- The set S_X ⊆ [n] of |S_X| = L positions in X participating in the LCS
- The set S_Y ⊆ [n] of |S_Y| = L positions in Y participating in the LCS

The number of bits to describe S_X is ≤ log₂(C(n,L)), and similarly for S_Y.

Given X and the alignment, Y can be reconstructed:
- The L matched positions of Y equal X restricted to S_X
- The remaining (n-L) positions of Y are free

Since Y is random, K(Y) ≥ n - O(log n). By the chain rule:
  n ≤ K(alignment) + K(Y | X, alignment) + O(log n)
  n ≤ 2 log₂ C(n,L) + (n-L) + O(log n)
  L ≤ 2 log₂ C(n,L) + O(log n)

Setting c = L/n and using log₂ C(n, cn)/n → H(c) (binary entropy):
  c ≤ 2H(c) + o(1)

The equation c = 2H(c) has a solution c* ≈ 0.9051. ∎

**Assessment:** This bound is weaker than Dancik-Paterson (0.838) and much weaker than Lueker (0.826). The weakness comes from ignoring the structure of the LCS problem.

## 2. Refined Encoding via Monotone Alignment

**Theorem 2.** γ₂ ≤ c** where c** ≈ 0.907.

**Proof sketch.** Instead of encoding S_X and S_Y separately, encode the alignment as a monotone walk on the n × n grid. The walk consists of:
- L diagonal (match) steps  
- (n-L) right (skip X) steps
- (n-L) down (skip Y) steps

Total walk length: 2n - L steps. The number of such walks is:
  (2n-L)! / (L! · (n-L)!²)

The encoding rate per character is:
  R(c) = (2-c) · H₃(c/(2-c), (1-c)/(2-c), (1-c)/(2-c))

where H₃ is the ternary entropy. The bound c ≤ R(c) gives c** ≈ 0.907. ∎

**Assessment:** Also weaker than Lueker's bound. The issue is that information-theoretic arguments only capture the "entropy" of the alignment, not the algebraic constraints from the DP recurrence.

## 3. Bernoulli LPP Comparison (Conjectural Upper Bound)

**Conjecture.** γ₂ ≤ 2(√2 - 1) ≈ 0.82843.

**Argument (not rigorous).** Define:
- **LCS model:** w_{ij} = 1[X_i = Y_j] where X, Y are i.i.d. uniform binary. The weights along each row and column are dependent (they share a common random variable X_i or Y_j).
- **Bernoulli model:** w̃_{ij} ~ Bernoulli(1/2) independently. 

The LCS model has the SAME marginal distribution (P(w_{ij} = 1) = 1/2) but with negative correlations within rows and columns. Specifically:
- Cov(w_{ij}, w_{ik}) = P(X_i = Y_j, X_i = Y_k) - 1/4 = P(Y_j = Y_k)/2 - 1/4 = -1/4 + 1/4 = 0 (independent since Y_j, Y_k are independent)

Wait - actually the correlations are more subtle:
- w_{ij} = 1[X_i = Y_j], w_{ik} = 1[X_i = Y_k]
- E[w_{ij} w_{ik}] = P(X_i = Y_j AND X_i = Y_k) = P(X_i = Y_j = Y_k) = P(Y_j = Y_k)/2
- For j ≠ k: E[w_{ij} w_{ik}] = 1/4 (since Y_j, Y_k independent)
- Cov = 1/4 - 1/4 = 0

So within a row, the weights are actually UNCORRELATED (but not independent).
Similarly, within a column. However, there are higher-order dependencies.

The key structural difference: in the Bernoulli model, each w_{ij} is independent; in the LCS model, they are pairwise uncorrelated but not independent (e.g., knowing w_{ij} = 1 and w_{ik} = 1 implies Y_j = Y_k, which constrains w_{lj} and w_{lk}).

**Numerical evidence:**
- Bernoulli LPP: E[T_n]/n → 2(√2-1) ≈ 0.82843
- LCS: E[L_n]/n → γ₂ ≈ 0.8117
- Gap: ~0.017

The gap suggests γ₂ < 2(√2-1), but a rigorous proof requires demonstrating that the higher-order dependence structure strictly reduces the expected last-passage value. This remains an open problem.

## 4. Novel Direction: Conditional Variance Reduction

**Idea.** Consider the variance of LCS(X,Y) conditional on the "row sums" r_i = #{j : X_i = Y_j}. In the LCS model, r_i ~ Binomial(n, 1/2), and Σ r_i = n²/2 almost surely. In the Bernoulli model, the row sums are independent.

The constraint Σ r_i = n²/2 (approximate, but with O(√n) fluctuations) reduces the "effective degrees of freedom" compared to the Bernoulli model. This should reduce the expected LPP value.

A quantitative bound via the second moment:
  E[T_LCS] ≤ E[T_Bernoulli] - Δ(n)

where Δ(n) comes from the conditional variance analysis. If Δ(n)/n → δ > 0, this gives γ₂ ≤ 2(√2-1) - δ.

**Status:** This is a novel research direction that warrants further investigation. The gap δ ≈ 0.017 from MC simulations suggests the bound is achievable.
