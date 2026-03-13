# Concept: orbit_stable_obstruction_atlas

- Route: H1
- Promotion Status: promoted on 2026-03-13
- Topic Context: Improve the Ramsey number R(5,5) bound
- Domains: Ramsey theory, computational group theory, graph mining
- Closest Prior Art: Study of Exoo's Lower Bound for Ramsey number R(5,5), Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t, R(5,5) <= 46
- Experiment Seed: Use the saved Exoo/Ge/Lehavi line as the initial parent set and measure how many failed extensions are covered by the top-k cores.

## Promotion Rationale
- Primary object-level H1 concept.
- Novelty-safe only when the atlas transfers across parent families and survives witness-safety checks.
- Sibling concepts: `minimal_core_canonicalization`, `leave_one_parent_out_transfer`, `witness_safe_filter_bank`.

## Implementation Backlog
- [ ] Materialize the exact input schema for this concept.
- [x] Attach one measurable executable test or audit table.
- [x] Record how this concept differs from the closest prior art in local artifacts.
- [x] Cross-link this concept to at least one sibling concept in the bridge graph.

## Executable Test
- Artifact targets: `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, `results/h1/failure_witnesses.jsonl`, `results/h1/obstruction_cores.jsonl`
- Test: Materialize the first Exoo/Ge/Lehavi atlas packet and measure top-25 core coverage on orbit-distinct failures.
- Pass signal: At least 30 percent coverage across at least 3 non-isomorphic parent families, with zero witness-safety violations on the saved 42/43 safety set.
