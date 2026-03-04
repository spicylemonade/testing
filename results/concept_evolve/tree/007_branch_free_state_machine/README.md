# Branch-Free State Machine

## Context

JSON parsing Stage 2 (value parsing and validation) involves many conditional branches: checking character types, validating number formats, handling escape sequences. On modern out-of-order CPUs, branch mispredictions cost 15-20 cycles each. For JSON inputs with irregular structure (mixed types, varying key lengths), the branch predictor struggles.

## Key Insight

The JSON state machine has only ~8-12 states and ~8 input character equivalence classes. This is small enough to encode the entire transition table in VPSHUFB lookup tables (16 entries per table). Each state transition becomes a single VPSHUFB instruction with zero branches and perfectly predictable throughput.

## Cross-Domain Bridges

- **Constant-time cryptography**: eliminate timing side channels by removing data-dependent branches
- **GPU programming**: warp divergence from branches is the GPU analog of branch misprediction on CPUs
- **Table-driven finite automata**: classic compiler technique using lookup tables instead of switch statements

## Implementation Backlog

1. [ ] Enumerate JSON parser states and character equivalence classes
2. [ ] Build transition table and encode in VPSHUFB register constants
3. [ ] Implement branchless state machine kernel in AVX-512
4. [ ] Measure branch misprediction rate (target: exactly 0)
5. [ ] Profile throughput vs. simdjson's Stage 2 on various inputs
6. [ ] Test on adversarial inputs where branch prediction would fail
7. [ ] Combine with VBMI2 compress/expand for branchless value extraction
8. [ ] Port to ARM NEON using TBL instruction as VPSHUFB equivalent
