# Peer Review

## Overall Verdict

**DEEPEN**

The manuscript is honest about not improving the bound, but the achieved contribution is still an internal no-go / route-specification memo rather than a publishable Ramsey advance. The only potentially novel idea, a transfer-safe cross-family obstruction atlas for failed `42 -> 43` extensions, is entirely unexecuted. Quality blockers remain as well: multiple bibliography entries are incorrect or not fully verifiable, `pdflatex` exits nonzero on every pass, the central exact-measurement table contains a stale unsupported count, and several figures are visibly not publication-quality.

## Scores

| Criterion | Score | Rationale |
| --- | ---: | --- |
| Completeness | 5 | All required high-level sections are present: abstract, introduction, related work, background/method, experimental setup, results, discussion, conclusion, and references, plus appendices. |
| Technical Rigor | 2 | The paper contains formal definitions, algorithms, and proofs, but the technical core is mostly claim-governance formalization rather than new Ramsey computation, and no actual experiment on the proposed `H1` object is executed. |
| Results Integrity | 3 | Most repository-count claims check out, and the paper does not fabricate a bound result. However, the measurement table is presented as exact while `Known papers tracked = 106` is contradicted by current packet sources that record `111`, and the stale value is hardcoded in `figures/generate_figures.py:123`. |
| Citation Accuracy | 1 | Citation accuracy fails the stated zero-tolerance bar. At least three bibliography entries are incorrect or not fully verifiable (`noga2022`, `gauthier2025`, `mckayramseydata`), and several others have broken or weak metadata. |
| Compilation | 2 | `research_paper.pdf` exists and the required `pdflatex -> bibtex -> pdflatex -> pdflatex` pipeline can emit a PDF, but all three `pdflatex` passes exit with LaTeX errors because `\theHalgorithm` and `\theHALG@line` are undefined at `research_paper.tex:45-46`. |
| Writing Quality | 4 | The prose is clear, organized, and professionally toned. The main weakness is conceptual over-weighting: governance-level lemmas and a repository-state theorem are written with more scientific gravitas than the actual Ramsey contribution merits. |
| Figure Quality | 1 | Several figures are visibly broken or not publication-ready. `figures/fig_evidence_dashboard.png` and `figures/fig_prior_work_matrix.png` render raw matrix option syntax inside cells, while `figures/fig_frontier_timeline.png` and `figures/fig_bridge_status.png` have severe overlap/clipping. |
| Novelty & Creative Contribution | 1 | The paper does not demonstrate a new Ramsey object, new algorithm, new bound, or surprising empirical/theoretical result. The only possibly novel route remains a hypothesis, not an achieved contribution. |

## Findings

1. **Novelty is still entirely prospective.** The manuscript correctly narrows itself to an infrastructure-only plus negative-result scope, but that is also the main novelty problem. The proposed `H1` obstruction-atlas route is the only potentially interesting idea, yet none of the route-defining artifacts exists under `results/h1/`, no transfer or witness-safety evidence is reported, and all 11 `results/concept_evolve/tree/*/concept.json` files have `experimental_result = null`. The concept-evolution packet therefore documents brainstorming and prioritization, not realized cross-domain experimentation.

2. **The citation spine does not pass a zero-tolerance audit.** I verified every entry in `sources.bib` by web search. `gauthier2025` is incorrect, `noga2022` is not verifiable as a real paper citation, and `mckayramseydata` has a title/url mismatch. Additional entries such as `narvez2024` and `radziszowski2024ds1` are real but still need metadata repair. Under the task instructions, any such failure blocks acceptance.

3. **The figures are not publication-quality.** Two matrix figures visibly leak TikZ matrix option syntax into the rendered cells, which is a hard production error, not a cosmetic preference. Two others have overlapping annotations that make them hard to read. On figure grounds alone this would require at least `REVISE`; combined with the novelty deficit, it contributes to `DEEPEN`.

4. **Compilation is not clean.** A fresh rebuild reproduces `research_paper.pdf`, but every `pdflatex` pass exits nonzero with:
   - `LaTeX Error: Command \theHalgorithm undefined.`
   - `LaTeX Error: Command \theHALG@line undefined.`
   
   Those originate at `research_paper.tex:45-46`, so the manuscript does not satisfy the clean-compilation bar.

5. **The results section overstates “exact deterministic” integrity in one central place.** `research_paper.tex:549-568` says all table entries are exact repository measurements, but the row `Known papers tracked = 106` at `research_paper.tex:556` is inconsistent with `results/research_context.md:9`, `results/research_context.json:42`, and `results/literature/semantic_scholar_manifest.json:556`, which all record `111`. This is not broad fabrication, but it is still a concrete support failure in the paper’s main measurement table.

## Citation Verification Report

All 15 unique in-text citation keys in `research_paper.tex` resolve to entries in `sources.bib`. The bibliography contains 20 entries total; 5 are unused in the manuscript but were still audited.

