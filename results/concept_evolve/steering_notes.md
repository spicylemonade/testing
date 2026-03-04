# ConceptEvolve Steering Notes

## 3 Concrete Steering Directions

### Direction 1: ILP-First Single-Thread Optimization via Multi-Symbol Wide Tables
**Description:** Maximize instruction-level parallelism in a single-threaded decoder by combining wide lookup tables (11+ bit primary table decoding 2-3 symbols per access), branchless 64-bit bit-buffer refill, and latency-hiding techniques. This is the highest-confidence approach grounded in proven techniques from libdeflate and dougallj's analysis.

**Rubric items informed:** item_012 (multi-symbol Huffman decode), item_015 (optimized bit reader), item_016 (fast table build), item_018 (unified decoder), item_019 (benchmarks)

**Risk:** Low. These are proven techniques with documented speedups. The challenge is in combining them optimally.

### Direction 2: Two-Pass Architecture with SIMD-Accelerated Copy Phase
**Description:** Separate Huffman decoding from LZ77 match execution into two distinct passes. Pass 1 decodes all Huffman symbols into a compact token stream (literal bytes, length/distance pairs). Pass 2 executes the token stream with SIMD-accelerated memcpy for both literal runs and match copies. This separation allows each pass to be optimized independently, improves branch prediction (no interleaved literal/match dispatch), and enables SIMD utilization in the copy phase.

**Rubric items informed:** item_013 (SIMD literal copying), item_014 (speculative decoding), item_017 (parallel block evaluation), item_018 (unified decoder), item_020 (ablation study)

**Risk:** Medium. The intermediate token buffer adds memory overhead (~2-4 bytes per symbol). May not win on very small blocks where the overhead dominates.

### Direction 3: Speculative Block-Parallel Decoding with Sync-Point Discovery
**Description:** For large files, speculatively discover DEFLATE block boundaries and decode blocks on multiple threads. Uses FSM convergence (convergence_set_fsm concept) to find valid bit-aligned sync points within a DEFLATE bitstream. Falls back to serial decode if sync fails. Combined with optimistic concurrency (verify-at-end pattern).

**Rubric items informed:** item_005 (cross-domain exploration), item_014 (speculative decoding), item_017 (parallel block evaluation), item_022 (cross-arch analysis)

**Risk:** High. DEFLATE block boundaries are not byte-aligned and have no sync markers. FSM convergence requires significant theoretical work. Multi-threading adds complexity. However, this has the highest potential payoff for large files.

## Priority Decision

**Direction 1 (ILP-First) is prioritized** because:

1. **Highest confidence:** Multi-symbol decode tables and branchless bit readers are proven techniques with documented 2-4x speedups over naive implementations. libdeflate already demonstrates this is achievable.
2. **Drop-in compatibility:** Single-threaded, no format assumptions, works on all input sizes.
3. **Foundation for later work:** The optimized decoder core from Direction 1 is a prerequisite for both Direction 2 (the Huffman pass still needs to be fast) and Direction 3 (each thread uses the fast decoder).
4. **Benchmark credibility:** Having a strong single-threaded baseline establishes credibility before adding complexity.

Direction 2 should be attempted next as it's the highest-value novel contribution (no existing open-source DEFLATE decompressor uses this architecture). Direction 3 is exploratory and should be evaluated theoretically before committing to implementation.

## Walk Path Analysis

The most common concept appearing in walk paths is `multi_stream_ilp_decode` (appears in 18/21 paths), confirming it as the central hub. The path `precomputed_mega_table -> multi_stream_ilp_decode -> interleaved_entropy_streams -> speculative_sync_point -> convergence_set_fsm` represents the natural progression from proven techniques to novel research.
