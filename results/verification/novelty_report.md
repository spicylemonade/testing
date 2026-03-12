# Novelty Report

## Review scope

- Round: `review_round_2`.
- Audit basis: `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, `results/swarm/director_brief.md`, `research_paper.tex`, `results/final_claim_memo.md`, `results/core/h1_modular_shadow_memo.md`, `results/core/h2_pisot_backup.md`, `results/experiments/literature_baseline_comparison.md`, `scripts/run_full_panel.py`, `scripts/run_claim_sensitive_ablations.py`, `special_numbers/baseline.py`, and `special_numbers/diagnostics.py`.
- Novelty should be judged against the curated comparison branches in `results/literature/prior_art_gap.md`, not against the raw `results/literature/prior_art_watchlist.md`, whose top entries still include lexical false positives.

## Overall assessment

- The revised package now has one clear novelty-bearing contribution: the eventually-periodic-gap theorem for ordered Beatty-value recurrences.
- That core claim is materially distinct from the closest nearby branches named in `results/literature/prior_art_gap.md`: Schaeffer-Shallit-Zorcic on quadratic Beatty decidability, Durand and Bucci-Puzynina-Zamboni on symbolic recurrence, Byszewski-Konieczny on generalised-polynomial value sets, and Bell-Derksen on zero sets of pre-existing recurrences.
- The rest of the package is not equally new. The four quadratic identities sit close to self-matching/generalized-Beatty work, the modular-shadow layer is a verification discipline rather than a new theorem, and the sparse panel still lacks the controls needed for any quadratic-only or not-Pisot boundary claim.
- On the current draft, the contribution is materially distinct if the paper keeps novelty centered on the periodic-gap theorem and treats the sparse lane as supporting evidence only.

## Major-claim assessment

### 1. Eventually periodic-gap characterization

- Claim: `research_paper.tex` and `results/final_claim_memo.md` assert that `floor(n_k r)` satisfies a homogeneous integer recurrence for some eventually periodic-gap selector if and only if `r` is rational.
- Closest prior art: Schaeffer, Shallit, and Zorcic, *Beatty Sequences for a Quadratic Irrational: Decidability and Applications*; Bell, *A Generalised Skolem-Mahler-Lech Theorem for Affine Varieties*; Derksen, *A Skolem-Mahler-Lech theorem in positive characteristic and finite automata*; with Durand's symbolic linear-recurrence line as the main category-boundary comparison.
- Distinctness judgment: materially distinct. Those lines study Beatty definability, automatic recognizability, symbolic linear recurrence, or zero/intersection sets of already-given recurrences. The present theorem asks the Beatty-side existence question for ordered numeric subsequences under frozen eventually periodic-gap selectors, exactly the distinction recorded in `results/literature/prior_art_gap.md` and `results/experiments/literature_baseline_comparison.md`.
- Weak differentiation: the proof mechanism itself is not radically new. The rational direction is baseline, and the irrational direction is an assembly of standard recurrence facts plus Beatty-difference aperiodicity. The novelty lies in the locked formulation and the exact theorem-level synthesis, not in a new recurrence-theoretic engine.
- Missing gap evidence: the gap note is comparative rather than exhaustive. The package still does not show a dedicated near-duplicate search proving that no earlier Beatty paper already states this exact selector-family theorem. That is a caution, not a blocker.

### 2. Four certified quadratic-convergent identities

- Claim: `research_paper.tex`, `results/final_claim_memo.md`, and `special_numbers/baseline.py` certify exact cases for `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)` along even convergent denominators.
- Closest prior art: Masakova and Pelantova, *Self-Matching Properties of Beatty Sequences*; Allouche and Dekking, *Generalized Beatty sequences and complementary triples*; secondarily the quadratic Beatty/Ostrowski line of Schaeffer-Shallit-Zorcic.
- Distinctness judgment: weak as a novelty anchor. These identities live inside an already active quadratic Beatty ecosystem.
- Concrete overlap signals: `results/literature/prior_art_gap.md` already treats the quadratic lane as a comparison branch rather than the main novelty claim; `special_numbers/baseline.py` encodes the four certificates directly as named identities; `scripts/run_claim_sensitive_ablations.py` shows nearby convergent variants also keep long exact holdouts, so `quadratic_convergent_even` is not a sharply isolated frontier by itself.
- Missing gap evidence: the package still does not show paper-by-paper that the displayed formulas are absent from the self-matching/generalized-Beatty literature.
- Novelty illusion: presenting these examples as the main discovery, or as evidence of a new quadratic family theorem, would slide back into territory already occupied by `maskov2006` and `allouche2018`.

### 3. Sparse panel and the "not broad Pisot" takeaway

- Claim: in the frozen panel, only the four quadratic cases certify exactly; higher-degree Pisot, Salem, and transcendental controls do not.
- Closest prior art: Byszewski and Konieczny, *Pisot numbers, Salem numbers, and generalised polynomials*; Byszewski and Konieczny, *Sparse generalised polynomials*; Adamczewski and Konieczny, *Bracket words*; plus the quadratic Beatty/Ostrowski line.
- Distinctness judgment: useful as calibrated evidence, not as a major novelty claim.
- Concrete overlap signals: `results/core/h2_pisot_backup.md` already says the strong Pisot-family story failed; `scripts/run_full_panel.py` and `results/verification/benchmark_report.md` show the control bank is still too thin for a family boundary, with no `floor(n r + beta)` intercept controls and no continued-fraction-prefix-matched nonquadratic controls.
- Missing gap evidence: there is no literature-separated argument that these negative panel results correspond to a new structural theorem rather than a local experimental map.
- Novelty illusion: "quadratic, not broad Pisot" is a falsifier outcome, not a theorem.

### 4. Modular-shadow / certificate-first workflow

- Claim: the package's exact fitting, holdout, and modular replay discipline prevents finite-prefix mirages from being misreported as theorem evidence.
- Closest prior art: Walnut and Pecan theorem-proving workflows; Baranwal, Schaeffer, and Shallit on Ostrowski-automatic sequences; Schaeffer-Shallit-Zorcic on automata-assisted Beatty reasoning.
- Distinctness judgment: good methodology, but not strongly differentiated as standalone research novelty.
- Concrete overlap signals: `special_numbers/diagnostics.py` implements finite modular replay and conservative labeling, not a proved semilinearity or p-adic obstruction theorem; `results/literature/repository_search.md` already identifies Walnut and Pecan as the nearest reusable tooling line.
- Missing gap evidence: no explicit comparison shows that this workflow, by itself, is novel relative to existing computer-assisted Beatty/automatic-sequence practice.
- Novelty illusion: the phrase `p-adic semilinearity barrier` is stronger than what the current paper and code actually prove.

## Cross-cutting risks

- `results/literature/prior_art_watchlist.md` is still not usable novelty evidence; most of its top entries are lexical false positives and should remain retired except as search-hygiene warnings.
- The main category-error risk remains the word/value boundary. Durand and Bucci-Puzynina-Zamboni are genuinely close enough to create superficial overlap, but only at the symbolic level; `results/definition_lock.md` correctly blocks treating that literature as a solution to the ordered-value problem.
- The paper stays novelty-safe only if the theorem remains stated for `eventually periodic-gap selectors` and the sparse lane remains explicitly auxiliary. Any return to all-positive-density, quadratic-family, periodic-CF, or zero-intercept language would reopen the same overlap problems flagged in `results/verification/benchmark_report.md` and `results/verification/verification_summary.md`.
- The direct novelty case for the theorem is good but modest: it is a new result at a carefully frozen interface between nearby literatures, not a replacement for the broader Beatty, generalized-polynomial, or symbolic-recurrence lines.

## Bottom line

- Materially distinct now: the periodic-gap theorem for ordered Beatty-value subsequences.
- Weakly differentiated and non-anchor: the four quadratic exact identities, the sparse negative/control story, and the modular-shadow workflow.
- Missing but non-fatal gap evidence: a tighter paper-by-paper exclusion note for near-duplicate theorems or formulas, especially around the quadratic identities.

VERDICT: ACCEPT
