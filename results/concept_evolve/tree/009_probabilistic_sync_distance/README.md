# Probabilistic Sync Distance

## Topic Context

When a Huffman decoder starts at an arbitrary (misaligned) offset in a bitstream,
it will eventually synchronize with the true codeword boundaries. The expected
distance to this synchronization event is a fundamental parameter that governs
the feasibility and efficiency of all sync-point-based parallel decoding schemes.

This connects deeply to renewal theory. The misaligned decoder generates a sequence
of "pseudo-symbols" with random lengths. Synchronization occurs when the cumulative
length happens to land on a real boundary. This is a renewal process, and the expected
time to renewal is governed by the code's length distribution.

Key relationships:
- Codes with high length variance synchronize faster (more "chances" to hit a boundary)
- Codes with uniform length are hardest to synchronize (no diversity in step sizes)
- The max codeword length L bounds the worst case (guaranteed sync within O(L^2) bits)
- For DEFLATE (L<=15), empirical sync distances are typically 30-80 bits

This analysis directly determines the minimum viable chunk size for parallel decoding
and the expected overhead of sync-point finding.

## Key Challenges

- Exact analysis requires modeling the conditional decode distribution for misaligned offsets
- Real DEFLATE data is not i.i.d.; context matters for actual sync behavior
- Worst-case codes (uniform length) need special handling
- Trade-off between theoretical guarantees and average-case performance

## Implementation Backlog

1. [ ] Implement renewal-theory-based sync distance estimator
2. [ ] Validate against Monte Carlo simulation on 1000 random Huffman codes
3. [ ] Profile sync distances for real DEFLATE blocks from major corpora
4. [ ] Derive closed-form bounds for canonical Huffman codes
5. [ ] Build sync distance predictor from Huffman table statistics
6. [ ] Use predictions to set optimal chunk sizes in parallel decoder
7. [ ] Analyze worst-case codes and design fallback strategies
8. [ ] Investigate connection to Markov chain mixing time
