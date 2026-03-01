# Open Problems and Research Directions for SSSP

## Open Problem 1: Is O(m) Directed SSSP Achievable in the Comparison-Addition Model?

**Status:** Wide open.

**Context:** For undirected graphs, Thorup 1999 achieves O(m) in the word RAM model, and Pettie-Ramachandran 2005 achieve O(mα(m,n)) in the comparison-addition model — tantalizingly close to linear. For directed graphs, the current best in the comparison-addition model is O(m log^{2/3} n) by Duan et al. 2025.

**The question:** Is there an O(m) algorithm for SSSP on directed graphs with non-negative real weights in the comparison-addition model?

**Why it's hard:** The directed case is fundamentally different from undirected because:
1. There is no MST-based hierarchy to exploit (MST is undefined for directed graphs).
2. The shortest-path tree structure in directed graphs is less constrained.
3. Duan et al. 2025's interval pivot technique inherently introduces a log^{2/3}(n) factor through the three-way tradeoff.

**Lower bounds:** No non-trivial lower bound is known for SSSP in the comparison-addition model beyond the trivial Ω(m) (must read all edges). The gap between Ω(m) and O(m log^{2/3} n) is the central open problem.

**References:** Fredman-Tarjan 1987, Pettie-Ramachandran 2005, Duan et al. 2025.

---

## Open Problem 2: Can the log^{2/3} Factor in Duan et al. Be Reduced?

**Status:** Open — this is the most directly attackable problem.

**Context:** Duan et al. 2025 achieve O(m log^{2/3} n) through a three-way tradeoff between hop limit k, recursion depth parameter t, and the total number of recursive levels. The exponent 2/3 arises from balancing k = log^{1/3}(n) and t = log^{2/3}(n).

**The question:** Can the exponent 2/3 be reduced to, say, 1/2 or less? Is O(m log^{1/2} n), O(m log^{1/3} n), or even O(m · polylog(log n)) achievable?

**Approaches:**
1. **Improved data structures:** If the block-based linked list could support BatchPrepend with lower amortized cost, the edge processing overhead t could be reduced.
2. **Tighter recursion:** If the FindPivots subroutine could be made more efficient (e.g., by reusing partial computations across recursive levels), the nk/t factor could decrease.
3. **Randomization:** Duan et al. 2025 is deterministic. Randomized algorithms might achieve better tradeoffs (the undirected precursor by Duan et al. 2023 uses randomization).
4. **Adaptive parameters:** Instead of fixed k and t, adapting these parameters based on the graph structure could yield better bounds on specific graph families.

**References:** Duan et al. 2025, Duan et al. 2023.

---

## Open Problem 3: Deterministic Near-Linear Negative-Weight SSSP

**Status:** Partially resolved.

**Context:** Bernstein-Nanongkai-Wulff-Nilsen 2022 gave a randomized O(m log⁸(n) log W) algorithm. Bringmann-Cassis-Fischer 2023 improved this to O(m log²(n) log(nW)). Both are randomized.

**The question:** Is there a deterministic near-linear time algorithm for SSSP with negative weights?

**Progress:** A deterministic m^{1+o(1)} algorithm for min-cost flow (which subsumes SSSP) was given by van den Brand et al. at FOCS 2023, extending Chen et al. 2022. However, this gives m^{1+o(1)} rather than O(m · polylog(n)), and the constant in the o(1) exponent is significant.

**Open sub-questions:**
- Can the BNW framework be derandomized to O(m · polylog(n))?
- Can Duan et al. 2025's deterministic approach be extended to handle negative weights?

**References:** Bernstein-Nanongkai-Wulff-Nilsen 2022, Bringmann-Cassis-Fischer 2023, Chen et al. 2022.

---

## Open Problem 4: SSSP in Word RAM vs. Comparison-Addition Model

**Status:** Significant gap exists.

**Context:**
- Word RAM (integer weights): Thorup 2004 achieves O(m + n log log n) for directed graphs.
- Comparison-addition (real weights): Duan et al. 2025 achieve O(m log^{2/3} n) for directed graphs.

**The question:** What is the exact complexity of directed SSSP with non-negative integer weights in the word RAM model? Can it be solved in O(m) time?

**The gap:** There is a super-constant gap between the word RAM bound O(m + n log log n) and the comparison-addition bound O(m log^{2/3} n). This suggests that integer-specific techniques (bitwise operations, hashing, van Emde Boas trees) provide a genuine advantage, but the precise advantage is unknown.

