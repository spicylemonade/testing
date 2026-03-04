# SVE Vector-Length Agnostic Base64 Decode

## Context

ARM's Scalable Vector Extension (SVE) introduces a fundamentally different SIMD programming model compared to fixed-width extensions like NEON (128-bit) or AVX-512 (512-bit). SVE vectors can be 128 to 2048 bits wide, and the programmer writes code without knowing the vector length at compile time. The hardware provides the actual width at runtime.

For Base64 decoding, this means a single implementation can automatically scale from processing 16 bytes/iteration (128-bit NEON-equivalent) to 256 bytes/iteration (2048-bit) as hardware evolves. SVE's native predication also elegantly handles the tail of the input (when remaining bytes are fewer than the vector width).

## Key Insight

SVE's SVTBL instruction is the equivalent of x86's VPERMB: it performs arbitrary byte-level permutation across the full vector width. Combined with SVMLA (multiply-accumulate), it can implement the complete lookup+pack pipeline. The whilelt/ptest loop pattern eliminates the need for scalar tail handling.

## Implementation Backlog

- [ ] Implement lookup using svtbl with a base64-to-value table in a vector register
- [ ] Implement packing using svmla (multiply-accumulate for 6-bit field merging)
- [ ] Write VLA loop using svwhilelt + svptest_any for termination
- [ ] Handle output stride (3/4 of input length) with svcntb-based arithmetic
- [ ] Benchmark on AWS Graviton3 (c7g) instances
- [ ] Compare against NEON-optimized aklomp/base64 library
- [ ] Validate on QEMU SVE emulation at multiple vector widths (128, 256, 512, 1024, 2048)
