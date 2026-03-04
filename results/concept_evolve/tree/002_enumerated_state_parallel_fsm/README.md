# Enumerated State Parallel FSM

## Topic Context

Finite State Machine (FSM) computations appear inherently sequential because each
state depends on the previous one. However, Mytkowicz et al. (ASPLOS 2014) showed
a breakthrough: by enumerating transitions from ALL possible states simultaneously,
you create functions Q -> Q that compose associatively. This transforms FSM evaluation
into a parallel prefix problem, solvable in O(log n) depth.

For Huffman decoding specifically, the FSM reads one bit at a time and traverses a
binary tree. The state is the current node in the tree. When a leaf is reached, a symbol
is emitted and the state resets to the root. The enumerated approach processes each bit
against all ~2^L possible tree positions simultaneously.

The practical key insight is **convergence**: after processing enough bits, all starting
states map to the same state (because Huffman trees have bounded depth). This means
the effective state count shrinks rapidly, making the O(s^2) composition cost manageable.

## Key Challenges

- DEFLATE Huffman trees can have up to 15-bit codewords -> 2^15 = 32768 potential states
- SIMD register width limits how many states can be processed in parallel
- Convergence rate varies with Huffman table structure
- Memory cost of transition tables: O(s * |alphabet|) per composition step

## Implementation Backlog

1. [ ] Characterize convergence rates for real DEFLATE Huffman tables
2. [ ] Implement enumerated transition using AVX-512 VPGATHERDD
3. [ ] Implement parallel prefix composition of transition functions
4. [ ] Optimize for convergence: stop enumerating states that have merged
5. [ ] Benchmark against scalar Huffman decode on Zen4
6. [ ] Profile memory/cache behavior of transition tables
7. [ ] Explore hybrid: enumerated for first N bits until convergence, then scalar
8. [ ] Compare to Zhao & Shen's speculation-based approach on same benchmarks
