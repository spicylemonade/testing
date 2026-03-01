# Peer Review: BALT-H: Bidirectional ALT with Hub Acceleration for Faster Point-to-Point Shortest Paths

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standards)
**Date:** 2026-03-01

---

## Criterion Scores

| # | Criterion | Score (1-5) | Summary |
|---|-----------|:-----------:|---------|
| 1 | Completeness | 4 | All required sections present with good structure |
| 2 | Technical Rigor | 4 | Solid methods with pseudocode and correctness proof sketch |
| 3 | Results Integrity | 2 | **Critical**: Key numerical claims do not match actual data |
| 4 | Citation Accuracy | 3 | 20/22 verified; 2 citations have errors |
| 5 | Compilation | 4 | PDF compiles successfully, well-formatted |
| 6 | Writing Quality | 4 | Professional tone, clear arguments, logical flow |
| 7 | Figure Quality | 3 | Adequate but Fig 4 is misnamed; most figures lack error bars |

---

## Overall Verdict: REVISE

The paper presents a well-structured and clearly written contribution combining known techniques (bidirectional Dijkstra, ALT landmarks, hub-based upper bounds) into a unified framework. The experimental methodology is generally sound, and the honest reporting of limitations (e.g., slower than bidirectional Dijkstra on grids) is commendable. However, **two critical results integrity issues** must be resolved before the paper can be accepted: (1) the headline "4.08x geometric mean speedup over Dijkstra" claim is incorrect, and (2) specific numerical claims about nodes expanded do not match the underlying data. Two bibliography entries also require correction.

---

## Detailed Findings

### 1. Completeness (Score: 4/5)

**Strengths:**
- All required sections present: Abstract, Introduction, Related Work (Section 2), Background/Preliminaries (Section 3), Method (Section 4), Experiments (Section 5), Results (Section 6), Discussion (Section 7), Conclusion (Section 8), References.
- Well-organized paper outline with clear section numbering and cross-references.
- Notation table (Table 1) and formal problem statement are helpful additions.
- Ablation study and break-even analysis provide thorough evaluation.

**Weaknesses:**
- The experiment plan (research/experiment_plan.md) mentions Wilcoxon signed-rank tests with Bonferroni correction, but the paper reports no statistical significance tests. For a venue like NeurIPS, reporting p-values or confidence intervals is expected.
- No explicit "Threats to Validity" subsection, though some limitations are discussed in Section 7.

### 2. Technical Rigor (Score: 4/5)

**Strengths:**
- Algorithm presented with clear pseudocode (Algorithm 1) with line-by-line explanation.
- Correctness proof sketch covers four essential properties (P1-P4) in a structured manner.
- Complexity analysis is presented in tabular form (Table 2) with clear comparison to baselines.
- The key design decision (g-value ordering vs f-value ordering for bidirectional correctness) is well-explained.

**Weaknesses:**
- The proof is a sketch only; a full proof (or reference to a supplementary appendix) would strengthen the paper.
- The claim of "superadditive pruning" (abstract, Section 7.1) is informal and not quantified or proven. A formal definition or empirical decomposition of the pruning sources would strengthen this claim.
- The paper could benefit from a clearer discussion of when landmark bounds are tight vs. loose and how this relates to graph structure.

### 3. Results Integrity (Score: 2/5) -- CRITICAL

**ISSUE 1: Inflated geometric mean speedup claim.**

The paper repeatedly claims "4.08x geometric mean speedup over Dijkstra" (abstract, Section 1, Section 6.1, Table 3, Section 8). However, independent verification from the actual data reveals:

| Computation | Geomean Speedup vs Dijkstra P2P |
|---|---|
| All synthetic configs (n=18 graph types) | **3.10x** |
| Table 3 subset only (n=12 graph types) | **3.78x** |
| All configs including real-world (n=20 graph types) | **3.07x** |
| Per-query level (n=380 individual queries) | **2.94x** |

