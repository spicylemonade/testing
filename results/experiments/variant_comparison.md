# Robustness Variant Comparison

## Variants

Exactly two nearby perturbations were evaluated.

1. `row_immediate`
   - choose the next row mex from the old square;
   - insert the new row products immediately;
   - then choose the next column term from the updated coverage.
2. `column_immediate`
   - choose the next column mex first;
   - insert the new column products immediately;
   - then choose the next row term from the updated coverage.

No third variant was run. This keeps the experiment inside the tool-plan budget and
avoids a variant zoo.

## Commands

```bash
time -p python3 scripts/prime_separator_variants.py \
  --variant row_immediate \
  --steps 1000000 \
  --out-dir results/experiments/row_immediate_1000000
time -p python3 scripts/prime_separator_variants.py \
  --variant column_immediate \
  --steps 1000000 \
  --out-dir results/experiments/column_immediate_1000000
python3 scripts/summarize_record_gaps.py \
  --record-gaps results/experiments/row_immediate_1000000/record_gaps.json \
  --row-terms results/experiments/row_immediate_1000000/row_terms.json \
  --column-terms results/experiments/row_immediate_1000000/column_terms.json \
  --out results/experiments/row_immediate_1000000/record_gap_summary.json
python3 scripts/summarize_record_gaps.py \
  --record-gaps results/experiments/column_immediate_1000000/record_gaps.json \
  --row-terms results/experiments/column_immediate_1000000/row_terms.json \
  --column-terms results/experiments/column_immediate_1000000/column_terms.json \
  --out results/experiments/column_immediate_1000000/record_gap_summary.json
python3 scripts/export_witness_hypergraphs.py \
  --record-gaps results/experiments/row_immediate_1000000/record_gaps.json \
  --row-terms results/experiments/row_immediate_1000000/row_terms.json \
  --column-terms results/experiments/row_immediate_1000000/column_terms.json \
  --gaps 30 \
  --out results/experiments/row_immediate_1000000/full_witness_gap30.json
python3 scripts/export_witness_hypergraphs.py \
  --variant column_immediate \
  --record-gaps results/experiments/column_immediate_1000000/record_gaps.json \
  --row-terms results/experiments/column_immediate_1000000/row_terms.json \
  --column-terms results/experiments/column_immediate_1000000/column_terms.json \
  --gaps 31 \
  --out results/experiments/column_immediate_1000000/full_witness_gap31.json
```

## Validation

- `row_immediate` full-witness gap-30 check: multiplicity mismatch count `0`
- `column_immediate` full-witness gap-31 check: multiplicity mismatch count `0`

Both perturbations therefore retain witness logs that are internally consistent with
their own recurrence order.

## Comparison Against The Original Rule

### 1. `row_immediate`

- Same million-step row-gap trajectory as the original rule:
  - record-gap count `17`
  - largest record gap `30`
  - same gap locations through step `729353`
  - same final border values `row_last = 5195523`, `column_last = 5195525`
- Same late-gap qualitative profile:
  - gap `30` is composite-only
  - singleton share `19/29`
  - tiny-factor share `10/29`
  - balanced-factor share `13/29`

Interpretation: inserting the new row before choosing the new column does not change the
row-gap behavior at this horizon. This perturbation is informative precisely because it
collapses back to the original rule on the observables under study.

### 2. `column_immediate`

- The trajectory changes materially:
  - record-gap count `20`
  - largest record gap `31`
  - late records `21`, `23`, `26`, `27`, `31`
  - final border values swap orientation: `row_last = 5195525`, `column_last = 5195523`
- But the qualitative conclusions survive:
  - large record gaps are still mostly composite-only (`21`, `23`, `26`, `31` have zero skipped primes)
  - singleton-heavy coverage persists (`0.68` to `0.82` on the late records)
  - tiny-factor language does not recover (`0.32` to `0.50`)
  - balanced witnesses remain nontrivial (`0.20` to `0.32`)
  - a single axis-1 marker still appears in each late gap

Interpretation: the precise staging changes the record-gap trajectory, but it does not
rescue the compact-certificate or prime-obstruction stories.

## Surviving Conclusions

The qualitative conclusions that survive all three runs are:

- large record gaps persist well beyond the 30k horizon;
- prime-free record gaps are common, so prime obstruction is not the main mechanism;
- witness coverage remains singleton-heavy;
- the only stable T-specific motif is the one-point axis-1 boundary marker;
- the witness language does not simplify under these nearby perturbations.

The experiment therefore supports keeping the original negative-result interpretation and
rejecting any robustness claim that depends on one exact admissibility ordering.
