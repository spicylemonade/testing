# Benchmark Report

## Status

Benchmark audit result: **PASS with explicit documented risks**.

The initial audit correctly identified that the old benchmark package mixed deterministic structural outputs with volatile timing and RSS data. That issue has been fixed by separating:

- `contract.json` for deterministic structural claims;
- `performance.json` for volatile runtime/memory observations.

## Pass/Fail Checks

### Correctness

- **PASS**
- `results/baseline_spec.md` and `scripts/prime_separator.py` agree on the critical old-square update order.
- `tests/test_prime_separator.py` validates the known `11`-step prefix and now includes a nearby wrong-rule negative control.
- `results/baseline/smoke_11/contract.json` reports all three prefix checks as `true`.

### Reproducibility

- **PASS**
- repeated `30000`-step runs are checked by `tests/test_prime_separator.py` and agree on `structural_digest_sha256`.
- `results/baseline/run_30000/contract.json` now contains stable gap locations and a deterministic digest.
- volatile performance fields were moved to `results/baseline/run_30000/performance.json`.

### Witness-Log Completeness

- **PASS**
- `results/baseline/run_30000/record_gaps.json` stores, for every record gap, every skipped integer together with:
  - prime/composite status;
  - witness multiplicity;
  - one valid witness pair;
  - offset metadata.

### Stale Small-Horizon Refresh

- **PASS**
- the validated run goes beyond the stale `17`-gap horizon and reproduces:
  - gap `19` at `38630 -> 38649` on step `8475`;
  - gap `20` at `130699 -> 130719` on step `27676`;
  - gap `21` at `139039 -> 139060` on step `29373`.

### Prime-Free Record Gaps

- **PASS**
- the baseline already shows that gap `21` contains `0` skipped primes and `20` skipped composites.
- the million-step run strengthens this rather than weakening it:
  - gap `28` is composite-only;
  - gap `30` is composite-only;
  - the `column_immediate` perturbation also produces composite-only late records, including gap `31`.

Interpretation: prime-free record gaps are a validated feature of the package, not a hidden contradiction.

### Brittle Single-Witness Coverage

- **PASS**
- in the gap-`21` interval, `16` of the `20` skipped values have multiplicity `1`;
- in the million-step run, the late record gaps have singleton shares:
  - gap `25`: `18/24`;
  - gap `28`: `18/27`;
  - gap `30`: `19/29`.

Interpretation: brittle coverage remains present at larger horizons and is now explicitly benchmarked rather than buried.

### Recurrence-Order Mistakes

- **PASS**
- the benchmark package now includes a negative control test for a nearby wrong axis-choice rule.
- the deterministic digest test makes silent recurrence drift easier to catch than before.
- the two nearby perturbation runs are logged separately under `results/experiments/row_immediate_1000000/` and `results/experiments/column_immediate_1000000/`, so the package no longer blurs the validated baseline with robustness experiments.
- full-witness hypergraph exports validate multiplicity counts on:
  - original gap `30`;
  - `row_immediate` gap `30`;
  - `column_immediate` gap `31`.

### Stale Small-Horizon Claims

- **PASS**
- the package no longer stops at the old `21`-gap horizon.
- `results/experiments/run_1000000/contract.json` extends the record-gap trajectory to `25`, `28`, and `30`.
- `results/experiments/run_1000000/experiment_note.md` records the exact command and runtime.

### Unsupported Benchmarks

- **PASS**
- the primary experiment, the two perturbation runs, and the late-gap hypergraph exports are all backed by exact commands recorded in:
  - `results/experiments/run_1000000/experiment_note.md`;
  - `results/experiments/variant_comparison.md`.
- no claim in the current package relies on an uncaptured shell transcript or on a benchmark path that cannot be regenerated.

## Allowed Non-Structural Perturbations

No more than these two perturbations are allowed for later robustness work:

1. Witness canonicalization:
   - change which valid witness pair is stored for a skipped value, while preserving validity and multiplicity.
2. Performance-only coverage tuning:
   - vary `--initial-limit` or limit-growth policy, provided `contract.json` stays identical.

## Residual Risks

- The test suite is still lightweight and subprocess-based rather than property-heavy.
- The negative control is a nearby wrong rule, not an exhaustive family of recurrence mistakes.
- The `column_immediate` perturbation shows that some trajectory-level phenomena are sensitive to staging, even though the high-level negative-result conclusions survive.
- Performance numbers remain environment dependent and should not be treated as structural evidence.
