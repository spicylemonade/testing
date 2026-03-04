# ConceptEvolve Steering Notes

## Date: 2026-03-04

## Summary

The ConceptEvolve `evolve` command produced 12 concept cards with 20 bridge nodes and 55 walk paths.
The concept tree covers approaches from automata theory, information theory, computer architecture,
SIMD programming, and parallel algorithms.

---

## 3 Concrete Steering Directions

### Direction 1 (PRIORITIZED): Speculative Multi-Symbol + Branchless Bitbuffer + SIMD LZ77

**Rubric items informed:** item_012, item_013, item_014, item_015, item_016

**Rationale:** This direction combines concepts from `branch_prediction_huffman`,
`transducer_composition_monoid`, and `simd_multi_table_decode`. Rather than pursuing
full parallel FSM decomposition (which has high complexity and large table sizes),
we focus on the practical fast-path: precomputed multi-symbol decode tables that
amortize Huffman lookup overhead by decoding 2-4 symbols per table access, combined
with branchless bit-buffer management and SIMD-accelerated literal runs and LZ77 copies.

This is the approach used successfully by libdeflate (which already achieves ~1.5-2x over zlib-ng),
and we extend it further with:
- Wider decode tables (4 symbols instead of 2)
- AVX2 literal burst detection and bulk copy
- Branchless back-reference copy with overlapping-match SIMD support
- Unconditional 64-bit bit-buffer refill

**Why prioritized:** This approach is:
1. Fully compatible with RFC 1951 (no format changes)
2. Single-threaded (no thread coordination overhead)
3. Well-understood implementation pattern (libdeflate proves viability)
4. Targets the exact bottlenecks identified in the spec analysis (Section 4)
5. Achievable within the project scope

### Direction 2: Sync-Point Parallel Prefix Huffman Decode

**Rubric items informed:** item_004, item_011, item_017

**Rationale:** Combines concepts `sync_point_convergence`, `enumerated_state_parallel_fsm`,
and `prefix_scan_composition`. The Huffman self-synchronization property (convergence after
~20-50 bits) enables splitting a single block's bitstream into independently decodable chunks.
Using parallel prefix composition of FSM transitions, we can determine the correct decode
state at each chunk boundary.

**Trade-off:** Higher theoretical ceiling but requires AVX-512 for practical benefit, and
the overhead of state enumeration and prefix scan may not pay off for blocks under ~4KB.
This is a "research exploration" direction rather than the primary implementation path.

### Direction 3: Multi-Core Block Speculation (rapidgzip architecture)

**Rubric items informed:** item_004, item_005, item_017

**Rationale:** Combines `speculative_block_boundary`, `cache_prefetch_speculation`, and
the rapidgzip architecture. Multiple threads speculatively begin decoding at guessed
block boundaries. This provides near-linear multi-core scaling for large files.

**Trade-off:** Requires multi-threading, which adds complexity and is not a drop-in
replacement for single-threaded inflate(). The focus of our project is single-core
throughput improvement, so this direction informs future work discussion rather than
the core implementation.

---

## Priority Assessment

**Direction 1 is prioritized** because:
- It directly targets the ≥2× throughput goal on single-core
- It builds on proven techniques (libdeflate's multi-symbol decode, zlib-ng's fast path)
- It requires no hardware beyond SSE4.2/AVX2 (widely available)
- All components are independently testable and their speedup contributions measurable
- It satisfies the RFC 1951 compatibility requirement by construction

Directions 2 and 3 will be explored during the concept-tree reframing (item_017) and
discussed as future work in the research paper (item_023).

---

## Concept Cards to Monitor

| Card | Relevance | Phase |
|------|-----------|-------|
| `transducer_composition_monoid` | Core technique for multi-symbol decode tables | Phase 3 |
| `branch_prediction_huffman` | Informs loop structure for minimal misprediction | Phase 3 |
| `simd_multi_table_decode` | AVX2 literal run acceleration | Phase 3 |
| `wavefront_lz77_resolution` | LZ77 copy optimization insight | Phase 3 |
| `sync_point_convergence` | Alternative/future direction | Phase 5 |
| `probabilistic_sync_distance` | Informs chunk size decisions | Phase 2 |
