# Sync Point Convergence

## Topic Context

Variable-length prefix codes (Huffman codes, x86 instructions) have the property that
when you begin decoding from an arbitrary (misaligned) position in the bitstream, the
decoded boundaries will eventually converge to the correct boundaries. This is because
each misaligned decode produces a result of some length, advancing the cursor to a new
position that may or may not be aligned. With high probability, after a few symbols the
cursor lands on a real boundary.

Dougallj formalized this into a practical algorithm: launch `n` parallel decoders at `n`
consecutive offsets (where n = maximum codeword length). At least one decoder is guaranteed
to start at a valid boundary. As decoders advance, they merge when they reach the same
offset. When all have merged, you've found a synchronization point.

This technique was demonstrated on DEFLATE Huffman decoding with a ~25% speedup on
Apple M1 by splitting a single Huffman block into two halves decoded simultaneously
(exploiting instruction-level parallelism).

## Key Challenges

- DEFLATE blocks have unknown sizes, requiring heuristic guessing of midpoints
- LZ77 back-references from the second half may depend on first half output
- Adversarial inputs (all same-length codewords) can prevent convergence
- Error handling complexity when speculative second-half overshoots block boundary

## Implementation Backlog

1. [ ] Implement sync-point finder for canonical Huffman codes (DEFLATE format)
2. [ ] Benchmark convergence distance across Silesia, Canterbury, Calgary corpora
3. [ ] Characterize worst-case inputs and add bailout heuristic
4. [ ] Implement 2-way ILP decode: split block at sync point, decode both halves
5. [ ] Handle LZ77 back-reference fixup for second-half output
6. [ ] Benchmark on x86-64 (Zen4, Sapphire Rapids) and ARM (Apple M2/M4)
7. [ ] Compare to libdeflate and zlib single-thread baselines
8. [ ] Integrate with rapidgzip's multi-core architecture for combined ILP + multi-core
