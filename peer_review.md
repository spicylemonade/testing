# Peer Review

## Overall Verdict: DEEPEN

The manuscript is technically coherent as a narrow negative-result paper, and its main quantitative claims are largely consistent with the saved artifacts. It is not submission-ready for two independent reasons. First, `sources.bib` contains multiple incorrect or insufficiently verified entries, which fails the citation-accuracy requirement outright. Second, the underlying contribution is not novel enough for a top-tier venue: the work documents one seed-matched cellular-automaton-style repair attempt on a published order-668 frontier object and shows that it fails. That is useful internal science, but it is not yet a materially new algorithmic, mathematical, or empirical advance.

## Scores

| Criterion | Score (1-5) | Rationale |
| --- | --- | --- |
| Completeness | 5 | All required paper sections are present, including Abstract, Introduction, Related Work, Method, Experiments/Setup, Results, Discussion, Conclusion, and References. |
| Technical Rigor | 3 | The method is mathematically described and the main experiments are reproducible from saved artifacts, but the benchmark remains underpowered for method claims: one frontier seed, one RNG seed, unequal executed restarts, and no CA-off ablations. |
| Results Integrity | 4 | The reported control results, frontier summaries, locality scan counts, and figure annotations are consistent with the saved JSON artifacts. I found no obvious fabricated numbers. Residual auditability limits remain because raw outputs are sampled and top-level run JSON semantics are easy to misread. |
| Citation Accuracy | 1 | Multiple bibliography entries are wrong, incomplete, or not fully verifiable from web sources. This alone blocks acceptance. |
| Compilation | 5 | `research_paper.pdf` exists, and a fresh `pdflatex -> bibtex -> pdflatex -> pdflatex` build completed successfully. Only minor underfull-box warnings remained. |
| Writing Quality | 3 | The manuscript is readable and mostly disciplined, but several interpretation-heavy passages overstate what the evidence proves, especially in the related-work synthesis and discussion. |
| Figure Quality | 4 | The figures are custom-styled, labeled, and publication-oriented rather than default matplotlib output. Some labels are crowded, but the figures are not a rejection-level weakness. |
| Novelty & Creative Contribution | 2 | The surviving contribution is a well-documented falsification scaffold on top of a published seed, not a new method family or a frontier advance. The concept-evolve tree also does not show genuine experimental realization of the broader CE ideas. |

## Major Findings

1. **Citation accuracy fails submission standard.** `sources.bib` contains multiple incorrect entries, including wrong years, wrong venue types, incomplete author lists, non-paper URLs, and at least one entry that is really a proceedings/book title rather than a paper entry. The highest-risk items are `tsompanas2017`, `ghaleb2019`, `leeuwen2000`, `suksmono2024`, `bright2019_williamson`, `artacho2013`, `eliahou2001`, `mariot2019_mols`, and `gadouleau2020`.

2. **Novelty is too weak for the claimed venue.** The paper’s own verification artifacts already narrow the contribution to “a seeded falsification attempt on the published 64-modular order-668 frontier seed,” not a new CA repair method or an order-668 advance. The concept-evolve tree also does not show experimentally realized CE outputs: every inspected `results/concept_evolve/tree/*/concept.json` still has `"experimental_result": null`, so the broader CE bridge ideas were not turned into tested contributions.

3. **Several manuscript passages outrun the saved evidence.** The related-work synthesis and discussion are the weakest parts. In particular, `research_paper.tex:115-127`, `research_paper.tex:624`, `research_paper.tex:650-655`, `research_paper.tex:686-698`, and `research_paper.tex:702` move from observed results to stronger mechanism or positioning claims than the saved artifacts justify.

4. **The benchmark is adequate for branch elimination, not for literature-level method claims.** The negative result is valid as an H1 kill test, but the evidence base is still too narrow for strong method conclusions: one frontier seed, one RNG seed, unequal executed restart coverage, toy solved controls, no actuator-basis ablation, and no CA-off control. This is consistent with `results/verification/benchmark_report.md`, which supports branch gating but explicitly rejects publication-grade benchmark framing.

## Citation Verification Report

All in-text citation keys used in `research_paper.tex` exist in `sources.bib`. I did not find any missing `\cite` key. The problem is bibliography correctness, not missing local keys.

