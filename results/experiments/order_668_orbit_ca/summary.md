# Orbit Quotient CA Summary

Fixed orbit-level rule table over symmetry-quotient representatives of the retained composite library.

## Setup

- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Retained library: `results/analysis/composite_packet_retained_library.json`
- Perturbation suite: `results/experiments/order_668_hypergraph_ca/perturbation_ladder.json`
- Rule-table size: `137` orbit signatures.
- Lookup budget per run: `256`.

## Outcomes

- `canonical_frontier`: orbit `13/2744/480` (updates `1`, lookups `65`), raw `13/2880/512`, scorer_only `13/2880/512`.
- `barrier_ladder_01`: orbit `13/2880/512` (updates `1`, lookups `60`), raw `14/2812/496`, scorer_only `14/2812/496`.
- `barrier_ladder_02`: orbit `13/2744/480` (updates `1`, lookups `72`), raw `14/2820/496`, scorer_only `14/2820/496`.
- `barrier_ladder_03`: orbit `13/2744/480` (updates `1`, lookups `64`), raw `15/2408/416`, scorer_only `15/2408/416`.
- `barrier_ladder_04`: orbit `13/2744/480` (updates `1`, lookups `70`), raw `15/2408/416`, scorer_only `15/2408/416`.
- `barrier_ladder_05`: orbit `13/2744/480` (updates `2`, lookups `98`), raw `15/2544/448`, scorer_only `15/2544/448`.

## Leakage Audit

- Reused frontier leakage audit: `results/verification/family_leakage_audit.json`.
- The winning orbit trajectory lands in the same frontier state audited in item_029, so the full Williamson/Turyn/Goethals-Seidel/cocyclic/block-circulant pass carries over unchanged.

## Verdict

- Orbit CA beats both the raw-coordinate baseline and scorer_only on `6` of `6` frontier states, including the canonical seed.
