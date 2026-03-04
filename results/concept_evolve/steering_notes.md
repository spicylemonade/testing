# ConceptEvolve Steering Notes

**Date:** 2026-03-04  
**Topic:** SIMD-Accelerated Base64 Decoding  
**Source artifacts:** `steering_directions.json`, `walk_paths.json`, `concept_cards.json`

## Three Concrete Steering Directions

### Direction 1: VBMI + Multiply-Add Optimized AVX-512 Decoder (PRIORITIZED)

**Description:** Combine VPERMB-based single-instruction alphabet lookup (concept: `pshufb_nibble_lookup` extended via VBMI) with the PMADDUBSW/PMADDWD bitfield packing (concept: `multiply_add_bitfield_packing`) and software-pipelined loop structure (concept: `software_pipelined_decode_loop`). This is the most direct path to achieving near-memcpy decode throughput on modern x86-64 hardware.

**Walk path:** `pshufb_nibble_lookup → galois_field_affine_transform → error_correcting_decode_fusion`  
**Walk path:** `multiply_add_bitfield_packing → butterfly_permutation_network → wider_vector_amortization`

**Rubric items informed:** item_005 (SIMD landscape), item_011 (novel strategies), item_012 (AVX2), item_013 (AVX-512), item_017 (ILP optimizations), item_020 (speedup analysis)

**Rationale for priority:** This direction has the highest expected impact because:
1. AVX-512 VBMI (Ice Lake+) reduces lookup from 12 instructions to 1 (VPERMB with 64-byte table)
2. The multiply-add packing is well-proven (Mula/Lemire) but combining with VBMI lookup is underexplored in open source
3. Software pipelining of 2 independent decode blocks can hide the 4-cycle latency of PMADDUBSW
4. Directly targets the 5x speedup goal for the most common server hardware

### Direction 2: Vector-Length-Agnostic SVE/SVE2 Decoder for ARM

**Description:** Build a VLA Base64 decoder using SVE predicated operations (concept: `sve_vector_length_agnostic_decode`, `branch_free_predicated_fixup`). This is a novel contribution since no production-quality SVE Base64 decoder exists. SVE predication eliminates the scalar tail loop entirely — a persistent pain point in fixed-width SIMD decoders.

**Walk path:** `sve_vector_length_agnostic_decode → branch_free_predicated_fixup`  
**Walk path:** `sve_vector_length_agnostic_decode → wider_vector_amortization → galois_field_affine_transform`

**Rubric items informed:** item_005 (SIMD landscape), item_011 (novel strategies), item_014 (NEON), item_015 (SVE), item_018 (benchmarks)

**Rationale:** ARM server adoption is accelerating (AWS Graviton3/4, Ampere Altra). A VLA decoder automatically scales from 128-bit NEON compatibility mode through 256-bit Graviton3 SVE to future 512-bit implementations. The predicated-tail approach from SVE is conceptually superior to the scalar-fallback approach used in x86 SIMD decoders.

### Direction 3: Fused Validation-and-Decode Pipeline

**Description:** Instead of separate validation and decode passes, fuse invalid-character detection directly into the decode pipeline (concepts: `streaming_validation_automaton`, `turbo_parallel_belief_check`). Use SIMD comparison instructions to generate error masks alongside the decode computation, accumulating errors via OR reduction checked only at the end of the stream.

**Walk path:** `streaming_validation_automaton → turbo_parallel_belief_check → error_correcting_decode_fusion`  
**Walk path:** `pshufb_nibble_lookup → streaming_validation_automaton → turbo_parallel_belief_check`

**Rubric items informed:** item_004 (algorithm analysis), item_007 (scalar baseline), item_012 (AVX2), item_016 (streaming), item_019 (correctness validation)

**Rationale:** Most existing SIMD decoders either (a) skip validation for speed or (b) perform a separate validation pass. Fusing validation into the decode pipeline costs only 1-2 additional instructions per SIMD iteration (comparison + OR accumulation) while maintaining full RFC 4648 compliance. This is critical for security-sensitive use cases (JWT, S/MIME) and addresses the rubric's explicit requirement for "full validation of invalid characters and padding."

## Priority Decision

**Direction 1 (VBMI + multiply-add AVX-512) is prioritized** because:

1. It targets the most widely-deployed server architecture (x86-64 with AVX-512)
2. It has the clearest path to measurable results against published baselines (Mula/Lemire, simdutf)
3. The VPERMB single-instruction lookup is a concrete, quantifiable advantage over AVX2 approaches
4. It naturally feeds into Directions 2 (SVE port) and 3 (fused validation) — the algorithm structure is transferable

Direction 3 (fused validation) will be incorporated into all implementations as a cross-cutting concern rather than pursued as an independent direction. Direction 2 (SVE) will be the primary novel research contribution since no production SVE Base64 decoder exists.

## GFNI Exploration (Deferred)

The steering_directions.json proposed a GFNI-native decoder using VGF2P8AFFINEQB. This is intellectually interesting but deferred because:
- GFNI adds complexity without clear advantage over VPERMB (both are single-instruction lookups)
- Hardware availability is more limited than AVX-512 VBMI
- The affine decomposition of the Base64 alphabet is non-trivial (4 piecewise regions)
- May revisit as a bonus exploration in Phase 3 if time permits
