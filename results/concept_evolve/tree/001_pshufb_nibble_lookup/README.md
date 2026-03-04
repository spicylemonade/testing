# PSHUFB Nibble Lookup for Base64 Decoding

## Context

The core challenge in SIMD Base64 decoding is converting ASCII characters to their 6-bit values in parallel. A scalar decoder uses a 256-entry lookup table, but SIMD has no equivalent of random-access table lookup across arbitrary addresses. The PSHUFB (Packed Shuffle Bytes) instruction provides a 16-entry lookup table indexed by the low 4 bits of each byte in a vector register.

Wojciech Muła pioneered the technique of decomposing the 256-entry Base64 lookup into operations on the high nibble (4 bits) of each byte. By using 3 PSHUFB lookups (shift values, lower bounds, upper bounds) indexed by the high nibble, the full lookup+validation is achieved in just 12 instructions for 16 bytes — 0.75 instructions per character.

## Key Insight

The Base64 alphabet has a structure that aligns with nibble boundaries: all uppercase letters have high nibbles 4-5, lowercase have 6-7, digits have 3, and symbols have 2. This means the high nibble alone narrows the valid range to at most 16 characters, which can be checked with a single range comparison.

## Implementation Backlog

- [ ] Implement VPERMB-based 64-byte lookup on AVX-512 VBMI (eliminates nibble split)
- [ ] Benchmark against PSHUFB-bitmask at various input sizes (64B to 10MB)
- [ ] Explore using two VPERMB calls with 128-entry table for direct mapping (no validation step)
- [ ] Port PSHUFB technique to ARM NEON using TBL/TBX instructions
- [ ] Measure instruction count reduction on Ice Lake vs Haswell
- [ ] Test with URL-safe Base64 alphabet (different lookup constants)
