# Item 021 Decision Memo

Date: 2026-03-12
Scope: decide whether H1 is promoted, killed, or narrowed after the startup matrix, falsifier suite, and run audit
Status: NARROWED

## Decision

- H1 is **not promoted**.
- H1 is **not killed**.
- H1 is **narrowed** to a helper-free pre-arbitration startup claim that only survives in adversarial mixed-source cases.

## Promotion Threshold Used

- The lane-specific promotion rule from `results/swarm/hypotheses.json` is load-bearing:
  - promote only if H1 survives the prior-art kill check **and** shows a clean startup-correctness advantage under mixed-source stress cases
- The benchmark governance in `results/swarm/tool_plan.md` makes the comparator set load-bearing:
  - the result must survive against two strong baselines with equal control-energy accounting

## Direct-Overlap Check

- `verification/claim_matrix.md` already narrowed the allowed story before execution.
- That overlap screen ruled out:
  - any `first`, `novel`, or `best` claim
  - any absolute startup-voltage claim
  - any steady-state extraction-efficiency claim
  - any broad superiority claim over the 2023-2024 self-powered multi-input interface family
- The only claim family allowed after the overlap screen was:
  - helper-free source-aware pre-arbitration startup sequencing under heterogeneous weak sources with mixed polarity and impedance asymmetry

## Baseline Audit Readout

- `verification/item011_signoff.md` accepted the fixed startup path and the nonaware multi-input startup path as the required strong baselines.
- `verification/item020_run_audit.md` found no material instrumentation error and blocked any new broad sweep.
- The benchmark therefore has to stand on the existing `24` startup-matrix cases and `6` falsifier cases rather than on a rerun.

## Evidence Against Promotion

- Primary startup matrix:
  - champion, fixed, and nonaware each start in `17/24` cases
  - the primary matrix shows `0` cases where the champion improves startup count over either baseline
  - the primary matrix shows `0` cases where the champion reduces back-drive relative to either baseline
- Pairwise benchmark result:
  - the champion is sometimes lower in `e_ctrl`, but that is not enough to satisfy the promotion rule
  - the fixed baseline remains as fast or faster on the successful primary-matrix cases
- Interpretation consequence:
  - the measured advantage threshold for promotion was **not** met

## Evidence Against Killing H1 Entirely

- The direct-overlap screen did **not** collapse H1 into an already-proven helper-free mixed-source startup result.
- The falsifier suite exposed a narrow operating region where the champion still matters:
  - `fa_001`: champion starts, fixed fails, and nonaware starts later with nonzero back-drive
  - `fa_005`: champion and fixed start, while nonaware fails with large wrong-way energy
  - `fa_004` and `fa_006`: all designs fail startup, but only nonaware accumulates measurable back-drive
- This means the lane still has a nontrivial, experimentally supported distinction:
  - the champion can avoid some nonaware multi-input failure modes under collapse and mixed-polarity stress

## Literature Comparison Readout

- `tables/benchmark_comparison.csv` maps the primary cases to the closest recovered startup and multi-source interface families.
- The literature-mapped benchmark does **not** support a broad claim that the champion beats the closest 2023-2024 self-powered multi-input interfaces on general startup correctness.
- What remains materially different from the closest prior work is narrower:
  - the claim is about pre-arbitration helper-free correctness under adversarial source collapse and polarity stress, not about generic multi-input harvesting or minimum startup voltage

## Final Lane Decision

- Keep H1 alive only on this narrowed boundary:
  - helper-free source-aware startup may reduce wrong-way energy and rescue startup specifically against nonaware multi-input behavior in collapse and mixed-polarity stress
- Reject these broader stories:
  - `general win over the fixed startup path`
  - `general win across the primary matrix`
  - `best startup interface`
  - `stronger literature-family performance than recent multi-input self-powered interfaces`

## Remaining Budget And Activation Rule

- `H2` Phase B budget remains available at `~24 hours`.
- `H3` Phase C budget remains available at `~16 hours`.
- Neither backup budget is activated now.
- Reason:
  - the lane is narrowed rather than killed, and `verification/item020_run_audit.md` already blocks a new broad sweep
- Activation condition from this point:
  - spend H2 or H3 budget only if H1 is later killed by a materially stronger overlap finding or by a changed experiment formulation, not by repeating the same startup matrix
