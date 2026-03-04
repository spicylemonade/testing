# Bitstream Swizzle Interleaving

## Topic Context

NVIDIA's GDEFLATE format is a key innovation: it takes a standard DEFLATE bitstream
and rearranges the bits so that 32 parallel decoders can each read an independent
sub-stream. The crucial insight is that this is a pure bit permutation — it doesn't
change the compression ratio at all (with minor end effects). The same Huffman tables,
the same LZ77 references, just reordered bits.

The "swizzle" distributes consecutive bits round-robin across 32 lanes. Lane k reads
every 32nd bit starting from bit k. Since each lane sees a contiguous sequence of the
original bitstream, it can perform standard Huffman decoding independently.

This approach requires format modification (not backward compatible with DEFLATE),
but preserves compression ratio and enables massive parallelism on GPUs. Microsoft's
DirectStorage uses GDEFLATE for game asset decompression, achieving throughput that
saturates NVMe SSD bandwidth.

## Key Challenges

- Requires format change (not backward compatible with existing gzip/zlib)
- LZ77 back-references still create inter-lane dependencies in the output phase
- CPU SIMD (AVX-512) has only 16 lanes at 32-bit width vs. GPU's 32 warp lanes
- Transcoding from DEFLATE to GDEFLATE has non-trivial overhead

## Implementation Backlog

1. [ ] Study Microsoft's GDEFLATE reference implementation in detail
2. [ ] Implement DEFLATE-to-GDEFLATE transcoder (bitstream-level, no decompress)
3. [ ] Implement AVX-512 parallel Huffman decoder for swizzled streams
4. [ ] Handle LZ77 resolution in a second pass after Huffman decode
5. [ ] Benchmark transcoder throughput (target: >5 GB/s single-core)
6. [ ] Benchmark parallel decode throughput vs. libdeflate/zstd
7. [ ] Evaluate for CPU SIMD (16-lane AVX-512 vs. 32-lane GPU warp)
8. [ ] Measure end-to-end pipeline: storage -> transcode -> parallel decode
