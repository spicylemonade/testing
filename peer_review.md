# Peer Review

## Overall verdict

**REVISE**

The manuscript is close to being a coherent paper, but it is not acceptable in its current form because the bibliography is not reliable enough for publication and the paper slightly overstates one of its post-H1 results. The core empirical story is real: the repo does contain executable H1 controls, an exact checked-class depth-1 locality barrier on the canonical order-668 frontier seed, a first certified retained depth-2 escape to `13/2744/480`, and an honest negative population result. But the paper needs a narrower framing and a fully repaired bibliography before it meets publication standards.

## Scores

| Criterion | Score | Notes |
| --- | --- | --- |
| Completeness | 5 | All required major sections are present, plus appendices and reproduction notes. |
| Technical Rigor | 4 | Methods are explicit, equations are present, and artifacts are reproducible, but the stronger post-H1 mechanism claims are not benchmarked as tightly as the prose suggests. |
| Results Integrity | 3 | Most quantitative claims match the saved artifacts, but the orbit-transfer claim is overstated for `barrier_ladder_01`, and the population “strict wins” wording needs a median/state-level qualifier. |
| Citation Accuracy | 1 | Multiple entries in `sources.bib` are wrong or only partially verifiable. Under the stated zero-tolerance policy, this fails. |
| Compilation | 4 | `pdflatex -> bibtex -> pdflatex -> pdflatex` succeeds and `research_paper.pdf` exists, but the LaTeX log still contains several overfull/underfull box warnings. |
| Writing Quality | 4 | Clear and professional overall, but some related-work and comparative language is stronger than the evidence. |
| Figure Quality | 4 | Figures are customized, labeled, and not default-matplotlib plain; they are serviceable, though somewhat dense and annotation-heavy. |
| Novelty & Creative Contribution | 3 | The defensible novelty is modest and narrow: a seed-specific barrier/counterexample result. This is not a new CA family for Hadamard search and not substantial progress on solving order 668. |

## Key findings

1. The paper is structurally complete and compiles successfully.
2. The repo artifacts do support the narrow barrier/counterexample story:
   - H1 is exact on tiny controls and negative on the canonical frontier.
   - The checked depth-1 actuator class (`334 + 55,611 + 9 = 55,954`) contains no improving single actuator.
   - The first certified retained depth-2 escape is the cone `[3,7]`, reaching `13/2744/480`.
   - Hypergraph and lattice-gas reproduce that state on the canonical frontier.
   - Population does not beat zero-coupling.
3. The manuscript overstates the orbit result. The paper says orbit transfers “the same improvement” across the canonical seed and all five ladder states, but the saved orbit artifact lands at `13/2880/512` on `barrier_ladder_01`, not `13/2744/480`.
4. The novelty case is only modest. The strongest claim is a seed-specific structural result on top of Eliahou’s published `64`-modular frontier object. The paper does not present an exact order-668 witness, a new CA search family, or a robust generalization story.
5. The concept-evolution tree does not itself constitute experimental evidence. The `results/concept_evolve/tree/*/concept.json` files are planning/hypothesis artifacts, not execution records with `experimental_result` fields.

## Results integrity assessment

The paper is mostly faithful to the repo:

- H1 control/frontier numbers in the manuscript match `results/experiments/controls/summary.json` and `results/experiments/order_668_64m/summary.json`.
- The retained-library counts, low-splash cutoff `25.5`, retained size `9`, and depth-1 barrier numbers match the saved JSON artifacts.
- The hypergraph and lattice-gas canonical frontier outcomes match the raw summaries.
- The population medians and diffusion-only phase map match the saved results.

The main integrity issue is representational, not fabricated data:

- The orbit branch does **not** achieve the same improved state on every ladder state. `barrier_ladder_01` is the clear counterexample.
- The population “strict wins” language is only safe if explicitly scoped to state-level medians; at the run level there is at least one coupled win on `barrier_ladder_05`.

## Novelty assessment

The work is **not** a solution to Hadamard order 668, and it is **not** persuasive as a broad new cellular-automaton search paradigm. What is genuinely new here, if framed carefully, is narrower: the paper identifies an exact checked-class locality barrier on Eliahou’s published order-668 frontier seed and then isolates the first retained depth-2 local counterexample that escapes it. That is a modest but real scientific contribution. What is not novel is the use of CA rhetoric for search in general, the use of a published near-solution as the frontier anchor, or the presentation of the hypergraph/lattice-gas/orbit branches as independent CA discoveries. Those branches reuse the same retained nine-action library and largely replay the same six-packet target state. The concept-evolve artifacts also do not demonstrate experimentally grounded creative branching; they are mostly planning scaffolds. In short: modest novelty if reframed as a seed-specific barrier/counterexample paper, not as a new CA family and not as meaningful progress toward an exact Hadamard matrix of order 668.

## Citation verification report

All in-text `\cite{}` keys used in `research_paper.tex` exist in `sources.bib`. There are no broken in-text citation keys.

However, `sources.bib` does **not** meet a zero-tolerance accuracy standard. I verified every entry by web search and classified each entry below.

