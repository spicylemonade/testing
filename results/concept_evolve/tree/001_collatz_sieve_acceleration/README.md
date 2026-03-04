# 001: Collatz Sieve Acceleration

## Overview

The Collatz sieve is the computational backbone of high-performance delay record searches. It exploits the fact that the first k steps of any Collatz trajectory are completely determined by the number's residue class mod 2^k. By precomputing these first k steps for all 2^k residue classes, we can eliminate >99% of candidates before performing any actual iteration.

## Key Insight

A number n = q * 2^k + r has the same first k Collatz steps as the number r. If those k steps cause the trajectory to drop below the starting value, then n cannot be a delay record (assuming all smaller numbers have already been checked). This observation was first used by Leavens & Vermeulen (1992) and later refined by Barina (2020, 2025).

## Current State of the Art

- Roosendaal's distributed project uses a sieve of width 2^32, eliminating 99.2% of numbers
- Barina's GPU implementation verified convergence up to 2^71 using similar techniques
- The sieve can be further enhanced by also checking mod 9 congruences (Roosendaal)

## Implementation Backlog

1. [ ] Implement basic Collatz sieve in Python for width 2^16
2. [ ] Extend to width 2^20 with completeness filtering
3. [ ] Add Shannon entropy ranking of surviving residue classes
4. [ ] Benchmark against brute force for delay records below 10^9
5. [ ] Verify reproduction of known OEIS A284668 terms a(1)-a(10)
6. [ ] Port to Cython/Numba for production-grade performance
7. [ ] Implement 128-bit arithmetic for numbers beyond 10^18
8. [ ] Profile memory usage for sieve widths up to 2^28

## Cross-Domain Connections

- **Coding Theory**: The sieve is a form of error-correcting code over the Collatz channel
- **Statistical Mechanics**: Surviving residue classes are "rare states" in a partition function
- **Parallel Computing**: The sieve is embarrassingly parallel - each residue class is independent
