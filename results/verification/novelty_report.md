# Novelty Report

Phase: `review_round_1`

## Assessment Summary

The current draft is already much closer to the honest novelty position than the earlier bridge narrative. On the present artifact set, only **two lanes look materially distinct**, and both are narrow corridor-family theorems:

- a sound-and-complete exact verifier theorem for the width-2 corridor family,
- a one-seed obstruction theorem that kills the frozen H1 route before scoring.

Everything else is **not materially distinct** as a new arithmetic-Kakeya theorem, a new formulation, a successful cellular-automaton mechanism, a successful abelian-network mechanism, or a decoder-style route. Outside those two narrow theorem lanes, the paper is only **operationally distinct** as an exact benchmark-and-falsification artifact inside the existing finite-certificate arithmetic-Kakeya setting.

That narrower identity is real. But it is still small, family-local, and easy to overread if the paper drifts back toward mechanism-level language.

## Claim-By-Claim Comparison

### 1. Claim lane: contribution to arithmetic Kakeya beyond existing theorem/formulation lines

- Closest papers or line of work:
  - Katz-Tao (1999), *Bounds on Arithmetic Projections, and Applications to the Kakeya Conjecture*
  - Green-Ruzsa (2019), *On the Arithmetic Kakeya Conjecture of Katz and Tao*
  - Cowen-Breen, Karangozishvili, Varadarajan, Wang (2020), *Pattern Problems Related to the Arithmetic Kakeya Conjecture*
  - Pohoata-Zakharov (2024), *Generalized Arithmetic Kakeya*
  - Tao (2025), *Sum-Difference Exponents for Boundedly Many Slopes, and Rational Complexity*
- Distinctness assessment:
  - Not materially distinct mathematically.
  - The paper now correctly places itself inside the same finite-certificate universe rather than claiming a new projection framework, equivalence, or theorem.
- Concrete overlap signal:
  - `research_paper.tex` explicitly says the work is not a new theorem or reformulation.
  - `results/literature/prior_art_gap.md` marks those stronger claims as not defensible.
- Missing gap evidence:
  - no new exponent,
  - no new implication,
  - no new generalized theorem,
  - no evidence of movement against the bounded-slope / rational-complexity barrier flagged by Tao (2025).

### 2. Claim lane: width-2 corridor compiler and exact verifier

- Closest paper or line of work:
  - the Katz-Tao / Green-Ruzsa finite-certificate lane,
  - plus the repo's own certificate-first operational packaging in `results/phase2_certificate_grammar.md` and `scripts/ca_kakeya_search.py`
- Distinctness assessment:
  - Materially distinct at the corridor-family level, but narrow.
  - This is a genuine sound-and-complete theorem for the repo's width-2 corridor semantics.
  - It is not a new mathematical framework and not a general verifier for arbitrary constructible graphs.
- Concrete overlap signal:
  - `research_paper.tex` restricts Proposition `prop:compiler` and Theorem `thm:verifier` to the width-2 corridor family.
  - `results/literature/prior_art_gap.md` already warns against marketing the verifier-friendly language as a new framework.
- Missing gap evidence:
  - no broader constructible-graph validation,
  - no evidence that the compiler/verifier exposes phenomena unavailable to direct exact search beyond this corridor subset,
  - no external benchmark showing that the corridor restriction is principled rather than merely convenient.

### 3. Claim lane: one-seed obstruction theorem

- Closest paper or line of work:
  - finite-certificate linear-invariant reasoning inside the arithmetic-Kakeya certificate setting,
  - with the surrounding mathematical universe still closest to Katz-Tao (1999) and Green-Ruzsa (2019)
- Distinctness assessment:
  - Materially distinct, but narrow.
  - This is a legitimate route-kill theorem for the frozen H1 family, but not a new obstruction line for arithmetic Kakeya more broadly.
