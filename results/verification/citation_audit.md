# Citation Audit

## Phase

- `post_deepen`

## Inputs Audited

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`

Spot checks used for support validation:

- `results/analysis/paper_metrics.json`
- `results/analysis/cellar_paper_metrics.json`
- `results/experiments/cellar_phase6.json`
- `results/analysis/cellar_no_go.md`

## Overall Assessment

- The narrow, load-bearing manuscript claim is supported. The cellar no-go claim in `research_paper.tex:610-646` is backed by the internal proofs in `research_paper.tex:281-443` and by exact counts in `results/experiments/cellar_phase6.json` and `results/analysis/cellar_paper_metrics.json`.
- The precursor `H1/H2` comparison packet is also supported. The summary numbers in `research_paper.tex:498-513` match `results/analysis/paper_metrics.json`.
- All `\repoevidence{...}` paths currently resolve to real files.
- The main citation risk is not a fabricated core source. The main risk is weaker framing and provenance support around literature-positioning claims, plus stale or incorrect bibliography metadata.

## Claim Coverage Snapshot

| Claim cluster | Status | Notes |
| --- | --- | --- |
| Core cellar no-go (`research_paper.tex:610-646`) | Supported | Formal support comes from `research_paper.tex:281-443`. Quantitative support comes from `results/experiments/cellar_phase6.json` and `results/analysis/cellar_paper_metrics.json`. |
| Precursor `H1/H2` packet (`research_paper.tex:498-513`) | Supported | Means, wins, ties, and packet sizes match `results/analysis/paper_metrics.json`. |
| Opening anchor framing (`research_paper.tex:92`) | Partially supported | The sentence refers to two anchors but cites only `eliahou2025mod64`. `constantine2025cyclic` should also appear there. |
| Prior-art ranking and novelty framing (`research_paper.tex:113`, `121-124`) | Weak / overclaimed | Current sources support representative examples, not the stronger ranking and publication-threshold language. |
| Writer-pass recomputation and setup provenance (`research_paper.tex:459-464`) | Support exists but is weakly cited | The relevant repo artifacts exist, but the paragraph should cite them directly. |
| Bibliography integrity (`sources.bib`) | Needs repair | No clear fake paper found, but several entries have wrong or stale metadata. |

## Findings

### High

1. `sources.bib:100-130` has incorrect metadata for three `Scientific Reports` entries.
   - `suksmono2019` (`sources.bib:100-108`) uses `pages = {17387}`, but DOI resolution for `10.1038/s41598-019-50473-w` gives article number `14380`.
   - `suksmono2022quantum` (`sources.bib:111-119`) uses `pages = {749}`, but DOI resolution for `10.1038/s41598-021-03586-0` gives article number `197`.
   - `suksmono2024qaoa` (`sources.bib:122-130`) uses `pages = {18778}`, but DOI resolution for `10.1038/s41598-025-18778-1` gives article number `33254`.
   - This is a traceability problem, not a content problem, but these are load-bearing prior-art citations and their exported metadata should be correct.

### Medium

2. `research_paper.tex:92` under-cites and slightly overstates the opening anchor sentence.
   - The sentence says there are "two unusually sharp exact anchors" but cites only `eliahou2025mod64`.
   - The cyclic `167/80` anchor is from `constantine2025cyclic`, already present in `sources.bib:1-7`.
   - The sentence should either add `constantine2025cyclic` directly or split the claim into two separately cited clauses.
   - The wording "exact anchors" is slightly loose because the Eliahou paper is a modular near-solution, not an exact Hadamard certificate.

3. `research_paper.tex:113` and `research_paper.tex:121-124` contain weakly supported comparison language.
   - "The closest structured-search comparators are ..." (`research_paper.tex:113`) reads like an evidenced ranking, but the cited papers are better treated as representative examples.
   - "The order-668 search problem already has a heuristic literature outside cellular automata" (`research_paper.tex:121`) overstates what the cited Suksmono papers establish. Those papers support heuristic Hadamard search more generally; they do not, from the current bibliography alone, establish an order-668-specific heuristic literature.
   - "Not a publishable advance" and "survives only because" (`research_paper.tex:121-124`) are editorial or venue-threshold judgments, not statements directly supported by the cited technical papers.
   - Recommendation: soften these sentences into authorial positioning, or add broader review/status sources if stronger framing is required.

4. `research_paper.tex:459-464` needs direct repository support citations.
   - The writer-pass rerun claim at `research_paper.tex:459` is likely supported by `results/analysis/cellar_paper_metrics.json`, but that artifact is not cited in the paragraph.
   - The precursor packet budget and interval-description sentence at `research_paper.tex:463-464` is supported by `results/analysis/paper_metrics.json`, but that artifact is not cited there either.
   - This is not a contradiction, but it weakens the paper's own stated evidence discipline.

5. Literature provenance is stale or incomplete even where the cited paper is real.
   - `results/research_context.md:10` says `sources.bib` has `26` entries; the current file has `17`.
   - `results/literature/semantic_scholar_manifest.json` records search history and `seen_paper_ids`, but it is not a full result-to-entry ledger. Some cited items are therefore hard to reconstruct from the manifest alone.
   - Examples:
     - `2503.10320` was searched with `0` Semantic Scholar results at `results/literature/semantic_scholar_manifest.json:15-22`, even though the survey exists.
     - `64-modular Hadamard matrix 668` was searched with `0` results at `results/literature/semantic_scholar_manifest.json:35-42`, even though `eliahou2025mod64` is real and load-bearing.
   - This is a provenance weakness, not evidence that the citations are fake.

6. `sources.bib:42-48` and `sources.bib:80-86` cite preprint versions where published versions now exist.
   - `manzoni2025survey` points to the arXiv preprint, but a journal version now exists.
   - `suksmono2016sa` points to the arXiv preprint, but a published conference-series version exists.
   - These are not false citations, but they are stale choices for a paper emphasizing evidence traceability.

### Low

7. No clear citation hallucination was found among the cited, load-bearing sources.
   - `constantine2025cyclic`, `eliahou2025mod64`, `bright2018satcas`, `fitzpatrick2023williamson`, `djokovic2018goethalsseidel`, `manzoni2025survey`, `mariot2016ols`, `mariot2021semibent`, and the Suksmono line all appear to refer to real works.
   - The stronger problem is metadata drift and over-attribution, not fabricated papers.

## Uncited Or Weakly Cited Comparisons

- `research_paper.tex:113`: "closest structured-search comparators" is too strong for the present citation base.
- `research_paper.tex:121`: "order-668 search problem already has a heuristic literature" is stronger than the cited evidence supports.
- `research_paper.tex:123-124`: the literature-wide novelty and "publishable advance" judgments are authorial inference and should be marked that way if retained.

## Most Important Concrete Sources To Add Or Replace

1. Use the existing `constantine2025cyclic` entry directly in `research_paper.tex:92`.
   - This is the most important missing citation placement issue.

2. Replace or supplement `manzoni2025survey` with the published journal version.
   - `Combinatorial Designs and Cellular Automata: A Survey`
   - `Discrete Applied Mathematics` 379 (2026), `656-674`
   - DOI: `10.1016/j.dam.2025.10.014`

3. Replace or supplement `suksmono2016sa` with the published version.
   - `Finding a Hadamard Matrix by Simulated Annealing of Spin Vectors`
   - `Journal of Physics: Conference Series` 856 (2017), `012012`
   - DOI: `10.1088/1742-6596/856/1/012012`

4. Add direct repo-artifact support for setup and recomputation claims.
   - `results/analysis/cellar_paper_metrics.json` for `research_paper.tex:459`
   - `results/analysis/paper_metrics.json` for `research_paper.tex:463-464`

5. If the paper keeps the stronger prior-art positioning language, add broader review/status support or rephrase.
   - With the current bibliography, rephrasing is safer than trying to force order-668-specific support from general Hadamard-search papers.

## Bottom Line

- The manuscript's branch-specific no-go claim is citation-supportable as written in substance.
- The highest-priority repairs are:
  - fix the wrong `Scientific Reports` metadata in `sources.bib`,
  - add `constantine2025cyclic` directly to the opening anchor sentence,
  - soften or better support the strongest literature-positioning claims,
  - and add explicit repo-artifact citations for writer-pass recomputation and setup details.
