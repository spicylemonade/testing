# Concept: tzcnt_dependency_chain

- Topic Context: Branchless Binary GCD
- Domains: CPU pipeline analysis, instruction scheduling, loop optimization
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
The critical path in binary GCD is the loop-carried dependency chain: SUB -> TZCNT -> SARX -> next SUB. TZCNT has 3-cycle latency on modern Intel/AMD. Total chain is 5-7 cycles per iteration.

## Mathematical Formalization
Critical path: t_iter = lat(SUB) + lat(TZCNT) + lat(SARX) = 1 + 3 + 1 = 5 cycles (Skylake). With CMOV in chain: +1 cycle.

## Implementation Hypothesis
To break the chain: (1) speculative dual-path execution, (2) lookup table for small values, (3) move TZCNT before ABS to overlap with CMOV

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
