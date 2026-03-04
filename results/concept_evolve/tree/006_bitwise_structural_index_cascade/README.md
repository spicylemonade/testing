# Bitwise Structural Index Cascade

## Context

The key insight from Mison and simdjson is that JSON parsing can be decomposed into bitwise operations on bitmaps derived from the input. Each 64-byte input block produces several 64-bit bitmaps (one bit per input byte), and these bitmaps are combined through a cascade of bitwise operations to produce the final structural index.

## Key Insight

The entire structural index cascade — from raw input bytes to final structural character positions — can be expressed as ~12 instructions per 64 bytes. This is near the theoretical minimum: you need at least 1 comparison per character class and 1 prefix operation for string state. The cascade is a pure combinational function (no conditional branches, no memory access for intermediates).

## Cross-Domain Bridges

- **Digital circuit design**: the cascade is essentially a combinational logic circuit implemented in SIMD instructions
- **Carry-lookahead adders**: prefix-XOR for string state uses the same algebraic structure as carry-lookahead
- **Coding theory**: structural characters serve as "synchronization markers" similar to sync words in frame-based protocols

## Implementation Backlog

1. [ ] Enumerate the minimal instruction sequence for the full cascade
2. [ ] Implement in AVX-512 with explicit register allocation
3. [ ] Measure instructions/byte with perf stat
4. [ ] Profile with VTune to verify no cache pollution from intermediates
5. [ ] Compare against simdjson's existing bitmap cascade
6. [ ] Explore vpternlog to fuse 3-input boolean operations (reduce instruction count further)
7. [ ] Analyze the cascade's critical path length (determine throughput vs. latency bottleneck)
8. [ ] Port to ARM NEON and measure instruction count difference
