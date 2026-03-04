# Literature Review: Collatz Conjecture Delay Records & Computational Methods

## 1. Problem Definition

The Collatz conjecture states that for any positive integer n, the sequence defined by:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

always eventually reaches 1. The **total stopping time** (or **delay**) of n is the number of steps required to reach 1. A **delay record** is a number n whose stopping time exceeds that of all numbers less than n.

## 2. Current Computational Verification Status

### 2.1 Convergence Verification
- **Current bound**: All numbers below **2^71** (~2.36 × 10^21) have been verified to converge to 1 (Barina, 2025).
- Previous bounds: 2^68 (Barina, 2021), 5 × 2^60 (Oliveira e Silva, 2008), 87 × 2^60 (~10^20) (yoyo@home, 2017).
- Barina's GPU-accelerated approach achieves 1335× speedup over naive CPU baseline.
- Uses European supercomputers with thousands of parallel GPU workers.
- Found 4 new path records during verification (Barina, 2025).

### 2.2 Delay Record Tables (Roosendaal)
Eric Roosendaal maintains the definitive delay record database at ericr.nl/wondrous/delrecs.html. Key observations:
- ~7-8 delay records per power of 10 (factor ~1.36 between consecutive records on average)
- The distributed computing project has confirmed records up to block 35,900 (as of Dec 2025), where blocks are in units of 10^12 (~3.59 × 10^16)
- Record #59 at N=63,728,127 (delay=949) improved previous record by 205 steps - the largest single-record improvement
- Many delay records share similar "residues" indicating coalescing paths

### 2.3 Known Delay Records per Decade (OEIS A284668)
| Range | Record Holder | Stopping Time |
|-------|--------------|---------------|
| <10^1 | 9 | 19 |
| <10^2 | 97 | 118 |
| <10^3 | 871 | 178 |
| <10^4 | 6171 | 261 |
| <10^5 | 77031 | 350 |
| <10^6 | 837799 | 524 |
| <10^7 | 8400511 | 685 |
| <10^8 | 63728127 | 949 |
| <10^9 | 670617279 | 986 |
| <10^10 | 9780657630 | 1132 |
| <10^11 | 75128138247 | 1228 |
| <10^12 | 989345275647 | 1348 |
| <10^13 | 7887663552367 | 1563 |
| <10^14 | 80867137596217 | 1662 |
| <10^15 | 942488749153153 | 1862 |
| <10^16 | 7579309213675935 | 1958 |
| <10^17 | 93571393692802302 | 2091 |
| <10^18 | 931386509544713451 | 2283 |

## 3. Algorithmic Approaches in Literature

### 3.1 Sieving Methods
The core acceleration technique eliminates candidates that provably have short stopping times based on their residue class modulo 2^k:

- **Roosendaal's sieve (2^32)**: Eliminates >99.2% of candidates. Only 1720 out of every 65536 numbers survive a sieve of depth 2^16 (Roosendaal, 2025).
- **Mod 9 filter**: Numbers congruent to 2, 4, 5, or 8 mod 9 lie on the path of a smaller number (44.4% elimination) (Roosendaal, techpage).
- **Dutta (2025)**: Theoretically proven sieve bitsets of O(2^m) elements; CPU implementation verifies 1.3 × 10^9 128-bit integers per second on i7-11850H.
- **Angeltveit (2026)**: New algorithm where checking all n < 2^(N+1) takes less than twice the time for n < 2^N. Uses mod 9 exclusion plus k-step sieve.

### 3.2 GPU Acceleration
- **Honda et al. (2017)**: GPU implementation on GTX TITAN X verifies 1.31 × 10^12 64-bit numbers/second (249× over CPU).
- **Czarnul (2023)**: Multi-node CUDA+OpenMP framework on 16-node GPU clusters achieving 89-97% parallel efficiency.
- **Barina (2025)**: Combined sieving + GPU acceleration achieving 1335× total speedup.

