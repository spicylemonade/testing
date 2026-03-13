# Concept: minimal_core_canonicalization

- Route: H1
- Promotion Status: promoted on 2026-03-13
- Topic Context: Improve the Ramsey number R(5,5) bound
- Domains: graph isomorphism, combinatorics, proof certificates
- Closest Prior Art: Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t, A Formal Proof of R(4,5)=25
- Experiment Seed: Run canonicalization on all cores found in the first atlas pass and compare compression ratio before and after canon().

## Promotion Rationale
- Required to prevent fake recurrence caused by symmetry representatives or encoding differences.
- Sibling concepts: `orbit_stable_obstruction_atlas`, `leave_one_parent_out_transfer`, `witness_safe_filter_bank`.

## Implementation Backlog
- [ ] Materialize the exact input schema for this concept.
- [x] Attach one measurable executable test or audit table.
- [x] Record how this concept differs from the closest prior art in local artifacts.
- [x] Cross-link this concept to at least one sibling concept in the bridge graph.

## Executable Test
- Artifact targets: `results/h1/failure_witnesses.jsonl`, `results/h1/obstruction_cores.jsonl`
- Test: Canonicalize every failure witness from the first atlas pass, then compare pre- and post-canonicalization core counts.
- Pass signal: Core count shrinks by at least 2x while witness coverage stays unchanged and canonical hashes are stable under symmetry representatives.
