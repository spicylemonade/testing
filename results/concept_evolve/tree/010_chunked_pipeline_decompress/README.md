# Chunked Pipeline Decompression

## Context

Standard DEFLATE decompression interleaves three operations in a single loop: Huffman decode, LZ77 copy, and checksum update. This tight coupling prevents optimizing each phase independently and limits pipeline utilization.

## Pipeline Architecture

```
Time ->
        Chunk 0    Chunk 1    Chunk 2    Chunk 3
Stage 1: [Huffman]  [Huffman]  [Huffman]  [Huffman]
Stage 2:           [LZ77]     [LZ77]     [LZ77]
Stage 3:                      [CRC32]    [CRC32]
```

## Benefits

1. **Phase-specific optimization**: Huffman loop is pure decode (no branching on literal/match), LZ77 loop is pure copy (SIMD-optimized), checksum is pure SIMD reduction
2. **Better branch prediction**: The Huffman-only loop has fewer branch types
3. **Better SIMD utilization**: LZ77 copies can use wider SIMD without decode stalls
4. **Multi-thread friendly**: Each stage can run on a different core with double-buffered token queues

## Token Buffer Format

Each token: 4 bytes
- Literal: `[0x00][byte_value][unused][unused]`
- Match: `[length_high:4|0001][length_low:8][distance:16]`
- End-of-block: `[0xFF][0x00][0x00][0x00]`

## Implementation Backlog

- [ ] Design token buffer format and allocation strategy
- [ ] Implement Huffman-to-token decoder
- [ ] Implement token-to-bytes LZ77 reconstructor
- [ ] Implement SIMD-accelerated CRC32/Adler32 stage
- [ ] Benchmark single-thread pipeline vs monolithic decode
- [ ] Implement multi-thread pipeline with lock-free ring buffers
- [ ] Measure memory overhead of token buffers