- Concrete overlap signal:
  - `results/phase4_h1_frontier.md` records that every frozen H1 instance has exactly one singleton seed and empty initial `T`.
  - `research_paper.tex` Theorem `thm:one-seed` and Corollary `cor:h1` formalize exactly that kill condition.
- Missing gap evidence:
  - no evidence that the obstruction applies to a broader natural certificate class,
  - no comparison showing that this invariant creates a reusable theorem frontier beyond the frozen H1 corridor pilot.

### 4. Claim lane: CA-inspired macrocell route adds genuine mechanism or search power

- Closest papers or line of work:
  - Bollobas-Duminil-Copin-Morris-Smith (2015), *Universality for Two-Dimensional Critical Cellular Automata*
  - Hartarsky-Mezei (2020), *Complexity of Two-Dimensional Bootstrap Percolation Difficulty*
  - together with the arithmetic-Kakeya line above
- Distinctness assessment:
  - Not materially distinct as a positive mechanism.
  - The only surviving distinctness is negative: the work exactly falsifies one CA-style corridor grammar after exact extraction.
- Concrete overlap signal:
  - `results/phase4_h1_frontier.md` shows exact verification failure before any score comparison.
  - `results/phase5_ca_vs_search_prior.md` states that no mathematical gain survived verification.
  - `results/literature/prior_art_gap.md` explicitly warns that bootstrap/critical-CA overlap will swallow weak claims.
- Missing gap evidence:
  - no matched-baseline win over direct no-CA corridor search,
  - no level-1 to level-2 transfer success,
  - no evidence that extracted families leave the bounded-slope / low-rational-complexity basin.

### 5. Claim lane: target-direction abelian invariants add useful screening

- Closest papers or line of work:
  - Bond-Levine, *Abelian Networks I-III* (2013-2015)
  - chip-firing / sandpile / critical-group line
- Distinctness assessment:
  - Not materially distinct.
  - The imported abelian language yields only a negative comparison: on the tested family IDs it does not outperform direct arithmetic descriptors.
- Concrete overlap signal:
  - `results/phase3_h2_program.md` pre-registers that H2 survives only if it beats raw arithmetic features on the same family IDs.
  - `results/phase4_h2_screen.md` shows that support size and target-solvable count already separate the dead H1 rows from the surviving direct controls.
  - `results/phase5_negative_results.md` records the route kill.
- Missing gap evidence:
  - no predictive lift,
  - no retained-best frontier advantage,
  - no theorem extracted from the abelian encoding,
  - only a four-family screen.

### 6. Claim lane: decoder / slope-bloom reserve route contributes novelty

- Closest papers or line of work:
  - Sipser-Spielman (1996), *Expander Codes*
  - Hemenway-Ostrovsky-Wootters (2015), *Local Correctability of Expander Codes*
  - Kubica-Preskill (2019), *Cellular-Automaton Decoders with Provable Thresholds for Topological Codes*
  - Tao (2025) as the barrier note for bounded-slope / rational-complexity collapse
- Distinctness assessment:
  - No novelty established in this round.
  - H3 never activated, so it cannot count as a material contribution.
- Concrete overlap signal:
  - `results/literature/prior_art_gap.md` keeps H3 reserve-only.
  - `results/phase5_negative_results.md` records that H3 was not activated.
- Missing gap evidence:
  - no exact extraction equivalence,
  - no matched-baseline result,
  - no evidence of leaving the bounded-slope / low-rational-complexity regime.

### 7. Claim lane: the surviving contribution is an exact benchmark-and-falsification workflow

- Closest paper or line of work:
  - exact certificate search inside the existing finite-certificate arithmetic-Kakeya lane,
  - with no strong direct published analogue identified in the repo notes
- Distinctness assessment:
  - This is the only claim with plausible material distinction.
  - Even here the distinction is operational and narrow rather than mathematical.
  - The real contribution is the combination of exact extraction, matched direct controls, route-specific kill criteria, and anti-overclaim documentation.
