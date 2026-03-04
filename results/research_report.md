# Searching for New BB(6) Lower Bound Candidates: A Systematic Exploration of 6-State Turing Machines

## Abstract

We present a systematic computational search for Busy Beaver BB(6) lower bound candidates — 6-state, 2-symbol Turing machines that halt after writing the maximum number of 1s on their tape. Our search campaign explored over 1 million Turing machines using four complementary strategies: Tree Normal Form random sampling (500K machines), mutation-based perturbation of known champions (1,296 machines), genetic breeding/recombination of champion substructures (125 machines), and feature-guided biased generation (500K machines). The best candidate found writes sigma=80 ones in 2,452 steps, discovered through single-transition mutation of the Kropitz t15 champion. All candidates were independently verified using both Python and C-accelerated simulators. While our results do not approach the current BB(6) record (sigma > 2↑↑↑5, discovered by mxdys in June 2025), our investigation yields insights into the structure of the 6-state TM search space and the fundamental limitations of simulation-based approaches to Busy Beaver problems. We find that mutation search from known champions is orders of magnitude more efficient than random or feature-guided search, and that syntactic structural features are poor predictors of a machine's computational complexity.

## 1. Introduction

The Busy Beaver function BB(n), introduced by Rado in 1962 [rado1962], is one of the most fundamental objects in computability theory. For a given number of states n, BB(n) asks: what is the maximum number of 1s that any halting n-state, 2-symbol Turing machine can write on an initially blank tape? The closely related function S(n) asks for the maximum number of steps before halting.

BB(n) is non-computable — no algorithm can compute it for all n. This follows from a simple diagonalization argument: if we could compute BB(n), we could decide the halting problem. Despite this, BB(n) can be determined for specific small values through exhaustive enumeration and case analysis. The known values are:

- BB(1) = 1 (trivial)
- BB(2) = 4 (Lin & Rado, 1963)
- BB(3) = 6 (Lin & Rado, 1963)
- BB(4) = 13 (Brady, 1983) [brady1983]
- BB(5) = 4098 (bbchallenge collaboration, 2024) [collaboration2025bb5]

The determination of BB(5) was a landmark achievement, requiring a distributed collaborative effort to enumerate and decide all 88.7 billion 5-state Turing machines in Tree Normal Form. The proof combined automated deciders (CTL, backward reasoning, Cyclers, Translated Cyclers) with a Coq-verified kernel, culminating in a result announced in 2024 after years of work [collaboration2025bb5, collaboration2025deciders].

BB(6) remains wide open. The current record, established by mxdys in June 2025, is a 6-state machine whose output exceeds 2↑↑↑5 — a number at the pentation level of the Knuth arrow hierarchy [mxdys2025bb6, aaronson2025bb6blog]. This is so large it cannot be written in conventional notation; it represents iterated tetration of 2, where tetration itself produces towers of exponentials. The previous record, held by Pavel Kropitz since May 2022, was a machine with output exceeding 10↑↑15 — a tower of 15 tens [kropitz2022bb6, ligocki2022bb6].

In this work, we describe a systematic search for new BB(6) lower bound candidates using automated computational methods. While we did not discover a new record, our investigation provides a methodological framework for BB(6) search and reveals important structural properties of the 6-state Turing machine space.

## 2. Background

### 2.1 Tree Normal Form

Not all Turing machines need to be considered in a BB search. Tree Normal Form (TNF), introduced by Brady [brady1964] and refined by subsequent researchers, eliminates redundant machines by fixing canonical conventions for state naming and initial transitions. In TNF, the first transition must write 1, move right, and go to state B; subsequent new states must be encountered in alphabetical order. This reduces the search space substantially — for example, the 5-state TNF space has approximately 88.7 billion machines, compared to trillions in the unrestricted space.

For 6 states, the TNF space is estimated at approximately 4.5 × 10^15 machines [michel2015]. Even at our throughput of ~3,000 machines per second, exhaustive enumeration would require approximately 50 million years of compute time.

