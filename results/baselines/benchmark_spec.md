# Benchmark Specification

This file freezes the matched baseline matrix for the first exact-verification pass. No runs are authorized yet because `results/verification/verification_summary.md` records that the exact verifier is missing.

## Shared Evaluation Budget

- Active lane only: `H1`
- Tiny-grid scope only:
  - `d_1 x d_2` and `d_1 x d_2 x d_3`
  - no larger grids before the first audit
- Exact-decode budget:
  - at most `10^3` exact decodes per CA family
  - every baseline receives the same exact-decode budget per matched condition
- Family count:
  - at most `3` H1 rule families before review
  - each baseline must be evaluated on the same grid set, alphabet budget, and decode budget

## Shared Structural Budgets

- Same legal alphabet class:
  - matched `|X|`
  - matched rational-complexity regime
  - matched prohibition on nonzero `(a,b)` with `a+b=0`
- Same graph-shape budget:
  - matched `d`-shape family
  - matched number of stages `k`
- Same density budget:
  - matched nonzero `f_i` density
  - matched initial `|R|` and `|T|` budget range
- Same decoder:
  - identical legality filter
  - identical exact score accounting
  - no repair on any method

## Required Non-CA Baselines

### Baseline A: Random Local Search

- Representation:
  - sample legal `X`, `d`, `f_i`, `R`, and `T` directly in the same witness encoding.
- Search move:
  - local random edits to one coordinate block, one edge label, one seed element of `R`, or one vertex in `T`.
- Purpose:
  - tests whether any apparent CA gain is better than plain local mutation under the same verifier.

### Baseline B: Whole-Witness Mutation

- Representation:
  - same full witness encoding as the CA output target.
- Search move:
  - mutate whole witness objects between decodes, including stage counts, grid sizes, label sets, and sparse-support seeds.
- Purpose:
  - controls against the claim that the CA is only helping because the space has a convenient global encoding.

### Baseline C: Decoder-Matched Search

- Representation:
  - same compiler/extractor path that would decode CA states into `(X,G,R,T)`.
- Search move:
  - replace the CA with a non-CA proposal mechanism, such as iid proposal sampling, coordinate descent, or beam mutation over the same decoded object.
- Purpose:
  - isolates whether the decoder or compiler contains the real arithmetic content.

## Optional Negative Controls

- Label-shuffled geometry control:
  - keep graph geometry and nonzero-label multiset fixed, shuffle the label assignment in `X`.
- Background-only control for sparse-defect stories:
  - reserved for `H2` only if opened later.

## Required Reporting

For every method-condition pair, report:

- total exact decodes attempted
- number of legal decodes
- hit rate for any prespecified threshold event
- full score distribution over legal decodes
- median verified score
- quartiles or equivalent distribution summary
- best verified score
- failure-mode histogram:
  - illegal `X`
  - malformed dictionaries
  - forcing failure
  - denominator failure
  - verifier rejection for any other reason

Best-of-many reporting alone is forbidden.

## Compute-Parity Rules

- Same wall-clock cap is not enough; parity is defined by exact-decode count.
- If a method generates many illegal candidates before decode, those failures still count against its budget.
- Any caching, warm start, or curriculum advantage given to the CA must also be available to the non-CA decoder-matched baseline or be reported as asymmetry.

## Why This Matrix Is Frozen Before Runs

- It prevents post hoc baseline weakening.
- It keeps the first audit focused on exact verified score rather than proxy metrics.
- It makes the missing-verifier blocker explicit: the matrix exists, but execution remains closed until an exact evaluator is available.
