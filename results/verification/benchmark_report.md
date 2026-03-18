# Benchmark Report

## Scope

This report covers the frozen width-2 corridor research program after:

- exact H1 evaluation in `results/phase4_h1_frontier.md`
- narrow H2 screening in `results/phase4_h2_screen.md`
- required ablations in `results/phase4_ablations.md`

It is a benchmark report for the corridor family only. It is not an exhaustive search over all constructible graphs.

## Exact Score Frontier

| Row | Geometry / family | Exact outcome |
| --- | --- | --- |
| `H1_L1_exact` | frozen CA level 1 | verification failure from the one-seed obstruction |
| `H1_L2_exact` | frozen CA level 2 | verification failure from the one-seed obstruction |
| matched direct control | `2 x 4` corridor | `2.0` with `m=7`, `r=5`, `n=8`, `t=2` |
| matched direct control | `2 x 6` corridor | `2.0` with `m=13`, `r=7`, `n=12`, `t=2` |
| exploratory direct control | `2 x 8` corridor | `29/14 = 2.071428...` with `m=20`, `r=9`, `n=16`, `t=2` |
| exploratory direct control | `2 x 8` corridor | `30/14 = 2.142857...` with `m=18`, `r=12`, `n=16`, `t=2` |

No exact row reached the `1.70` neighborhood, let alone the target `1.675`.

## Matched Baselines

The matched baselines required by `results/phase2_baseline_matrix.md` were satisfied narrowly inside the frozen corridor family:

- same height-2 corridor geometry
- same exact verifier backend
- same exact score metric `(m+r)/(n-t)`
- same finite same-sum `X` budget on the matched width-4 and width-6 controls
- direct no-CA search used as the primary comparison class

The evidence is adequate to reject the frozen CA route inside this narrow family. It is not adequate to claim a global lower bound or a full benchmark over every low-height constructible graph.

## Pivot Decision

- The H1-to-H2 pivot was justified because the frozen H1 family never produced a forcing certificate at any level.
- The failure mode was stronger than flat transfer: the template grammar injects exactly one seed and no initial solved vertices, so exact operation 2 can never fire.
- H2 was then tested only on the same family IDs and was killed immediately because its invariant package added no screening value beyond raw support size, rank, and target-solvable counts.

## Finite-Size Caveats

- All successful exact witnesses are tiny direct corridor controls (`2 x 4`, `2 x 6`, and exploratory `2 x 8`).
- The direct-search rows are heuristic frontiers, not exhaustive optima.
- The direct witnesses remain in a tiny fixed-`X` corridor regime consistent with the bounded-slope / rational-complexity warning literature.
- Stage-order perturbation became not applicable once no substitution-mediated family survived.
- Random `X` relabelings often preserved the same `2.0` witness score, which weakens any interpretation that the arithmetic labels encode a special CA mechanism.

## Benchmark Verdict

Inside the frozen corridor benchmark, the evidence rejects the CA route.

- `H1_macrocell_substitution` is rejected by exact obstruction.
- `H2_target_direction_abelian` is rejected as a non-additive screening layer.
- The only surviving objects are direct boundary-sensitive corridor witnesses around score `2.0`, and those do not scale or stabilize under the required ablations.
