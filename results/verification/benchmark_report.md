# Benchmark Report

Verification phase: `post_deepen`

## Verdict

- Internal reproducibility and negative-result benchmarking: **PASS**
- Publication-quality benchmark adequacy for mechanism, robustness, or asymptotic claims: **FAIL**

The post-deepen package is materially stronger than the earlier review-round artifact.
It now includes a partial independent checker, matched non-record controls, affine
surrogate windows, a dual-canonicalization full-hypergraph audit, a sampled schedule
audit, and one genuine admissibility perturbation. That is enough to support a narrow
finite-horizon negative-result package. It is still not enough to support
publication-quality claims about a `T`-specific mechanism, robustness of the witness
story, or boundedness/unboundedness of `T(1,n+1) - T(1,n)`.

## What The Current Benchmark Package Actually Establishes

- The baseline recurrence is reproducible through the checked million-step run:
  prefix validation passes, the largest baseline record gap is `30`, and three
  million-step repeats agree on the baseline digest.
- The package now has a separately written checker that agrees with the baseline
  row/column terms through `10^5` steps.
- The evaluation package is no longer record-only. The post-deepen shared corpus
  contains `5` late record windows, `45` matched non-record controls, and `50`
  size-matched affine surrogate windows.
- Full-witness error analysis improved: the hypergraph audit recomputes candidate
  metrics from the full pair set under balanced and lexicographic canonicalizations.
- Schedule testing improved: `row_immediate` is confirmed as the baseline process on
  audited states, and `column_immediate` is confirmed as the axis swap.
- The package now includes one genuine admissibility perturbation, `coprime_only`,
  which is strong enough to kill the small-`q` modular-locking lane.

These additions support negative claims such as:

- no bounded-correction anchor/backbone law on the held-out late records;
- no credible full-hypergraph rigidity invariant on the current matched corpus;
- no modular-residue mechanism that beats the anchor comparator;
- no robustness story that can be inferred from the stored variant runs alone.

## Baselines

### 1. Same-code reproducibility baseline

Status: **PASS**

- The baseline contract validates the known prefix and the million-step run records
  the expected late record gaps `25`, `28`, and `30`.
- `results/experiments/runtime_repeats_1000000.json` records three digest-matching
  million-step repeats for the baseline, `row_immediate`, and `column_immediate`.

Benchmark implication:
- The main generator is deterministic on the recorded machine and command path.

### 2. Independent implementation baseline

Status: **PARTIAL**

- `results/novelty_deepening/checker_agreement.json` shows a separately written
  checker agreeing with the baseline through `10^5` steps.
- There is still no independent agreement artifact at the headline `10^6` horizon, and
  no independent checker for witness logs, matched-window corpora, or hypergraph
  summaries.

Benchmark implication:
- The package is protected against some shared-logic mistakes, but not yet strongly
  enough for publication-quality use of the full late-horizon evaluation stack.

### 3. Matched controls and surrogate baselines

Status: **PARTIAL**

- The earlier claim that no matched controls exist is now false. The shared corpus
  includes `45` matched non-record windows and `50` affine size-matched surrogates.
- These controls are already strong enough to falsify several positive stories:
  the anchor/backbone law fails bounded-support on held-out records, and the best
  hypergraph near-miss still leaves `28.9%` of matched controls inside the balanced
  record band.
- The control package is still narrow. The held-out positive set for Item 026 is only
  two late records, and the affine surrogate family is easier than the true matched
  controls.

Benchmark implication:
- The package now supports controlled negative-result claims.
- It still does not support publication-quality separation of `T`-specific structure
  from generic local product coverage.

## Ablations And Controls

### 1. Main variant package

Status: **FAIL** as robustness ablation evidence

- `row_immediate` is not an ablation; it is the baseline process.
- `column_immediate` is not an independent nearby mechanism; it is the axis swap.
- The current tests and the late schedule audit both support this identity/symmetry
  reading.

Benchmark implication:
- The main experiment package contains zero genuine nearby robustness ablations.
- Any claim that the baseline conclusions survive perturbation cannot cite
  `row_immediate` or `column_immediate` as substantive robustness evidence.

### 2. Genuine perturbation controls

Status: **PARTIAL**

- `coprime_only` is a real coverage-rule change and therefore a real negative control.
- It is useful for falsifying the modular-locking direction, but it is not a matched
  robustness baseline for the original recurrence: it fails all baseline prefix checks
  and changes the object substantially.

Benchmark implication:
- The repo now has one real perturbation test.
- It still lacks a nearby admissibility/tie-rule control that preserves enough of the
  baseline geometry to support a publication-grade robustness argument.

### 3. Schedule control

Status: **PARTIAL**

- The post-deepen schedule audit sampled `1000` late frontier states and found batched
  equals row-immediate on all audited states, while column-immediate matches the axis
  swap on all audited states.
- This is a useful one-step control, not an exhaustive proof that all downstream
  evaluation artifacts are schedule-insensitive at every horizon.

