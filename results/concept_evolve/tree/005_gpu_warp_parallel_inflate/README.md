# GPU Warp-Parallel Inflate

## Topic Context

GPUs offer massive parallelism (thousands of threads) but DEFLATE decompression is inherently serial. The CODAG paper (Park et al., 2023) showed that prior GPU decompression approaches suffered from poor resource utilization because they dedicated most threads to data movement while few threads actually decoded.

NVIDIA's GDeflate solves the Huffman parallelism problem by swizzling bits to enable 32-way parallel decode. But LZ77 copy operations still create dependencies: overlapping copies (where distance < length) require serial execution.

## Key Insight

CODAG's insight: eliminate specialized thread roles. Instead of having "decoder threads" and "mover threads," let all threads decode, and use the GPU's hardware scheduler to tolerate latency from memory operations. This provides 13.46x speedup for RLE and 1.18x for Deflate over state-of-the-art.

The GSST paper (Vonk et al., 2025) pushes further: 191 GB/s on an A100 by replacing LZ-based compression entirely with GPU-optimized FSST string compression.

## Implementation Backlog

1. **GDeflate baseline implementation**: Implement or port nvCOMP's GDeflate kernel
2. **Warp-shuffle LZ77 copy**: Replace shared memory copies with warp shuffle for distances <= 32
3. **Register-file caching**: Keep recent output bytes in registers for short-distance copies
4. **Pipeline overlap**: Use CUDA streams to overlap Huffman decode and LZ77 execution
5. **Adaptive thread assignment**: Dynamically balance decode vs. copy threads based on block statistics
6. **Multi-GPU scaling**: Distribute chunks across GPUs for terabyte-scale decompression
7. **GPUDirect integration**: Test with GPUDirect Storage for NVMe-to-GPU direct transfer
