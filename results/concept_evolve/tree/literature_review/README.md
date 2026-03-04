# Literature Review: Fast DEFLATE Decompression Techniques

## Summary Table

| # | Source | Year | Technique | Claimed Speedup | Compat. w/ Standard DEFLATE |
|---|--------|------|-----------|-----------------|-----------------------------|
| 1 | libdeflate (Biggers) | 2017-present | Wide Huffman lookup tables (11-bit primary), branchless bit reader, SIMD match copy, optimized table build | ~2-3x over zlib on decompression | Yes (fully RFC 1951 compliant) |
| 2 | zlib-ng | 2013-present | SIMD-accelerated inflate (SSE2/AVX2/NEON), optimized chunkset, improved hash functions for compression | ~1.5-2x over zlib-madler on decompression | Yes (drop-in zlib replacement) |
| 3 | Intel ISA-L (igzip) | 2014-present | Hand-coded x86 assembly, SIMD bitstream processing, specialized inflate tables, multi-buffer API | ~2-3x over zlib on decompression; claimed >2x over libdeflate on some workloads | Yes (standard DEFLATE) |
| 4 | dougallj blog: Faster zlib/DEFLATE decompression | 2022 | Zero-refill-latency bit reader, unconditional refill overlapping table lookup, literal fastpath | 1.51x over zlib-cloudflare, 2.1x over Apple zlib on M1 | Yes (patches to zlib-cloudflare) |
| 5 | Giesen (ryg blog): Reading bits in far too many ways | 2018 | Comprehensive analysis of bit reader dependency chains; variant 4 (unconditional refill from pointer) optimal for OoO CPUs | Foundation for dougallj and Oodle approaches | N/A (technique analysis) |
| 6 | Giesen: Entropy decoding in Oodle Data | 2022 | Multi-stream interleaved Huffman decode for ILP; 3 parallel decode streams hide latency | ~2.8 cycles/byte on Jaguar with 3-stream Huffman | No (Oodle custom format), but technique is transferable |
| 7 | dougallj: Parallelising Huffman decoding by synchronising prefix codes | 2022 | FSM convergence to find sync points in mid-stream variable-length codes; enables parallel decode | Enables multi-threaded DEFLATE decompression | Yes (no format changes required) |
| 8 | rapidgzip (Knespel & Brunst) | 2023 | Parallel gzip decompression via speculative block boundary finding + cache/prefetcher architecture | 33-55x speedup on 128 cores vs single-thread gzip | Yes (arbitrary gzip files) |
| 9 | GDeflate (NVIDIA / Uralsky) | 2022 | Bit-swizzled DEFLATE stream for 32-way SIMD parallelism on GPU; same compression ratio | High GPU throughput for DirectStorage | No (modified bitstream format, not standard DEFLATE) |
| 10 | nvcomp (NVIDIA) | 2022 | GPU compression library including GDeflate, LZ4, Snappy, Cascaded, ANS | Various; GDeflate enables GPU DEFLATE-like decompression | No (GDeflate variant) |
| 11 | Weissenberger & Schmidt: Massively Parallel Huffman Decoding on GPUs | 2018 | Self-synchronization property of Huffman codes exploited for massively parallel GPU decode | 10x+ speedup over Zstandard CPU Huffman decoder | Yes (compatible with standard Huffman codes) |
| 12 | Rivera et al.: Optimizing Huffman Decoding for Lossy Compression on GPUs | 2022 | Shared memory optimization, online tuning, improved memory access patterns for GPU Huffman decode | 3.64x over cuSZ Huffman decoder | Yes (standard Huffman codes) |
| 13 | Belu & Coltuc: Fast Canonical Huffman Decoder | 2022 | Multi-symbol canonical Huffman decode per cycle, minimal decode table storage, 12-bit limited codes | 2.1 GiB/s on highly redundant data | Yes (standard canonical Huffman) |
| 14 | Collet (FSE/huff0): Huffman revisited | 2015 | Interleaved multi-stream Huffman decode using FSE-style bitstream; 4-stream interleave for ILP | ~475 MB/s FSE vs ~250 MB/s traditional Huffman | No (custom bitstream format, but technique is transferable) |
| 15 | Satpathy et al.: DEFLATE Decompression Accelerator in 14nm CMOS | 2018 | Hardware accelerator: dual-ALU block-adaptive Huffman, opportunistic code skip, 3-way symbol gen | 2.4x faster than serial hardware decode; 1.65 Gb/s | Yes (standard DEFLATE) |
| 16 | Takafuji et al.: GPU implementations of deflate encoding/decoding | 2022 | GPU DEFLATE decode using gap arrays for parallel Huffman, SKSS synchronization | 4-36x over single-thread CPU | Yes (standard DEFLATE) |
| 17 | Hirschberg & Lelewer: Efficient decoding of prefix codes | 1990 | Table-based Huffman decoding with multi-bit lookup tables; foundational work | Foundation technique used by all modern decoders | N/A (algorithmic foundation) |
| 18 | Huffman: A Method for Construction of Minimum Redundancy Codes | 1952 | Original Huffman coding algorithm | N/A (original algorithm) | N/A |
| 19 | Zhang et al.: 43.3 bit/cycle Inflate Accelerator with Multiple Checkpoints | 2024 | Speculative Huffman decoder with multiple checkpoints; primary/speculative thread architecture | 43.3 bits/cycle; improved over single-checkpoint designs | Yes (standard DEFLATE) |

## Key Observations

### Most Promising Techniques for 2x+ over zlib-ng

1. **Wide multi-symbol lookup tables (11+ bits)**: libdeflate and ISA-L both use this; decoding 2-3 symbols per table access eliminates branches and amortizes lookup latency.

2. **Zero-refill-latency bit reader (dougallj)**: By refilling the bit buffer *before* it's needed for the next lookup, the refill latency is hidden behind the table lookup. This alone gives ~20% improvement.

3. **Multi-stream interleaved decode (Giesen/Collet)**: Running 2-4 independent Huffman decode streams in parallel exploits ILP on superscalar CPUs. The key challenge for DEFLATE is that the format has a single bitstream, so "virtual" streams must be created via sync-point discovery.

4. **Parallel block-boundary detection (dougallj/rapidgzip)**: Finding sync points where decoding can restart enables multi-threaded decompression. rapidgzip demonstrates this at scale (55x speedup on 128 cores).

5. **SIMD-accelerated literal and match copies**: Once symbols are decoded, the copy operations can use AVX2/SSE2 for 32-byte wide copies, significant for text-heavy content with long literal runs.

### Gaps in Prior Work (Our Opportunity)

- No existing open-source single-threaded CPU decoder combines *all* of: wide tables + zero-refill bit reader + SIMD copies + speculative/multi-symbol decode.
- libdeflate is closest but does not use dougallj's zero-refill technique or multi-stream ILP.
- ISA-L uses hand-coded assembly, making it difficult to extend; a C implementation matching its speed would be valuable.
- The two-pass (Huffman-then-LZ77) architecture has not been explored for CPU DEFLATE decompression.
