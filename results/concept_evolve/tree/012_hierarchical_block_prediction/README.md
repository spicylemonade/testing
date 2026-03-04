# Hierarchical Block Prediction

## Context

DEFLATE streams consist of multiple blocks, each with its own Huffman table (for dynamic blocks). Building the decode table from the code lengths in the block header takes ~1000-2000 cycles, which can be a significant fraction of total decode time for small blocks.

In practice, consecutive DEFLATE blocks from the same compressor often have very similar or identical Huffman tables, especially for homogeneous data (XML, source code, logs). This temporal locality can be exploited.

## Prediction Strategies

### 1. Table Caching
Cache the most recently used decode table. When parsing a new dynamic block header, compare the code length sequence to the cached table's code lengths. If identical, skip the O(n) table build.

### 2. Table Similarity Detection
Even if tables are not identical, they may be "close enough" that a cached table produces correct (but suboptimal) decoding. However, for DEFLATE, the table must be exact - there's no concept of "close enough" for correctness. But we can speculatively start decoding with the cached table while building the new one in parallel.

### 3. Block Size Prediction
If consecutive blocks have similar sizes, we can predict the next block boundary and begin scanning for its header before the current block is fully decoded. Combined with sync-point discovery, this enables block-level pipelining.

## Cross-Domain Connection: Video Coding

In H.264/H.265, frame headers are predicted from previous frames (temporal prediction). The analogous technique here predicts DEFLATE block metadata from previous blocks in the same stream.

## Implementation Backlog

- [ ] Instrument a DEFLATE decoder to log block-by-block Huffman table statistics
- [ ] Measure inter-block table similarity across Silesia corpus
- [ ] Implement table caching with O(1) comparison (hash the code length sequence)
- [ ] Benchmark table build time as fraction of total decode time by block size
- [ ] Implement speculative decode with cached table + background table rebuild
- [ ] Test on streaming workloads (HTTP compressed responses, log files)
