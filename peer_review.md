# Peer Review

## Scores

- Completeness: 5/5
- Technical Rigor: 4/5
- Results Integrity: 4/5
- Citation Accuracy: 1/5
- Compilation: 4/5
- Writing Quality: 4/5
- Figure Quality: 3/5
- Novelty & Creative Contribution: 3/5

## Assessment

- The manuscript is structurally complete and the core theorem for eventually periodic-gap selectors is stated and proved clearly.
- The main quantitative claims in the paper match the current result artifacts: `results/experiments/full_panel_results.json` and `results/experiments/metrics_full_panel.json` support 145 executed cases, 20 waivers, 32 exact-certified cases, and a 28 rational / 4 irrational exact split; `results/experiments/claim_sensitive_ablation.json` supports the reported holdout and order-cap ablations.
- The package is not fully synchronized: `results/experiments/falsifier_controls.md` still reports stale counts (`7` exact rational positives and `13` sparse leaks), which do not match the refreshed metrics (`28` exact rational cases and `12` sparse leaks).
- The PDF exists and I re-ran `pdflatex -> bibtex -> pdflatex -> pdflatex` plus one stabilizing `pdflatex`; the document builds successfully to 26 pages. However, the final compile still reports overfull/underfull boxes, especially around the holdout table and appendix summary table.
- The figures are not default/plain Matplotlib output, but several are still crowded rather than publication-polished. In particular, `figures/fig6_claim_sensitive_ablations.png` has overlapping subplot titles, `figures/fig7_variant_matrix.png` uses oversized titling, and `figures/fig4_full_panel_heatmap.png` is dense at print scale.

## Citation Verification Report

| Bib key | Status | Verification result |
| --- | --- | --- |
| `schaeffer2024` | Verified | arXiv/DOI `10.48550/arXiv.2402.08331` confirms title, Luke Schaeffer / Jeffrey Shallit / Stefan Zorcic, and year 2024. |
| `hieronymi2021` | Verified | DOI `10.46298/lmcs-20(3:12)2024` confirms the LMCS article, authors, and year 2024. |
| `baranwal2021` | Verified | DOI `10.1016/j.tcs.2021.01.018` confirms title, authors, venue, and year 2021. |
| `gnaydin2020` | Incorrect | DOI `10.1016/j.apal.2021.103062` resolves to a 2022 `Annals of Pure and Applied Logic` article, not 2021. |
| `khani2021` | Verified | DOI `10.1016/j.apal.2024.103493` confirms title, authors, venue, and year 2024. |
| `bucci2013` | Verified | DOI `10.1017/etds.2013.69` confirms title, authors, venue, and year 2013. |
| `durand2000` | Verified | DOI `10.1017/S0143385700000584` confirms title, author, venue, and year 2000. |
| `durand2003` | Verified | DOI `10.1017/S0143385702001293` confirms title, author, venue, and year 2003. |
| `durand1998` | Verified | DOI `10.1016/S0012-365X(97)00029-0` confirms title, author, venue, and year 1998. |
| `byszewski2016` | Incorrect | DOI `10.1090/tran/7257` resolves to a 2018 `Transactions of the AMS` article, not 2016. |
| `byszewski2023` | Verified | DOI `10.1016/j.jnt.2025.01.001` confirms title, authors, venue, and year 2025. |
| `adamczewski2022` | Incorrect | DOI `10.1090/tran/8906` resolves to a 2023 `Transactions of the AMS` article, not 2022. |
| `bell2005` | Incorrect | DOI `10.1112/S002461070602268X` resolves to a 2006 `Journal of the London Mathematical Society` article, not 2005. |
| `derksen2005` | Incorrect | DOI `10.1007/S00222-006-0031-0` resolves to a 2007 `Inventiones Mathematicae` article, not 2005. |
| `allouche2018` | Verified | DOI `10.2140/moscow.2019.8.325` confirms title, authors, venue, and year 2019. |
| `maskov2006` | Verified | DOI `10.14311/924` confirms `Self-Matching Properties of Beatty Sequences`, Masakova/Pelantova, `Acta Polytechnica`, year 2007. |
| `mousavi2021walnut` | Incorrect | DOI `10.48550/arXiv.1603.06017` is the 2016 arXiv paper `Automatic Theorem Proving in Walnut`; the BibTeX entry gives year 2021 and mixes the paper with a GitHub repo URL. |
| `oei2020pecan` | Incorrect | URL resolves to the GitHub repository `ReedOei/Pecan`, not to a paper; the entry provides no DOI/publisher metadata, and the stated year 2020 is not supported by the repository metadata I could verify. |

In-text citation audit: every `\cite` key used in `research_paper.tex` is present in `sources.bib`. The only uncited bibliography entries are `mousavi2021walnut` and `oei2020pecan`.

## Novelty Assessment

The novelty is modest but real. The one clearly defensible new contribution is the periodic-gap characterization for ordered Beatty-value subsequences under eventually periodic-gap selectors: this is narrower than nearby Beatty decidability, symbolic linear recurrence, generalized-polynomial definability, or Skolem-Mahler-Lech zero-set results, and the current archive does not show a prior paper solving exactly that ordered-value selector-family problem. By contrast, the proof lemmas are standard infrastructure, the modular-shadow pipeline is a useful verification workflow rather than a new theorem, and the four quadratic certificates sit close to known self-matching/generalized Beatty phenomena and should not be sold as co-equal novelty anchors. The ConceptEvolve artifacts show genuine partial use (`005_convergent_hankel_detector`, `009_pisot_beta_endpoint_sampler`, and the H1 obstruction transfer), but most concept nodes remain deferred, so the cross-domain creative contribution is limited rather than sweeping.

## Verdict

REVISE

The core theorem-backed direction is sound, but the package is not publication-ready because the bibliography fails a zero-tolerance audit, some artifacts are stale/inconsistent, and the sparse-lane framing still overstates what is actually proved.

## Actionable Feedback

1. Repair `sources.bib` completely before resubmission.
   - Fix the incorrect publication years for `gnaydin2020`, `byszewski2016`, `adamczewski2022`, `bell2005`, and `derksen2005`.
   - Replace `mousavi2021walnut` and `oei2020pecan` with clean, citable software references or remove them if they are not cited in the manuscript.
   - Replace Semantic Scholar URLs with canonical DOI / publisher / arXiv URLs wherever possible.

2. Narrow the manuscript's contribution hierarchy.
   - Keep the eventually periodic-gap theorem as the sole theorem-grade novelty claim.
   - Demote the proof lemmas, modular-shadow workflow, and four quadratic examples to supporting roles.
   - State more explicitly that the unrestricted problem from the title remains open.

3. Synchronize the artifact package.
   - Update `results/experiments/falsifier_controls.md` so that it matches the refreshed writer-stage metrics.
   - Check for any other stale summaries that still describe the pre-refresh baseline rather than the current package.

4. Clean the presentation details.
   - Remove the overfull table/layout issues in the PDF.
   - Regenerate `figures/fig6_claim_sensitive_ablations.png` and `figures/fig7_variant_matrix.png` with less crowded titling and more print-friendly typography.

5. Keep the sparse quadratic lane explicitly empirical unless you add the missing controls flagged in `results/verification/benchmark_report.md`.
   - In particular, the paper should not imply a quadratic-family boundary without intercept controls, stronger matched nonquadratic controls, and longer follow-up on unresolved cases such as `salem_quartic / ost_suffix_001`.
