# Novelty Report

## Scope

This report evaluates whether the current package is materially distinct from the
known prior-art boundary already recorded in:

- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/claims/h1_frontier_witness_certificate.md`
- `results/claims/h2_prime_support_fixed_point.md`
- `results/evaluation/literature_comparison.md`

The controlling question is not whether the repo now has more computation than the
public OEIS baseline. It does. The question is whether the surviving claims clear
named prior art by enough margin to count as a materially new mechanism rather than
better instrumentation around an old open problem.

## Executive Assessment

The package is **not** materially distinct if framed as a new positive mechanism for
the first-row gap behavior of the prime-separator array.

It is materially narrower and more defensible if framed as:

- a validated computational baseline for the correct recurrence;
- a witness-carrying negative result against the original compact-certificate
  hypothesis;
- an overlap-control dossier explaining why overclaiming would collapse into the Ford
  multiplication-table / divisor-in-an-interval branch.

That is a real contribution, but it is not the same contribution as a new mechanism,
new theorem, or new proof program.

## Claim-By-Claim Prior-Art Comparison

| major claim | closest prior art | distinctness assessment |
|---|---|---|
| The array, recurrence, and prime-separator framing are novel or newly established. | OEIS `A129258`. | Not distinct. This is baseline provenance only. The generator in `scripts/prime_separator.py` correctly reconstructs the object, but reconstruction is not novelty. |
| The first-row sequence and bounded-difference question are newly posed or substantially reframed. | OEIS `A129259`; Clark Kimberling, *100 Conjectures and/or Problems*. | Not distinct. The public problem statement already exists. The repo adds stronger finite-horizon evidence, not a new statement of the problem. |
| `H1_frontier_witness_certificate`: long record gaps admit a compact, endogenous witness certificate. | Kevin Ford, *The multiplication table problem*; Kevin Ford, *The distribution of integers with a divisor in a given interval*. | Weakly differentiated at best, and currently not sustained. The present witness story remains too close to generic local product/divisor coverage unless mex coupling yields an essential certificate. The current corpus does not show that. |
| `H2_prime_support_fixed_point`: the row/column prime-support split explains record-gap behavior. | OEIS `A129259` / Kimberling provenance for the prime split. | Not distinct in its current form. The split is already public, and the repo’s own evidence shows the support observables do not explain anything that the direct witness logs do not. |
| Full witness hypergraphs or factorization exports rescue the mechanism claim. | Closest line of work: Ford-style local coverage, now expressed with richer factorization instrumentation. | Potentially distinct as data infrastructure, not yet distinct as mathematics. The hypergraph export validates multiplicities and sharpens the negative result, but no low-description invariant or compact certificate has been isolated. |
| Million-step baseline and nearby perturbation runs establish a novel mathematical conclusion. | Closest line of work: computational extension of the OEIS/Kimberling object. | Distinct as reproducible computation, not as mathematical novelty. The runs strengthen the evidence package, but they do not prove boundedness, unboundedness, or a new mechanism. |

## Closest-Overlap Findings

### 1. Provenance baseline is already occupied

The repo does not clear novelty by restating the object. `A129258` already defines the
prime-separator array, and `A129259` plus Kimberling already publicize the first-row
sequence and the bounded-difference question. The baseline generator is valuable only
because it validates the recurrence order and turns the public object into a
reproducible experiment package.

### 2. H1 sits directly on the Ford overlap boundary

`results/literature/prior_art_gap.md` correctly identifies Ford's multiplication-table
and divisor-in-an-interval work as the live overlap hazard. That judgment is borne out
by the experiment artifacts:

- `results/claims/h1_frontier_witness_certificate.md` rejects the strong H1 claim.
- `results/experiments/run_1000000/experiment_note.md` shows late record gaps remain
  low-multiplicity and increasingly balanced rather than compressing into a small
  witness grammar.
- `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json` shows that gap `30`
  has `29` skipped values, `43` admissible witness pairs, `39` distinct row factors,
  and `41` distinct column factors.

That is an overlap signal, not a separation signal. It looks like heterogeneous local
factor coverage near a frontier, which is exactly the kind of story that risks
collapsing into Ford-style product/divisor coverage unless the mex-coupled generation
is shown to be mathematically essential.

### 3. H2 does not clear even the provenance baseline

The prime-support line is weaker than H1 from a novelty standpoint. The prime split is
already part of the public framing, and `results/claims/h2_prime_support_fixed_point.md`
shows that the support observables add no explanatory power beyond the direct witness
corpus.

The most damaging overlap signal is conceptual, not bibliographic: composite-only
record gaps already occur in the shared corpus and persist at larger horizons, so the
prime-support line does not even isolate the events it is supposed to explain.

### 4. The hypergraph export improves evidence quality, not distinct mechanism content

The full-witness export is a legitimate technical improvement because it validates that
the stored multiplicities match the full admissible factor-pair set on selected late
gaps. But this is still an evidentiary upgrade, not a novelty rescue, because the
resulting hypergraphs have not yet yielded a compact invariant that size-matched
generic local product sets would fail to show.

## Novelty Illusions

The current package is especially vulnerable to the following novelty illusions.

### 1. Recomputing OEIS is not novelty

Correctly regenerating the array and pushing farther than a public term dump is useful,
but it does not create new mathematics on its own.

### 2. Restating the prime split is not novelty

Any H2 framing that mainly says "the primes divide across the two axes" is repeating
public provenance unless it predicts gap behavior better than the witness logs. The
current package does not.

### 3. "Covered interval in `A_n B_n`" is not enough

That statement is close to a restatement of the recurrence plus generic local product
coverage. Without a mex-specific certificate or obstruction, the work reads as renamed
multiplication-table / divisor-in-an-interval language.

### 4. Hypergraph vocabulary alone does not create differentiation

Renaming witnesses as hypergraphs or constrained factorizations does not clear prior
art unless the graph-level description compresses the intervals in a way that ordinary
local product sets do not.

### 5. More finite-horizon data does not settle the mathematics

The million-step run and nearby variants kill small-gap optimism, but they do not prove
boundedness or unboundedness. Any novelty claim that treats horizon growth as a theorem
surrogate would overstate the record.

## Missing Gap Evidence

The current package still lacks the evidence needed to claim material differentiation as
a positive mechanism paper.

### 1. No decisive separation from Ford-style local coverage

There is no proof, invariant, or compression result showing that the witness behavior
depends on the endogenous mex coupling in a way that generic divisor/product coverage
cannot mimic.

### 2. No compact interval-wide certificate for H1

The only stable T-specific motif is the one-point axis-1 marker at the previous column
term. That is too thin to explain the rest of each interval.

### 3. No predictive observable for H2

The prime-support state is measurable, but nothing in the current record shows that it
predicts when record gaps appear or why composite-only record gaps arise.

### 4. No horizon-independent bridge

The package has no theorem, no disproof-quality obstruction, and no horizon-independent
invariant that upgrades finite computation into a mathematical conclusion.

### 5. No ablation against generic surrogate product sets

The repo has not yet shown that the observed witness/hypergraph structure is more
compressible or more regular than size-matched surrogate product sets without mex
coupling. Without that control, distinctness remains unproven.

## What Survives As A Real Contribution

What survives novelty scrutiny is narrower than the original champion hypothesis:

- a correct, validated generator for the OEIS/Kimberling object;
- a reproducible million-step evidence package with witness logs and selected full
  hypergraph exports;
- a negative result showing that the raw-witness H1 story does **not** compress into a
  compact certificate language on the current corpus;
- a documented overlap argument explaining why the obvious positive story is too close
  to Ford's multiplication-table / divisor-in-an-interval branch.

That is a real contribution if presented honestly as a negative-result and
overlap-control package. It is not a materially distinct positive mechanism claim.

## Recommendation

Revise the contribution statement to say explicitly:

- provenance belongs to OEIS / Kimberling;
- the main mathematical overlap branch is Ford;
- the repo contributes validated computation and negative mechanistic evidence;
- H1 survives only as a narrowed hypergraph-compression rescue question;
- H2 is not a differentiated mechanism.

Do **not** present the current package as discovering a new frontier certificate, a
prime-support mechanism, or a theorem-level explanation of the gap process.

Verdict: REVISE
