# Speculative Row Length Prediction

## Topic Context

Real-world CSV files exhibit strong statistical regularity in row lengths. Database tables with consistent column types produce rows of similar byte widths. This regularity can be exploited to predict where the next row starts before actually scanning to it, enabling prefetch instructions and speculative parallel processing.

This technique is inspired by two cross-domain sources: (1) CPU branch prediction, which speculatively executes the predicted path and rolls back on misprediction, and (2) Mison's speculative field location for JSON parsing.

## Key Insight

If we can predict the next row's starting byte offset with high accuracy, we can issue cache prefetch instructions to ensure the data is in L1/L2 by the time the structural indexer reaches it. More aggressively, we can start SIMD structural detection at the predicted offset in parallel with the current row's processing, achieving instruction-level parallelism.

## Implementation Backlog

- [ ] Implement exponential moving average (EMA) row length predictor
- [ ] Implement median-of-last-8 predictor for robustness
- [ ] Add PREFETCHNTA instruction emission at predicted offsets
- [ ] Implement speculative parallel row processing (process 4 predicted rows ahead)
- [ ] Add verification logic: check that predicted newline position contains actual newline
- [ ] Implement rollback mechanism for mispredictions
- [ ] Profile prediction accuracy on diverse CSV datasets
- [ ] Measure cache miss reduction via hardware performance counters
- [ ] Compare throughput with/without speculation on real datasets
