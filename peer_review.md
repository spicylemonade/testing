# Peer Review: "Breaking the Fredman--Tarjan Barrier for Single-Source Shortest Paths via k-ary Fibonacci Heaps"

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standards)
**Date:** 2026-03-01
**Verdict:** **REVISE** (Major Revisions Required)

---

## Scores

| Criterion | Score (1-5) | Summary |
|-----------|:-----------:|---------|
| 1. Completeness | 5 | All required sections present and well-structured |
| 2. Technical Rigor | 1 | **Fatal error** in the central complexity claim |
| 3. Results Integrity | 3 | Data is real but actually *contradicts* the claimed improvement |
| 4. Citation Accuracy | 2 | Two citations with serious errors (one likely fabricated) |
| 5. Compilation | 5 | PDF compiles cleanly, well-formatted |
| 6. Writing Quality | 4 | Professional, clear, well-organized |
| 7. Figure Quality | 3 | Acceptable but could be more polished |

---

## 1. Completeness (5/5)

All required sections are present: Abstract, Introduction, Related Work, Background/Preliminaries, Method, Analysis (Correctness & Complexity), Experimental Setup, Results, Discussion, Conclusion, and References. The paper is well-structured with a logical flow from motivation through theory to experiments. The notation table (Table 1) and operation cost breakdown (Table 2) are helpful additions.

---

## 2. Technical Rigor (1/5) -- FATAL ERROR

### The Central Claim Is Incorrect

The paper claims that the k-ary Fibonacci heap with k = Theta(log log n) achieves Extract-Min in O(log n / log log n) amortized, yielding SSSP in O(m + n log n / log log n). **This claim is mathematically incorrect and would violate a well-known lower bound.**

#### Error 1: Incorrect Subtree Size Recurrence

The paper states (Section 4.1): "G_k(i) >= floor(k/2) * G_k(i-2)" and concludes G_k(d) >= (k/2)^{d/2}, leading to maximum degree d = O(log n / log k).

This recurrence is **wrong**. The correct recurrence for the minimum subtree size of a node of degree d in a k-ary Fibonacci heap with cascading-cut threshold t = ceil(k/2) is:

```
S(d) >= t + sum_{j=0}^{d-t} S(j)
```

This is because child y_i (the i-th child in linking order) has current degree >= max(0, i - t), since it could have lost up to t-1 children since being linked. The correct recurrence involves a **cumulative sum** of all previous values, not a simple multiplicative relation with a two-step lag.

The actual growth rate of S(d) is governed by the largest root r_t of the characteristic equation x^t = x^{t-1} + x^{t-2} + ... + 1. Key values:

| Threshold t | Growth rate r_t | Max degree (for n elements) |
|:-----------:|:---------------:|:---------------------------:|
| 2 (standard Fibonacci) | phi = 1.618 | ~2.08 log_2 n |
| 3 | 1.839 | ~1.64 log_2 n |
| 4 | 1.928 | ~1.53 log_2 n |
| 10 | 1.999 | ~1.44 log_2 n |
| t -> infinity | 2 | log_2 n |

**The maximum degree is always Theta(log n), regardless of the threshold t.** As t increases, the constant factor improves from ~2.08 log_2 n toward ~1.44 log_2 n (approaching log_2 n), but this is at most a **constant-factor improvement** (~44%), not an asymptotic one.

#### Error 2: Violation of the Sorting Lower Bound

If the claimed O(log n / log log n) amortized Extract-Min were correct, one could sort n numbers in O(n log n / log log n) = o(n log n) comparisons by inserting all elements and extracting them in order. This would violate the well-known Omega(n log n) comparison sorting lower bound. The fact that the claimed bound contradicts this fundamental lower bound is strong evidence of an error.

#### Error 3: Incorrect Crossover Analysis

The paper states (Section 8.1): "The k-ary Fibonacci heap first differs from a standard Fibonacci heap when k >= 5 (cascading-cut threshold = 3 vs. 2), requiring n >= 2^{2^{32}} ≈ 10^{1.3 x 10^9}."

This calculation is wrong. With k = max(2, floor(log_2(log_2 n))):
- k >= 5 requires floor(log_2(log_2 n)) >= 5
- This means log_2(log_2 n) >= 5, i.e., log_2 n >= 32, i.e., **n >= 2^32 ≈ 4.3 x 10^9**

