# Phase 2 Benchmark Sign-Off

## Inputs Reviewed

- `results/phase2_certificate_grammar.md`
- `results/phase2_baseline_matrix.md`
- `results/phase2_symmetry_policy.md`
- `results/swarm/director_brief.md`
- `results/swarm/falsifier.md`
- `results/swarm/tool_plan.md`
- `results/literature/prior_art_gap.md`

Specialist review used:

- `benchmark_auditor`
- `falsifier`

## Sign-Off Status

`GO` for the narrow pre-registered `H1_macrocell_substitution` pilot on the frozen corridor-substitution family.

`NO-GO` for any broader claim, full benchmark program, or novelty statement until the later experiment matrix, ablations, and verification artifacts are complete.

## Required Conditions Before Any Experiment Counts

Every reported row must satisfy all of the following:

- exact extracted legal certificate only,
- exact score `(m+r)/(n-t)` only,
- matched no-CA baseline on the same geometry,
- same `|X|`, coordinate-height budget, search budget, verifier backend, canonicalization policy, and grammar-size cap,
- frontier reporting over search budget and family size,
- logged `|Sigma_active|` and serialized grammar description length.

## Authorized Pilot Rows

The first experiments may use only these rows:

1. `H1` level-1 corridor substitution family.
2. `H1` level-2 transfer on the same family.
3. matched direct no-CA search on the same `H x W` corridor.
4. isotropic control.
5. random-label control.
6. stage-order perturbation.
7. aspect-ratio perturbation.
8. boundary-seed removal control.

If these fail, do not widen the search first; decide stop, kill, or pivot first.

## Stop-Go Language

Go only if:

- the `H1` frontier beats the matched direct no-CA baseline on exact score, or
- the `H1` frontier matches the best exact score while using no more hidden complexity and materially improving verifier-success efficiency.

Stop or kill `H1` if:

- gains disappear under direct-search, isotropic, randomization, stage-order, aspect-ratio, or boundary-seed controls;
- the best extracted family stays in a bounded-slope or low-rational-complexity basin;
- the story depends on surrogate metrics, hidden complexity, or imported descriptors that add no power beyond direct arithmetic features.

## Exact H1-To-H2 Pivot Trigger

`H2_target_direction_abelian` is the only pre-registered pivot.

Pivot immediately from `H1_macrocell_substitution` to `H2_target_direction_abelian` if either of these happens:

1. level-2 transfer is flat or worse than level-1 on exact extracted score;
2. exact extraction requires bespoke global repair not present in the frozen grammar.

Control failures, bounded-slope failures, and symmetry/ablation collapses are stop-or-kill conditions, not H1-to-H2 pivot triggers.

## Remaining Cautions

- A fixed but too-rich state alphabet can still hide most of the real complexity, so `|Sigma_active|` and description length must stay visible in every table.
- Semantic interface tags do not certify forcing by themselves; the exact verifier remains the source of truth.
- Boundary programming is a major failure mode in corridor families, so `R/T` ablations are not optional.
