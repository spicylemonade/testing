# NEWTONS_THIRD_EXPLOIT

Exploit F_ij = -F_ji to halve the O(N^2) force computation. The simplest optimization: compute each pair once, apply equal-and-opposite forces. Zero added complexity, 2x speedup.

## Mathematical Formalization

Standard: for i in 0..N, for j in 0..N, compute F_ij. Cost: N^2.  Exploited: for i in 0..N, for j in i+1..N, compute F_ij, set F_ji = -F_ij. Cost: N*(N-1)/2.  Speedup: exactly 2x minus diagonal.

## Analogical Connections

- Newton's third <-> symmetric matrix storage (only store upper triangle)
- Pair symmetry <-> undirected graph edge list (each edge stored once, used twice)
- Half-iteration trick <-> FFT butterfly (exploit symmetry to halve computation)

## Implementation Hypothesis

Change inner loop from `for j in range(N)` to `for j in range(i+1, N)`. Add force to both i and j (with opposite signs). One-line change, 2x speedup.

## Experiment Seed

Benchmark N=1000 brute-force with and without Newton's third law optimization. Verify exactly 2x speedup and identical force results (bitwise).
