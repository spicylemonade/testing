# Falsifier Memo

## Current Claim Boundary

- The watchlist-derived "closest prior art" is malformed by LaTeX-token collisions and should not be used for novelty judgments.
- The active lane is verifier-blocked and benchmark-blocked. The repo state recorded in `results/verification/verification_summary.md`, `results/experiments/h1_tiny_grid_report.md`, `results/experiments/h1_controls.md`, and `results/experiments/complexity_sweep.md` is still: no shared exact `(X,G,R,T)` verifier or decoder in use, `0 / 3` H1 rule families evaluated, and `0` exact decodes.
- Therefore the only defensible claim boundary is narrow: verifier-coupled CA design plus blocker reporting. Any stronger claim such as "solved using cellular automata," "new arithmetic-Kakeya progress," or "benchmark-cleared CA advantage" is already falsified by the current repo evidence.

## Fastest Kill Criteria

- Kill any mathematical-progress claim if no exact legal six-line witness with score `<= 1.675` is produced. A CA search story without a legal witness is not arithmetic-Kakeya progress.
- Kill any empirical-method claim if there is still no shared exact decoder and verifier over `\mathbb{Z}`. Without exact score and forcing checks, the lane remains design-only.
- Kill `H1` if the fixed decoder, no-repair rule, or explicit `X`-registry discipline is relaxed. Then the arithmetic content sits in the decoder rather than in the CA.
- Kill `H1` if any apparent gain survives `X`-label shuffling at fixed geometry and fixed nonzero-label multiset. Then the method is exploiting geometry or density, not arithmetic structure.
- Kill `H1` if signal appears only for tiny fixed alphabets or low rational-complexity slope sets. That is the bounded-slope trap already flagged in the literature and in `results/literature/prior_art_gap.md`.
- Kill `H2` if sparse defects fail to beat both the clean recursive background and density-matched random defects under full score accounting `(m(G)+|R|)/(n(G)-|T|)`.
- Kill `H2` if the "defects" are just hand-inserted certificate patches, or if a defect type lacks bounded-radius symbolic justification.
- Kill `H3` if odometer or sink features do not beat depth, degree, or layer position as predictors of exact forcing, or if the signal survives `X`-label shuffling.
- Kill any branch that works only modulo `p` or `N`, only on proxy scores, only on one fixed alphabet, or only after decoder repair.

## Easiest Rehash Accusations By Active Hypothesis

### H1: Proof-Carrying Symbolic Forcing-Front CA

- "This is generic automated search over the Katz-Tao witness serialization."
- "This is bounded-slope or low-rational-complexity search in CA clothing."
- "This is geometry memorization on one family of product grids."
- "This is decoder engineering disguised as CA structure."

What makes the accusation stick:

- no exact verifier-backed score improvement;
- no held-out larger or different-aspect-ratio success;
- no held-out `X` success;
- label-shuffle survival;
- malformed states that need decoder repair or hidden legalization.

### H2: Sparse-Defect Amplifier CA On A Recursive Background

- "This is a tidy recursive background plus a few hand-placed certificate patches."
- "This is just local mutation or quality-diversity around a periodic family."
- "The apparent gain comes from defect bookkeeping, not from full-score improvement."

What makes the accusation stick:

- the clean background matches the defected version;
- density-matched random defects match the curated defects;
- local certificate counts improve but exact verified score does not;
- defect types cannot be justified locally and symbolically.

### H3: Flow-Firing Exact Forcing Decoder

- "This is a sandpile, chip-firing, or abelian-network re-description with no new arithmetic content."
- "Odometer or sink features are just aliases for depth, degree, or layer position."
- "The real work is in a specially engineered compiler-decoder pair, not in the invariant."

What makes the accusation stick:

- no predictive gap beyond trivial graph statistics;
- label shuffling does not destroy the signal;
- success disappears when the same compiler and decoder are tested against simple depth or degree baselines.

## Missing Controls And Documentary Gaps

