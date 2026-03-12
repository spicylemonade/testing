# Falsifier Memo

## Scope

Adversarial pass on the likely hypothesis family around `A129258` / `A129259`: bounded first-row differences via frontier coverage, prime-side assignment, valuation-space structure, or larger computation.

## Bottom line

The easiest way to fail here is to mistake "interesting mechanism" for "new mathematics." OEIS already contains the construction, the prime-split observation, and the bounded-difference problem statement. A weak paper that mainly regenerates terms, plots gaps, or rephrases the mex rule will read like a gloss on Kimberling's open problem, not a contribution.

The easiest way to overclaim is to infer boundedness from small data. A local rerun of the greedy process already pushes the first-row record gap past the previously logged `17`:

- gap `19` at `38630 -> 38649` (step `8475`)
- gap `20` at `130699 -> 130719` (step `27676`)
- gap `21` at `139039 -> 139060` (step `29373`)

That last record interval has no skipped primes at all, and `16` of its `20` skipped values had only a single visible factor witness from the current border sets. So any story that leans on ordinary prime-gap heuristics or generic density language is immediately suspect: long row-1 jumps can arise with zero prime obstruction in the skipped block and with mostly brittle coverage.

## Fastest failure modes by hypothesis

### 1. Frontier-coverage / multiplication-table hypothesis

Weak form:
- "Large row-1 gaps come from covered intervals in `A_n B_n`."

Falsifier response:
- That is probably true but not new. It is almost a restatement of the recurrence.
- If the proof technology is "treat `A_n B_n` like a restricted multiplication table" without exploiting the endogenous way `A_n` and `B_n` are generated, the work risks collapsing into multiplication-table / divisor-in-interval folklore.
- If the argument only counts products or invokes average density, it misses the hard part: consecutive local coverage near the mex.

What would invalidate a weak claim:
- failure to distinguish local interval coverage from global distinct-product counts;
- failure to show why existing divisor-in-an-interval machinery does not already subsume the claimed mechanism;
- no witness-level analysis of how each skipped integer is covered.

### 2. Prime-side assignment hypothesis

Weak form:
- "Understanding which primes go to row 1 versus column 1 should control the gap sizes."

Falsifier response:
- This is the most tempting wrong abstraction.
- OEIS already records the prime split. Repackaging it is not novelty.
- Large record gaps do not need skipped primes. The `139039 -> 139060` gap is already a direct counterexample to a prime-obstruction narrative.

What would invalidate a weak claim:
- any proof sketch that treats `A129259` as a sparse prime subsequence with ordinary prime-gap heuristics attached;
- any claim that prime assignment alone controls row-1 jumps without accounting for composite coverage in `A_n B_n`.

### 3. Valuation-frontier / finite-state hypothesis

Weak form:
- "The process becomes simple in `v_p` coordinates, so boundedness should follow from a small-state frontier rule."

Falsifier response:
- This can turn into decorative language very quickly.
- Unless the valuation model predicts new gaps, forbids large ones, or yields a rigorous transition invariant, it is just a re-encoding.
- If the state space grows with the number of relevant primes, "finite-state" is probably illusory.

What would invalidate a weak claim:
- no theorem or falsifiable prediction beyond pattern description;
- no control showing that low-prime valuations actually dominate the frontier;
- no explanation for why high-prime effects can be truncated safely.

### 4. Compressed-computation hypothesis

Weak form:
- "We computed much farther, so the contribution is stronger."

Falsifier response:
- Computation is necessary here, but bigger term tables are not a mathematical result.
- A purely empirical paper is vulnerable unless it produces either a disproof-quality counterexample or proof-oriented artifacts such as reusable witness certificates for every skipped integer in each record gap.

What would invalidate a weak claim:
- longer plots without mechanistic diagnostics;
- runtime claims without a baseline generator and reproducible scaling profile;
- empirical claims about boundedness based on horizons that are too low to beat already observed record growth.

## Missing controls

### Empirical controls

- The current repo state had no reusable generator script. That is already a reproducibility risk.
- The previous swarm note stopped at record gap `17`; a modest extension already reaches `21`. Any narrative built on the earlier horizon is stale.
- Record-gap studies need witness logs, not just gap sizes. For each skipped integer in a record interval, store at least one factorization `u*v` with `u in A_n`, `v in B_n`.
- Prime/composite composition of skipped intervals must be logged. The latest record gap found here had no skipped primes, which is exactly the sort of control that can kill a bad heuristic early.

