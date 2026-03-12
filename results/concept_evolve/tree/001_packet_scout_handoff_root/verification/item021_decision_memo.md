# Item 021 Decision Memo

Date: 2026-03-12
Scope: decide whether H1 is promoted, killed, or reframed after the executed startup matrix, expanded falsifier suite, same-family ablations, and robustness study
Status: REFRAMED

## Decision

- H1 is **not promoted** as a winning source-aware architecture.
- H1 is **not killed** as a research lane.
- H1 is **reframed** into a falsification and simplification result.

## Promotion Threshold Used

- The original lane-level promotion rule required a clean startup-correctness advantage under mixed-source stress against strong baselines.
- The RC-ranked champion no longer meets that bar because the executed `source_blind` ablation is stronger on the falsifier suite and identical on the startup matrix.

## Evidence That Kills The Original Champion Story

- Primary startup matrix:
  - `champion`, `fixed`, `nonaware`, `source_blind`, and `time_constant_ranked` each start in `17/24` cases.
- Expanded falsifier suite:
  - `champion`: `8/10`
  - `fixed`: `7/10`
  - `nonaware`: `5/10`
  - `source_blind`: `10/10`
  - `time_constant_ranked`: `9/10`
- Same-family implication:
  - the RC-ranked selector is not the causal reason the packet-gated family survives the narrowed adversarial boundary.
  - the surviving reason is the packet-gated isolation topology shared by `champion`, `source_blind`, and `time_constant_ranked`.

## Evidence That Keeps The Lane Alive

- The lane still isolates a real and nontrivial startup boundary:
  - `fixed` collapses in `fa_001`
  - `nonaware` fails badly in `fa_005`, `fa_009`, and `fa_010`, and remains weaker in `fa_001`
  - packet-gated families avoid those join-topology failures
- The robustness pack confirms that the boundary is not just a single deterministic artifact:
  - in `fa_001`, `fixed` is `0/24`, `nonaware` is `21/24`, and the packet-gated designs are `24/24`
  - in `fa_005`, `nonaware` is `0/24` and the other four designs are `24/24`

## New Lane Decision

- Keep H1 alive only as this final result:
  - helper-free packet-gated isolation preserves the adversarial startup boundary, while explicit pre-handoff source ranking is unnecessary and can underperform a blind packet gate.
- Carry one positive secondary result forward:
  - `time_constant_ranked` keeps `9/10` falsifier successes with a `52.9%` lower successful-case pre-handoff control-energy median than the RC-ranked champion.

## Rejected Storylines

- `the RC-ranked selector is the winning new mechanism`
- `general superiority over the fixed startup path`
- `general superiority across the primary matrix`
- `measured superiority over the closest literature family`

## Remaining Budget And Activation Rule

- H2 and H3 remain inactive.
- The lane no longer needs a backup because it now has a writeable negative-result paper.
- Additional budget, if any, should go to polishing the writeup or adding a literature-faithful executed comparator, not to reopening the killed RC-ranked champion narrative.
