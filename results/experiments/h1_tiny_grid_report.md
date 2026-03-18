# H1 Tiny-Grid Exact Sweep Report

Snapshot date: 2026-03-18 UTC

## Status

Blocked. No exact H1 tiny-grid sweep was run.

## Why No Sweep Was Run

The run remains blocked by the same missing-verifier condition recorded in:

- `results/verification/verification_summary.md`
- `results/core/lane_gates.md`

No exact decoder or verifier for six-line arithmetic-Kakeya witnesses `(X,G,R,T)` over `\mathbb{Z}` is available in the current repo snapshot or in the targeted public checks already logged. Under the standing no-repair rule, running CA families against proxy metrics would not satisfy the rubric or the problem statement.

## Planned Budget That Was Not Spent

- H1 local-rule families evaluated: `0 / 3`
- Exact decodes executed per family: `0 / 10^3`
- Total exact decodes executed: `0`

## Metrics

- Verified hit rate: `not available`
- Best verified score: `not available`
- Median verified score: `not available`

These values are intentionally left blank rather than replaced with proxy numbers.

## Failure Reason

The first exact gate did not open because the required evaluator is missing. That means:

- no candidate can be checked for exact forcing over `\mathbb{Z}`;
- no candidate can be scored honestly under `(m(G)+|R|)/(n(G)-|T|)`;
- and no comparison against matched non-CA baselines can be made.

## Operational Consequence

Later experiment items remain closed.

- `item_017` may not claim control results because no H1 family has cleared the first exact gate.
- `item_018` may not claim complexity-sweep behavior because no exact-valid family exists to sweep.
- `item_019` and `item_020` may audit only blocker integrity, not experimental signal.

## Current Decision

Preserve the experiment plan, but treat phase 4 as blocker-aware documentation until a real exact verifier is found.