- No exact tiny-grid `H1` sweep has executed.
- No matched benchmark block has executed.
- No label-shuffle run has executed.
- No held-out larger or different-aspect-ratio run has executed.
- No exact complexity sweep has executed.
- The current `H1` control artifact does not expose held-out `X` as its own row, even though held-out `X` is mandatory in `results/swarm/hypotheses.json` and `results/verification/verification_summary.md`.
- The current `H1` control artifact does not expose decoder ablation or randomization as its own row, even though `results/baselines/benchmark_spec.md` and `results/verification/verification_summary.md` make it mandatory.
- `H2` and `H3` have branch-specific kill rules in `results/swarm/hypotheses.json`, but there is no frozen benchmark artifact for them comparable to the `H1` matrix in `results/baselines/benchmark_spec.md`.
- The tiny-grid report does not yet surface the full reporting scaffold required by the frozen benchmark spec: legality hit rate, forcing hit rate, full score distributions, and failure-reason distributions.

## Benchmark Traps

- Benchmark-blocked versus benchmark-cleared trap:
  Empty control tables are evidence of a blocker, not evidence that the controls were passed.
- Decode-budget-only fairness trap:
  Matching exact-decode counts is not enough if CA branches get materially more generator-side search or training compute.
- Baseline aggregation trap:
  Random Local Search and Whole-Witness Mutation should remain separate. A CA that beats only the weakest non-CA comparator has not shown a robust advantage.
- Score-decomposition trap:
  Matching edge density `rho = m(G) / n(G)` is not enough. Reports must expose `m(G)`, `|R|`, `n(G)`, and `|T|` separately, or a branch can look good for the wrong reason.
- Fixed-`X` leakage trap:
  Geometry generalization without held-out `X` can still be alphabet overfit.
- H1-matrix reuse trap:
  Reusing the `H1` benchmark matrix for `H2` or `H3` would miss `H2`'s clean-background and random-defect controls and `H3`'s depth or degree baseline.
- Best-of-many trap:
  Best witness only reporting is forbidden. The frozen benchmark spec requires hit rates, score distributions, and failure reasons.
- Proxy-metric trap:
  Local certificate growth, odometer mass, current imbalance, or entropy reduction do not count unless they predict better exact verified score after full decode.

## Literature Branches That Invalidate Weak Claims

- Katz-Tao (1999):
  If a candidate does not decode back into the original six-line witness `(X,G,R,T)` with exact score accounting, it is off-target rather than merely weak.
- Green-Ruzsa (2017):
  Modular or finite-field behavior is not evidence for the integer forcing-pair target.
- Cowen-Breen, Karangozishvili, Varadarajan, Wang (2020):
  Optimizing a nearby pattern-count or homothety task is not the same as improving the forcing-pair witness problem.
- Pohoata-Zakharov (2024):
  A generalized arithmetic-Kakeya reformulation is not evidence unless it transfers back to the original witness target.
- Tao (2025):
  Small fixed alphabets, boundedly many slopes, and low rational complexity are exactly the regime most vulnerable to false progress stories.
- Hickman-Wright (2018):
  Success over rings or modular curricula is a side branch until it lifts honestly back to `\mathbb{Z}`.
- AlphaEvolve (2025) and *Mathematical exploration and discovery at scale* (2025):
  "Automation searched the space" is already prior art. Without a verifier-coupled exact witness advantage, the CA framing adds no novelty.
- Bond-Levine and adjacent abelian-network literature:
  Local-dynamics language is only relevant if it predicts or improves exact forcing beyond trivial graph baselines.

## Bottom Line

- The malformed watchlist is not the main risk.
- The real falsifier is that the repo still has no shared exact decoder or verifier and has executed `0` exact decodes.
- Until that gate opens, the active lane can honestly claim only a verifier-coupled CA design and blocker report.
- Any stronger claim can be invalidated immediately as one of the following:
  - off-target relative to Katz-Tao;
  - bounded-slope or modular false progress;
  - generic automated search with decoder leakage;
  - benchmark theater built on empty controls.
