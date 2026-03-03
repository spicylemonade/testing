# Peer Review of `research_paper.tex`

## Scores (1-5)

| Criterion | Score | Assessment |
| --- | ---: | --- |
| 1. Completeness | 4 | All core sections are present (Abstract, Introduction, Related Work, Method, Results, Discussion, Conclusion, References). The paper uses `Experimental Setup` rather than a section explicitly named `Experiments`, but experiment design and protocol details are included. |
| 2. Technical Rigor | 4 | Methodology is clearly described, includes governing equations, and documents diagnostics/provenance. Reproducibility metadata is good, though methodological detail for force/integrator confounds and uncertainty reporting could be stronger. |
| 3. Results Integrity | 5 | Reported key numbers match repository artifacts (`results/experiments/statistics.json`, `results/research/scaling_eval.json`, `results/experiments/sensitivity_dt_softening.json`, `results/baseline/metrics.json`). Matrix coverage (45 runs) is consistent with `results/experiments/raw/coverage_summary.json`. |
| 4. Citation Accuracy | 5 | Every entry in `sources.bib` was checked via web search and DOI resolution; all entries correspond to real papers with matching title/authors/year/venue and resolving DOI URLs. All in-text citation keys resolve to bibliography entries. |
| 5. Compilation | 5 | `research_paper.pdf` exists and was recompiled successfully using `pdflatex -> bibtex -> pdflatex -> pdflatex`; final pass completed without citation/reference warnings. |
| 6. Writing Quality | 4 | Tone is professional and logically organized; claims are generally evidence-backed. A few passages remain dense and could better separate limitations from claims. |
| 7. Figure Quality | 2 | Figures are serviceable but not publication-grade. Several panels are visually basic and lack uncertainty visualization; readability/layout is weak in places (notably the sensitivity/runtime figure). |

## Citation Verification Report (every `sources.bib` entry)

Verification protocol used for each entry:
- Web search: Crossref bibliographic query (`https://api.crossref.org/works?query.bibliographic=...`) to confirm discoverability and DOI match.
- Metadata validation: Crossref DOI record (`https://api.crossref.org/works/<doi>`) for title/authors/year/venue checks.
- DOI resolution: `https://doi.org/<doi>` with CSL metadata negotiation to confirm resolving URL and canonical record.

- `barnes1986` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `greengard1987` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `yoshida1990` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `forest1990` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `wisdom1991` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `duncan1998` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `chambers1999` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `springel2005` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `rein2012` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `reinspiegel2015` — VERIFIED via web search and DOI resolution. Title/authors/venue/DOI match; year is valid against Crossref date fields (print year 2015).
- `reintamayo2015` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `potter2017` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.
- `rein2019` — VERIFIED via web search and DOI resolution. Title/authors/year/venue/DOI match.

In-text citation-key consistency check:
- All in-text citation keys in `research_paper.tex` map to entries in `sources.bib`.
- One bibliography entry (`rein2012`) is currently uncited in the main text (not an accuracy error, but potentially unnecessary in final bibliography scope).

## Overall Verdict: REVISE

The manuscript is technically coherent, reproducible, and citation-accurate. However, per venue standards and the stated review rule set, figure quality is below acceptance threshold (Criterion 7 < 3), so the paper should be revised before acceptance.

## Actionable Revision Requests

1. Regenerate all final figures to publication quality, not just correctness:
   - Show uncertainty/dispersion (e.g., seed-level distributions, CI bars) for comparison claims.
   - Increase readability (font sizing, axis spacing, panel labeling, tick management) for print-scale rendering.
   - Use consistent visual encodings across figures (palette, legends, marker semantics, annotation style).
2. Improve Figure 4 (`figures/final/claim_04_sensitivity_and_runtime_gap.*`):
   - Fix crowded/overlapping visual elements and improve separation between heatmap/colorbar and runtime panel.
   - Use a scaling strategy (inset, broken axis, ratio plot, or log scale) so the threshold bar remains interpretable next to the large observed runtime.
3. Upgrade Figure 1/2-style bar summaries:
   - Replace or augment simple two-bar panels with distribution-aware plots (box/violin + point estimates) and explicit sample size annotations.
4. Minor structure polish:
   - Consider renaming/adding a top-level `Experiments` section heading for strict rubric alignment.
