# Complexity Sweep

Snapshot date: 2026-03-18 UTC

## Status

Blocked. No exact complexity sweep was run.

The gate remains the same one recorded in:

- `results/verification/verification_summary.md`
- `results/experiments/h1_tiny_grid_report.md`

Without an exact verifier, no family can be scored honestly across complexity regimes, and no modular curriculum can be checked for an honest lift back to `\mathbb{Z}`.

## Regimes

The planned regimes are inherited from `results/baselines/benchmark_spec.md`.

| regime | exact-valid families | score distribution | hit rate | lift success | status |
| --- | ---: | --- | --- | --- | --- |
| small complexity | 0 | `[]` | `not available` | `not applicable` | blocked |
| medium complexity | 0 | `[]` | `not available` | `not applicable` | blocked |
| unrestricted complexity | 0 | `[]` | `not available` | `not applicable` | blocked |
| modular curriculum -> integer lift | 0 | `[]` | `not available` | `not available` | blocked |

## Why The Sweep Is Empty

- No exact-valid H1 family exists.
- No exact decoder or verifier exists to certify score or forcing behavior.
- Any modular-only signal would be a curriculum artifact until it survives integer lift.

## Rejection Rule

The standing rejection rule remains unchanged:

- any future story that wins only in the small-complexity regime is rejected as bounded-slope trapped;
- any future story that wins only in modular or finite-ring settings is rejected as a modular mirage.

At this checkpoint, there is no exact evidence in any regime, so there is nothing to promote or reject empirically beyond the blocker itself.
