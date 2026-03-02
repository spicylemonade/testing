# Computational Survey: Collatz Implementations and Tools

## 1. High-Performance Verification Projects

### 1.1 xbarin02/collatz (David Barina)
- **URL**: https://github.com/xbarin02/collatz
- **Language**: C with CUDA GPU kernels
- **Capability**: Distributed convergence verification using GPU clusters
- **Performance**: One work unit takes ~5 seconds on modern GPUs; achieved 1335× speedup over initial CPU
- **Record**: Verified all n up to 2^71 (≈ 2.36 × 10^21)
- **Limitations**: Verification-only (convergence to 1), does not compute trajectory features. Not designed for analysis beyond yes/no convergence testing.

### 1.2 emreyolcu/rewriting-collatz
- **URL**: https://github.com/emreyolcu/rewriting-collatz
- **Language**: Various (SAT solvers, term rewriting)
- **Capability**: Automated approach using string rewriting systems and matrix interpretations (arctic, tropical, natural). Encodes termination proofs as SAT instances.
- **Performance**: Can handle large classes of numbers simultaneously
- **Limitations**: Focused on proving termination classes rather than trajectory analysis

### 1.3 Jaylouisw/ProjectCollatz
- **URL**: https://github.com/jaylouisw/projectcollatz
- **Language**: Python/JavaScript
- **Capability**: Distributed verification using IPFS peer-to-peer coordination with GPU acceleration and cryptographic result signing
- **Performance**: Moderate (network coordination overhead)
- **Limitations**: Distributed coordination overhead, less efficient than Barina's focused GPU approach

### 1.4 Collatz-Astana-Divergence
- **URL**: https://github.com/kirieshka2012/Collatz-Astana-Divergence
- **Language**: Python
- **Capability**: Divergence analysis and Lyapunov exponent computation for Collatz trajectories
- **Performance**: Research-grade Python implementation
- **Limitations**: Not optimized for scale; useful for exploratory analysis

### 1.5 GitHub Topics: collatz-conjecture
- **URL**: https://github.com/topics/collatz-conjecture
- **Count**: Hundreds of repositories spanning C, Python, Rust, Julia, Haskell
- **Typical capabilities**: Basic trajectory computation, visualization, stopping time histograms
- **Limitations**: Most are educational/hobby projects, not research-grade

## 2. Academic Implementations

### 2.1 Barina's Verification Algorithm (2025)
- Algorithm achieving ~28% efficiency improvement over prior state-of-the-art
- Leverages structural patterns in the Collatz tree
- Does not require memoization
- Published in arXiv:2501.04032

### 2.2 Elsenhans (2025) - Billion-Digit Verification
- Algorithm for verifying convergence of random numbers with billions of digits
- Uses bitwise operations and carries to avoid storing full numbers
- Novel approach for testing convergence at extreme scales

## 3. Analysis of What Has Been Done vs. What Remains

### 3.1 Well-Explored Computationally
- ✅ Convergence verification (up to 2^71)
- ✅ Cycle detection (no non-trivial cycles with length < ~10^10)
- ✅ Stopping time distributions for n up to ~10^8
- ✅ Benford's law verification along trajectories
- ✅ Mean stopping time growth rate fitting
- ✅ Odd/even ratio convergence verification
- ✅ Record trajectory heights and delay records
- ✅ Machine learning prediction of long Collatz steps

### 3.2 Partially Explored
- 🟡 Residue class structure of stopping times (some results, not systematic)
- 🟡 Generalized Collatz maps (individual cases studied, no comprehensive phase diagram)
- 🟡 Binary representation analysis (some papers, limited scale)

### 3.3 Unexplored Computationally
- ❌ Persistent homology / TDA of trajectory point clouds
- ❌ Random matrix statistics of predecessor graph eigenvalues
- ❌ Mutual information decay between initial conditions and trajectory
- ❌ Systematic modular resonance scan (m = 2..500)
- ❌ Forbidden k-gram catalog for parity sequences (k ≥ 6)
- ❌ Lyapunov exponent distribution from transfer matrix products
- ❌ Phase diagram with fractal boundary characterization for (a,b) family
- ❌ Spectral gap scaling laws for Collatz predecessor graph

## 4. Tool Gaps

No existing open-source tool provides:
1. A unified framework for computing Collatz trajectories + extracting features + statistical analysis
2. Graph construction and spectral analysis of the Collatz predecessor graph
3. Information-theoretic analysis pipeline (mutual information, conditional entropy)
4. Publication-quality visualization toolkit for Collatz dynamics

These gaps justify building our own modular Python toolkit as the foundation for novel research.
