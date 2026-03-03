# ANS Replacement Entropy Layer

## Topic Context

DEFLATE uses Huffman coding for entropy compression. Huffman is simple and fast, but it has a fundamental limitation: it can only assign integer bit lengths to symbols, wasting up to 1 bit per symbol compared to the theoretical entropy limit. This 0.5-1 bit/symbol overhead compounds across billions of decompression operations globally.

Asymmetric Numeral Systems (ANS), invented by Jarek Duda (2009), combines the compression efficiency of arithmetic coding with the speed of Huffman coding. ANS decoding is a single table lookup + state update, with no bit-shifting or range management. Zstandard (Facebook/Meta) adopted FSE (a tANS variant) and demonstrated ~50% faster decoding than Huffman with better compression.

## Key Insight

ANS has a unique property: encoder and decoder states are perfectly symmetric, meaning multiple ANS streams can be **interleaved into a single bitstream without any metadata**. This enables trivial parallelization: decode K streams simultaneously, each requiring only one table lookup per symbol.

## Implementation Backlog

1. **tANS table generator**: Build tANS tables from DEFLATE-style code-length sequences
2. **4-way interleaved decoder**: 4 independent ANS state machines decoded per iteration
3. **SIMD acceleration**: Use VPGATHERD for parallel table lookups across 8 ANS states
4. **Compression ratio comparison**: Measure bits/symbol vs Huffman on typical DEFLATE workloads
5. **Format specification**: Define "DEFLATE-ANS" block format with backward-compatible signaling
6. **Zstandard comparison**: Benchmark decode speed against zstd's FSE implementation
7. **Streaming support**: Ensure ANS variant works with streaming (non-seekable) inputs
