# 04 Matched Control Families

## Prerequisites

- certificate grammar frozen
- baseline matrix frozen
- symmetry policy frozen

## Dependency Edges

- depends on: certificate grammar
- depends on: baseline matrix
- depends on: symmetry policy
- enables: benchmark sign-off
- enables: Phase 4 experiment matrix

## Why This Branch Could Lower Score

- Matched controls on the same `H x W` corridor can show whether H1 actually buys exact-score leverage.
- Separate ablations on `R`, `T`, `X`, stage order, and aspect ratio can isolate which part of the pipeline matters.

## Why This Branch Could Fail

- If controls do not match `|X|`, geometry, and rule-description budget, the comparison is invalid.
- If the transposed or isotropic controls are illegal under extraction, the branch can accidentally protect H1 from the hardest comparisons.
- If boundary-seed removal kills the gain immediately, the route is only boundary programming.
