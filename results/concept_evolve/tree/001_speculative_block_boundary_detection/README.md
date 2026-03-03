# Speculative Block Boundary Detection

## Topic Context

DEFLATE streams consist of sequential blocks, each with its own Huffman table. The fundamental challenge of parallel DEFLATE decompression is that you cannot begin decoding block N+1 until block N is fully decoded, because block boundaries are only discoverable during sequential decode.

**pugz** (Kerbiriou & Chikhi, 2019) broke through this barrier for gzip-compressed text by showing that block boundaries can be probabilistically discovered: randomly guess a bit position, attempt to decode a Huffman table there, and validate the resulting output. For text files (byte values 9-126), validation is trivial.

**rapidgzip** (Knespel & Brunst, 2023) generalized this to arbitrary binary data by implementing a cache-and-prefetch architecture that handles faulty speculative results gracefully. It achieved 8.7 GB/s on base64 data with 128 cores (55x over GNU gzip).

## Key Insight

The probability that a random bit position is a valid DEFLATE block boundary is low (~2^-20), but the probability that a position NEAR a real block boundary can be identified is high if you use heuristic scoring (valid Huffman table properties, plausible code-length distributions).

## Implementation Backlog

1. **SIMD block header scanner**: Use AVX2/AVX-512 to scan for candidate BTYPE=01/10 patterns at byte-aligned positions
2. **Huffman table validator**: Fast check that a candidate table satisfies the Kraft inequality (sum of 2^-l_i <= 1)
3. **Speculative decode framework**: Thread pool that assigns chunks to workers, validates outputs, and merges results
4. **Cache architecture**: Store validated decode results in a thread-safe cache (following rapidgzip's design)
5. **LZ77 window reconstruction**: When a speculative thread needs history bytes from a previous chunk, fetch from cache or wait
6. **Benchmark suite**: Compare against libdeflate (sequential), pigz (block-parallel), pugz, rapidgzip
7. **File format analysis**: Characterize block size distributions in real-world gzip/ZIP/PNG files to estimate parallelization potential
