# Galois Field Affine Transform for Base64 Decoding

## Context

The AVX-512 GFNI (Galois Field New Instructions) extension adds VGF2P8AFFINEQB, which performs an 8x8 bit-matrix multiply over GF(2) on each byte of a vector. This is equivalent to computing an arbitrary affine function of the 8 input bits, producing an 8-bit result. Originally designed for AES S-box substitution, this instruction can be repurposed for any byte-to-byte mapping that can be decomposed into affine regions.

The Base64 alphabet consists of 4 contiguous ASCII ranges (A-Z, a-z, 0-9, +/) that map to 4 contiguous 6-bit ranges (0-25, 26-51, 52-61, 62-63). Each of these mappings is an affine function: value = byte + constant. Over GF(2), this can be expressed as a bit-matrix multiplication.

## Key Insight

The Base64 decode function is piecewise-affine with 4-5 pieces. GFNI can compute each piece in a single instruction, and mask-blend can select the correct piece per byte. This trades the PSHUFB lookup infrastructure (nibble split + 3 shuffles + range check) for a smaller number of GFNI + blend operations.

## Implementation Backlog

- [ ] Derive the 8x8 GF(2) matrices for each Base64 alphabet region
- [ ] Implement 4-region GFNI lookup with VPTERNLOGD-based blending
- [ ] Compare instruction count against PSHUFB-bitmask approach
- [ ] Test on Ice Lake, Alder Lake, Sapphire Rapids (all have GFNI)
- [ ] Verify that GFNI port usage does not conflict with PMADDUBSW (packing stage)
- [ ] Explore using GFNI for the packing step as well (bit-field rearrangement)