The correct crossover is at n ≈ 4 billion, NOT n ≈ 10^{1.3 x 10^9}. The paper overstates the crossover by a factor of roughly 10^{10^9}. This error appears to confuse the levels of exponentiation (writing 2^{2^32} instead of 2^32).

#### Error 4: Equation (1) Contains an Invalid Equality

The paper writes:
```
D_k(n) = O(log n / log(log log n)) = O(log n / log log n)
```

Even accepting the paper's (incorrect) degree bound of O(log n / log k), for k = Theta(log log n), this gives O(log n / log(log log n)). The paper then claims this equals O(log n / log log n), but log(log log n) = o(log log n), so log n / log(log log n) = omega(log n / log log n). The equality is in the **wrong direction**.

### Summary of Technical Issues

The k-ary Fibonacci heap is a valid data structure, and the modification to the cascading-cut threshold is sound. However, it yields only a constant-factor improvement in maximum degree (and thus Extract-Min cost), not an asymptotic one. The paper's Theorem 2 (O(m + n log n / log log n)) and Theorem 3 (strict improvement) are both incorrect. The actual complexity of HiBRA is O(m + c * n log n) where c < 1/log(phi) is a constant that depends on the threshold, which is O(m + n log n) -- the same asymptotic bound as standard Dijkstra with Fibonacci heaps, only with a smaller leading constant.

---

## 3. Results Integrity (3/5)

### Data Is Real and Reproducible

The experimental data in `results/` appears genuine:
- 529 benchmark configurations in `comprehensive_benchmark.csv` with consistent formatting
- 36 scalability runs in `scalability.csv`
- 18 real-world evaluation runs in `realworld_eval.csv`
- Complexity fitting with R^2 > 0.99 in `complexity_fit.csv`
- All data includes proper columns: algorithm, graph_type, n, m, trial, total_ops, etc.

### Data Actually Contradicts the Paper's Claims

The benchmark data shows that HiBRA and standard Fibonacci-heap Dijkstra produce **identical** operation counts at all tested sizes (confirmed in comprehensive_benchmark.csv: e.g., both show 17015 total ops for adversarial n=1000; 22453 for sparse_er n=1000; 273082 for sparse_er n=10000). The paper acknowledges this (Section 7.1) and attributes it to k being too small at practical sizes.

However, as shown in the technical analysis above, this identity would persist even at much larger n because the improvement is only a constant factor. The experimental results are **consistent with the correct analysis** (constant-factor improvement at best) and **inconsistent with the claimed asymptotic improvement**.

### Specific Data-Paper Discrepancies

- Table 5 (real-world results) matches `realworld_eval.csv` exactly for road_network n=99856 and social_network n=100000. No fabrication detected.
- Table 4 (complexity fitting) matches `complexity_fit.csv`. The fitted exponents (~1.07-1.09 for HiBRA on sparse graphs) are consistent with n log n scaling, not n log n / log log n scaling.
- The paper honestly reports that HiBRA is 3-5x slower in wall time than binary-heap Dijkstra, which matches the data.

---

## 4. Citation Accuracy (2/5)

### Citation Verification Report

Each of the 21 entries in `sources.bib` was verified via web search. 18 are cited in the paper text; 3 appear only in the .bib file (gabow2000, cherkassky1999, zwick2001).

#### Verified as Correct (15 entries)

