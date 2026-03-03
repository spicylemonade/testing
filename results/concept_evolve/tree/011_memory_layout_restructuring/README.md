# Memory Layout Restructuring

## Topic Context

DEFLATE decompression is memory-access-intensive: every decoded symbol requires a Huffman table lookup, and every LZ77 copy requires reading from the 32KB sliding window. On modern CPUs, L1 cache is 32-48KB, meaning the sliding window alone can thrash the entire L1 cache.

libdeflate already uses a 2-tier Huffman table: a primary table indexed by the first K bits (typically 8-10), with a secondary table for codes longer than K bits. This is good but not optimal.

## Key Insight

The access pattern of Huffman tables follows a heavy-tailed distribution: a few short codes (representing common symbols like 'e', 't', space in English text) account for 80-90% of all lookups. If these hot entries fit in 1-2 cache lines (64-128 bytes), the effective cache miss rate drops to near zero for the majority of decodes.

The FastLanes thesis (Afroozeh, 2025) demonstrated that restructuring data layouts for SIMD-friendly access patterns can yield 100+ billion integers/second decode speed -- the same principle applies to Huffman table layout.

## Implementation Backlog

1. **Access pattern analysis**: Instrument Huffman table lookups on Silesia corpus to measure access frequency distribution
2. **Hot/cold partition**: Identify the top-K entries that cover 90% of accesses
3. **Cache-line-aligned Tier 0**: Pack hot entries into 2-4 cache lines (128-256 bytes)
4. **Prefetch Tier 1**: Issue prefetch for Tier 1 table when Tier 0 miss is detected
5. **Sliding window layout**: Experiment with circular buffer vs. double-copy for 32KB window
6. **NUMA awareness**: For multi-threaded decompression, ensure tables are local to each NUMA node
7. **Micro-benchmark**: Isolate Huffman table lookup performance with synthetic access patterns
