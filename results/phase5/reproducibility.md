# Reproducibility Guide

## Software Dependencies

- Python 3.10+
- mpmath 1.4.0 (arbitrary precision + interval arithmetic)
- numpy 2.2.6
- scipy 1.15.3
- matplotlib 3.10.8
- seaborn 0.13.2
- cvxpy 1.7.5

Install: `pip install mpmath numpy scipy matplotlib seaborn cvxpy`

## Scripts and Commands

### Phase 2: Baseline Computations

```bash
# Run conformal mapping toolkit tests (7 tests, all should pass)
python3 results/phase2/conformal_toolkit.py
# Output: results/phase2/toolkit_tests.json

# Reproduce Skinner analysis
python3 results/phase2/reproduce_skinner.py
# Output: results/phase2/skinner_reproduction.json

# Scan domain families
python3 results/phase2/domain_families.py
# Output: results/phase2/domain_families_results.json
```

### Phase 3: Core Research

```bash
# Lower bound analysis (includes Grunsky + random search)
python3 results/phase3/lower_bound_approach.py
# Output: results/phase3/lower_bound_results.json

# Upper bound search (polynomial optimization)
python3 results/phase3/upper_bound_approach.py
# Output: results/phase3/upper_bound_numerics.json

# Interval arithmetic verification
python3 results/phase3/interval_proof.py
# Output: results/phase3/interval_verification.json
```

### Figures

```bash
# Generate all figures
python3 figures/generate_figures.py
# Output: figures/bounds_timeline.png, extremal_domain.png, constant_chain.png (+ PDF versions)
```

## Key Output Files

| File | Description |
|------|-------------|
| `results/phase2/toolkit_tests.json` | Conformal toolkit test results |
| `results/phase2/skinner_reproduction.json` | Skinner bound analysis |
| `results/phase2/domain_families_results.json` | Domain family scan |
| `results/phase3/lower_bound_results.json` | Lower bound computation |
| `results/phase3/upper_bound_numerics.json` | Upper bound search |
| `results/phase3/interval_verification.json` | Interval arithmetic results |
| `results/phase5/new_bounds_summary.json` | Summary of all bounds |

## Deterministic Seeds

All random computations use `np.random.seed(42)` for reproducibility.

## Verification Checklist

1. ✅ Strip map inradius = pi/4 (to 50 digits)
2. ✅ Koebe 1/4 theorem verified via interval arithmetic
3. ✅ Landau constant upper bound = 0.5432589653...
4. ✅ Ahlfors-Grunsky conjecture value = 0.4718616535...
5. ✅ Identity function B_f ≈ 1.0
6. ✅ Certified cubic upper bound B_u ≤ 0.7975
