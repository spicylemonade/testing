# Baseline Design Review

## Researcher Pass

- Proposed architecture source: `results/baseline_architecture.md`
- Proposed metric pack source: `results/benchmark_spec.md`
- Proposed comparator set source: `results/comparison_plan.md`
- Baseline runtime under review: Python direct-sum leapfrog kernel in `src/minigrav/`

## Reviewer Audit

### 1. Risk: analytic durations do not always divide cleanly by `dt`
- Why it matters: benchmark horizons can silently drift if scenarios round duration differently across runtimes.
- Disposition: fixed immediately by adding an optional `steps` override to the scenario format and documenting that choice in `results/baseline_architecture.md`.

### 2. Risk: current baseline outputs are too verbose for long experiment sweeps
- Why it matters: saving every position and velocity sample for every run will bloat `results/` and make later benchmark summaries harder to scan.
- Disposition: accepted for the baseline kernel only; Phase 4 harness will add thinned report tables and figure-ready summaries while preserving machine-readable traces where needed.

### 3. Risk: external comparator adapters do not exist yet
- Why it matters: the comparison plan is frozen, but REBOUND, poliastro, and classroom-Euler runner code is still missing.
- Disposition: mandatory follow-up before item_018; do not start benchmark claims until all three adapters exist.

### 4. Risk: SI and normalized-unit handling is documented but not yet validated
- Why it matters: silent unit mismatch would undermine analytic controls and cross-runtime reproducibility.
- Disposition: keep all current scenarios in normalized units, and treat explicit SI validation as required debt in scenario IO before final documentation is closed.

### 5. Risk: close-encounter behavior is still hidden inside the baseline kernel's fixed-step assumptions
- Why it matters: this is the main falsifier branch for H1, and the current kernel only measures drift after the fact.
- Disposition: Phase 3 must add encounter-aware triggers, reversibility diagnostics, and a failure envelope instead of pretending the baseline already solves close passes.

### 6. Risk: cross-runtime reproducibility path is not implemented yet
- Why it matters: the H1 claim explicitly depends on replaying the same scenarios in at least two runtimes or numeric targets.
- Disposition: Node.js mirror is required before item_019 can pass.

### 7. Risk: current benchmark spec has thresholds but no automated pass/fail renderer yet
- Why it matters: manual threshold checking invites inconsistency once the experiment matrix expands.
- Disposition: benchmark harness must emit pass/fail flags directly into machine-readable outputs during Phase 4.