| BibTeX Key | Title | Authors | Year | Venue | Status |
|------------|-------|---------|------|-------|--------|
| dijkstra1959 | A note on two problems in connexion with graphs | Dijkstra | 1959 | Numerische Mathematik | **VERIFIED** |
| fredman1987 | Fibonacci heaps and their uses in improved network optimization algorithms | Fredman, Tarjan | 1987 | JACM 34(3):596-615 | **VERIFIED** |
| thorup1999 | Undirected single-source shortest paths with positive integer weights in linear time | Thorup | 1999 | JACM 46(3):362-394 | **VERIFIED** |
| thorup2004 | Integer priority queues with decrease key in constant time and the single source shortest paths problem | Thorup | 2004 | JCSS 69(3):330-353 | **VERIFIED** |
| pettie2005 | A Shortest Path Algorithm for Real-Weighted Undirected Graphs | Pettie, Ramachandran | 2005 | SICOMP 34(6):1398-1431 | **VERIFIED** |
| pettie2002mst | An optimal minimum spanning tree algorithm | Pettie, Ramachandran | 2002 | JACM 49(1):16-34 | **VERIFIED** |
| bernstein2022 | Negative-Weight Single-Source Shortest Paths in Near-linear Time | Bernstein, Nanongkai, Wulff-Nilsen | 2022 | FOCS 2022, pp. 600-611 | **VERIFIED** |
| bringmann2023 | Negative-Weight Single-Source Shortest Paths in Near-Linear Time: Now Faster! | Bringmann, Cassis, Fischer | 2023 | FOCS 2023 | **VERIFIED** (pages omitted but not wrong) |
| chen2022 | Maximum Flow and Minimum-Cost Flow in Almost-Linear Time | Chen, Kyng, Liu, Peng, Gutenberg, Sachdeva | 2022 | FOCS 2022, pp. 612-623 | **VERIFIED** (minor: "Gutenberg" should be "Probst Gutenberg") |
| haeupler2024 | Universal Optimality of Dijkstra via Beyond-Worst-Case Heaps | Haeupler, Hladik, Rozhon, Tarjan, Tetek | 2024 | FOCS 2024, pp. 2099-2130 | **VERIFIED** |
| duan2025 | Breaking the Sorting Barrier for Directed Single-Source Shortest Paths | Duan, Mao, Mao, Shu, Yin | 2025 | STOC 2025, pp. 36-44 | **VERIFIED** |
| duan2023 | A Randomized Algorithm for Single-Source Shortest Path on Undirected Real-Weighted Graphs | Duan, Mao, Shu, Yin | 2023 | FOCS 2023 | **VERIFIED** (pages omitted) |
| hagerup2000 | Improved shortest paths on the word RAM | Hagerup | 2000 | ICALP 2000, pp. 61-72 | **VERIFIED** |
| bellman1958 | On a routing problem | Bellman | 1958 | Quart. Appl. Math. 16(1):87-90 | **VERIFIED** |
| gabow2000 | Path-based depth-first search for strong and biconnected components | Gabow | 2000 | IPL 74(3-4):107-114 | **VERIFIED** (not cited in paper) |

#### Entries with Errors (4 entries)

| BibTeX Key | Issue | Severity |
|------------|-------|----------|
| **goldberg2001** | **Missing author** (Boris V. Cherkassky omitted -- paper has 3 authors); **wrong year** (BibTeX says 1993, actual journal publication is 1996); **wrong volume** (says 59, actual 73); **wrong pages** (says 1-46, actual 129-174); BibTeX key says 2001 but paper is 1993/1996 | **MAJOR** |
| **cassis2025** | **Title and authors appear fabricated.** No paper titled "An Experimental Study of Negative-Weight Single-Source Shortest Paths Algorithms" by Cassis, Fischer, Haeupler exists. The closest real SEA 2025 paper is "Algorithm Engineering of SSSP with Negative Edge Weights" by Cassis, Karrenbauer, Nusser, and Rinaldi (DOI: 10.4230/LIPIcs.SEA.2025.10). Fischer and Haeupler are not authors of any SEA 2025 paper. | **CRITICAL -- LIKELY FABRICATED** |
| cherkassky1999 | Uses `@inproceedings` for a journal article (Mathematical Programming). Content is correct. | Minor (not cited in paper) |
| johnson1977 | Uses `@inproceedings` with `booktitle` for a JACM journal article. Content is correct. | Minor |

#### Additional BibTeX Issues

- `thorup1999`: Uses `@inproceedings` with `booktitle` but is a JACM journal article. Should be `@article` with `journal`.
- `thorup2004`: Same issue -- uses `@inproceedings` for a JCSS journal article.
- `hagerup2000`: Uses `@article` but is an ICALP conference proceedings paper.
- `meyer2001`: Uses `@article` with `journal` field for a SODA proceedings paper.
- 3 entries in sources.bib are not cited in the paper text: gabow2000, cherkassky1999, zwick2001.

---

## 5. Compilation (5/5)

The PDF (`research_paper.pdf`, 434 KB) exists and is well-formatted. The LaTeX source uses appropriate packages (amsmath, amsthm, algorithm, algorithmic, booktabs, natbib, pgfplots, tikz, subcaption, hyperref). All cross-references (\ref, \cite) appear to resolve correctly. The TikZ architecture diagram (Figure 1) renders cleanly. Tables are properly formatted with booktabs.

---

## 6. Writing Quality (4/5)

The paper is well-written overall:
- Professional academic tone throughout
- Clear problem motivation and positioning relative to prior work
- Good use of comparison tables (Tables 1-5) to organize information
- Honest acknowledgment of limitations (Section 8.4)
- The related work section is comprehensive and well-organized

