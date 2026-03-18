# Lane Gates

This file fixes the conditions under which the active lane `H1` is killed, the backup lane `H2` is allowed to open, and the reserve lane `H3` stays closed.

## 1. Global Gate

No lane may claim progress without:

- a fixed decoder that maps candidate state directly into legal `(X,G,R,T)`,
- exact forcing verification over `\mathbb{Z}`,
- exact score accounting `(m(G)+|R|)/(n(G)-|T|)`,
- and matched-budget controls.

If any of those are missing, phase-4 experimentation is blocked rather than relaxed.

## 2. H1 Kill Gates

Kill `H1` immediately if any of the following occur.

### A. Missing-verifier gate
- Observation: no exact integer verifier or exact decoder entry point is available.
- Action: `H1` becomes `blocked`, not promoted.
- Consequence: do not open `H2` or `H3` yet, because they inherit the same verifier dependency.

### B. Decoder-leakage gate
- Threshold: any candidate requires repair, support merging, label rewriting, inferred legality, or nonlocal postprocessing before it becomes a legal witness.
- Action: kill `H1`.
- Reason: the novelty would sit in the repair heuristic, not in the CA.

### C. Label-shuffle gate
- Test: keep geometry, edge density, and nonzero-label multiset fixed; shuffle the nonzero labels in `X`; rerun exact evaluation.
- Threshold: kill `H1` if shuffled runs retain either
  - at least `50%` of the unshuffled hit rate, or
  - at least `75%` of the unshuffled median score gain over the matched non-CA baseline.
- Reason: the family is exploiting geometry rather than arithmetic structure.

### D. Out-of-distribution gate
- Test: evaluate on held-out larger grids or different aspect ratios after the first exact gate opens.
- Threshold: kill `H1` if either
  - hit rate falls below `25%` of the in-distribution hit rate, or
  - the median verified-score gain over the matched non-CA baseline disappears on every held-out condition.
- Reason: the lane is memorizing one witness grammar.

### E. Bounded-slope / rational-complexity gate
- Test: run the small-, medium-, and unrestricted-complexity `X` regimes already fixed in `results/baselines/benchmark_spec.md`.
- Threshold: kill `H1` as bounded-slope trapped if
  - all verified improvements occur only in the `small` regime, and
  - no family beats the matched non-CA baseline in either the `medium` or `unrestricted` regime at the same decode budget.
- Reason: the lane would be living exactly in the low-complexity regime warned about by Tao (2025).

### F. First exact-gate stall
- Test budget: the first exact gate is the `item_016` sweep, namely at most `3` H1 families and at most `10^3` exact decodes per family on tiny legal grids.
- Threshold: kill `H1` if, after that full budget,
  - no family produces any verified witness beating the matched non-CA baseline best score, and
  - the verified hit-rate distribution is indistinguishable from the matched baselines.
- Reason: the champion lane failed its first budgeted exact test.

## 3. H2 Opening Gates

Open `H2` only if all of the following are true.

- The missing-verifier gate is cleared.
- The decoder-leakage gate is cleared.
- `H1` has been killed by the first exact-gate stall, the bounded-slope gate, or the out-of-distribution gate.
- The failure mode still leaves room for the sparse-defect hypothesis to differ materially from `H1`.

Do **not** open `H2` if `H1` is blocked only because the verifier is absent. That is a shared infrastructure blocker, not evidence for switching hypotheses.

## 4. H3 Reserve-Only Gates

Keep `H3` closed unless all of the following happen.

- The exact verifier exists.
- `H1` has failed cleanly under exact controls.
- `H2` has either failed or been ruled too derivative.
- There is a concrete abelian-network or flow-firing invariant that predicts exact forcing behavior better than raw graph depth, layer index, or edge density.

Without all four conditions, `H3` remains reserve-only.

## 5. Current State

As of this checkpoint:

- `H1`: active in design, blocked by the missing-verifier gate.
- `H2`: closed, because `H1` has not yet failed an exact gate.
- `H3`: closed, because no exact verifier or validated abelian invariant is available.

Therefore the correct next action is blocker-aware documentation, not lane expansion.
