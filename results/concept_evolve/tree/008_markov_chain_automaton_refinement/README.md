# Markov Chain Automaton Refinement for Lower Bounds

## Topic Context

The automaton-based approach is the most successful computational method for lower bounds:

### History of Lower Bounds (sigma=2, d=2)
| Year | Bound | Method | Reference |
|------|-------|--------|-----------|
| 1994 | 0.773911 | DFA, buffer h | Dancik |
| 2009 | 0.788071 | DFA, buffer h=15 | Lueker |
| 2024 | 0.792665992 | DFA, optimized h | Heineman et al. |

### How It Works
1. Design a DFA that reads symbol pairs from two random binary strings
2. At each step, the DFA decides whether to "match" (output common character) or "skip"
3. The DFA's matching rate on random inputs is analyzed as a Markov chain
4. The steady-state matching rate is a rigorous lower bound on gamma_2

### Key Bottleneck
The state space grows exponentially with buffer size h: |Q| = 2^h * 2^h * O(1).
For h=15, |Q| ~ 10^9, requiring careful memory management.

## Implementation Backlog

1. [ ] Reproduce Heineman et al. (2024) results for h=14,15
2. [ ] Profile runtime and memory bottlenecks
3. [ ] Design new state space exploiting alignment structure (not just buffer)
4. [ ] Implement h=16 with distributed computing
5. [ ] Explore RL-based automaton design (see concept 012)
6. [ ] Investigate whether the upper bound dual can be improved similarly
