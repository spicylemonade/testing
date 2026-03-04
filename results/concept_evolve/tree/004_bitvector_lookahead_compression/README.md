# Bitvector Lookahead Compression

## Topic Context

The bitvector lookahead is the second stage of Angeltveit's algorithm, bridging the CPU-side recursive search and the GPU-side iterative verification. It compresses multiple sieve checks (Descent, Path-Merging, OEE, and mod-9) into a single bitwise AND operation.

The key innovation is the reordering of bitvector entries: instead of linear ordering by the last B bits of m, entries are ordered by a*3^f mod 2^B, which ensures that consecutive values of a (the high bits) map to consecutive bitvector positions — enabling coalesced GPU memory access.

## Cross-Domain Bridges

- **Bloom filters**: Compact approximate set membership via bit arrays
- **GPU texture compression**: Reorder data for cache-coherent access patterns
- **Succinct data structures**: Near-optimal bit encoding of combinatorial objects

## Implementation Backlog

- [ ] Precompute dip_B(m) values for B=24 on CPU
- [ ] Implement bitvector reordering using 3^f mod 2^B multiplication
- [ ] Store bitvectors in GPU shared memory / L2 cache
- [ ] Benchmark cache hit rates for B=20..26
- [ ] Test roaring bitmap compression for sparse BV_i (i=0, density ~2%)
- [ ] Profile memory bandwidth bottleneck vs compute bottleneck
