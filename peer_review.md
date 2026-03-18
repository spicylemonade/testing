# Peer Review

## Findings

1. **The paper’s core novelty claim does not survive close review because the literal `cellar automata` idea was not actually executed.** The manuscript itself limits the validated contribution to `H1` and `H2` and treats literal cellar automata as reserve work, while the concept-evolve artifacts show the pushdown/prefix-debt branch remained unvalidated and its concept files still lack `experimental_result` fields. The strongest creative idea is therefore still a hypothesis, not a result. See [research_paper.tex:257](/home/archivara/work/repo/research_paper.tex#L257), [research_paper.tex:540](/home/archivara/work/repo/research_paper.tex#L540), [concept_delta.md:22](/home/archivara/work/repo/results/concept_evolve/concept_delta.md#L22), [novelty_report.md:174](/home/archivara/work/repo/results/verification/novelty_report.md#L174), [002_autocorrelation_debt_pushdown/concept.json:15](/home/archivara/work/repo/results/concept_evolve/tree/002_autocorrelation_debt_pushdown/concept.json#L15), and [011_convolution_slice_ca/concept.json:15](/home/archivara/work/repo/results/concept_evolve/tree/011_convolution_slice_ca/concept.json#L15).

2. **Citation accuracy fails the zero-tolerance bar.** The in-text keys all resolve mechanically, but `sources.bib` contains multiple incorrect or inconsistent entries: wrong page range for Eliahou, mixed preprint/journal metadata for Manzoni and Bagnoli, wrong year for Suksmono 2016 and Tsompanas, wrong author metadata for the single-elevator paper, a malformed proceedings entry for `leeuwen2000agentsworld`, and an unused entry that I could not verify by web search. Several prose claims in the manuscript also cite literature where the real support is internal repository provenance or search logs. See [sources.bib:9](/home/archivara/work/repo/sources.bib#L9), [sources.bib:41](/home/archivara/work/repo/sources.bib#L41), [sources.bib:66](/home/archivara/work/repo/sources.bib#L66), [sources.bib:93](/home/archivara/work/repo/sources.bib#L93), [sources.bib:159](/home/archivara/work/repo/sources.bib#L159), [sources.bib:176](/home/archivara/work/repo/sources.bib#L176), [sources.bib:194](/home/archivara/work/repo/sources.bib#L194), [sources.bib:212](/home/archivara/work/repo/sources.bib#L212), [research_paper.tex:114](/home/archivara/work/repo/research_paper.tex#L114), and [research_paper.tex:195](/home/archivara/work/repo/research_paper.tex#L195).

3. **The headline results are mostly supported by the checked artifacts, but the figure/summary layer is not fully reproducible.** The main H1/H2 means, hit rates, and paired win counts match the JSON packets, so I do not see evidence of fabricated results. However, the current manuscript’s H1 target bootstrap confidence intervals do not exactly match the checked `paper_metrics.json`, and the generator seeds its bootstrap with Python’s salted `hash(...)`, making those intervals process-dependent. See [research_paper.tex:436](/home/archivara/work/repo/research_paper.tex#L436), [research_paper.tex:479](/home/archivara/work/repo/research_paper.tex#L479), [paper_metrics.json](/home/archivara/work/repo/results/analysis/paper_metrics.json), and [generate_figures.py:182](/home/archivara/work/repo/figures/generate_figures.py#L182).

4. **The experimental packet supports only a narrow branch-specific no-go, not a stronger benchmark or method conclusion.** The manuscript is honest about this in places, but the control/real-task limits remain substantial: the solved `4x79` control still has exact-hit rate `0/16` for both serious methods, and the decisive real `H2` claim rests on one degraded order-668 start. That is enough to reject the implemented rules; it is not enough to sustain a broader creative or benchmark claim. See [research_paper.tex:437](/home/archivara/work/repo/research_paper.tex#L437), [research_paper.tex:480](/home/archivara/work/repo/research_paper.tex#L480), [research_paper.tex:530](/home/archivara/work/repo/research_paper.tex#L530), and [benchmark_report.md:1](/home/archivara/work/repo/results/verification/benchmark_report.md#L1).

## Scores

| Criterion | Score | Notes |
| --- | --- | --- |
| Completeness | 5 | All required sections are present, including Abstract, Introduction, Related Work, Method, Experimental Setup, Results, Discussion, Conclusion, and References. |
| Technical Rigor | 4 | Methods are formalized carefully and backed by code-linked artifacts, but the strongest experimental claims are intentionally narrow and the positive-control story remains weak. |
| Results Integrity | 4 | I did not find fabricated headline numbers; the main tables and claims match the checked experiment JSON. The summary CI layer is not fully reproducible because of salted-hash seeding. |
| Citation Accuracy | 1 | Multiple bibliography entries are incorrect or inconsistent, and one unused entry could not be verified by web search. This fails the paper’s citation layer outright. |
| Compilation | 4 | `research_paper.pdf` exists and a fresh `pdflatex -> bibtex -> pdflatex -> pdflatex` rebuild succeeded. The PDF compiles, though the build still emits some typographic warnings. |
| Writing Quality | 4 | The prose is clear and professional overall, but several claims over-attribute literature support where the evidence is actually internal repository provenance. |
| Figure Quality | 3 | The figures are not default Matplotlib output and use a custom palette/layout, but they still read as draft-quality rather than final publication figures. |
| Novelty & Creative Contribution | 2 | The executed contribution is a careful negative result on two CA-vs-greedy branches. The materially different “literal cellar” idea was not executed, so the paper’s most creative concept remains unvalidated. |

## Citation Verification Report

| BibTeX key | Status | Verification call |
| --- | --- | --- |
| `constantine2025cyclic` | Verified via web search | arXiv record for *Convolution numbers: the cyclic case* matches title, authors, year, and URL. |
| `eliahou2025mod64` | **Incorrect metadata** | Paper is real, but the checked AJC PDF is 6 pages, so the entry’s `422--429` page range is wrong. |
| `bright2018satcas` | Verified via web search | DOI/title/authors/year/venue match AAAI 2018. |
| `fitzpatrick2023williamson` | Verified via web search | DOI/title/authors/year/venue match *Discrete Mathematics* 346(12):113615. |
| `manzoni2025survey` | **Incorrect metadata** | The paper is real, but the entry mixes an arXiv DOI with a journal venue/URL and should be normalized to one version. |
| `mariot2016ols` | Verified via web search | The 2016 preprint exists with the stated title/authors; the stored URL is noncanonical but points to the paper record. |
| `gadouleau2020bent` | Verified via web search | IACR ePrint 2020/1272 matches the entry. |
| `mariot2021semibent` | **Incorrect metadata** | DOI resolves to the *Natural Computing* journal paper published in 2022, not a 2021 journal article. |
| `bagnoli2025controllability` | **Incorrect metadata** | The paper is real, but the entry mixes preprint-era yearing with a journal DOI/version; the journal record is later and should be normalized. |
| `herold2014decoder` | Verified via web search | Title/authors/year/venue/DOI match the 2015 *npj Quantum Information* paper; the BibTeX key name is stale but the fields are correct. |
| `suksmono2016sa` | **Incorrect metadata** | DOI resolves to a 2017 *Journal of Physics: Conference Series* paper, not a 2016 journal publication. |
| `suksmono2018sqa` | Verified via web search | DOI/title/authors/year/venue match *Entropy* 20(2):141. |
| `suksmono2019` | Verified via web search | DOI/title/authors/year/venue match *Scientific Reports* 2019. |
| `suksmono2022quantum` | Verified via web search | DOI/title/authors/year/venue match *Scientific Reports* 2022. |
| `suksmono2024qaoa` | Verified via web search | DOI/title/author/year/venue match the 2025 *Scientific Reports* article; the key name is stale but the fields are acceptable. |
| `eliahoukervaire2005survey` | Verified via web search | DOI/title/authors/year/venue match *Discrete Mathematics* 302(1-3):85-106. |
| `horadam2007applications` | **Incorrect metadata** | The book is real, but the checked edition metadata does not match the ISBN in the entry; the edition should be normalized. |
| `djokovic2018goethalsseidel` | **Incorrect metadata** | Paper is real, but the journal should be *Mathematics in Computer Science*, and the DOI `10.1007/s11786-018-0381-1` is missing. |
| `tsompanas2017shortestpath` | **Incorrect metadata** | DOI/title are real, but the Springer chapter metadata is 2018 rather than 2017. |
| `ghaleb2019singleelevator` | **Incorrect metadata** | DOI/title are real, but the author metadata is wrong: the paper is by `O. / Omar Ghaleb`, not `Osamah Ghaleb`. |
| `ghaemi2022ebola` | Verified via web search | DOI/title/authors/year/venue match the PLOS ONE article. |
| `leeuwen2000agentsworld` | **Incorrect metadata** | DOI/title resolve to the ESAW proceedings volume/workshop record, not the paper-type/author record stored here. |
| `ghaleb2019multielevator` | Verified via web search | DOI/title/year/venue are consistent with the Springer conference chapter. |
| `khatoon2019tutoring` | **Unverified via web search** | I could not verify this exact entry with web search, and it is unused in the manuscript. It should be removed. |

## Novelty Assessment

The paper does contribute a legitimate negative-result packet, but it does not contribute a genuinely novel method. The executed work is two tightly matched CA-vs-greedy comparisons on the exact `167/80` obstruction and the published mod-64 order-668 seed. That is careful and useful, but it is not especially surprising, and the most creative direction suggested by the prompt, the literal `cellar automata` / pushdown / deferred-debt representation, was never taken past concept-evolution ideation into an implemented and benchmarked branch. The concept tree confirms that the reserve branches remain at the level of `implementation_hypothesis`, with no `experimental_result` fields. The manuscript is therefore strongest as a modest, benchmarked no-go study and weakest wherever it gestures toward a new automaton family or a broader creative advance.

## Verdict

**DEEPEN**

The paper is technically competent enough to revise, but the main blocker is deeper than paper polish. The executed contribution is a narrow negative result on two conservative local-update variants, while the only materially different idea stayed unexecuted. That is a novelty problem first, plus a citation-cleanup problem second.

To elevate this project meaningfully, the next cycle should:

1. Implement and benchmark a **materially different representation**, not just a different move-selection rule on the same neighborhood. The literal prefix-debt / pushdown-style cellar automaton is the obvious candidate because it is the one branch that actually changes the state object.
2. Preserve **same-space positive controls** in that new representation and beat a matched non-automaton comparator on at least one discriminative exact or near-exact task.
3. Show a **new reachable regime or new pruning power** that ordinary same-space direct search does not achieve, rather than another tie-or-loss against `direct_greedy`.
4. Strengthen the evidence packet around order 668 itself by expanding beyond the single real degraded `H2` start.
5. Repair the citation layer completely and make the figure-summary generation deterministic before resubmission.

If the authors do not want to deepen the research contribution, the paper should be reframed even more narrowly as a negative benchmark note and stripped of any residual suggestion that a new `cellar automata` method has been demonstrated.
