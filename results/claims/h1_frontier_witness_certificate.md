# H1 Claim Sheet: Frontier Witness Certificates

## Status

Weak negative result. The current witness corpus does **not** support a compact
interval-wide certificate language for record gaps. The only stable T-specific motif
is a single axis-1 boundary marker at the previous column term.

## Corpus

- Primary corpus: `results/baseline/run_30000/record_gaps.json`
- Derived summary: `results/analysis/h1_h2_gap_summary.json`
- Gaps analyzed: `13`, `17`, `19`, `20`, `21`

| gap | step | skipped | singleton share | axis-1 marker | min factor <= 10 | min factor > 100 | skipped primes |
|---|---:|---:|---:|---|---:|---:|---:|
| 13 | 866 | 12 | 10/12 | `3571 = 1 * 3571` | 8/12 | 0/12 | 1 |
| 17 | 2063 | 16 | 14/16 | `8871 = 1 * 8871` | 8/16 | 0/16 | 0 |
| 19 | 8475 | 18 | 15/18 | `38639 = 1 * 38639` | 9/18 | 1/18 | 1 |
| 20 | 27676 | 19 | 17/19 | `130712 = 1 * 130712` | 9/19 | 1/19 | 0 |
| 21 | 29373 | 20 | 16/20 | `139052 = 1 * 139052` | 9/20 | 3/20 | 0 |

## Candidate Certificate Families

### 1. Axis-1 boundary marker

- In every analyzed record gap there is exactly one skipped value with witness
  `1 * previous_column_term`.
- The witness value is the previous column border term itself:
  `3571`, `8871`, `38639`, `130712`, `139052`.
- This is a genuine endogenous feature of the mex-coupled array.

Verdict: real but too thin. It marks one point inside the interval and does not
explain the other `11`, `15`, `17`, `18`, or `19` skipped values.

### 2. Tiny-factor grammar

- If a compact witness language existed, the same low-factor templates should dominate
  larger record gaps.
- Instead the tiny-factor share decays across the five-gap corpus:
  `8/12`, `8/16`, `9/18`, `9/19`, `9/20`.
- By gap `21`, many skips already need mesoscopic or balanced witnesses such as
  `139049 = 659 * 211`, `139057 = 577 * 241`, and `139050 = 225 * 618`.

Verdict: the low-factor grammar weakens as gaps grow.

### 3. Redundant certificate family

- A robust certificate family should create redundancy.
- The corpus is dominated by singleton witnesses:
  `10/12`, `14/16`, `15/18`, `17/19`, `16/20`.
- Gap `21` already has multiplicity histogram `1:16, 3:1, 4:2, 5:1`, so the extra
  coverage is present but sparse.

Verdict: the visible witness layer is brittle, not redundant.

### 4. Mesoscopic / balanced fallback

- As the gaps increase, the witness signatures broaden rather than compress.
- Gap `19` already needs the balanced redundant witness `38631 = 237 * 163`.
- Gap `20` adds the balanced singleton `130702 = 457 * 286`.
- Gap `21` contains two balanced singletons and one balanced redundant witness:
  `139049 = 659 * 211`, `139057 = 577 * 241`, `139050 = 225 * 618`.

Verdict: witness types proliferate into Ford-like local factor coverage instead of
stabilizing into a small reusable taxonomy.

## Claim

The strong H1 formulation fails on the current record-gap corpus. What survives is a
much weaker claim:

- every large record gap examined so far contains a single endogenous axis-1 boundary
  marker at the previous column term;
- the rest of the interval is covered by heterogeneous mostly-singleton witnesses;
- the witness mix drifts away from a tiny-factor language as record gaps grow.

This is evidence **against** a compact raw-witness certificate language, not for one.

## Corroboration Beyond 30k Steps

`results/concept_evolve/probe_result.json` strengthens the same conclusion on the late
record gaps `19`, `20`, `21`, `25`, `28`, and `30`: singleton share stays high while
the balanced-factor share rises and the tiny-factor share falls. That trend is
consistent with witness-taxonomy failure rather than compression.
