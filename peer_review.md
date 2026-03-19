# Peer Review

I read `research_paper.tex`, rebuilt `research_paper.pdf`, read `research_rubric.json`, inspected the claimed result artifacts under `results/` and `figures/`, re-ran `python3 tools/kakeya_trace_corpus.py`, and verified every bibliography entry in `sources.bib` against web-searchable sources.

The paper has a real narrow core: the exact verifier exists, the `2 x 2` corpus and one-sided strip atlas are reproducible, and the main quantitative claims in the paper match the newer machine-readable artifacts. But the manuscript is not publication-ready. The bibliography has zero-tolerance failures, the repository still contains contradictory “verifier missing” source-of-truth files, several figures are not yet publication quality, and the novelty is narrower than the framing suggests.

## Scores

| Criterion | Score | Rationale |
| --- | ---: | --- |
| Completeness | 5 | The paper contains Abstract, Introduction, Related Work, Method, Experimental Setup, Results, Discussion, Conclusion, References, and appendices. |
| Technical Rigor | 3 | The exact finite-audit portion is formal and reproducible, but the larger-search and CA-method story is not benchmark-complete and the semantics boundary is still limited to the repository verifier. |
| Results Integrity | 3 | The core exact-trace claims match the current artifacts and I reproduced the tiny-corpus outputs, but the repo still contains stale blocker-era files that contradict the paper’s current narrative. |
| Citation Accuracy | 1 | Several entries are incorrect or not web-verifiable, which is a hard failure under the stated zero-tolerance standard. |
| Compilation | 4 | The PDF builds successfully with `pdflatex -> bibtex -> pdflatex -> pdflatex`, but the log still has multiple overfull-box warnings and some layout rough edges. |
| Writing Quality | 4 | The prose is clear and professional, but it sometimes frames the contribution more broadly than the evidence supports. |
| Figure Quality | 2 | The style is custom rather than default, but several figures are crowded or hard to read, especially the coverability and bridge-decision graphics. |
| Novelty & Creative Contribution | 2 | The strongest contribution is a narrow semantics-relative local theorem plus tiny exact audits. This is not yet a surprising arithmetic-Kakeya advance or a demonstrated CA-method breakthrough, and the ConceptEvolve trail is only weakly tied to experimentally validated new ideas. |

## Major Findings

1. The core exact-result claims are supported by the newer exact-trace artifacts.
The `44,608 / 48 / 7/4 / four trace signatures of size 12` claims match `results/theory/forcing_traces/tiny_2x2_full_seeds_le3/corpus_summary.json`. The `256 / 8,192 / 0 strict improvements` claims match `results/theory/forcing_traces/index.json`. The larger-family negative frontier matches `results/experiments/h1_exact_advantage.md`. Re-running `python3 tools/kakeya_trace_corpus.py` reproduced the same summary counts.

2. Source-of-truth hygiene is still poor.
The paper says older blocker-era files are historical only, but the repo still contains live contradictory artifacts such as `results/final_assessment.md`, `results/experiments/h1_controls.md`, and `results/experiments/complexity_sweep.md`, all of which still describe a missing-verifier regime. The manuscript acknowledges this conflict, but the repo still needs one authoritative post-pivot manifest.

3. Citation accuracy fails the review standard.
Most entries are real papers, but `sources.bib` still contains at least one non-web-verifiable local artifact and at least two metadata-defective entries. Under the stated review rules, that alone blocks acceptance.

4. The paper’s real novelty is narrow.
The most credible novelty is the width-`2` seedless-column obstruction under the repository’s executable semantics, together with the exact `2 x 2` and one-sided-strip classifications. That is interesting, but it is much narrower than “solved using cellular automata,” much narrower than genuine arithmetic-Kakeya progress, and not a benchmark-cleared CA contribution. The ConceptEvolve tree does not show strong experiment-trace evidence inside the `concept.json` files; I did not find `experimental_result` fields demonstrating that the bridge ideas themselves were rigorously turned into tested new directions.

5. Several figures are not yet publication quality.
The figure suite is styled and not generic, which is good. But `fig_coverability_modes` has overlapping text and weak contrast in the central labels, `fig_bridge_decisions` is cramped and text-heavy, and some panels rely on annotation blocks to compensate for sparse data. That is below top-tier figure quality.

