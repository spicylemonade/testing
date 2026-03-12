# Final Research Package Summary

- Primary result: `results/final_claim_memo.md` now separates the theorem-backed eventually-periodic-gap characterization from four exact-certified quadratic examples and the remaining empirical sparse leaks.
- Revision experiments: `results/experiments/claim_sensitive_ablation.md` extends all 15 uncertain holdouts to `320`, adds fit-length sensitivity, breaks `salem_quartic / ost_suffix_001` by `80`, and keeps the surviving sparse quadratic lane empirical.
- Citation base: `sources.bib` now uses canonical DOI/arXiv URLs and clean Walnut/Pecan software-paper references.
- Figures: `figures/fig4_full_panel_heatmap.pdf`, `figures/fig6_claim_sensitive_ablations.pdf`, and `figures/fig7_variant_matrix.pdf` were regenerated with the seaborn styling stack and print-friendlier layouts; the full figure set was refreshed in the same pass.
- Verification bundle: `results/verification/benchmark_report.md`, `results/verification/citation_audit.md`, and `results/verification/verification_summary.md` record the benchmark, citation, and reviewer context for the revised package.
- Remaining writer-side issue: the rebuilt `research_paper.pdf` still reports overfull/underfull table warnings because `research_paper.tex` was intentionally not edited in this revision.
