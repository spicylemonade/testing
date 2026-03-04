# Wavefront LZ77 Resolution

## Topic Context

DEFLATE uses two layers of compression: LZ77 (dictionary-based) followed by Huffman
coding. Even if Huffman decoding is parallelized perfectly, the LZ77 back-references
create a second serial dependency: output byte at position P may reference bytes at
positions P-D through P-D+L-1, which themselves may be back-references.

The key insight is that these dependencies form a DAG, not a linear chain. Most
references point to recently decompressed data (short distances), and reference chains
are typically shallow. This enables wavefront parallelism: process all positions whose
dependencies are satisfied, then process the next frontier.

Sitaridi et al. formalized two approaches:
- **MRR (Multi-Round Resolution)**: Iterate rounds of memcpy, each resolving one level
  of reference indirection. Typically converges in 3-5 rounds.
- **DE (Dependency Elimination)**: Modify the compressor to avoid deep reference chains,
  trading ~10% compression ratio for guaranteed single-round resolution.

## Key Challenges

- Chain depth depends on compression level and data characteristics
- Scatter/gather memory access patterns hurt cache performance
- Output buffer must handle overlapping copies (when len > dist)
- Two-phase (Huffman then LZ77) approach doubles memory traffic

## Implementation Backlog

1. [ ] Profile LZ77 chain depths across compression levels 1-9
2. [ ] Implement MRR on CPU using AVX-512 gather/scatter
3. [ ] Implement dependency bitvector for tracking resolved positions
4. [ ] Benchmark rounds-to-convergence on real data
5. [ ] Implement DE-compatible compressor variant
6. [ ] Measure compression ratio impact of depth-limited LZ77
7. [ ] Profile cache miss rates during scatter/gather resolution
8. [ ] Integrate with parallel Huffman decode for end-to-end pipeline
