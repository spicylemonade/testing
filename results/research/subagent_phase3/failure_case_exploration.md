# Phase-3 Failure-Case Exploration (Subagent)

- Subagent type: `explore`
- Task id: `ses_34e11ebebffeMNUaj0owcjyMec`

## Identified failure cases

1. **Random-N symplectic regression:** `random_n64` shows worse energy drift for symplectic vs baseline in `results/research/symplectic_eval.json`.
2. **Relative-improvement masking:** three-body scenario passes improvement threshold while absolute drift remains far above target thresholds.
3. **Integrator/force confounding:** current `barnes_hut` method uses Euler stepping, so force and integrator effects can be conflated.
4. **N-threshold discontinuity:** Barnes-Hut direct fallback near `bh_min_n` can introduce regime jumps around N=64.
5. **Theta over-approximation risk:** high theta values increase throughput while amplifying trajectory error.
6. **Center-of-mass drift risk in approximation mode:** approximate forces may introduce net-force asymmetry compared with direct pairwise updates.
7. **Seed robustness illusion for deterministic scenarios:** two-body and three-body initial states are deterministic regardless of seed.
8. **Metric contract mismatch across scripts:** baseline, symplectic, and scaling scripts report non-identical metric definitions.
9. **Instrumentation confounds in runtime comparisons:** differing snapshot frequencies affect measured runtime.

## Diagnostic indicators to monitor

- `improvement_pct < 0` on any scenario-method pair.
- Absolute threshold failures even when relative improvement passes.
- Non-monotonic speed/error behavior under theta sweep.
- Inconsistent ranking across metric pipelines due definition drift.
