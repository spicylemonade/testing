# Recursive Bit-Tree Sieve

## Topic Context

The Collatz conjecture verification problem requires checking that all integers below some bound N eventually reach 1 under the map T(n) = n/2 (even) or (3n+1)/2 (odd). The naive approach iterates T for each integer independently. The **recursive bit-tree sieve** transforms this into a binary tree search over the bit positions of n, exploiting the fact that T^k(n) depends only on the last k bits of n (Lemma 2.1, Wirsching 1998).

Angeltveit (2026) introduced this as Algorithm 2: start with the least significant bit and recursively extend, applying multiple pruning sieves at each node. Survivors at depth N-A are passed to GPU-based bitvector sieving and iterative verification.

Key insight: the fraction of integers surviving all sieves decreases as N grows (~1.9x per additional bit), meaning the algorithm becomes more efficient for larger verification targets.

## Cross-Domain Bridges

- **Tree search algorithms**: The bit-tree is a specific instance of branch-and-bound with domain-specific pruning rules
- **IP routing / binary tries**: Each bit of n determines a branch, analogous to longest-prefix-match in networking
- **Combinatorial optimization**: The multiple sieves correspond to different bounding functions in B&B

## Implementation Backlog

- [ ] Implement basic recursive bit-tree with Descent Sieve only (Rust, CPU)
- [ ] Add Path-Merging Sieve using mod-3 counter (Lemma 2.8)
- [ ] Add Odd-Even-Even Sieve using state machine
- [ ] Validate survivor count at N=40 against Angeltveit's 756,583,624
- [ ] Profile recursion depth and memory usage for N=50..60
- [ ] Implement GPU dispatch: collect survivors at depth N-A, batch by f-value
- [ ] Port Step 1 to multi-threaded CPU with work-stealing for independent subtrees
- [ ] Compare against Barina's flat sieve approach for equivalent N
