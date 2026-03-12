# Peer Review

## Findings

1. **Citation accuracy fails the stated bar and blocks acceptance.** I verified every entry in `sources.bib` via web search. Seven of the fifteen entries are bibliographically incorrect or too incomplete for publication use, including four entries that are actually cited in the manuscript: `oeisA129258`, `oeisA129259`, `kimberling100conjectures`, and `pach2017multiplicativebases` (`sources.bib:1`, `sources.bib:10`, `sources.bib:19`, `sources.bib:93`). Under the task's zero-tolerance citation rule, this alone rules out ACCEPT.

2. **The contribution is narrower than the paper's venue target.** The manuscript and the repo's own novelty ledgers converge on the same position: the defensible contribution is structural cleanup of a public recurrence plus a validated negative-result package, not a new mechanism, not a proof-quality invariant, and not progress on boundedness. See `research_paper.tex:72`, `research_paper.tex:94`, `results/verification/novelty_report.md:33`, `results/verification/novelty_report.md:176`, and `results/literature/prior_art_gap.md:7`. That is useful work, but for a top-tier standard it is still incremental.

3. **Some headline witness-mechanism claims are stronger than the current artifact basis.** The paper's witness-taxonomy narrative and the hypergraph/modular summary are mostly directionally correct, but the repo's own benchmark notes say the headline witness summaries still rely on first-witness bookkeeping rather than full-pair canonicalization (`research_paper.tex:549`, `research_paper.tex:563`, `research_paper.tex:685`; `results/verification/benchmark_report.md:141`; `results/verification/verification_summary.md:60`). In addition, the cycle-rank sentence at `research_paper.tex:599` is stronger than the cited JSON alone supports; the controls/surrogates part lives in the markdown audit, not in `item_029_hypergraph_metrics.json`.

4. **Results integrity is otherwise mostly sound.** I did not find fabricated core numbers. The baseline `17` record gaps, maximum gap `30`, late record steps `92320`, `247399`, `729353`, gap-30 hypergraph counts, checker/runtime numbers, and the axis-swapped `31` claim all match stored artifacts in `results/experiments/` and `results/analysis/`. The main issue is not invented data; it is claim strength and evidence routing.

5. **Compilation and figures are adequate, not polished.** `research_paper.pdf` exists, and a fresh `pdflatex` rebuild completed successfully. The build still emits multiple overfull/underfull box warnings, and Figures 4 and 7 have visible title crowding at the top of the rendered PNG/PDF outputs (`figures/src/figure4_gap_composition.tex:21`, `figures/src/figure7_gap_distribution.tex:21`). The figures are custom TikZ/PGFPlots figures, not default matplotlib exports, so this is a polish issue rather than a disqualifying figure-quality failure.

## Scores

| Criterion | Score | Notes |
|---|---:|---|
| Completeness | 5 | All required sections are present: Abstract, Introduction, Related Work, Method, Experimental Setup, Results, Discussion, Conclusion, References. |
| Technical Rigor | 3 | The theorem section is substantive and the computational protocol is reproducible, but the checker horizon is partial and some mechanism-level summaries outrun the strongest canonicalized evidence. |
| Results Integrity | 4 | Core quantitative claims match the committed artifacts, and I found no fabricated results. The main weakness is overinterpretation of some witness-level summaries. |
| Citation Accuracy | 1 | Seven bibliography entries fail strict verification; four of those are cited in the paper. |
| Compilation | 4 | The PDF exists and `pdflatex` succeeds, but the build is not warning-free and layout polish remains uneven. |
| Writing Quality | 4 | The manuscript is clear, professional, and generally disciplined about scope. |
| Figure Quality | 4 | The figures are clearly custom and publication-oriented, but several panels need spacing/title cleanup. |
| Novelty & Creative Contribution | 2 | The surviving contribution is mainly structural clarification plus a negative-result audit package around a public OEIS/Kimberling object. |

## Citation Verification Report

All 10 in-text `\cite` keys used in `research_paper.tex` exist in `sources.bib`. The problem is not missing keys; it is incorrect bibliography metadata.

