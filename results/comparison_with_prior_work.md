# Comparison with Prior Work

## 1. Our Best Candidates vs. Known BB(6) Champions

| Rank | Machine | Sigma | Steps | Discoverer | Year | Method |
|------|---------|-------|-------|------------|------|--------|
| **1** | `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | **> 2↑↑↑5** | > 2↑↑↑5 | mxdys | 2025 | Algebraic / Coq proof |
| **2** | `1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE` | **> 10↑↑15** | > 10↑↑16 | Kropitz | 2022 | Collatz-like analysis |
| **3** | `(see sligocki blog)` | **> 10↑↑5** | > 10↑↑5 | Ligocki family | 2022 | Algebraic analysis |
| **4** | `(see known_champions.json)` | **> 10^1.3B** | > 10^1.3B | Kropitz | 2022 | Collatz analysis |
| **5** | `(see known_champions.json)` | **> 10^10566** | > 10^10566 | Kropitz | 2010 | Manual analysis |
| ... | ... | ... | ... | ... | ... | ... |
| **Our #1** | `1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE` | **80** | 2452 | This work (mutation) | 2026 | Automated mutation search |
| **Our #2** | `1RB1LE_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | **66** | 3507 | This work (mutation) | 2026 | Automated mutation search |
| **Our #3** | `1RB0RF_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE` | **66** | 3313 | This work (mutation) | 2026 | Automated mutation search |

### Honest Assessment

**We did not achieve a new BB(6) record.** This was expected and should be clearly stated.

The gap between our best result (sigma=80) and the current record (sigma > 2↑↑↑5) is not merely large — it is incomprehensibly vast. The number 2↑↑↑5 is a pentation-level number: it represents iterated tetration of 2, itself an operation that produces numbers so large they dwarf anything expressible in conventional notation. Even the previous record holder (10↑↑15, a tower of 15 tens) is already far beyond what any step-by-step simulation could reach.

The fundamental reason is that **all known BB(6) champions operate through algebraic mechanisms** (Collatz-like rules, counter machines, shift-overflow patterns) that produce outputs scaling as towers of exponentials or higher in the Knuth arrow hierarchy. These machines cannot be found or verified through brute-force simulation with bounded step counts. They require:

