# Butterfly Permutation Network for Byte Compaction

## Context

After Base64 decoding, 64 input bytes produce 48 output bytes (4:3 ratio). In a SIMD register, the 48 useful bytes are interleaved with 16 garbage bytes (the high 2 bits of each decoded 6-bit value, zeroed but occupying space). These 48 bytes must be compacted into contiguous memory for the output.

This compaction is a fixed permutation — the same pattern repeats for every iteration. In FFT algorithms, the butterfly network is the canonical structure for implementing fixed data permutations using a cascade of simple swap/shuffle operations.

## Key Insight

AVX-512 VBMI provides VPERMB, which can implement any byte permutation of a 64-byte vector in a single instruction. This is equivalent to a complete butterfly network collapsed into one hardware operation. Without VBMI, the permutation must be decomposed into dword-level permutes (VPERMD) and lane-local byte shuffles (VPSHUFB), which is exactly a 2-level butterfly decomposition.

## Implementation Backlog

- [ ] Precompute the VPERMB index vector for 4:3 byte compaction
- [ ] Implement AVX2 fallback using VPERMD + VPSHUFB decomposition
- [ ] Implement NEON fallback using TBL with 4-register source
- [ ] Handle the 48-byte store (either masked 64-byte store or 32+16 split store)
- [ ] Benchmark compaction in isolation to measure overhead vs total decode cost
- [ ] Explore overlapping stores (write 64 bytes but advance pointer by 48) to avoid masked stores