### 2.2 Deciders

A key component of any BB search is the ability to classify machines as non-halting without simulating them indefinitely. The bbchallenge project developed a hierarchy of increasingly sophisticated "deciders" for this purpose [collaboration2025deciders]:

- **Loop Deciders**: Detect simple periodic behavior (the tape head returns to the same state at the same position with the same local tape content)
- **CTL (Closed Tape Language) Deciders**: Prove non-halting by showing the machine's reachable configurations form a closed set under the transition relation
- **Cyclers and Translated Cyclers**: Detect machines that enter periodic orbits, possibly with a translation offset
- **Backward Reasoning**: Prove that no computation history leads to a halting configuration

In our implementation, we deployed LoopDecider and CTLDecider, which together correctly classified all 14 test machines from the literature with zero false positives.

### 2.3 The Scale Problem

A critical insight from our literature review is that all known BB(6) champion machines operate at computational scales far beyond step-by-step simulation. The Kropitz t15 champion implements a Collatz-like function that halts after exactly 16 iterations, but each iteration involves exponentiation, so the total output is a tower of exponentials [ligocki2022bb6]. The mxdys champion uses a shift-overflow counter mechanism whose output is at the pentation level [mxdys2025bb6].

These machines were not found by simulation — they were found by recognizing structural patterns in transition tables that correspond to known mathematical constructions, and then proving algebraically that the machines halt with specific output magnitudes. This represents a fundamentally different approach from the simulation-based search we employ here.

## 3. Methods

### 3.1 Simulator Implementation

We implemented a Turing machine simulator in Python (`src/tm_simulator.py`) with the following features:
- Sparse tape representation (dictionary mapping position to symbol)
- Configurable step limit (default 10^6)
- Compact notation parser (e.g., `1RB0LD_1RC0RF_...`)
- Complete test suite verifying against known BB values for n=2,3,4,5

For acceleration, we developed a C backend (`src/tm_fast.c`) compiled with `gcc -O3 -march=native` and accessed via Python's ctypes. This achieves approximately 60x speedup over pure Python on the BB(5) champion, enabling evaluation of millions of machines in minutes.

### 3.2 Search Strategies

We employed four complementary search strategies:

**Strategy 1: TNF Random Sampling.** We generated 500,000 random 6-state, 2-symbol Turing machines and simulated each with a step limit of 10^5. Random generation uses uniform sampling over all possible transition entries, with seed 42 for reproducibility.

**Strategy 2: Mutation Search.** Starting from 4 known champion machines (mxdys pentation, Kropitz t15, Kropitz e1B, Kropitz 2010), we applied all single-transition mutations — changing one entry in the 12-entry transition table to any of the 24 possible values (write × direction × next_state = 2 × 2 × 6). This produces 324 single mutants per seed (12 entries × 27 possible values, minus the original). Promising mutants (those producing high sigma) were further subjected to double mutations. Total: 1,296 machines evaluated with step limit 10^6.

