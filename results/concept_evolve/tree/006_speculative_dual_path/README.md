# Concept: speculative_dual_path

- Topic Context: Branchless Binary GCD
- Domains: speculative execution, instruction-level parallelism, branch prediction
- Purpose: Treat this concept as a software module with iterative implementation and tests.

## Description
Execute two loop bodies: one assuming ctz=1, one computing actual ctz. Select correct result via CMOV. Overlaps iterations.

## Mathematical Formalization
Speculate: diff1 = (a-b)>>1. Actual: ctz=tzcnt(a-b); diff_actual=(a-b)>>ctz. result = (ctz==1)?diff1:diff_actual.

## Implementation Hypothesis
ctz=1 occurs ~50% of the time for random inputs. When correct, save TZCNT latency from critical path.

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Add measurable experiment and result file under this folder.
- [ ] Add citations from literature.json to sources.bib.
