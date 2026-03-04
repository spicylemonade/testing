# Cache Prefetch Speculation

## Topic Context

The fundamental challenge of parallel DEFLATE decompression is that you can't know
where to start decoding block N+1 without finishing block N. Rapidgzip (Knespel &
Brunst, 2023) solved this with an architecture borrowed from CPU cache design:

1. **Speculative prefetcher**: Multiple threads start decompressing at guessed positions
   (evenly spaced through the file). Each thread finds a sync point and begins decoding.
2. **Cache**: Decoded results are stored in a cache indexed by compressed-stream offset.
3. **Validator**: As the sequential "truth" decoder advances, it checks if the next
   block's output is already in the cache. If so, skip ahead (cache hit). If not,
   decode sequentially (cache miss).

This generalizes pugz (which was limited to ASCII text by requiring byte values 9-126
for sync validation) to arbitrary gzip data by using the cache to handle incorrect
speculations gracefully — bad results are simply never consumed.

The approach achieves near-linear speedup with core count on large files, limited
mainly by the accuracy of sync point detection on non-text data.

## Key Challenges

- Memory overhead: each speculative thread needs a full decompression buffer
- Sync point detection on binary data is less reliable than on text
- Small files have too few blocks to benefit from multi-core speculation
- Thread scheduling: optimal number of workers depends on file size and core count

## Implementation Backlog

1. [ ] Implement core cache-prefetch architecture with thread pool
2. [ ] Implement sync-point detection for binary (non-text) DEFLATE data
3. [ ] Build concurrent cache with lock-free insertion and ordered consumption
4. [ ] Benchmark on large gzip files (100MB-10GB) across core counts
5. [ ] Measure wasted work from failed speculations
6. [ ] Optimize worker spacing heuristic for different file types
7. [ ] Add adaptive worker count based on speculation hit rate
8. [ ] Compare to rapidgzip on identical test set
