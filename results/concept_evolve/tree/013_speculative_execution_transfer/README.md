# Speculative Execution Transfer

## Cross-Domain Connection

Speculative execution in modern CPUs is the closest architectural analogy to speculative row-length prediction in SIMD CSV parsing. Both systems face the same fundamental tradeoff: pay a small cost to predict and verify, or pay a large cost to compute sequentially. This concept node deepens the analogy by transferring three specific mechanisms from adjacent domains.

**CPU Branch Prediction to Row-Length Prediction.** The parser's EWMA predictor is a first-order linear filter, analogous to a bimodal (2-bit saturating counter) branch predictor. CPU architects learned decades ago that correlating prediction with recent history dramatically improves accuracy. A 2-level adaptive predictor, indexed by a hash of the last K row-length quantiles, could capture periodic patterns (e.g., alternating short/long rows in key-value exports) that EWMA smooths away. The reorder buffer analogy maps directly: speculative field outputs are staged in a tentative buffer and retired (committed) only after boundary verification.

**Network Protocol Dissectors to Multi-Template Parsing.** Wireshark and nDPI run candidate dissectors in parallel when a flow's protocol is ambiguous. Similarly, CSV files with mixed row types (headers, data, comments, annotations) exhibit multimodal row-length distributions. Running 2-4 candidate templates in parallel and committing the best match transfers the "speculative multi-dissector" pattern to parsing.

**Profile-Guided Optimization to Runtime Specialization.** Compilers use profiling to speculate on hot paths. A CSV parser can profile the first 1024 rows, compile a specialized SIMD kernel (fixed-offset gathers), and guard it with a lightweight verification check. This eliminates per-row prediction arithmetic on the fast path while preserving correctness via fallback.

## Proposed Transfers

Each transfer produces a falsifiable hypothesis. H1 (2-level predictor) targets variable-width files. H2 (multi-template) targets multimodal distributions. H3 (profile-then-specialize) targets homogeneous files where prediction overhead itself becomes the bottleneck. Together, they cover the full spectrum of real-world CSV regularity.

## Implementation Backlog

- [ ] Implement 2-level adaptive row-length predictor with configurable history depth
- [ ] Implement checkpoint-and-restore for speculative output buffer (ROB analogy)
- [ ] Implement online k-means (k=2,3,4) for multi-template row prediction
- [ ] Implement profile-then-specialize pipeline with SIMD gather fast path
- [ ] Benchmark all three approaches against EWMA baseline on 5+ datasets
- [ ] Measure misprediction recovery cost in cycles via hardware perf counters
