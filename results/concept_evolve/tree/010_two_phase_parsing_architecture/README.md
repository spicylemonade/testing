# Two-Phase Parsing Architecture

## Topic Context

The two-phase architecture is the organizing principle of the entire SIMD CSV parser. Phase 1 is a fast, streaming scan that produces a structural index (array of byte offsets for every field and row boundary). Phase 2 reads this index to extract, convert, and materialize field values into columnar output.

This separation has profound implications: Phase 1 is memory-bandwidth-bound and benefits from SIMD width; Phase 2 is compute-bound and benefits from multi-threading across columns.

## Key Insight

Phase 1 throughput is limited by memory bandwidth (~20-50 GB/s on modern systems), while Phase 2 can be parallelized across columns. The structural index is compact (4 bytes per field boundary) and fits in cache. This means Phase 2 operates mostly from L1/L2 cache on the index, only touching main memory for the actual field data.

## Implementation Backlog

- [ ] Define structural index format: Vec<u32> for field offsets, Vec<u32> for row offsets
- [ ] Implement Phase 1 SIMD indexer using concepts 001-005
- [ ] Implement Phase 2 columnar extractor using concept 004
- [ ] Add thread pool for parallel Phase 2 column extraction
- [ ] Benchmark Phase 1 / Phase 2 split on various file sizes and column counts
- [ ] Implement streaming mode: Phase 1 + Phase 2 on overlapping windows
- [ ] Integrate with Arrow RecordBatch for zero-copy output
- [ ] Compare end-to-end against pandas, pyarrow, polars, arrow-csv, xsv
