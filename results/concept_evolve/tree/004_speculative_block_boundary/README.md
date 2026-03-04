# Speculative Block Boundary

## Topic Context

DEFLATE streams are sequences of compressed blocks. Each block contains its own
Huffman tables (for dynamic blocks) or uses fixed tables. The critical problem:
you cannot know where block N+1 starts until you have fully decoded block N, because
the block doesn't encode its compressed size.

This is directly analogous to branch prediction in CPUs. We can speculate where
the next block boundary is, start decoding there speculatively, and validate once
the actual boundary is known. If the speculation is wrong, we discard and retry.
If correct, we've gained parallel speedup.

The pugz and rapidgzip projects have demonstrated this approach in practice.
pugz was limited to ASCII text (exploiting known byte value ranges for validation),
while rapidgzip generalized to arbitrary data using a cache-and-prefetch architecture.

## Key Challenges

- Block boundaries are not self-evident in the bitstream (no unique marker pattern)
- Validation requires attempting to parse a block header, which can false-positive
- Block size distributions vary widely across file types
- Speculation memory overhead: each speculative thread needs its own output buffer
- Coordination between sequential and speculative threads adds complexity

## Implementation Backlog

1. [ ] Analyze block size distributions for common file types (text, binary, genomic)
2. [ ] Implement block header validation heuristic (HLIT/HDIST/HCLEN range checks)
3. [ ] Build adaptive block size predictor (EMA, histogram-based, neural)
4. [ ] Implement 2-thread speculative decoder with commit/rollback
5. [ ] Extend to N-thread with multiple simultaneous speculations
6. [ ] Measure speculation accuracy and net speedup across Silesia corpus
7. [ ] Compare to rapidgzip's approach on same test files
8. [ ] Profile thread synchronization overhead on Zen4 (cross-CCD latency)
