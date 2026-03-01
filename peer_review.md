# Peer Review: Hop-Guided Frontier Reduction for Single-Source Shortest Paths

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-03-01
**Paper:** "Hop-Guided Frontier Reduction for Single-Source Shortest Paths"

---

## Scores

| Criterion | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| **1. Completeness** | 5 | All required sections present and well-structured |
| **2. Technical Rigor** | 2 | **CRITICAL FLAW: The claimed bound O(m(log log n)^2 + n log n log log n) is strictly worse than Dijkstra + Fibonacci heap's O(m + n log n) in ALL regimes** |
| **3. Results Integrity** | 3 | Experimental data is real and matches CSV files; figures match data; but empirical advantages reflect Python implementation artifacts, not algorithmic improvements |
| **4. Citation Accuracy** | 1 | 11 of 30 citations have errors: 2 fabricated, 9 with incorrect metadata |
| **5. Compilation** | 5 | PDF compiles without errors; well-formatted output |
| **6. Writing Quality** | 4 | Professional academic tone, clear pseudocode, logical flow; loses a point for misleading framing of results |
| **7. Figure Quality** | 4 | Publication-quality figures using seaborn; proper labels, legends, error bars, color palettes |

---

## Overall Verdict: REVISE

---

## Detailed Review

### 1. Completeness (5/5)

The paper contains all required sections: Abstract, Introduction, Related Work (embedded in Introduction), Background & Preliminaries, Method, Correctness, Complexity Analysis, Experimental Setup, Results, Discussion, Conclusion, and References. The structure follows standard TCS conference formatting. The comparison table (Table 3) covers 12 algorithms as required. The paper includes 6 high-quality figures, formal pseudocode for all subroutines (Algorithms 1-3), theorem statements with proofs, and a thorough experimental evaluation across 11 graph families.

### 2. Technical Rigor (2/5)

**CRITICAL ISSUE: The main theoretical result does not achieve the paper's stated goal.**

The paper claims to solve SSSP in "asymptotically fewer operations than the current best known bound." However, the claimed bound of O(m(log log n)^2 + n log n log log n) is **strictly asymptotically worse** than the classical Dijkstra + Fibonacci heap bound of O(m + n log n) (Fredman & Tarjan 1987) **for every possible graph density**:

- **Sparse graphs (m = O(n)):** Paper gives O(n log n log log n) vs. Dijkstra's O(n log n). **Dijkstra is better by factor log log n.**
- **Medium density (m = Theta(n log n)):** Paper gives O(n log n (log log n)^2) vs. Dijkstra's O(n log n). **Dijkstra is better by factor (log log n)^2.**
- **Dense graphs (m = Theta(n^2)):** Paper gives O(n^2 (log log n)^2) vs. Dijkstra's O(n^2). **Dijkstra is better by factor (log log n)^2.**

This is because (log log n)^2 >= 1 for all n, so m(log log n)^2 >= m always, and n log n log log n >= n log n always. **The paper's bound is dominated term-by-term by Dijkstra's 1987 result.**

The paper's comparison against DMMSY and Duan-Mao is technically valid (the m-factor (log log n)^2 is smaller than log^{2/3} n or sqrt(log n)), but this comparison is irrelevant since Dijkstra outperforms all three algorithms in the regimes where this paper claims advantages. Specifically:

- For m = Omega(n log n / log log n) where the paper claims its bound simplifies to O(m(log log n)^2): Dijkstra achieves O(m), which is strictly better.
- The paper does NOT break the sorting barrier. DMMSY's O(m log^{2/3} n) genuinely eliminates the n log n term for sparse graphs; this paper re-introduces it (multiplied by log log n) due to running Dijkstra cleanup at every recursion level.

**Root cause of the weakness:** The algorithm runs Dijkstra on each sub-problem at each of the O(log log n) recursion levels. While the hop-guided partition eliminates comparisons at the partition step, the accumulated Dijkstra cleanups cost O((n log n + m) * log log n), which dominates the savings from the partition.

The proof structure itself (feasibility invariant, hop-ordering lemma, inductive correctness, edge-charging argument) is mathematically sound. The recurrence analysis and its solution are correct. The bound O(m(log log n)^2 + n log n log log n) does follow from the algorithm as described. **The mathematics is correct; the result simply does not improve upon the state of the art.**

### 3. Results Integrity (3/5)

**Positive:**
- The experimental data in `results/novel_results.csv`, `results/baselines.csv`, and `results/stress_test.csv` is internally consistent.
- Tables in the paper (comparisons/m ratios, wall-clock times, log-log regression slopes) match the values in `results/empirical_validation.md`, which appear to be correctly computed from the CSV data.
- Correctness verification against Bellman-Ford is reported for all runs.
- Stress test results on adversarial families are included and documented.

