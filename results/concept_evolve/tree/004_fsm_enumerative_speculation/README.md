# FSM Enumerative Speculation

## Topic Context

Huffman decoding is a finite state machine (FSM) where the state is the current bit position within a code word. This FSM has been called "embarrassingly sequential" because each state transition depends on the previous one. However, Zhao et al. (ASPLOS 2014) showed that FSMs can be parallelized through principled speculation.

The key insight: if you start decoding at an arbitrary bit position, you are in an unknown state. But after processing enough bits, speculative paths **converge** to the correct state. Jiang & Agrawal (PPoPP 2017) extended this with **enumerative speculation**: instead of guessing one state, enumerate a small set of likely states and run them all in parallel using SIMD.

For DEFLATE's Huffman codes (max length 15 bits), there are at most 15 possible start states within a code. SIMD with 16 lanes (AVX-512) can enumerate ALL states simultaneously, guaranteeing convergence.

## Key Trade-off

More speculative paths = faster convergence but more wasted work. The optimal number of paths depends on the FSM's convergence rate, which depends on the code distribution.

## Implementation Backlog

1. **DEFLATE FSM formalization**: Express Huffman decode as explicit FSM with transition tables
2. **Convergence analysis**: For typical DEFLATE code distributions, measure bits-to-convergence
3. **SIMD enumerative decoder**: Run 8/16 speculative paths using AVX2/AVX-512 gather instructions
4. **Convergence detector**: SIMD comparison to detect when all paths agree on output
5. **Chunk boundary alignment**: Determine optimal chunk sizes for speculation (bits between convergence checks)
6. **Lookback heuristic**: Use preceding decoded symbols to predict likely start states (reduce E)
7. **GPU adaptation**: Map speculative paths to GPU threads instead of SIMD lanes (following GSpecPal)
