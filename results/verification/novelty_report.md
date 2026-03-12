# Novelty Report

## Scope

This review checks whether the **current** manuscript and code package are materially
distinct from the closest prior art after the post-deepen audits. It is grounded in:

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/evaluation/literature_comparison.md`
- `results/claims/h1_frontier_witness_certificate.md`
- `results/claims/h2_prime_support_fixed_point.md`
- `results/novelty_deepening/item_026_anchor_backbone.md`
- `results/novelty_deepening/item_027_schedule_network.md`
- `results/novelty_deepening/item_028_prefix_law.md`
- `results/novelty_deepening/item_029_hypergraph_invariants.md`
- `results/novelty_deepening/item_030_modular_locking.md`
- `results/verification/verification_summary.md`
- `research_paper.tex`
- `scripts/prime_separator.py`
- `scripts/novelty_deepening.py`

I also ran targeted external checks against OEIS `A129258` / `A129259`, Kimberling's
public problem statement, and the Ford overlap branch. Those checks did not surface a
closer named source than the repo's current watchlist, but they do reinforce that the
public provenance and the Ford divisor/product-coverage line are the real novelty
boundary.

## Executive Assessment

The package is materially distinct only in a **narrow** sense:

- as a proof-level cleanup of exact consequences of Kimberling's public recurrence;
- as a validated computation and audit package around that recurrence;
- as a negative-result dossier showing that the strongest currently proposed mechanism
  stories fail on the stored corpus.

It is **not** materially distinct if presented as:

- a new positive mechanism for row-gap formation;
- a prime-support explanation of late records;
- a `T`-specific witness or hypergraph invariant that clearly escapes Ford-style local
  divisor/product coverage;
- a boundedness or unboundedness result for `T(1,n+1) - T(1,n)`.

So the surviving novelty is real, but smaller than the strongest rhetorical version of
the paper.

## Claim-by-Claim Comparison

| major claim | closest paper or line of work | assessment |
|---|---|---|
| The array, recurrence, first-row sequence, and bounded-difference question are introduced here. | OEIS `A129258`, OEIS `A129259`, Clark Kimberling, *100 Conjectures and/or Problems*. | Not novel. This is public provenance. |
| Theoretical cleanup: “first two missing values” formulation, strict interleaving, unique column term in each row gap, `row_immediate = baseline`, and `column_immediate = axis swap`. | Closest line: direct consequences of the public OEIS/Kimberling recurrence. | Distinct but close to provenance. These look like real formal additions, but they are low-distance structural consequences of an already public rule. |
| Every prime lies on exactly one axis. | OEIS `A129258` / `A129259` prime-separation observation. | Distinct only as a proof of a public fact. The phenomenon is not new; the proof is. |
| The forced axis-1 anchor / previous-column witness is a meaningful `T`-specific invariant. | Closest line: the same recurrence geometry behind OEIS/Kimberling. | Real but thin. It covers exactly one point per row gap and does not by itself differentiate a broader mechanism. |
| The million-step generator, digest checks, and independent checker materially deepen the mathematics. | Closest line: reproducible computation around the public OEIS/Kimberling object. | Distinct as artifact quality and validation, not as new mathematics. Better evidence is not itself a new theorem. |
| `H1`: late windows admit a compact mex-coupled witness certificate or bounded-memory anchor law. | Kevin Ford, *The multiplication table problem*; Kevin Ford, *The distribution of integers with a divisor in a given interval*. | Not differentiated as a positive claim. The strong form fails, and the surviving witness picture still looks too close to heterogeneous local divisor/product coverage. |
| The schedule / abelian audit supplies a new mechanism. | Closest line: recurrence-identity cleanup of the same `T` process; external overlap remains OEIS/Kimberling provenance. | Weak novelty as a separate claim. It is a useful consistency result, but it collapses back to the same anchor geometry rather than creating a new explanatory object. |
| The border-prefix lane yields a broad certificate impossibility theorem. | Closest line: the paper's own forced-unit-witness geometry, with Ford's divisor-interval line as overlap control. | Distinct only in a narrow negative sense. It rules out bounded recent-prefix raw-witness / border-order explanations of the current type; it does not justify broader “all certificate formalisms are impossible” language. |
| Full witness hypergraphs rescue H1 via a rigidity invariant. | Closest line: Ford-style local coverage seen through constrained-factorization / witness-hypergraph instrumentation. | Not differentiated as a positive claim. Item 029 is a failed positive search: the best near-miss still overlaps matched controls too heavily. |
| `H2`: prime-support asymmetry explains record-gap formation. | OEIS / Kimberling prime-split provenance. | Not novel and not explanatory. The package itself demotes this lane. |
| `H3`: modular or multiplicative-basis framing supplies a low-overlap rescue route. | Pach and Sandor, *Multiplicative Bases and an Erdős Problem*, plus the broader multiplicative-basis branch. | Not currently differentiated. The lane remains reserve-only and fails in the present audit package. |

## Closest-Overlap Findings

### 1. Provenance is already occupied

OEIS `A129258` publicly gives the recurrence and records the prime-separation
observation. OEIS `A129259` and Kimberling's problem page already occupy the first-row
sequence and the bounded-difference question. Reconstructing the array, repeating the
prime split, or restating the open problem is therefore not novelty.

### 2. The real overlap pressure remains the Ford branch

The repo's watchlist is still correct: the main novelty hazard is Ford's
multiplication-table / divisor-in-an-interval line, not the provenance sources and not
the multiplicative-basis branch. The reason is structural:

- late skipped values are still explained by local border-factor pairs;
- singleton-heavy coverage persists;
- balanced-factor share rises rather than collapsing to a small reusable grammar;
- the hypergraph layer improves bookkeeping, but not enough to isolate a clearly
  mex-coupled invariant.

The paper survives best when Ford is used as an overlap-control comparison and the
remaining witness story is treated as a failed positive mechanism search.

### 3. The post-deepen audits strengthen the negative case, not the positive one

The new audits do add something materially distinct from the public OEIS/Kimberling
baseline, but what they add is mostly **negative discrimination**:

- Item 026 shows the anchor geometry is real and predictive on the matched corpus, but
  the correction alphabet does not stay bounded.
- Item 027 shows one-step schedule-independence up to axis swap, but the only strong
  schedule-independent observable is still the same anchor geometry.
- Item 028 shows bounded recent-prefix raw-witness explanations fail for structural
  reasons.
- Item 029 finds only a hypergraph near-miss, not a promoted invariant.
- Item 030 rejects small-modulus locking as a window-level mechanism.

This is real progress. It is not a new positive mechanism.

## Novelty Illusions

### 1. Structural cleanup can be oversold as mechanism

The theorem section is the strongest part of the paper, but its nearest source is still
the public recurrence itself. That makes it real novelty of a modest kind, not a new
mechanism paper by itself.

### 2. A proof of a public OEIS fact is not a new phenomenon

The prime-separation proposition matters because it upgrades a public observation into
an explicit proof. Novelty lives in the proof, not in discovering the phenomenon.

### 3. “Discriminative on the matched corpus” is not the same as “explains the process”

The matched-control language can still overread. The anchor score is highly
discriminative on the current bounded corpus, but Item 026 also shows the supposed
low-memory rule fails on held-out late records. That is negative evidence against a
compact mechanism, not a promoted positive explanation.

### 4. Hypergraph vocabulary alone does not clear the Ford overlap boundary

Renaming the witness system as a hypergraph or constrained-factorization object does
not create differentiation by itself. A promoted claim would need a graph-level
invariant or compression result that clearly survives matched non-record controls. The
current package does not have that.

### 5. The prefix obstruction should not be stated more broadly than the evidence

The repo does support a narrow obstruction: bounded recent-prefix raw-witness
certificates of the current border-ordered type fail because the anchor requires the
ancient factor `1`. It does **not** support the stronger wording that every bounded
certificate formalism is impossible.

### 6. More horizon is not a theorem surrogate

The million-step run, later records, and checker agreement improve credibility and
finite-horizon evidence. They do not, by themselves, produce a mathematically stronger
claim than “better audited evidence around the same open problem.”

## Missing Gap Evidence

The current package still lacks the evidence needed to claim broad material distinctness
for the stronger version of the manuscript.

### 1. No decisive separation from Ford-style local coverage

There is still no theorem or invariant showing that late-gap witness structure depends
on endogenous mex coupling in a way that generic local divisor/product coverage cannot
mimic.

### 2. No promoted positive mechanism survives controls

The anchor lane fails bounded-support generalization, the hypergraph lane remains a
near-miss, the modular lane is nonpredictive, and the prime-support lane is explicitly
demoted.

### 3. No horizon-independent bridge to boundedness

Nothing in the present paper upgrades the finite-horizon audits into a proof-oriented
statement about boundedness or unboundedness.

### 4. The strongest `T`-specific invariant is still too thin

The previous-column anchor is real and theorem-backed, but it explains one value inside
each row gap while the rest of the interval remains heterogeneous.

## What Actually Survives

The materially defensible contribution is:

1. proof-level cleanup of several exact consequences of the public recurrence;
2. a proof of the public prime-separation observation from the recurrence itself;
3. a validated generator, replay digest, and bounded independent checker;
4. a matched-control negative-result package showing that the obvious compact-mechanism
   stories fail in specific ways.

That is enough for a narrow paper about structural clarification plus failed-mechanism
evidence. It is not enough for a broader novelty pitch.

## Recommendation

Keep the novelty statement ranked in this order:

1. exact structural cleanup of the recurrence;
2. proof of prime separation from the recurrence;
3. validated computation and audit infrastructure;
4. negative mechanism evidence against compact witness, prime-support, hypergraph, and
   modular stories.

Avoid claiming:

- a new frontier certificate;
- a differentiated prime-support mechanism;
- a promoted hypergraph rigidity law;
- a clean theorem-level escape from Ford's overlap branch;
- any implication that boundedness or unboundedness is now substantially closer to
  proof.

VERDICT: REVISE
