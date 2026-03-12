# Benchmark Report

## Verdict

- Internal benchmark package: **PASS**
- Publication-quality benchmark adequacy: **FAIL**

The repo now has a correct reproducible baseline generator, machine-readable witness
logs, one million-step experiment artifacts, and two logged perturbation runs. That is
enough to support finite-horizon negative-result claims. It is not enough to support a
publication-quality mechanism claim, asymptotic claim, or strong robustness claim.

## What The Current Benchmarks Actually Support

- The original recurrence is implemented reproducibly enough to clear the local contract
  bar: the `11`-step prefix checks pass, repeated `30000`-step runs agree on
  `structural_digest_sha256`, and the old-square update order is explicitly tested.
- The baseline million-step run extends the record-gap trajectory from `21` to `25`,
  `28`, and `30`, with exact commands and runtime metadata recorded under
  `results/experiments/run_1000000/`.
- `row_immediate` and the baseline agree on the tracked row-gap observables at
  `10^6` steps: same final border values, same record-gap count, same largest record
  gap, and identical `record_gap_summary.json` content. The structural digests differ,
  so this supports equality of the tracked benchmark outputs, not full structural
  identity.
- `column_immediate` is a real perturbation: it changes the trajectory to `20` record
  gaps and a largest record gap of `31`, while preserving the observed late-gap
  negative-result features such as composite-only records and singleton-heavy coverage.
- Selected full hypergraph exports validate stored multiplicities on baseline gaps
  `21`, `25`, `28`, `30`, plus one late gap for each perturbation.

## Missing Baselines

- **No independent implementation baseline.**
  All large-horizon claims come from one generator family. Repeated runs of the same
  script catch nondeterminism, not shared logic bugs. A publication-quality package
  needs one independently written checker at a smaller horizon such as `10^4` or
  `10^5`.
- **No large-horizon reproducibility baseline.**
  Structural repeatability is documented for `30000` steps, not for the `1000000`-step
  experiment or its perturbations. The million-step evidence is effectively single-run.
- **No surrogate/null benchmark.**
  There is still no comparison against size-matched generic product sets, surrogate
  hypergraphs, or matched non-record windows. Without that control, the repo cannot
  show that the observed witness structure is specific to the mex-coupled process
  rather than generic local factor coverage.

## Missing Ablations And Controls

- **Only one materially distinct ablation is present.**
  `row_immediate` collapses back to the same tracked gap outputs as the baseline, so
  the benchmark package contains only one perturbation that changes the measured
  trajectory: `column_immediate`.
- **The falsifier's requested controls are not fully covered.**
  The current variants are staging/order perturbations. The package still lacks:
  1. a same-snapshot explicit tie-rule control;
  2. an admissibility perturbation that changes coverage rules rather than staging.
- **Variant correctness evidence is thinner than baseline correctness evidence.**
  The baseline contract records prefix-validation flags; the variant contracts do not.
  That asymmetry weakens cross-run benchmark comparability.

## Missing Error Analysis

- **Chosen-witness summaries are not canonicalization-robust.**
  `scripts/prime_separator.py` stores the first witness seen for each skipped value, and
  `scripts/summarize_record_gaps.py` builds signature statistics from that chosen
  witness. Those summaries can shift under witness canonicalization even when
  multiplicities stay fixed.
- **Full hypergraph validation is only partial.**
  The repo exports full witness sets for selected late gaps, not for every late record
  gap and not for matched non-record intervals. That is enough to validate some stored
  multiplicities, not enough to prove that the reported witness-taxonomy trends are
  witness-selection invariant.
- **No matched negative controls for mechanism metrics.**
  Prime-free intervals, singleton-heavy coverage, balanced-factor growth, and the
  axis-1 marker are reported only on record gaps. There is no benchmark against
  equal-length non-record windows showing whether these features are actually
  discriminative.
- **H2 error analysis stops too early.**
  The prime-support table is only analyzed on gaps `13`, `17`, `19`, `20`, and `21`.
  It is not extended in the same form to baseline gaps `25`, `28`, `30` or to the late
  perturbation gaps.

## Missing Stress Tests

- **No horizon sweep.**
  The main experiment benchmark is pinned at `10^6` steps. There is no controlled sweep
  across horizons such as `10^5`, `3 x 10^5`, `10^6`, `3 x 10^6` to show how record-gap
  counts, largest gaps, singleton share, and offset statistics evolve.
- **No reproducible scaling profile.**
  The repo records one runtime and RSS observation per run, with no repeats, no machine
  metadata, and no variance estimate. These numbers are observational only and cannot
  support performance claims.
- **Recurrence-mistake stress testing is still shallow.**
  The test suite includes one nearby wrong-rule negative control, but not a broader
  family of wrong-order, stale-state, or witness-accounting perturbations.
- **Hypergraph stress testing is selective.**
  Hypergraph exports check a few late records. They do not yet provide a systematic
  rolling-horizon audit of all large gaps or any non-record controls.

## Publication-Quality Claim Boundary

- The current package **can** claim:
  - a validated recurrence implementation;
  - reproducible finite-horizon record-gap growth through gap `30` in the baseline and
    `31` in one perturbation;
  - composite-only late record gaps;
  - failure of the raw-witness compact-certificate story on the current corpus.
- The current package **cannot** claim:
  - boundedness or unboundedness of `T(1,n+1) - T(1,n)`;
  - a T-specific mechanism separated from Ford-style local divisor/product coverage;
  - robustness under nearby perturbations in any broad sense;
  - statistical runtime or memory conclusions.

## Falsifiable Next Checks

1. Add one independently written reference implementation and require agreement with the
   baseline contract through at least `10^5` steps. If the contracts diverge, the large
   run package is not trustworthy enough for publication.
2. Run the two missing controls from the falsifier memo: a same-snapshot tie-rule
   variant and an admissibility perturbation. If the qualitative conclusions break, the
   current robustness story fails.
3. Benchmark record-gap metrics against matched non-record windows and size-matched
   surrogate product sets. If prime-free or singleton-heavy structure is equally common
   there, kill the T-specific mechanism interpretation.
4. Export full witness hypergraphs for every baseline record gap from `20` upward and
   for every late perturbation record gap. If the high-level witness taxonomy changes
   materially after removing chosen-witness bias, retract the current witness-summary
   narrative.
5. Run a horizon sweep with repeated digests and performance logs at fixed checkpoints
   such as `10^5`, `3 x 10^5`, `10^6`, and `3 x 10^6`. If gap growth or qualitative
   summaries plateau, reverse, or become unstable across checkpoints, state that
   explicitly instead of extrapolating from one horizon.
