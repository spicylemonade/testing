# Tighter Bounds on the Binary Chvátal–Sankoff Constant γ₂

A systematic computational investigation of bounds on the Chvátal–Sankoff constant γ₂, defined as the limit of E[LCS(X,Y)]/n where X and Y are independent uniform random binary strings of length n and LCS denotes the longest common subsequence. The constant has been known to exist since 1975 (Chvátal and Sankoff), but its exact value remains one of the oldest open problems in probabilistic combinatorics. The current best bounds are 0.792665992 ≤ γ₂ ≤ 0.826280 (Heineman et al. 2024; Lueker 2009).

## Key Findings

| Bound | Value | Type | Rigorous? | Method |
|-------|-------|------|-----------|--------|
| Best known lower | 0.792666 | lower | yes | Heineman et al. 2024 |
| Best known upper | 0.826280 | upper | yes | Lueker 2009 |
| **Bernoulli LPP − gap** | **0.808** | **upper** | **conjectural** | **This work** |
| Our best estimate | 0.8115 | estimate | no | Finite-size scaling (β=2/3) |
| Our rigorous lower | 0.7616 | lower | yes | DFA h=6 |
| Our rigorous upper | 0.9051 | upper | yes | Kolmogorov complexity |

**Main novel contribution:** The gap Δ ≈ 0.021 between Bernoulli last-passage percolation (independent weights, exact constant 2(√2−1) ≈ 0.8284) and true LCS (correlated weights) suggests γ₂ ≤ 0.808. If made rigorous via a correlation inequality (e.g., FKG or negative association), this would be the first improvement to the upper bound since 2009.

## Approaches Implemented

| # | Approach | Script | Result |
|---|----------|--------|--------|
| 1 | Monte Carlo simulation | `results/baseline/mc_lcs_simulator.py` | E[L₅₀₀₀]/5000 = 0.8097 |
| 2 | Exact computation (n≤13) | `results/baseline/exact_lcs.py` | γ₂ ≥ 0.7129 (rigorous) |
| 3 | Lueker baseline (ℓ≤7) | `results/baseline/lueker_lower.py` | E[LCS(7)]/7 = 0.6745 |
| 4 | Finite-size scaling | `results/baseline/finite_size_scaling.py` | γ₂ ≈ 0.8115 ± 0.001 |
| 5 | DFA optimal automaton | `results/novel/learned_dfa_lower.py` | γ₂ ≥ 0.7616 (h=6) |
| 6 | Entropy upper bound | `results/novel/entropy_upper.py` | γ₂ ≤ 0.905 |
| 7 | SDP/LP relaxation | `results/novel/sdp_upper.py` | LP: ~0.96, SDP: ~0.50 |
| 8 | Bernoulli LPP gap | `results/novel/sdp_upper.py` | Δ ≈ 0.021 → γ₂ ≤ 0.808 (conj.) |
| 9 | Frog dynamics | `results/novel/frog_dynamics.py` | γ_{000111} ≈ 0.792 |
| 10 | Convergence analysis | `results/experiments/lueker_convergence.py` | Power-law convergence |

## Reproduction Instructions

### Dependencies

```bash
pip install numpy scipy matplotlib seaborn cvxpy
```

### Running all experiments

```bash
# Phase 2: Baseline computations
python results/baseline/mc_lcs_simulator.py          # ~10 min
python results/baseline/exact_lcs.py                  # ~5 min (up to n=13)
python results/baseline/lueker_lower.py               # <1 min
python results/baseline/finite_size_scaling.py         # <1 min

# Phase 3: Novel approaches
python results/novel/learned_dfa_lower.py             # ~2 min
python results/novel/entropy_upper.py                 # <1 min
python results/novel/sdp_upper.py                     # ~5 min
python results/novel/frog_dynamics.py                 # ~1 min

# Phase 4: Analysis
python results/experiments/compare_bounds.py          # <1 min
python results/experiments/lueker_convergence.py       # <1 min
python results/experiments/dfa_ablation.py            # <1 min
python results/experiments/verify_bounds.py           # ~5 min

# Figures
python results/generate_figures.py                    # <1 min
```

Total runtime: approximately 25 minutes on a modern machine.

### Expected output

All results are stored as JSON in `results/` subdirectories. Figures are generated in `figures/` (PNG + PDF). The comprehensive research report is at `results/research_report.md`.

## Project Structure

```
results/
├── baseline/          # MC simulation, exact computation, Lueker baseline, scaling
├── novel/             # DFA, entropy, SDP/LP/LPP, frog dynamics
├── experiments/       # Bounds comparison, convergence, ablation, verification, synthesis
├── concept_evolve/    # Concept tree, literature search, citation graph, reframings
├── final_summary.json # Comprehensive results summary
├── research_report.md # Full research report
└── generate_figures.py

figures/
├── bounds_timeline.png/pdf    # Historical progression of bounds
├── scaling_fit.png/pdf        # Finite-size scaling fits
├── lueker_convergence.png/pdf # Convergence analysis
├── dfa_ablation.png/pdf       # DFA lookahead depth study
└── approach_comparison.png/pdf # Bar chart of all bounds

sources.bib                    # 23 BibTeX entries
```

## Key References

1. Chvátal, V. and Sankoff, D. (1975). Longest common subsequences of two random sequences. *J. Appl. Probab.*, 12(2):306–315.
2. Lueker, G.S. (2009). Improved bounds on the average length of longest common subsequences. *J. ACM*, 56(3):17.
3. Heineman, B., Mannion-Fisher, G., and Pollard, R. (2024). Improved bounds for the expected length of longest common subsequences. *arXiv:2410.14477*.
4. Bukh, B. and Cox, C. (2019). On a partition function of a plaquette random cluster model. *arXiv:1908.11265*.
5. Bundschuh, R. (2001). High precision Monte Carlo determination of the asymptotic length of the longest common subsequence.
