# Novelty Report

## Scope under review

- Current package claims come from `results/final_claim_memo.md`, `results/final_package_draft.md`, `results/core/h1_modular_shadow_memo.md`, `results/core/h2_pisot_backup.md`, `scripts/run_full_panel.py`, and the `special_numbers/` checker code.
- The right comparison set is the curated branch map in `results/literature/prior_art_gap.md`, not the noisy lexical watchlist in `results/literature/prior_art_watchlist.md`.

## Claim-by-claim assessment

### 1. Theorem-backed AP / finite-AP-union characterization

- Claim: for selectors with eventually periodic gaps - concretely arithmetic progressions and finite unions of arithmetic progressions - `floor(n_k r)` satisfies a homogeneous constant-coefficient recurrence over `Z` iff `r` is rational.
- Closest prior art / line of work: Skolem-Mahler-Lech style recurrence structure (`bell2005`, `derksen2005`) on the recurrence side; quadratic Beatty/Ostrowski definability (`schaeffer2024`) on the Beatty side; symbolic linear-recurrence work (`durand2000`, `durand2003`) as the main category-error neighbor.
- Distinctness judgment: materially distinct if kept exactly this narrow. The package is about ordered numeric Beatty values under frozen selector families, not zeros of a pre-existing recurrence (`bell2005`) and not definability/synchronization of Beatty relations (`schaeffer2024`).
- Weak differentiation: the rational direction is a mandatory baseline, not novelty. The irrational exclusion also relies on standard ingredients - bounded integer recurrences forcing eventual periodicity, versus non-eventual periodicity of irrational mechanical codings - so the novelty is the exact packaging of these ingredients for the locked Beatty-subsequence problem, not a wholly new mechanism.
- Novelty illusion to avoid: do not rephrase this as a theorem about all positive-density selectors. `results/final_package_review.md` already flags that overreach.

### 2. Modular-shadow / p-adic screening layer

- Claim: zero-density candidates should pass a modular-shadow barrier before they are treated as serious recurrence survivors.
- Closest prior art / line of work: Bell/Derksen recurrence obstruction language (`bell2005`, `derksen2005`) plus the Beatty/Ostrowski automatic infrastructure around `schaeffer2024`, Walnut, and Pecan.
- Distinctness judgment: currently a useful synthesis and verification tactic, not yet a clearly separated theoretical contribution.
- Concrete overlap signal: `special_numbers/diagnostics.py` implements finite residue checks on `2,3,5,7,11,25`; that is an executable screen, not a proved semilinearity or p-adic theorem.
- Weak differentiation: the phrase `p-adic semilinearity barrier` sounds stronger than the current artifact support. Right now the code shows a benchmark heuristic that helps reject prefix mirages; it does not yet establish a new recurrence-theoretic result beyond the screened families.

### 3. Sparse quadratic survivor lane (`quadratic_convergent_even`)

- Claim: the writer-stage refresh certifies the even-convergent examples `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)`, while nearby sparse quadratic holdouts on `fib_indices` and `pell_indices` remain empirical only.
- Closest prior art / line of work: quadratic Beatty/Ostrowski structure (`schaeffer2024`) and generalized Beatty / complementary Beatty constructions (`allouche2018`), with continued-fraction specialness already central in the surrounding literature.
- Distinctness judgment: empirically interesting, but not yet materially differentiated enough to stand as a novelty claim by itself.
- Concrete overlap signals:
  - `results/concept_evolve/tree/005_convergent_hankel_detector/experiment.py` tests one highly specific selector and only a 12-fit / 20-holdout exact protocol.
  - `special_numbers/baseline.py` now certifies the four named even-convergent identities, including the previously unresolved low-slope case `phi - 1`.
  - `results/experiments/claim_sensitive_ablation.json` shows that the related `fib_indices` and `pell_indices` quadratic lanes persist through 160 exact samples but still have no structural proof.
  - `results/core/h2_pisot_backup.md` already concedes that this is a quadratic / periodic-CF phenomenon, not a theorem-grade family classification.
- Missing gap evidence: there is still no cited paper-by-paper demonstration that these exact convergent-sampled or Fibonacci/Pell-sampled recurrences are absent from the quadratic Beatty / Ostrowski / generalized-Beatty literature. Without that, the package can safely claim exact named examples, but not a securely novel quadratic-family discovery.
- Novelty illusion to avoid: do not sell `quadratic irrationals are the surviving irrational family` as if it were already a literature-separated theorem. The falsifier note in `results/swarm/falsifier.md` explicitly warns that quadratic-special narratives are the easiest derivative story to accuse of rephrasing known Sturmian/Ostrowski structure.

### 4. `Quadratic, not broad Pisot` refinement

- Claim: the live survivor mechanism looks periodic-continued-fraction / quadratic rather than broadly Pisot.
- Closest prior art / line of work: Pisot/Salem generalized-polynomial work (`byszewski2023`, `byszewski2016`, `adamczewski2022`) and beta-numeration selector ideas.
- Distinctness judgment: this is currently a negative finding about one backup route, not a materially distinct mathematical contribution.
- Concrete overlap signals:
  - `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/analysis.md` calls the endpoint construction a concrete proxy.
  - `special_numbers/beta_numeration.py` uses a rounded-power basis proxy, so the failure result is against one executable approximation of beta-endpoint selection, not the full Pisot numeration line of work.
- Missing gap evidence: the negative result does not rule out richer Pisot endpoint, Rauzy-face, or generalized-polynomial embeddings already suggested by `byszewski2023`. So this claim should remain a falsifier-guided demotion of one story, not a novelty-bearing classification statement.

## Cross-cutting novelty risks

- `results/literature/prior_art_watchlist.md` is still dominated by lexical false positives. Novelty cannot be defended by that watchlist; it has to be defended by the curated comparison branches in `results/literature/prior_art_gap.md`.
- The phrase `linearly recurrent subsequence` remains dangerous unless every outward-facing draft keeps the value/word distinction explicit. `bucci2013` and the Durand line stay the main category-error traps.
- The strongest exact contribution is the narrow H1 obstruction core. Everything beyond that is either screening infrastructure or experiment-backed survivor evidence.
- `results/literature/gap_frontier.md` is now populated, but it still supports only the narrow periodic-gap contribution plus named-example reporting in the sparse quadratic lane.
- `results/literature/repository_search.md` reports that no targeted repository search found an existing solver, but that is not the same as a mathematical absence-of-prior-art argument.

## Bottom line

- The H1 theorem core looks materially distinct from the named nearby branches if it stays limited to ordered value recurrences on eventually-periodic-gap selectors.
- The sparse quadratic lane is now stronger evidentially than before because four exact identities are certified, but it is still not differentiated enough from quadratic Beatty/Ostrowski prior art to carry novelty on its own.
- The Pisot backup currently contributes more as a falsifier of an overclaim than as a positive novelty result.
- The main novelty risk is not direct duplication of a named paper; it is overclaiming from adjacent symbolic, Ostrowski, or generalized-polynomial lines without a paper-specific gap closure.

VERDICT: REVISE
