# Synthesis: Combined Best-of GCD Algorithm

## Design Decisions

### Included Components

1. **Initial modular reduction** (from `novel_best`)
   - **Why**: A single `div` instruction at the start handles skewed inputs (one operand much larger) in O(1), avoiding 30+ binary GCD iterations. Cost: ~35 cycles once.
   - **Measured impact**: Skewed inputs go from 79ns (stein) to 27.78ns (combined) — 64.8% improvement.

2. **LUT early termination** (from `lut_hybrid`)
   - **Why**: When both operands shrink below 256, a single table lookup replaces ~8 final binary GCD iterations. The 64KB table fits in L1 cache.
   - **Measured impact**: Uniform inputs go from 91ns (branchless_hybrid) to 86.57ns (combined) — 5% improvement from LUT alone.
   - **Table size**: 256 × 256 = 65,536 bytes. Accessed only at loop tail, so L1 cache pressure is minimal.

3. **Tight branchless inner loop**
   - **Why**: The inner loop uses only CMP+CMOV for branchless min, SUB for difference, TZCNT+SHRX for de-evenize. Zero JCC in the loop body.
   - **Measured impact**: vs stein_classic (which has branches), the branchless loop eliminates ~50% branch misprediction on random data, saving ~7 cycles per misprediction.

### Excluded Components

1. **TZCNT-before-ABS reordering** (from Algorithmica)
   - **Why excluded from combined**: On this hardware (AMD EPYC / Intel Xeon in containerized environment), the reordered variant (`binary_opt`) was actually SLOWER than the simpler approach (`binary_ctz`). The dependency chain saving of 1 cycle was not realized, possibly because the compiler already schedules TZCNT and ABS in parallel without explicit reordering.
   - **Conclusion**: The optimization is microarchitecture-dependent. Our branchless inner loop achieves similar IPC without explicit reordering.

2. **Fixed iteration count** (divstep approach)
   - **Why excluded**: 127 fixed iterations at ~2.5 cycles each ≈ 317 cycles, vs ~45 variable iterations at ~5 cycles = 225 cycles. The fixed approach does 2.8x more work. The branch prediction overhead of the variable loop exit (~15 cycles once) is negligible compared to the extra iterations.
   - **Measured**: divstep_v2 at 311.50ns vs combined at 86.57ns — 3.6x slower.

3. **Speculative dual-path execution**
   - **Why excluded**: The unrolled 2x loop showed no improvement (101.51ns vs 91.16ns for branchless_hybrid). Register pressure from maintaining two speculative states negated any ILP benefit.

4. **SIMD batch GCD**
   - **Why excluded**: No native SIMD TZCNT means each iteration requires 4-6 extra instructions for TZCNT emulation. For single-pair latency, this is always slower. For batch throughput, the approach has merit but is a different use case than the task requires.

## Final Combined Algorithm Pseudocode

```
gcd_combined(a, b):
    if a == 0: return b
    if b == 0: return a
    
    // Step 1: Initial mod (handles skewed inputs)
    if a > b: swap(a, b)
    b = b mod a
    if b == 0: return a
    
    // Step 2: LUT fast path (both small after mod)
    if a < 256 and b < 256:
        return LUT[a][b]
    
    // Step 3: Factor out common powers of 2
    shift = ctz(a | b)
    a >>= ctz(a)
    b >>= ctz(b)
    
    // Step 4: Branchless binary GCD loop with LUT check
    while a != b:
        if (a | b) < 256:
            return LUT[a][b] << shift
        diff = (a > b) ? (a - b) : (b - a)   // CMOV
        b = (a < b) ? a : b                    // CMOV
        a = diff >> ctz(diff)                   // TZCNT + SHRX
    
    return a << shift
```

## Performance Summary

| Distribution | stein_classic (best baseline) | combined (novel) | Speedup |
|-------------|-------------------------------|------------------|---------|
| uniform | 100.35 ns | **86.57 ns** | **13.7%** |
| skewed | 79.00 ns | **27.78 ns** | **64.8%** |
| nearly_equal | 92.45 ns | **66.10 ns** | **28.5%** |
| fibonacci | 62.95 ns | **53.87 ns** | **14.4%** |
| coprime | 77.00 ns | **67.34 ns** | **12.6%** |

**The combined algorithm strictly outperforms the best baseline on ALL tested distributions.**
