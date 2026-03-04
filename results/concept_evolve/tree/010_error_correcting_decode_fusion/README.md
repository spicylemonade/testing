# Error-Correcting Decode Fusion

## Context

In many real-world applications, Base64-decoded data is immediately processed further: JWT tokens are checksummed (HMAC), email attachments are integrity-checked (CRC), and API payloads are validated. Running decode and integrity check as separate passes means the decoded data must be written to memory and then read back — wasting memory bandwidth.

In communication systems, the Viterbi decoder and CRC checker are typically fused into a single pipeline stage. The same principle applies here: keep the decoded data in SIMD registers and immediately feed it into the integrity computation.

## Key Insight

AVX-512 provides VPCLMULQDQ for carry-less multiplication, which is the core operation for CRC-32C computation. Processing 48 bytes of CRC costs ~8 VPCLMULQDQ instructions. When those 48 bytes are already in a ZMM register from the decode stage, there's zero additional memory traffic — the CRC computation piggybacks on the decode for free (modulo instruction-level competition for execution ports).

## Implementation Backlog

- [ ] Implement fused decode + CRC-32C using VPCLMULQDQ
- [ ] Benchmark fused vs separate decode-then-CRC at 1KB, 64KB, 1MB, 10MB
- [ ] Measure marginal cost of CRC fusion (expected: <15% decode throughput reduction)
- [ ] Explore fusing decode with HMAC-SHA256 (more complex; requires hash state management)
- [ ] Test on both Intel (PCLMULQDQ) and ARM (PMULL polynomial multiply) architectures
- [ ] Integrate with JWT verification library as a real-world benchmark