| Bib key | Status | Verification result |
| --- | --- | --- |
| `exoo1989` | Verified | Exact title, author, year, journal, and DOI match the Journal of Graph Theory record for Exoo’s 1989 lower-bound paper. |
| `ge2022` | Verified | Exact title, author list, year, and arXiv identifier `2212.12630` match the arXiv record. |
| `aijaam2010` | Verified with caveat | Exact title, author, year, and the QSpace handle were found by web search. This is a weak institutional-repository citation, not a strong comparison-grade primary source. |
| `mckay1992` | Verified | Exact title, authors, year, and Australasian Journal of Combinatorics record were verified. |
| `angeltveit2018` | Verified | Exact title, authors, year, Journal of Graph Theory venue, and DOI `10.1002/jgt.22235` were verified. |
| `lehavi2024` | Verified | Exact title, author, year, and arXiv identifier `2411.04267` were verified. |
| `exoo2023` | Verified | Exact title, author, year, and arXiv identifier `2310.17099` were verified. |
| `pontiveros2013` | Verified | Exact title, authors, year, and arXiv identifier `1302.6279` were verified. |
| `noga2022` | **Incorrect / unverifiable** | Web search surfaced a workshop/event page rather than a paper record, and the stored Semantic Scholar URL does not resolve cleanly. I could not verify this as a real paper citation with matching title/author/year metadata. |
| `gauthier2024` | Verified | Exact title, authors, year, ITP 2024 venue, and DOI `10.4230/LIPIcs.ITP.2024.16` were verified. |
| `gauthierbrown2024arxiv` | Verified | Exact title, authors, year, and arXiv identifier `2404.01761` were verified. |
| `angeltveitmckay2024` | Verified | Exact title, authors, year, and arXiv identifier `2409.15709` were verified. |
| `gauthier2025` | **Incorrect** | The real AITP/ACM item is `Decreasing the upper bound on the Ramsey number R(5,5)` with DOI `10.1145/3727993.3728010`; the bibliography stores a different title and a wrong AITP PDF URL (`paper_7` instead of the actual paper). |
| `narvez2024` | Verified with caveat | The chapter `Formalizing Finite Ramsey Theory in Lean 4` was verified via DOI `10.1007/978-3-031-66997-2_6` and Springer/CICM metadata. The stored URL should be replaced with the official DOI/Springer landing page. |
| `radziszowski2024ds1` | Verified with caveat | The Dynamic Survey entry was verified via the Dynamic Surveys page and DOI `10.37236/21`. The bibliography should include the DOI and exact revision/date used for the current-frontier claim. |
| `barakeelramseyrepo` | Verified as artifact page | The GitHub repository exists and is a valid artifact citation, but it is a repository entry rather than a paper citation. |
| `heule2018schur` | Verified | Exact title, author, year, AAAI 2018 venue, and DOI `10.1609/AAAI.V32I1.12209` were verified. |
| `li2025ramseycert` | Verified | Exact title, authors, year, IJCAI 2025 venue, and DOI `10.24963/ijcai.2025/292` were verified. |
| `lehavirepo` | Verified as artifact page | The GitHub repository exists and is a valid artifact citation, but it is a repository entry rather than a paper citation. |
| `mckayramseydata` | **Incorrect metadata** | The URL resolves to Brendan McKay’s `Ramsey Graphs` data page, but I could not verify the stored title `Maximal Triangle-Free Graphs and Maximal (4,5)-Graphs` as the title of that page. The bibliography row should be corrected to match the actual page. |

## Novelty Assessment

The paper’s only genuinely interesting idea is the proposed cross-family canonical obstruction atlas over failed `42 -> 43` extensions. If that object were actually built, if it recurred across at least three non-isomorphic parent families, if it survived leave-one-parent-out anti-Exoo transfer, and if it remained witness-safe while feeding a credible upper-bound lemma path, that would be materially different from Ge 2022 and Lehavi 2024. But none of that has happened here. The achieved contribution is instead a claim grammar, an evaluation ladder, and a repository-state no-go theorem driven by missing artifacts. That is disciplined governance, not a new Ramsey result. The concept-evolution files reinforce this conclusion: `results/concept_evolve/semantic_bridge.json` contains bridge chains, but the concept tree folders are still planning records, and every audited `concept.json` lacks an `experimental_result`. In blunt terms: what is novel here is not a mathematical object or a surprising result; it is a careful refusal to overclaim. That is useful, but it is not enough for publication-level novelty in this venue.

## Required Deepening And Repairs

- Materialize the actual `H1` evidence packet: `results/h1/frontier_parents.jsonl`, `extension_cases.jsonl`, `failure_witnesses.jsonl`, `obstruction_cores.jsonl`, `transfer_records.jsonl`, `atlas_summary.md`, and `witness_safety_audit.md`.
- Execute the `H1` ladder in order on at least three non-isomorphic parent families and report real coverage, held-out retention, family-balance, and witness-safety numbers.
- Demonstrate a real structural moat over prior work: at least one canonical core family must survive identity-preserving reuse beyond Exoo-line digestion or Lehavi-style OVE bookkeeping.
- Reproduce at least one lower-bound comparator and one solved certificate benchmark under a versioned benchmark manifest before making any method-comparison claim.
- Fix the bibliography before resubmission: remove or replace `noga2022`, correct `gauthier2025`, repair `mckayramseydata`, replace Semantic Scholar mirror URLs with official sources where possible, and add the missing Dynamic Survey DOI/revision metadata.
- Fix the LaTeX errors at `research_paper.tex:45-46` and verify that the full build pipeline exits cleanly.
- Regenerate the figures after fixing the matrix rendering bug and annotation layout problems. Also remove the stale hardcoded `known_papers = 106` value from `figures/generate_figures.py:123`.

## Bottom Line

As an internal checkpoint memo, the manuscript is disciplined and mostly honest. As a submission claiming a meaningful advance on `R(5,5)`, it is not there yet. The core novelty is still hypothetical, and several paper-quality blockers remain unresolved. Under this rubric, the right decision is **DEEPEN**.
