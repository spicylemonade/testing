# H2 Claim Sheet: Prime-Support Fixed Point

## Status

Not promoted. The prime-support observables are measurable, but on the shared record-gap
corpus they do not explain anything that the direct witness logs do not already show.

## Support Observables

On each record gap from `results/analysis/h1_h2_gap_summary.json`, track:

- `skipped_prime_count`: how many skipped values in the interval are prime.
- `row_primes_le_sqrt_prev`: row-border primes at or below `sqrt(previous_row_term)`.
- `column_primes_le_sqrt_prev`: column-border primes at or below `sqrt(previous_row_term)`.
- `support_imbalance = column_primes_le_sqrt_prev - row_primes_le_sqrt_prev`.
- `chosen_witness_prime_either_count`: skipped values whose stored witness uses at least
  one prime border factor.

These are intentionally conservative observables: they stay on the same witness corpus
used for H1 and do not introduce a second data source.

## Shared-Corpus Comparison

| gap | skipped primes | row primes <= sqrt(prev) | col primes <= sqrt(prev) | imbalance | chosen witness uses a prime |
|---|---:|---:|---:|---:|---:|
| 13 | 1 | 6 | 11 | 5 | 9/12 |
| 17 | 0 | 11 | 13 | 2 | 11/16 |
| 19 | 1 | 18 | 26 | 8 | 14/18 |
| 20 | 0 | 29 | 43 | 14 | 16/19 |
| 21 | 0 | 29 | 44 | 15 | 14/20 |

## What H2 Does Explain

- The prime-support state is not static. The available row-side and column-side prime
  supports below the square-root scale grow smoothly with the frontier.
- The column side stays prime-heavier than the row side on all five gaps, so the
  support split is real and measurable.

## What H2 Does Not Explain

### 1. Composite-only record gaps

- Gaps `17`, `20`, and `21` contain zero skipped primes.
- `results/concept_evolve/probe_result.json` extends the same phenomenon to larger
  record gaps `28` and `30`.

Consequence: prime obstructions are not required for long first-row jumps.

### 2. Record-to-record growth

- Between gaps `20` and `21`, the row-side prime support stays fixed at `29` while the
  column-side support changes by only `+1`.
- That is too small and too smooth to explain the jump from gap `20` to gap `21`.

Consequence: the support counts behave like background state, not a sharp trigger.

### 3. Witness behavior

- The chosen-witness prime share is non-monotone: `9/12`, `11/16`, `14/18`, `16/19`,
  then back down to `14/20`.
- Meanwhile the direct witness story from H1 remains decisive: singleton coverage
  dominates, the axis-1 marker is composite, and balanced witnesses become more common.

Consequence: the prime-support layer adds less explanatory resolution than the witness
layer itself.

## Claim

On the current shared corpus, H2 adds no explanatory power beyond H1.

- It correctly records a genuine row/column prime-support asymmetry.
- It does **not** distinguish the composite-only record gaps from the prime-bearing ones.
- It does **not** isolate why new record gaps appear when they do.
- It does **not** compress the witness heterogeneity that already weakens H1.

The backup line therefore remains demoted. If it is revisited later, it needs a new
support observable that predicts record-gap behavior better than direct witness logs,
not just another restatement of the prime split.
