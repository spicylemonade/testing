# SIMD Literal Scatter / LZ77 Copy Acceleration

## Context

DEFLATE decompression involves two interleaved operations: Huffman symbol decoding and LZ77 output reconstruction. The LZ77 phase copies bytes from the output buffer (for back-references) or writes literal bytes directly. For back-references with distance >= 16, SIMD copy is straightforward. For short distances (e.g., distance=1 for run-length encoding), a specialized approach is needed.

The "chunkcopy" optimization (zlib-cloudflare) copies 16 bytes at a time using SSE, even when fewer bytes are needed, relying on output buffer padding to safely over-write.

## Techniques

1. **Wide literal copy**: Decoded literals are buffered and flushed 16/32 bytes at a time
2. **Wide match copy**: For distance >= 16, use memcpy-style SIMD loops
3. **Short-distance pattern fill**: For distance < 16, replicate the pattern using pshufb then write
4. **Overlapping writes**: Allow writes past the actual end, safe with buffer padding

## Implementation Backlog

- [ ] Benchmark scalar vs SSE2 vs SSSE3 vs AVX2 copy routines
- [ ] Implement pshufb-based short-distance pattern fill for distances 1-15
- [ ] Measure branch mispredict cost for distance < 16 vs >= 16 check
- [ ] Profile which copy lengths are most common in real DEFLATE data
- [ ] Test with AVX-512 masked stores for precise-length copies without padding
- [ ] Measure L1/L2 cache effects of wide copies on decode table retention
