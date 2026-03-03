# Literature Survey: Branchless Binary GCD Algorithms

## 1. Core GCD Algorithms

### 1.1 Stein 1967 — Binary GCD Algorithm [stein1967]
- **Key idea**: Replace division with bit-shifts, subtraction, and comparison
- **Rules**: (1) gcd(0,b)=b; (2) gcd(2a,2b)=2·gcd(a,b); (3) gcd(2a,b)=gcd(a,b) if b odd; (4) gcd(a,b)=gcd(|a-b|,min(a,b)) if both odd
- **Complexity**: O(n²) bit operations for n-bit inputs, O(n) iterations
- **Relevance**: Foundation of all binary GCD variants; avoids expensive division

### 1.2 Knuth TAOCP Vol 2, Section 4.5.2 [knuth1997]
- **Key idea**: Comprehensive analysis of GCD algorithms including binary GCD
- **Analysis**: Expected iterations ~0.706n for n-bit random inputs; worst case ~1.44n (Fibonacci-adjacent inputs)
- **Historical note**: Knuth attributes binary GCD to Stein 1967, but notes earlier Chinese origins
- **Relevance**: Theoretical foundation for iteration count bounds and convergence analysis

### 1.3 Bernstein-Yang 2019 — Fast Constant-Time GCD (divstep) [bernsteinyang2019]
- **Key idea**: "Division step" (divstep) transition: single unified rule replacing all branching cases
- **Formula**: divstep(δ,f,g) → (δ',f',g') with conditional swap and halving
- **Properties**: Fixed 2n-1 iterations for n-bit inputs; fully constant-time; no data-dependent branches
- **Performance**: Enables constant-time modular inversion competitive with Fermat's method
- **Applications**: Curve25519, NTRU lattice-based crypto
- **Relevance**: **Critical reference** — the divstep approach is the cleanest branchless GCD formulation

### 1.4 Pornin 2020 — Optimized Binary GCD for Modular Inversion [pornin2020]
- **Key idea**: Practical optimization of extended binary GCD for modular inversion
- **Performance**: 6253 cycles for inversion mod 2^255-19 on Intel Coffee Lake, fully constant-time
- **Technique**: Inner loop processes k-1 bits per iteration using a compressed representation
- **Implementation**: Available at github.com/pornin/bingcd
- **Relevance**: State-of-the-art constant-time binary GCD with detailed cycle analysis

## 2. Practical Implementations

### 2.1 Algorithmica.org Binary GCD [slotin2022]
- **Key idea**: Derive a binary GCD ~2x faster than std::gcd using three optimizations:
  1. Use `__builtin_ctz` (TZCNT instruction) instead of loop-based shift
  2. Factor out initial shared powers of 2 once, not per-iteration
  3. Compute TZCNT on raw difference before absolute value (key insight!)
- **Performance**: 91ns vs 198ns for std::gcd on 32-bit random inputs
- **Assembly**: Inner loop is SUB, CMOVG, NEG, CMOVS, TZCNT, SARX — zero JCC
- **Credit**: Main optimization ideas from Daniel Lemire and Ralph Corderoy (2013)
- **Relevance**: **Primary baseline** — this is the algorithm to beat

### 2.2 Lemire 2013 — Fastest Way to Compute GCD [lemire2013]
- **Key idea**: Binary GCD with `__builtin_ctz` is 55% faster than Euclidean on i7
- **Insight**: The Wikipedia binary GCD code was inefficient; proper CTZ usage critical
- **Performance**: 39M GCD/sec vs 25M GCD/sec (Euclidean) for [0,2000) inputs
- **Relevance**: First popular demonstration of CTZ-optimized binary GCD

### 2.3 Lemire 2024 — Extended Euclidean Algorithm and Speed [lemire2024]
- **Key idea**: Hybrid approach with initial division step, plus Bonzini's no-swap variant
- **Bonzini variant**: Eliminates conditional swap with different subtraction logic
- **Relevance**: Shows modern C++20 `std::countr_zero` makes the pattern portable

### 2.4 Linux Kernel lib/gcd.c [zeng2016]
- **Key idea**: Zhaoxiu Zeng replaced Euclidean GCD with binary GCD in Linux kernel
- **Implementation**: Uses `__ffs` (find-first-set) for trailing zero count
- **Two paths**: Binary GCD when __ffs is efficient; odd-even algorithm otherwise
- **Relevance**: Production binary GCD code; prioritizes portability over microarch tricks

### 2.5 libc++ D145982 — Binary GCD for std::gcd [libcxxD145982]
- **Key idea**: Replace Euclidean std::gcd with binary version in LLVM libc++
- **Performance**: ~2x faster; inspired by Algorithmica.org
- **Status**: Merged into LLVM
- **Relevance**: Demonstrates industry adoption of binary GCD as the standard

### 2.6 libstdc++ Optimize std::gcd [libstdcxxgcd2024]
- **Key idea**: Rearrange subtractions and branches to encourage CMOV generation
- **Performance**: 20-60% improvement in GCC's libstdc++
- **Insight**: Compiler needs specific patterns to emit CMOV instead of branches
- **Relevance**: Shows importance of source-level patterns for branchless codegen

## 3. Constant-Time and Cryptographic Implementations

### 3.1 Bos 2014 — Constant Time Modular Inversion [bos2014]
- **Key idea**: Modified Kaliski algorithm for constant-time Montgomery inverse
- **Platform**: ARM 32-bit
- **Relevance**: Alternative constant-time approach for modular inversion

### 3.2 Sreedhar-Horowitz-Torng 2022 — Hardware XGCD [sreedhar2022]
- **Key idea**: ASIC design for extended GCD using Stein's subtraction-based algorithm
- **Performance**: 1024-bit XGCD in 294ns; constant-time 255-bit in 85ns (31x faster than software)
- **Key finding**: Stein-based (subtraction) algorithms lead to significantly faster hardware than Euclid-based (division)
- **Relevance**: Hardware perspective validates binary GCD's superiority; informs SIMD approach

### 3.3 Barenghi-Pelosi 2020 — Constant-Time Polynomial Inversion [barenghi2020]
- **Key idea**: Comprehensive analysis of constant-time binary polynomial inversion
- **Relevance**: Techniques for constant-time implementation applicable to integer GCD

## 4. Microarchitectural References

### 4.1 Agner Fog Instruction Tables [fog2024]
- **Key data**: TZCNT latency: 3 cycles (Skylake/Alder Lake), 1 cycle (Zen 3/4); CMOV: 1 cycle; SARX (BMI2): 1 cycle
- **Relevance**: Essential for critical path analysis

### 4.2 Intel Optimization Manual [intel2024]
- **Key data**: CMOV fusion, port scheduling, BMI2 instruction details
- **Relevance**: Authoritative source for cycle-level optimization

### 4.3 uops.info [abel2022]
- **Key data**: Empirically measured instruction latencies, throughputs, and port mappings
- **Relevance**: More accurate than vendor documentation for actual microarchitectural behavior

## 5. Related Branchless Techniques

### 5.1 Skarupke 2023 — Branchless Binary Search [skarupke2023]
- **Key idea**: Shar's algorithm for branchless binary search; >2x faster than std::lower_bound in GCC
- **Relevance**: Demonstrates CMOV-based branchless patterns achieving dramatic speedups

### 5.2 Shallit-Sorenson 1993 — Binary Jacobi Symbol [shallit1993]
- **Key idea**: Binary algorithm for Jacobi symbol using similar shift/subtract patterns
- **Relevance**: Extended binary GCD techniques

## 6. Summary of Key Performance Numbers

| Algorithm | Platform | Bit-width | Metric | Value | Source |
|-----------|----------|-----------|--------|-------|--------|
| std::gcd (Euclidean) | x86-64 | 32 | Latency | 198ns | [slotin2022] |
| Binary GCD (CTZ+CMOV) | x86-64 | 32 | Latency | 91ns | [slotin2022] |
| Binary GCD (Lemire) | i7 | 32 | Throughput | 39M ops/s | [lemire2013] |
| Euclidean GCD | i7 | 32 | Throughput | 25M ops/s | [lemire2013] |
| Pornin binary GCD | Coffee Lake | 255 | Cycles | 6253 | [pornin2020] |
| ASIC XGCD (Sreedhar) | 16nm ASIC | 255 | Latency | 85ns | [sreedhar2022] |
| ASIC XGCD (Sreedhar) | 16nm ASIC | 1024 | Latency | 294ns | [sreedhar2022] |

## 7. Key Insights for Novel Algorithm Design

1. **TZCNT-before-ABS**: The Algorithmica optimization of computing TZCNT on the raw difference before ABS is the single most important optimization (saves 1-2 cycles per iteration)
2. **CMOV for swap/abs**: Modern compilers can emit CMOV for conditional swap and absolute value, but need specific source patterns
3. **Fixed iteration count**: Bernstein-Yang divstep eliminates loop-termination branch at cost of 2x iterations
4. **Hybrid approaches**: Initial modular reduction + binary GCD core can help for skewed inputs
5. **No SIMD TZCNT**: This is the main obstacle for SIMD batch GCD; must emulate via bit manipulation
6. **Compiler sensitivity**: The exact C source pattern matters enormously for generated assembly (libstdc++ patch shows 20-60% difference from rearranging the same operations)
