# Microarchitectural Bottleneck Analysis of GCD Implementations

## 1. Annotated Assembly: Euclidean GCD (std::gcd equivalent)

```nasm
; gcd_euclid(uint64_t a, uint64_t b)
; a = rdi -> rax, b = rsi -> rdx
loop:
    mov    rcx, rdx          ; t = b               [1 cycle, port 0156]
    xor    edx, edx          ; clear upper rdx      [0 cycles, eliminated]
    div    rcx               ; rax=a/b, rdx=a%b    [35-90 cycles, port 0*]
    mov    rax, rcx          ; a = t (old b)        [1 cycle, port 0156]
    test   rdx, rdx          ; b == 0?              [1 cycle, port 0156]
    jne    loop              ; continue if b != 0   [1 cycle, port 06]
```

**Critical path per iteration**: 35-90 cycles (dominated entirely by `div`)
- Intel Skylake: `div r64` latency = 35-88 cycles (data-dependent)
- AMD Zen 3: `div r64` latency = 8-41 cycles
- The `div` instruction is a single micro-op but has extreme variable latency
- Branch prediction: Loop back is well-predicted (~97% taken), but the JNE after TEST adds 1 cycle on mispredict at termination

**Bottleneck**: Integer division. This is fundamentally a serial loop with one `div` on the critical path.

## 2. Annotated Assembly: Binary GCD v1 (TZCNT after ABS)

```nasm
; gcd_binary_cmov_v1 inner loop
; a = rdi (odd), b = rax (odd)
loop:
    mov    rdx, rdi          ; diff = a              [1c, p0156]
    sub    rdx, rax          ; diff = a - b          [1c, p0156] *CHAIN START*
    cmp    rax, rdi          ;                       [1c, p0156]
    cmova  rax, rdi          ; b = min(a,b)          [1c, p06]
    mov    rdi, rdx          ; prepare abs            [1c, p0156]
    neg    rdi               ; -diff                  [1c, p0156]
    cmovs  rdi, rdx          ; a = abs(diff)          [1c, p06] 
    tzcnt  rdx, rdi          ; az = ctz(abs_diff)     [3c, p1]  *AFTER ABS*
    shrx   rdi, rdi, rdx     ; a >>= az               [1c, p06]
    test   rdi, rdi          ; a != 0?                [1c, p0156]
    jne    loop              ;                        [1c, p06]
```

**Critical path (loop-carried dependency chain)**:
```
SUB rdx,rax  [1c] -> MOV rdi,rdx [1c] -> NEG rdi [1c] -> CMOVS rdi,rdx [1c]
                                                              |
                                                     TZCNT rdx,rdi [3c]
                                                              |
                                                     SHRX rdi,rdi,rdx [1c]
```

Total critical path: SUB(1) + MOV(1) + NEG(1) + CMOVS(1) + TZCNT(3) + SHRX(1) = **8 cycles** per iteration

- MOV instructions on the critical path are NOT eliminated (register renaming handles them at 0c on some uarches, but they are on the dependency chain)
- The CMP+CMOVA for min(a,b) is OFF the critical path (computes `b` in parallel)
- The JNE at the end adds 0 cycles when correctly predicted (taken), ~15-20 cycle penalty on final mispredict

## 3. Annotated Assembly: Binary GCD v2 (TZCNT before ABS — Algorithmica optimized)

```nasm
; gcd_binary_cmov_v2 inner loop
; rdi carries a (shifted from previous iteration), rax carries b, rcx carries az
loop:
    shrx   rdi, rdi, rcx     ; a >>= az (from prev)  [1c, p06]
    mov    rdx, rax          ; diff_base = b           [0c, eliminated*]
    sub    rdx, rdi          ; diff = b - a            [1c, p0156] *CHAIN START*
    tzcnt  rcx, rdx          ; az = ctz(diff)          [3c, p1]   *PARALLEL WITH ABS*
    cmp    rax, rdi          ;                         [1c, p0156]
    cmova  rax, rdi          ; b = min(a,b)            [1c, p06]
    mov    rdi, rdx          ; prepare abs              [0c, eliminated*]
    neg    rdi               ; -diff                    [1c, p0156]
    cmovs  rdi, rdx          ; a = abs(diff)            [1c, p06]
    test   rdx, rdx          ; diff != 0?              [1c, p0156]
    jne    loop              ;                          [1c, p06]
```

**Critical path (loop-carried dependency chain)**:
```
SUB rdx (=b-a) [1c]
    |          \
    |           TZCNT rcx,rdx [3c]   <-- TZCNT starts immediately from SUB result
    |                    |
    |              (next iter: SHRX rdi,rdi,rcx [1c])
    |
NEG rdi [1c] -> CMOVS rdi,rdx [1c]
    |
(next iter: SHRX rdi,rdi,rcx [1c])
```

The KEY optimization: TZCNT reads `diff` (the raw signed difference) and ABS reads `diff` independently. They execute in PARALLEL.

**True critical path**: Two chains must complete before next iteration:
- Chain A: SUB(1) → TZCNT(3) → SHRX(1) = **5 cycles**
- Chain B: SUB(1) → NEG(1) → CMOVS(1) → (next SHRX needs this for rdi) = **3 cycles + SHRX(1) = 4 cycles**