## Citation Verification Report

All in-text citation keys used in `research_paper.tex` resolve to entries in `sources.bib`. `leng2024` is present in `sources.bib` but not cited in the manuscript.

| Bib key | Status | Verification result |
| --- | --- | --- |
| `katz1999` | Verified | International Press / Mathematical Research Letters confirms the title, Nets Hawk Katz and Terence Tao, 1999, *Mathematical Research Letters*, DOI `10.4310/MRL.1999.V6.N6.A3`. |
| `green2017` | Verified | Springer confirms *On the arithmetic Kakeya conjecture of Katz and Tao*, Ben Green and Imre Z. Ruzsa, published 2018 / volume year 2019 in *Periodica Mathematica Hungarica*, DOI `10.1007/s10998-018-0270-z`. |
| `cowenbreen2020` | Verified | arXiv confirms *Pattern Problems related to the Arithmetic Kakeya Conjecture*, Charlie Cowen-Breen, Elene Karangozishvili, Narmada Varadarajan, Thomas Wang, 2020, arXiv `2011.07056`. |
| `pohoata2024` | Verified | arXiv confirms *Generalized Arithmetic Kakeya*, Cosmin Pohoata and Dmitrii Zakharov, 2024, arXiv `2411.13395`. |
| `tao2025` | Verified | arXiv confirms *Sum-difference exponents for boundedly many slopes, and rational complexity*, Terence Tao, 2025, arXiv `2511.15135`. |
| `hickman2018` | Verified | Discrete Analysis confirms *The Fourier restriction and Kakeya problems over rings of integers modulo N*, Jonathan Hickman and James Wright, 2018, DOI `10.19086/da.3682`. |
| `bond2013` | Verified | DBLP and the unpaywalled paper confirm *Abelian Networks I. Foundations and Examples*, Benjamin Bond and Lionel Levine, 2016, *SIAM Journal on Discrete Mathematics*, DOI `10.1137/15M1030984`. |
| `bond2014` | Verified | arXiv plus external publication metadata confirm *Abelian networks II. Halting on all inputs*, Benjamin Bond and Lionel Levine, published 2016 in *Selecta Mathematica*, DOI `10.1007/s00029-015-0192-z`. |
| `dennunzio2023` | Verified | DBLP / IEEE metadata confirm *An Easy to Check Characterization of Positive Expansivity for Additive Cellular Automata Over a Finite Abelian Group*, Dennunzio, Formenti, Margara, 2023, *IEEE Access*, DOI `10.1109/ACCESS.2023.3328540`. |
| `faldor2024` | Verified | The paper is real: *Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity*, Maxence Faldor and Antoine Cully, 2024, DOI `10.1162/isal_a_00827`, arXiv `2406.04235`. The venue string in the BibTeX should be normalized to the actual ALIFE proceedings form, but the paper itself is real. |
| `novikov2025` | Incorrect metadata | arXiv `2506.13131` is real, but the author list in `sources.bib` is wrong: the arXiv record lists 18 human authors and does not list `Google DeepMind` as a bibliographic author. The `journal={arXiv.org}` field is also not a proper venue/preprint citation. |
| `georgiev2025` | Incorrect metadata | arXiv `2511.02864` is real and the title/authors/year are correct, but the entry uses `journal={arXiv.org}` instead of a proper arXiv-preprint citation form. Under the stated zero-tolerance rule, I count this as incorrect metadata. |
| `bourgain1999` | Verified | The paper exists as *On the Dimension of Kakeya Sets and Related Maximal Inequalities*, J. Bourgain, 1999, *Geometric and Functional Analysis*, DOI `10.1007/S000390050087`. |
| `leng2024` | Verified but unused | arXiv confirms *Improved Bounds for Szemerédi's Theorem*, James Leng, Ashwin Sah, Mehtaab Sawhney, 2024, arXiv `2402.17995`. It is unused in the paper and should probably be removed from `sources.bib` unless needed. |
| `moura2008` | Verified | Springer confirms *Z3: An Efficient SMT Solver*, Leonardo de Moura and Nikolaj Bjørner, TACAS 2008, DOI `10.1007/978-3-540-78800-3_24`. |
| `wang2025` | Verified | The preprint is real: *Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions*, Hong Wang and Joshua Zahl, 2025, arXiv `2502.17655`. The BibTeX should ideally cite the arXiv DOI or arXiv URL directly rather than a Semantic Scholar landing page. |
| `archivara2026task` | Incorrect / not web-verifiable | I could not verify this via web search as a public paper or external scholarly source. It is a local repository provenance artifact, not a normal bibliography entry, and should be cited as repository/task provenance or a footnote instead of a scholarly reference. |

