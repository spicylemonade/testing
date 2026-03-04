# KPZ Universality and LCS Fluctuations

## Topic Context

The Kardar-Parisi-Zhang (KPZ) universality class is a broad family of stochastic growth models sharing the same fluctuation behavior. Key predictions:
- Fluctuations scale as n^{1/3} (not n^{1/2} as for sums of i.i.d. random variables)
- Limiting distribution is Tracy-Widom (from random matrix theory)
- Two-point correlations decay as n^{2/3}

The LCS of binary strings, viewed as an LPP problem, is conjectured to lie in the KPZ class. This has been proven for related models (geometric weights, exponential weights) but NOT for Bernoulli weights (which correspond to binary LCS).

## Significance for γ₂ Bounds

If KPZ universality holds for binary LCS:
1. **Finite-size corrections** have the form γ₂·n + c·n^{2/3} + ..., enabling better extrapolation
2. **Variance** is Θ(n^{2/3}), giving tighter confidence intervals from simulations
3. **The fluctuation distribution** provides additional data for fitting γ₂

## Implementation Backlog

1. **Numerical fluctuation exponent test** (Priority: HIGH)
   - Compute Var[LCS(n,n)] for many n values
   - Fit Var ~ n^{2χ} and extract χ
   - Test χ = 1/3 vs alternatives

2. **Tracy-Widom distribution test** (Priority: HIGH)
   - Compute centered and scaled LCS distributions
   - Compare with TW-GOE and TW-GUE via KS test

3. **Multi-point correlation analysis** (Priority: MEDIUM)
   - Measure LCS(⌊sn⌋, n) for multiple s values simultaneously
   - Extract correlation structure and compare with Airy process

4. **Finite-size scaling with KPZ ansatz** (Priority: HIGH)
   - Fit E[LCS]/n = γ₂ + c₁·n^{-1/3} + c₂·n^{-2/3} + c₃·n^{-1}
   - Compare γ₂ estimate with that from polynomial scaling ansatz
