# Speculative Structural Indexing

## Context

JSON structural indexing — the process of identifying all structural characters ({, }, [, ], :, ,) and their positions while tracking which characters are inside strings — is the performance-critical first stage of SIMD-based JSON parsers like simdjson. The key bottleneck is the **sequential string-state dependency**: whether a structural character is inside a string depends on the parity of all preceding quote characters, creating a data dependency that prevents straightforward parallelization.

This concept applies **speculative execution** (from CPU architecture) to break this dependency: process chunks in parallel with a guessed initial string state, then fix up the few chunks where the guess was wrong.

## Key Insight

The JSON DFA has a **high convergence rate**: regardless of the assumed initial state, the parser converges to the correct state within a few structural characters. This means speculation almost always succeeds, making fixup rare and cheap.

## Cross-Domain Bridges

- **CPU branch prediction**: speculate on the likely execution path, execute speculatively, roll back on misprediction
- **Speculative parallel DFA matching** (Ko et al. 2012): partition input strings for parallel regex matching with provable speculation guarantees
- **GPU warp execution**: all threads in a warp speculatively follow the same path; here, all chunks speculatively assume the same string state

## Implementation Backlog

1. [ ] Build the complete JSON DFA and enumerate its states
2. [ ] Compute convergence factor empirically on real JSON files
3. [ ] Implement per-chunk speculative Stage 1 with configurable chunk size
4. [ ] Implement chunk-boundary string-state reconciliation
5. [ ] Benchmark against baseline simdjson on standard test files
6. [ ] Profile speculation miss rates across different JSON genres
7. [ ] Integrate with entropy-adaptive chunk sizing (concept 10)
8. [ ] Test with adversarial inputs (pathological string density)
9. [ ] Measure scaling efficiency with 2/4/8/16 parallel chunks
10. [ ] Write up convergence analysis as standalone technical note
