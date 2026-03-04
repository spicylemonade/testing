# Runahead Prefetch Parsing

## Context

On-demand JSON parsers traverse the structural index sequentially, materializing values only when accessed. For large files where the structural index exceeds the L1 cache, each value materialization may trigger L2/L3 cache misses for both the structural index entry and the corresponding input bytes. These misses stall the parser for 10-50 cycles each.

## Key Insight

CPU runahead execution deals with exactly this problem: when a load misses in cache, the CPU continues executing future instructions speculatively to discover more cache misses and issue prefetches in parallel. We can implement the same strategy in software: when the parser materializes a value (a long-latency operation), a lightweight "runahead" routine prefetches the structural entries and input bytes that will be needed for subsequent operations.

## Cross-Domain Bridges

- **CPU runahead execution**: hardware technique for prefetching past cache misses
- **OS readahead**: kernel prefetches disk blocks on sequential file access detection
- **LLM speculative decoding**: draft model generates speculative tokens to pipeline with verification

## Implementation Backlog

1. [ ] Profile simdjson On-Demand cache miss patterns during field traversal
2. [ ] Identify optimal prefetch distance (entries ahead) based on access patterns
3. [ ] Implement software prefetch in the structural tape traversal loop
4. [ ] Design coroutine-based runahead that walks tape without modifying parser state
5. [ ] Benchmark on large JSON files (10MB+) with scattered field access
6. [ ] Measure L1/L2/L3 cache miss rate reduction with perf
7. [ ] Test interaction with hardware prefetcher (avoid interference)
8. [ ] Compare simple prefetch insertion vs. full coroutine-based runahead