1. **Algebraic analysis** of the TM's macro-behavior (identifying the Collatz-like or counter rules it implements)
2. **Number-theoretic proofs** that the rules eventually terminate (e.g., using Euler's totient theorem for modular arithmetic, as in the Kropitz t15 verification \[ligocki2022bb6\])
3. **Formal verification** in proof assistants like Coq/Rocq \[mxdys2025bb6\]

Our step-limited simulation approach (step limit 10^5–10^6) can only discover machines whose behavior terminates within that horizon. This is a well-understood limitation: as noted by Aaronson \[aaronson2020\], the Busy Beaver function grows faster than any computable function, so for sufficiently large n, BB(n) will always exceed any fixed computational budget.

## 2. Search Strategy Comparison

| Strategy | Machines Explored | Halting Found | Best Sigma | Best Steps | Wall Time | Throughput |
|----------|------------------|---------------|------------|------------|-----------|------------|
| TNF Random Sample | 500,000 | 206,461 (41.3%) | 10 | 92 | 23.8s | 21,008 TMs/s |
| Mutation Search | 1,296 | 662 (51.1%) | **80** | **3,507** | 1.4s | 926 TMs/s |
| TM Breeding | 125 | 62 (49.6%) | 66 | 3,507 | 0.6s | 208 TMs/s |
| Guided (Feature-biased) | 500,000 | 151,457 (30.3%) | 11 | 68 | 321.0s | 1,558 TMs/s |
| **Total** | **1,001,296** | **358,642** | **80** | **3,507** | **346.9s** | **2,886 TMs/s** |

### Key Findings

1. **Mutation search is the most effective strategy for finding high-scoring machines.** Despite exploring only 1,296 machines (0.13% of the total), it found the campaign's best result (sigma=80) and contributed 55 of the top 100 candidates. This confirms the hypothesis from our ConceptEvolve analysis that champion neighborhoods are enriched for interesting behavior.

2. **Random search produces volume but not quality.** The TNF random sample explored 500K machines and found nothing above sigma=10. This is consistent with the extreme sparsity of high-scoring machines in the 6-state TM space, which has approximately 10^15 machines in TNF \[marxen1990, michel2015\].

3. **Guided search underperformed expectations.** The feature-biased approach found only marginally better results (sigma=11) than pure random (sigma=10), while being 13x slower. This suggests that the structural features extracted from known champions (write ratio, self-loops, graph density) do not sufficiently capture the properties that lead to long-running behavior. The features that matter most are likely **semantic** (what computation the TM implements) rather than **syntactic** (graph topology).

4. **Breeding produces reasonable candidates efficiently.** With only 125 unique offspring from 4 parent machines, breeding found sigma=66 machines. However, these were one-mutation-away variants of the mxdys champion, suggesting the breeding strategies (row swap, column swap, block crossover) effectively act as structured mutations.

## 3. Throughput Comparison with Published Projects

| Project | Machines Evaluated | Hardware | Time Period | Focus |
|---------|-------------------|----------|-------------|-------|
| bbchallenge.org \[collaboration2025bb5\] | ~88.7 billion (5-state) | Distributed compute, 100+ contributors | 2022–2024 | Complete enumeration + deciding |
| Marxen & Buntrock \[marxen1990\] | ~2.7 million (5-state) | Single workstation, 1989 | Months | TNF enumeration |
| This work | ~1 million (6-state) | 20-core server, C-accelerated | ~6 minutes | Heuristic search |

Our throughput of ~2,886 TMs/s with parallel C-accelerated simulation is reasonable for a research prototype. The bbchallenge project achieved far greater scale through distributed computing and years of effort, but their focus was complete enumeration of the 5-state case, not heuristic search in the 6-state case.

For context, the 6-state 2-symbol TNF space contains approximately 4.5 × 10^15 machines \[michel2015\]. At our throughput, exhaustive enumeration would take approximately 50 million years. This underscores why heuristic and algebraic approaches are essential for BB(6).

## 4. What Would It Take to Find a New BB(6) Record?

Based on our analysis and the literature:

1. **Step-limited simulation alone is insufficient.** All known BB(6) champions produce output exceeding any reasonable simulation bound. A new record would likely also operate at astronomical scales.

2. **The path to new records is algebraic.** Both the Kropitz t15 \[kropitz2022bb6, ligocki2022bb6\] and mxdys \[mxdys2025bb6\] champions were found and verified through:
   - Identification of the macro-level computation (Collatz-like rules, shift-overflow counters)
   - Proof that the computation terminates
   - Calculation of the output magnitude using number theory

3. **Promising directions:**
   - **Symbolic simulation** with CTL and other closed-form techniques \[collaboration2025deciders\], extended to 6 states
   - **Automated algebraic analysis** — detecting Collatz-like rules in TM transition tables and attempting termination proofs
   - **Collatz-connected search** — searching specifically for TMs that implement known-to-terminate Collatz variants with longer chains
   - **Formal verification integration** — coupling search with Coq/Lean proof search, as demonstrated by mxdys

4. **The bbchallenge approach scaled up.** The BB(5) proof \[collaboration2025bb5\] used a pipeline of increasingly sophisticated deciders (CTL, backward reasoning, Cyclers, Translated Cyclers, etc.) to decide all 88.7 billion 5-state machines. Applying this pipeline to 6-state machines, with deciders extended for the larger state space, could identify holdouts that are candidates for new records.

## 5. What We Learned

1. **The mutation neighborhood of champions is rich.** Single mutations from the Kropitz t15 champion produced machines with sigma up to 80 — far exceeding anything found by random search. This suggests that champion machines occupy "interesting" regions of TM space where many nearby machines also exhibit complex behavior.

2. **Syntactic features are poor predictors.** Graph topology metrics (density, self-loops, etc.) did not effectively identify promising machines. This is consistent with the observation by Aaronson \[aaronson2020\] that Busy Beaver machines can have simple transition tables but extremely complex behavior — the complexity is in the dynamics, not the syntax.

3. **The C acceleration was worthwhile.** The 60x speedup from the C backend allowed us to evaluate 1M machines in under 6 minutes. Without it, the campaign would have taken 6+ hours.

4. **Cross-checking catches bugs.** Running both Python and C simulators on every candidate provides confidence in results. All 100 verified candidates passed cross-checking.

## References

- \[rado1962\] Rado, T. (1962). On non-computable functions. Bell System Technical Journal.
- \[marxen1990\] Marxen, H. & Buntrock, J. (1990). Attacking the Busy Beaver 5.
- \[michel2015\] Michel, P. (2015). Problems in number theory from busy beaver competition.
- \[aaronson2020\] Aaronson, S. (2020). The Busy Beaver Frontier.
- \[collaboration2025bb5\] bbchallenge Collaboration (2025). Determination of the fifth Busy Beaver value.
- \[collaboration2025deciders\] bbchallenge Collaboration (2025). Turing machines deciders, part I.
- \[ligocki2022bb6\] Ligocki, S. (2022). BB(6,2) > 10↑↑15.
- \[kropitz2022bb6\] Kropitz, P. (2022). New BB(6) Lower Bound.
- \[mxdys2025bb6\] mxdys (2025). New BB(6) Lower Bound: 2↑↑↑5.
- \[aaronson2025bb6blog\] Aaronson, S. (2025). BusyBeaver(6) is really quite large.
