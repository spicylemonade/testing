# Tensor Network Contraction for Precise gamma_2 Estimation

## Topic Context

Tensor network methods from quantum physics provide powerful tools for computing partition
functions and expected values of 2D lattice models. The LCS DP naturally defines such a model.

### Transfer Matrix Formulation
The LCS DP on an n x n grid can be contracted row-by-row. Each row defines a transfer matrix
of dimension 2^n (the anti-diagonal state). The product of n random transfer matrices gives
the LCS value. The expected value of this product can be computed using MPS techniques.

### Why This Could Work
- The anti-diagonal state has dimension 2^n but is highly structured (monotone)
- MPS with bond dimension chi << 2^n can capture this structure
- For each random string pair, contraction takes O(n * chi^3) time
- Averaging over M pairs: O(M * n * chi^3) total
- For M=1000, n=500, chi=64: feasible in hours on a single machine

## Implementation Backlog

1. [ ] Formulate LCS DP as tensor network (specify local tensors)
2. [ ] Implement transfer matrix for binary LCS
3. [ ] Implement MPS contraction with truncation at bond dimension chi
4. [ ] Benchmark: compare MPS result with exact LCS for n=20
5. [ ] Scale up: n=50, 100, 200, 500 with chi=32, 64, 128
6. [ ] Average over 1000+ random pairs
7. [ ] Apply Bundschuh's finite-size correction formula
8. [ ] Report gamma_2 estimate with error bars
