# Baseline Audit

Snapshot date: 2026-03-18 UTC

## Inputs

- `results/baselines/benchmark_spec.md`
- `results/baselines/witness_spec.md`
- `results/verification/verification_summary.md`
- `results/swarm/tool_plan.md`
- `results/swarm/falsifier.md`

Role usage:

- `benchmark_auditor` was launched for this pre-run review.
- `falsifier` guidance was incorporated from the standing falsifier memo plus the current baseline matrix.
- Integration below is a planning-stage synthesis only; no executed audit exists because the exact verifier is still missing.

## Checklist

### Label shuffling

- Judgment: PASS
- Reason:
  - the benchmark spec explicitly requires label-shuffle control at fixed geometry and fixed nonzero-label multiset.

### Decoder leakage

- Judgment: PASS WITH CAVEAT
- Reason:
  - the benchmark spec explicitly requires a decoder-matched baseline using the same compiler, extractor, legality checks, and exact scorer.
  - caveat: this is a design-time pass only; actual leakage cannot be ruled out until an exact evaluator runs.

### Compute parity

- Judgment: PASS
- Reason:
  - the spec fixes equal exact-decode budgets and forbids best-of-many reporting.
  - matched `|X|` and matched edge-density bands are also written explicitly.

### Out-of-distribution grids

- Judgment: PASS
- Reason:
  - the matrix requires held-out larger or different-aspect-ratio grids for comparison blocks once runs begin.

### Rational-complexity sweeps

- Judgment: PASS
- Reason:
  - the matrix includes small-, medium-, and unrestricted-complexity `X` regimes as mandatory controls.

## Sharpest Remaining Weakness

The baseline matrix is defensible on paper, but the audit cannot move beyond a planning-stage conditional pass because there is still no exact verifier. Until the exact evaluator exists, decoder leakage and compute parity can only be specified, not empirically certified.

## Overall Readiness

Conditional pass for pre-run planning.

- The checklist covers the required controls.
- Execution remains blocked by the unresolved verifier.
