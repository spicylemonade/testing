# Verification Summary

## Decision

**Disposition: REVISE**

The specialist reports agree that the current artifact set supports only a **narrow negative result**:

- `H1_macrocell_substitution` is dead by an exact one-seed obstruction.
- `H2_target_direction_abelian` adds no useful screening power on the tiny tested family set.
- direct no-CA corridor controls reach only about score `2.0`, look fragile, and do not justify any stronger mechanism claim.

This should not be accepted as a positive novelty, new framework, or publication-grade benchmark section in its current form. It does **not** need a wide new search pass to become internally consistent; it needs a tighter writeup.

## Must-Fix Issues

1. Rewrite the contribution as a narrow negative operational result.
   - Remove or explicitly reject claims that the repo establishes a new arithmetic-Kakeya formulation, a successful CA mechanism, a useful abelian-network mechanism, a decoder-style route, or a new verifier-first framework.
   - State the surviving claim directly: exact verifier-backed corridor experiments falsify H1 and H2 and leave only small direct controls around `2.0`.

2. Tighten the benchmark claim to what is actually supported.
   - Do not present the current artifact set as a publication-quality CA-guided benchmark.
   - Limit benchmark language to: exact H1 failure, no H2 lift on the tested families, and fragile direct corridor witnesses that do not approach the `1.70` range.

3. Clean up citation boundaries.
   - Cite repo-backed experimental claims to the repo artifacts, not to external literature.
   - Cite mathematical history and frontier statements to primary papers, not to FrontierMath/Epoch summaries alone.
   - Remove or replace under-supported background claims until the missing primary citations are added.

4. Soften inference-heavy comparison language.
   - Keep bounded-slope / low-rational-complexity remarks only as interpretation or consistency language unless explicit measurements are added.
   - Avoid novelty-positioning sentences that overread Tao (2025) or other literature without precise support.

5. Normalize bibliography records before any paper-facing reuse.
   - Fix hybrid preprint/journal entries and broken metadata in `sources.bib`.
   - Verify the exact intended references for the Hausdorff-dimension and frontier-history statements.

## Optional Improvements

1. Add the missing primary citations for the intro and frontier discussion.
   - This includes the Bourgain Kakeya-dimension paper, the intended Leng-Sah-Sawhney citation, the Katz/Tao historical frontier papers, and the primary source(s) behind the stronger `1.6751308` and `3/2` statements if those statements remain.

2. Make the benchmark section publication-grade if that remains a goal.
   - Run the missing matched `2 x 8` no-CA baseline with the same palette and budgets.
   - Execute the missing pre-registered non-CA baselines: low-height asymmetric `X`, explicit bounded-slope, and slowly growing-`X`.
   - Re-run ablations under matched budgets and expand width-8 / H2 evaluation beyond the current tiny sample.

3. Improve auditability of experiment traces.
   - Add per-trial verifier success/failure, failure reason, score, active-state count, grammar length, search budget, and `X`-complexity summaries.
   - Report frontiers over budget and family size instead of best-row snapshots only.

4. Measure the literature-comparison quantities directly.
   - If the writeup wants to keep bounded-slope / rational-complexity comparisons as factual claims, add explicit slope and complexity summaries for the surviving width-4/6/8 rows.

## Publication-Safe Position Right Now

The current work is defensible only as follows:

- exact verification kills the frozen H1 corridor family before scoring;
- H2 adds no value on the tiny screened family set;
- direct corridor search still finds only fragile exact witnesses around score `2.0`;
- nothing in the current verified artifacts supports a CA route to the `1.675` target.

If the team wants a stronger benchmark or broader novelty claim, that is a **deepen-next** program. For the current draft, the correct move is **revise the framing and citations now**.
