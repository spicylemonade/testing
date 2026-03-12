# Novelty Report

## Review scope

- Round: `review_round_1`.
- Audit basis: `research_paper.tex`, `results/final_claim_memo.md`, `results/core/h1_modular_shadow_memo.md`, `results/core/h2_pisot_backup.md`, `special_numbers/*.py`, `scripts/run_full_panel.py`, `scripts/run_claim_sensitive_ablations.py`, `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, and `results/swarm/director_brief.md`.
- Novelty must be argued from the curated gap notes in `results/literature/prior_art_gap.md` and `results/literature/gap_frontier.md`, not from `results/literature/prior_art_watchlist.md`, whose top entries are largely lexical false positives.

## Overall assessment

- The package has a materially distinct core, but it is narrower than the five-item contribution list in `research_paper.tex:91`.
- The defensible novelty anchor is the periodic-gap theorem for ordered Beatty-value subsequences under frozen selector classes.
- The proof lemmas, modular-shadow pipeline, sparse quadratic identities, and quadratic-not-Pisot narrative are useful, but they are not equally separated from prior art.
- Safe positioning: one narrow theorem, one exact verification workflow, and several non-anchor boundary examples.

## Claim-by-claim assessment

### 1. Periodic-gap characterization

- Claim: `research_paper.tex:93` and `research_paper.tex:482` assert that `floor(n_k r)` satisfies a homogeneous integer recurrence for some eventually periodic-gap selector if and only if `r` is rational.
- Closest prior art: the Beatty/Ostrowski decidability line, especially Schaeffer-Shallit-Zorcic, `Beatty Sequences for a Quadratic Irrational: Decidability and Applications` (`schaeffer2024`), with recurrence-side obstruction language from Bell's generalized Skolem-Mahler-Lech theorem (`bell2005`) and Derksen (`derksen2005`).
- Distinctness judgment: materially distinct if kept exactly at ordered value recurrences and eventually periodic-gap selectors. `results/literature/prior_art_gap.md:49` and `results/literature/prior_art_gap.md:73` correctly note that the nearby papers solve Beatty definability or zero/intersection-set questions, not the Beatty-side existence problem under frozen selectors.
- Weak differentiation: the rational direction is baseline, and the irrational direction packages standard ingredients: arithmetic subsequences of recurrence sequences, bounded integer recurrences are eventually periodic, and irrational Beatty differences are not eventually periodic. The novelty is the exact assembly for this locked problem, not a new recurrence-theoretic mechanism.
- Gap status: acceptable but narrow. `results/literature/gap_frontier.md:8` says no saved paper in the current archive solves this exact ordered-value selector-family problem; that supports a modest distinctness claim, not a broad claim of literature exhaustion.

### 2. Supporting lemmas as a claimed contribution

- Claim: `research_paper.tex:94` presents the supporting lemmas as a separate contribution.
- Closest prior art: classical linear-recurrence-sequence theory and mechanical/Sturmian folklore; the closest named comparison lines in the current package are Bell/Derksen on recurrence structure and Durand on symbolic linear recurrence (`durand1998`, `durand2000`, `durand2003`).
- Distinctness judgment: weak. These lemmas are proof infrastructure, not the novelty-bearing part of the paper.
- Novelty illusion: counting self-contained proofs of standard ingredients as one of the paper's five contributions inflates differentiation without a paper-specific gap note showing that these lemmas themselves were missing from prior work.
- Recommended framing: keep them as completeness/exposition, not as a standalone novelty claim.

### 3. Exact screening pipeline and "modular-shadow" layer

- Claim: `research_paper.tex:95`, `research_paper.tex:366`, and `research_paper.tex:897` present an exact screening pipeline with certificates, holdouts, and modular-shadow diagnostics.
- Closest prior art: Beatty/Ostrowski automata and exact-decision tooling (`baranwal2021`, `schaeffer2024`), plus Walnut/Pecan-style automata-assisted verification workflows (`mousavi2016walnut`, `oei2021pecan`), with Bell/Derksen as the recurrence-side obstruction language.
- Distinctness judgment: useful artifact contribution, but not yet a clearly new mathematical result.
- Concrete overlap signals:
  - `scripts/run_full_panel.py:31` fixes a short exact panel (`COUNT = 20`, `FIT_LENGTH = 12`, `MAX_ORDER = 4`).
  - `special_numbers/diagnostics.py:57` and `special_numbers/diagnostics.py:71` implement finite modular replay and a conservative classification rule, not a proved semilinearity or p-adic theorem.
  - `results/literature/prior_art_gap.md:73` already frames Bell as obstruction language rather than a solved Beatty theorem.
- Weak differentiation: terms like `p-adic semilinearity barrier` or `modular-shadow obstruction` are stronger than the artifact support. The code shows a good verification filter, not a new theorem beyond the proved selector classes.
- Missing gap evidence: there is no paper-specific comparison showing that this workflow itself is novel relative to existing Beatty/automata verification practice. Keep it as methodology, not as the main novelty claim.

### 4. Four certified quadratic-convergent identities

- Claim: `research_paper.tex:96`, `research_paper.tex:550`, and `research_paper.tex:731` treat `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)` on even convergents as exact certified examples.
- Closest prior art: Masakova-Pelantova, `Self-Matching Properties of Beatty Sequences` (`maskov2006`), and Allouche-Dekking, `Generalized Beatty sequences and complementary triples` (`allouche2018`), with Schaeffer-Shallit-Zorcic (`schaeffer2024`) as the nearby quadratic/Ostrowski line.
- Distinctness judgment: exact and worthwhile as named examples, but weakly differentiated as a novelty anchor.
- Concrete overlap signals:
  - `results/literature/prior_art_gap.md:49` and `results/literature/gap_frontier.md:8` already warn that the quadratic lane overlaps with known quadratic Beatty phenomena and should not carry the paper's main novelty.
  - `special_numbers/baseline.py:59` hard-codes the four named quadratic certificates; the code verifies specific identities rather than deriving a broader quadratic classification.
  - `results/experiments/claim_sensitive_ablation.md:9` and `results/experiments/claim_sensitive_ablation.md:14` show nearby quadratic selectors also survive long exact holdouts, which weakens any attempt to portray `quadratic_convergent_even` as a sharply isolated new family theorem.
- Missing gap evidence: there is no cited paper-by-paper demonstration that these exact convergent-sampled recurrences, especially the `phi - 1` case, are absent from the self-matching/generalized-Beatty literature. Without that, these should remain auxiliary exact examples.
- Novelty illusion: do not turn `four certified quadratic examples` into `quadratics are the surviving irrational family`. `results/swarm/falsifier.md:16` explicitly warns that such a quadratic-special narrative is derivative and unstable.

### 5. `Quadratic, not broad Pisot` and the procedural honesty claim

- Claim: `research_paper.tex:96` and `research_paper.tex:899` suggest two further contributions: a quadratic-not-Pisot refinement and a broader procedural lesson about keeping proof, certificate, and empirical evidence separate.
- Closest prior art: the mathematical neighbor is the generalized-polynomial/Pisot-Salem line (`byszewski2016`, `byszewski2023`, `adamczewski2022`); the procedural neighbor is automata-assisted exact verification tooling such as Walnut/Pecan.
- Distinctness judgment:
  - The `not broad Pisot` part is a falsifier result, not a new positive classification.
  - The procedural part is good practice, but it is not literature-separated enough to count as a novelty-bearing research claim.
- Concrete overlap signals:
  - `results/core/h2_pisot_backup.md:31` already says the strong Pisot narrative is unsupported.
  - `special_numbers/beta_numeration.py:8` and `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/analysis.md:5` show that the negative Pisot evidence is against one rounded-power-basis proxy, not against the full beta-numeration or Rauzy-face literature suggested by `byszewski2023`.
  - The revision citation audit now normalizes the Walnut/Pecan references, so the remaining weakness is not metadata but the lack of a literature-separated argument that the workflow itself is a novelty-bearing contribution.
- Missing gap evidence: there is no direct literature comparison establishing that the workflow-level `keep proof/certificate/evidence separate` contribution is itself novel in computer-assisted mathematics.
- Novelty illusion: present both points as scope discipline and falsifier outcomes, not as co-equal mathematical contributions.

## Cross-cutting risks

- `results/literature/prior_art_watchlist.md` is still a novelty trap. Its leading entries are geology, systems, and materials false positives, so it cannot support any novelty defense.
- The main category-error risk remains word/value confusion. `results/literature/prior_art_gap.md:57` and `results/literature/prior_art_gap.md:15` correctly keep Durand and Bucci-Puzynina-Zamboni as comparison branches, not solution templates.
- The theorem should stay at `eventually periodic-gap selectors`. `results/final_package_review.md:10` already flags the overreach of rephrasing it as all positive-density selectors.
- Benchmark evidence is not gap closure. Long exact holdouts and modular replay help calibration, but they do not replace paper-specific prior-art separation.

## Bottom line

- Materially distinct: the narrow periodic-gap theorem for ordered Beatty-value recurrences under frozen eventually periodic-gap selectors.
- Distinct but not novelty-bearing on their own: the proof lemmas, the verification pipeline, the four quadratic exact examples, and the quadratic-not-Pisot negative.
- Main required revision: keep the novelty hierarchy explicit and avoid presenting all five numbered contributions as equally new.

VERDICT: REVISE
