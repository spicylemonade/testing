# Problem Statement: Minimal Gravity Simulator

## Primary objective

Build a deterministic, minimal Newtonian gravity simulator that remains numerically stable over long horizons while meeting explicit thresholds for conservation fidelity, orbit accuracy, and step-time performance.

## Research questions

1. Which fixed-step integrator gives the best stability/performance trade-off for minimal implementation complexity?
2. How sensitive are drift and orbit error metrics to timestep size across two-body, three-body, and random N-body scenarios?
3. Can we preserve reproducibility and physical fidelity while scaling to larger N values needed for throughput experiments?

## Success metrics and target thresholds

| Metric | Definition | Target threshold |
| --- | --- | --- |
| Energy drift | `max_t |E(t)-E(0)| / |E(0)| * 100` | `<= 0.10%` |
| Angular momentum drift | `max_t ||L(t)-L(0)|| / ||L(0)|| * 100` | `<= 0.01%` |
| Orbit error | Two-body RMS position error normalized by initial radius | `<= 1.0%` |
| Runtime per step | Median wall-clock step time on benchmark scenario | `<= 1.0 ms/step` for baseline N=256 |

These thresholds define pass/fail criteria used later in experiment statistics and final claims.
