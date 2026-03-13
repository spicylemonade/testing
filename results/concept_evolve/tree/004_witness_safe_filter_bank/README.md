# Concept: witness_safe_filter_bank

- Route: H1
- Promotion Status: promoted on 2026-03-13
- Topic Context: Improve the Ramsey number R(5,5) bound
- Domains: formal methods, search pruning, computational combinatorics
- Closest Prior Art: R(5,5) <= 46, Decreasing the upper bound on the Ramsey number R(5,5), Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t
- Experiment Seed: Create a witness-survival matrix with rows = known witnesses and columns = candidate filters.

## Promotion Rationale
- Prevents the atlas from becoming an unsound pruning story.
- Sibling concepts: `orbit_stable_obstruction_atlas`, `minimal_core_canonicalization`, `leave_one_parent_out_transfer`.

## Implementation Backlog
- [ ] Materialize the exact input schema for this concept.
- [x] Attach one measurable executable test or audit table.
- [x] Record how this concept differs from the closest prior art in local artifacts.
- [x] Cross-link this concept to at least one sibling concept in the bridge graph.

## Executable Test
- Artifact targets: `results/h1/witness_safety_audit.md`, `results/h1/transfer_records.jsonl`
- Test: Build the witness-survival matrix with rows = known 42/43 witnesses and columns = candidate core-derived filters, then run an on/off ablation on the same rung.
- Pass signal: Zero witness kills and a measurable reduction in failure cases relative to the no-filter baseline.
