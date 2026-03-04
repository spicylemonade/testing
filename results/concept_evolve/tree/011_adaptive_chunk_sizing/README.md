# Adaptive Chunk Sizing

## Topic Context

Different regions of a CSV file have different structural complexity. Regions with no quotes are trivially parseable at maximum SIMD width. Regions with dense quoting require more careful state tracking that may benefit from smaller processing chunks.

This concept is inspired by adaptive mesh refinement (AMR) in computational fluid dynamics, where fine grids are used near boundaries and shock waves while coarse grids suffice in smooth regions. The "shock wave" analogy in CSV is a quoted field with embedded delimiters.

## Key Insight

The overhead of CLMUL carry propagation and quote-state management scales with chunk count, not chunk size. Larger chunks amortize this overhead but may waste cycles on bytes that don't need careful analysis. Matching chunk size to local complexity optimizes the throughput-accuracy trade-off.

## Implementation Backlog

- [ ] Implement quote density computation per 64-byte block (POPCNT on quote bitmask)
- [ ] Define density thresholds for chunk size selection
- [ ] Implement dual-path processing: W_max for clean regions, W_min for complex
- [ ] Profile overhead of adaptive switching vs. fixed-width processing
- [ ] Test on CSV with clustered quoting patterns (columns, regions)
- [ ] Evaluate whether the CLMUL approach already handles dense quotes efficiently enough to make adaptivity unnecessary
