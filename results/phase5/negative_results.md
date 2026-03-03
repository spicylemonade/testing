# Negative Results and Failed Approaches

Documenting all approaches that were tried but did not yield improvement, with quantitative data explaining why. These results are essential for reproducibility and guiding future work.

## 1. Bernstein-Yang Divstep (Constant-Time GCD)

**Implementation**: `src/novel/divstep_gcd.h`

**Hypothesis**: The divstep algorithm from Bernstein-Yang 2019, which uses a fixed number of iterations with no data-dependent branches, might achieve competitive performance due to its simple, predictable control flow that avoids branch mispredictions entirely.

**Result**: **3.6x SLOWER** than the best baseline.

| Metric | divstep | stein_classic | combined |
|--------|---------|--------------|----------|
| Median latency (64-bit uniform) | 311.50ns | 100.35ns | 86.57ns |
| Iterations | 127 (fixed) | ~45 (variable) | ~35 (variable) |
| ns/iteration | 2.45 | 2.23 | 2.47 |

**Why it failed**: The divstep algorithm uses exactly 127 iterations for 64-bit inputs (sufficient to guarantee correctness per Theorem 11.2 of BY2019). Variable-iteration algorithms like binary GCD only need ~35-45 iterations on average. The per-iteration cost is nearly identical (~2.4ns), so the 2.8x more iterations directly translate to 2.8x slower execution. The branch-misprediction savings from constant-time execution (~0.5ns per misprediction × ~5 mispredictions = ~2.5ns saved) are negligible compared to the ~200ns of wasted iterations.

**When it IS appropriate**: Divstep is designed for cryptographic applications where constant-time execution is a hard security requirement (preventing timing side channels). For non-cryptographic GCD computation, it is never competitive.

## 2. Fixed-Iteration Branchless Binary GCD

**Implementation**: `src/novel/branchless_gcd.h` — `gcd_branchless_fixed()`

**Hypothesis**: A binary GCD with a fixed iteration count (64 for 64-bit inputs) and fully branchless body might achieve good performance by eliminating all branches, including the loop-exit condition.

**Result**: **280-322ns — 2.8-3.2x SLOWER** than stein_classic, and also failed correctness for some inputs.

**Why it failed**: 
1. **Correctness**: 64 fixed iterations are insufficient for all 64-bit input pairs. Some inputs (e.g., Fibonacci numbers) require more iterations. Increasing to 128 iterations fixes correctness but doubles the already-excessive cost.
2. **Performance**: Same problem as divstep — fixed iterations waste cycles on inputs that converge quickly. The average case needs ~45 iterations but the fixed variant executes 64-128.
3. **Wasted work**: When `a == b` before the iteration limit, the remaining iterations compute `|a-a| = 0`, then `ctz(0)` which is undefined behavior (though our implementation handles it by clamping).