**Sub-questions:**
- Is O(m + n) achievable for directed integer SSSP on the word RAM?
- Is there a comparison-addition lower bound that separates integer and real-weight SSSP?
- Can Thorup's O(m + n log log n) be improved using Duan et al.'s techniques?

**References:** Thorup 2004, Hagerup 2000, Duan et al. 2025.

---

## Open Problem 5: Connections to Circuit Complexity and Lower Bound Barriers

**Status:** Deep open problem.

**Context:** Proving super-linear lower bounds for any natural graph problem in the word RAM model is a major open challenge in complexity theory. The best known lower bounds for SSSP are:
- Ω(m) trivially (must read input)
- Ω(n log n) for comparison-based algorithms that must output sorted distances (Haeupler et al. 2024)

**The question:** Can we prove any lower bound better than Ω(m) for SSSP in the comparison-addition model (without requiring sorted output)?

**Barriers:**
1. **Natural proofs barrier:** Strong lower bounds for SSSP in general computational models would likely require techniques that overcome the natural proofs barrier, as SSSP can be solved by polynomial-size circuits.
2. **Cell probe lower bounds:** The cell probe model provides a framework for proving data structure lower bounds, but SSSP is not naturally a data structure problem.
3. **Comparison-addition model limitations:** The comparison-addition model is weak enough that lower bounds might be provable (similar to comparison-based sorting bounds), but no technique has succeeded beyond the trivial Ω(m).

**Significance:** Any lower bound of ω(m) for directed SSSP in the comparison-addition model would be a major result, as it would prove that Dijkstra's O(m + n log n) cannot be improved to O(m), definitively settling Open Problem 1.

**References:** Haeupler et al. 2024, Pettie-Ramachandran 2005, Fredman-Tarjan 1987.

---

## Open Problem 6: Practical Sub-Dijkstra SSSP

**Status:** Completely open.

**Context:** The Duan et al. 2025 algorithm has a theoretical crossover point of ~10^{67} vertices, making it utterly impractical. Even the undirected randomized algorithm of Duan et al. 2023 has enormous constants.

**The question:** Is there a sub-O(m + n log n) SSSP algorithm with sufficiently small constants to outperform Dijkstra on practical graph sizes (n ≤ 10⁹)?

**Approaches:**
1. Design algorithms specifically optimized for small constants rather than optimal asymptotic exponents.
2. Identify graph families where the theoretical advantage manifests at smaller n.
3. Combine theoretical insights with practical engineering (cache-oblivious design, parallelism, etc.).

**References:** Cassis-Fischer-Haeupler SEA 2025, Duan et al. 2025.

---

## Open Problem 7: SSSP on Special Graph Classes

**Status:** Various results known, many gaps.

**Context:** Many graph classes have structural properties that could enable faster SSSP:
- Planar graphs: O(n) SSSP is known (Henzinger et al. 1997).
- Bounded treewidth: O(m) is achievable.
- Expander graphs: The high connectivity might enable faster batch relaxation.

**The question:** For which graph classes can directed SSSP be solved in O(m) time in the comparison-addition model? Can the techniques of Duan et al. 2025 be specialized to achieve better bounds on structured graphs?

**References:** Pettie-Ramachandran 2005, Duan et al. 2025.

---

## Summary of Open Problems

| # | Problem | Current Best | Target | Difficulty |
|---|---------|-------------|--------|-----------|
| 1 | O(m) directed SSSP (comp-add) | O(m log^{2/3} n) | O(m) | Very hard |
| 2 | Reduce log^{2/3} exponent | 2/3 | < 2/3 | Moderate |
| 3 | Deterministic negative-weight SSSP | m^{1+o(1)} | O(m polylog) | Hard |
| 4 | Word RAM vs comp-add gap | O(n log log n) vs O(n log^{2/3} n) | Understand gap | Moderate |
| 5 | Super-Ω(m) lower bound | Ω(m) | ω(m) | Extremely hard |
| 6 | Practical sub-Dijkstra | Crossover ~10^{67} | Crossover ~10^{6} | Hard |
| 7 | Special graph classes | Various | O(m) for more classes | Moderate |

**Our research direction:** We target Open Problem 2 — reducing the log^{2/3} exponent — as the most accessible direction with the highest chance of a meaningful contribution.
