# ConceptEvolve Reframe Analysis

## Query

"The branchless binary GCD inner loop has a 5-cycle critical path from SUB to TZCNT to SARX — can this dependency chain be broken?"

## Method

Used ConceptEvolve `reframe` command to evaluate the problem from 8 different domain perspectives, looking for transferable techniques that might further reduce the critical path latency.

## Reframings

### 1. Digital Circuit Design / VLSI

**Key Insight**: The critical path in a binary GCD hardware unit is dominated by the conditional subtraction and comparison logic; restructuring the datapath to use carry-lookahead or speculative computation can collapse multiple serial dependencies into parallel ones.

**Technique**: Pipeline stage insertion (retiming), carry-lookahead adders for the subtraction step, and speculative dual-path execution where both possible outcomes of a comparison are computed simultaneously and the correct one is selected via a multiplexer.

**Feasibility**: **Partially applicable.** Our CMOV-based approach already implements the software equivalent of a multiplexer-selected dual path. However, the pipeline retiming insight is interesting — it suggests that throughput-oriented applications (batch GCD) could benefit from software pipelining across multiple independent GCD computations, even if single-computation latency cannot be reduced.

### 2. Compiler Optimization / Instruction Scheduling

**Key Insight**: Converting control flow to data flow (branchless code) and exploiting hardware CTZ instructions can dramatically shorten the dependency chain.

**Technique**: If-conversion to CMOV, __builtin_ctz, loop unrolling, and software pipelining to overlap iterations on out-of-order cores.

**Feasibility**: **Already implemented.** This is precisely what our combined algorithm does. The reframing validates our approach. We explored loop unrolling (speculative_gcd.h) and found it provided no improvement due to register pressure — confirming this domain's suggestion has been fully exploited.

### 3. Project Management / Operations Research (CPM)

**Key Insight**: The critical path can only be shortened by "crashing" activities on it — spending extra resources to reduce bottleneck duration. Non-critical tasks have float.

**Technique**: Identify cheapest-to-crash activities, compute cost-time tradeoff curves, crash iteratively until the critical path shifts.

**Feasibility**: **Insightful framing.** Applying this: our 5-cycle critical path is SUB(1c) → TZCNT(3c Skylake / 2c Zen) → SHRX(1c). The "cheapest to crash" is TZCNT at 3 cycles. On Zen 3/4 where TZCNT is 2 cycles, the critical path drops to 4 cycles — a free 20% improvement. On Skylake, there is no cheaper TZCNT substitute. The CPM analysis confirms we've exhausted the crashing budget on this specific microarchitecture.

### 4. Graph Theory / Network Flow

**Key Insight**: DAG longest-path analysis reveals which edges can be contracted (operation fusion) or which nodes can be parallelized.

**Technique**: Node splitting, edge contraction, Dilworth's theorem for minimum parallel chains.

**Feasibility**: **Limited.** The inner loop DAG is already minimal — 3 operations on the critical path with no parallelizable alternatives. SUB depends on both operands (input), TZCNT depends on SUB result, SHRX depends on TZCNT result. There are no independent chains to exploit.

### 5. Control Theory / Feedback Systems

**Key Insight**: Convergence speed depends on the contraction rate per iteration. Processing multiple bits per step increases the "loop gain."

**Technique**: Multi-bit acceleration — processing k trailing zeros or k bits of quotient per step, look-ahead techniques, coordinate transformation.

**Feasibility**: **Future work candidate.** This is essentially Lehmer's method for large integers — using leading bits to predict multiple quotient steps. For 64-bit integers, our initial mod step already provides the largest single-step contraction. For 128/256-bit, a Lehmer-style approach could reduce iteration count from ~128 to ~70 by processing ~2 bits per iteration via 64-bit approximate quotients. This is the most promising unexplored direction for wider integers.

### 6. Parallel / Distributed Computing

**Key Insight**: Speculative parallel execution trees computing 2^k possible future states for k steps ahead.

**Technique**: Batched GCD computation across independent instances using SIMD parallelism (inter-problem parallelism).

**Feasibility**: **Viable for throughput workloads.** We already documented that SIMD TZCNT emulation makes single-pair SIMD unprofitable. However, for applications computing many independent GCDs (e.g., rational number normalization in bulk), AVX-512 batch processing with 8 independent 64-bit GCDs in parallel could achieve near-8x throughput improvement. This remains future work.

### 7. Information Theory / Coding Theory

**Key Insight**: The algorithm processes ~1 bit of information per iteration. Processing multiple bits per step is like using higher-rate codes.

**Technique**: k-ary GCD, Lehmer's method, MSB-guided large jumps.

**Feasibility**: **Same as Reframing 5.** The information-theoretic minimum iterations for 64-bit GCD is ~64 (processing 1 bit/iteration). Our combined algorithm averages ~40 iterations (due to the initial mod reducing bit-width). Further improvement requires multi-bit-per-iteration methods, which are most beneficial at 128+ bits.

### 8. Biological Evolution / Genetic Algorithms

**Key Insight**: The design space is vast; evolutionary search might find non-obvious combinations.

**Technique**: Multi-objective GA optimizing for latency, area, power.

**Feasibility**: **Interesting but impractical for this scope.** An auto-tuning framework that explores combinations of (initial-mod: yes/no, LUT-size: 0/256/4096, unroll-factor: 1/2/4, loop-variant: stein/binary/hybrid) across different input distributions could potentially find distribution-specific optimal configurations. This is an engineering direction rather than an algorithmic breakthrough.

## Summary

| Domain | Applicable? | Already Exploited? | Future Work? |
|--------|------------|-------------------|-------------|
| VLSI / Retiming | Partially | CMOV ≈ mux select | Batch pipelining |
| Compiler / Scheduling | Yes | Fully | — |
| CPM / Crashing | Insightful | Exhausted on Skylake | Zen benefits from 2c TZCNT |
| Graph Theory | Limited | DAG is minimal | — |
| Control Theory | Promising | Initial mod only | Lehmer for 128/256-bit |
| Parallel Computing | Viable | Not implemented | SIMD batch GCD |
| Information Theory | Same as #5 | Partial | Multi-bit per iteration |
| Genetic Algorithms | Impractical | — | Auto-tuning framework |

## Conclusion

The reframe analysis confirms that the 5-cycle critical path (SUB → TZCNT → SHRX) on Skylake is a hard lower bound for this algorithmic structure. The two most promising unexplored directions are:

1. **Lehmer-style multi-bit acceleration for 128/256-bit integers** (Control Theory / Information Theory reframing): Process ~2 bits per iteration using 64-bit approximate quotients, reducing iteration count by ~40%.

2. **SIMD batch GCD for throughput workloads** (Parallel Computing reframing): Process 4-8 independent GCD computations in parallel using AVX2/AVX-512, achieving near-linear throughput scaling.

Both are documented as future work items. For single-pair 64-bit GCD latency, our combined algorithm appears to be at or near the practical optimum for the binary GCD family.
