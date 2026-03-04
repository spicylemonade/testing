# Entropy-Adaptive Chunk Sizing

## Context

Speculative parallel parsing divides the input into fixed-size chunks. But JSON files have non-uniform structure: arrays of numbers have very different characteristics from objects with long string values. Fixed chunk sizes lead to suboptimal parallelism: too small in string-dense regions (high speculation misses), too large in structure-dense regions (insufficient parallelism).

## Key Insight

The speculation miss rate correlates with string density, which correlates with local byte entropy. Low-entropy regions (structural characters, short repeated keys) have low string density and thus low speculation miss rates. High-entropy regions (Base64 data, UUID strings, random text) have high string density. By adapting chunk sizes to entropy, we can maintain low miss rates while maximizing parallelism.

## Cross-Domain Bridges

- **Adaptive compression**: gzip adjusts its hash chain length based on compression ratio
- **TCP congestion control**: AIMD algorithm adapts window size based on packet loss (analogous to miss rate)
- **Adaptive mesh refinement**: FEM solvers use finer meshes where the solution changes rapidly

## Implementation Backlog

1. [ ] Profile speculation miss rates vs. chunk size on diverse JSON files
2. [ ] Compute byte entropy per 4KB block for representative JSON files
3. [ ] Correlate entropy with speculation miss rate empirically
4. [ ] Implement lightweight SIMD entropy estimator (byte frequency counting)
5. [ ] Design chunk boundary placement algorithm based on entropy profile
6. [ ] Benchmark adaptive vs. fixed chunk sizing
7. [ ] Measure load balance improvement across cores
8. [ ] Analyze overhead of the entropy pre-scan relative to parsing time
