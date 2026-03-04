# Finite-Size Scaling and Extrapolation

## Topic Context

Direct Monte Carlo estimation of γ₂ requires computing E[LCS(n,n)]/n and extrapolating n → ∞. The challenge: convergence is slow because E[LCS(n,n)]/n = γ₂ + O(n^{-1/3}) (conjectured KPZ scaling). Bundschuh (2001) addressed this with two innovations:

1. **Multi-spin coding**: Pack 64 binary string pairs into 64-bit machine words. Bitwise operations process all 64 pairs simultaneously, achieving ~64x speedup.

2. **Analytical finite-size scaling**: Instead of blind extrapolation, use the functional form E[LCS(n,n)] = γ₂n + c₁n^{2/3} + c₂n^{1/3} + c₃ + ... motivated by KPZ theory. Fitting multiple parameters to data at several n values gives a much more accurate γ₂ estimate than naive averaging.

### Bundschuh's Estimate
γ₂ ≈ 0.8118 ± 0.0004 (2001, using computers of that era)

## Implementation Backlog

1. **Modern multi-spin coded LCS** (Priority: HIGH)
   - Implement in C with AVX-512 for 512 simultaneous pairs
   - CUDA version for GPU with thousands of parallel pairs
   - Validate against exact computation for small n

2. **Systematic finite-size scaling** (Priority: HIGH)
   - Generate data at n = 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000
   - Fit multiple ansätze and compare
   - Use Bayesian model comparison to select best ansatz

3. **PSLQ integer relation detection** (Priority: MEDIUM)
   - If γ₂ estimate achieves 8+ digits, apply PSLQ
   - Test against √2, π, ln 2, etc.
   - Check algebraic numbers of low degree

4. **Variance scaling analysis** (Priority: MEDIUM)
   - Measure Var[LCS(n,n)] for each n
   - Confirm or deny Var ~ n^{2/3} (KPZ prediction)
   - Use variance structure for optimal weighting in γ₂ fit
