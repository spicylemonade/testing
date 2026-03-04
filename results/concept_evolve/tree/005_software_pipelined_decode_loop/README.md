# Software Pipelined Decode Loop

## Context

A Base64 SIMD decode iteration has 4 distinct phases: (1) Load 64 input bytes, (2) Lookup/validate characters, (3) Pack 6-bit values into bytes, (4) Store 48 output bytes. Each phase uses different execution units and has multi-cycle latency. In a naive loop, the CPU must wait for each phase to complete before starting the next, leaving execution units idle.

Software pipelining interleaves phases from different iterations: while iteration N is in the pack phase, iteration N+1 is in the lookup phase, and iteration N+2 is in the load phase. This keeps all execution units busy simultaneously.

## Key Insight

The Base64 decode pipeline has no inter-iteration data dependencies (each 64-byte block is independent), making it an ideal candidate for software pipelining. The only constraint is register pressure: the pipelined loop must hold data for 3-4 iterations simultaneously.

## Implementation Backlog

- [ ] Profile the unpipelined loop to identify the bottleneck phase (likely lookup or pack)
- [ ] Implement 4-deep software-pipelined loop with explicit register allocation
- [ ] Measure IPC improvement with perf stat
- [ ] Test on both Intel (deep OOO buffer) and AMD (different scheduler) architectures
- [ ] Explore compiler-assisted pipelining using #pragma unroll + reordering
- [ ] Combine with prefetch instructions for L2-to-L1 data movement overlap
