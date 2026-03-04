# Stochastic Particle Process for LCS

## Topic Context

The Chvátal-Sankoff constant γ₂ ≈ 0.81 governs the expected length of the longest common subsequence (LCS) of two random binary strings of length n: E[LCS(n,n)] ~ γ₂·n. Tiskin (2022, arXiv:2212.01582) made a breakthrough by connecting γ₂ to the stationary density of a stochastic particle process.

The key insight is that the incremental LCS scores (how LCS changes as we extend the strings by one character) can be encoded as particles on a lattice. These particles evolve according to specific interaction rules derived from the combinatorial structure of LCS (specifically, from the algebra of unit-Monge matrices). In the stationary regime, the particle density ρ determines γ₂.

This bridges:
- **Statistical mechanics**: particle systems, equilibrium measures
- **Combinatorics**: LCS structure, unit-Monge matrices
- **Probability**: ergodic theory, stochastic processes

## Current State of Knowledge

- Best lower bound on γ₂: **0.792666** (Heineman et al. 2024)
- Best upper bound on γ₂: **0.826280** (Lueker 2003)
- Best numerical estimate: **≈ 0.8118** (Bundschuh 2001, with finite-size scaling)
- Tiskin's particle process: provides a new computational framework but exact stationary distribution is unknown

## Implementation Backlog

1. **Implement Tiskin particle process simulator** (Priority: HIGH)
   - Language: Rust or C for performance
   - System sizes: L = 10^2 to 10^6
   - Measure: stationary density, correlation functions

2. **Finite-size scaling analysis** (Priority: HIGH)
   - Fit ρ_L = ρ_∞ + c₁/L^α + c₂/L^{2α}
   - Test α = 1 (standard) vs α = 1/3 (KPZ-informed)
   - Extract γ₂ estimate with error bars

3. **Correlation structure analysis** (Priority: MEDIUM)
   - Measure spatial correlations ⟨ρ(x)ρ(x+r)⟩ - ⟨ρ⟩²
   - Determine if correlations are short-range (product measure) or long-range
   - If short-range: cluster expansion may give exact γ₂

4. **Comparison with frog dynamics** (Priority: MEDIUM)
   - Compare Tiskin process with Bukh-Cox frog dynamics
   - Identify structural similarities/differences
   - Test whether periodic-word frog dynamics approximations converge to γ₂

5. **Hydrodynamic limit derivation** (Priority: LOW)
   - Derive the macroscopic PDE for particle density evolution
   - Relate PDE solutions to the Burgers equation (as in TASEP)
   - Use PDE structure to constrain γ₂
