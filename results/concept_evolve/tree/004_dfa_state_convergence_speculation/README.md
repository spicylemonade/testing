# DFA State Convergence Speculation

## Context

The fundamental barrier to parallelizing JSON parsing is the sequential state dependency: the parser's state at position i depends on all bytes 0..i-1. However, for DFAs with the **convergence property**, the state tends to converge to the same value regardless of the initial state after processing a short prefix. If the JSON DFA converges rapidly, we can partition the input and process chunks in parallel with arbitrary initial state guesses.

## Key Insight

JSON's grammar has very few states (~8-12 for the core parser). Structural characters ({, [, }, ], :, ,) force the DFA into specific states regardless of the starting state. Since structural characters appear frequently in JSON (every ~10-20 bytes on average), convergence should be very fast, potentially within 2-4 bytes of a chunk boundary.

## Cross-Domain Bridges

- **Markov chain mixing time**: convergence in DFAs is analogous to a Markov chain rapidly reaching its stationary distribution
- **Distributed consensus**: validators converge to agreement despite starting from different states
- **Speculative decoding in LLMs**: draft model speculates tokens that may be verified by the target model

## Implementation Backlog

1. [ ] Formally specify the JSON DFA (states, transitions, alphabet equivalence classes)
2. [ ] Compute the convergence factor gamma for the JSON DFA
3. [ ] Empirically measure convergence distance on 20+ real-world JSON files
4. [ ] Plot convergence CDF: fraction of chunk boundaries vs. bytes to convergence
5. [ ] Build a convergence lookup table for fast runtime checks
6. [ ] Integrate with speculative structural indexing (concept 1)
7. [ ] Analyze worst-case inputs (pure string data, deeply escaped content)
8. [ ] Compare against enumeration-based approach (run all |Q| states in parallel, take correct one)
