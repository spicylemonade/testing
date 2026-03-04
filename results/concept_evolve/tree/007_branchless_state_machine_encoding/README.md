# Branchless State Machine Encoding

## Topic Context

The CSV parser's scalar fallback path (used for tail bytes, platforms without SIMD, and debugging) still needs a state machine to track quote context. Traditional implementations use if/switch statements that cause branch mispredictions on CSV data with mixed quoting patterns.

Branchless programming, borrowed from constant-time cryptography and GPU shader programming, replaces conditional branches with arithmetic/bitwise operations that always execute the same instructions regardless of input.

## Key Insight

CSV has only 3-4 states. A 15-entry lookup table (3 states x 5 char classes) fits in a single cache line. The transition `T[state * 5 + class]` is a single memory load with zero branches. Output actions (emit field, emit row) can be computed with bitwise AND against state predicates.

## Implementation Backlog

- [ ] Design state encoding and transition table
- [ ] Implement branchless scalar CSV parser
- [ ] Compare branch misprediction rate vs. branchy parser
- [ ] Benchmark on quote-heavy and quote-free CSV data
- [ ] Verify constant-time property (no timing variation with input)
- [ ] Integrate as fallback for SIMD parser's tail-byte processing
