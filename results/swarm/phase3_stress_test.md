# Phase 3 Hypothesis Stress Test

Date: 2026-03-13
Rubric item: `item_015`
Delegation roles:
- `research_director`
- `falsifier`
- `novelty_checker`
- `integrator`

Reviewed artifacts:
- `results/plans/phase3_route_sheet.md`
- `results/plans/ramsey_research_program.md`
- `results/concept_evolve/probe_result.json`
- `results/verification/benchmark_report.md`
- `results/swarm/phase1_cleanup.md`
- `results/literature/prior_art_gap.md`

## Route Triage

| Route | Decision | Threshold basis |
| --- | --- | --- |
| `H1` | Keep | Keep as champion only if the atlas stays novelty-safe: top-25 cores cover at least 30 percent of failed orbit-distinct `42 -> 43` extensions across at least 3 non-isomorphic parent families, held-out coverage stays at or above 50 percent of training-side coverage, zero witness kills occur, no family contributes more than 50 percent of accepted recurring-core support, and reuse stays canonical rather than encoding-specific. |
| `H2` | Demote | Keep closed as backup only. It opens only after `H1` fails transfer or witness-safety. It survives later only if a primitive clears the non-equivalence gate and beats split-vertex/transverse-edge gluing under the fixed upper-bound win rule and matched-compute tuple. |
| `H3` | Demote | Keep as attachment-only infrastructure. No standalone `H3` route proceeds before `H1` or `H2` yields a transferable structural object. Structural credit requires cross-branch or cross-family transfer plus reduced checked proof size or checker runtime. |

No route is killed on the present record because none of the written kill conditions has actually fired.

## Shared Blockers

- No route should scale yet because the repo still lacks the local `frontier_parent` corpus, orbit-distinct `42 -> 43` extension enumerator, independent `44`-vertex witness verifier, and `45`-vertex certificate checker.
- Any claim stronger than intermediate evidence would still violate the current anti-proxy rules until those missing artifacts exist.

## Failure Thresholds That Matter Most

- `H1`: the `anti_exoo_holdout` is the decisive falsifier. If coverage collapses when the most Exoo-like family is held out, the route is memorizing one lineage rather than capturing a reusable Ramsey object.
- `H2`: the non-equivalence gate is decisive. If a candidate primitive cannot show that it is more than split-vertex or transverse-edge gluing plus a different branch order, kill the route before benchmarking.
- `H3`: replay and transfer are decisive. If the same canonical core does not survive proof-format replay, branch changes, or family changes, the route stays infrastructure-only.

## Current Phase 3 Call

- `H1`: kept under probationary numeric falsifiers.
- `H2`: demoted to inactive backup.
- `H3`: demoted to attachment-only infrastructure.
