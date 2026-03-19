# Phase 6 Metastability

## Exact Word Scan

- Family: `asym_a`.
- Word alphabet: `['S', 'D', 'P']` over `27` exact words.
- Best score word (one representative): `DPS` with `13/7 m=10 r=3 n=8 t=1`.
- Equal-best frontier words: `['DPS', 'PDS', 'SDP', 'SPD']`.
- Matched direct frontier representative: `SDP`.

## Negative Result

- Metastability has no predictive value on the frozen H6 grammar once exact extraction and matched direct controls are enforced. The best-score frontier is a four-word tie that already contains the matched direct control SDP, while high-closure failures remain present and do not produce exact certificates.
- Near-maximal closure-time failures: `['DDP', 'DDS', 'DPP', 'DSP', 'DSS', 'PDD', 'PPD', 'PPS', 'PSD', 'PSS', 'SDD', 'SPP', 'SSD', 'SSP']`.
- Why this is not bootstrap folklore: The metric is attached to exact forcing orders and exact certificate quality on a fixed grammar, not to macroscopic fill times or threshold behavior.

## Decision

- Exact dependency-hypergraph and closure-time summaries do not identify any certificate better than the already-matched direct frontier, so metastability is a red herring in this frozen regime.
