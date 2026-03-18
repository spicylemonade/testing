# Verification Summary

Snapshot date: 2026-03-18 UTC
Verification phase: `review_round_1`

Inputs synthesized:

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`

## Decision

`REVISE`

The current work is not ready for `ACCEPT`. The three audits agree that process integrity is strong: the repo preserved the exact objective, avoided repair or proxy substitution, and reported negative results honestly. They also agree that the publication claim set is too wide for the current evidence. There is no shared exact `(X,G,R,T)` verifier/decoder in use, no matched benchmark block, no executed control suite, and no support for a strong novelty claim beyond a narrower verifier-coupled design or protocol contribution.

This is a `REVISE` rather than `DEEPEN` because the immediate task is to contract the claim boundary and repair the evidence trail. If the project still wants a stronger empirical CA-method claim after that revision, additional experimental work will be required.

## Must-Fix Issues

1. Re-establish exact verification as the foundation.
Recover or implement a shared exact no-repair decoder and verifier for six-line witnesses `(X,G,R,T)` over `\mathbb{Z}`. Until that exists, do not make empirical benchmark claims or expand the search story.

2. Run one fully matched benchmark block.
Compare one CA family against Random Local Search, Whole-Witness Mutation, and Decoder-Matched Search on the same grid block with identical `X` or `|X|`, density band, decoder, and exact-decode budget. Report legality hit rate, forcing hit rate, full score distributions, and candidate-level failure reasons for every family.

3. Execute the mandatory controls already specified in the repo.
Run label shuffle, decoder ablation or randomization, held-out geometry, held-out `X`, and small/medium/unrestricted complexity sweeps. Apply the existing kill thresholds as written. If the signal survives label shuffle, disappears under decoder matching or ablation, or only appears in the `small` regime, drop the CA-specific empirical claim.

4. Narrow the manuscript to the defensible claim boundary.
Do not present the current work as mathematical progress on arithmetic Kakeya or as a demonstrated new CA search method. The supported claim is narrower: an audited verifier-coupled search design or blocker report with a fixed no-repair decoder contract and explicit anti-overclaim gates.

5. Fix citation and provenance blockers.
Remove or replace the misapplied `leng2024` citation, add direct provenance for the `<= 1.675` target and prompt-derived `AK(alpha)` wording, and soften related-work comparisons unless they are tied to specific theorem or result anchors.

6. Resolve bridge-status traceability.
Choose one authoritative source for final bridge status, or explain the stage distinction between the `2/3/4` iterate-time split and any later surviving shortlist. The manuscript should not state bridge counts while repo artifacts disagree.

## Optional Improvements

- Add an early artifact or provenance footnote in the abstract or introduction for the `0/3` families, `0` exact decodes, and missing-verifier status.
- Normalize bibliography hygiene: key-year mismatches, canonical publisher or arXiv URLs, and consistent arXiv metadata.
- Split the control report into explicit rows for each baseline family and each stress test so later audits do not need to reconstruct the comparison matrix.
- If the verification reports will be reused downstream, add direct source anchors for high-load status claims and distinguish sourced kill rules from auditor-added completion criteria.

## Next Step

Revise the paper and repo narrative around the narrower audited-design claim, then recover the exact verifier or decoder and run a single matched benchmark or control block. Revisit stronger novelty or empirical-superiority claims only after that block exists.
