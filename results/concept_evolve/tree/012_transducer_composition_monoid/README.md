# Transducer Composition Monoid

## Topic Context

A Finite State Transducer (FST) reads input symbols and produces output symbols while
transitioning between states. Huffman decoding is a special case: input = bits,
output = decoded symbols, states = positions in the Huffman tree.

The composition of two FSTs is another FST. This composition is associative, meaning
FSTs form a monoid under composition. This algebraic structure is the foundation for:
1. **Parallel prefix scan**: compose N transition functions in O(log N) depth
2. **Chunk-based amortization**: precompute composition for k-bit chunks, reducing
   per-symbol overhead

For speech recognition, WFST (Weighted FST) composition is a critical optimization:
composing the language model, pronunciation dictionary, and acoustic model into a
single transducer enables efficient beam search. The same idea applies here:
precompute the composition of multiple bit transitions into a single chunk transition.

Concretely: for an 8-bit chunk, precompute a table mapping (current_state, byte_value)
to (next_state, list_of_decoded_symbols). This replaces 8 sequential bit-level
transitions with a single table lookup plus output copy.

## Key Challenges

- Table size grows as |Q| * 2^k * avg_output_size
- For DEFLATE, Q changes per block (dynamic Huffman tables) requiring rebuild
- Table build time must be amortized over enough decoded bytes
- Output buffering: variable number of symbols per chunk complicates output layout

## Implementation Backlog

1. [ ] Formalize the FST model for canonical Huffman codes
2. [ ] Implement chunk-transducer table builder
3. [ ] Benchmark table build time vs. block size for amortization analysis
4. [ ] Implement byte-at-a-time decode using precomputed tables
5. [ ] Measure throughput improvement over bit-at-a-time decode
6. [ ] Profile L1 cache occupancy for different chunk sizes
7. [ ] Implement lazy table construction (build entries on demand, cache)
8. [ ] Integrate with parallel prefix scan for combined chunk + parallel approach