Benchmark implication:
- The schedule story is good enough to demote the old robustness rhetoric.
- It is not a substitute for real nearby ablations of the claimed mechanism metrics.

## Error Analysis

### 1. Chosen-witness sensitivity

Status: **PARTIAL**

- The old criticism is no longer fully accurate: full-witness recomputation exists and
  the hypergraph audit compares balanced and lexicographic canonicalizations.
- The remaining problem is scope. The chosen-witness summaries in
  `record_gap_summary.json`, the H1 sheet, the H2 sheet, and the final-status note are
  still driven by first-witness bookkeeping rather than by full-pair recomputation of
  the same headline taxonomy.

Benchmark implication:
- Graph-level canonicalization risk is partly quantified.
- Publication-quality witness-taxonomy claims are still unsupported until the headline
  summaries themselves are shown to be canonicalization-stable.

### 2. Stale evidence routing

Status: **FAIL**

- The benchmark narrative and claim-source routing are stale relative to the
  post-deepen artifacts. They still lean on the earlier five-gap summaries even though
  matched-control and surrogate evaluations now exist.
- H1 and especially H2 remain tabled on the old `13, 17, 19, 20, 21` corpus despite
  later late-gap evidence and phase-6 controls.

Benchmark implication:
- The repo currently mixes old and new evidence layers.
- That inconsistency is itself a benchmark weakness because it makes it unclear which
  artifact is the authoritative support for each computational claim.

## Stress Tests

### 1. Horizon and checkpoint testing

Status: **PARTIAL**

- A checkpoint sweep now exists in the modular lane at `10^5`, `3 x 10^5`, and `10^6`.
- There is still no corresponding checkpoint sweep for the core witness, offset,
  anchor, or hypergraph metrics used in the main narrative.

Benchmark implication:
- The package has some temporal stress testing.
- It still does not show whether the main mechanism-style summaries stabilize, drift,
  or reverse with horizon.

### 2. Full late-window audits

Status: **PARTIAL**

- Late full-witness artifacts now cover the main baseline late records used in the
  phase-6 corpus, and matched controls/surrogates are present in the shared corpus.
- The package still does not benchmark every headline witness summary against the full
  corpus under multiple canonicalizations, and it does not extend the matched-control
  evaluation beyond the narrow late-record slice.

Benchmark implication:
- The late negative-result package is credible on its audited slice.
- It remains too narrow for broad claims about the process as a whole.

### 3. Performance benchmarking

Status: **FAIL** for publication-grade benchmarking

- Runtime evidence is limited to three same-machine repeats and single-run wall-clock /
  RSS snapshots.
- That is enough for reproducibility notes, not for serious performance benchmarking or
  cross-environment claims.

## Publication-Quality Claim Boundary

The current package **can** support:

- a validated recurrence implementation and reproducible million-step baseline run;
- a partial independent check through `10^5` steps;
- controlled negative-result claims against the bounded-correction anchor/backbone,
  full-hypergraph rigidity, and modular-locking lanes;
- the statement that the archived variant runs are identity/symmetry checks rather than
  robustness ablations.

The current package **cannot** support:

- boundedness or unboundedness of `T(1,n+1) - T(1,n)`;
- a publication-quality robustness claim;
- a `T`-specific witness or hypergraph mechanism cleanly separated from generic local
  product coverage;
- headline witness-taxonomy claims that still depend on first-witness summaries;
- performance benchmarking claims beyond simple same-machine repeatability.

## Falsifiable Next Checks

1. Extend the independent checker to the full `10^6` horizon and require exact
   agreement on row/column terms, record-gap locations, and the matched-window export.
   If any disagreement appears, stop using the current late-horizon package as
   publication evidence.

2. Add one genuinely nearby admissibility or tie-rule control that preserves the
   baseline prefix for a substantial prefix while changing coverage decisions. If the
   main negative conclusions fail under that control, retract the current robustness
   language completely.

3. Recompute the headline witness taxonomy from the full witness pair set, not from the
   first witness encountered, on every phase-6 record/control window under at least two
   canonicalizations. If singleton share, balanced-factor share, or prime-support
   summaries move materially, remove those narratives from the publication claim set.

4. Replace or augment the affine surrogate family with a harder size- and
   factor-budget-matched surrogate baseline. If the best hypergraph or anchor metrics
   stop separating records from the harder surrogates, kill the `T`-specific mechanism
   framing.

5. Run the core benchmark metrics at fixed checkpoints such as `10^5`, `3 x 10^5`,
   `10^6`, and `3 x 10^6`. If anchor AUROC, control overlap, or witness-taxonomy
   summaries drift materially, downgrade all mechanism language to an explicitly
   finite-horizon statement.

6. Rewrite the evidence ledger so every computational claim routes to one current
   post-deepen artifact. If H1/H2 or the final-status note still depend on stale
   small-corpus summaries after that rewrite, treat those claims as unsupported.
