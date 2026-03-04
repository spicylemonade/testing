# Information-Directed Branch Pruning

## Topic Context

The recursive bit-tree in Angeltveit's algorithm is currently traversed via DFS, which is simple but does not optimize for CPU-GPU pipeline overlap. An information-directed approach would prioritize exploring branches that are most likely to produce GPU work items, keeping the GPU busy while the CPU continues exploring.

This concept bridges information theory (quantifying the informativeness of each branch decision) with the practical need for CPU-GPU pipeline concurrency.

## Cross-Domain Bridges

- **Bandit algorithms**: Information-directed sampling maximizes information about the optimum
- **A* search**: Admissible heuristics guide exploration toward solutions
- **Compiler scheduling**: Instruction scheduling overlaps computation with memory access

## Implementation Backlog

- [ ] Compute expected survivor counts per f-value from bitvector densities
- [ ] Implement priority queue for bit-tree traversal ordered by f and dip
- [ ] Add asynchronous GPU kernel launch when batch of 2^16 survivors ready
- [ ] Measure CPU-GPU overlap ratio vs DFS approach
- [ ] Profile peak memory usage (priority queue may be large)
- [ ] Test whether BFS ordering provides better GPU utilization than DFS
