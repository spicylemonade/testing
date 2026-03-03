# SIMD Bitstream Swizzling

## Topic Context

The fundamental bottleneck in DEFLATE decompression is that Huffman-coded bits form a single serial stream: you must decode symbol N before you can find where symbol N+1 begins. SIMD instructions can process 16-64 data elements in parallel, but only if those elements are independent.

**Bitstream swizzling** breaks this serial dependency by reorganizing the compressed data at encoding time so that multiple independent sub-streams are interleaved in a SIMD-friendly pattern. Each SIMD lane processes its own independent Huffman stream.

NVIDIA's **GDeflate** demonstrated this for GPUs: by swizzling DEFLATE bits to extract 32-way parallelism, GPU decompression achieves throughput impossible with the standard format. Sneller's **Iguana** applied similar principles to AVX-512 CPUs, achieving 13 GB/s on a single core -- nearly 2x faster than LZ4 with comparable compression ratios.

## Key Trade-off

Swizzling requires **format modification** at compression time. This means it cannot accelerate existing DEFLATE files. However, for new data (cloud storage, databases, game assets), the format change is acceptable and the performance gain is transformative.

## Implementation Backlog

1. **Swizzle encoder**: Modify a DEFLATE encoder to emit W-way interleaved Huffman sub-streams
2. **AVX-512 decoder**: Implement parallel Huffman decode using VPERMB, vpcompressb, VBMI2 instructions
3. **Lane synchronization**: Handle the case where lanes decode at different rates (symbol length variation)
4. **LZ77 integration**: After parallel Huffman decode, execute LZ77 copies (still partially serial)
5. **Fallback path**: Scalar decoder for CPUs without AVX-512 (decode interleaved streams sequentially)
6. **Compression ratio analysis**: Verify that swizzling does not degrade compression ratio vs standard DEFLATE
7. **Benchmark against Iguana**: Compare throughput, compression ratio, and CPU utilization
