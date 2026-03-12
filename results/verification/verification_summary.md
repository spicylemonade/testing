# Verification Summary

Date: 2026-03-12
Phase: review_round_1
Scope: synthesize novelty, citation, and benchmark verification for the current H1 manuscript and evidence pack
Recommendation: REVISE

## Decision

- The current package is not ready as a broad architecture-novelty paper or as a benchmark-centered positive claim.
- It is viable as a narrower falsification/simplification paper if the manuscript and verification narrative are revised to match what the repo actually demonstrates.
- Choose `DEEPEN` only if the intent is to keep any claim that packet-gated isolation is already causally isolated, or that the package says something measured against the closest prior-art families.

## Must-Fix Issues

1. Re-scope the paper to the claim boundary the evidence actually clears.
- Keep the headline on the same-family negative result: inside the executed helper-free model, explicit pre-handoff ranking is not needed within the packet-gated family.
- Remove or soften statements that still imply new-architecture novelty, broad dominance, or a validated positive mechanism story for packet-gated isolation itself.
- Revise the strongest overreach points in `research_paper.tex`, especially `research_paper.tex:65-67`, `research_paper.tex:78`, `research_paper.tex:87`, `research_paper.tex:601-603`, and `research_paper.tex:617`, so they no longer claim that the literature generally omits this comparison, that the selector was definitively never the ingredient, or that a blind packet gate is broadly sufficient and often better.

2. Repair under-supported literature framing.
- Split or re-cite `research_paper.tex:63` so the mixed-polarity and source-conflict parts are supported where they appear.
- Narrow `research_paper.tex:81` so the sub-`100 mV` statement is only attached to papers that actually support that threshold.
- Strengthen or soften the category framing at `research_paper.tex:83`, `research_paper.tex:85`, `research_paper.tex:98`, and `research_paper.tex:100`; the current prose does more work than the citation density supports.
- Replace the absence claim at `research_paper.tex:65-66` and `research_paper.tex:87` with a scoped formulation such as "the recovered overlap set did not reveal a close same-family falsification study" unless a stronger gap search is added.

3. Align the manuscript with the benchmark gate that is actually cleared.
- Keep claims to: the five-way `17/24` primary-matrix tie, the internal falsification of the original RC-ranked story, and `time_constant_ranked` as a secondary internal tradeoff.
- Do not claim publication-grade proof that packet gating itself is the surviving causal mechanism; `blind_packet_merge` has not yet been executed in the shared summaries.
- Do not make stronger-than-supported handoff, chatter, or back-drive claims while the decisive metrics still depend on the `V(n_store)` proxy and an undocumented back-drive threshold.
- Synchronize or quarantine stale benchmark notes (`item018_benchmark_note.md`, `item019_falsifier_note.md`) so the artifact pack does not mix repaired and pre-repair interpretations.

4. Close the remaining citation-hygiene loose ends.
- Keep `hernandez2013tegboost` uncited or remove it from `sources.bib`.
- Delete or soften the publication-culture claim at `research_paper.tex:614` unless a review citation is added.

## Optional Improvements

- Execute `blind_packet_merge` on the separator cases and matched primary-matrix cases to test whether packet-gated isolation, not just ranking removal, carries the boundary.
- Add one literature-faithful executed comparator before making any measured prior-art comparison.
- Emit explicit `n_handoff` rise, fall, and second-rise measurements, then rerun the decisive falsifier cases to validate the current store-voltage proxy.
- Reissue back-drive summaries with a documented simulator noise floor and both raw and thresholded counts.
- Extend robustness reruns to `fa_002`, `fa_006`, `fa_009`, and `fa_010`.
- Add a failure taxonomy for the failed startup-matrix rows and decisive falsifier losses.
- Strengthen the novelty-gap support with a review-level source or a better-scoped search summary if stronger field-level rarity language is desired.

## Bottom Line

- Current status: `REVISE`.
- Fastest viable route: write the paper as a bounded negative-result / simplification study and tighten the literature framing to match the retrieved overlap set.
- Escalate to `DEEPEN` only if the goal is to keep a benchmark-positive packet-gating claim or any stronger separation from prior work.
