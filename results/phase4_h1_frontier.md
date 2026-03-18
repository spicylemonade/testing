# Phase 4 H1 Frontier Note

## Scope

This note records the exact extracted-score evidence for the pre-registered `H1_macrocell_substitution` pilot and the matched direct corridor controls.

## Exact H1 Result

Command:

```bash
python3 scripts/ca_kakeya_search.py h1-obstruction --sum-value 1 --nonzero-count 4 > results/phase4_h1_obstruction.json
```

Outcome:

- The frozen H1 template family injects exactly one singleton seed at every level.
- The frozen H1 template family injects no initial solved vertices.
- Every edge generator has total label sum `(0,0)` across all vertices.
- Therefore every singleton relation generated from the exact verifier has total label in `Z * x`, where `x` is the unique initial seed label.
- Since `x_1 + x_2 = 1` for every nonzero label in the active same-sum palette, no nonzero multiple of `x` can equal an anti-diagonal vector `(a,-a)`, whose coordinate sum is `0`.

Conclusion:

- `H1_L1_exact`: exact verification failure before scoring.
- `H1_L2_exact`: exact verification failure before scoring.
- `H1_transfer_gate`: failed. There is no surviving level-1 or level-2 forcing certificate in the frozen H1 family.

This is stronger than the expected flat-transfer failure: the route is structurally blocked before any score improvement can occur.

## Matched Direct No-CA Controls

Commands:

```bash
python3 scripts/ca_kakeya_search.py random-search --width-min 4 --width-max 4 --trials 50 --nonzero-count 4 --seed-budget 8 --initial-t-budget 2 --allow-zero-horizontal --rng-seed 601 --output results/phase4_width4_seed601.json
python3 scripts/ca_kakeya_search.py random-search --width-min 6 --width-max 6 --trials 20 --nonzero-count 4 --seed-budget 8 --initial-t-budget 2 --allow-zero-horizontal --rng-seed 602 --output results/phase4_width6_seed602.json
python3 scripts/ca_kakeya_search.py random-search --width-min 8 --width-max 8 --trials 1 --seed-budget 12 --initial-t-budget 2 --allow-zero-horizontal --rng-seed 501 --output results/phase4_width8_seed501.json
```

Best exact forcing witnesses found:

| Geometry | `X` budget | Best score | `m` | `r` | `n` | `t` | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `2 x 4` | 4 nonzero labels | `2.0` | `7` | `5` | `8` | `2` | `results/phase4_width4_seed601.json` |
| `2 x 6` | 4 nonzero labels | `2.0` | `13` | `7` | `12` | `2` | `results/phase4_width6_seed602.json` |
| `2 x 8` | 3 nonzero labels | `29/14 = 2.071428...` | `20` | `9` | `16` | `2` | exploratory unrestricted witness in `results/phase4_width8_seed501.json` |
| `2 x 8` | 3 nonzero labels | `30/14 = 2.142857...` | `18` | `12` | `16` | `2` | exploratory unrestricted witness in `results/phase4_sparse_unrestricted_seed502.json` |

## Literature-Aware Interpretation

- The forcing controls that succeed remain in a fixed finite same-sum palette and a width-2 corridor with constant vertical label.
- This is exactly the low-rational-complexity / bounded-slope basin that the saved literature review marked as a warning sign.
- Nothing in the current frontier approaches the `1.70` neighborhood, let alone the target `1.675`.

## Decision

- Kill the frozen `H1_macrocell_substitution` route as an exact certificate route.
- Permit the narrow `H2_target_direction_abelian` screening pass, because the H1 pilot has no surviving forcing family and therefore no positive transfer signal to preserve.
- Do not make any claim stronger than: direct verifier-backed corridor search produced witnesses around `2.0`, while the frozen CA substitution route failed by an exact one-seed obstruction.
