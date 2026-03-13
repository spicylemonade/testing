# Concept: seed_family_diversification_audit

- Route: H1
- Promotion Status: promoted on 2026-03-13
- Topic Context: Improve the Ramsey number R(5,5) bound
- Domains: design theory, experimental design, Ramsey lower bounds
- Closest Prior Art: A lower bound for R(5,5), Study of Exoo's Lower Bound for Ramsey number R(5,5), Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)
- Experiment Seed: Compare atlas statistics under Exoo-only parents versus diversified parents.

## Promotion Rationale
- Negative-control bridge for the `anti_exoo_holdout` threat.
- Prevents the atlas from reading as a single-lineage Exoo memorizer.
- Sibling concepts: `orbit_stable_obstruction_atlas`, `leave_one_parent_out_transfer`, `witness_safe_filter_bank`.

## Implementation Backlog
- [ ] Materialize the exact input schema for this concept.
- [x] Attach one measurable executable test or audit table.
- [x] Record how this concept differs from the closest prior art in local artifacts.
- [x] Cross-link this concept to at least one sibling concept in the bridge graph.

## Executable Test
- Artifact targets: `results/h1/frontier_parents.jsonl`, `results/h1/transfer_records.jsonl`, `results/h1/atlas_summary.md`
- Test: Compare dominant canonical cores and coverage profiles under Exoo-only parents versus diversified parent families before and after leave-one-parent-out transfer.
- Pass signal: Core identities remain qualitatively stable across provenance classes, and held-out coverage stays at least 50 percent of training-side coverage with zero witness-safety violations.
