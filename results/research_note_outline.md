# Research Note Outline

## 1. Problem And Provenance

| claim | required evidence | current support | blocker |
|---|---|---|---|
| Kimberling's bounded-difference question for `A129259` is the exact target. | OEIS / Kimberling provenance and recurrence definition. | supported | none |

## 2. Baseline Generator And Reproducible Corpus

| claim | required evidence | current support | blocker |
|---|---|---|---|
| The repo contains a recurrence-validated generator with reproducible structural outputs. | `scripts/prime_separator.py`, tests, `contract.json`, `benchmark_report.md`. | supported | none |
| The record-gap corpus is witness-carrying rather than a pure term dump. | `record_gaps.json`, `record_gap_summary.json`, hypergraph exports. | supported | none |

## 3. H1: Frontier Witness Certificates

| claim | required evidence | current support | blocker |
|---|---|---|---|
| Raw witnesses compress into a compact T-specific certificate language. | Repeating witness families across late record gaps. | unsupported | current corpus shows heterogeneous mostly-singleton coverage |
| A weaker T-specific motif survives. | Stable axis-1 marker and consistent late-gap behavior. | supported | motif is too thin to settle boundedness |
| Full witness hypergraphs may still hide a rescuing invariant. | Hypergraph-level compression beyond first-witness data. | open but weak | no invariant extracted yet |

## 4. H2: Prime-Support Fixed Point

| claim | required evidence | current support | blocker |
|---|---|---|---|
| Prime-support observables predict record-gap growth better than witness logs. | Shared-corpus support metrics with stronger explanatory power than H1. | unsupported | composite-only large gaps and smooth support counts |

## 5. Negative Results / Dead Ends

| claim | required evidence | current support | blocker |
|---|---|---|---|
| Prime obstruction is the main mechanism. | Prime-heavy late record gaps. | rejected | large composite-only records already exist |
| A tiny-factor witness grammar stabilizes at scale. | Stable or rising tiny-factor share in late records. | rejected | balanced-factor share rises instead |
| Nearby admissibility perturbations destroy the qualitative picture. | Variant runs that remove large composite-only singleton-heavy gaps. | rejected | both perturbations preserve the negative-result profile |

## 6. Proof-Status Conclusion

| claim | required evidence | current support | blocker |
|---|---|---|---|
| The difference sequence is bounded. | Global upper-bound invariant or theorem. | unsupported | missing proof bridge |
| The difference sequence is unbounded. | Asymptotic divergence theorem or decisive counterexample scheme. | unsupported | finite record growth is not enough |
| Best current verdict is `still unresolved`. | Verification synthesis across baseline, variants, and mechanism claims. | supported | none |

## Sources

See `results/verification/claim_source_matrix.md` and `sources.bib`.
