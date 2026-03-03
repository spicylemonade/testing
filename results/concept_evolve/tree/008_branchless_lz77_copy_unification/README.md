# Branchless LZ77 Copy Unification

## Topic Context

DEFLATE's inner loop has a fundamental branch: after decoding a Huffman symbol, the decoder must decide whether it's a literal (value 0-255), an end-of-block marker (256), or a length code (257-285) initiating a copy. This branch is data-dependent and hard to predict, especially for mixed content where literals and copies alternate unpredictably.

On modern CPUs with 15-20 cycle branch misprediction penalties, even a 10% misprediction rate costs significant throughput. For a decoder processing 1 billion symbols per second, 100 million mispredictions * 15 cycles = 1.5 billion wasted cycles.

## Key Insight

Charles Bloom (cbloom) showed that LZ77 can be made branchless by observing that both literals and copies are fundamentally the same operation: **copy N bytes from some source to the output**. For literals, the source is the compressed stream; for copies, it's the output buffer. A conditional move (CMOV) selects the source pointer without branching.

## Implementation Backlog

1. **Branch misprediction profiling**: Measure misprediction rates in libdeflate's inflate on diverse file types
2. **CMOV-based selector**: Implement source pointer selection using x86 CMOV instruction
3. **Fixed-size over-copy**: Always copy a fixed large size (e.g., 32 bytes) but only advance output pointer by actual length
4. **Literal run batching**: Accumulate consecutive literals into a single memcpy for amortized overhead
5. **ARM CSEL variant**: Port branchless technique to ARM64 using CSEL (conditional select)
6. **Interaction with multi-stream**: Combine branchless LZ77 with multi-stream Huffman for compounding gains
7. **Compiler auto-vectorization**: Test if modern compilers (GCC 14, Clang 18) can auto-vectorize the branchless loop
