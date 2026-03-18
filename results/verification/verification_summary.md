# Verification Summary

Verification phase: `post_deepen`

## Decision

Current work should: `REVISE`

The verification reports now agree on a narrow path to acceptance. The encoding-specific no-go claim is novel enough and supported enough to keep: the literal cellar tail-panel encoding collapses to the matched static boundary-debt state, the stack adds no surviving advantage on the audited controls or real-anchor panels, and that branch should be retired. What is not yet acceptable is any broader claim about positive solver novelty, broad `CA for Hadamard search` novelty, pushdown memory in general, or publication-grade benchmark breadth.

This is a `REVISE`, not a `DEEPEN`, if the manuscript stays narrow. It becomes `DEEPEN` only if the authors want to keep stronger efficacy, mechanism, or benchmark-generalization claims.

## Must-Fix Issues

1. Freeze the manuscript scope to the supported encoding-specific no-go.
   - Present the contribution as a narrow formal-and-empirical retirement of the implemented literal cellar encoding.
   - Keep `H1` and `H2` as precursor context or negative benchmark branches only; do not sell them as surviving algorithmic contributions.
   - Remove or rewrite any language implying a new Hadamard construction, a validated general CA search paradigm, or a general theorem about pushdown memory being unnecessary.

2. Repair the literature framing so it matches the evidence actually audited.
   - Add `constantine2025cyclic` to the opening anchor framing alongside `eliahou2025mod64`.
   - Soften wording that currently reads like evidenced ranking or venue judgment, especially the `closest structured-search comparators`, `order-668 heuristic literature`, and `not a publishable advance` style claims.
   - Keep all prior-art positioning explicitly at the level supported by the current bibliography: representative comparators, not exhaustive ranking.

3. Fix bibliography integrity and provenance support.
   - Correct the wrong `Scientific Reports` metadata in `sources.bib` for `suksmono2019`, `suksmono2022quantum`, and `suksmono2024qaoa`.
   - Replace stale preprint-only entries where published versions now exist, especially `manzoni2025survey` and `suksmono2016sa`, or cite both versions deliberately.
   - Add direct repo-artifact citations where the manuscript currently relies on internal evidence without citing it, especially `results/analysis/cellar_paper_metrics.json` and `results/analysis/paper_metrics.json` for recomputation/setup claims.

4. Make the benchmark statement as narrow as the benchmark packet warrants.
   - State explicitly that `H1` rejects the current CA rule only under matched controls; it does not establish solver competence because the solved `4 x 79` control still has exact-hit rate `0/16` for both serious methods.
   - State explicitly that `H2` is only a no-go for the tested `s`-local repair branch on the single audited real degraded start; the `n = 9` ladder is too weak and too degenerate to support a mechanism claim.
   - State explicitly that Phase 6 retires the implemented cellar encoding only; it does not rule out weaker static summaries, alternate tokenizations, or broader symbolic reopenings.

5. Clean up experiment auditability for the narrow claim.
   - Make the canonical artifacts self-describing enough to audit fairness and panel identity: serialize the important method settings symmetrically, unify Phase 6 panel labels, and fold the held-out cellar control metrics into the canonical experiment record.
   - Ensure the narrow no-go claim can be checked from the canonical outputs without depending on scattered analysis-only notes.

## Optional Improvements

These are optional only if the manuscript stays narrow. They become required if the project wants a broader benchmark or mechanism paper.

1. Add stronger same-representation baselines.
   - For `H1` and `H2`, add at least one additional serious non-CA comparator.
   - For the `n = 9` ladder, add an exact or exhaustive reference baseline.
   - For cellar, compare against weaker static summaries, not only the strongest boundary-debt state.

2. Add nondegenerate positive controls and broader real-start coverage.
   - Recover at least one solved same-template control in a discriminative way.
   - Expand `H2` beyond the single real degraded start to a preregistered panel of degraded `668` starts.
   - For cellar, include at least one real or surrogate panel with nonzero exact frontier before making any memory-mechanism claim.

3. Run actual ablations instead of single-setting rejections.
   - Sweep `window`, `min_gain`, `phase_move_cap`, and budget on locked seeds.
   - Add accepted-move-matched comparisons.
   - For cellar, add `stack off`, `feedback off`, weaker-static-summary, and tail-length ablations on the same panel family.

4. Improve diagnostics and cost reporting.
   - Publish paired seed-level win/loss tables, uncertainty intervals, and best-step trajectory diagnostics.
   - Save event-level snapshots at decisive updates.
   - Add `oracle_calls`, cache-hit, and wall-time views for cellar on nondegenerate panels.

## Bottom Line

- `ACCEPT` is justified only for the narrow novelty call: one exact literal cellar encoding has been formalized, shown to collapse to a finite residual state, and retired empirically on the audited controls and anchor panels.
- The current manuscript package should still be treated as `REVISE` because citation integrity, prior-art framing, benchmark wording, and artifact auditability are not yet clean enough.
- Do not spend more budget on wide new experiments unless the scope expands again. If the scope remains narrow, finish the manuscript and artifact repairs above and re-run verification.
