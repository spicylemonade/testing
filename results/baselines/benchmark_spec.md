# Benchmark Spec

## Scope

This file defines the matched non-CA baseline matrix for the `H1` lane. It is a planning artifact only until an exact verifier exists. No baseline may claim success using a proxy score or a permissive decoder.

## Shared Fairness Rules

Every promoted CA family and every baseline must use:

- the same exact decoder and exact score function;
- the same legal grid shapes in a given comparison block;
- the same `|X|` budget or the same explicit `X` alphabet when `X` is fixed;
- the same target nonzero-edge density band;
- the same exact-decode budget.

For the first gate, the budget envelope is:

- at most `3` H1 rule families;
- at most `10^3` exact decodes per family;
- therefore at most `10^3` exact decodes per baseline family per comparison block.

## Matched Budgets

### Exact-decode budget

- Each baseline receives exactly the same number of exact witness evaluations as the CA family it is compared against.
- If the CA family uses `N` exact decodes on a grid block, the baseline also gets `N`.

### Alphabet budget

- If the CA family fixes `X`, each baseline must use that same `X`.
- If the CA family searches over `X`, the baseline must use the same allowed `|X|` range and the same legality rule `a+b != 0` for nonzero labels.

### Edge-density budget

- Let `rho = m(G) / n(G)` for a decoded witness.
- Each baseline must target the same density band as the CA family on the same grid block.
- For the tiny-grid gate, use a comparison band of `rho_target +/- 10%` relative error unless the CA family already has a tighter fixed density.

## Baseline Matrix

### Baseline A: Random Local Search

- Proposal type:
  - randomly sample legal local edits to a witness parameterization while staying within the matched `|X|` and density budget.
- Purpose:
  - tests whether simple local perturbation already matches the CA signal.
- Fairness condition:
  - no learned rule, no extra decoder logic, and no extra exact decodes.

### Baseline B: Whole-Witness Mutation

- Proposal type:
  - mutate the six-line witness as a whole: modify `X`, `d`, the `f_i` dictionaries, `T`, and singleton-supported `R` entries directly.
- Purpose:
  - checks whether the CA framing is doing anything beyond generic search over the same witness space.
- Fairness condition:
  - mutations must obey the same legality filters and the same exact-decode budget as the CA family.

### Baseline C: Decoder-Matched Search

- Proposal type:
  - keep the same compiler or decoder interface as `H1`, but replace the CA generator with non-CA proposal mechanisms such as random symbolic templates or direct parameter search.
- Purpose:
  - isolates whether the arithmetic content sits in the decoder rather than in the CA rule.
- Fairness condition:
  - the decoder, extractor, legality checks, and exact scorer must be identical to those used by the CA lane.

## Reporting Requirements

Each comparison block must report:

- legality hit rate:
  - fraction of proposals that decode to legal witnesses;
- forcing hit rate:
  - fraction of legal witnesses that pass exact forcing verification;
- best verified score;
- median verified score;
- full score distribution:
  - at minimum count, min, median, quartiles, max;
- failure-reason distribution:
  - illegal `X`, malformed `f_i`, malformed `R`, failed forcing, denominator failure, or other explicit category.

Best-of-many only reporting is forbidden.

## Comparison Blocks

Each baseline must be compared against the same CA family on:

- the same tiny legal `d_1 x d_2` or `d_1 x d_2 x d_3` grids;
- the same alphabet or `|X|` budget;
- the same density target;
- the same decode count.

If held-out larger or different-aspect-ratio grids are used for `H1`, the decoder-matched baseline must also be evaluated there.

## Negative Controls Built Into The Matrix

- label-shuffle control:
  - keep geometry and nonzero-label multiset fixed, shuffle labels in `X`, and rerun;
- decoder-matched control:
  - same decoder, different non-CA proposal mechanism;
- out-of-distribution control:
  - larger or different-aspect-ratio grids under the same decode budget;
- complexity sweep:
  - small-, medium-, and unrestricted-complexity `X` regimes.

## Current Status

The benchmark matrix is frozen for audit, but execution remains blocked until a real exact verifier is available.
