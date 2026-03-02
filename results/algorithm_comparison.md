# Algorithm Comparison

## Performance at bound=5000

| Method | Euler Bricks | Time (s) | Candidates/s | Speedup vs BF |
|--------|-------------|----------|-------------|---------------|
| brute_force | 69 | 16.11 | 957,935 | 1.0x |
| modular_sieve | 69 | 3.65 | 19 | 4.4x |
| novel_search | 24 | 0.02 | 569,528 | 1000.7x |

## Scaling Exponents

| Method | Exponent (runtime ~ n^k) |
|--------|-------------------------|
| brute_force | 2.09 |
| modular_sieve | 2.01 |
| novel_search | 1.30 |

## Estimated Search Reach

| Method | 1 hour | 1 day | 1 week |
|--------|--------|-------|--------|
| brute_force | 7e+04 | 3e+05 | 8e+05 |
| modular_sieve | 2e+05 | 8e+05 | 2e+06 |
| novel_search | 7e+07 | 8e+08 | 3e+09 |

## Comparison with Published Results

- Butler (2004): searched odd edges up to 3e12
- Matson (2015): searched odd edges up to 2.5e13
- Rathbun (2020): min edge up to 2.325e10
- Our best (modular sieve): can reach ~50K edges in 1 hour
- De Grey-Gibbs-Helm (2024): much more efficient via elliptic curve methods