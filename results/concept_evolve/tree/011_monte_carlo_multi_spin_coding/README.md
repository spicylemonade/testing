# Monte Carlo with Multi-Spin Coding

## Topic Context

Estimating γ₂ via Monte Carlo requires computing LCS(a,b) for many random string pairs. The standard DP algorithm takes O(n²) time per pair. For binary strings, multi-spin coding (Bundschuh 2001) achieves a factor-64 speedup by packing 64 independent string pairs into 64-bit machine words and using bitwise operations.

### Multi-Spin Coding Principle
- Represent 64 random binary strings as 64 bits of each position word
- Character matching: bitwise XNOR detects matches for all 64 pairs
- DP update: encode column differences as bit vectors
- Each arithmetic/logic operation processes 64 pairs simultaneously

### Modern Extensions
- **AVX-512**: 512-bit SIMD registers → 512 pairs per instruction
- **GPU**: Thousands of CUDA cores, each processing 64 pairs → millions of pairs concurrently
- **Estimated throughput**: 10^9 LCS(10^4, 10^4) computations per GPU-hour

## Implementation Backlog

1. **Baseline scalar LCS** (Priority: HIGH)
   - Standard O(n²) DP in C
   - Benchmark throughput

2. **64-bit multi-spin coding** (Priority: HIGH)
   - Implement Bundschuh's technique
   - Validate against scalar version
   - Measure 64x speedup

3. **AVX-512 multi-spin** (Priority: MEDIUM)
   - Extend to 512-bit SIMD
   - Handle carry propagation across SIMD lanes
   - Target 8x speedup over 64-bit

4. **CUDA multi-spin** (Priority: MEDIUM)
   - Port to GPU
   - Optimize memory access patterns (coalesced reads)
   - Target 1000x speedup over scalar

5. **Production γ₂ estimation run** (Priority: HIGH)
   - Use best implementation for massive data generation
   - String lengths n = 10^3 to 10^6
   - 10^6-10^9 samples per length
   - Apply finite-size scaling for final estimate