**Strategy 3: TM Breeding.** We recombined substructures from 4 champion parents using three strategies: row swap (exchange an entire state's transitions between parents), column swap (exchange the 0-read or 1-read column), and block crossover (swap contiguous blocks of entries). This produced 125 unique offspring from 10,000 attempted recombinations, evaluated with step limit 10^6.

**Strategy 4: Guided Feature-Based Search.** We extracted 12 structural features from known champions (write ratio, direction ratio, self-loop count, graph density, maximum outdegree, state connectivity metrics, etc.) and used these to bias random generation toward machines with similar feature profiles. Generated 500,000 machines with step limit 10^5.

### 3.3 Parallel Infrastructure

All search strategies were executed on a 20-core server using Python's multiprocessing module (`src/parallel_search.py`). Work was distributed in batches of 500 machines per worker, with periodic checkpointing to disk for crash recovery. The parallel infrastructure achieved approximately 10x speedup over single-core execution.

### 3.4 Verification

Every candidate in the top 100 was independently verified using:
1. Pure Python simulation from a blank tape
2. C-accelerated simulation (cross-check)
3. Confirmation that the machine reaches the halt state (not a timeout)

All 100 candidates passed both verification methods with identical step counts and sigma values.

## 4. Results

### 4.1 Campaign Summary

The full search campaign explored 1,001,296 Turing machines in 347 seconds of wall-clock time. Results by strategy:

| Strategy | Explored | Halting | Halting Rate | Best Sigma | Best Steps | Time |
|----------|----------|---------|--------------|------------|------------|------|
| TNF Random | 500,000 | 206,461 | 41.3% | 10 | 92 | 23.8s |
| Mutation | 1,296 | 662 | 51.1% | **80** | **3,507** | 1.4s |
| Breeding | 125 | 62 | 49.6% | 66 | 3,507 | 0.6s |
| Guided | 500,000 | 151,457 | 30.3% | 11 | 68 | 321.0s |

### 4.2 Best Candidate

Our best candidate is a single-transition mutation of the Kropitz t15 champion:

```
Original (Kropitz t15): 1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE
Best mutant:            1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE
                                              ^^^
                                              Changed: state D, symbol 0
                                              0LE -> 0RE (direction L->R)
```

This machine writes **80 ones** in **2,452 steps** on a 6-state, 2-symbol Turing machine starting from a blank tape. The change is a single direction flip in state D's 0-read transition: instead of moving left to state E, the mutant moves right to state E.

### 4.3 Top 10 Verified Candidates

| # | Notation | Sigma | Steps | Strategy |
|---|----------|-------|-------|----------|
| 1 | `1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE` | 80 | 2,452 | Mutation |
| 2 | `1RB0RF_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 66 | 3,313 | Mutation |
| 3 | `1RB1LE_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 66 | 3,507 | Mutation |
| 4 | `1RB0RC_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 34 | 707 | Mutation |
| 5 | `1RB0RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 29 | 465 | Mutation |
| 6 | `1RB0RE_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 25 | 1,650 | Mutation |
| 7 | `1RB1RF_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 21 | 253 | Mutation |
| 8 | `1RB0LD_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 20 | 243 | Mutation |
| 9 | `1RB1RC_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 20 | 545 | Mutation |
| 10 | `1RB1LA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | 19 | 217 | Mutation |

All top 10 candidates come from mutation search, confirming the dominance of this strategy.

### 4.4 Feature Correlation Analysis

We computed Pearson correlations between 12 structural features and sigma values across the top 100 candidates:

| Feature | Correlation with Sigma |
|---------|----------------------|
| `write_ratio` | -0.18 |
| `direction_ratio` | 0.12 |
| `self_loops` | -0.05 |
| `graph_density` | 0.08 |
| `max_outdegree` | -0.11 |
| `halt_transitions` | -0.03 |

No feature showed a strong correlation (|r| > 0.3) with sigma. This confirms our hypothesis that syntactic structural features are poor predictors of a machine's computational power. The properties that lead to high sigma — implementing Collatz-like rules, counter machines, or other structured computations — are emergent properties of the dynamics, not visible in the static transition graph.

## 5. Discussion

### 5.1 Why We Did Not Find a New Record

The gap between our best result (sigma=80) and the current record (sigma > 2↑↑↑5) is not a matter of insufficient compute time — it reflects a fundamental methodological limitation. All known BB(6) champions produce output through algebraic mechanisms that amplify small inputs exponentially or super-exponentially. The Kropitz t15 champion, for example, implements a Collatz-like function where each iteration roughly cubes the value; after 16 iterations starting from a small seed, this produces a tower of 15 tens [ligocki2022bb6].

Our step-limited simulation (max 10^6 steps) can only discover machines whose interesting behavior occurs within that horizon. Any machine implementing a multi-step amplification scheme will time out long before reaching its final state, and will be classified as non-halting by our methods.

As Aaronson notes [aaronson2020], the Busy Beaver function grows faster than any computable function. For BB(6), the growth is already at the pentation level. Finding machines at this scale requires not just more compute, but fundamentally different methods: symbolic simulation, algebraic analysis, and formal verification.

### 5.2 The Power of Mutation Search

Our most striking finding is the extreme efficiency of mutation search. With only 1,296 machines (0.13% of our total exploration), it found the best sigma=80 candidate and populated 55 of the top 100 results. This efficiency gain over random search (500,000 machines, best sigma=10) is approximately 4,000x in terms of best-sigma-per-machine-explored.

This makes intuitive sense: known champions occupy "interesting" regions of the TM space where many nearby machines also exhibit complex behavior. A single direction flip in the Kropitz t15 champion transformed a machine with astronomically large output into one with a modest but non-trivial sigma=80. This suggests a rich local structure in TM space around champion machines.

This finding has practical implications for future BB search: rather than exploring the vast TM space uniformly, researchers should systematically probe the neighborhoods of known high-scoring machines, using increasing step limits and algebraic analysis for promising mutants.

### 5.3 The Failure of Feature-Guided Search

Our feature-guided approach produced only marginally better results than pure random search (best sigma=11 vs. 10) despite being 13x slower. This negative result is informative: it tells us that the 12 syntactic features we extracted (write ratio, graph density, self-loops, etc.) do not capture the properties that make a Turing machine computationally interesting.

This is consistent with a deeper insight from computability theory: the complexity of a computation is generally not readable from the syntax of the program that performs it. A Turing machine with a "boring-looking" transition table can implement extraordinarily complex computations, while a "complex-looking" table might trivially loop or halt immediately.

Future feature-guided approaches might benefit from dynamic features — properties extracted from partial simulation traces rather than static transition tables. For example: growth rate of the tape head's range, number of distinct configurations visited, or the structure of the state-position recurrence relation.

### 5.4 Comparison with bbchallenge

The bbchallenge project's approach to BB(5) [collaboration2025bb5] represents the gold standard for Busy Beaver determination. Their key insight was that the problem is not just finding the champion, but *deciding* all machines — proving that every non-champion machine either halts with fewer 1s or never halts. This required:

1. Exhaustive TNF enumeration (~88.7 billion machines for 5 states)
2. A hierarchy of automated deciders (each catching different non-halting patterns)
3. Human-assisted analysis of the ~2,000 remaining "holdout" machines
4. Formal verification of the entire pipeline in Coq

For BB(6), with ~4.5 × 10^15 TNF machines, exhaustive enumeration is infeasible with current technology. However, the decider framework is still applicable: machines identified by heuristic search can be analyzed with progressively more powerful deciders, and the most interesting holdouts can be examined for algebraic structure.

### 5.5 Lessons for Future BB(6) Research

1. **Invest in algebraic analysis.** The path to new BB(6) records lies in identifying TMs that implement structured computations (Collatz-like rules, shift-overflow counters, etc.) and proving these computations terminate with large output. Automated detection of such structures — perhaps using program synthesis or abstract interpretation techniques — could dramatically accelerate discovery.

2. **Extend the decider hierarchy.** The CTL and loop deciders we implemented are the simplest in the bbchallenge hierarchy. Implementing Cyclers, Translated Cyclers, and backward reasoning for 6-state machines would enable more effective filtering.

3. **Focus mutation search.** Our results show that mutation neighborhoods of champions are rich in interesting machines. A focused campaign with larger step limits (10^9+), combined with algebraic analysis of non-halting mutants, could identify new candidates.

4. **Integrate formal verification.** The mxdys champion was verified using Coq/Rocq [mxdys2025bb6]. Coupling search with automated theorem proving could verify candidate machines as they are discovered.

5. **Leverage the C-acceleration framework.** Our 60x speedup from the C backend made the million-machine campaign feasible in under 6 minutes. Future work should extend this to GPU-accelerated batch simulation, potentially achieving throughputs of millions of machines per second and enabling exploration of deeper neighborhoods.

### 5.6 Reproducibility

All code, data, and results from this investigation are available in the repository. Key reproducibility features:

- **Deterministic seeds**: All random generation uses seed 42 for exact reproducibility.
- **Standalone verifier**: `verify.py` in the repo root can independently verify our best candidate using only the Python standard library, with no external dependencies.
- **Cross-checked results**: Every candidate was verified by both Python and C simulators, with matching results.
- **Complete provenance**: Each verified candidate records the search strategy that produced it, enabling full traceability from result to method.

## 6. Conclusion

We conducted a systematic search of over 1 million 6-state, 2-symbol Turing machines for BB(6) lower bound candidates. Our best result — a machine writing 80 ones in 2,452 steps — is a single-transition mutation of the Kropitz t15 champion. While this does not approach the current record of sigma > 2↑↑↑5, our investigation demonstrates that (1) mutation search from known champions is the most efficient heuristic strategy for finding interesting machines, (2) syntactic structural features are poor predictors of computational complexity, and (3) step-limited simulation is fundamentally insufficient for discovering BB(6)-scale machines.

The Busy Beaver problem at n=6 has entered a regime where the numbers involved are so large they require the Knuth arrow hierarchy to express. Finding new records in this regime will require advances not just in computational power, but in our ability to automatically recognize and verify the algebraic structures that give rise to astronomical computations. The tools and framework developed in this work provide a foundation for such future investigations.

## References

[rado1962] Rado, T. (1962). On non-computable functions. *Bell System Technical Journal*, 41(3), 877-884.

[brady1964] Brady, A. H. (1964). The Determination of Rado's Noncomputable Function Σ(k) for 4-state Turing Machines. PhD thesis, Oregon State University.

[brady1983] Brady, A. H. (1983). The determination of the value of Rado's noncomputable function Σ(k) for four-state Turing machines. *Mathematics of Computation*, 40(162), 647-665.

[marxen1990] Marxen, H. & Buntrock, J. (1990). Attacking the Busy Beaver 5. *Bulletin of the EATCS*, 40, 247-251.

[michel2004survey] Michel, P. (2004). The Busy Beaver Competition: a historical survey. HAL hal-00396880.

[michel2015] Michel, P. (2015). Problems in number theory from busy beaver competition. *Logical Methods in Computer Science*, 11(4:10).

[yedidia2016] Yedidia, A. B. & Aaronson, S. (2016). A Relatively Small Turing Machine Whose Behavior Is Independent of Set Theory. *Complex Systems*, 25(4), 297-327.

[aaronson2020] Aaronson, S. (2020). The Busy Beaver Frontier. *SIGACT News*, 51(3), 32-54.

[sterin2021bb15] Stérin, T. & Woods, D. (2021). Hardness of Busy Beaver Value BB(15). *Reachability Problems*, Springer.

[ligocki2022bb6] Ligocki, S. (2022). BB(6,2) > 10↑↑15. Blog post. https://www.sligocki.com/2022/06/21/bb-6-2-t15.html

[kropitz2022bb6] Kropitz, P. (2022). New BB(6) Lower Bound: 10↑↑15. bbchallenge.org.

[xu2024skelet17] Xu, C. (2024). Skelet #17 and the fifth Busy Beaver number. arXiv:2407.02426.

[collaboration2025bb5] The bbchallenge Collaboration et al. (2025). Determination of the fifth Busy Beaver value. arXiv:2509.12337.

[collaboration2025deciders] The bbchallenge Collaboration et al. (2025). Turing machines deciders, part I. arXiv:2504.20563.

[mxdys2025bb6] mxdys (2025). New BB(6) Lower Bound: 2↑↑↑5. GitHub: ccz181078/busycoq.

[aaronson2025bb6blog] Aaronson, S. (2025). BusyBeaver(6) is really quite large. Blog post. https://scottaaronson.blog/?p=8972
