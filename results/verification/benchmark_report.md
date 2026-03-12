# Benchmark Report

## Status

Baseline audit result: **PASS after contract cleanup**.

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
- the gap-`21` interval contains `0` skipped primes and `20` skipped composites.

### Brittle Single-Witness Coverage

- **PASS**
- in the gap-`21` interval, `16` of the `20` skipped values have multiplicity `1`.
- this confirms the falsifier’s warning that long gaps can be sustained by brittle coverage.

### Recurrence-Order Mistakes

- **PASS**
- the benchmark package now includes a negative control test for a nearby wrong axis-choice rule.
- the deterministic digest test makes silent recurrence drift easier to catch than before.

## Allowed Perturbations

No more than these two perturbations are allowed for later robustness work:

1. Witness canonicalization:
   - change which valid witness pair is stored for a skipped value, while preserving validity and multiplicity.
2. Performance-only coverage tuning:
   - vary `--initial-limit` or limit-growth policy, provided `contract.json` stays identical.

## Residual Risks

- The test suite is still lightweight and subprocess-based rather than property-heavy.
- The negative control is a nearby wrong rule, not an exhaustive family of recurrence mistakes.
- Performance numbers remain environment dependent and should not be treated as structural evidence.