| Bib key | Status | Verification result |
| --- | --- | --- |
| `eliahou2025_64mod668` | Verified | Official Australasian Journal of Combinatorics PDF confirms title, author (Shalom Eliahou), year 2025, venue, volume/issue, and page range. URL is appropriate. |
| `tsompanas2017` | Incorrect | The paper exists, but web results identify it as a Springer chapter associated with *Cellular Automata* / *Emergence, Complexity and Computation* and DOI `10.1007/978-3-319-77510-4_8`, published in 2018, not a 2017 `arXiv.org` journal article. The BibTeX year and venue are wrong, and the URL is only a Semantic Scholar page. |
| `ghaleb2019` | Incorrect | A paper with this title exists in the AIAI 2019 proceedings, but the entry is not cleanly verified as written: the record is stored as an article-like journal entry, the web evidence around the author name is inconsistent with `Osamah Ghaleb`, and the bibliography points to Semantic Scholar rather than the actual paper page. Under the zero-tolerance rule this remains incorrect/unverified. |
| `ghaemi2022` | Verified | PLOS ONE results confirm the title, author list, year 2022, journal, and DOI `10.1371/journal.pone.0265065`. |
| `leeuwen2000` | Incorrect | Web results show this is a Springer proceedings/book title (*Engineering Societies in the Agents' World*), not a normal article by `J. Leeuwen and Andrea Omicini and R. Tolksdorf and F. Zambonelli`. The current entry conflates a volume/proceedings title with paper-style metadata. |
| `suksmono2019` | Verified | Scientific Reports confirms the title, authors, year 2019, venue, and DOI `10.1038/s41598-019-50473-w`. |
| `suksmono2024` | Incorrect | The paper exists, but the official Scientific Reports record is from 2025, not 2024. The BibTeX year is wrong. |
| `suksmono2018` | Verified | MDPI *Entropy* confirms the title, author, year 2018, venue, and DOI `10.3390/e20020141`. |
| `suksmono2022` | Verified | Scientific Reports confirms the title, authors, year 2022, venue, and DOI `10.1038/s41598-021-03586-0`. |
| `bright2018` | Verified | AAAI results confirm the title, authors, year 2018, venue, and DOI `10.1609/aaai.v32i1.12203`. |
| `bright2019` | Verified with metadata cleanup needed | The paper exists in *Annals of Mathematics and Artificial Intelligence* with DOI `10.1007/s10472-019-09681-3`, but the BibTeX author metadata are not exact as written. |
| `bright2019_williamson` | Incorrect | A short publication with this title exists, but the current entry is not correct as written: the year and venue metadata are off or too vague (`ACCA`), and the DOI corresponds to a specific ACM publication record that is not captured accurately here. |
| `cati2024` | Verified | arXiv record `2411.18897` confirms the title, authors, year 2024, and DOI-style arXiv identifier. |
| `artacho2013` | Incorrect | The paper exists, but the official journal record is associated with 2014 publication metadata tied to DOI `10.1017/S1446181114000145`. The BibTeX year is wrong and the entry is incomplete. |
| `eliahou2005` | Verified | Web results confirm the title, authors, year 2005, venue (*Discrete Mathematics*), and DOI `10.1016/j.disc.2005.02.021`. |
| `eliahou2001` | Incorrect / insufficiently verified | The paper clearly exists and the title/authors/journal/year are supported by web references, but I could not independently verify the DOI/landing record cleanly enough from web search. Under the review instructions, an entry not fully verifiable must be flagged incorrect. |
| `sudhakaran2022` | Verified | arXiv/OpenReview results confirm the title, authors, year 2022, and arXiv identifier `2205.06806`. |
| `mariot2019_mols` | Incorrect | The paper exists, but the official journal version is a 2020 *Designs, Codes and Cryptography* article with a fuller author list and DOI. The current entry has the wrong year, truncated authors, missing DOI/pages, and only a Semantic Scholar URL. |
| `gadouleau2020` | Incorrect | The paper exists as an IACR ePrint preprint, but the current entry does not use the actual ePrint URL and therefore does not provide a correct direct paper link. The metadata should be repaired before use. |

## Novelty Assessment

The strongest honest reading of this work is: it takes a published 64-modular order-668 frontier seed, defines one compressed CA-flavored repair policy in the same coordinates as matched local-search baselines, and shows that this policy fails. That is a useful negative result for internal branch selection, but it is not a genuinely new algorithmic contribution, theorem, or frontier advance. The direct one-packet locality scan is the most interesting part of the package because it turns a vague “fake locality” intuition into a finite computation. Even so, that scan remains a diagnostic attached to a failed single-branch pilot. The broader CE-inspired design space was not converted into tested new methods: the concept tree folders still lack `experimental_result` fields, and the promoted follow-on ideas (`H2`, decoder-graph bridges, message-passing hybrids) remain proposals rather than contributions. Relative to the named prior art, the work does not yet produce a material “difference that matters” beyond careful negative documentation. That is enough for an internal pivot memo, not for a top-tier novelty score.

## What Must Be Deepened

To elevate this from an internal negative-result package to a publishable research contribution, the next cycle needs novelty that is substantive rather than rhetorical:

1. **Deliver a representation-changing method, not another retune of H1.**
   - A credible next step would be an actuator basis or locality graph that is genuinely different from one-bit packet scoring, for example composite packets, a defect-packet influence graph, or a lag-space/decoder-graph method that remains local after inspection.

2. **Show that the “CA” part causes something nontrivial.**
   - Run matched ablations against CA-off variants (zero coupling, zero refractory, scorer-only, fallback-disabled). Without that, the work still risks collapsing to generic local search with CA vocabulary.

3. **Produce evidence that survives beyond one canonical seed and one budget.**
   - At minimum: multiple RNG seeds, equal executed restart coverage, a small budget sweep, and a perturbation suite around the frontier seed.

4. **Clear the structured-family leakage problem for H2 or any successor branch.**
   - If the next method effectively collapses into Williamson/Turyn/Goethals-Seidel/cocyclic/block-circulant search, the honest claim is “optimizer over a known family,” not a new CA contribution.

5. **If the project remains negative, make the negative result deeper.**
   - A stronger negative paper would need either a theorem or a sharper empirical impossibility statement, for example a certified barrier for a whole actuator class, not only for the currently implemented H1 branch.

## Actionable Feedback

- Repair `sources.bib` completely before any submission-facing use.
- Rewrite the interpretation-heavy passages so they state what is observed, what is inferred, and what is only proposed.
- Keep the paper’s core claim narrow: no exact order-668 matrix was found, and H1 did not beat the published seed.
- Treat the current paper as an internal falsification record unless a successor method survives matched controls and leakage audits.
- If the goal is publication rather than internal branch management, invest the next cycle in a genuinely new method family or a much stronger impossibility result.
