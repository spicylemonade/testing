# Verification Summary

## Status

The frozen corridor research program does **not** produce a certificate with score `<= 1.675`.

The verified outcome is a finite-size no-go for the current CA routes plus a narrow direct-search residual:

- `H1_macrocell_substitution`: rejected
- `H2_target_direction_abelian`: rejected
- direct corridor controls: exact witnesses around score `2.0`, but not robust or scalable

## Exact Frontier

- `H1_L1_exact`: verification failure before scoring
- `H1_L2_exact`: verification failure before scoring
- best matched direct control on `2 x 4`: score `2.0`
- best matched direct control on `2 x 6`: score `2.0`
- best recorded exploratory `2 x 8` control: `29/14 = 2.071428...`

No verified row reached the `1.70` neighborhood.

## Pivot And Kill Decisions

- H1-to-H2 pivot: justified. The frozen H1 template family has an exact one-seed obstruction, so transfer never reaches a forceable level.
- H2 kill: justified. The abelian-style invariant package added no screening value beyond raw support size, rank, and target-solvable counts on the same family IDs.
- Direct-search residual: weakened heavily by ablations. The surviving `2.0` witness is boundary-sensitive, fails seed and `T` randomization, and does not scale under frozen `X`.

## Finite-Size Caveats

- The successful rows are tiny width-2 corridor controls only.
- The direct-search frontiers are heuristic search results, not exhaustive optima.
- The whole surviving frontier remains in a tiny fixed-`X` corridor regime consistent with the bounded-slope / rational-complexity warning literature.
- Random `X` relabelings often preserve the same `2.0` score, so the surviving witness should not be interpreted as evidence for a special CA arithmetic mechanism.
- Stage-order perturbation became not applicable once no substitution-mediated family survived.

## Verification Verdict

The current evidence supports a constrained negative claim only:

- exact verifier-backed corridor search found small witnesses around score `2.0`;
- the frozen CA routes fail before producing a competitive certificate;
- nothing in the verified artifact set supports a CA route to the `1.675` target.
