# VBMI2 Compress/Expand Parsing

## Context

Token extraction in JSON parsing typically involves conditional stores: for each byte, check if it's a structural character, and if so, store it to an output buffer. This creates a data-dependent branch pattern that the CPU must predict. AVX-512 VBMI2 introduces VPCOMPRESSB and VPEXPANDB instructions that perform conditional packing/unpacking in a single instruction with zero branches.

## Key Insight

VPCOMPRESSB takes a 64-byte register and a 64-bit mask, and packs only the bytes where the mask bit is 1 into the low positions of the output register. This is exactly the operation needed for extracting structural characters (sparse: ~2-5% of bytes) or string content (dense: ~60-90% of bytes) from the input.

## Cross-Domain Bridges

- **Column-store databases**: BitWeaving processes compressed data in-place using bit-parallel operations
- **FPGA stream routing**: hardware crossbars perform byte-level routing natively
- **Sparse matrix operations**: compressed sparse row format packs only non-zero elements, analogous to VPCOMPRESSB packing only structural bytes

## Implementation Backlog

1. [ ] Microbenchmark VPCOMPRESSB latency and throughput on target microarchitectures
2. [ ] Implement structural character extraction using VPCOMPRESSB
3. [ ] Implement string content extraction using VPCOMPRESSB with inverted mask
4. [ ] Compare against PSHUFB-based extraction (lookup-table approach)
5. [ ] Measure throughput at varying structural character densities
6. [ ] Implement Unicode escape decoding using VPEXPANDB
7. [ ] Integrate with fused tokenize-validate pass (concept 2)
8. [ ] Test portability: emulate VPCOMPRESSB on AVX2 using PEXT + PSHUFB cascade
