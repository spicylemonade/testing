# Peer Review: DAMS-SSSP — A Density-Adaptive Multi-Scale Algorithm for Single-Source Shortest Paths Below the Sorting Barrier

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standards)
**Date:** 2026-03-02
**Paper:** `research_paper.tex` / `research_paper.pdf`

---

## Criterion Scores

| # | Criterion | Score (1–5) | Summary |
|---|-----------|:-----------:|---------|
| 1 | Completeness | **4** | All required sections present; proofs are only sketched |
| 2 | Technical Rigor | **2** | Central complexity proof has a critical gap |
| 3 | Results Integrity | **4** | Data matches; one metric (memory) is unreliable |
| 4 | Citation Accuracy | **3** | 4 of 21 citations have metadata errors |
| 5 | Compilation | **4** | PDF exists and compiles |
| 6 | Writing Quality | **4** | Professional tone, clear structure, honest limitations |
| 7 | Figure Quality | **4** | Publication-quality; proper labels, legends, error bars |

**Overall Verdict: REVISE**

---

## 1. Completeness (4/5)

All required sections are present and well-structured:

- Abstract, Introduction (§1), Related Work (§2), Background/Preliminaries (§3), Method (§4), Experimental Setup (§5), Results (§6), Discussion (§7), Conclusion (§8), References.
- Formal definitions (SSSP, comparison-addition model) are provided.
- Two algorithm boxes with pseudocode (Algorithm 1: DAMS-SSSP, Algorithm 2: BucketedDijkstra).
- Notation table (Table 1), hyperparameter table (Table 2), multiple results tables.
- Comprehensive experimental evaluation: 80 synthetic benchmarks, 16 realistic instances, 88 ablation configurations.

**Deduction:** The correctness proof (Theorem 2) is stated but only informally argued via invariants (§4.6, lines 501–508). The complexity proof (Theorem 1) is explicitly labeled a "proof sketch." For a top-tier venue claiming a new complexity result, full formal proofs are expected, not sketches. A dedicated proofs section or appendix is needed.

---

## 2. Technical Rigor (2/5)

This is the weakest aspect of the paper and the primary reason for the REVISE verdict.

### 2a. Critical Gap in the Complexity Proof

**Theorem 1** claims O(m√(log n) + n log n). The proof sketch (lines 478–493) asserts:

> "Each edge is relaxed once: O(m) additions and comparisons" [per scale]

This claim is **not substantiated** by the algorithm as written. Algorithm 2 (BucketedDijkstra) explicitly allows re-processing of buckets:

- Line 9–10: "if bucket[cur] is non-empty: continue (re-process current bucket)"
- Line 4–5: A vertex v whose distance improves is re-inserted into bucket ⌊d(v)/β⌋ mod B, which may be a bucket the pointer has already visited or is currently processing.

In standard Dial's algorithm, correctness and linear-time guarantees come from bounded integer weights ensuring monotone bucket progress. In DAMS, the modular bucket assignment (mod B) means vertices can be inserted into buckets that are currently being processed, leading to repeated extractions. The paper does not bound the number of times a vertex can be re-extracted per scale.

**Worst-case analysis:** With reduced weights in [0, δ_{j-1}) and bucket width β_j = δ_j/√n, a vertex can move across up to δ_{j-1}/β_j = 2√n bucket positions per scale. Each re-extraction triggers processing of all outgoing edges. This suggests O(n√n) vertex extractions per scale in the worst case, giving O(m√n · √(log n)) total — far worse than claimed.