- Concrete overlap signal:
  - `results/phase4_h1_frontier.md`, `results/phase4_h2_screen.md`, `results/phase4_ablations.md`, `results/phase5_negative_results.md`, and `results/phase5_ca_vs_search_prior.md` jointly support this reading.
- Missing gap evidence:
  - the successful positive rows come from direct no-CA controls rather than the imported bridge ideas,
  - the family remains corridor-only,
  - the ablations are small-sample,
  - the best score stays at `2.0` / `29/14`, not near `1.675`.

## Novelty Illusions

- “This is a new arithmetic Kakeya theorem or formulation.”
  - `results/literature/prior_art_gap.md` already marks that as not defensible; the closest line remains Katz-Tao / Green-Ruzsa / Cowen-Breen / Pohoata-Zakharov.
- “The CA mechanism improved the exact arithmetic.”
  - `results/phase5_ca_vs_search_prior.md` says no mathematical gain survived verification.
- “Arithmetic forcing is basically a cellular automaton.”
  - `results/swarm/falsifier.md` and `results/literature/prior_art_gap.md` both warn that global integer-span closure, not local CA rollout, does the mathematical work.
- “The abelian-network interpretation adds new mathematics here.”
  - `results/phase4_h2_screen.md` shows no screening lift beyond raw arithmetic features on the tested family IDs.
- “The verifier language is a new framework.”
  - the paper's own Related Work and `results/literature/prior_art_gap.md` reject that reading.
- “The direct corridor controls reveal a scalable new mechanism.”
  - `results/phase4_ablations.md` supports only a boundary-sensitive finite-size control story, and even that should be phrased cautiously.

## Weak Differentiation

- The strongest results are negative kills of H1 and H2, not positive wins over prior art or matched baselines.
- The only successful exact witnesses are matched direct no-CA controls, so the imported CA / abelian bridge language is not carrying the positive rows.
- The proof-level distinctness of the paper is narrow and family-local: a corridor verifier theorem and a route-specific obstruction theorem.
- The empirical frontier remains in the tiny fixed-`X`, width-2 corridor regime singled out by Tao (2025) and `results/swarm/gap_map.md` as a likely bounded-slope / rational-complexity trap.

## Missing Gap Evidence

- A positive route would need a matched-baseline win over direct no-CA search on the same geometry; current artifacts show the opposite.
- A materially new mechanism would need some evidence of transfer or of leaving the bounded-slope / low-rational-complexity basin; no such evidence appears.
- Any abelian or decoder vocabulary would need predictive power beyond raw arithmetic features; none is shown.
- Any novelty claim above the workflow level would need evidence outside the frozen width-2 corridor family.
- If the paper keeps strong scale language, it needs more than one base witness, four randomization trials, and bounded-search frozen-`X` failures.

## Recommended Framing Changes

- Keep “negative operational benchmark-and-falsification result” as the headline identity.
- Scope every negative empirical statement to “the tested family IDs,” “the saved corridor rows,” or “the frozen width-2 corridor program.”
- Treat the corridor compiler, verifier theorem, and one-seed obstruction theorem as route-local formal contributions, not as theorem-frontier contributions.
- Replace any “plateau” or “does not scale” wording with the narrower claim actually supported by `results/phase4_ablations.md`: no clean transfer was found in the saved frozen-`X` bounded search.

## Bottom Line

As currently drafted, the paper has a real but narrow novelty position: two corridor-local theorem contributions, plus an exact, audit-ready falsification of two bridge hypotheses inside the existing finite-certificate arithmetic-Kakeya setting. It is still not materially distinct as a new arithmetic-Kakeya theorem line, formulation, CA mechanism, abelian-network mechanism, or decoder route. The current draft is close to the honest version of that claim, but it still needs tighter scope language so corridor-local novelty is not mistaken for broader mathematical novelty.

REVISE