The source of the discrepancy is `results/comparison_analysis.md`, which reports "Geometric mean speedup (all queries) | 4.08x" computed across **all 1,140 query-baseline pairs** -- i.e., averaging speedups vs Dijkstra P2P, vs Bidirectional Dijkstra, AND vs A*-Landmark. Since BALT-H achieves 32.7x geomean speedup over A* (due to A*'s high per-node landmark overhead), including the A* baseline dramatically inflates the overall number. The paper's claim of "4.08x over Dijkstra" is therefore **incorrect**; the actual geomean vs Dijkstra P2P is approximately **3.1x**.

**Action required:** Correct all instances of "4.08x" to the actual geomean vs Dijkstra P2P (~3.1x across all benchmarks, or ~3.8x for the Table 3 subset). Update the abstract, introduction, Table 3, and conclusion accordingly.

**ISSUE 2: Incorrect nodes expanded statistics.**

Section 6.3 states: "On BA graphs with 5,000 nodes, BALT-H expands an average of 22 nodes per query compared to 280 for Dijkstra P2P -- a 92% reduction."

The actual data in `results/synthetic_results.csv` shows:
- BALT-H on BA-5000: **61.4 nodes** (not 22)
- Dijkstra P2P on BA-5000: **1,493.3 nodes** (not 280)

The actual reduction is 95.9%, and the actual ratio is 24.3x -- but the specific numbers cited in the paper are both incorrect by factors of ~3x and ~5x respectively.

**Action required:** Correct the nodes expanded claim with accurate numbers from the data.

**Other data verification notes (no issues):**
- Table 3 speedup values for individual graph types match `results/comparison.csv` within rounding.
- Grid speedup of 0.70x matches data (0.704x).
- Break-even points in Table 6 are consistent with the data.
- Real-world proxy results in Table 5 match `results/comparison.csv`.
- Ablation study numbers in Table 4 match `results/optimization_results.csv`.

### 4. Citation Accuracy (Score: 3/5)

**All 22 in-text citation keys have corresponding entries in sources.bib. No missing references.**

#### Citation Verification Report

| # | Key | Status | Notes |
|---|-----|--------|-------|
| 1 | dijkstra1959 | VERIFIED | Title, author, year, journal (Numerische Mathematik), DOI all correct |
| 2 | bellman1958 | VERIFIED | Title, author, year, journal (Q. Appl. Math.), DOI all correct |
| 3 | ford1956 | VERIFIED | Title, author, year, RAND P-923, URL all correct |
| 4 | floyd1962 | VERIFIED | Title, author, year, journal (CACM), DOI all correct |
| 5 | warshall1962 | VERIFIED | Title, author, year, journal (JACM), DOI all correct |
| 6 | hart1968 | VERIFIED | Title, authors, year, journal (IEEE Trans. SSC), DOI all correct |
| 7 | fredman1987 | VERIFIED | Title, authors, year, journal (JACM), DOI all correct |
| 8 | pohl1971 | VERIFIED | Title, author, year, venue (Machine Intelligence vol 6) correct. Minor: entry type should be `@incollection` not `@article` |
| 9 | johnson1977 | VERIFIED | Title, author, year, journal (JACM), DOI all correct |
| 10 | dial1969 | VERIFIED | Title, author, year, journal (CACM), DOI all correct |
| 11 | geisberger2008 | VERIFIED | Title, authors, year, venue (WEA 2008), DOI all correct |
| 12 | abraham2012 | VERIFIED | Title, authors, year, venue (ESA 2012), DOI all correct |
| 13 | bast2007 | **INCORRECT** | **Author name mismatch**: Listed as "Hannah Bast" but published as "Holger Bast" in Science. Also, entry type is `@inproceedings` but Science is a journal (`@article`). Title, year, volume, page, DOI are correct. |
| 14 | goldberg2005 | VERIFIED | Title, authors, year, venue (SODA 2005) correct. Minor: URL is university PDF, not a persistent DOI |
| 15 | delling2011 | VERIFIED | Title, authors, year, venue (SEA 2011), DOI all correct |
| 16 | delling2017 | VERIFIED | Title, authors, year, journal (Transportation Science), DOI all correct |
| 17 | wang2021 | VERIFIED | Title, authors, year, venue (PPoPP 2021) all correct |
| 18 | ortega2015 | VERIFIED | Title, authors, year, journal (IJPP), DOI all correct |
| 19 | velickovic2021 | VERIFIED | Title, authors, year, journal (Patterns), DOI all correct |
| 20 | abboud2022 | VERIFIED | Title, authors, year, venue (LoG/PMLR), arXiv URL all correct |
| 21 | li2020 | VERIFIED | Title, authors, year, venue (NeurIPS 2020), arXiv URL all correct |
| 22 | elmasry2019 | **INCORRECT** | **Year mismatch**: Claims 2019, but arXiv ID `2410.23383` is an October 2024 submission. The 2019 version (arXiv `1905.01325`) was **withdrawn** after criticism. Either update year to 2024 or use the correct 2019 arXiv ID (and note withdrawal). |

**Summary:** 20/22 citations verified correct. 2 require corrections:
1. **bast2007**: Change author from "Hannah Bast" to "Holger Bast" (published name), change entry type to `@article`.
2. **elmasry2019**: Fix year to 2024 to match the arXiv URL, or update URL to `1905.01325` if the 2019 version is intended (note: that version was withdrawn).

### 5. Compilation (Score: 4/5)

- PDF (`research_paper.pdf`) exists and is properly compiled.
- LaTeX source uses appropriate packages (amsmath, algorithm, booktabs, natbib, pgfplots, tikz).
- TikZ architecture diagram (Figure 1) is well-executed and informative.
- Tables are well-formatted with booktabs rules.
- Minor: the `\textsc` command in the pseudocode (lines 239, 249) may not render as expected depending on the font.

### 6. Writing Quality (Score: 4/5)

**Strengths:**
- Professional academic tone throughout.
- Clear problem motivation with concrete applications.
- Logical flow from problem statement through methodology to results.
- Effective use of paragraph headings within sections.
- Limitations section (Section 7.3) is honest and thorough -- acknowledging that BALT-H is slower than bidirectional Dijkstra on grids and that the Python implementation limits absolute performance.

**Weaknesses:**
- The abstract and conclusion overclaim by using the inflated 4.08x number (see Results Integrity).
- The term "superadditive pruning" appears in the abstract and Section 7.1 without formal definition.
- The paper describes the "real-world proxy" experiments somewhat ambiguously -- using synthetic graphs as proxies for real-world data is fine but should be more explicitly caveated. These are not truly "real-world" evaluations.

### 7. Figure Quality (Score: 3/5)

**Strengths:**
- Uses a colorblind-friendly palette (Wong 2011) consistently across figures.
- All figures have labeled axes, titles, and legends.
- Figures saved at 300 DPI as both PNG and PDF.
- Scalability plot (Fig 2) includes fitted power-law curves with exponent annotations -- very informative.
- Value annotations on bar charts (Fig 3) aid readability.

**Weaknesses:**
- **Figure 4 is mislabeled**: The paper caption calls it a "Speedup heatmap" but the actual figure is a horizontal bar chart with a single color. This is not a heatmap. The caption text describes "warmer colors indicate higher speedup" which does not match the actual figure. Either regenerate as an actual 2D heatmap (graph type vs. size) or update the caption.
- Most figures lack error bars or confidence intervals. Only Fig 1's caption mentions standard deviation, but error bars are not visible on the plot.
- Fig 4 uses a single color for all bars -- a gradient or multiple colors would improve readability.
- Fig 5 (preprocessing vs query time) compares "Preprocessing" to "10 Queries" which is a somewhat arbitrary choice -- it would be more informative to show the break-even number of queries.
- Fig 3 reveals that BALT-H expands **more** nodes than A*-Landmark (447 vs 267) while being much faster -- this counterintuitive result deserves discussion in the text.

---

## Required Revisions (Actionable)

### Critical (must fix)

1. **Correct the 4.08x geomean speedup claim** throughout the paper (abstract, Section 1, Table 3 overall row, Section 8). The actual geomean vs Dijkstra P2P is ~3.1x (all benchmarks) or ~3.8x (Table 3 subset). The current 4.08x number is the geomean across all baselines including A*, not just Dijkstra.

2. **Correct the nodes expanded numbers** in Section 6.3. Replace "22 nodes ... compared to 280 for Dijkstra P2P" with the actual values from the data (61.4 and 1,493.3 respectively). Update the "92% reduction" and "12.7x" ratio accordingly.

3. **Fix citation bast2007**: Change author from "Hannah Bast" to "Holger Bast" and change BibTeX entry type from `@inproceedings` to `@article`.

4. **Fix citation elmasry2019**: Either change year to 2024 (to match arXiv 2410.23383) or update the URL to `https://arxiv.org/abs/1905.01325` and note the 2019 version's withdrawal status.

### Recommended (strongly advised)

5. **Fix Figure 4**: Either regenerate as an actual heatmap (2D: graph type vs. graph size) or rename/re-caption it as "Speedup bar chart by graph configuration." Remove the "warmer colors" language from the caption.

6. **Add error bars or confidence intervals** to Figures 1, 3, and 6. Statistical variability across queries is important for assessing reproducibility.

7. **Add statistical significance tests** (e.g., Wilcoxon signed-rank as mentioned in the experiment plan) to the results section, at minimum for the main comparison in Table 3.

8. **Discuss the nodes expanded paradox**: BALT-H expands more nodes than A*-Landmark (Fig 3) yet is dramatically faster. This is because A*'s per-node landmark overhead is higher (it evaluates all landmarks per node vs. BALT-H's active subset). This finding deserves explicit discussion.

### Minor

9. Update `goldberg2005` URL to a persistent DOI rather than a university-hosted PDF.
10. Change `pohl1971` entry type from `@article` to `@incollection`.
11. Clarify that "real-world proxy" experiments use synthetic graphs as proxies, not actual real-world datasets.
12. Define "superadditive pruning" formally or remove the term.
13. The description of BALT-H being "slower" than bidirectional Dijkstra (0.79x overall, Table 3) should be addressed more prominently -- this is a significant limitation partially hidden in the table.

---

## Summary

This paper makes a solid incremental contribution by combining three well-known shortest path techniques (bidirectional search, ALT landmarks, hub upper bounds) into a unified framework with formal correctness guarantees. The experimental evaluation is extensive and the writing quality is high. However, the inflated headline speedup number (4.08x vs. the actual ~3.1x) and incorrect nodes-expanded statistics represent significant results integrity issues that must be corrected before publication. Two bibliography entries also require fixes. With these revisions, the paper would meet the standard for acceptance.
