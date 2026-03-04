# SIMD Multi-Table Decode

## Topic Context

Fabian Giesen showed that decoding multiple independent Huffman streams simultaneously
achieves near-linear ILP speedup: if you have 4 independent streams, 4 table lookups
can be in-flight simultaneously in the CPU pipeline, hiding memory latency.

The SIMD multi-cursor approach extends this to a SINGLE stream by exploiting the
bounded codeword length. Since codewords are at most L bits long, if you start decode
attempts at offsets {cursor, cursor+1, ..., cursor+L-1}, one of them will be at the
correct next boundary. This is essentially the sync-point convergence idea applied
at the per-symbol level.

Each SIMD lane reads bits from a different offset and does a table lookup. When the
current symbol's length is known, the valid lanes are identified and their results
extracted. Remaining lanes are discarded or recycled.

On AVX-512 with 16x32-bit lanes and max codeword length 15, you can theoretically
decode ~16/E[L] symbols per SIMD operation, which for typical E[L]~7 gives ~2.3
symbols per op — a significant improvement over scalar's 1 symbol per ~5 ops.

## Key Challenges

- VPGATHERDD latency is high (~20 cycles on Zen4), limiting throughput
- Table must be in L1 cache for gather to be fast
- Validation logic (which lane has the valid next symbol?) adds overhead
- Only useful when the table lookup is the bottleneck (not bit manipulation)

## Implementation Backlog

1. [ ] Implement AVX-512 multi-cursor Huffman decode prototype
2. [ ] Benchmark VPGATHERDD throughput vs. scalar table lookup on Zen4/SPR
3. [ ] Implement lane validation using mask registers
4. [ ] Measure symbols per SIMD instruction across different entropy levels
5. [ ] Compare to multi-independent-stream approach (Giesen's method)
6. [ ] Profile cache miss rates for different table sizes
7. [ ] Explore VPCONFLICTD for detecting duplicate offsets (convergence)
8. [ ] Test on real DEFLATE blocks integrated with LZ77 resolution