Minor issues:
- The algorithm name "HiBRA" (Hierarchical Batch Relaxation with Adaptive Splitting) is misleading -- the algorithm does not perform batch relaxation or adaptive splitting. It is simply Dijkstra's algorithm with a modified heap. The name appears to describe something more complex than what is actually presented.
- The Discussion section (Section 8.3) attempts to reconcile with Haeupler et al.'s universal optimality result, but the explanation ("sidesteps this by changing the heap's internal structure") is hand-wavy and does not engage with the comparison sorting lower bound.

---

## 7. Figure Quality (3/5)

Six figures are provided in both PNG (300 DPI) and PDF format. They include:
- Proper axis labels, titles, and legends
- Log-log scales where appropriate
- Multiple series with distinct colors and markers
- Reference lines for theoretical models (e.g., c * n log n in Fig 1)

However:
- Figures use default matplotlib styling (standard color cycle, default gridlines, no custom font sizing)
- Fig 3 (speedup ratio) is confusing: the green bars (n=100,000) show ratios around 0.3-0.5, meaning HiBRA uses MORE operations than Dijkstra (binary heap), yet the paper frames this as HiBRA being comparable. The y-axis label says "Dijkstra Fib / HiBRA" but the actual bars appear to show "Dijkstra bin / HiBRA" ratios for the green series.
- Fig 4 (scalability) uses the same color (red/green) for two different algorithms on two different graph types, making it hard to distinguish series.
- Fig 5 (operation breakdown) shows data at n=100,000 but the visual encoding (grouped bars) makes comparison across algorithms difficult.

