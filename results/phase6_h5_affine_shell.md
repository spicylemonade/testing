# Phase 6 H5 Affine-Core / Nonlinear-Shell Audit

## Frozen Audit

- Geometry: `height 2, width 4`.
- Families: `['asym_a', 'asym_b', 'asym_c']`.
- Affine core symbols: `['closed', 'top', 'bottom']`.
- Nonlinear shell symbols: `['gate_up', 'gate_down']`.
- Seed budget: `4`; initial-T budget: `1`; boundary band: `1`.
- Direct-search RNG seeds: `[6201, 6202]` with `20` exact trials per seed.

## Family Results

### asym_a

- Canonical shell words checked: `39`.
- Forcing words by shell size: `{'0': 0, '1': 0, '2': 0, '3': 0}`.
- Affine-only hit rate: `0.0000`.
- Any-shell hit rate: `0.0000`.
- Matched direct hit rate: `0.2000` over `40` exact trials.
- Best matched direct certificate: `13/7 m=10 r=3 n=8 t=1`.

### asym_b

- Canonical shell words checked: `39`.
- Forcing words by shell size: `{'0': 0, '1': 0, '2': 0, '3': 0}`.
- Affine-only hit rate: `0.0000`.
- Any-shell hit rate: `0.0000`.
- Matched direct hit rate: `0.2000` over `40` exact trials.
- Best matched direct certificate: `13/7 m=10 r=3 n=8 t=1`.

### asym_c

- Canonical shell words checked: `39`.
- Forcing words by shell size: `{'0': 0, '1': 0, '2': 0, '3': 0}`.
- Affine-only hit rate: `0.0000`.
- Any-shell hit rate: `0.0000`.
- Matched direct hit rate: `0.2000` over `40` exact trials.
- Best matched direct certificate: `14/7 m=10 r=4 n=8 t=1`.

## Obstruction

- Across asym_a, asym_b, and asym_c, the frozen two-gate shell library produces zero exact forcing width-4 words under the H4 budgets, while same-budget unrestricted direct search finds forcing certificates on every family. Therefore the audited bounded shell library does not improve hit rate or score over either the affine core or the matched direct no-CA baseline.
- Direct-search wins occur on: `['asym_a', 'asym_b', 'asym_c']`.
- Scale-up verdict: Shell size does not stay bounded under scale-up in any reusable sense: there is no width-4 base witness to lift, so any wider positive claim would have to add new nonlinear motifs or change the extractor.

## Novelty Position

- This is not generic SAT controller search because no solver is allowed to invent new local rules or boundary privileges; the audit freezes the extractor and checks the full tiny-instance shell alphabet exactly. It is not abelian-network relabeling because the comparison is between local mixed-row gate motifs and exact certificate outcomes, not between alternative global invariant packages.
