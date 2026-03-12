# Benchmark Reproducibility Note

## Commands

Validation:

```bash
python3 -m unittest -q tests/test_prime_separator.py
python3 scripts/prime_separator.py --steps 11 --out-dir results/baseline/smoke_11
```

Benchmark:

```bash
time -p python3 scripts/prime_separator.py --steps 30000 --out-dir results/baseline/run_30000
```

## Recurrence Validation Checks

- `tests/test_prime_separator.py` passes with the system `unittest` module.
- `results/baseline/smoke_11/table_preview.json` matches the provided `5 x 11` table exactly.
- `results/baseline/smoke_11/contract.json` reports all three prefix checks as `true`.
- repeated `30000`-step runs now match on `contract.json.structural_digest_sha256`.
- the test suite includes a negative control showing that a nearby wrong axis-choice rule does not reproduce the known prefix.
- The implementation uses the old-square snapshot for `b_{n+1}` and only adds new products after both new border terms are fixed.

## Runtime And Memory

Structural reproducibility is recorded in `results/baseline/run_30000/contract.json`.

Volatile performance data is recorded separately in `results/baseline/run_30000/performance.json`:

- steps: `30000`
- baseline runtime: about `0.232` seconds on the checked-in run
- shell wall time from `time -p`: about `0.30` seconds
- max RSS: `32456` KB

## Record-Gap Refresh

The validated run reproduces and extends the stale small-horizon evidence:

- gap `19` at `38630 -> 38649` on step `8475`
- gap `20` at `130699 -> 130719` on step `27676`
- gap `21` at `139039 -> 139060` on step `29373`

For the record gap `21`:

- skipped-prime count: `0`
- skipped-composite count: `20`
- single-witness skipped values: `16` of `20`

These values are recorded directly in `results/baseline/run_30000/record_gaps.json`.
