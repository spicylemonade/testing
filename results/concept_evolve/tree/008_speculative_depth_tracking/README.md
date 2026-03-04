# Speculative Depth Tracking

## Context

JSON nesting depth tracking is inherently sequential: the depth at position i depends on all opening/closing brackets before i. This creates a data dependency that limits parallelism. However, depth changes are simple +1/-1 increments, making them amenable to parallel prefix-sum — one of the most fundamental and well-studied parallel algorithms.

## Key Insight

Each chunk's contribution to depth is a simple integer (net open brackets minus close brackets). The parallel prefix-sum over these integers gives absolute depth at every chunk boundary in O(log P) steps. The minimum relative depth within each chunk validates that no intermediate position underflows to negative depth.

## Cross-Domain Bridges

- **Parallel prefix-sum (Blelloch 1990)**: the workhorse of parallel computing; depth tracking is a direct instance
- **GPU parallel scan**: highly optimized implementations on CUDA (CUB library) and OpenCL
- **Compiler dependence breaking**: transforms a sequential loop-carried dependency into a parallel reduction

## Implementation Backlog

1. [ ] Implement per-chunk depth metadata computation using VPOPCNTDQ
2. [ ] Implement Blelloch parallel prefix-sum for chunk metadata
3. [ ] Build absolute-depth array at chunk boundaries
4. [ ] Implement binary-search skip_value() using depth array
5. [ ] Benchmark against sequential depth tracking
6. [ ] Measure parallel speedup scaling with core count
7. [ ] Test on deeply nested JSON (max depth 100+)
8. [ ] Integrate with lazy materialization pointer machine (concept 5)
