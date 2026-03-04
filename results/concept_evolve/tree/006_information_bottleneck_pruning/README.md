# Information Bottleneck Pruning

## Topic Context

The Information Bottleneck (IB) method, introduced by Tishby et al. (2000), formalizes
the tradeoff between compression and relevance: given input X and relevant variable Y,
find a compressed representation T that preserves I(T;Y) while minimizing I(X;T).

Applied to the DEFLATE parallel decoding problem, X represents bit positions in the
compressed stream, and Y represents whether a given position is a symbol boundary.
Not all bit positions are equally informative about boundaries. For example, the first
bit of a long codeword is highly diagnostic (it determines a specific subtree), while
bits deep in a uniform-depth region are less so.

This analysis has two applications:
1. **Probe placement**: In sync-point convergence, place probes at positions with high
   I(bit; boundary) rather than uniformly, reducing average convergence distance.
2. **State pruning**: In enumerated-state FSM decode, prune states with low posterior
   probability, reducing the state count from 2^L to a manageable number.

## Key Challenges

- Computing I(bit_k; boundary) requires knowledge of the Huffman table and source statistics
- The IB optimization is NP-hard in general; practical approximations needed
- Overhead of information-based reasoning must be amortized over many symbols
- Different Huffman tables per DEFLATE block change the information landscape

## Implementation Backlog

1. [ ] Compute per-bit-position mutual information for representative Huffman tables
2. [ ] Derive closed-form approximation for I(bit_k; boundary) for canonical Huffman codes
3. [ ] Implement information-weighted probe placement strategy
4. [ ] Benchmark convergence improvement vs. uniform placement
5. [ ] Implement posterior-based state pruning for enumerated FSM decode
6. [ ] Measure state count reduction and throughput impact
7. [ ] Test generalization: train on one file type, evaluate on another
8. [ ] Compare to simpler heuristics (e.g., prune states by tree depth)
