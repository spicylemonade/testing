# Benchmark Report

Snapshot date: 2026-03-18 UTC

Audit roles invoked for this checkpoint:

- `monitor`
- `benchmark_auditor`
- `falsifier`
- `integrator`

## Overall Verdict

- Benchmark-integrity audit: `pass`
- Experimental-signal audit: `blocked`

This is a pass on blocker integrity, compute-accounting discipline, and negative-result preservation. It is not a pass on experimental evidence, because no exact verifier exists and no exact-decoded search was run.

## Findings

### 1. Matched budgets
- Verdict: `pass`
- Evidence:
  - `results/experiments/h1_tiny_grid_report.md` preserves the intended H1 budget as `0 / 3` families and `0 / 10^3` exact decodes per family.
  - `results/experiments/h1_controls.md` records `0` promoted families and empty control distributions.
  - `results/experiments/complexity_sweep.md` records `0` exact-valid families in every regime.
- Interpretation:
  - No compute mismatch was introduced, because no family or baseline was allowed to consume real evaluation budget under a missing verifier.

### 2. Identical decoder usage
- Verdict: `blocked but consistent`
- Evidence:
  - `results/verification/verification_summary.md` states that no exact decoder or verifier entry point exists.
  - `results/core/lane_gates.md` forbids relaxing that gate and forbids repair.
  - All experiment documents refuse proxy evaluation rather than letting one method use a softer decoder.
- Interpretation:
  - Identical decoder usage is preserved in the only honest sense currently available: no method used a different decoder because no method was run.
  - This remains unresolved for any real experiment until an exact shared decoder exists.

### 3. Full score accounting
- Verdict: `pass at audit layer`
- Evidence:
  - `results/experiments/h1_tiny_grid_report.md` explicitly refuses proxy hit-rate or score substitutes.
  - `results/core/lane_gates.md` keeps `(m(G)+|R|)/(n(G)-|T|)` as the only valid score.
  - `results/experiments/complexity_sweep.md` leaves distributions empty rather than backfilling modular or bounded-slope proxies.
- Interpretation:
  - The run preserved full score accounting by declining to produce fake scores under an absent verifier.

### 4. Negative-result preservation
- Verdict: `pass`
- Evidence:
  - The tiny-grid report records a blocked non-run instead of silently dropping item_016.
  - The control report records empty distributions rather than implying passed controls.
  - The complexity sweep records blocked regimes and explicit rejection rules.
- Interpretation:
  - Negative and null outcomes were preserved faithfully.

## Audit Risks That Remain Open

- The experiment phase is still infrastructure-blocked, not empirically falsified.
- Any future report must not reinterpret these blocker documents as baseline wins, control wins, or complexity-generalization evidence.
- The first real benchmark audit must be rerun after an exact shared decoder or verifier is available.

## Bottom Line

The phase-4 artifacts are internally consistent: matched budgets stayed unspent, no decoder asymmetry was introduced, the exact score formula was preserved, and the blocked outcome was reported honestly. What remains missing is the evaluator itself, so benchmark parity is documented but not operationally exercised.
