# Citation Audit

Review round: `review_round_2`.

## Verdict

- `MINOR_REVISE`.
- The manuscript's core claims are traceable: the periodic-gap theorem is proved in-paper, the four quadratic identities are proved in-paper, and the benchmark counts are repository-backed rather than literature-backed.
- The current 18-entry bibliography covers the main comparison branches, and every entry in `sources.bib` is cited at least once in `research_paper.tex`.
- Remaining risk is local: a few terminology/comparison sentences are under-cited or slightly loosely anchored, but I do not see evidence of fabricated or hallucinated references.

## Key claims with adequate support

- `research_paper.tex:91`, `research_paper.tex:478`, and `research_paper.tex:901`: the paper's sole novelty-bearing theorem claim is supported by the in-paper proof, so citation dependence here is contextual rather than foundational.
- `research_paper.tex:550`, `research_paper.tex:634`, and `research_paper.tex:727`: the four certified quadratic identities are supported internally as exact propositions/corollary; outside citations matter only for prior-art positioning.
- `research_paper.tex:770`, `research_paper.tex:787`, `research_paper.tex:829`, and `research_paper.tex:831`: panel counts, holdout lengths, and anomaly/failure statements are artifact claims, not literature claims, and are traceable to the repository context rather than to missing citations.
- `research_paper.tex:108`, `research_paper.tex:115`, `research_paper.tex:118`, `research_paper.tex:121`, `research_paper.tex:124`, and `research_paper.tex:127`: the related-work backbone now covers the Beatty/Ostrowski, symbolic-recurrence, generalized-polynomial, Skolem-Mahler-Lech, and software-tool branches.

## Missing citations

- `research_paper.tex:82`: the first terminology split says that `linearly recurrent` often means return-word recurrence "in the sense of Durand", but no citation is attached at first use. The support exists later via `durand1998`, `durand2000`, and `durand2003`; it should be anchored here too.
- `research_paper.tex:472`: the figure caption says the irrational first-difference sequence is "an aperiodic two-letter mechanical word". That is stronger than the proof needs, and it currently has no citation. Either cite a standard Sturmian/mechanical-word source or weaken the caption to the strictly proved claim that the difference sequence is not eventually periodic.
- Low priority: `research_paper.tex:76` opens with a broad cross-branch framing sentence and no citation. This is not acceptance-critical, but it is the one remaining uncited overview sentence in the introduction.

## Weak citations

- `research_paper.tex:115`: `hieronymi2021` is a real and relevant neighbor, but it is an indirect support for the phrase "many Beatty relations are decidable or automaton-recognizable in Ostrowski numeration". The direct supports in the current bibliography are `schaeffer2024` and `baranwal2021`; `hieronymi2021` fits better as a Sturmian bridge than as the main Beatty-relation citation.
- `research_paper.tex:873` and `research_paper.tex:888`: `maskov2006` and `allouche2018` support the claim that the sparse quadratic lane sits near known self-matching/generalized-Beatty phenomena, but they do not by themselves show that the exact even-convergent recurrences in this paper are already covered there. The comparison is reasonable, just not maximally tight.
- `research_paper.tex:121`: the generalized-polynomial cluster is directionally correct, but the phrase `recurrence-value sets` is broader than what each of `adamczewski2022`, `byszewski2016`, and `byszewski2023` individually does. This is a mild phrasing/support looseness, not a serious mismatch.

## Likely citation hallucinations

- None identified.
- All cited keys in `research_paper.tex` resolve to real entries in `sources.bib`, and the Semantic Scholar manifest/cached results are consistent with those records.
- The earlier Walnut/Pecan citation gap is repaired: both `mousavi2016walnut` and `oei2021pecan` are now cited at `research_paper.tex:127`.
- Several BibTeX keys encode earlier draft years (`hieronymi2021`, `gnaydin2020`, `bell2005`, `derksen2005`, `allouche2018`, `maskov2006`), but the entry metadata itself points to real publications, so this is not a hallucination issue.

## Uncited comparisons

- `research_paper.tex:82`: symbolic-word linear recurrence versus arithmetic recurrence is a literature comparison and should carry the Durand citations where it is first stated.
- `research_paper.tex:472`: the rational-versus-irrational comparison in the first-difference figure is presently uncited.
- I do not see other major uncited comparison moves in the revised `Related Work` section; the main remaining issue is first-mention anchoring, not wholesale coverage.

## Most important concrete sources to add

- Amy Glen, `On Sturmian and episturmian words, and related topics`, Bull. Aust. Math. Soc. 74(1), 2006, DOI `10.1017/S0004972700047559`. Highest-value addition for `research_paper.tex:472` and for the symbolic/mechanical-word vocabulary around the introduction.
- Martin W. Bunder and Keith Tognetti, `On the self matching properties of [j tau]`, DOI `10.1016/S0012-365X(01)00147-9` (surfaced in `results/literature/ss_self_matching_beatty.json`). Best direct add if the paper keeps claiming the `phi`/`phi-1` examples sit near prior self-matching work.
- Martin W. Bunder, `Self matching in floor(n alpha)`, The Fibonacci Quarterly 44(4), 2006. Best add if the authors want a more explicit convergent-shift comparison for the even-convergent examples instead of relying only on `maskov2006`.
- Julien Cassaigne, Eric Duchene, and Michel Rigo, `Nonhomogeneous Beatty Sequences Leading to Invariant Games`, SIAM J. Discrete Math., DOI `10.1137/130948367`. Most useful add only if the discussion keeps the `floor(nr+\beta)` / zero-intercept framing and wants a literature anchor for nonhomogeneous Beatty sequences.

## Bottom line

- The citation base is now serviceable and mostly clean.
- The core paper is not blocked by a citation hallucination problem.
- Before treating the package as fully citation-safe, I would still repair the first-use Durand citation, the uncited mechanical-word caption, and the slightly loose self-matching comparison around the four quadratic examples.
