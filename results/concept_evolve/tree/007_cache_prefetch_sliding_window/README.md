# Cache Prefetch Sliding Window

## Topic Context

DEFLATE's LZ77 layer resolves back-references by copying data from previously decoded output. When the copy distance is large (up to 32KB), the source data may not be in L1 cache, causing a stall of 10-200 cycles. These cache misses are a significant fraction of total decode time, especially for high-compression-ratio files with large match distances.

The rapidgzip project demonstrated that cache prefetching is critical for parallel decompression: when speculative threads need data from other threads' output, a prefetch architecture avoids blocking on cache misses.

## Key Insight

Huffman decoding and LZ77 copy execution can be **decoupled**: decode several symbols ahead, issue prefetches for upcoming copies, then execute the copies when the data has arrived in cache. This transforms a latency-bound operation into a throughput-bound one.

## Implementation Backlog

1. **Cache miss profiling**: Run libdeflate with perf stat on diverse file types, measure L1/L2 miss rates during inflate
2. **Prefetch injection**: Add _mm_prefetch() calls after each length-distance decode, before executing the copy
3. **Command buffer**: Implement a circular buffer of 16 decoded commands (literal or copy) to allow lookahead
4. **Prefetch distance tuning**: Experiment with prefetch timing (immediate vs. N symbols ahead) on different CPUs
5. **Two-pass decoder**: First pass: Huffman decode all symbols into command buffer. Second pass: execute all copies with full prefetch coverage
6. **ARM integration**: Use ARM's PRFM instruction for equivalent prefetch on Apple Silicon and Graviton
7. **Benchmark**: Measure improvement on files with different distance distributions (text, binary, PNG image data)
