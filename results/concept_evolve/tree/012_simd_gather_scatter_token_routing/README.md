# SIMD Gather-Scatter Token Routing

## Context

JSON parsers that use a structural index must traverse the index to visit each structural character position. In simdjson, this traversal is sequential: load the next index entry, jump to that input position, classify the character, process the value, repeat. This creates a pointer-chasing pattern that is difficult for the CPU to pipeline and prefetch.

## Key Insight

AVX-512 VPGATHERDQ can load 8 non-contiguous 64-bit values in a single instruction using an index register. By loading 8-16 structural index entries at once and gathering the corresponding input bytes in parallel, we can classify and begin processing multiple tokens simultaneously. This transforms pointer-chasing into batch processing.

## Cross-Domain Bridges

- **Network packet switching**: packets arrive at scattered input ports and are routed to scattered output ports; the gather-scatter operation is the SIMD equivalent
- **Vectorized database execution**: MonetDB/X100 processes column vectors through SIMD primitives rather than row-at-a-time interpretation
- **GPU coalesced memory access**: GPUs achieve peak bandwidth when threads access contiguous memory; gather-scatter optimizes non-contiguous CPU access patterns

## Implementation Backlog

1. [ ] Microbenchmark VPGATHERDQ latency/throughput on target architectures
2. [ ] Implement batch structural index loading (16 entries per batch)
3. [ ] Implement parallel token classification using gathered first-bytes
4. [ ] Add SIMD inline number parsing for integer-dense JSON
5. [ ] Benchmark against sequential structural index traversal
6. [ ] Test on different JSON shapes: arrays of integers, arrays of objects, deep nesting
7. [ ] Measure memory bandwidth utilization vs. theoretical peak
8. [ ] Combine with runahead prefetching (concept 11) to prime cache for gathers
