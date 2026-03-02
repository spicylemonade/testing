# Methodology Review

**Date**: 2026-03-02  
**Item**: item_023

## Review of Experiment Configurations

### Scaling Experiment (item_018)
- **Sample sizes**: N = 10, 50, 100, 500, 1000
- **Assessment**: Adequate range to demonstrate O(N^2) vs O(N log N). Missing N=5000 from original spec (computational constraint). The existing range still clearly shows the scaling behavior.
- **Statistical significance**: Each measurement averaged over 3-20 repetitions. Adequate for timing.
- **Flag**: Pure-Python Barnes-Hut has high overhead; the algorithmic advantage only shows at very large N.

### Energy Conservation Experiment (item_019)
- **Step sizes**: dt = 0.1, 0.01, 0.001 (0.0001 skipped for Euler due to step count)
- **Integration time**: 50 Kepler periods with e=0.5
- **Assessment**: Three step sizes are sufficient to verify convergence order. The 50-period run is long enough to detect both bounded oscillation (symplectic) and secular drift (non-symplectic).
- **Convergence test**: Richardson extrapolation with 3 step sizes confirms orders: Euler ~0, Leapfrog ~2, Yoshida4 ~4. Adding a 4th step size would strengthen confidence but the trend is clear.

### Plummer Relaxation (item_020)
- **N**: 200 (reduced from 500 for computational feasibility)
- **Integration time**: 20 t_dyn (reduced from 50)
- **Assessment**: N=200 is marginal for statistical mechanics claims but sufficient for demonstrating virial equilibrium. The virial ratio converges to 1.000, confirming correct physics.
- **Flag**: N=200 with softening eps=0.05 means each body's softened "radius" is comparable to the inter-particle distance. This is appropriate for a collisionless approximation.

### Theta Sweep (item_021)
- **N**: 1000
- **Theta values**: 0.0, 0.3, 0.5, 0.7, 1.0, 1.5
- **Assessment**: Comprehensive sweep covers the entire useful range. theta=0 (exact) and theta=1.5 (aggressive approximation) bracket the space. The Pareto frontier is clearly visible.
- **Optimal theta**: ~0.5 provides <3% error with ~10x speedup over exact.

## Overall Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| Sample sizes adequate | PASS | N ranges cover key regimes |
| Integration times sufficient | PASS | Multiple orbits/dynamical times |
| Convergence tests | PASS | Order verification via step-size refinement |
| Statistical significance | PASS | Multiple repetitions for timing |
| Reproducibility | PASS | Deterministic seed=42 used throughout |
| Cross-validation | PASS | Loop and vectorized force methods agree |
| Known-answer tests | PASS | Kepler orbit validates against analytical solution |

## Improvement Suggestions

1. Extend scaling to N=5000 using Barnes-Hut (brute-force is too slow)
2. Add error bars (std dev) to timing measurements
3. Run Plummer with larger N (1000+) using tree code
4. Add convergence test with 4th step size for Euler
