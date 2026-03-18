# Verification Summary

Verification phase: `review_round_1`

## Decision

Current work should: `REVISE`

The current packet supports a narrow negative-result claim only: the implemented `H1` and `H2` CA branches were tested on the exact `167/80` cyclic obstruction and the published mod-`64` order-`668` seed under matched same-representation controls, and they did not beat the matched `direct_greedy` baseline or produce an order-`668` solution. The packet does not currently support a positive method-novelty claim, a broad `CA for Hadamard search` novelty claim, or a broader publication-grade benchmark claim.

## Must-Fix Issues

1. Narrow the manuscript claim to the supported no-go result.
   - In `research_paper.tex`, remove or rewrite any language implying a new general search paradigm, a new Hadamard construction, a validated literal `cellar automata` method, or a broad `CA for Hadamard-like search is new` claim.
   - Keep the validated contribution tied to the executed `H1/H2` branches, the exact `167/80` and mod-`64` order-`668` anchors, and the matched-control negative result.

2. Repair citation and provenance support where the manuscript currently over-attributes or miscites evidence.
   - At `research_paper.tex:84`, attach `eliahou2025mod64` directly to the order-`668` status clause.
   - At `research_paper.tex:114-115`, support the lexical-noise / search-drift paragraph with repository artifacts such as `results/literature/seed_search.json`, `results/literature/literature_snapshot.json`, and `results/literature/semantic_scholar_manifest.json`, rather than only citing the noisy-hit papers themselves.
   - For the prompt-history / literal-cellar provenance claims at `research_paper.tex:76`, `86`, `258`, `432`, `541`, and `556`, add repository-artifact support from `results/research_context.json`, `results/concept_evolve/recurrent_state.json`, and `results/concept_evolve/bridge_candidates.json`.
   - Separate external `H2` seed provenance from repository-derived facts such as the `13` nonzero defects and the deterministic `s_41` degradation by citing `results/analysis/paper_metrics.json`, `hadamard668/experiments.py`, and `results/experiments/h2_seed_attempt.json`.

3. Clean up `sources.bib` so the bibliography is publication-grade.
   - Correct the metadata issues called out for `eliahou2025mod64`, `manzoni2025survey`, `mariot2021semibent`, `bagnoli2025controllability`, and `djokovic2018goethalsseidel`.
   - Remove unused residue such as `khatoon2019tutoring`.
   - Replace Semantic Scholar landing pages with canonical DOI, publisher, journal, or arXiv URLs for the load-bearing entries.

4. State the benchmark limits explicitly instead of implying broader evidentiary coverage.
   - `H1` is sufficient to reject the current CA rule family under matched controls, but the solved `4 x 79` positive control still has exact-hit rate `0/16` for both serious methods under the locked budget.
   - `H2` is only a no-go for the tested `s`-local repair branch on one real degraded order-`668` start; the `n = 9` ladder is too weak to support a mechanism claim.
   - The current packet has one serious non-CA comparator, no CA ablation matrix, no budget ladder, and no publication-grade robustness panel.

5. Keep reserve branches out of the validated contribution.
   - Treat literal / pushdown / symbolic reserve branches as hypotheses only unless they are separately executed and benchmarked against matched non-CA comparators.

## Optional Improvements

These are optional if the target is the narrow negative-result paper above. They become required if the project wants a broader benchmark or method claim.

1. Make at least one solved same-template control recover exactly under the published evaluation stack.
2. Expand `H2` to a prespecified panel of degraded real order-`668` starts, not just the single `s[41]` degradation.
3. Add at least one stronger same-representation non-CA heuristic baseline per branch, plus an exact reference baseline for the `n = 9` ladder.
4. Run a preregistered CA ablation matrix over `window`, `min_gain`, `phase_move_cap`, and budget.
5. Improve benchmark diagnostics and auditability with paired win/loss reporting, uncertainty intervals, orbit-growth or reachability analysis, best-versus-final error views, and fully self-describing run records.

## Actionable Bottom Line

- Acceptable after revision: a narrow branch-specific no-go paper.
- Not acceptable yet: a broader novelty paper or a broader publication-grade benchmark claim.
- If the scope stays narrow, revise the manuscript and citation layer now.
- If the scope stays broad, deepen the benchmark packet before any acceptance decision.
