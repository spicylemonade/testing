# Benchmark Report

Review phase: `review_round_1`

## Verdict

- Internal reproducibility package: **PASS**
- Publication-quality benchmark adequacy: **FAIL**

The repository now supports a narrow finite-horizon computational claim set: the
baseline recurrence is reproducible, the million-step baseline digest repeats, and the
stored witness artifacts are rich enough to reject the strongest compact-certificate
version of H1 on the current corpus. The benchmark package is still not strong enough
for publication-quality robustness, mechanism, or asymptotic claims.

## What The Current Evidence Actually Establishes

- The baseline implementation clears the local contract bar. Prefix validation is
  recorded in `results/experiments/run_1000000/contract.json`, the small-table checks
  exist in `tests/test_prime_separator.py`, and the old-square update-order mistake is
  explicitly tested.
- Large-horizon reproducibility is now better than the previous audit stated.
  `results/experiments/runtime_repeats_1000000.json` records three digest-matching
  million-step repeats for the baseline, `row_immediate`, and `column_immediate`, with
  mean and variance summaries.
- The archived variant runs do **not** provide two meaningful robustness ablations.
  `row_immediate` is exactly the baseline process on the stored outputs, and
  `column_immediate` is the exact axis swap of the baseline sequences rather than an
  independent nearby mechanism. The test suite and direct sequence equality confirm
  this.
- The experiment package therefore supports finite-horizon negative-result statements,
  not a robustness story. It supports: reproducible record gaps through `30` in the
  baseline, rejection of the strong raw-witness H1 story on the current corpus, and the
  empirical fact that several late record gaps are composite-only.

## Missing Baselines

- **No independent implementation baseline.**
  All large-horizon evidence still comes from one generator family. Repeated digests of
  the same implementation protect against nondeterminism, not against shared logic
  errors. A publication-quality package needs one separately written checker that
  agrees with the baseline contract through at least `10^5` steps.
- **No generic null or surrogate baseline.**
  There is still no benchmark against size-matched surrogate product sets, shuffled or
  degree-matched witness hypergraphs, or any matched generic factor-coverage process.
  Without that baseline, the current witness summaries cannot distinguish mex-coupled
  structure from generic local divisor/product coverage.
- **No matched non-record window baseline.**
  Prime-free intervals, singleton-heavy coverage, balanced-factor growth, and the
  axis-1 marker are summarized on record gaps only. There is no equal-length
  non-record-window control showing whether these features are actually discriminative.

## Missing Ablations And Controls

- **Zero genuine robustness ablations remain after the identity checks.**
  The original variant memo still describes `column_immediate` as a real perturbation,
  but the current code and tests show that it is just the axis swap. After accounting
  for that fact, the package has no materially distinct robustness variant at all.
- **The falsifier-requested controls are still missing.**
  The benchmark package does not include:
  1. a same-snapshot explicit tie-rule control;
  2. an admissibility perturbation that changes coverage rules rather than update
     staging.
- **Variant contracts are not benchmarked on the same footing as the baseline.**
  The baseline contract records prefix-validation flags. The variant contracts record
  digests and gap summaries only. That asymmetry weakens any cross-run evaluation,
  especially once the variants are being used as control evidence.
- **The benchmark narrative is internally inconsistent.**
  `results/experiments/variant_comparison.md` and the previous benchmark report still
  frame the archived variants as robustness evidence, while the paper and tests now
  treat them as identity and symmetry validations. That inconsistency needs to be fixed
  before any external-facing claim about ablations or robustness.

## Missing Error Analysis

- **Chosen-witness summaries are still canonicalization-sensitive.**
  `scripts/prime_separator.py` stores the first witness seen for each skipped value, and
  `scripts/summarize_record_gaps.py` derives prime/tiny/balanced/signature summaries
  from that chosen witness. Those metrics are not yet shown to be invariant under
  witness ordering or canonicalization.
- **Full hypergraph validation is selective.**
  Full witness exports cover baseline gaps `13, 17, 19, 20, 21` in one artifact and
  `21, 25, 28, 30` in another, but they are not yet used to recompute the headline
  taxonomy on every late record gap and not compared against matched non-record
  intervals.
- **H1/H2 analysis stops short of the available corpus.**
  The claim sheets still analyze the five-gap corpus `13, 17, 19, 20, 21` even though
  the million-step run produced later baseline records `25, 28, 30` and the
  axis-swapped run produced later row-gap records `21, 23, 26, 27, 31`. H2 explicitly
  does not extend its support table to those later gaps.
- **Mechanism language still outruns the controls.**
  Claims such as "the only stable T-specific motif" or "Ford-like local factor
  coverage" are still being made without surrogate controls or matched generic windows.
  Those statements may be right, but the current benchmark package does not isolate them
  strongly enough for publication-quality presentation.

## Missing Stress Tests

- **No horizon sweep for the mechanism metrics.**
  The repeat artifact is pinned at `10^6` steps. There is still no controlled checkpoint
  sweep at horizons such as `10^5`, `3 x 10^5`, `10^6`, and `3 x 10^6` showing whether
  the witness summaries, gap counts, offset statistics, and balanced-factor share
  stabilize, drift, or reverse.
- **No rolling hypergraph audit.**
  Hypergraph exports validate selected late gaps, not every late record gap and not any
  non-record controls. That is enough to validate some multiplicities, not enough to
  stress-test the witness-taxonomy narrative over scale.
- **No adversarial wrong-rule family beyond one nearby failure.**
  The test suite catches one misread update order, but there is no broader family of
  stale-state, wrong-snapshot, or witness-accounting negative controls that would
  pressure-test the benchmark instrumentation itself.

## Publication-Quality Claim Boundary

- The current package **can** support:
  - a validated recurrence implementation;
  - digest-repeatable million-step baseline computation;
  - finite-horizon record-gap growth through baseline gap `30`;
  - rejection of the strong raw-witness compact-certificate story on the current
    finite corpus;
  - the empirical existence of composite-only late record gaps.
- The current package **cannot** support:
  - boundedness or unboundedness of `T(1,n+1) - T(1,n)`;
  - any broad robustness claim;
  - a T-specific mechanism separated from generic local divisor/product coverage;
  - witness-taxonomy claims that depend on chosen-witness summaries being canonical;
  - publication-quality novelty language against the Ford overlap branch.

## Falsifiable Next Checks

1. Add one independently written reference implementation and require agreement with the
   baseline contract through at least `10^5` steps. If the contracts diverge, stop
   using the current large-horizon package as publication evidence.
2. Implement the two missing falsifier controls: a same-snapshot tie-rule variant and a
   real admissibility perturbation. If the qualitative conclusions break under either
   control, retract the current robustness language.
3. Benchmark the true process against matched non-record windows and size-matched
   surrogate product sets or hypergraphs. If prime-free, singleton-heavy, or
   balanced-factor patterns are equally common there, kill the T-specific mechanism
   framing.
4. Recompute the witness taxonomy from full hypergraphs for every baseline record gap
   from `20` upward and for the late axis-swapped row-gap records, under at least two
   witness canonicalizations. If the high-level summary changes materially, retract the
   current witness-summary narrative.
5. Extend the H1 and H2 tables to baseline gaps `25, 28, 30` and the late
   axis-swapped-row gaps. If the negative conclusions fail to persist on the larger
   corpus, update the claim sheets accordingly.
6. Run a repeated horizon sweep at fixed checkpoints such as `10^5`, `3 x 10^5`,
   `10^6`, and `3 x 10^6`. If the mechanism metrics drift or reverse, replace the
   current trend language with a horizon-limited statement.
