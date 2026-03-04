# Entropy-Guided Field Width Prediction

## Topic Context

Real-world CSV files contain columns with vastly different structural complexity. A column of 5-digit zip codes has near-zero entropy in field widths (always 5 bytes), while a free-text description column has high entropy. By measuring this entropy, we can route each column to the optimal extraction strategy.

This concept bridges information theory (Shannon entropy as a measure of predictability) with adaptive algorithm design (runtime selection of processing strategy).

## Key Insight

Shannon entropy of field widths directly predicts the effectiveness of fixed-offset extraction. H < 0.5 bits means >70% of values share the modal width, enabling a fast path that skips SIMD structural scanning for that column. The profiling cost (sampling 1024 rows) is amortized over millions of subsequent rows.

## Implementation Backlog

- [ ] Implement per-column field width histogram collection (first 1024 rows)
- [ ] Compute Shannon entropy per column
- [ ] Design threshold for fixed-width classification (H < 0.5 or configurable)
- [ ] Implement fixed-offset extraction fast path
- [ ] Implement regime-change detection (re-profile every N rows)
- [ ] Benchmark on diverse CSV types: all-numeric, mixed, all-text
- [ ] Profile the overhead of the sampling phase itself
- [ ] Compare against uniform SIMD extraction (no profiling)