The paper may intend an amortized argument (each vertex's total distance decrease is bounded, limiting re-insertions), but no such argument is presented.

### 2b. Unexplained n log n Term

The proof sketch derives "O(K·(m+n)) = O(m√(log n) + n√(log n))" from the scale loop, plus "O(m) for 3 [cleanup] passes." Neither source produces an n log n term. Yet Theorem 1 claims O(m√(log n) + **n log n**). Where does the n log n come from? This discrepancy is never explained.

If the actual complexity is O(m√(log n) + n√(log n)), the result is strictly better than stated. If additional work (e.g., initialization, weight scanning) requires O(n log n), this must be identified and justified.

### 2c. Novelty Relative to State of the Art

Even accepting the claimed bound O(m√(log n) + n log n), this is **strictly weaker** than Duan et al. 2026's O(m√(log n)). The additive n log n term means DAMS offers no improvement for sparse graphs (m = O(n)). The paper acknowledges this (§7.1, Table 6), but the title "Below the Sorting Barrier" is only valid for m = Ω(n√(log n)), which should be more prominently stated.

### 2d. Power-Law Graph Anomaly

The benchmark data for power-law graphs shows only 1–10 total operations at all sizes (e.g., Dijkstra+Binary at n=100K: 1 comparison, 0 additions, 2 heap ops). This indicates the source vertex has no reachable vertices, meaning the generated graphs are nearly or completely disconnected from the source. This data anomaly is never discussed in the paper. While the paper wisely excludes power-law from detailed tables, it should acknowledge the graph-generation issue.

### 2e. Memory Benchmark Unreliability

The memory comparison figure shows 0 KB peak RSS for DAMS, Duan, and Dijkstra+Binary at most sizes. Any algorithm processing 100K vertices and 300K edges cannot have 0 KB peak memory. The `resource.getrusage()` tracking is clearly not capturing incremental memory correctly (likely measuring delta rather than absolute RSS). This undermines the memory claims in §6.5.

---

## 3. Results Integrity (4/5)

### Verified Claims

All numerical values in paper tables were cross-checked against the actual JSON data files:

| Paper Table | Data Source | Match? |
|-------------|-----------|--------|
| Table 3 (ops at n=100K) | `results/operation_analysis.json` | **Exact match** for all 12 values |
| Table 4 (R² values) | `results/operation_analysis.json` | **Exact match** for all 12 values |
| Table 5 (realistic benchmarks) | `results/realistic_benchmarks.json` | **Exact match** for all 16 values |
| Table 6 (ablation) | `results/ablation_study.json` | Consistent |

### Honest Reporting

The paper commendably acknowledges several limitations:
- DAMS does not outperform Dijkstra in practice (§7.2)
- R² values cannot distinguish sub-logarithmic factors at feasible sizes (§7.4, Table 4)
- The crossover point is "far beyond n = 10^30" (Figure 8)
- Consistent with Castro et al.'s findings that Dijkstra is 3–4× faster (§7.2)

### Minor Issues

- The paper claims DAMS is "2–5× slower" than Dijkstra+Binary (§6.1, line 602), but on grid graphs at n=100K the ratio is ~7× (3.30s / 0.47s). The stated range understates the gap.
- The paper claims DAMS is "consistently faster than Dijkstra + Fibonacci heap" — this is true for sparse and worst-case, but for grid n=100K the times are nearly identical (3.30s vs 3.33s). "Competitive with" would be more accurate for grid graphs.

**Deduction:** -1 for unreliable memory data and slightly overstated performance claims.

---

## 4. Citation Accuracy (3/5)

### Methodology

All 21 entries in `sources.bib` were verified via web search (Google Scholar, arXiv, ACM DL, Springer, IEEE, Semantic Scholar, DBLP).

All `\cite{}` commands in the paper reference existing entries in `sources.bib`. No orphaned or missing citations were found.

### Citation Verification Report

| # | Citation Key | Verdict | Details |
|---|-------------|---------|---------|
| 1 | `dijkstra1959` | **VERIFIED** | Title, author, year, journal, volume, pages all correct |
| 2 | `fredmantarjan1987` | **VERIFIED** | All fields correct. DOI: 10.1145/28869.28874 |
| 3 | `driscoll1988` | **VERIFIED** | All fields correct. DOI: 10.1145/50087.50096 |
| 4 | `thorup1999` | **VERIFIED** | All fields correct. DOI: 10.1145/316542.316548 |
| 5 | `goldberg2001` | **ISSUE** | URL `https://link.springer.com/chapter/10.1007/3-540-45643-0_10` points to Pettie, Ramachandran & Sridhar (ALENEX 2002), NOT Goldberg. Correct URL: `https://link.springer.com/chapter/10.1007/3-540-44676-1_19`. Entry type should be `@inproceedings` (ESA 2001) or `@techreport`, not `@article`. |
| 6 | `meyersanders2003` | **VERIFIED** | All fields correct |
| 7 | `pettieramachandran2005` | **VERIFIED** | All fields correct. DOI: 10.1137/S0097539702419650 |
| 8 | `bernstein2022` | **VERIFIED** | Title, authors, year, venue (FOCS 2022), pages, arXiv all correct |
| 9 | `bringmann2023` | **VERIFIED** | All fields correct. DOI: 10.1109/FOCS57990.2023.00038 |
| 10 | `duan2023` | **VERIFIED** | All fields correct |
| 11 | `haeupler2024` | **VERIFIED** | All fields correct including diacritics. DOI: 10.1109/FOCS61266.2024.00125 |
| 12 | `duan2025` | **VERIFIED** | All fields correct. STOC 2025 Best Paper. DOI: 10.1145/3717823.3718179 |
| 13 | `duan2026` | **VERIFIED** | arXiv preprint 2602.07868, submitted Feb 2026. All fields correct |
| 14 | `castro2025` | **VERIFIED** | arXiv preprint 2511.03007. All fields correct |
| 15 | `bellmanford1958` | **VERIFIED** | All fields correct |
| 16 | `johnson1977` | **VERIFIED** | All fields correct. DOI: 10.1145/321992.321993 |
| 17 | `goldbergradzik1993` | **ISSUE** | Author first name wrong: "Thomas Radzik" should be **"Tomasz Radzik"**. Tomasz is the correct Polish name (confirmed via King's College London faculty page and ScienceDirect). |
| 18 | `thorup2004` | **ISSUE** | **Three errors:** (1) Year should be **2003** not 2004 — this is a STOC 2003 paper. (2) Venue should be **35th** STOC, not 36th. (3) DOI `10.1145/1007352.1007374` resolves to a completely different paper ("Dictionary matching..." from STOC 2004). Correct DOI: **10.1145/780542.780566**. |
| 19 | `barabasialbert1999` | **VERIFIED** | All fields correct. DOI: 10.1126/science.286.5439.509 |
| 20 | `bertsekas1992` | **ISSUE** | Entry type is `@book` with `publisher={Computational Optimization and Applications}`. This is actually a **journal article** in *Computational Optimization and Applications*, Vol. 1, pp. 7–66. Should be `@article` with `journal={...}`. DOI: 10.1007/BF00247653 |
| 21 | `dial1969` | **VERIFIED** | All fields correct. DOI: 10.1145/363269.363610 |

### Summary

- **17 of 21** citations fully verified
- **4 citations** have errors:
  - `goldberg2001`: incorrect URL (points to wrong paper)
  - `goldbergradzik1993`: author first name wrong (Thomas → Tomasz)
  - `thorup2004`: wrong year, wrong conference number, wrong DOI
  - `bertsekas1992`: wrong BibTeX entry type
- **0 fabricated citations** — all 21 papers genuinely exist
- All in-text `\cite{}` commands resolve to valid bib entries

The errors are metadata mistakes, not fabrication. However, the `thorup2004` entry has three independent errors including a DOI resolving to a completely different paper, which is a significant concern.

---

## 5. Compilation (4/5)

- `research_paper.pdf` exists in the repository (confirmed via file listing).
- The LaTeX source uses standard packages (amsmath, algorithm, pgfplots, natbib, booktabs, hyperref) and should compile with standard pdfLaTeX + BibTeX toolchain.
- TikZ architecture diagram (Figure 1) is generated inline.
- External figures referenced via `\includegraphics` all exist in `figures/`.

**Deduction:** -1 because I cannot fully verify error-free compilation without running the toolchain; the presence of a correct-looking PDF is strong evidence.

---

## 6. Writing Quality (4/5)

### Strengths

- Professional academic tone throughout.
- Logical flow: problem → prior work → approach → experiments → discussion → conclusion.
- Excellent Related Work section (§2) covering classical, integer-weight, sub-barrier, negative-weight, and practical SSSP algorithms.
- Honest limitations section (§7.4) with five explicitly enumerated weaknesses.
- Clear notation table and hyperparameter table.
- Proper use of theorem/proof environments.
- Well-integrated citations throughout the narrative.

### Weaknesses

- The title "Below the Sorting Barrier" is misleading — the algorithm only beats the barrier when m = Ω(n√(log n)). The qualification should appear in the title or at least the abstract.
- The abstract says "achieving O(m√(log n) + n log n)" without immediately clarifying that this is weaker than Duan et al. 2026's pure O(m√(log n)).
- "Proof sketch" is insufficient for the main theorem at top-tier venues. At minimum, the sketchy steps should be flagged as conjectures or the argument made rigorous in an appendix.
- Section 6.1 (line 602): the claim DAMS is "2–5× slower" than binary-heap Dijkstra is inaccurate (the range extends to ~7× on grid graphs).

---

## 7. Figure Quality (4/5)

### Assessment

Figures are **publication-quality** — clearly NOT default matplotlib styling:

- **Color palette:** Distinct, colorblind-friendly colors (blue, green, orange, red) with different markers (circles, squares, triangles, diamonds).
- **Axes:** Properly labeled with units; log-log scaling where appropriate.
- **Legends:** Present and clear in all figures.
- **Error bars:** Standard deviation bars included in scaling plots.
- **Theoretical overlays:** Dashed reference curves for O(m + n log n), O(m log^{2/3} n), O(m√(log n)) fitted to data.
- **Annotations:** Realistic comparison bar charts include numeric value labels.
- **Ablation figures:** Use red X markers to indicate correctness failures — an effective visual convention.

### Minor Issues

- `realistic_comparison.png` is extremely wide (7160×1538 pixels) — may render poorly in single-column layout. Consider a 2×2 grid arrangement.
- `memory_comparison.png` shows most algorithms at 0 KB (data tracking issue, not visualization issue), making the comparison uninformative.
- The crossover analysis figure caption says "ratio decreases from ~5× at n=1,000 to ~4.5× at n=100,000 on sparse" but the actual sparse line shows a slight increase at n=100K in the figure.

---

## Overall Verdict: **REVISE**

### Rationale

The paper is well-written, professionally structured, and commendably honest about its limitations. The experimental evaluation is thorough and the data integrity is excellent. However, several critical issues prevent acceptance:

1. **The central complexity proof has a fundamental gap.** The O(m) per-scale claim is not justified by the algorithm, which allows unbounded re-processing of vertices within a scale. This is the core theoretical contribution and it is not rigorously established.

2. **Four bibliography entries contain errors**, including one (`thorup2004`) with three independent metadata errors and a DOI resolving to the wrong paper entirely.

3. **The claimed novelty is limited.** O(m√(log n) + n log n) is strictly weaker than Duan et al. 2026's O(m√(log n)). The paper frames this as "matching" the state of the art, but it is a weaker result with an additive n log n term.

4. **Memory benchmarks are unreliable** (showing 0 KB for most algorithms).

### Required Revisions

1. **Provide a complete, rigorous proof of Theorem 1.** Specifically:
   - Bound the number of times a vertex can be extracted from the BucketPQ per scale.
   - Account for the modular bucket wraparound and its effect on monotone progress.
   - Explain the source of the additive n log n term, or revise the bound.
   - Consider providing the proof in an appendix if space-constrained.

2. **Fix all bibliography errors:**
   - `goldberg2001`: Correct URL to `https://link.springer.com/chapter/10.1007/3-540-44676-1_19`
   - `goldbergradzik1993`: Change "Thomas" to "Tomasz"
   - `thorup2004`: Change year to 2003, venue to "35th Annual ACM STOC", DOI to `10.1145/780542.780566`
   - `bertsekas1992`: Change `@book` to `@article`, `publisher` to `journal`

3. **Temper the title and abstract.** Either:
   - Add the density qualifier to the title (e.g., "...Below the Sorting Barrier for Dense Graphs"), or
   - State the density requirement (m = Ω(n√(log n))) prominently in the abstract.

4. **Fix the "2–5× slower" claim** in §6.1 to "2–7× slower" to accurately reflect the grid graph results.

5. **Address the memory benchmark issue.** Either fix the `resource.getrusage()` tracking to report accurate peak RSS, or remove the memory comparison and Figure 9 entirely.

6. **Discuss the power-law graph connectivity anomaly.** Acknowledge that the BA-model graphs have poor reachability from the chosen source vertex, explaining the near-zero operation counts.

7. **Revise the crossover analysis figure caption** to accurately describe the trend shown in the figure.

### Positive Aspects

- The paper's honesty about practical performance is exemplary and should be preserved.
- The cross-domain design methodology (epsilon-scaling from auction algorithms, bucketing from Dial/Delta-stepping) is a genuinely interesting contribution.
- The ablation study is thorough and well-designed.
- The experimental methodology (warmup runs, GC control, operation counting) follows best practices.
- The algorithmic framework, while needing a rigorous proof, represents a plausible and simpler alternative to BMSSP-based approaches.

---

*Review generated by automated peer reviewer applying Nature/NeurIPS publication standards.*
