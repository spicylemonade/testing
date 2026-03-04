# Prefix Scan Composition

## Topic Context

Parallel prefix scan (also called parallel prefix sum or scan) is one of the most
fundamental primitives in parallel computing. Given an associative operator ⊕ and a
sequence a_1, a_2, ..., a_n, it computes all prefix results:
  a_1, a_1⊕a_2, a_1⊕a_2⊕a_3, ..., a_1⊕...⊕a_n

The Ladner-Fischer construction achieves this in O(n) work and O(log n) depth,
which is work-optimal and depth-optimal.

The connection to Huffman decoding: each input bit defines a transition function
on the decoder's state space. The composition of transition functions is associative
(function composition is always associative). Therefore, parallel prefix scan can
compute the decoder state at every bit position in O(n * s) work and O(s * log n)
depth, where s is the state count.

The practical version divides the bitstream into chunks, computes per-chunk transitions
sequentially (cheap due to small chunk size), then does a parallel prefix scan across
chunks to propagate state information, and finally extracts symbols within each chunk
using the now-known start state.

## Key Challenges

- State count s can be up to 2^15 for DEFLATE Huffman codes
- Composition cost O(s) per merge makes large s impractical
- Need convergence-aware implementation to reduce effective s
- Chunk size tradeoff: small = more parallelism, large = less scan overhead

## Implementation Backlog

1. [ ] Implement sequential per-chunk transition function computation
2. [ ] Implement parallel prefix scan of transition functions
3. [ ] Use convergence detection to reduce state representation mid-scan
4. [ ] Benchmark across chunk sizes 64-4096 bits
5. [ ] Implement on both multi-core (pthread scan) and SIMD (intra-core scan)
6. [ ] Profile scan overhead vs. total decode time
7. [ ] Compare to alternative parallel Huffman methods (sync-point, speculation)
8. [ ] Evaluate for streaming vs. batch decode scenarios
