# Phase 4 H2 Screen

## Trigger

`H2_target_direction_abelian` was activated only after the frozen H1 pilot failed its exact gate in `results/phase4_h1_frontier.md`.

## Command

```bash
python3 scripts/phase4_h2_screen.py \
  --control results/phase4_width4_seed601.json \
  --control results/phase4_width6_seed602.json \
  --output results/phase4_h2_screen.json
```

## Screened Families

- `h1_identity_L1`
  - representative frozen-H1 level-1 family in the exact template grammar
- `h1_identity_L2`
  - representative frozen-H1 level-2 family in the exact template grammar
- `phase4_width4_seed601`
  - matched direct corridor control with exact score `2.0`
- `phase4_width6_seed602`
  - matched direct corridor control with exact score `2.0`

## Invariant Summary

| Family | Forcing | Score | `r` | Rank | Smith tail | `m/n` | Target-solvable vertices |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `h1_identity_L1` | no | verification failure | `1` | `8` | all ones | `0.875` | `0` |
| `h1_identity_L2` | no | verification failure | `1` | `16` | all ones | `0.9375` | `0` |
| `phase4_width4_seed601` | yes | `2.0` | `5` | `12` | final `2` torsion factor | `0.875` | `2` |
| `phase4_width6_seed602` | yes | `2.0` | `7` | `20` | final `2` torsion factor | `1.0833...` | `1` |

Common arithmetic descriptors:

- determinant pattern of the nonzero `X` labels: `{1, 2, 3}`
- coordinate height: `3`
- nonzero `|X|`: `4`

## Decision

- Raw arithmetic features already identify the dead H1 families:
  - `support_size = 1`
  - `target_solvable_vertices = 0`
  - no forcing certificate
- The abelian-style invariant package adds no screening advantage over those raw features on this family set.
- `H2_target_direction_abelian` is therefore killed immediately, exactly as required by `results/phase3_h2_program.md`.
