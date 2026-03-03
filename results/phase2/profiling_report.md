# Profiling Report: GCD Baseline Performance

## Benchmark Environment
- CPU: Cloud VM (likely AMD EPYC or Intel Xeon)
- Compiler: GCC 12.2.0
- Flags: -O3 -march=native -std=c++20
- Method: 100K pairs × 10 iterations per configuration

## Summary Table: 64-bit Algorithms

| Algorithm | Uniform (ns) | Skewed (ns) | Nearly-Equal (ns) | Fibonacci (ns) | Coprime (ns) |
|-----------|-------------|------------|-------------------|---------------|-------------|
| euclid | **175.6** | **56.4** | 48.3 | **242.2** | **26.6** |
| stein_classic | **99.1** | 78.4 | 78.0 | 62.7 | 76.5 |
| binary_ctz | 193.2 | 85.4 | 64.5 | 53.8 | 50.9 |
| binary_opt | 179.3 | 78.8 | **61.6** | 57.7 | 50.2 |

### Key Observations (64-bit):

1. **stein_classic wins uniform random** at 99ns — faster than both CTZ-optimized variants (179-193ns). This is unexpected and suggests the compiler is generating good branch prediction for this workload, or the branchy version has fewer instructions per iteration despite mispredictions.

2. **euclid wins coprime** at 26.6ns — because coprime numbers converge in 1-2 divisions. The `idiv` is expensive per iteration but coprime pairs have very few iterations.

3. **euclid wins skewed** at 56.4ns — when one operand is much smaller, the division-based approach reduces the large operand rapidly in one step.

4. **binary_opt wins nearly-equal** at 61.6ns — for nearly-equal operands, binary GCD's subtraction is efficient and TZCNT optimization helps.

5. **binary_ctz/binary_opt are SLOWER than stein_classic on uniform** — this is the critical finding. The CMOV-based versions have higher instruction count per iteration and the CMOV instructions may not be faster than well-predicted branches in this container environment.

## Summary Table: 128-bit Algorithms

| Algorithm | Uniform (ns) | Skewed (ns) | Nearly-Equal (ns) | Fibonacci (ns) | Coprime (ns) |
|-----------|-------------|------------|-------------------|---------------|-------------|
| euclid | **499.3** | **74.8** | **77.8** | **574.8** | **39.0** |
| stein_classic | **559.0** | 229.1 | 206.9 | 185.8 | 192.7 |
| binary_ctz | 575.2 | 239.1 | 211.7 | 186.8 | 204.7 |
| binary_opt | 618.0 | 251.9 | 226.6 | 185.7 | 212.0 |

### Key Observations (128-bit):
1. **euclid is competitive** even at 128-bit for non-worst-case distributions (skewed, coprime, nearly_equal)
2. **binary variants are all similar** at 128-bit — the overhead of 128-bit CTZ (branch on low/high word) dominates
3. **fibonacci worst case**: euclid at 574.8ns vs binary at ~186ns — binary GCD clearly wins for worst-case inputs

## The Target to Beat

For our novel algorithm, we must beat the BEST baseline for each configuration:

| Bit-width | Distribution | Best Baseline | Latency | Target (<90%) |
|-----------|-------------|---------------|---------|---------------|
| 64 | uniform | stein_classic | 99.1ns | <89ns |
| 64 | fibonacci | binary_ctz | 53.8ns | <48ns |
| 128 | uniform | euclid | 499.3ns | <449ns |
| 128 | fibonacci | binary_opt | 185.7ns | <167ns |

## Inner Loop Assembly Analysis (from Phase 1)

The binary_opt inner loop on this machine:
```nasm
loop:
    shrx   rdi, rdi, rcx     ; [1c] shift by previous ctz
    mov    rdx, rax           ; [0c] register move
    sub    rdx, rdi           ; [1c] diff = b - a
    tzcnt  rcx, rdx           ; [3c] ctz(diff) -- parallel with abs
    cmp    rax, rdi           ; [1c]
    cmova  rax, rdi           ; [1c] b = min(a,b)
    mov    rdi, rdx           ; [0c]
    neg    rdi                ; [1c]
    cmovs  rdi, rdx           ; [1c] a = abs(diff)
    test   rdx, rdx           ; [1c]
    jne    loop               ; [1c]
```

Critical path: 5 cycles (SUB → TZCNT → SHRX on the dependency chain)

## Note on Environment Limitations
- No `perf stat` available (container lacks CAP_SYS_ADMIN for perf_event_open)
- No `llvm-mca` available (LLVM not installed, no root for package install)
- Branch misprediction data estimated from assembly structure and theoretical analysis
- IPC estimated from instruction count / critical path analysis
