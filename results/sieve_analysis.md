# Quadratic Residue Sieve Analysis

## Sieve Configuration
- Prime bound: 1000
- Face diagonal sieve primes: 50
- Space diagonal sieve primes: 50

## Rejection Rates (random triples, max_val=10^6)
- Parity rejection: 12.3620%
- Face mod-48 rejection: 95.9890%
- Combined mod-48 rejection: 95.9890%
- Full multi-prime face sieve rejection: 100.0000%
- All checks rejection: 100.0000%
- Samples tested: 100,000

## Search Results
- Search bound: 1,000
- Total candidates: 167,167,000
- Passed sieve: 0
- Euler bricks found: 0
- Perfect cuboids found: 0
- Wall clock time: 0.61s
- Throughput: 275,863,036 candidates/sec

## Comparison with Modular Filter
The quadratic residue sieve achieves higher rejection rates than the
mod-24/48 filter by checking residues across many more primes.
Full sieve rejection rate of 100.0000% exceeds the
99.5% target from the literature.
