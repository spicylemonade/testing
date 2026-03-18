# Novelty Report

## Assessment Summary

Material distinction from known prior art is weak unless the contribution is rewritten as a narrow negative operational result. The current artifact set does **not** support a positive novelty claim for a new arithmetic-Kakeya formulation, a successful cellular-automaton mechanism, a useful abelian-network mechanism, or a verified decoder-style route. The only defensible novelty is a small exact benchmark-and-falsification workflow inside the existing finite-certificate arithmetic-Kakeya setting.

## Claim-By-Claim Comparison

### 1. Claim: a CA-style macrocell compiler improves exact arithmetic-Kakeya certificates

- Closest paper or line of work:
  - Katz-Tao (1999), *Bounds on Arithmetic Projections, and Applications to the Kakeya Conjecture*
  - Green-Ruzsa (2017), *On the arithmetic Kakeya conjecture of Katz and Tao*
  - bootstrap / critical cellular-automata line: Bollobas-Duminil-Copin-Morris-Smith (2014), Hartarsky-Mezei (2018)
- Distinctness assessment:
  - Not materially distinct on the current evidence.
  - The arithmetic object remains inside the Katz-Tao / Green-Ruzsa finite-certificate lane, while the CA overlay never earns a verified matched-baseline gain.
  - The route dies before scoring because of the exact one-seed obstruction recorded in `results/phase4_h1_frontier.md`.
- Overlap signal:
  - `H1_L1_exact` and `H1_L2_exact` both fail exact verification before any level-1 versus level-2 transfer comparison.
  - `results/literature/prior_art_gap.md` already narrows H1 to a fixed corridor compiler plus exact verifier, not a new theorem or formulation.
- Missing gap evidence:
  - no level-2 transfer improvement,
  - no matched-baseline win over direct no-CA corridor search,
  - no evidence that extracted families escape the bounded-slope / low-rational-complexity basin flagged by Tao (2025).

### 2. Claim: target-direction abelian invariants add genuine screening or mathematical power

- Closest paper or line of work:
  - Bond-Levine, *Abelian Networks I-III* (2013-2015)
  - chip-firing / sandpile / critical-group line
- Distinctness assessment:
  - Not materially distinct.
  - The imported abelian language acts only as a screen on the same relation matrices already visible to direct arithmetic analysis.
  - `results/phase4_h2_screen.md` shows no screening gain beyond raw support size, rank, Smith-tail information, and target-solvable counts.
- Overlap signal:
  - The dead H1 families are already separated by `support_size = 1`, `target_solvable_vertices = 0`, and verification failure.
  - The abelian package adds no extra ordering power on the tested family IDs.
- Missing gap evidence:
  - no predictive lift over direct arithmetic descriptors,
  - no theorem extracted from the abelian encoding,
  - no matched family where abelian invariants retain a better exact witness frontier than raw features.

### 3. Claim: slope-bloom or local-decoder machinery opens a new certificate route

- Closest paper or line of work:
  - Sipser-Spielman (1996), *Expander Codes*
  - Hemenway-Ostrovsky-Wootters (2013), *Local correctability of expander codes*
  - Kubica-Preskill (2018), *Cellular-Automaton Decoders with Provable Thresholds for Topological Codes*
- Distinctness assessment:
  - No material distinction is established because this route was never activated.
  - At present it is only a reserve hypothesis, not a verified contribution.
- Overlap signal:
  - `results/literature/prior_art_gap.md` and `results/phase5_negative_results.md` both leave H3 inactive.
  - The repo already treats Tao (2025) as a kill condition if realized slope or rational complexity stays bounded.
- Missing gap evidence:
  - no exact extraction equivalence between decoder success and legal forcing,
  - no matched-baseline result,
  - no evidence that the route leaves the bounded-slope / low-rational-complexity regime.

### 4. Claim: the verifier-friendly certificate language is a new framework for arithmetic Kakeya