**Concerns:**
- The empirical advantage of HopGuidedSSSP over Dijkstra (e.g., 2-4x faster in wall-clock time) is a **Python implementation artifact**. Python's Fibonacci heap implementation involves heavy pointer-chasing overhead that disproportionately penalizes Dijkstra. The theoretical analysis shows HopGuidedSSSP should be *slower* than Dijkstra. The paper should acknowledge this explicitly rather than presenting the wall-clock results as evidence of algorithmic superiority.
- The paper's claim (Section 6.7) that "HopGuidedSSSP begins outperforming Dijkstra at n ~ 500 for sparse graphs" is misleading. This crossover reflects implementation-specific constant factors in Python, not algorithmic complexity.
- Graph sizes tested (n <= 100,000) are acknowledged as insufficient to distinguish polylog-log factors, which is honest.

### 4. Citation Accuracy (1/5)

**11 of 30 citations have errors. This is unacceptable for a publication-quality paper.**

#### Citation Verification Report

| # | Key | Status | Details |
|---|-----|--------|---------|
| 1 | `dijkstra1959` | **VERIFIED** | All fields correct |
| 2 | `bellman1958` | **VERIFIED** | All fields correct |
| 3 | `ford1956` | **VERIFIED** | All fields correct |
| 4 | `johnson1977` | **VERIFIED** | All fields correct |
| 5 | `fredman1987` | **VERIFIED** | All fields correct |
| 6 | `gabow1989` | **INCORRECT** | Conflates STOC 1988 conference version ("Almost-Optimum Speed-ups of Algorithms for Bipartite Matching and Related Problems") with SIAM J. Comput. 1989 journal version ("Faster Scaling Algorithms for Network Problems"). Title, year (1989 vs 1988), STOC edition (21st vs 20th), pages (515-523 vs 514-527), and DOI are all inconsistent. |
| 7 | `ahuja1990` | **VERIFIED** | All fields correct |
| 8 | `goldberg1993` | **VERIFIED** | All fields correct |
| 9 | `goldberg1995` | **VERIFIED** | All fields correct (not cited in paper text) |
| 10 | `thorup1999` | **INCORRECT** | Paper was presented at FOCS 1997 (38th), not FOCS 1999 (40th). Title matches JACM 1999 journal version. DOI 10.1109/SFFCS.1999.814570 is from FOCS 1999 proceedings, not FOCS 1997. Correct DOI: 10.1109/SFCS.1997.646088. |
| 11 | `hagerup2000` | **VERIFIED** | All fields correct |
| 12 | `thorup2004` | **VERIFIED** | All fields correct |
| 13 | `pettie2005` | **INCORRECT** | DOI is wrong: 10.1137/S0097539702418819 returns 404. Correct DOI: 10.1137/S0097539702419650. Other fields correct. (Not cited in paper text.) |
| 14 | `pettie2008` | **FABRICATED** | The title "Sensitivity analysis of minimum spanning trees and shortest path trees" belongs to a 1982 paper by R.E. Tarjan in *Information Processing Letters*, not by Seth Pettie. Pettie's related work was published in JGAA (2015), not Algorithmica (2008). The volume, pages, journal, and author attribution are all wrong. This entry appears to be hallucinated. (Not cited in paper text.) |
| 15 | `bernstein2022` | **VERIFIED** | All fields correct |
| 16 | `bringmann2023` | **VERIFIED** | All fields correct |
| 17 | `duan2023` | **INCORRECT** | Wrong title. Actual title: "A Randomized Algorithm for Single-Source Shortest Path on Undirected Real-Weighted Graphs" (arXiv:2307.04139). The bib title "Single-source shortest paths and strong connectivity in near-linear time" does not match. |
| 18 | `haeupler2024` | **VERIFIED** | All fields correct (minor: diacritics omitted, acceptable in BibTeX) |
| 19 | `fineman2024` | **VERIFIED** | All fields correct |
| 20 | `dmmsy2025` | **VERIFIED** | All fields correct |
| 21 | `duanmao2026` | **INCORRECT** | Wrong title: actual title is "A Faster Directed Single-Source Shortest Path Algorithm." Wrong authors: lists only "Duan, Ran and Mao, Jiayi" but actual authors are Ran Duan, **Xiao** Mao (not Jiayi), Xinkai Shu, and Longhui Yin (4 authors, not 2). |
| 22 | `yan2025` | **VERIFIED** (with caveat) | Paper exists by Shuyi Yan. Title is paraphrased: actual title is "Lossless Derandomization for Undirected Single-Source Shortest Paths and Approximate Distance Oracles." Missing arXiv ID. (Not cited in paper text.) |
| 23 | `huang2025` | **INCORRECT** | Wrong title: actual title is "Faster single-source shortest paths with negative real weights via proper hop distance." Wrong authors: "Shang-En Huang" should be **Yufan Huang**, "Ce Jin" should be **Peter Jin**. Only Kent Quanrud is correct. |
| 24 | `sea2025` | **INCORRECT** | Wrong title: actual title is "Algorithm Engineering of SSSP with Negative Edge Weights." Wrong author: "Rinaldi, Marco" should be **Paolo Luigi Rinaldi**. |
| 25 | `hoog2025` | **INCORRECT** | Wrong venue: claims STOC 2025, but actually published at **ESA 2025** (33rd Annual European Symposium on Algorithms). Paper does not appear on STOC 2025 accepted papers list. Minor title discrepancy ("A simple" vs "Simpler"). |
| 26 | `khanna2026` | **LIKELY FABRICATED** | No evidence of this paper existing. No arXiv preprint found. Sanjeev Khanna and Zhao Song have no known collaboration on shortest paths with negative weights. The closest real paper on this topic (arXiv:2602.16153, "Bellman-Ford in Almost-Linear Time for Dense Graphs") is by George Z. Li, Jason Li, and Junkai Zhang -- completely different authors. |
| 27 | `castro2025` | **INCORRECT** | Wrong title: actual title is "Implementation and Brief Experimental Analysis of the Duan et al. (2025) Algorithm for Single-Source Shortest Paths." All author initials wrong: "G." should be **Lucas**, "A." should be **Thailsson**, "B." should be **Rosiane**. Venue "Proceedings" is misleadingly vague (it's an arXiv preprint). |
| 28 | `dimacs2006` | **VERIFIED** | All fields correct |
| 29 | `bringmann2025ldd` | **VERIFIED** | All fields correct (trivial singular/plural difference in title) |
| 30 | `chen2022maxflow` | **VERIFIED** | All fields correct |

**Summary: 19 verified, 9 incorrect metadata, 2 fabricated/likely fabricated. All in-text \citep commands resolve to entries in sources.bib.**

### 5. Compilation (5/5)

The PDF (`research_paper.pdf`) exists and was compiled successfully. The paper uses standard LaTeX packages (amsmath, algorithm, booktabs, natbib, pgfplots, tikz, hyperref) and compiles cleanly. TikZ diagrams for the architecture overview and partition example render correctly. All 6 figures are included via `\includegraphics` and display properly.

### 6. Writing Quality (4/5)

**Strengths:**
- Professional academic tone throughout
- Clear and well-organized pseudocode (Algorithms 1-3)
- Proper theorem/lemma/proof structure
- Good notation table (Table 1)
- Thorough experimental methodology description
- Honest acknowledgment of limitations (Section 7.1)

**Weaknesses:**
- **Misleading framing:** The abstract and introduction frame the result as an improvement upon "all prior bounds for sufficiently dense graphs," but fail to prominently state that the bound is always worse than Dijkstra + Fibonacci heap (1987). The comparison in Corollary 3.4 against Duan-Mao is technically correct but gives a misleading impression of progress.
- The paper should explicitly state in the abstract and introduction that the proposed bound does not improve upon the classical O(m + n log n) Dijkstra bound.
- The Introduction's first paragraph claims the result "achieves... time in the comparison-addition model" without contextualizing that this is worse than the 1987 bound.

### 7. Figure Quality (4/5)

Figures are publication-quality:
- Proper seaborn styling with distinct color palettes (blue/red/green)
- Axis labels with units (ms, microseconds, KB)
- Legends clearly identifying all three algorithms
- Error bars on comparative_time_vs_n and comparative_crossover
- Log-scale axes where appropriate
- Heatmap with diverging color scale

Minor issues:
- The comparative_ops_vs_n figure (3-panel) is somewhat compressed horizontally
- The heatmap y-axis labels (m/n ratios) could be more readable

---

## Critical Issues Requiring Revision

### Issue 1: The Main Theoretical Claim Is Invalid (BLOCKING)

The paper's claimed bound of O(m(log log n)^2 + n log n log log n) does not improve upon Dijkstra + Fibonacci heap's O(m + n log n) for any graph density. This is the paper's central contribution and it fails to deliver. The algorithm re-introduces the sorting barrier through Dijkstra cleanups at each recursion level.

**Required action:** Either:
(a) Modify the algorithm to eliminate the Dijkstra cleanup cost (e.g., replace with a sub-O(n log n) method), OR
(b) Reframe the paper as improving upon frontier-reduction methods (DMMSY, Duan-Mao) in a specific density regime, while explicitly acknowledging the result does not improve upon the classical Dijkstra bound. This would significantly reduce the paper's contribution but would be honest.

### Issue 2: Citation Errors (BLOCKING)

11 of 30 citations have errors, including 2 fabricated entries. This is far below publication standards.

**Required action:**
- **Delete** `pettie2008` (fabricated) and `khanna2026` (likely fabricated), and remove any in-text references
- **Correct** `duanmao2026`: fix title to "A Faster Directed Single-Source Shortest Path Algorithm", fix authors to Ran Duan, Xiao Mao, Xinkai Shu, and Longhui Yin
- **Correct** `duan2023`: fix title to "A Randomized Algorithm for Single-Source Shortest Path on Undirected Real-Weighted Graphs"
- **Correct** `gabow1989`: either cite as STOC 1988 (title "Almost-Optimum Speed-ups...") or as SIAM J. Comput. 1989 (title "Faster Scaling Algorithms..."), not a hybrid
- **Correct** `thorup1999`: fix year to 1997, booktitle to 38th FOCS, DOI to 10.1109/SFCS.1997.646088
- **Correct** `pettie2005`: fix DOI to 10.1137/S0097539702419650
- **Correct** `huang2025`: fix title to "Faster single-source shortest paths with negative real weights via proper hop distance", fix authors to Yufan Huang, Peter Jin, Kent Quanrud
- **Correct** `sea2025`: fix title to "Algorithm Engineering of SSSP with Negative Edge Weights", fix author to Paolo Luigi Rinaldi
- **Correct** `hoog2025`: fix venue from STOC 2025 to ESA 2025
- **Correct** `castro2025`: fix title to "Implementation and Brief Experimental Analysis of the Duan et al. (2025) Algorithm for Single-Source Shortest Paths", fix authors to Lucas Castro, Thailsson Clementino, Rosiane de Freitas

### Issue 3: Misleading Empirical Comparison

The wall-clock performance advantage of HopGuidedSSSP over Dijkstra (2-4x faster) is a Python implementation artifact. Fibonacci heaps in Python suffer extreme pointer-chasing overhead. The paper should:
- Explicitly state that wall-clock advantages are implementation-specific, not algorithmic
- Consider implementing in C/C++ for a fairer comparison, or at minimum use `heapq` (binary heap) as the Dijkstra baseline
- Remove or qualify the crossover analysis claim ("outperforms Dijkstra at n ~ 500")

---

## Minor Issues

1. **Table 3 (DMSY row):** Lists the undirected SSSP result by Duan, Mao, Shu, Yin (2023) but the cited entry `duan2023` has incorrect metadata (see citation issues above).

2. **Section 4 (Correctness), Lemma 4.2 (Hop-ordering):** The proof states "h(v_t) <= h(v_{t+1}) + 1 for each edge." This is correct for unweighted BFS but the direction should be clarified: on a directed graph, BFS from s gives h(v) = min hops from s to v, and for edge (v_t, v_{t+1}) on a shortest path, h(v_{t+1}) <= h(v_t) + 1 (not the reverse). The inequality in the proof is stated backwards.

3. **Complexity analysis (Section 5):** The edge-charging argument in Equation (1) states each edge participates in correction at "at most R = O(log log n) levels." This should be proved more formally -- the claim that an edge appears in exactly one sub-problem per level (due to vertex-disjointness of blocks) is correct but stated without proof.

4. **Section 6.7 (Family-Specific Performance):** Grid graphs have hop-diameter O(sqrt(n)), not O(n). The text correctly states O(sqrt(n)) for grids but then groups it with high-diameter graphs at O(n). These should be distinguished more carefully.

5. **Uncited entries:** `goldberg1995`, `pettie2005`, `pettie2008`, and `yan2025` appear in `sources.bib` but are never cited in the paper text. Remove uncited entries to keep the bibliography clean.

---

## Summary

The paper presents a well-structured and clearly written algorithm for SSSP using hop-guided frontier reduction. The writing quality is high, the experimental methodology is thorough, and the figures are publication-quality. However, the paper suffers from two critical and blocking issues:

1. **The main theoretical contribution is invalid:** The claimed bound O(m(log log n)^2 + n log n log log n) is strictly worse than Dijkstra + Fibonacci heap's O(m + n log n) for all graph densities. The algorithm does not achieve the paper's stated goal of solving SSSP in asymptotically fewer operations than O(m + n log n).

2. **Severe citation problems:** 11 of 30 bibliography entries contain errors, including 2 fabricated entries. This is unacceptable for any publication venue.

These issues must be addressed before the paper can be considered for acceptance. The most constructive path forward would be to either find a way to eliminate the Dijkstra cleanup cost at each recursion level (which would yield a genuine improvement), or to substantially reframe the contribution as an improvement within the frontier-reduction paradigm rather than an improvement over the classical SSSP bound.
