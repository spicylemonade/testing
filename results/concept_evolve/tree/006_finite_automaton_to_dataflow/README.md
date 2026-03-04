# Finite Automaton to Dataflow Transformation

## Topic Context

Traditional CSV parsers are implemented as finite state machines (FSMs) that consume one byte at a time and transition between states (NORMAL, IN_QUOTE, ESCAPE, etc.). This creates a chain of serial dependencies -- each state depends on the previous byte's state.

The key architectural insight from simdjson is to replace the FSM with a dataflow graph where each stage operates on bitmasks representing structural properties of the input. This transforms sequential control-flow dependencies into parallel data-flow operations on wide SIMD vectors.

## Key Insight

An FSM has O(N) serial dependency depth. A 4-stage dataflow pipeline on W-byte SIMD blocks has O(N/W) serial depth, a W-fold reduction. Each stage is independently optimizable and the pipeline can be software-pipelined for ILP.

## Implementation Backlog

- [ ] Define stage interfaces: Block -> ClassifyResult -> QuoteResult -> MaskedResult -> Fields
- [ ] Implement software pipelining across stages
- [ ] Profile per-stage latency to identify bottleneck stage
- [ ] Measure IPC improvement over monolithic FSM parser
- [ ] Consider out-of-order processing of non-dependent stages
- [ ] Evaluate whether Stage 2 (quote resolution) limits overall pipeline throughput
