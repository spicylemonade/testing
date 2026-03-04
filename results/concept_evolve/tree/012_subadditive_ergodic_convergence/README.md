# Subadditive Ergodic Theory and Convergence

## Topic Context

The foundational result in the theory of random LCS is Chvátal and Sankoff's (1975) proof that E[LCS(n,n)]/n converges to a constant γ₂ as n → ∞. This follows from the subadditivity of E[LCS(n,n)] and Kingman's subadditive ergodic theorem (or the simpler Fekete's lemma for the expected value).

### Key Questions
1. **Rate of convergence**: How fast does E[LCS(n,n)]/n approach γ₂?
   - Alexander (1994): O(n^{-1/3+ε}) — surprisingly fast if true
   - KPZ prediction: O(n^{-1/3}) with known prefactor

2. **Fluctuations**: What is Var[LCS(n,n)]?
   - Trivial bound: O(n) from Azuma-Hoeffding
   - KPZ prediction: Θ(n^{2/3})
   - Proving Var = o(n) is open (except for special cases)

3. **Concentration**: How tightly is LCS concentrated around its mean?
   - Azuma-Hoeffding: P[|LCS - E[LCS]| > t] ≤ 2exp(-2t²/n)
   - Talagrand: P[|LCS - Med[LCS]| > t] ≤ 4exp(-t²/(4n))
   - Tighter bounds possible using LCS-specific structure

## Significance for Bounding γ₂

Better convergence rate bounds directly improve the quality of Monte Carlo estimates. If we know that |E[LCS(n,n)]/n - γ₂| ≤ C/n^α, then simulations at length n give γ₂ to within ±C/n^α + statistical error. The α = 1/3 rate (if confirmed) means n = 10^6 gives ~10^{-2} accuracy in the convergence term.

## Implementation Backlog

1. **Variance estimation** (Priority: HIGH)
   - Compute Var[LCS(n,n)] for many n values
   - Fit power law Var ~ n^{2χ}
   - Determine χ empirically

2. **Convergence rate estimation** (Priority: HIGH)
   - Plot E[LCS(n,n)]/n vs n on log-log scale
   - Extract convergence exponent
   - Compare with Alexander's theoretical bound

3. **Improved concentration inequality** (Priority: MEDIUM)
   - Apply Efron-Stein with LCS-specific structure
   - Try tensorization / modified log-Sobolev approach
   - Derive tighter exponential bounds

4. **Large deviation rate function** (Priority: LOW)
   - Estimate P[LCS(n,n) ≥ xn] for various x
   - Compute rate function I(x) = -lim (1/n) log P[LCS ≥ xn]
   - Find zero of I(x) (should be at x = γ₂)
