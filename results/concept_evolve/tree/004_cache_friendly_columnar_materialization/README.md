# Cache-Friendly Columnar Materialization

## Topic Context

Most CSV parsers produce row-oriented output: each row is a record with fields in order. However, modern analytics (pandas, Polars, Arrow, DuckDB) process data column-at-a-time. The row-to-column transposition is a hidden cost that traditional parsers force onto the consumer.

By materializing directly into columnar format during parsing, we eliminate this transposition cost and improve cache utilization. When writing to C column buffers with a batch size of 1024 rows, each column buffer fits in L1/L2 cache, resulting in near-optimal spatial locality.

## Key Insight

The classic AoS-to-SoA transformation from game engine development applies directly: instead of storing Row{field1, field2, field3}, store Column1{row1, row2, ...}, Column2{row1, row2, ...}. This is a fundamental cache optimization that yields 2-5x improvements in downstream processing.

## Implementation Backlog

- [ ] Design column buffer allocation strategy (pre-allocate vs. grow)
- [ ] Implement Arrow StringArray output (offsets + data buffer)
- [ ] Implement Arrow PrimitiveArray output for numeric columns
- [ ] Batch processing: accumulate 1024 rows before emitting a RecordBatch
- [ ] Cache-line alignment for column buffers to prevent false sharing
- [ ] Integrate with Arrow C Data Interface for zero-copy handoff to Python/R
- [ ] Profile cache behavior with perf stat on various CSV shapes
- [ ] Compare materialization throughput: row-major vs. columnar