The critical path is MAX(Chain A, Chain B) = **5 cycles** per iteration.

Wait — more precisely, the next iteration's SHRX needs BOTH:
- rdi (from CMOVS, available at cycle 3 from SUB)  
- rcx (from TZCNT, available at cycle 4 from SUB)

So SHRX starts at cycle 4, completes at cycle 5. The SUB in the next iteration needs the SHRX result.

**Total loop-carried critical path: 5 cycles per iteration on Skylake.**

## 4. Data Dependency Graph Summary

### Skylake / Alder Lake (P-core)

| Instruction | Latency | Ports | Notes |
|-------------|---------|-------|-------|
| SUB r64,r64 | 1 | p0156 | |
| TZCNT r64,r64 | 3 | p1 | BMI1; 3c latency on Skylake |
| SHRX r64,r64,r64 | 1 | p06 | BMI2 |
| CMOV r64,r64 | 1 | p06 | |
| NEG r64 | 1 | p0156 | |
| MOV r64,r64 | 0-1 | eliminated or p0156 | Register renaming may eliminate |

| Algorithm | Critical Path | Iterations (avg, 64-bit) | Total Cycles (est.) |
|-----------|---------------|--------------------------|---------------------|
| Euclidean (div) | 35-88c | ~10 | 350-880c |
| Binary v1 (TZCNT after ABS) | 8c | ~45 | ~360c |
| Binary v2 (TZCNT before ABS) | 5c | ~45 | ~225c |

### AMD Zen 3/4

| Instruction | Latency | Notes |
|-------------|---------|-------|
| TZCNT r64,r64 | 2 | Faster than Intel! |
| CMOV r64,r64 | 1 | |
| SHRX r64,r64,r64 | 1 | |

| Algorithm | Critical Path (Zen 3) | Total Cycles (est.) |
|-----------|-----------------------|---------------------|
| Binary v2 (TZCNT before ABS) | 4c | ~180c |

**AMD Zen 3/4 has 2-cycle TZCNT, making the critical path 4 cycles vs. Intel's 5 cycles.**

## 5. Branch Misprediction Analysis

### Stein's Original Formulation (Branchy)
```
if (a > b) swap(a, b);  // conditional branch
b -= a;
b >>= ctz(b);           // loop back if b != 0
```

- The `if (a > b)` branch is essentially random for random inputs → **~50% misprediction rate**
- At ~15-20 cycle mispredict penalty on Skylake, this costs 7.5-10 cycles per iteration
- Combined with instruction overhead: ~15-20 cycles per iteration

### CMOV-Based Version (Branchless inner loop)
```
diff = b - a;
b = min(a, b);      // CMOV, no branch
a = abs(diff);       // NEG + CMOV, no branch
az = ctz(diff);      // no branch
// JNE loop           // only branch: loop back (99%+ predicted taken)
```

- **Zero mispredictions in steady state** (CMOV replaces all data-dependent branches)
- The only branch is the loop-back JNE, which is taken on every iteration except the last
- For ~45 iterations, that's 44 correct predictions + 1 mispredict at exit = **~0.3 mispredictions per iteration**
- Total branch mispredict cost: ~15-20 cycles once (at loop exit) ≈ negligible

### Comparison

| Variant | Mispredictions/iter | Mispredict Cost/iter | Total Overhead (45 iters) |
|---------|--------------------|--------------------|--------------------------|
| Stein's (branchy) | ~0.50 | ~7.5-10c | 340-450c |
| CMOV-based | ~0.02 | ~0.3-0.4c | 15-20c (one-time) |

The CMOV version eliminates ~99% of branch misprediction overhead.

## 6. Specific Bottleneck Identification

**The bottleneck is the loop-carried dependency chain: SUB → TZCNT → SHRX**

This chain is 5 cycles on Intel Skylake (3-cycle TZCNT) and 4 cycles on AMD Zen 3 (2-cycle TZCNT).

The chain cannot be broken by reordering alone — SHRX needs the TZCNT result, and TZCNT needs the SUB result, and the next iteration's SUB needs the SHRX result.

### Possible attacks on the bottleneck:
1. **Speculative execution**: Guess TZCNT result (most likely = 1) and compute the next SUB speculatively
2. **Lookup table**: When operands < 256, skip remaining iterations entirely
3. **Fixed iteration count** (Bernstein-Yang): Eliminate the loop-back branch entirely, making the total execution perfectly predictable
4. **SIMD batch**: Process multiple independent pairs to hide single-pair latency behind throughput

## 7. Instruction-Level Parallelism in the Inner Loop

The v2 inner loop has 10 instructions per iteration. On a 4-wide superscalar like Skylake:
- Theoretical IPC limit: 4.0
- Actual IPC (estimated): ~2.0 (limited by 5-cycle dependency chain with 10 instructions)
- Instructions per iteration: 10
- Cycles per iteration (from dependency analysis): 5
- Effective IPC: 10/5 = 2.0

There is room for the CPU to do other work (memory accesses, prefetching) during the ~50% of unused issue slots. This suggests that a speculative dual-path approach could potentially fill those slots.
