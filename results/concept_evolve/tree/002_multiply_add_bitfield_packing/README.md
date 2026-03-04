# Multiply-Add Bitfield Packing for Base64

## Context

After the lookup phase produces 16 bytes each containing a 6-bit decoded value (in the format `[00dddddd|00cccccc|00bbbbbb|00aaaaaa]`), these must be packed into 12 output bytes (format `[aaaaaabb|bbbbcccc|ccdddddd]`). The naive approach uses shifts, masks, and ORs — 9 instructions per 4 output bytes.

Muła discovered that the x86 PMADDUBSW instruction (multiply unsigned bytes, add adjacent pairs to signed words) can be repurposed: by choosing the right multiplier constants (0x01 and 0x40 = 64), it simultaneously shifts and merges adjacent 6-bit fields. A second PMADDWD completes the merge.

## Key Insight

The 6-bit to 8-bit packing is a linear operation over integers. The multiply-add instructions implement exactly the right linear combination: `a*64 + b` merges two 6-bit values into a 12-bit field, which is precisely what PMADDUBSW computes.

## Implementation Backlog

- [ ] Implement AVX-512 version with VPMADDUBSW + VPMADDWD on ZMM registers
- [ ] Add VPERMB compaction step to extract 48 useful bytes from 64-byte register
- [ ] Test edge cases: maximum 6-bit values (63), padding bytes
- [ ] Software-pipeline two packing iterations to hide multiply-add latency (4 cycles)
- [ ] Compare against VPDPBUSD (dot-product) instruction for possible single-instruction packing
- [ ] Benchmark on ARM NEON using equivalent SMLAL/SMULL instructions