### 3.3 Algorithmic Innovations
- **Getachew & Assefa (2025)**: Leverage structural patterns in the Collatz tree to minimize redundant operations; 28% improvement over state-of-the-art.
- **Binary tail analysis**: Lowest k bits of n determine first k steps exactly (used in all modern sieve implementations).
- **Path coalescing**: Once two trajectories meet, they merge forever - used to skip numbers on existing paths.

### 3.4 Probabilistic Models
- **Lagarias heuristic**: Expected stopping time ~ C × log(n) where C ≈ log(4/3)/log(2) × (something). The 3/4 shrinkage per odd step gives expected behavior.
- **Tao (2019)**: Proved almost all orbits attain almost bounded values using probabilistic methods on 3-adic cyclic groups. The key insight is the Syracuse iteration's connection to random walks.
- **Sinai (2003)**: Studied uniform distribution properties of the 3x+1 dynamics.
- **Polli et al. (2024)**: Showed Collatz orbits display properties of geometric Brownian motion with short- and mid-range correlations.

### 3.5 Kontorovich-Sinai-Tao Probabilistic Framework
The heuristic model: after k odd steps and m even steps (total k+m steps), the value is approximately:
n × (3/2)^k × (1/2)^m

Since odd/even steps occur with roughly equal probability and 3/2 vs 1/2 determines long-term drift, the expected total stopping time is:
E[stopping_time(n)] ≈ (2 × log(2) / log(4/3)) × log(n) ≈ 6.95 × log₂(n)

Numbers with anomalously high stopping times are those where the random walk deviates significantly from the expected drift.

## 4. OEIS Sequences
- **A006877**: Delay record holders (numbers setting new stopping time records)
- **A006884**: Maximum stopping times (the stopping times of the records)
- **A006577**: Number of steps for n to reach 1
- **A284668**: Numbers with largest stopping time below 10^n

## 5. Open Questions Relevant to This Project
1. Can we find delay records beyond the current confirmed boundary (~3.59 × 10^16)?
2. Can novel sieving or probabilistic guidance find records faster than exhaustive search?
3. Are there structural patterns in delay record trajectories that can predict new records?
4. Can trajectory fingerprinting identify "delay-prone" binary patterns?

## 6. Papers Cited (15+ sources)
1. Lagarias (1985) - "The 3x+1 problem and its generalizations" - foundational survey
2. Lagarias (2010) - "The Ultimate Challenge: The 3x+1 Problem" - book/AMS
3. Lagarias (2021) - "The 3x+1 Problem: An Overview" - arXiv:2111.02635
4. Wirsching (1998) - "The Dynamical System Generated by the 3n+1 Function" - Springer LNM
5. Tao (2019) - "Almost all orbits of the Collatz map attain almost bounded values" - Forum of Math Pi
6. Oliveira e Silva (1999) - "Maximum excursion and stopping time record-holders" - Math. Comp.
7. Barina (2021) - "Convergence verification of the Collatz problem" - J. Supercomputing
8. Barina (2025) - "Improved verification limit...up to 2^71" - J. Supercomputing
9. Angeltveit (2026) - "An improved algorithm for checking the Collatz Conjecture" - arXiv
10. Honda et al. (2017) - "GPU-accelerated Exhaustive Verification" - IJNC
11. Czarnul (2023) - "Multithreaded CUDA and OpenMP framework" - Concurrency & Computation
12. Getachew & Assefa (2025) - "Efficient Computation of Collatz Sequence Stopping Times" - IEEE Access
13. Dutta (2025) - "Chronological Verification Using Theoretically Proven Sieves" - EJMAA
14. Polli et al. (2024) - "Stochastic-like characteristics of Collatz hailstone sequences" - J. Phys. Complexity
15. Sinai (2003) - "Uniform Distribution in the (3x+1)-Problem" - Moscow Math. J.
16. Leavens & Vermeulen (1992) - "3x+1 Search Programs" - Computers & Math. Applic.
17. Roosendaal (2025) - Online delay record database (ericr.nl)
18. OEIS A006877, A284668 - Integer sequence databases
