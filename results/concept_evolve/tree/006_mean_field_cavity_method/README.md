# Mean-Field Cavity Method for LCS

## Topic Context

The cavity method, a powerful technique from spin glass theory (Mézard, Parisi, Virasoro), can be adapted to the LCS problem. The key idea: replace the correlated match indicators 1_{a_i = b_j} with independent Bernoulli(1/σ) variables, creating a "Bernoulli matching" model that is analytically tractable.

Boutet de Monvel (1998-2000) showed:
- The Bernoulli matching model has an exact cavity solution: γ_BM(σ) = 2/(1 + √(1 + 4/σ))
- For σ = 2: γ_BM ≈ 0.732, significantly below true γ₂ ≈ 0.81
- The gap comes from correlations (if a_i = b_j and a_i = b_k, then automatically b_j = b_k)
- These correlations are long-ranged and non-perturbative in 1/σ

## Key Insight

The "strong coupling" nature of the σ = 2 case makes it the hardest to analyze. As σ → ∞, the Bernoulli matching model becomes exact (correlations vanish). For σ = 2, we need a fundamentally different approach that accounts for the correlation structure.

## Implementation Backlog

1. **Implement cavity solution** (Priority: HIGH)
   - Compute γ_BM(σ) for σ = 2,...,100
   - Compare with Monte Carlo estimates of true γ_σ
   - Quantify the mean-field gap Δ(σ) = γ_σ - γ_BM(σ)

2. **Correlation correction expansion** (Priority: HIGH)
   - Implement k-th order correlation corrections
   - Check convergence of the expansion for σ = 2
   - Determine if expansion is convergent or asymptotic

3. **Belief propagation on DP table** (Priority: MEDIUM)
   - Formulate LCS DP as factor graph
   - Run belief propagation to approximate marginals
   - Extract γ₂ estimate from BP fixed point

4. **Temperature-dependent analysis** (Priority: MEDIUM)
   - Study free energy F(β) = (1/β) log Σ_π exp(β|π|)
   - Compute F(β) via transfer matrix at finite temperature
   - Extrapolate β → ∞ to get γ₂
