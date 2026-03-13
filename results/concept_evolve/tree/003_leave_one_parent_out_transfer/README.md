# Concept: leave_one_parent_out_transfer

- Route: H1
- Promotion Status: promoted on 2026-03-13
- Topic Context: Improve the Ramsey number R(5,5) bound
- Domains: statistical validation, software testing, Ramsey search
- Closest Prior Art: Study of Exoo's Lower Bound for Ramsey number R(5,5), Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)
- Experiment Seed: Hold out the most non-Exoo-like parent family and compare recurrence counts against the training-only atlas.

## Promotion Rationale
- Strongest discriminator between a structural Ramsey object and an overfit family-specific catalog.
- Sibling concepts: `orbit_stable_obstruction_atlas`, `minimal_core_canonicalization`, `witness_safe_filter_bank`.

## Implementation Backlog
- [ ] Materialize the exact input schema for this concept.
- [x] Attach one measurable executable test or audit table.
- [x] Record how this concept differs from the closest prior art in local artifacts.
- [x] Cross-link this concept to at least one sibling concept in the bridge graph.

## Executable Test
- Artifact targets: `results/h1/obstruction_cores.jsonl`, `results/h1/transfer_records.jsonl`
- Test: Hold out the most non-Exoo-like parent family, rebuild the atlas on the remaining families, and measure held-out recurrence and coverage retention.
- Pass signal: Held-out coverage remains at or above half of the training-side coverage, with zero witness-safety violations.
