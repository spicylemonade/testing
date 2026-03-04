# Fused Tokenize-Validate Pass

## Context

simdjson's Stage 1 performs multiple logically independent operations: structural character detection, string boundary tracking, UTF-8 validation, and escape sequence processing. While these operations are interleaved to some degree, they still involve multiple conceptual passes over the data, and intermediate results may evict each other from L1 cache for large inputs.

GPU kernel fusion demonstrates that combining multiple operations into a single kernel dramatically reduces memory traffic. The same principle applies to CPU SIMD: fuse all Stage 1 operations into a single tight loop iteration that loads each 64-byte block exactly once and produces all outputs from registers.

## Key Insight

AVX-512 provides 32 zmm registers (2048 bytes of register file). The fused pass needs ~20 registers for all concurrent operations, leaving room for software pipelining. The operations are independent within a 64-byte block, so they can execute without data hazards.

## Cross-Domain Bridges

- **GPU kernel fusion**: eliminate intermediate memory traffic by keeping data in shared memory/registers
- **Database push-based execution**: Neumann's HyPer compiles query plans into tight loops that fuse operators
- **Camera ISP pipelines**: fuse debayer + denoise + tone-map in one pass over sensor data

## Implementation Backlog

1. [ ] Profile simdjson Stage 1 to identify cache miss patterns between sub-operations
2. [ ] Design the fused iteration: list all register inputs/outputs per 64-byte block
3. [ ] Verify register pressure with 32 zmm registers (count live registers at each point)
4. [ ] Implement the fused loop in AVX-512 intrinsics
5. [ ] Benchmark: instructions/byte, L1 misses/byte, throughput
6. [ ] Compare against simdjson's existing Stage 1 on multiple input sizes
7. [ ] Test the boundary between L1-resident and L2-resident inputs
8. [ ] Explore software pipelining: load block N+1 while processing block N
