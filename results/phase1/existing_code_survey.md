# Existing Code & Database Survey: Collatz Computation

## 1. GitHub Repositories

### 1.1 hellpig/collatz (★18, MIT License)
- **URL**: https://github.com/hellpig/collatz
- **Language**: C (81%), C++ (11%), CUDA (7.8%), Python (0.2%)
- **Claims**: "World's fastest CPU and GPU codes for experimentally testing the Collatz conjecture"
- **Features**: 128-bit integer support, partially sieveless approach, CUDA and OpenCL GPU support
- **Last active**: May 2024

### 1.2 xbarin02/collatz-sieve (David Barina's official code)
- **URL**: https://github.com/xbarin02/collatz-sieve
- **Language**: C with GPU support
- **Features**: The actual code used for the 2^71 verification record. Implements the sieve-based convergence algorithm from Barina (2021, 2025).
- **Significance**: The state-of-the-art implementation achieving 1335× speedup

### 1.3 rogerdahl/cuda-collatz (★5)
- **URL**: https://github.com/rogerdahl/cuda-collatz
- **Language**: CUDA C
- **Claims**: "The world's fastest Collatz Delay Record calculator?"
- **Focus**: Specifically designed for finding delay records (not just convergence verification)
- **License**: MIT

### 1.4 TSP66/GPU-Collatz-Search (★1)
- **URL**: https://github.com/tsp66/gpu-collatz-search
- **Language**: CUDA
- **Features**: Distributed system for values >2^63, handles 10,000+ digit numbers
- **Last active**: August 2024

### 1.5 perspector/Collatz-Cruncher
- **URL**: https://github.com/perspector/Collatz-Cruncher
- **Features**: Testing billions of numbers to find counterexamples
- **Approach**: Brute-force search with optimizations

### 1.6 SchVinzenz/Collatz-Generator
- **URL**: https://github.com/schvinzenz/collatz-generator
- **Language**: Python with SymPy
- **Features**: Interactive GUI for exploring Collatz sequences, symbolic analysis
- **Last active**: April 2025

## 2. Eric Roosendaal's Delay Record Tables

**Source**: https://www.ericr.nl/wondrous/delrecs.html

### Current Status (as of March 2026):
- Distributed project has completed all blocks up to **35,900** (units of 10^12), meaning all numbers below ~3.59 × 10^16 have been checked for class records
- Records confirmed by exhaustive search through the distributed project
- Records up to 10^6 first published by Leavens and Vermeulen (1992)

### Key Delay Records (confirmed):
| # | N | Delay | Level | Notes |
|---|---|-------|-------|-------|
| 1 | 9 | 19 | | |
| 2 | 97 | 118 | | |
| 10 | 871 | 178 | | |
| 20 | 6171 | 261 | | |
| 30 | 77031 | 350 | | |
| 44 | 837799 | 524 | | |
| 50 | 8400511 | 685 | | |
| 59 | 63728127 | 949 | Level -1, largest single improvement (+205) |
| 70 | 670617279 | 986 | |
| 80 | 9780657630 | 1132 | |

### Notable Observations:
- ~7-8 records per order of magnitude
- Average factor between consecutive records: 1.36
- Record #59 (63,728,127) improved previous by 205 steps — largest gap
- Many records share similar residues, indicating path coalescence

## 3. OEIS Sequences

### A006877 (Delay Record Holders)
- **Title**: "In the 3x+1 problem, these values set new records for number of steps to reach 1"
- **Current terms**: 148 known terms (from Hugo Pfoertner/Eric Roosendaal)
- **First terms**: 1, 2, 3, 6, 7, 9, 18, 25, 27, 54, 73, 97, 129, 171, 231, 313, 327, 649, 703, 871, 1161, 2223, 2463, 2919, 3711, 6171, 10971, 13255, 17647, 23529, 26623, 34239, 35655, 52527, 77031, 106239, 142587, 156159, 216367, 230631, 410011, 511935, 626331, 837799, ...
- **Counting**: Both 3x+1 steps and halving steps counted

### A006884 (Delay Record Values)
- **Title**: "In the 3x+1 problem, record number of steps to reach 1"
- **Corresponds to**: The stopping times of numbers in A006877
- **First terms**: 0, 1, 7, 8, 16, 19, 20, 23, 111, 112, 118, 120, 144, 170, 178, ...

### A006577 (Stopping Times)
- **Title**: "Number of halving and tripling steps to reach 1 in '3x+1' problem"
- **Note**: Both halving and tripling steps counted
- **First terms**: 0, 1, 7, 2, 5, 8, 16, 3, 19, 6, 14, 9, 9, 17, 17, 4, 12, 20, ...

### A284668 (Records per Decade)
- **Title**: "Numbers that have the largest Collatz total stopping time of all numbers below 10^n"
- **Current terms**: 18 known terms (up to 10^18)
- **Values**: 9, 97, 871, 6171, 77031, 837799, 8400511, 63728127, 670617279, 9780657630, 75128138247, 989345275647, 7887663552367, 80867137596217, 942488749153153, 7579309213675935, 93571393692802302, 931386509544713451

## 4. Performance Benchmarks

| Implementation | Platform | Speed | Notes |
|---------------|----------|-------|-------|
| Barina GPU (2025) | Multi-GPU supercomputer | 1335× over CPU baseline | State-of-the-art, 2^71 verification |
| Honda et al. (2017) | GTX TITAN X | 1.31 × 10^12 numbers/sec | 249× over i7-4790 CPU |
| Czarnul (2023) | 16-node GPU cluster | 89-97% parallel efficiency | Multi-node CUDA+OpenMP |
| Dutta (2025) | i7-11850H CPU | 1.3 × 10^9 128-bit numbers/sec | Sieve-based approach |
| Getachew (2025) | CPU | 28% improvement over prior | Structural pattern exploitation |
| Roosendaal's sieve | CPU | >99.2% candidate elimination | 2^32 sieve depth |
| hellpig/collatz | CPU+GPU | Self-claimed fastest | 128-bit, partially sieveless |

## 5. Key Technical Insights for Our Implementation

1. **Sieve depth tradeoff**: Deeper sieve (higher 2^k) eliminates more candidates but requires more memory. Sweet spot seems to be 2^16 to 2^20 for CPU implementations.
2. **Mod 9 filter**: Simple but effective — eliminates 44.4% of candidates.
3. **128-bit arithmetic**: Essential for paths that exceed 2^64 intermediate values.
4. **Path coalescing**: Once trajectories meet a number already visited, they can be terminated early.
5. **Delay records vs convergence**: Different algorithms needed — delay records need full stopping time computation, not just convergence check.
