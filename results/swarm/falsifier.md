# Falsifier Memo

## Scope

Adversarial pass on the active hypothesis family for the prime-separator array with
`T(1,1) = 1`. The goal here is not to invent a new mechanism. It is to enumerate the
fastest ways the current claims fail, the nearest prior-art branches that make weak
claims look derivative, and the missing controls that would invalidate any stronger
story.

## Bottom Line

The easiest attack is no longer "boundedness is probably false." The easier and much
stronger attack is this:

- OEIS `A129258`, OEIS `A129259`, and Kimberling already define the object, state the
  prime split, and pose the bounded-difference question.
- The current repo evidence still does not separate a positive mechanism claim from
  Ford-style local divisor/product coverage.
- The latest internal evidence is already mostly negative:
  - strong-form `H1` fails on the stored corpus;
  - current-form `H2` adds no explanatory power;
  - `H3` remains overlap-heavy and should stay demoted.

So the current package survives best as a validated negative-result dossier around an
open problem, not as a new bounded-gap mechanism.

## Fastest Failure Modes By Hypothesis

### 1. H1: Frontier witness certificates

Weak claim:
- Long first-row gaps are controlled by a compact witness language specific to the
  mex-coupled border sets.

Fastest falsifier:
- The chosen-witness corpus already points the wrong way, and the million-step
  extension makes that worse rather than better.
- Beyond the old 30k horizon, the baseline adds record gaps `25`, `28`, and `30`.
  Across `21 -> 30`, singleton share falls from `16/20` to `19/29`, while the
  `min factor > 100` bucket rises from `3/20` to `13/29`.
- Full-witness hypergraphs do not rescue the story. Gap `30` has `29` skipped values
  but only `43` admissible witness pairs, using `39` distinct row factors and `41`
  distinct column factors. That is weak reuse, not compression.

Why this will be accused of rehashing prior art:
- If the claim reduces to "the skipped interval is covered by local products from
  `A_n B_n`," it is too close to multiplication-table / divisor-in-an-interval
  language.
- If the claim is only that every skipped value has some local factor pair, it is
  nearly a restatement of the mex rule.

What would invalidate a weak H1 claim immediately:
- no matched non-record-window baseline;
- no size-matched surrogate product-set or hypergraph baseline;
- no recomputation of the headline taxonomy from full hypergraphs under multiple witness
  canonicalizations;
- no explanation of why Ford-style local coverage does not already subsume the claim.

Current adversarial verdict:
- Strong H1 is rejected on the stored corpus.
- The only live rescue route is a full-hypergraph invariant that beats surrogate and
  non-record controls. That rescue route is not yet evidence; it is only the last
  unfailed test.

### 2. H2: Prime-support fixed point

Weak claim:
- The row/column prime split or prime-support state controls when large row-1 gaps
  appear.

Fastest falsifier:
- Composite-only record gaps already kill any prime-obstruction narrative.
- In the baseline run, record gaps `17`, `20`, `21`, `28`, and `30` contain zero
  skipped primes.
- In the axis-swapped run, late row gaps `20`, `21`, `23`, `26`, and `31` are also
  composite-only.
- The current H2 claim sheet already says the support counts add no explanatory power
  beyond direct witness logs, and the later corpus only strengthens that negative read.

Why this will be accused of rehashing prior art:
- OEIS already records the prime split.
- A paper that mostly repackages the prime split, prime counts, or support imbalance is
  just retelling a public observation.
- A paper that drifts into ordinary prime-gap heuristics misses the empirical fact that
  the skipped intervals can be entirely composite.

What would invalidate a weak H2 claim immediately:
- any story that does not explain composite-only late records;
- any story whose predictive state variables stay as smooth background counts;
- any story that does not beat direct witness data on the same corpus.

Current adversarial verdict:
- Current-form H2 is rejected.
- Reopening it without a materially sharper state variable is budget waste.

### 3. H3: Near-minimal multiplicative basis

Weak claim:
- The border sets form a canonical sparse multiplicative basis, so unbounded gaps or
  asymptotic behavior should follow.

Fastest falsifier:
- This is the most overlap-heavy lane in the whole project.
- Without a `T`-specific invariant that uses the mex coupling essentially, the claim is
  just a reformulation inside the multiplication-table / multiplicative-basis branch.

Why this will be accused of rehashing prior art:
- Ford already owns the nearest multiplication-table branch.
- Pach-Sandor and related multiplicative-basis papers already own the sparse-basis
  branch.
- Asymptotic curve fitting or density narration without a theorem-level invariant is
  not differentiation.

What would invalidate a weak H3 claim immediately:
- no theorem or proof-oriented obstruction tied to the mex coupling;
- no explanation of why the argument is not generic sparse product-set behavior;
- any reliance on the current "variant" runs as if they were real robustness ablations.

Current adversarial verdict:
- Keep H3 de-prioritized.
- Treat it as overlap control, not as an active claim.

## Missing Controls

These are the controls whose absence most directly weakens the current package.

### 1. No independent implementation baseline

- The million-step repeats show determinism of one generator family, not protection
  against shared logic errors.
- A publication-quality claim needs a separately written checker that agrees with the
  baseline through at least a substantial prefix.

### 2. No generic null or surrogate baseline

