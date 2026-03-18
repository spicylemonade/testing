# H1 Control Report

Snapshot date: 2026-03-18 UTC

## Status

No control runs were executed because no H1 family was promoted past the first exact gate.

The blocker is upstream and already documented in:

- `results/experiments/h1_tiny_grid_report.md`
- `results/verification/verification_summary.md`

## Promoted Families

- Count: `0`
- Family identifiers: `[]`

## Control Matrix

### X-label shuffle at fixed geometry
- Executed families: `0`
- Score distribution: `[]`
- Verdict: `not evaluable`

### Matched-budget non-CA baseline
- Executed families: `0`
- Score distribution: `[]`
- Verdict: `not evaluable`

### Decoder-matched baseline
- Executed families: `0`
- Score distribution: `[]`
- Verdict: `not evaluable`

### Held-out larger or different-aspect-ratio grids
- Executed families: `0`
- Score distribution: `[]`
- Verdict: `not evaluable`

## Why The Distributions Are Empty

The rubric requires controls for promoted families. No family reached that stage because the exact verifier is missing, so there is no exact-valid family on which to apply shuffles, baselines, or held-out tests.

Reporting empty distributions here is intentional. Filling them with proxy metrics would violate the no-repair, exact-verification discipline already established for this run.

## Consequence

No claim about collapse, robustness, or baseline superiority is available. The correct conclusion is that the control phase is blocked, not passed.