**Lesson**: Eliminating the loop-exit branch is not worth the cost of executing unnecessary iterations. The loop-exit branch (`a != b`) is nearly perfectly predicted by hardware (it's taken ~45 times, not-taken once) with < 1% misprediction rate.

## 3. Speculative 2x Loop Unrolling

**Implementation**: `src/novel/branchless_gcd.h` — `gcd_novel_unrolled()`

**Hypothesis**: Unrolling the inner loop 2x to execute two binary GCD steps per iteration, allowing the CPU's out-of-order engine to overlap computation between the two steps.

**Result**: **101ns — no improvement** over stein_classic (100.4ns).

| Variant | Median (ns) | vs. stein_classic |
|---------|------------|-------------------|
| unrolled 2x | 101.0 | -0.6% (worse) |
| single-step | 91.2 | +9.2% (better) |

**Why it failed**: 
1. **Register pressure**: Unrolling doubles the number of live registers. With a, b, diff, min, ctz_result all live, 2x unrolling requires 10+ registers. On x86-64 with 16 GPRs (minus RSP, RBP, and callee-saved), this causes register spills to the stack.
2. **No ILP benefit**: The second step depends entirely on the first step's output (`a'` from step 1 is the input to step 2). There is no instruction-level parallelism to exploit — the dependency chain is strictly serial.
3. **Code size**: The unrolled loop body exceeds the L1i cache line (64 bytes), causing instruction cache pressure.

**Lesson**: Loop unrolling only helps when there are independent computations to overlap. In a serial dependency chain like binary GCD, unrolling adds overhead without benefit.

## 4. TZCNT-Before-ABS Reordering

**Implementation**: `src/novel/branchless_gcd.h` — `gcd_binary_opt()` variant

**Hypothesis**: Reordering the inner loop to compute `TZCNT` before the absolute-value/min selection might reduce the critical path by allowing TZCNT to start earlier.

**Result**: **190.2ns vs 189.7ns — no measurable difference** (within noise).

**Why it failed**: On the actual hardware, both orderings produce the same critical path latency because the out-of-order engine already schedules TZCNT as early as possible. The SUB instruction that feeds TZCNT depends on the comparison result in both orderings, so there is no scheduling advantage.

**Caveat**: On microarchitectures with shorter out-of-order windows or different TZCNT latencies, this reordering might matter. Our assembly analysis suggests it could provide ~1 cycle benefit on in-order cores.

## 5. SIMD Batch GCD

**Analysis**: `results/phase3/simd_approach.md` (not implemented — deferred after feasibility analysis)

**Hypothesis**: Processing 4 independent GCD pairs simultaneously using AVX2 (256-bit SIMD) would achieve near-4x throughput improvement.

**Why it was not implemented**:
1. **No native SIMD TZCNT**: There is no AVX2/AVX-512 instruction that computes count-trailing-zeros on packed integers. The workaround requires 6-8 SIMD instructions per TZCNT emulation: `VPAND(-x, x)` to isolate lowest bit, then `VPLZCNTD` (AVX-512CD only) or a De Bruijn lookup.
2. **No native SIMD variable shift**: SIMD shift-by-variable requires `VPSRLVD/Q` (AVX2), but the shift amounts differ per lane, preventing use of the simpler `VPSRLQ` with a single shift amount.
3. **Lane divergence**: Different GCD pairs converge at different rates. When one lane finishes (a == b), it must either waste cycles or be masked out, reducing utilization.

**Estimated overhead**: The TZCNT emulation adds ~6 instructions × 0.5ns = 3ns per iteration, while the scalar TZCNT costs ~1ns. Net cost per SIMD iteration: ~8ns for 4 pairs vs. ~2.5ns × 4 = 10ns scalar. The theoretical 20% throughput gain is marginal and depends heavily on the specific instruction mix.

**When it WOULD work**: For applications with thousands of independent GCD computations (e.g., rational arithmetic in computer algebra), the amortized setup cost becomes negligible and SIMD batch processing becomes viable. AVX-512 with `VPLZCNTD` makes TZCNT emulation cheaper, potentially tipping the balance.

## 6. LUT Without Initial Modular Reduction

**Implementation**: `src/novel/lut_gcd.h` — `gcd_lut_hybrid()`

**Hypothesis**: Adding a LUT for small operands to a standard binary GCD loop (without the initial mod step) would provide significant speedup.

**Result**: **87.2ns — decent** but not as good as `combined` (86.6ns) and much worse on skewed inputs.

| Distribution | lut_hybrid | combined | Difference |
|-------------|-----------|----------|-----------|
| uniform | 87.2ns | 86.6ns | +0.7% |
| skewed | 67.9ns | 27.8ns | +144% |
| nearly_equal | 80.5ns | 66.1ns | +21.8% |

**Why**: Without the initial mod, skewed inputs (e.g., a=2^63, b=17) require ~45+ binary iterations to reduce the large operand, while one mod operation handles it in O(1). The LUT only helps at the end of computation when operands are small — it cannot address the iteration count problem for initially-skewed inputs.

**Lesson**: The initial modular reduction is the single most impactful optimization for real-world inputs, which are often skewed. The LUT is a secondary optimization that provides diminishing returns.

## Summary Table

| Approach | Result | Reason for Failure | Key Lesson |
|----------|--------|--------------------|-----------|
| Divstep (BY2019) | 3.6x slower | 127 fixed iterations vs ~35 variable | Constant-time is for security, not speed |
| Fixed-iteration branchless | 2.8-3.2x slower + incorrect | Wasted iterations + correctness gap | Loop-exit branch is cheap (well-predicted) |
| 2x unrolled loop | No improvement | Register pressure, no ILP | Unrolling serial chains adds overhead |
| TZCNT-before-ABS reorder | No improvement | OoO engine already schedules optimally | Microarch-dependent; may help in-order cores |
| SIMD batch GCD | Not implemented | No SIMD TZCNT, lane divergence | Viable only for bulk throughput workloads |
| LUT without mod | 87.2ns (decent) | Missing initial reduction for skewed inputs | Initial mod is the biggest single win |
