# Probabilistic Sync Point Discovery

## Topic Context

The core challenge of parallel DEFLATE decompression is finding safe entry points in the compressed stream. DEFLATE blocks begin with 3 header bits (BFINAL + BTYPE) but are not byte-aligned, making them hard to find without sequential decode.

pugz (Kerbiriou & Chikhi, 2019) showed that for text-only content, block boundaries can be discovered by trial-and-error decompression. rapidgzip (Knespel & Brunst, 2023) generalized this with a cache-prefetch architecture that handles arbitrary binary content.

## Key Insight

DEFLATE block boundaries have **statistical signatures**: a dynamic Huffman block starts with specific bit patterns (BTYPE=10, followed by HLIT/HDIST/HCLEN fields with constrained value ranges). These patterns can be detected by a fast SIMD scan without actually attempting decompression. The scan reduces the search space from every bit position to a small set of high-probability candidates.

This is analogous to **frame synchronization** in digital communications: receivers scan for known preamble patterns to synchronize with the transmitted signal, tolerating false positives through subsequent validation.

## Implementation Backlog

1. **Block boundary characterization**: Analyze bit-level statistics of real DEFLATE block headers
2. **Pattern signature extraction**: Identify discriminative bit patterns that distinguish real block headers from random data
3. **SIMD pattern scanner**: Use pcmpistri/pcmpistrm (SSE4.2) or VPMOVMSKB (AVX2) for fast bitwise pattern matching
4. **Bayesian scoring model**: Score candidate positions based on multiple features (bit pattern match, field value plausibility)
5. **False positive filtering**: Attempt lightweight validation (Kraft inequality check) before full speculative decode
6. **Integration with speculative framework**: Feed high-scoring candidates to concept 001's speculative block boundary detection
7. **Streaming variant**: Adapt for real-time scanning of network-streamed gzip data (HTTP responses)
8. **Cross-format support**: Extend patterns for PNG (IDAT chunks), ZIP (local file headers), Git (pack objects)
