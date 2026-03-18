# Writeup Outline

This outline is the handoff package for drafting a faithful report without reopening the search.

Start from `results/verification/verification_summary.md` as the hub document. It links the artifact set below and should be the first file a writer opens.

## 1. Problem Statement

Use:

- `results/repo_map.md`
- `results/context_sync.md`
- `results/baselines/witness_spec.md`

Write:

- the six-line arithmetic-Kakeya witness target,
- the score objective `(m(G)+|R|)/(n(G)-|T|)`,
- and the explicit requirement that any CA story decode directly to a legal witness with no repair.

## 2. Literature Boundary

Use:

- `results/literature/prior_art_gap.md`
- `sources.bib`
- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`

Write:

- the false-overlap watchlist caveat,
- the real adjacent arithmetic-Kakeya comparison set,
- the CA / automated-search comparison set,
- and the final claim boundary: design-level novelty only, no mathematical advance.

## 3. Core Design

Use:

- `results/core/h1_design.md`
- `results/core/lane_gates.md`
- `results/swarm/phase_3_h1_review.md`
- `results/concept_evolve/tree/phase_3_core/index.md`

Write:

- the proof-carrying stage-indexed H1 design,
- the no-repair decoder rule,
- the keep/kill gates,
- and the reason H2/H3 never opened.

## 4. Experiment Phase

Use:

- `results/verification/verification_summary.md`
- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`
- `results/verification/benchmark_report.md`

Write:

- that no exact verifier existed,
- that the tiny-grid sweep, controls, and complexity sweep were blocked,
- and that benchmark integrity passed only as a blocker-integrity audit.

Do not write:

- any claimed verified score,
- any claimed baseline win,
- any claim that controls were actually executed.

## 5. Concept-Evolve Outcome

Use:

- `results/concept_evolve/concept_delta.md`
- `results/concept_evolve/reframings.json`
- `results/concept_evolve/bridge_candidates.json`
- `results/concept_evolve/tree/phase_5_retrospective/index.md`

Write:

- the shift from generic CA intuitions to proof-carrying exact-decoder bridges,
- the promoted bridges:
  - `proof_carrying_exact_decoder_bridge`
  - `spatially_coupled_peeling_ladders`
  - `sat_egraph_symbolic_backbone`
- the retired proxy-heavy bridges,
- and the retrospective blocker lesson.

## 6. Final Decision

Use:

- `results/final_assessment.md`
- `results/verification/final_audit.md`

Write:

- the final decision as `pivot`,
- the reason the pivot is to exact-verifier recovery,
- and the pass/fail split:
  - reporting discipline passed
  - experimental completion failed

## 7. Safe Claim Checklist

Safe:

- blocker-aware design program
- verifier-coupled CA architecture
- literature and novelty boundary mapping
- exact-evaluator recovery as the next task

Unsafe:

- solved witness
- verified score improvement toward `<= 1.675`
- empirical CA superiority
- cleared bounded-slope or modular-mirage objections

## 8. Minimal Figure / Table Suggestions

- one table for phase status and blocker state
- one table for literature differentiation categories
- one table for promoted vs retired ConceptEvolve bridges

No figure or table should imply experimental success.