The figures are functional but do not meet the polish standards of a top-tier venue. Recommended: use a publication-quality style (e.g., seaborn's `paper` context), increase font sizes, use a colorblind-friendly palette, and add error bars where multiple trials exist.

---

## Detailed Technical Comments

### On the k-ary Fibonacci Heap (Major Issue)

The idea of parameterizing the cascading-cut threshold in a Fibonacci heap is interesting and valid as a data structure contribution. However, the asymptotic analysis is incorrect, as detailed in Section 2 above. The paper should:

1. **Correct the subtree size recurrence** to the cumulative-sum form: S(d) >= t + sum_{j=0}^{d-t} S(j)
2. **Derive the correct maximum degree**: Theta(log n / log r_t) where r_t is the largest root of x^t = x^{t-1} + ... + 1, which is Theta(log n) for any constant or slowly-growing t
3. **Acknowledge the sorting lower bound**: Any comparison-based priority queue performing n inserts and n extract-mins must use Omega(n log n) total comparisons, precluding o(log n) amortized extract-min
4. **Reposition the contribution** as a constant-factor improvement to the Fibonacci heap (reducing the degree from ~2.08 log_2 n to ~1.44 log_2 n), which is still a valid algorithmic engineering result

### On the Experimental Evaluation

The experiments are well-designed and comprehensive. The operation-counting framework is a useful contribution. However, the interpretation needs revision:
- The identical performance of HiBRA and standard Fibonacci heap at all tested sizes is not merely a "practical crossover" issue -- it reflects the fundamental fact that the improvement is at most a constant factor
- The complexity fitting (Table 4) showing power-law exponents ~1.07-1.09 is consistent with O(n log n) scaling on sparse graphs, not a sub-logarithmic improvement

### On Novelty

The paper positions itself as breaking the Fredman-Tarjan barrier, but:
- The idea of varying the cascading-cut threshold in Fibonacci heaps is straightforward and may exist in the data structures literature (e.g., work on thin heaps, rank-pairing heaps, and other Fibonacci heap variants)
- Without the claimed asymptotic improvement, the contribution reduces to a constant-factor optimization of a well-known data structure
- The paper should conduct a more thorough literature search on Fibonacci heap variants with modified cascading-cut rules

---

## Required Revisions

### Critical (Must Fix)

1. **Correct the complexity analysis.** The main theorems (Theorem 2 and Theorem 3) are incorrect. The paper must either:
   - (a) Prove that the k-ary Fibonacci heap achieves o(log n) amortized extract-min without violating the Omega(n log n) sorting lower bound (which appears impossible), or
   - (b) Retract the O(m + n log n / log log n) claim and restate the contribution as a constant-factor improvement

2. **Fix or remove the fabricated citation** (`cassis2025`). The paper "An Experimental Study of Negative-Weight Single-Source Shortest Paths Algorithms" by Cassis, Fischer, and Haeupler does not appear to exist. Replace with the actual SEA 2025 paper: "Algorithm Engineering of SSSP with Negative Edge Weights" by Cassis, Karrenbauer, Nusser, and Rinaldi (DOI: 10.4230/LIPIcs.SEA.2025.10), or remove the citation.

3. **Fix the goldberg2001 citation.** The correct reference is: Cherkassky, Goldberg, and Radzik, "Shortest paths algorithms: Theory and experimental evaluation," Mathematical Programming, vol. 73, pp. 129-174, 1996.

4. **Fix the crossover calculation.** The k-ary heap differs from standard Fibonacci heap at n >= 2^32 ≈ 4.3 x 10^9, not n >= 2^{2^32} ≈ 10^{1.3 x 10^9}.

### Major (Should Fix)

5. **Revise the title and framing.** If the asymptotic improvement cannot be recovered, the paper should not claim to "break" the Fredman-Tarjan barrier.

6. **Address the sorting lower bound.** Add a discussion of why the comparison sorting lower bound Omega(n log n) constrains the achievable amortized extract-min cost to Omega(log n).

7. **Improve figures** to publication quality: custom styling, larger fonts, colorblind-friendly palette, error bars.

8. **Fix BibTeX entry types.** Multiple entries use `@inproceedings` for journal articles or vice versa (thorup1999, thorup2004, johnson1977, hagerup2000, meyer2001).

### Minor

9. **Rename the algorithm.** "HiBRA" (Hierarchical Batch Relaxation with Adaptive Splitting) describes features the algorithm does not have. Consider a name reflecting what it actually does (e.g., "k-ary Fibonacci Dijkstra").

10. **Remove unused BibTeX entries** (gabow2000, cherkassky1999, zwick2001) or cite them.

11. **Correct Equation (1).** O(log n / log(log log n)) != O(log n / log log n). The inequality goes the other way.

---

## Citation Verification Summary

| # | BibTeX Key | Verified? | Issues |
|---|------------|-----------|--------|
| 1 | dijkstra1959 | VERIFIED | None |
| 2 | fredman1987 | VERIFIED | None |
| 3 | thorup1999 | VERIFIED | BibTeX type mismatch |
| 4 | thorup2004 | VERIFIED | BibTeX type mismatch |
| 5 | pettie2005 | VERIFIED | None |
| 6 | pettie2002mst | VERIFIED | None |
| 7 | bernstein2022 | VERIFIED | None |
| 8 | bringmann2023 | VERIFIED | Pages omitted |
| 9 | chen2022 | VERIFIED | Minor: author surname abbreviated |
| 10 | haeupler2024 | VERIFIED | None |
| 11 | duan2025 | VERIFIED | None |
| 12 | duan2023 | VERIFIED | Pages omitted |
| 13 | hagerup2000 | VERIFIED | BibTeX type mismatch |
| 14 | bellman1958 | VERIFIED | None |
| 15 | goldberg2001 | **INCORRECT** | Missing author, wrong year/volume/pages |
| 16 | gabow2000 | VERIFIED | Not cited in paper |
| 17 | cherkassky1999 | VERIFIED | BibTeX type mismatch; not cited |
| 18 | johnson1977 | VERIFIED | BibTeX type mismatch |
| 19 | zwick2001 | VERIFIED | Not cited in paper |
| 20 | meyer2001 | VERIFIED | BibTeX type mismatch |
| 21 | cassis2025 | **FABRICATED** | Title and authors do not match any real paper |

---

## Overall Assessment

The paper is well-written, comprehensive in its experimental evaluation, and honest about practical limitations. The experimental infrastructure (operation counting, graph generators, benchmark framework) represents solid work. However, the central theoretical contribution -- the claimed O(m + n log n / log log n) SSSP bound -- contains a **fundamental mathematical error** in the amortized analysis of the k-ary Fibonacci heap. The claimed extract-min cost of O(log n / log log n) would violate the comparison sorting lower bound of Omega(n log n). The correct analysis shows only a constant-factor improvement over standard Fibonacci heaps.

Additionally, one citation (cassis2025) appears to be fabricated, and another (goldberg2001) has multiple factual errors.

**Verdict: REVISE.** The paper requires major corrections to its theoretical analysis, citation accuracy, and framing before it can be considered for publication. The experimental evaluation and writing quality are strengths that should be preserved in a revision.
