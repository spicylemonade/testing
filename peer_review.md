# Peer Review

## Overall Verdict

**DEEPEN**

The manuscript is technically careful, complete, and largely honest about the narrow claim it can support. The main quantitative statements in the paper match the checked artifacts, and the literal cellar branch was in fact executed rather than left as a slogan. However, the package still falls short of publication standard for two separate reasons. First, citation accuracy fails the stated zero-tolerance bar: four `sources.bib` entries are incorrect on metadata that should have been verified before submission. Second, the surviving contribution is only a modest encoding-specific no-go. The paper does not deliver a new Hadamard construction, a new positive solver, or a demonstrated broadly creative CE-driven method; it retires one exact literal-cellar encoding. Under the stricter novelty rule for this review, that is a `DEEPEN`, not merely a `REVISE`.

## Scores

| Criterion | Score | Rationale |
| --- | --- | --- |
| Completeness | 5 | All required sections are present: Abstract, Introduction, Related Work, Method, Experiments, Results, Discussion, Conclusion, and References. |
| Technical Rigor | 4 | The paper gives a real formalization, equations, proofs, and a matched-comparator design. The main deduction is defensible, but some reproducibility details still live in analysis-layer recomputations rather than canonical experiment outputs. |
| Results Integrity | 4 | I did not find fabricated headline numbers. The load-bearing H1, H2, and cellar counts match the checked JSON artifacts. The main weakness is auditability: H1 bootstrap CIs are not deterministic across reruns, and some cellar control metrics are recomputed during figure generation. |
| Citation Accuracy | 1 | Four bibliography entries are incorrect. This fails the paper's citation layer under the stated zero-tolerance rule. |
| Compilation | 5 | `research_paper.pdf` exists, and a sequential `pdflatex -> bibtex -> pdflatex -> pdflatex` rebuild completed cleanly. The final log contains no warnings, overfull boxes, or undefined references. |
| Writing Quality | 4 | The prose is professional and mostly clear. The main weakness is literature framing: a few sentences still overstate comparator ranking or venue-level judgment beyond what the bibliography actually supports. |
| Figure Quality | 3 | The figures are custom-styled and above default Matplotlib quality, so this is not a forced revise on styling grounds. Still, some layouts are crowded, especially the cellar mechanism/results views, and they do not yet read as polished publication figures. |
| Novelty & Creative Contribution | 2 | The surviving contribution is a narrow retirement of one executed encoding. That is real, but it is not a strong creative advance for a top-tier venue. The CE tree also remains a planning artifact rather than an experimentally annotated concept ledger. |

## Major Findings

1. **Citation accuracy is not acceptable.** `sources.bib` contains four incorrect entries: `suksmono2019`, `suksmono2022quantum`, `suksmono2024qaoa`, and `eliahoukervaire2005survey`. In addition, the opening anchor sentence in the Introduction discusses both the cyclic and modular anchors but cites only `eliahou2025mod64`; that framing should cite `constantine2025cyclic` as well.

2. **The main numerical claims are supported by the checked artifacts.** I did not find evidence of fabricated results. The precursor packet numbers in the manuscript match `results/analysis/paper_metrics.json`, and the cellar control/stress-packet counts match `results/analysis/cellar_paper_metrics.json` and `results/experiments/cellar_phase6.json`. In particular, the headline H1 control `11/16` direct-greedy wins, H1 target `24/24` direct-greedy wins with means `147.92` vs `188.50`, H2 real-seed tie at modulus `16` / `l1_defect 2944`, and the cellar control frontiers `11/13/15` all check out.

3. **The audit trail is weaker than the prose suggests.** The H1 bootstrap confidence intervals are not reproducible as written because `figures/generate_figures.py` seeds bootstrap resampling from Python's salted `hash()`, so the exact CI endpoints can change across reruns. For the cellar packet, tail-10 and tail-14 control-family rows are regenerated during figure production rather than stored in the cited phase-6 experiment JSON, `results/analysis/cellar_prefix_complexity.md` still uses stale panel names, and both figure scripts can write `fig_cellar_results.*`, which is an avoidable provenance hazard.

4. **Novelty is real but too narrow.** The executed contribution is an encoding-specific negative result: one literal cellar / pushdown-style tail-panel encoding is formalized, shown to collapse to the matched boundary-debt state, and retired empirically on solved controls and anchor-derived panels. That is worthwhile. What it is not is a new solver, a general CA-for-Hadamard-search paradigm, a broad statement about pushdown memory, or a substantial positive CE-derived method. The prior-art gap file itself narrows the claim to this retirement/no-go, and the novelty report explicitly rejects positive solver novelty and broad CA novelty.

5. **The CE evidence is not strong enough to rescue the novelty score.** `results/concept_evolve/concept_delta.md` shows that the literal cellar idea was genuinely reframed and implemented, so I do not think the branch was invented post hoc. But the concept tree files still expose planning fields such as `implementation_hypothesis`, `experiment_seed`, and `folder_plan` without `experimental_result`. Under the explicit review rule for this task, that means the pipeline did not demonstrate a strong, experimentally realized CE loop, and the novelty score must stay in the `1-2` range.

6. **The literature packet is broader than it is selective.** `results/literature/prior_art_gap.md` does a reasonable job narrowing the surviving claim, but `results/literature/prior_art_watchlist.md` still contains obviously irrelevant automata applications. That weak curation leaks into the manuscript as overconfident comparator language such as "closest structured-search comparators" and "not a publishable advance." Those judgments need either stronger evidence or softer wording.

## Citation Verification Report

All in-text `\cite` keys resolve to entries in `sources.bib`; there are no dangling citation commands. The bibliography itself contains `17` cited entries. Every entry below was checked via web search.

