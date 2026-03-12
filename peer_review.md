# Peer Review

## Major Findings

1. **Citation accuracy fails the stated review bar.** The manuscript cites only keys that exist in [`sources.bib`](/home/archivara/work/repo/sources.bib), but the bibliography itself is not publication-safe. I found multiple incorrect or inadequate entries: the Kimberling webpage title is wrong in [`sources.bib`](/home/archivara/work/repo/sources.bib#L19), the Ford rough-divisor entry has mismatched publication metadata in [`sources.bib`](/home/archivara/work/repo/sources.bib#L61), the Pach entry has inconsistent year metadata relative to the cited volume/issue/pages in [`sources.bib`](/home/archivara/work/repo/sources.bib#L93), and the Koukoulopoulos and Brent entries are metadata placeholders rather than primary bibliographic records in [`sources.bib`](/home/archivara/work/repo/sources.bib#L72) and [`sources.bib`](/home/archivara/work/repo/sources.bib#L143). Under the zero-tolerance citation policy in the task, this alone blocks acceptance.

2. **The novelty case is too narrow for a top-tier venue.** The strongest defensible contribution is structural cleanup of a public recurrence plus a reproducible finite-horizon negative-result package. The repo's own novelty audit reaches that conclusion in [`results/verification/novelty_report.md`](/home/archivara/work/repo/results/verification/novelty_report.md#L24), and the benchmark audit explicitly says the package does not yet separate the work from generic local divisor/product coverage in [`results/verification/benchmark_report.md`](/home/archivara/work/repo/results/verification/benchmark_report.md#L122). The concept-evolve layer also records H1 as only "pivoted" and H2 as "retired" rather than successful in [`results/concept_evolve/tree/012_frontier_witness_certificate/concept.json`](/home/archivara/work/repo/results/concept_evolve/tree/012_frontier_witness_certificate/concept.json#L13) and [`results/concept_evolve/tree/013_prime_support_fixed_point/concept.json`](/home/archivara/work/repo/results/concept_evolve/tree/013_prime_support_fixed_point/concept.json#L13).

3. **Results integrity is mostly solid, but not clean enough.** Most headline quantitative claims do match the stored artifacts, including the record-gap table and gap-30 hypergraph counts. But the manuscript reports fresh replay runtime and RSS numbers with no backing artifact in [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex#L398) and Appendix Table 2 in [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex#L623). The paper also overstates the balanced-share trend as "rises steadily" in [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex#L493); the stored series rises overall but dips between gaps 19 and 20.

4. **The benchmark story remains weaker than the prose implies.** The internal benchmark report is already explicit that there is no independent implementation baseline, no surrogate or matched non-record control, and no genuine robustness ablation after the identity/symmetry proofs in [`results/verification/benchmark_report.md`](/home/archivara/work/repo/results/verification/benchmark_report.md#L36) and [`results/verification/benchmark_report.md`](/home/archivara/work/repo/results/verification/benchmark_report.md#L53). That is adequate for a finite-horizon verification note, not for a strong mechanism paper.

5. **Figure quality is generally good, but two figures need revision.** The figure pipeline is reproducible and not default-matplotlib output. Still, the offset panel annotates the full-run maximum `24` while plotting only a sampled series in [`figures/src/figure2_interleaving.tex`](/home/archivara/work/repo/figures/src/figure2_interleaving.tex#L39), and the variant-identity figure lacks a legend despite plotting multiple clouds in [`figures/src/figure6_variant_identities.tex`](/home/archivara/work/repo/figures/src/figure6_variant_identities.tex#L28). Those are fixable presentation issues, not fatal aesthetic failures.

## Scores

| Criterion | Score | Notes |
|---|---:|---|
| Completeness | 5 | All required sections are present, including abstract, related work, method, setup, results, discussion, conclusion, and references. |
| Technical Rigor | 3 | The structural proofs are careful and reproducibility is reasonably documented, but the benchmark/control package is still below publication-grade rigor. |
| Results Integrity | 3 | Core tables and figures mostly match the stored artifacts, but unsupported fresh replay performance numbers and a mildly overstated trend remain. |
| Citation Accuracy | 1 | Several bibliography entries are incorrect, inconsistent, or metadata-only placeholders; zero-tolerance policy not met. |
| Compilation | 4 | [`research_paper.pdf`](/home/archivara/work/repo/research_paper.pdf) exists and `pdflatex` succeeds, but the build still emits warnings. |
| Writing Quality | 4 | Clear, professional, and mostly disciplined about claim scope. |
| Figure Quality | 3 | Custom, publication-oriented graphics overall, but a few panels are misleading or under-labeled. |
| Novelty & Creative Contribution | 2 | The contribution is modest: structural cleanup plus verified negative evidence, not a new mechanism or surprising theorem. |

## Citation Verification Report

- `oeisA129258`: **Verified via web search.** OEIS entry exists and the title matches the bibliography entry.
- `oeisA129259`: **Verified via web search.** OEIS entry exists and the title matches the bibliography entry.
- `kimberling100conjectures`: **Incorrect metadata.** The URL is real, but the webpage title does not match "100 Conjectures and/or Problems"; the entry should be corrected to the actual page title or replaced by a more precise bibliographic description.
- `ford2011multiplicationtable`: **Verified via web search.** Title, author, journal, volume, issue, pages, year, and DOI all match.
- `ford2008divisorinterval`: **Verified via web search.** Title, author, journal, year, volume, pages, and DOI match.
- `ford2006divisor2y`: **Verified via web search.** The arXiv preprint exists with the stated title, author, and year.
- `ford2020roughdivisorinterval`: **Incorrect metadata.** The DOI resolves to a real paper, but the publication metadata in the BibTeX entry do not match the journal record for year/issue/pages.
- `koukoulopoulos2010restrictedtables`: **Inadequate / incorrect for publication use.** A real 2010 dissertation with this title exists, but the entry is only a Semantic Scholar placeholder rather than a primary bibliographic record.
- `mehdizadeh2021smoothmultiplicationtable`: **Verified via web search.** Title, author, journal, volume, pages, year, and DOI match.
- `pach2017multiplicativebases`: **Incorrect / inconsistent metadata.** The cited volume/issue/pages correspond to the Combinatorica publication, but the year in the entry is inconsistent with that journal record.
- `pus1992multiplicativebases`: **Partially verified, treated as incorrect under the stated policy.** The paper exists and the core bibliographic data can be found, but I could not independently verify the DOI/URL from web search.
- `dressler1970newmultiplicativebases`: **Verified via web search.** Title, author, journal, year, and DOI match.
- `nathanson1987multiplicativerepresentations`: **Verified via web search.** Title, author, journal, year, pages, and DOI match.
- `brent2019algorithmsmultiplicationtable`: **Inadequate / incorrect for publication use.** The work exists as a 2019 preprint and later publication, but the entry is a Semantic Scholar placeholder with incomplete venue-level metadata.
- `meisner2018functionfieldmultiplicationtable`: **Verified via web search.** The arXiv preprint exists with the stated title, author, and year.

Additional bibliography checks:

- All 10 in-text `\cite` keys used in [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex) exist in [`sources.bib`](/home/archivara/work/repo/sources.bib).
- 5 bibliography entries are unused: `ford2020roughdivisorinterval`, `koukoulopoulos2010restrictedtables`, `mehdizadeh2021smoothmultiplicationtable`, `brent2019algorithmsmultiplicationtable`, and `meisner2018functionfieldmultiplicationtable`.
- I did not find an obviously fabricated paper, but several entries are bibliographically incorrect or too weak to survive a strict audit.

## Novelty Assessment

The paper does contribute something real, but it is not yet top-tier novel work. The novel part is narrow: it isolates and proves several exact consequences of Kimberling's public recurrence, cleans up the status of the update-order "variants," and assembles a reproducible million-step negative-result package showing that the simplest witness-certificate and prime-support stories fail on the stored corpus. That is useful scholarship. What it does **not** yet do is produce a new mechanism for record-gap growth, a theorem-level separation from Ford-style local divisor/product coverage, or a creative cross-domain CE-driven breakthrough. The concept-evolve artifacts themselves show mostly steering, pruning, and retrospective consolidation rather than a successful experimental bridge: old bridge cards still sit in backlog form in [`results/concept_evolve/tree/001_frontier_interval_certificate/README.md`](/home/archivara/work/repo/results/concept_evolve/tree/001_frontier_interval_certificate/README.md#L12) and [`results/concept_evolve/tree/002_divisor_window_density_control/README.md`](/home/archivara/work/repo/results/concept_evolve/tree/002_divisor_window_density_control/README.md#L12), while the surviving CE state explicitly pivots toward future surrogate controls instead of reporting a completed novelty-producing mechanism in [`results/concept_evolve/concept_delta.md`](/home/archivara/work/repo/results/concept_evolve/concept_delta.md#L5). For a Nature/NeurIPS standard, that is a score of **2/5**, not because the work is careless, but because the differentiated mathematical insight is still modest.

## Overall Verdict

**DEEPEN**

This is not an acceptance-ready top-tier research paper. The novelty score is below threshold, and there are also fixable paper-quality issues, especially in the bibliography. Under the task policy, a novelty score of 1-2 with concurrent quality issues requires `DEEPEN` rather than `REVISE`.

## Deepening Instructions

1. Repair the bibliography completely. Replace all metadata-only placeholders with primary records, correct the Kimberling title, correct the Ford/Pach metadata mismatches, and either verify or remove any DOI/URL that cannot be independently checked.
2. Remove or artifact-back the fresh replay performance claims in [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex#L398) and [`research_paper.tex`](/home/archivara/work/repo/research_paper.tex#L623). If a fresh replay is part of the paper, save it as a concrete artifact first.
3. Narrow the manuscript's claim hierarchy unless new research is added. As written, the safe contribution is "structural clarification + reproducible finite-horizon negative evidence," not "new mechanism."
4. Add the missing controls identified by the benchmark and falsifier layers: one independently written checker, one same-snapshot tie-rule control, one real admissibility perturbation, and matched non-record / surrogate product-set baselines.
5. Push for an actually differentiating contribution. In this domain, that means at least one of: a new theorem controlling frontier coverage, a genuinely T-specific invariant that generic local product coverage does not mimic, a counterintuitive structural law extracted from full witness hypergraphs, or a creative algorithmic/combinatorial compression result that survives surrogate baselines.
6. If the concept-evolve pipeline is meant to be part of the novelty story, execute the bridge experimentally rather than citing it as latent potential. Right now the CE layer mainly documents abandoned branches and future rescue paths.
