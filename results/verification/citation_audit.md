# Citation Audit

Date: 2026-03-13
Owner role: `citation_auditor`
Rubric item: `item_018`
Active hypothesis: `H1`
Active hypothesis label: `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

Reviewed artifacts:
- `sources.bib`
- `results/literature/literature_snapshot.json`
- `results/plans/phase3_route_sheet.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/verification/benchmark_report.md`
- `results/swarm/phase3_stress_test.md`

## Audit Verdict

The citation spine is adequate for planning and route triage, but not yet strong enough to treat any `H1` artifact as publishable or even internally solid against the bound-moving threshold above.
The lower-bound line, upper-bound line, and proof-certification context are all present, but the most load-bearing `H1` dependency still relies on weak bibliography metadata and too many mirror URLs.

## Coverage Strengths

- The lower-bound frontier used by the route sheet is grounded by Exoo 1989 and Ge et al. 2022, which is enough to justify the current `R(5,5) >= 43` baseline and the choice to mine Exoo-line parent families.
- The upper-bound frontier and comparison set are covered by McKay-Radziszowski 1992, Angeltveit-McKay 2018, Angeltveit-McKay 2024, Radziszowski's dynamic survey, and Gauthier 2025, so the Phase 4 evaluation sheet has the right named baselines for `improves bound` versus `improves certificate path`.
- The certificate/proof-engineering side is covered well enough for planning by Gauthier-Brown 2024, Barakeel-Gauthier-Commelin 2025, the Barakeel and Lehavi repositories, and McKay's artifact page.
- The benchmark report and stress test correctly treat the `H1` numeric thresholds as falsifiers and governance rules, not as literature-backed achievements.

## Missing Or Weakly Grounded Claims

- `results/literature/literature_snapshot.json` is not audit-safe as a discovery artifact by itself: its `seed_query` is too broad, its `top_papers` list is dominated by irrelevant non-Ramsey papers, and its `prior_art_watchlist` contains obvious lexical-noise false positives. Only the manually curated Ramsey-specific sections are usable.
- Several load-bearing bibliography entries still point to Semantic Scholar mirrors instead of primary endpoints even where arXiv, DOI, or publisher pages exist. This is most visible for `ge2022`, `lehavi2024`, `exoo2023`, `pontiveros2013`, `noga2022`, and also for classic papers where DOI or publisher metadata should be preferred over a discovery mirror.
- `gauthier2024` is not a hallucinated source, but the current BibTeX entry conflates the arXiv preprint with the ITP proceedings paper. If the repo cites the conference publication, it should use the ITP proceedings record and DOI rather than the arXiv DOI under a conference `journal` field.
- `aijaam2010` appears to be real prior art, but the current entry is weakly grounded: the venue and entry type are not well supported by the saved metadata, so this row should not carry much argumentative weight until it is tied to a primary publication or repository record.
- The central `H1` route claim is about transfer-safe obstruction recurrence across `42 -> 43` extensions. That is a hypothesis, not a literature result. The plan is fine to state it as a falsifiable route target, but it should not be described later as being established by prior work.

## Most Important Citation Gap

- Add a primary citation for Lehavi 2024 as `arXiv:2411.04267` and cite the matching code artifact alongside it wherever the plan invokes one-vertex extension or the `R(5,5,43)` emptiness-checking line. That is the single most important remaining gap because `H1` is built directly on reconstructing and auditing failed `42 -> 43` extensions.

## Highest-Value Bibliography Repairs

- Replace mirror-only `ge2022` metadata with the arXiv record for `2212.12630`.
- Replace or split `gauthier2024` so the proceedings paper uses the ITP DOI `10.4230/LIPIcs.ITP.2024.16`, with the arXiv version cited separately only if needed.
- Strengthen `aijaam2010` with a primary repository or publication record, or demote it to a weak-overlap note instead of a comparison-grade citation.