- There is still no matched surrogate product-set or witness-hypergraph control.
- Without that control, "mex-specific structure" is not separated from generic local
  divisor/product coverage.

### 3. No matched non-record-window baseline

- Prime-free intervals, singleton-heavy coverage, balanced-factor growth, and the
  one-point axis marker are summarized on record gaps only.
- Without matched non-record windows, those features are not yet discriminative.

### 4. No real robustness ablation

- `row_immediate` collapses to the baseline on the stored observables.
- `column_immediate` is the axis swap, not an independent nearby mechanism.
- The repo still lacks the falsifier-requested controls:
  - a same-snapshot explicit tie-rule control;
  - a real admissibility perturbation that changes coverage rather than just axis order.

### 5. Chosen-witness summaries are canonicalization-sensitive

- The generator stores the first witness it encounters for each skipped value.
- The tiny/balanced/signature summaries are then computed from that chosen witness.
- Those summaries are informative, but not yet canonical.

### 6. Full-hypergraph validation is selective

- Full witness exports exist for selected late gaps, not every late record gap and not
  matched non-record windows.
- That is enough to sharpen the negative result, but not enough to close the structural
  question completely.

### 7. Claim sheets are stale relative to the current corpus

- The public H1/H2 sheets still stop at gaps `13`, `17`, `19`, `20`, `21`.
- The current baseline reaches `25`, `28`, `30`, and the axis-swapped run reaches row
  gap `31`.
- Any memo that still bottoms out at `21` is stale.

## Benchmark Traps

- Treating `10^6` deterministic repeats as an independent correctness check.
- Treating `row_immediate` and `column_immediate` as genuine robustness evidence.
- Treating chosen-witness histograms as canonical rather than witness-order-sensitive.
- Treating "more horizon" as novelty.
- Treating distinct-product counts as evidence of local frontier coverage.
- Treating prime statistics as decisive after composite-only late record gaps already
  exist.

## Novelty Illusions

- Recomputing OEIS terms is not novelty.
- Repeating "every prime lies on exactly one axis" is not novelty.
- Restating Kimberling's bounded-difference question is not novelty.
- Rebranding local frontier coverage as a multiplication-table story is not novelty.
- Rebranding the process as a sparse multiplicative basis is not novelty.
- Re-encoding the witnesses in prime-support or valuation language is not novelty unless
  it yields a theorem, a disproof-quality obstruction, or a sharper predictive failure
  mode than direct witness logs already give.

## Literature Branches That Would Invalidate Weak Claims

### Mandatory provenance floor

- OEIS `A129258`
- OEIS `A129259`
- Kimberling's live unsolved-problem page for the prime-separator array

Consequence:
- Any paper whose payload is "define the array, note the prime split, list more terms,
  and re-ask bounded or not" is rehashing public baseline material.

### Main overlap branch

- Ford, *The multiplication table problem*
- Ford, *The distribution of integers with a divisor in a given interval*
- Ford, *Integers with a divisor in (y, 2y)*
- Koukoulopoulos, generalized/restricted multiplication-table work

Consequence:
- Any argument based on local product density, restricted product sets, or short-interval
  divisor coverage must state exactly what survives after direct comparison with this
  branch.

### Multiplicity / concentration branch

- Ford-Tenenbaum on integers with at least two divisors in a short interval
- Ford-Green-Koukoulopoulos on concentration-of-divisors behavior

Consequence:
- Any claim built around singleton witnesses, low multiplicity, or clustered witness
  behavior risks being generic divisor-concentration language unless it uses the
  mex-coupled border geometry essentially.

### Multiplicative-basis branch

- Pach-Sandor and related multiplicative-basis literature

Consequence:
- Any near-minimal-basis story without a `T`-specific invariant is derivative.

### Greedy-sequence branch

- Odlyzko-Stanley and related greedy-sequence work

Consequence:
- If the pitch degrades into "another curious mex/greedy process," it is already in an
  established lane and still lacks differentiation on the exact object.

## Specification And Citation Hygiene Traps

- The load-bearing implementation trap is update order:
  - choose `T(1,n+1)` from the old square;
  - choose `T(n+1,1)` from that same old square, excluding only the just-chosen row
    term;
  - only then add the new products.
- Any implementation that lets new products influence `T(n+1,1)` is the wrong process.
- Citation hygiene matters here because the exact object is so close to public baseline
  material. The live Kimberling source is currently an itemized unsolved-problem page;
  if numbering or page identity is cited loosely, that is an avoidable credibility hit.

## Adversarial Acceptance Bar

I would reject any positive mechanism paper that fails any of the following:

- it does not step clearly beyond OEIS/Kimberling provenance;
- it does not separate itself from Ford-style local coverage;
- it relies on prime assignment after composite-only record gaps already exist;
- it treats the current variants as robustness evidence;
- it uses chosen-witness summaries as if they were canonical;
- it lacks matched non-record and surrogate/null controls.

The current package is defensible only in the narrower form:

- validated recurrence implementation;
- reproducible finite-horizon computation through baseline gap `30`;
- direct negative evidence against strong raw-witness H1;
- direct negative evidence against current-form H2;
- a carefully delimited overlap-control dossier explaining why stronger positive claims
  are not yet earned.
