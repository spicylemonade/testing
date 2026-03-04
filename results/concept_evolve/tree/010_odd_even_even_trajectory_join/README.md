# Odd-Even-Even Trajectory Join

## Topic Context

The Odd-Even-Even (OEE) Sieve is a structural pruning rule based on the observation (Eliahou 2023) that specific patterns in the sequence of odd/even Collatz steps guarantee trajectory merging. When a sequence has one or more odd steps followed by at least 2 even steps, the trajectory joins that of a smaller number.

This can be detected by a finite automaton that tracks the step pattern, requiring only 2 bits of state.

## Cross-Domain Bridges

- **Automata theory**: Finite state machines for pattern detection in sequences
- **Symbolic dynamics**: Classifying orbits by their symbolic itineraries
- **Network protocol verification**: Detecting invalid state transitions

## Implementation Backlog

- [ ] Implement 2-bit state machine for OEE detection
- [ ] Integrate into recursive bit-tree traversal
- [ ] Measure marginal pruning rate beyond Descent + Path-Merging
- [ ] Encode OEE patterns into bitvector precomputation (Definition 4.3)
- [ ] Test extended patterns (odd run + 3 even steps)
- [ ] Analyze theoretical frequency of OEE patterns in random sequences
