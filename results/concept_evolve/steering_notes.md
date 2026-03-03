# Steering Notes — Fast DEFLATE Decompression

## 3 Concrete Steering Directions

### Direction 1: SIMD-Accelerated Sequential Decode (PRIORITIZED)
**Description:** Optimize the single-threaded hot path — Huffman decode, bit-stream parsing, and LZ77 copy — using SIMD intrinsics (AVX2/SSE4.2), branchless techniques, and cache-aware memory layout.

**Rubric items informed:** item_008 (baseline measurement), item_009 (profiling), item_011 (SIMD Huffman), item_012 (branchless parsing), item_014 (LZ77 copy), item_015 (integrated decompressor), item_017 (throughput eval), item_020 (uarch analysis), item_023 (ablation)

**Why prioritized:** This is the foundational layer everything else builds on. Parallel approaches multiply single-thread throughput, so a 1.5-2x single-thread improvement compounds with parallelism to reach 3-5x. It requires no format changes, works on all existing DEFLATE data, and is the most practically deployable approach. libdeflate already demonstrates ~2-3x over zlib via these techniques but leaves headroom in branch prediction, prefetching, and table layout.

### Direction 2: Speculative Parallel Block Decompression
**Description:** Discover DEFLATE block boundaries in compressed data using probabilistic scanning (inspired by pugz/rapidgzip), then decompress blocks in parallel with speculative state.

**Rubric items informed:** item_010 (theoretical ceiling / Amdahl), item_013 (parallel blocks), item_017 (throughput eval), item_021 (cross-platform), item_022 (application benchmarks)

**Why second:** This is the multiplier on top of Direction 1. rapidgzip achieves 55x over gzip with 128 cores. For the 2-5x target, even 2-4 cores suffice if single-thread is strong. The key challenge is cross-block back-references (LZ77 matches can span block boundaries), which requires either speculative decode or a two-pass approach.

### Direction 3: Hardware-Aware Memory Layout and Prefetching
**Description:** Restructure decode tables, output buffers, and LZ77 sliding window for modern cache hierarchies. Use software prefetch for long-distance copies. Optimize for 48KB L1D (Zen4) and 48KB L1D (Golden Cove).

**Rubric items informed:** item_009 (profile bottlenecks), item_010 (theoretical ceiling), item_014 (LZ77 copy), item_018 (latency/memory), item_020 (uarch analysis)

**Why third:** This is an orthogonal optimization that benefits both Directions 1 and 2. Cache misses during LZ77 copies with distances > 16KB are a significant bottleneck. Prefetch strategies can hide memory latency without changing the algorithm. This direction also informs the feasibility analysis of GPU offload (Direction 4 from ConceptEvolve, deferred to item_016).

## Concept Tree Path Analysis

The highest-value walk paths cluster around:
1. `simd_bitstream_swizzling -> interleaved_multi_stream_huffman -> memory_layout_restructuring` — the single-thread optimization chain
2. `speculative_block_boundary_detection -> probabilistic_sync_point_discovery -> cache_prefetch_sliding_window` — the parallelism chain
3. `branchless_lz77_copy_unification -> cache_prefetch_sliding_window -> memory_layout_restructuring` — the memory optimization chain

These three paths map directly to our three steering directions and cover 80%+ of the rubric items.
