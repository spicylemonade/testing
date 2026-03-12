# Million-Step Experiment Note

## Commands

```bash
time -p python3 scripts/prime_separator.py --steps 1000000 --out-dir results/experiments/run_1000000
python3 scripts/summarize_record_gaps.py \
  --record-gaps results/experiments/run_1000000/record_gaps.json \
  --row-terms results/experiments/run_1000000/row_terms.json \
  --column-terms results/experiments/run_1000000/column_terms.json \
  --out results/experiments/run_1000000/record_gap_summary.json
python3 scripts/export_witness_hypergraphs.py \
  --record-gaps results/experiments/run_1000000/record_gaps.json \
  --row-terms results/experiments/run_1000000/row_terms.json \
  --column-terms results/experiments/run_1000000/column_terms.json \
  --gaps 21 25 28 30 \
  --out results/analysis/full_witness_hypergraphs_gap21_25_28_30.json
```

## Runtime / Contract

- Steps: `1,000,000`
- Runtime: `10.156307567000113` seconds
- Max RSS: `321264` KB
- Final row term: `5195523`
- Final column term: `5195525`
- Record gaps found: `17`
- Largest record gap: `30`
- Structural digest: `3680d24d2073239978438eaf02f8f05a1ed81da4e52927909c4dc47c0d0291e3`

## Record-Gap Trajectory Beyond The 30k Horizon

The 30k baseline stopped at gap `21`. The million-step run adds:

| gap | step | interval | skipped primes | singleton share | min factor <= 10 | min factor > 100 | offset before | offset after |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| 25 | 92320 | `451018 -> 451043` | 1 | 18/24 | 10/24 | 7/24 | 21 | 4 |
| 28 | 247399 | `1241893 -> 1241921` | 0 | 18/27 | 10/27 | 9/27 | 11 | 1 |
| 30 | 729353 | `3760927 -> 3760957` | 0 | 19/29 | 10/29 | 13/29 | 16 | 2 |

Late-gap continuity with the previous horizon is preserved:

| gap | step | skipped primes | singleton share | min factor <= 10 | min factor > 100 |
|---|---:|---:|---:|---:|---:|
| 19 | 8475 | 1 | 15/18 | 9/18 | 1/18 |
| 20 | 27676 | 0 | 17/19 | 9/19 | 1/19 |
| 21 | 29373 | 0 | 16/20 | 9/20 | 3/20 |
| 25 | 92320 | 1 | 18/24 | 10/24 | 7/24 |
| 28 | 247399 | 0 | 18/27 | 10/27 | 9/27 |
| 30 | 729353 | 0 | 19/29 | 10/29 | 13/29 |

## Late-Gap Hypergraph Export

`results/analysis/full_witness_hypergraphs_gap21_25_28_30.json` enumerates every
admissible border-factor pair for each skipped value in gaps `21`, `25`, `28`, and
`30`.

Key checks:

- multiplicity mismatches: `0` on all four exported gaps
- full pair totals:
  - gap `21`: `32`
  - gap `25`: `31`
  - gap `28`: `36`
  - gap `30`: `43`
- pair-count histograms:
  - gap `21`: `1:16, 3:1, 4:2, 5:1`
  - gap `25`: `1:18, 2:5, 3:1`
  - gap `28`: `1:18, 2:9`
  - gap `30`: `1:19, 2:8, 3:1, 5:1`

Interpretation:

- The late gaps are still dominated by low-pair-count values, so the rescue route does
  not uncover a hidden explosion of witness multiplicity.
- Distinct factor reuse remains weak:
  - gap `21`: `31` distinct row factors, `30` distinct column factors
  - gap `25`: `28` distinct row factors, `29` distinct column factors
  - gap `28`: `34` distinct row factors, `34` distinct column factors
  - gap `30`: `39` distinct row factors, `41` distinct column factors

This keeps the current interpretation unchanged: the full witness export validates the
stored multiplicities and slightly sharpens the negative result, but it does not yet
produce a compact interval-level certificate.

## Sources

See `results/verification/claim_source_matrix.md` and `sources.bib`.
