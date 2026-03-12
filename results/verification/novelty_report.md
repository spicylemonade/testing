# Novelty Report

## Scope

This round checks whether the current manuscript and code package are materially
distinct from the closest prior art already identified in:

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/claims/h1_frontier_witness_certificate.md`
- `results/claims/h2_prime_support_fixed_point.md`
- `research_paper.tex`
- `scripts/prime_separator.py`

The review standard is narrow: compare the paper's actual major claims against the
nearest named source or line of work, then decide whether the claimed contribution is
really differentiated or mostly provenance recovery, recurrence unpacking, or better
instrumentation around an existing open problem.

## Executive Assessment

The package clears the novelty bar only in a **narrow** form:

- as a careful theorem-and-artifact cleanup of Kimberling's recurrence;
- as a validated finite-horizon computation package;
- as a negative-result dossier showing that the strongest witness-mechanism story does
  not survive contact with the stored corpus.

It does **not** clear the novelty bar if framed as:

- a new positive mechanism for record-gap formation;
- a differentiated prime-support explanation;
- a theorem-backed separation from Ford-style local divisor/product coverage;
- a mathematical resolution of the bounded-difference problem.

So the manuscript is not empty, but its differentiated core is materially smaller than
the strongest rhetorical version of the contribution statement. The required action is
to revise the claim hierarchy, not to pretend the whole package is novel in the same
sense.

## Claim-By-Claim Comparison

| major claim | closest prior art or line | assessment |
|---|---|---|
| The array, recurrence, and prime-separator framing are established here. | OEIS `A129258`. | Not novel. This is public provenance. The repo reconstructs and validates the object; it does not originate it. |
| The first-row sequence and bounded-difference question are newly posed or meaningfully reframed. | OEIS `A129259`; Clark Kimberling, *100 Conjectures and/or Problems*. | Not novel. The public problem statement already exists. Extending the computational horizon is evidence, not a new conjectural frame. |
| The exact "first two missing values" formulation, strict interleaving, unique column inside each row gap, and exact variant identities are the paper's main theoretical addition. | Closest line: direct consequences of the OEIS/Kimberling recurrence itself. No stronger external overlap source is named in the current watchlist. | Distinct but modest. These statements look genuinely absent from the current public provenance record, but they are still low-distance structural consequences of a public greedy recurrence, not a new mechanism or external comparison theorem. |
| Every prime lies on exactly one axis is a new phenomenon. | OEIS `A129258` / `A129259`, which already state the prime-separation observation. | Weakly distinct only as a proof of a known observation. The fact is public; the manuscript's contribution is giving a direct recurrence proof. That is real but should not be sold as discovery of a new effect. |
| The forced axis-1 witness inside each row gap materially differentiates the project. | Closest line: the same recurrence geometry, plus OEIS prime-separator provenance. | Thin differentiation only. This is a real T-specific invariant, but it explains exactly one point per interval. On its own it is too small to support a broader mechanism claim. |
| `H1_frontier_witness_certificate`: late gaps admit a compact mex-coupled witness certificate. | Kevin Ford, *The multiplication table problem*; Kevin Ford, *The distribution of integers with a divisor in a given interval*. | Not presently differentiated as a positive claim. The claim sheet itself says the strong form fails, and the remaining witness picture still resembles heterogeneous local product coverage more than a compact T-specific certificate. |
| Full witness hypergraphs rescue H1. | Closest line: Ford-style local coverage with richer factorization instrumentation. | Distinct as evidence infrastructure, not as mathematics. The exports validate multiplicities and sharpen the negative result, but they do not isolate a low-description invariant that generic local product sets would fail to show. |
| `H2_prime_support_fixed_point`: prime-support asymmetry explains record gaps. | OEIS/Kimberling prime-split provenance; backup claim family in `results/claims/h2_prime_support_fixed_point.md`. | Not differentiated. The asymmetry is measurable, but the repo's own sheet says it adds no explanatory power beyond the witness logs and fails on composite-only record gaps. |
| The million-step baseline and variant runs establish a novel mathematical conclusion. | Closest line: computational extension of the OEIS/Kimberling object, plus local repo validation work. | Distinct as reproducible computation and code validation, not as new mathematics. The runs extend the finite record, but they do not prove boundedness, unboundedness, or a new mechanism. |

## Closest-Overlap Findings

### 1. Provenance is already occupied

OEIS `A129258` already gives the array and recurrence, and its comments already record
the prime-separation phenomenon. OEIS `A129259` and Kimberling's problem page already
state the first-row sequence and ask whether the differences are bounded. That means:

- reconstructing the array is not novelty;
- restating the prime split is not novelty;
- restating the bounded-gap question is not novelty.

The paper is only differentiated to the extent that it proves additional structural
facts or supplies better evidence than those public sources.

### 2. The real novelty pressure point is not the recurrence lemmas; it is H1

The manuscript's structural lemmas are not the main overlap risk. Their nearest source
is the public recurrence itself. The main risk is the witness-mechanism story. Both
`results/literature/prior_art_watchlist.md` and `results/literature/prior_art_gap.md`
correctly identify the Ford multiplication-table / divisor-in-an-interval branch as
the active boundary. That remains correct after reading the paper.

Why:

- the skipped values are still explained by local border-factor pairs;
- witness multiplicity stays sparse rather than exploding into a distinctive internal
  grammar;
- balanced factors become more common as record gaps grow;
- nothing yet shows that the mex-coupled generation creates a certificate unavailable
  in generic local product coverage.

This means the paper survives best when H1 is treated as a failed strong hypothesis,
not as the source of novelty.

### 3. H2 is weaker than H1 from a novelty standpoint

The H2 sheet is explicit: prime-support observables are measurable but non-explanatory.
That is damaging for novelty in two ways.

- The fact pattern is already public enough that a mere prime-split restatement does
  not differentiate the work.
- The surviving observables do not predict the main events of interest, because large
  record gaps can be composite-only.

So H2 does not just fail as a mechanism; it fails to clear even a modest novelty bar.

### 4. The hypergraph layer improves auditability more than differentiation

The full witness exports are useful. They confirm that stored multiplicities match the
full admissible factor-pair set on selected late gaps and remove some chosen-witness
bias from the record. But the main conclusion of that richer layer is still negative:

- gap `21`: `20` skipped values, `32` full witness pairs, `31` distinct row factors,
  `30` distinct column factors;
- gap `25`: `24` skipped values, `31` full witness pairs;
- gap `28`: `27` skipped values, `36` full witness pairs;
- gap `30`: `29` skipped values, `43` full witness pairs, `39` distinct row factors,
  `41` distinct column factors.

Those counts reinforce sparsity and heterogeneity. They do not yet reveal a compressed
T-specific invariant. So this layer strengthens the negative result, not the novelty
of a positive mechanism.

## Novelty Illusions

### 1. Direct recurrence unpacking can look deeper than it is

The exact structural section is the most defensible part of the paper, but it is easy
to oversell. The lemmas are real, yet they are close to the public recurrence. Calling
them a new mechanism would overstate their distance from provenance.

### 2. A proof of a known OEIS observation is not the same as a new phenomenon

The prime-separation proposition is worthwhile because it turns an observed fact into a
short theorem. But the phenomenon itself is already part of the public OEIS framing.
Novelty lives in the proof, not in the fact.

### 3. Negative evidence is not a hidden positive mechanism

The witness data are strongest where they reject the compact-certificate story. Trying
to convert that negative result into an implicitly positive mechanism claim would be a
novelty illusion.

### 4. Hypergraph vocabulary alone does not clear Ford

Renaming the witness system as a hypergraph or constrained factorization object is not
enough. Differentiation requires a graph-level invariant or compression result that is
specific to the mex-coupled process. The current package does not have that yet.

### 5. Variant runs are symmetries, not extra novelty

The manuscript correctly proves that `row_immediate` is the same recurrence and
`column_immediate` is the axis swap. That is a useful cleanup. But once proved, those
runs stop being robustness evidence and become consistency checks. They should not be
counted twice as mathematical novelty.

### 6. More horizon is not a theorem surrogate

The baseline run reaches record gap `30`, with late records `25`, `28`, and `30`. That
matters empirically. It does not by itself create a materially new mathematical claim
about boundedness.

## Weak Differentiation Signals

These are the places where the manuscript still looks too close to known territory.

### 1. The H1 sheet already retracts the strong claim

`results/claims/h1_frontier_witness_certificate.md` says the strong compact-certificate
form fails. That makes any remaining positive H1 rhetoric suspect unless it is clearly
downgraded to "failed mechanism, surviving one-point invariant."

### 2. The H2 sheet already demotes itself

`results/claims/h2_prime_support_fixed_point.md` explicitly says the prime-support
layer adds no explanatory power beyond H1. Any novelty pitch that still treats H2 as a
backup mechanism overstates the record.

### 3. The computational package is strong as verification, not separation

The generator, digest checks, and million-step replay make the artifact set credible.
They do not separate the mathematics from Ford-style overlap on their own.

### 4. The multiplicative-basis fallback is not a rescue path

The de-prioritized H3 lane remains too close to existing multiplicative-basis and
restricted multiplication-table literature. Without a genuinely `T`-specific
invariant, reviving that branch would read as rebranding rather than differentiation.

### 5. The strongest T-specific invariant is still too thin

The unique axis-1 witness is real and theorem-backed, but it covers one value per gap.
The rest of the interval remains heterogeneous. That is not enough differentiation for
a broad mechanistic claim.

## Missing Gap Evidence

The package still lacks the evidence needed to claim material distinctness for the
stronger version of the paper.

### 1. No decisive separation from Ford-style local coverage

There is still no theorem, invariant, or controlled comparison showing that the late
gap witness structure depends on endogenous mex coupling in a way that generic local
divisor/product coverage cannot mimic.

### 2. No compact interval-wide certificate

The witness system does not compress. In the late corpus the singleton share falls and
the balanced-factor share rises, which points away from a compact grammar.

### 3. No predictive H2 observable

The prime-support asymmetry does not explain why record gaps occur when they do and
does not distinguish prime-bearing from composite-only late gaps.

### 4. No comparative surrogate baseline

The repo still does not benchmark its witness and hypergraph summaries against matched
non-record windows or size-matched surrogate product sets. Without that control, the
paper cannot show that the observed structure is special rather than generic.

### 5. No horizon-independent bridge

Nothing in the present package upgrades finite-horizon behavior into a proof-oriented
statement about boundedness or unboundedness.

## What Actually Survives Novelty Review

The materially defensible contribution is:

- a proof-level cleanup of several exact consequences of the public recurrence;
- a proof of the public prime-separation observation from the recurrence itself;
- a validated generator and digest-checked million-step replay package;
- a negative computational result showing that the compact-certificate and
  prime-support mechanism stories do not currently survive the stored evidence;
- a disciplined overlap analysis explaining why the obvious positive framing drifts
  toward Ford-style local coverage.

That is enough for a narrower paper about structural clarification plus negative
evidence. It is not enough for a broad "new mechanism" paper.

## Recommended Reframing

The contribution statement should be ranked in this order:

1. Exact structural cleanup of the recurrence and update-order identities.
2. Proof of prime separation from the recurrence.
3. Reproducible million-step evidence package.
4. Negative witness/hypergraph result against compact-certificate optimism.

The statement should explicitly avoid claiming:

- a new frontier certificate;
- a differentiated prime-support mechanism;
- a theorem-level explanation of gap growth;
- a clean mathematical separation from Ford's overlap branch.

VERDICT: REVISE