| BibTeX key | Status | Verification result |
| --- | --- | --- |
| `constantine2025cyclic` | Verified | Verified via web search: the arXiv preprint exists, and the title, authors, year, and URL match. |
| `eliahou2025mod64` | Verified | Verified via web search: the Australasian Journal of Combinatorics paper exists, and the title, author, year, venue, pages, and URL match. |
| `bright2018satcas` | Verified | Verified via web search: the AAAI 2018 paper exists, and the title, authors, year, venue, and DOI match. |
| `fitzpatrick2023williamson` | Verified | Verified via web search: the Discrete Mathematics article exists, and the title, authors, year, venue, and DOI match. |
| `manzoni2025survey` | Verified | Verified via web search as the 2025 arXiv preprint. The entry is real, though a later published version now exists and the bibliography should be updated deliberately if the authors want the journal version instead. |
| `mariot2016ols` | Verified | Verified via web search: the journal article exists, and the title, authors, year, venue, and DOI match. |
| `gadouleau2020bent` | Verified | Verified via web search: the IACR ePrint paper exists, and the title, authors, year, and URL match. |
| `mariot2021semibent` | Verified | Verified via web search: the Natural Computing paper exists, and the title, authors, year, and DOI match. |
| `suksmono2016sa` | Verified | Verified via web search as the arXiv preprint. The entry is real, though a later published version exists. |
| `suksmono2018sqa` | Verified | Verified via web search: the Entropy paper exists, and the title, author, year, venue, and DOI match. |
| `suksmono2019` | **Incorrect metadata** | Web search confirms the paper is real, but the Scientific Reports article number is `14380`, not `17387` as listed in `sources.bib`. |
| `suksmono2022quantum` | **Incorrect metadata** | Web search confirms the paper is real, but the Scientific Reports article number is `197`, not `749` as listed in `sources.bib`. |
| `suksmono2024qaoa` | **Incorrect metadata** | Web search confirms the paper is real, but the Scientific Reports article number is `33254`, not `18778` as listed in `sources.bib`. |
| `eliahoukervaire2005survey` | **Incorrect metadata** | Web search confirms the paper is real, but the DOI/URL in `sources.bib` is wrong. The verified paper resolves under DOI `10.1016/j.disc.2005.02.021`. |
| `horadam2007applications` | Verified | Verified via web search: the Princeton University Press book exists, and the title, author, year, and publisher match. |
| `djokovic2018goethalsseidel` | Verified | Verified via web search: the Mathematics in Computer Science paper exists, and the title, authors, year, venue, pages, and DOI match. |
| `alur2004vpl` | Verified | Verified via web search: the STOC 2004 paper exists, and the title, authors, year, pages, and DOI match. |

## Novelty Assessment

The paper's strongest genuinely new element is narrow: it formalizes one exact literal-cellar tail-panel encoding tied to the current order-668 anchors, proves that the matched boundary-debt state already determines exact completion on that encoding, and then shows empirically that the stack carries no surviving advantage on the solved controls or recorded anchor-derived panels. That is a real contribution. It is not, however, a new Hadamard construction, a new exact solver, a new positive CA method, or a broad automata-theoretic breakthrough. The precursor H1/H2 branches are mostly careful same-state move-selection comparisons and do not survive as novel algorithms. The concept-evolve packet also does not show a deeply executed CE-to-experiment loop: the concept tree remains largely planning boilerplate without `experimental_result` fields. In short, what is novel is the retirement of one specific encoding; what is not novel is the broader rhetoric around CA, automata, or Hadamard search. For a top-tier venue, that novelty is too modest, so I score it `2/5`.

## What Must Be Fixed In The Deepening Cycle

1. **Repair the bibliography completely.**
   Correct the four incorrect entries listed above. Also repair the manuscript's citation framing: cite both order-668 anchors in the opening sentence and soften unsupported ranking/judgment language in Related Work.

2. **Make the artifact trail deterministic and canonical.**
   Replace salted `hash()`-based bootstrap seeding with fixed explicit seeds. Store the cellar control-family packet in a canonical experiment artifact rather than partly regenerating it during figure production. Unify panel names across analysis notes, experiment JSON, and figures. Stop both figure scripts from writing the same `fig_cellar_results.*` output names.

3. **Improve the figures to publication standard.**
   Keep the current custom styling, but re-layout the crowded panels, especially `fig_cellar_mechanism` and `fig_cellar_results`. The current figure set is acceptable as draft research communication, not yet as final publication artwork.

4. **Earn novelty with a materially stronger research result.**
   To move from `DEEPEN` toward `ACCEPT`, the project needs more than cleaner prose around the current no-go. In this domain, "novel" would mean at least one of the following:
   - a genuinely new state representation or symbolic mechanism that yields a strict exact-frontier separation on nondegenerate panels;
   - a new pruning/proof-reuse/user-propagator idea that beats a matched non-automaton baseline;
   - an alternate tokenization or residual summary where stack memory demonstrably changes what exact completions are reachable or certifiable;
   - a broader theorem that says something surprising beyond the one hard-coded boundary-debt encoding;
   - a real transfer result from the modular seed into the cyclic obstruction that improves exact or near-exact search over a preregistered panel of starts.

5. **Do not oversell the current contribution while deepening.**
   If the authors choose not to pursue a more ambitious result, the honest endpoint is a narrow negative-result note on one retired encoding. That could still be useful, but it is not enough for an `ACCEPT` under the current novelty bar.

## Bottom Line

This manuscript is not failing because the experiments are fabricated or because the LaTeX is broken. The core problem is that the work currently offers only a modest encoding-specific no-go, and even that narrow paper is undermined by avoidable bibliography mistakes and a few provenance defects. Fix the citation layer, make the analysis pipeline deterministic, and then deepen the research with a genuinely more surprising algorithmic or theoretical contribution.
