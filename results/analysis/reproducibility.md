# Reproducibility Package

## 1. Environment

- **Python:** 3.10+
- **C compiler:** GCC with `-O3 -shared -fPIC` flags
- **OS:** Linux (tested on Ubuntu-based container)

## 2. Dependencies

```
numpy>=1.21
scipy>=1.7
matplotlib>=3.5
seaborn>=0.11
```

Optional (not used in final experiments):
```
torch  # Was planned for neural certificate but not needed
```

## 3. Compilation

The C shared library must be compiled before running experiments:

```bash
cd results/baselines/
gcc -O3 -shared -fPIC -o lcs_fast.so lcs_fast.c
```

## 4. Script Invocations

### Phase 2: Baselines

```bash
# Monte Carlo LCS estimator
python3 results/baselines/monte_carlo_lcs.py
# Expected runtime: ~5 minutes
# Output: results/baselines/mc_estimates.json

# DFA lower bounds (online matching)
python3 results/baselines/dfa_lower_bound.py
# Expected runtime: ~2 minutes
# Output: results/baselines/dfa_lower_bounds.json

# Upper bound baselines
python3 results/baselines/upper_bound_baseline.py
# Expected runtime: ~3 minutes
# Output: results/baselines/upper_bounds.json

# Windowed DP estimator
python3 results/baselines/windowed_lcs.py
# Expected runtime: ~10 minutes (n=100000 trials)
# Output: results/baselines/windowed_estimates.json
```

### Phase 3: Novel Approaches

```bash
# Particle process / KPZ scaling
python3 results/novel/particle_process.py
# Expected runtime: ~5 minutes
# Output: results/novel/particle_estimates.json
#         figures/particle_convergence.png

# Frog dynamics
python3 results/novel/frog_dynamics.py
# Expected runtime: ~2 minutes
# Output: results/novel/frog_results.json
#         figures/frog_gamma_by_period.png

# Neural certificate
python3 results/novel/neural_certificate.py
# Expected runtime: ~1 minute
# Output: results/novel/improved_lower_bound.json

# Scaled upper bound
python3 results/novel/scaled_upper_bound.py
# Expected runtime: ~3 minutes
# Output: results/novel/scaled_upper_bound.json
#         figures/scaled_upper_bound.png

# Entropy upper bound
python3 results/novel/entropy_upper_bound.py
# Expected runtime: ~2 minutes
# Output: results/novel/entropy_upper_bound.json
```

### Phase 4: Experiments

```bash
# Lower bound comparison
python3 results/experiments/lower_bound_comparison.py
# Expected runtime: <1 minute
# Output: results/experiments/lower_bound_comparison.json
#         figures/lower_bound_comparison.png

# Upper bound comparison
python3 results/experiments/upper_bound_comparison.py
# Expected runtime: <1 minute
# Output: results/experiments/upper_bound_comparison.json
#         figures/upper_bound_comparison.png

# Convergence analysis
python3 results/experiments/convergence_analysis.py
# Expected runtime: <1 minute
# Output: results/experiments/scaling_fit.json
#         figures/convergence_analysis.png

# Best bounds extraction
python3 results/experiments/best_bounds.py
# Expected runtime: <1 minute
# Output: results/experiments/best_bounds.json
```

## 5. Random Seeds

All experiments use deterministic seed `SEED = 42` via `numpy.random.default_rng(42)`.

Reproducing exact numerical results requires:
- Same NumPy version (random number generator implementation)
- Same C compiler and optimization level
- Same system architecture (floating-point behavior)

## 6. Total Runtime

| Phase | Estimated Time |
|-------|---------------|
| Phase 2 (Baselines) | ~20 minutes |
| Phase 3 (Novel) | ~13 minutes |
| Phase 4 (Experiments) | ~3 minutes |
| **Total** | **~36 minutes** |

## 7. Output Structure

```
results/
├── baselines/
│   ├── lcs_fast.c          # C source
│   ├── lcs_fast.so          # Compiled library
│   ├── monte_carlo_lcs.py
│   ├── mc_estimates.json
│   ├── dfa_lower_bound.py
│   ├── dfa_lower_bounds.json
│   ├── upper_bound_baseline.py
│   ├── upper_bounds.json
│   ├── windowed_lcs.py
│   └── windowed_estimates.json
├── novel/
│   ├── particle_process.py
│   ├── particle_estimates.json
│   ├── frog_dynamics.py
│   ├── frog_results.json
│   ├── neural_certificate.py
│   ├── improved_lower_bound.json
│   ├── scaled_upper_bound.py
│   ├── scaled_upper_bound.json
│   ├── entropy_upper_bound.py
│   ├── entropy_upper_bound.json
│   └── entropy_bound_derivation.md
├── experiments/
│   ├── lower_bound_comparison.py
│   ├── lower_bound_comparison.json
│   ├── upper_bound_comparison.py
│   ├── upper_bound_comparison.json
│   ├── convergence_analysis.py
│   ├── scaling_fit.json
│   ├── best_bounds.py
│   ├── best_bounds.json
│   └── transferability_assessment.json
├── analysis/
│   ├── results_summary.md
│   ├── concept_tree_synthesis.md
│   ├── reproducibility.md      (this file)
│   ├── bib_validation.json
│   └── executive_summary.md
├── concept_evolve/
│   ├── tree/                   (12 concept folders)
│   ├── concept_cards.json
│   ├── semantic_bridge.json
│   ├── steering_directions.json
│   └── ...
figures/
├── particle_convergence.png/pdf
├── frog_gamma_by_period.png/pdf
├── convergence_analysis.png/pdf
├── lower_bound_comparison.png/pdf
├── upper_bound_comparison.png/pdf
└── scaled_upper_bound.png/pdf
```