- Closest paper or line of work:
  - Katz-Tao (1999)
  - Green-Ruzsa (2017)
  - Cowen-Breen, Karangozishvili, Varadarajan, Wang (2020), *Pattern Problems related to the Arithmetic Kakeya Conjecture*
- Distinctness assessment:
  - Not materially distinct.
  - The repo's own gap note already says this language should not be marketed as a new mathematical framework; it is a certificate-first operational packaging inside an existing finite-certificate / pattern-problem lane.
- Overlap signal:
  - `results/literature/prior_art_gap.md` explicitly marks this framing as not defensible.
  - The surviving artifacts prove no new equivalence, theorem, or formulation claim beyond the named papers.
- Missing gap evidence:
  - no new equivalence theorem,
  - no new pattern implication,
  - no theorem-level separation from the Katz-Tao / Green-Ruzsa / Cowen-Breen line.

### 5. Claim: the surviving contribution is an exact corridor benchmark-and-falsification workflow

- Closest paper or line of work:
  - the Katz-Tao / Green-Ruzsa finite-certificate arithmetic-Kakeya line
  - direct arithmetic certificate search on matched corridor geometries, as evidenced by the no-CA controls in `results/phase4_h1_frontier.md`
- Distinctness assessment:
  - This is the only claim with plausible material distinction, but the distinction is operational and narrow rather than mathematical.
  - What survives is an exact extraction pipeline, matched direct controls, and clean route-kill criteria inside a tiny width-2 corridor family.
  - Even here the differentiation is weak because the surviving positive rows come from direct no-CA search, not from the imported CA or abelian ideas.
- Overlap signal:
  - direct controls at `2 x 4` and `2 x 6` both reach score `2.0`,
  - frozen H1 and H2 add no verified improvement,
  - `results/phase4_ablations.md` shows boundary sensitivity, weak dependence on the specific `X`, and failure under frozen-`X` scaling.
- Missing gap evidence:
  - no exhaustive frontier,
  - corridor-only scope,
  - no evidence that this workflow beats generic exact search outside the hand-built corridor family.

## Novelty Illusions

- "The CA route solved arithmetic Kakeya here." It did not; the exact H1 route never produces a legal forcing certificate.
- "The forcing process is a cellular automaton." The exact verifier and global linear-span step do the mathematical work; the CA framing is at most a candidate generator.
- "The abelian-network interpretation adds new mathematics." On current evidence it only renames arithmetic descriptors that already separate dead and live families.
- "The verifier language is a new framework." The closest line remains Katz-Tao to Green-Ruzsa to Cowen-Breen; no new equivalence or theorem is shown.
- "The direct corridor controls reveal a new mechanism." The ablations instead point to boundary-heavy, finite-size controls in the same tiny fixed-`X` basin flagged by Tao (2025).

## Weak Differentiation

- The strongest surviving artifact is negative: H1 is killed by exact obstruction and H2 is killed by non-additive screening.
- The only successful exact witnesses come from matched direct no-CA corridor search, which means the imported bridge language is not carrying the positive result.
- The final frontier stays around score `2.0`, far from the target `1.675`, and remains inside the corridor-local regime already marked in the gap note as low-rational-complexity danger territory.

## Missing Gap Evidence

- A positive route must beat matched direct no-CA search on the same geometry; the current artifacts show the opposite.
- A positive route must survive scale transfer or at least exit the bounded-slope / low-rational-complexity warning basin; the current artifacts do neither.
- Any abelian or decoder vocabulary must add predictive power beyond raw arithmetic features; no such lift is shown.
- Any claim beyond the width-2 corridor program needs evidence on broader constructible graph families, not only the frozen corridor grammar.

## Bottom Line

As a theorem or mechanism paper, the contribution is not materially distinct from the closest prior-art lines because the positive CA, abelian, and decoder stories collapse under exact verification and matched baselines. As a negative operational artifact, the work does have a narrow identity: an exact verifier-backed corridor benchmark that cleanly falsifies two overpromising bridge hypotheses and leaves only small direct controls around score `2.0`. That narrower identity is real, but it is much weaker than the original bridge narrative and should be written as such.

REVISE