## Novelty Assessment

This work does contribute something new, but only in a narrow sense. The width-`2` seedless-column obstruction, the exact `2 x 2` classification, and the one-sided low-height no-go atlas appear to be genuinely new repository-level results under the executable verifier semantics. That said, this is not a surprising arithmetic-Kakeya advance, not a witness below `1.675`, not an equivalence theorem back to the full forcing-pair formulation, and not a demonstrated CA-method breakthrough over baseline search. The ConceptEvolve scaffolding also does not show strong evidence of genuine cross-domain novelty generation: the tree `concept.json` files do not visibly carry `experimental_result` fields that would show the bridge ideas were systematically converted into validated experiments. In its current state, the paper reads more like a careful exact local audit plus a semantics-relative obstruction theorem than a field-moving creative contribution.

## Overall Verdict

**DEEPEN**

The paper is technically more serious than a generic pipeline writeup, and the exact local theorem/computation package is real. But the research contribution is still too narrow for a top-tier venue, and it is coupled to fixable paper-quality problems that also need attention. Even if the citation issues were corrected, the present contribution would still read as a careful local negative-result package rather than a genuinely surprising arithmetic-Kakeya or cellular-automaton breakthrough.

## What “Deeper” Needs To Mean Here

1. Produce a stronger mathematical contribution.
Examples: an exact theorem beyond the current width-`2` / one-sided-height-`3` audited classes; a nontrivial two-sided or macrocell obstruction theorem; or an exact verified witness family that materially improves the current `7/4` micro-regime and pushes toward or below `1.675`.

2. Bridge the semantics gap.
If the paper wants to matter mathematically beyond the repository, it needs either a proof that the executable quotient-span semantics matches the intended forcing-pair definition in the needed regime, or a sharply delimited claim that is much more explicit about what is and is not being proved.

3. Either drop the CA-method claim or earn it.
If the paper wants to claim something methodologically novel about CA search, it needs at least one matched benchmark block against non-CA baselines using the same exact verifier, plus the promised label-shuffle, held-out-geometry, held-out-`X`, and complexity controls.

4. Make the ConceptEvolve story real rather than retrospective.
If CE is part of the novelty case, the concept-tree artifacts need explicit experiment linkage and outcomes, not just bridge labels and narrative summaries.

5. Fix the quality blockers in parallel.
Correct the defective bibliography entries, remove or reclassify the local provenance citation, create a single authoritative post-pivot evaluation manifest, and regenerate the weak figures so they are readable without dense explanatory text.

## Actionable Feedback

1. Correct `sources.bib` immediately.
Remove `archivara2026task` from the scholarly bibliography, fix `novikov2025`, fix `georgiev2025`, and normalize the preprint/proceedings entries so the venue and URL/DOI fields match the actual source.

2. Reconcile the repository narrative.
Create one explicit post-pivot manifest that states which artifacts are authoritative and which blocker-era files are historical. Right now the manuscript is correct that the newer exact-trace artifacts exist, but the repo is still self-contradictory.

3. Reframe the paper around the narrow supported claim.
The strongest honest title/subtitle story is an exact local theorem-and-computation paper under repository semantics, not “cellular automata solved the task” and not broad arithmetic-Kakeya progress.

4. Improve the figures before resubmission.
`fig_coverability_modes` and `fig_bridge_decisions` should be redesigned from scratch for readability. Reduce text density, remove overlaps, enlarge labels, and make each figure intelligible without a paragraph-length caption.

5. If you want a stronger paper rather than a cleaner narrow paper, deepen the science.
The clearest next targets are a genuine coupled or two-sided construction, a stronger exact obstruction beyond the audited narrow classes, or a benchmark-cleared CA result on the exact witness object.
