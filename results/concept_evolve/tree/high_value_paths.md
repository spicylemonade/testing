# High-Value Concept Paths for 2-5x DEFLATE Decompression Speedup

## Path 1: "The Microarchitectural Squeeze" (Single-Thread Optimization)
**Concepts:** `simd_bitstream_swizzling → interleaved_multi_stream_huffman → memory_layout_restructuring → branchless_lz77_copy_unification`

**Estimated speedup:** 1.5-2.2x over libdeflate (single core)

**Bottlenecks attacked:**
- Huffman decode serial dependency (35-45% of cycles): Multi-stream breaks serial chain into 6 independent ILP streams
- Table cache misses (5-10%): 3-tier cache-aligned layout ensures 85% L1 hit rate even with 6-way access
- Branch misprediction (10-15%): CMOV-based branchless dispatch eliminates literal/match prediction failures
- Bit-buffer overhead (5-8%): SIMD parallel extraction across multiple streams

**Key synergy:** Giesen's Oodle Data analysis shows 6-stream decode achieves 1.83 cycles/symbol (~3+ GB/s Huffman-only). Memory layout restructuring is a dependency (not optional) because 6-way parallel table access creates 6x cache pressure. Production-validated in game engines.

---

## Path 2: "The Parallel Multiplier" (Multi-Core Parallelism)
**Concepts:** `probabilistic_sync_point_discovery → speculative_block_boundary_detection → fsm_enumerative_speculation → cache_prefetch_sliding_window`

**Estimated speedup:** 2-4x multiplier on top of single-thread (using 4-8 cores)

**Bottlenecks attacked:**
- Amdahl's Law serial constraint: Enable N-way parallel block decode
- Block boundary discovery cost: SIMD-accelerated Bayesian scanning reduces false positives to <5%
- Intra-block serial Huffman: 15-state FSM speculation with rapid convergence (~64 symbols)
- Cross-block cache misses: Prefetch copy sources during speculative validation

**Key synergy:** rapidgzip proves block-boundary approach works (55x over gzip, 128 cores). This path combines coarse probabilistic scan → fine speculative validation. FSM speculation enables parallelism within blocks, not just between them. Works on existing DEFLATE/gzip files.

---

## Path 3: "The Memory Wall Breaker" (Enabling Substrate)
**Concepts:** `cache_prefetch_sliding_window → memory_layout_restructuring → branchless_lz77_copy_unification`

**Estimated speedup:** 1.3-1.5x over libdeflate (standalone), but enables Paths 1 & 2 to reach full potential

**Bottlenecks attacked:**
- LZ77 copy cache misses (10-20%): Software prefetch hides 12-200 cycle latency
- Table lookup cache misses (5-10%): Hot entries in 4 cache lines
- LZ77 branch misprediction (10-15%): CMOV dispatch + unified overlapping copy path

**Key synergy:** This path removes the second and third biggest bottlenecks. Without it, Path 1's faster Huffman decode makes LZ77 copy the new bottleneck (~40-50% of remaining cycles). Without prefetching, Path 2's parallel threads thrash each other's cache lines. **Zero format changes required** — pure implementation optimization.

---

## Composite Speedup Projection

| Path | Factor | Compatible? | Risk |
|---|---|---|---|
| Path 3 (Memory Wall) | 1.3x | Yes | Low |
| Path 1 (Microarch, compatible mode) | 1.3x | Yes | Medium |
| Path 2 (Parallel, 4 cores) | 3.0x | Yes | Medium |
| **Combined** | **~5x over libdeflate** | **Yes** | **Medium** |

With format extension (multi-stream Huffman at full potential): **~8x over libdeflate**, ~16-24x over zlib.

## Concept Graph Gaps Identified

1. **Decode-execute decoupling buffer** — embedded in concept 7, deserves standalone concept card. Critical mechanism where multi-stream Huffman output feeds into prefetched LZ77 execution.
2. **SIMD↔LZ77 fusion** — no direct path from SIMD bitstream concepts to branchless LZ77. Missing unified inner loop design.
3. **Small-file fast path** — HTTP/web use case with <1KB payloads dominates real-world DEFLATE traffic, not addressed by any concept.
