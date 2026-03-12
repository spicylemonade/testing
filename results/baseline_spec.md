# Baseline Specification

## State Representation

Write

- `A_n = [a_1, ..., a_n]` for the first-row border terms, where `a_j = T(1,j)`;
- `B_n = [b_1, ..., b_n]` for the first-column border terms, where `b_i = T(i,1)`.

Then the defined `n x n` square is exactly the outer product

`P_n = {b_i * a_j : 1 <= i, j <= n}`.

The full array entries satisfy `T(i,j) = b_i * a_j`.

## Correct Update Order

Start with

- `a_1 = 1`;
- `b_1 = 1`;
- `P_1 = {1}`.

For each step `n >= 1`:

1. Choose `a_{n+1}` as the least positive integer not in `P_n`.
2. Choose `b_{n+1}` as the least positive integer not in `P_n` and not equal to `a_{n+1}`.
3. Only after both border terms are chosen, form `P_{n+1}` by adding:
   - `b_i * a_{n+1}` for `1 <= i <= n`;
   - `b_{n+1} * a_j` for `1 <= j <= n+1`.

This is the only admissible update order for the baseline.

Operational warning:
- `b_{n+1}` must be chosen from the old square `P_n`, excluding only the just-chosen `a_{n+1}`.
- Any implementation that allows products involving `a_{n+1}` or `b_{n+1}` to influence the choice of `b_{n+1}` is incorrect.

## Border Sets And Witnesses

For this run the machine-readable terminology is:

- `row_term`: an element of the first row, i.e. a value from `A_n`;
- `column_term`: an element of the first column, i.e. a value from `B_n`;
- `witness` for a covered integer `m` at step `n`: a pair `(column_term, row_term)` with
  `m = column_term * row_term`,
  `column_term in B_n`,
  `row_term in A_n`.

The baseline stores:
- one witness for each covered integer when first encountered at the current frontier;
- witness multiplicity, meaning the number of pairs `(b_i, a_j)` in `B_n x A_n` whose product equals that integer.

## Record Gaps

At step `n`, the first-row gap is

`gap_n = a_{n+1} - a_n`.

A record gap occurs when `gap_n` is larger than every previous first-row gap.

For a record gap, the skipped interval is

`[a_n + 1, a_{n+1} - 1]`.

Every integer in that interval must already lie in `P_n`; otherwise `a_{n+1}` would not be the mex.

## Skipped-Prime Status

For each skipped integer in a record interval, the baseline records:

- `is_prime`;
- `is_composite`;
- the witness multiplicity in `P_n`.

This supports the falsifier check that long record gaps need not contain skipped primes.

## Row/Column Offsets

The logged offset metadata is:

- `offset_before = b_n - a_n`;
- `offset_after = b_{n+1} - a_{n+1}`.

These are attached to each record gap so later analysis can test whether row/column drift explains anything about long gaps.

## Validation Targets

The baseline is considered valid only if it reproduces:

- the provided `5 x 11` table prefix;
- the provided first-row prefix `1,2,4,7,9,13,...`;
- deterministic record-gap locations under repeated runs.
