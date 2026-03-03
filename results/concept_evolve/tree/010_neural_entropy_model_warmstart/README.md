# Neural Entropy Model Warmstart

## Topic Context

Every DEFLATE block with dynamic Huffman codes requires constructing a decode table from the code-length sequence embedded in the block header. This construction involves: reading the code-length alphabet, decoding code lengths via a secondary Huffman tree, and building the primary decode table. This overhead is non-trivial, especially for small blocks.

The insight from neural compression research (Piau 2025, "Learning from entropy-encoded data") is that entropy-coded data has learnable statistical structure. A neural network trained on real-world DEFLATE blocks can predict the likely code distribution from minimal header information.

## Key Insight

DEFLATE's dynamic Huffman tables exhibit strong statistical regularity: most text files produce similar code distributions (common letters get short codes), most binary files produce flatter distributions. A tiny ML model can exploit this regularity to precompute decode tables speculatively, overlapping with the actual table construction.

## Caveat

This concept is the most speculative of the 12. Table construction is typically a small fraction of total decode time (5-15% for large blocks). The payoff is largest for streams with many small blocks or when combined with multi-block parallel decoding where table construction is on the critical path.

## Implementation Backlog

1. **Training data collection**: Instrument libdeflate to log code-length arrays from real DEFLATE blocks
2. **Model architecture**: Design tiny MLP (must run in <1 microsecond) with quantized weights
3. **Feature engineering**: Extract predictive features from block headers and preceding block statistics
4. **Speculative decode pipeline**: Decode with predicted tables while actual tables are built in parallel
5. **Misprediction recovery**: Detect misprediction and fall back to actual tables with minimal overhead
6. **ONNX/TFLite inference**: Use lightweight inference runtime for the neural model
7. **Common-case optimization**: Cache the K most common code distributions (skip neural inference for known patterns)