- `oeisA129258`: **Incorrect.** Real OEIS entry, but the BibTeX author/year do not match the OEIS record.
- `oeisA129259`: **Incorrect.** Real OEIS entry, but the BibTeX author/year do not match the OEIS record.
- `kimberling100conjectures`: **Incorrect.** Real Kimberling page, but the recorded title is wrong and the page is better identified as the Evansville unsolved-problems page.
- `ford2011multiplicationtable`: **Verified.** Title, author, journal, year, pages, and DOI match.
- `ford2008divisorinterval`: **Verified.** Title, author, journal, year, pages, and DOI match.
- `ford2006divisor2y`: **Verified.** Real arXiv preprint; title, author, year, and URL match.
- `ford2020roughdivisorinterval`: **Incorrect.** Real paper, but the BibTeX year/pages are inconsistent with the journal record and the entry omits volume/issue.
- `koukoulopoulos2010restrictedtables`: **Incorrect.** Real work, but the entry is a Semantic Scholar placeholder instead of a proper thesis/publication record with venue metadata.
- `mehdizadeh2021smoothmultiplicationtable`: **Verified.** Metadata and DOI match the Journal of Number Theory record.
- `pach2017multiplicativebases`: **Incorrect.** Real paper, but the cited volume/issue/pages correspond to the 2018 journal issue, not year 2017.
- `pus1992multiplicativebases`: **Verified.** Metadata and DOI match.
- `dressler1970newmultiplicativebases`: **Verified.** Metadata and DOI match.
- `nathanson1987multiplicativerepresentations`: **Verified.** Metadata and DOI match.
- `brent2019algorithmsmultiplicationtable`: **Incorrect.** Real work exists, but this entry is only a non-canonical Semantic Scholar placeholder and does not cleanly identify either the preprint or the journal publication.
- `meisner2018functionfieldmultiplicationtable`: **Verified.** Real arXiv preprint; title, author, year, and URL match.

Summary:

- Verified: 8
- Incorrect or bibliographically inadequate: 7
- Fabricated papers found: 0
- In-text citation keys missing from `sources.bib`: 0

## Novelty Assessment

The work is honest and narrower than many automated math manuscripts, but it is still not a genuinely deep new contribution by top-tier standards. The most defensible novelty is local: formal proofs of several exact consequences of Kimberling's public recurrence, clarification that the archived update-order variants are identities/symmetries, and a better-audited finite-horizon negative-result package. The repo's own novelty files say essentially this: the package survives as a "validated negative-result and overlap-control dossier" rather than as a new asymptotic theorem or new mechanism (`results/literature/prior_art_gap.md:13`, `results/verification/novelty_report.md:48`, `results/verification/novelty_report.md:176`). The ConceptEvolve layer does not rescue the novelty score. A few branch statuses were updated (`pivoted`, `retired`, `completed_negative`, `active_control`), but the surviving message in `results/concept_evolve/concept_delta.md:24` is again that positive bridges were retired and the contribution is a cleaner obstruction map. That is a modest contribution, not a surprising one.

## Overall Verdict

**DEEPEN**

This manuscript is not acceptance-ready. The citation audit fails outright, and the underlying research contribution is still too incremental for the claimed venue standard. Under the task rubric, a novelty score of 1-2 together with quality issues requires **DEEPEN**, not **REVISE**.

## Deepening Feedback

1. Repair `sources.bib` completely. Replace placeholder entries with primary records, fix the OEIS and Kimberling metadata, fix the Pach year, and either correct or remove every entry that cannot be fully verified.
2. Recast the paper around its actual contribution boundary unless new mathematics is added. As it stands, the safe pitch is "structural clarification plus audited negative results," not "new mechanism."
3. Either recompute the headline witness-taxonomy claims from full witness-pair corpora under multiple canonicalizations or demote them to exploratory observations. In particular, clean up the `research_paper.tex:599` cycle-rank summary.
4. If the goal is a stronger novelty claim, produce at least one recurrence-specific result that generic local product coverage does not mimic. In this domain that means something like a new theorem on frontier coverage, a genuinely `T`-specific invariant, or a nontrivial compression law that survives matched controls and surrogate baselines.
5. Use the ConceptEvolve layer more substantively or stop leaning on it as a novelty signal. Most of the tree still looks like steering and retirement of ideas rather than experimentally realized bridge hypotheses.
6. Regenerate the crowded figures and clean the LaTeX layout warnings before the next review cycle.

## Scope Note

I read `research_paper.tex`, checked that `research_paper.pdf` exists, rebuilt the paper once with `pdflatex`, read the rubric and the required verification/novelty artifacts, spot-checked the core results against `results/` and `figures/`, and verified every `sources.bib` entry via web search. I did not rerun the million-step experiments or independently re-prove the theorem section.
