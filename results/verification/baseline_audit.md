# Baseline Audit

Snapshot date: 2026-03-18 UTC

## Audit Mode

This is a pre-run audit of the baseline plan only.

Required role-specific review was attempted via:

- `benchmark_auditor`
- `falsifier`
- `integrator`

Those child runs were launched through the Codex CLI but failed with transport-layer stream disconnects before returning final messages. Per the run governance, delegation was then stopped and the checklist below was completed directly against the same criteria.

## Checklist

### Label shuffling

- Judgment: `PASS`
- Reason:
  - `results/baselines/benchmark_spec.md` explicitly requires an `X`-label shuffle control at fixed geometry and fixed nonzero-label multiset.
  - This closes the main risk that geometry or density, rather than arithmetic structure, is carrying the signal.

### Decoder leakage

- Judgment: `FAIL`
- Reason:
  - The plan includes a decoder-matched baseline, which is necessary.
  - But it does not yet require decoder ablation or decoder-randomization, and no exact verifier exists to measure how much of the hard work sits in the decoder.
  - Until a real exact evaluator exists, decoder leakage remains only partially addressed.

### Compute parity

- Judgment: `PASS`
- Reason:
  - The benchmark spec fixes equal exact-decode budgets, matched grid blocks, matched `|X|` or fixed `X`, and matched edge-density bands.
  - It also forbids best-of-many-only reporting.

### Out-of-distribution grids

- Judgment: `PASS`
- Reason:
  - The plan requires held-out larger or different-aspect-ratio grids whenever the CA family is tested there.
  - This is the right minimum check against memorized local tilings.

### Rational-complexity sweeps

- Judgment: `PASS`
- Reason:
  - The plan explicitly includes small-, medium-, and unrestricted-complexity `X` regimes.
  - That directly addresses the bounded-slope / low-rational-complexity trap highlighted by Tao (2025) and the falsifier memo.

## Overall Readiness

- Overall judgment: `FAIL / BLOCKED`
- Blocking reasons:
  - no exact verifier;
  - decoder leakage not fully closed.

## Required Fix Before Any Run

1. Locate or obtain a real exact `(X,G,R,T)` verifier.
2. Add decoder ablation and decoder-randomization checks to the execution plan.
3. Keep the existing parity, shuffle, OOD, and complexity controls unchanged.
