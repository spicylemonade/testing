# Memoized 3^f Lookup Table

## Topic Context

The key identity T^k(n_0 + a*2^k) = T^k(n_0) + 3^f * a allows precomputing k Collatz steps into a single table lookup. This is the oldest and most widely-used optimization for Collatz computation.

The tradeoff is between table size (2^k entries) and cache efficiency. On CPUs with large L1 caches, k=16 (1MB table) is optimal. On GPUs, random memory access patterns make LUTs counterproductive; instead, Barina's run-length approach (alternating batches of odd and even steps) achieves better throughput.

## Cross-Domain Bridges

- **Chess engines**: Transposition tables cache evaluated positions for O(1) retrieval
- **Cryptanalysis**: Rainbow tables precompute hash chains for fast reversal
- **Dynamic programming**: Classic memoization of overlapping subproblems

## Implementation Backlog

- [ ] Implement LUT for k=16 on CPU (Rust, 128-bit integers)
- [ ] Benchmark k=8,12,16,20 measuring L1/L2 cache hit rates
- [ ] Implement Barina's Algorithm 2 (run-length) for GPU
- [ ] Compare LUT vs run-length throughput on same GPU
- [ ] Test compressed LUT (store only odd entries, halving table size)
- [ ] Profile memory bandwidth vs compute for each approach