### Specification controls

- The recurrence for `T(n+1,1)` is easy to misread operationally: choose from the old `n x n` square, excluding the newly chosen row term, before adding new products. Any implementation should test this explicitly rather than assuming an equivalent update order.

### Robustness controls

- One trivial nearby control is already clear: reversing the order of choosing the two new axis terms just swaps the row-1 and column-1 border sequences. That is a label symmetry, not a robustness result.
- The meaningful controls are still missing. At minimum, compare:
  - the present rule;
  - a version that resolves the symmetric choice from the same snapshot with an explicit tie rule;
  - a version that perturbs the admissibility rule for covered integers without merely renaming the axes.

If a proposed mechanism disappears under tiny perturbations, then a broad heuristic explanation is probably false.

## Benchmark traps

- `5e3` border steps is not "deep asymptotics." It is barely enough to kill the small-constant guess.
- "No large gaps seen yet" is not evidence without a scalable generator. With a cheap optimized rerun, new records `19`, `20`, and `21` already appear by `3e4` steps.
- Distinct-product counts are a trap. Heavy multiplicative collisions mean that `|A_n||B_n|` says little about whether the frontier interval below the mex is saturated.
- Prime statistics are a trap. A long row-1 gap can be caused by composite coverage alone.

## Novelty illusions

- Recomputing OEIS terms is not novelty.
- Repeating "every prime lies on exactly one axis" is not novelty.
- Plotting gap growth or fitting heuristics to the first few thousand terms is not novelty.
- Translating the problem into "restricted multiplication tables" is not novelty unless the endogenous greedy structure is used in an essential way.
- Translating the problem into valuation space is not novelty unless it produces a theorem, a counterexample, or a testable obstruction that beats direct integer-space analysis.

## Prior-art overlap risks

### Direct provenance baseline

- `A129258`: the array itself.
- `A129259`: first row; comments already state the prime split and explicitly ask whether the first differences are bounded.
- Kimberling's AIM problem list already frames this as an open problem (`Problem 18` in the "100 conjectures" list).

Consequence:
- Any paper must treat OEIS + Kimberling as baseline prior art, not as a citation afterthought.

### Closest mathematical overlap branch

- The strongest overlap risk is with multiplication-table / distinct-product / divisor-in-interval literature.
- If the proposed proof argues that long row-1 gaps come from dense local factor coverage, then it is moving into the territory of:
  - Kevin Ford, "The distribution of integers with a divisor in a given interval";
  - Kevin Ford, "The multiplication table problem."

Consequence:
- If the paper uses divisor-density or product-set coverage language, it must state exactly what is new about the self-generated sets `A_n` and `B_n`.
- Otherwise the work can be accused of rebranding known divisor-in-interval phenomena inside an OEIS wrapper.

## Literature branches that should be cleared before making strong claims

- OEIS / Kimberling provenance: to avoid overstating novelty on the exact object.
- Multiplication-table literature: to avoid rediscovering generic product-set coverage heuristics.
- Divisor-in-an-interval literature: to avoid calling a standard divisor-density mechanism a new frontier certificate.
- Generic greedy / mex sequence literature: only if the argument becomes primarily one-dimensional or symbolic; otherwise this branch is secondary, not primary.

## Concrete sources to cite

- OEIS `A129258`
- OEIS `A129259`
- OEIS `A129259` comments and references noting:
  - every prime is in the first row or first column, but not both;
  - the bounded-difference question;
  - Kimberling's `Problem 18`
- Clark Kimberling, "100 Conjectures and/or Problems"
- Kevin Ford, "The multiplication table problem"
- Kevin Ford, "The distribution of integers with a divisor in a given interval"

## Adversarial acceptance bar

I would not accept a boundedness claim, or even a serious heuristic paper, unless it clears all of the following:

- proves something not already implicit in OEIS / Kimberling;
- does more than global density or prime-gap analogy;
- separates local frontier coverage from generic multiplication-table counting;
- shows why divisor-in-interval prior art does not already explain the claimed mechanism;
- uses computation as evidence with witness-carrying diagnostics, not term dumps.
