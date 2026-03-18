# H1 Macrocell Substitution

Status: champion

## Prerequisites

- `results/phase2_certificate_grammar.md`
- `results/phase2_baseline_matrix.md`
- `results/phase2_symmetry_policy.md`
- `results/phase2_benchmark_signoff.md`
- `results/phase3_h1_program.md`

## Dependency Edges

- Depends on the frozen width-2 corridor grammar and the exact extractor.
- Feeds the matched H1 frontier in Phase 4.
- If its transfer test fails, it unlocks `H2_target_direction_abelian`.

## Required Evidence

- exact legal extraction at level 1 and level 2 under one fixed `X`, interface alphabet, and extractor;
- `S_2 < S_1` on the extracted legal certificates;
- a matched-baseline advantage over direct no-CA, isotropic, random-label, stage-order, aspect-ratio, and boundary-seed-removal controls;
- explicit reporting of `|Sigma_active|`, grammar description length, and exact score frontier;
- evidence that the family does not collapse into bounded-slope or low-rational-complexity behavior.

## Kill Criteria

- any bespoke global repair or scale-specific patch;
- `S_2 >= S_1`;
- gains disappear under the required controls;
- the apparent gain is really `R/T` boundary programming or bounded-slope behavior.

## Why It Could Lower Score

- The corridor substitution may reuse one local motif across levels while keeping extraction exact.
- If the same grammar improves under level transfer, it can beat same-geometry direct search without claiming a new theorem.