| Bib key | Status | Verification outcome |
| --- | --- | --- |
| `eliahou2025_64mod668` | Verified | Official Australasian Journal of Combinatorics record/PDF matches title, author, year `2025`, venue, and URL. |
| `tsompanas2017` | Incorrect | The paper exists and the DOI is real, but the bibliography metadata does not match the DOI record. The title/authors are right, but the entry’s booktitle/series/pages are inconsistent with the Springer chapter identified by `10.1007/978-3-319-77510-4_8`. |
| `ghaleb2019` | Incorrect | The paper exists and the DOI is real, but the entry is misclassified as a journal article. It is a conference/proceedings chapter in the AIAI 2019 / Springer proceedings line, not a journal paper with the venue as given. |
| `ghaemi2022` | Verified | Official PLOS ONE record matches title, year `2022`, venue, and DOI `10.1371/journal.pone.0265065`. |
| `leeuwen2000` | Incorrect | `Engineering Societies in the Agents World` is an edited LNCS volume/proceedings record. The BibTeX entry treats it as an article with an incorrect author/venue model. |
| `suksmono2019` | Verified | Official Scientific Reports record matches title, authors, year `2019`, venue, and DOI `10.1038/s41598-019-50473-w`. |
| `suksmono2024` | Incorrect | The title exists as a `2024` arXiv preprint and also as a `2025` Scientific Reports article, but this BibTeX entry mixes the `2024` year with the `2025` journal DOI/venue. |
| `suksmono2018` | Verified | Official Entropy / PubMed record matches title, author, year `2018`, venue, and DOI `10.3390/e20020141`. |
| `suksmono2022` | Verified | Official Scientific Reports record matches title, authors, year `2022`, venue, and DOI `10.1038/s41598-021-03586-0`. |
| `bright2018` | Verified | AAAI 2018 paper exists with the stated title/authors/year and DOI `10.1609/aaai.v32i1.12203`. |
| `bright2019` | Verified | Annals of Mathematics and Artificial Intelligence paper matches title, authors, year `2019`, venue, and DOI `10.1007/s10472-019-09681-3`. |
| `bright2019_williamson` | Incorrect | The DOI is real, but the entry’s year/venue are wrong. The work is the short `2018` ACM Communications in Computer Algebra / ISSAC-associated publication, not a `2019` article in `ACCA`. |
| `cati2024` | Verified | The arXiv preprint exists with title, authors, year `2024`, and DOI `10.48550/arXiv.2411.18897`. Venue formatting could be cleaner (`arXiv` / `CoRR`), but the reference is real. |
| `artacho2013` | Verified | The paper is a `2014` ANZIAM Journal article with DOI `10.1017/S1446181114000145`; the BibTeX key name is stale, but the stored year/venue/title are correct. |
| `eliahou2005` | Verified | Discrete Mathematics paper matches title, authors, year `2005`, venue, and DOI `10.1016/j.disc.2005.02.021`. |
| `eliahou2001` | Incorrect | The paper itself is real and the title/authors/year/venue are supported by web references, but I could not independently verify the stored DOI via web search. Under the task’s zero-tolerance rule, this entry must be treated as failing verification. |
| `sudhakaran2022` | Verified | The arXiv preprint exists with the stated title, authors, year `2022`, and arXiv DOI `10.48550/arXiv.2205.06806`. |
| `mariot2019_mols` | Incorrect | The paper exists and the DOI is real, but the stored author list is wrong. The published paper is not authored by `Alessio Marcuzzi`; the verified author list includes Alberto Leporati. |
| `gadouleau2020` | Verified | The IACR ePrint paper exists with the stated title/authors/year. The paper is real, although the bibliography URL would be better pointed to the primary ePrint page than to Semantic Scholar. |

### Citation-accuracy bottom line

This bibliography fails the required standard. Several entries are real papers but have materially incorrect metadata, and at least one cited entry (`eliahou2001`) could not have its stored DOI independently confirmed via web search. Because the task explicitly requires zero tolerance for citation errors, the paper cannot receive a passing Citation Accuracy score.

## Actionable revision requests

1. Repair `sources.bib` completely before resubmission. Do not leave mixed preprint/journal metadata, wrong venues, wrong author lists, or unverifiable DOI fields.
2. Rewrite the contribution framing around the **narrow** result the repo actually supports:
   - checked-class depth-1 barrier on the canonical seed,
   - first retained depth-2 counterexample to `13/2744/480`,
   - lattice-gas and orbit as repackagings/transfer tests of that same escape,
   - population as a negative robustness result.
3. Correct the orbit language everywhere it overclaims. It does not achieve the same improved state on all six frontier states.
4. Add a median/state-level qualifier to the population “strict wins” wording.
5. Add point-of-use citations for the Eliahou seed provenance wherever the paper reuses those facts, not only in the introduction.
6. Tighten the related-work and comparison prose so each strong claim is locally supported rather than carried by broad synthesis sentences.
7. If the authors want stronger method claims, add at least one depth-matched non-CA comparator on the retained graph and a clean retained-graph oracle/exhaustive baseline.
8. Clean up the remaining LaTeX layout warnings, especially the overfull boxes in the compiled log.

## Final recommendation

The direction is sound enough to revise. The paper should come back as a narrower, more disciplined artifact paper: barrier, counterexample, and negative robustness result on a published frontier seed. It should **not** come back with the current bibliography or with the current stronger rhetoric about transfer and independent CA-method novelty.
