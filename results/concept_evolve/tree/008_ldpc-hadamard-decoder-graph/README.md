# Concept: ldpc_hadamard_decoder_graph

- Topic Context: solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it
- Domains: coding_theory, ldpc, cellular_automata
- Status: promoted bridge candidate feeding the H2 pivot.

## Implementation Backlog
- [ ] Derive a sparse defect-packet or defect-check graph from retained low-splash composite packets.
- [ ] Benchmark weighted bit-flip, warning-propagation, and CA-actuated updates on the same graph for solved controls first.
- [ ] Measure sparsification error, locality leakage, and exact reconstruction quality before any frontier claim.
- [ ] Use this bridge as a preconditioner or side-field candidate unless it survives the exact-hit benchmark directly.

## Promotion Note

- Evidence path:
  - `results/concept_evolve/reframings.json`
  - `results/concept_evolve/bridge_candidates.json`
  - `results/verification/benchmark_report.md`
- Promotion reason:
  - the reframe and iterate passes both push the search toward a syndrome-graph / decoder interpretation
  - this is the strongest representation-changing bridge that still preserves a local-update story
