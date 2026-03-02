# Peer Review: Computational Search for a Perfect Cuboid

**Paper:** "Computational Search for a Perfect Cuboid: Algorithms, Near-Miss Analysis, and Scaling Feasibility"
**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-03-02

---

## Criterion Scores (1--5)

| # | Criterion | Score | Comments |
|---|-----------|-------|----------|
| 1 | Completeness | **4** | All required sections present (Abstract, Introduction, Related Work, Background, Method, Experimental Setup, Results, Discussion, Conclusion, References). Well-structured with proper subsections. Minor: no Acknowledgments section. |
| 2 | Technical Rigor | **4** | Algorithms described with pseudocode; equations are correctly stated; scaling analysis uses log-log regression; chi-squared test is appropriate. The Pythagorean graph reformulation is a genuine algorithmic contribution. However, see data integrity issues below. |
| 3 | Results Integrity | **2** | **Multiple contradictions between data files and paper text.** See detailed findings below. This is the primary reason for revision. |
| 4 | Citation Accuracy | **2** | **No fabricated citations**, but 8 of 27 entries have errors ranging from wrong year/volume/pages to missing authors and incorrect URLs. See detailed verification report. |
| 5 | Compilation | **4** | PDF exists (370 KB), appears well-formatted. LaTeX source compiles with TikZ diagrams inlined. Minor: could not render PDF to verify final layout due to missing poppler-utils, but file size and structure are consistent with a complete document. |
| 6 | Writing Quality | **4** | Professional academic tone throughout. Clear logical flow. Equations are well-typeset. Tables are well-formatted with booktabs. Good use of paragraph headings. Honest about limitations. |
| 7 | Figure Quality | **3** | Figures use custom color palettes (not default matplotlib), have proper axis labels, legends, and annotations. The scaling comparison and ablation figures are publication-quality. The near-miss histogram is adequate but plain. Coverage comparison is clean. Overall acceptable but the near-miss histogram could use kernel density overlay and confidence bands. |

**Weighted Overall: 3.3 / 5**

---

## Verdict: REVISE

The paper presents genuine, well-structured computational research on the perfect cuboid problem. The algorithmic contributions (Pythagorean graph reformulation, modular sieve ablation) are solid. However, **multiple data integrity issues** and **citation errors** prevent acceptance. All issues are correctable.

---

## Detailed Findings

### A. Results Integrity Issues (CRITICAL)

**A1. Near-miss sample size contradiction (620 vs 527)**
- Paper text (Section 6.5, line 699): "We analyzed **620** Euler bricks from all sources"
- Figure 4 caption (line 738): "620 Euler bricks"
- Actual data (`results/near_miss_results.json`, statistics.n): **527**
- Figure legend in the actual PNG image: **n=527**
- The rubric item_014 notes also say "527 Euler bricks analyzed"
- Arithmetic check: 69 exhaustive + 517 parametric = 586 max unique (assuming no overlap); 620 > 586, which is impossible
- **Action required:** Reconcile the sample size. Use the actual value from the data (527 or whatever is correct after deduplication). Update all text, figure captions, and statistics accordingly.

**A2. Chi-squared statistic contradiction (4.45 vs 6.72)**
- Paper abstract and Section 6.5: χ² = **4.45**, dof = 9
- Actual data (`results/near_miss_results.json`, statistics.chi_squared): **6.719** (≈ 6.72)
- Both values lead to failure to reject uniformity (critical value 16.92), so the qualitative conclusion stands, but the reported statistic is wrong.
- **Action required:** Report the correct χ² value from the actual computation.

**A3. Mean and std values slightly off**
- Paper: mean = 0.257, std = 0.145
- Data: mean = 0.2564, std = 0.1462
- These are close but appear to be from different runs or sample sizes (likely from the 620 vs 527 discrepancy).
- **Action required:** Report statistics matching the actual data.

**A4. Near-miss table source mismatch (Rank #3)**
- Paper Table 4 (Rank 3): edges (28083, 43056, 105820), source listed as "**Saunderson**"
- Actual data (`results/near_miss_results.json`): source = "**bremner_shared_edge**"
- **Action required:** Correct the source attribution in the table.

**A5. Speedup factor discrepancy (780x vs ~1001x)**
- Paper claims 780x speedup for novel search over brute force
- From `results/scaling_data.json`: brute_force time = 16.1112s, novel time = 0.0161s → ratio = **1001x**
- Even with rounding (0.02s): 16.11/0.02 = **806x**
- **Action required:** Recompute and report the correct speedup factor, or explain the discrepancy.

**A6. Internal contradiction: Ablation table vs. main text**
- Section 4.2 (line 342-344): "reducing exact integer-square-root checks from ~15.4 million to just **69** at bound N=5,000"
- Table 5 / Ablation data (25 primes, same N=5000): exact_checks = **23**, total_c = 2,143,879
- These are contradictory: 69 ≠ 23, and 15.4M ≠ 2.14M at the same configuration
- The ablation data also shows count=23 bricks found at N=5000, but there should be 69 Euler bricks. This suggests the ablation may have been run at N=2000 (where count=23 bricks) but reported as N=5000.
- **Action required:** Verify the ablation was actually run at N=5000. Reconcile the exact-check counts and total candidate counts. If the ablation was at N=2000, rerun at N=5000 or correct the table caption.

### B. Citation Verification Report

All 27 entries in `sources.bib` were individually verified via web search. **No citations are fabricated.** All refer to real publications by real authors. However, 8 entries contain errors of varying severity.

#### Fully Verified (19/27)

| Key | Status |
|-----|--------|
| `halcke1719` | VERIFIED -- Paul Halcke, 1719, N. Sauer Hamburg. Euler brick (44,117,240) on p. 265. Confirmed via MathWorld and Google Books. |
| `lalblundon1966` | VERIFIED -- Lal & Blundon, Math. Comp. 20(94):144-147, 1966. Confirmed via AMS. |
| `leech1977` | VERIFIED -- Leech, Amer. Math. Monthly 84(7):518-533, 1977. DOI: 10.1080/00029890.1977.11994405. |
| `leech1981` | VERIFIED -- Leech, Canad. Math. Bull. 24(3):377-378, 1981. DOI: 10.4153/CMB-1981-058-1. |
| `guy2004` | VERIFIED -- Guy, Unsolved Problems in Number Theory, 3rd ed., Springer, 2004. Problem D18. |
| `rathbun2020` | VERIFIED -- Rathbun, arXiv:1705.05929v4, 2020. |
| `matson2015` | VERIFIED -- Matson, unsolvedproblems.org/S58.pdf. |
| `bremner1988` | VERIFIED -- Bremner, Rocky Mountain J. Math. 18(1):105-121, 1988. DOI: 10.1216/RMJ-1988-18-1-105. |
| `sharipov2012a` | VERIFIED -- Sharipov, arXiv:1205.3135, 2012. |
| `sharipov2012b` | VERIFIED -- Sharipov, arXiv:1209.5706, 2012. |
| `degrey2024` | VERIFIED -- de Grey, Gibbs, Helm. arXiv:2401.06784. Geombinatorics XXXIII(3), 2024. |
| `lloyd2022` | VERIFIED -- Lloyd, arXiv:2206.06160, 2022 (subsequently withdrawn v2, resubmitted v3). |
| `agbanwa2025` | VERIFIED -- Agbanwa, Figshare preprint, 2025. DOI: 10.6084/m9.figshare.28829606.v2. |
| `mathworld_euler_brick` | VERIFIED -- Weisstein, MathWorld. URL confirmed. |
| `wikipedia_euler_brick` | VERIFIED -- Wikipedia contributors. URL confirmed. |
| `saunderson1740` | VERIFIED (minor) -- Saunderson, 1740. Publisher listed as "Cambridge University Press" is anachronistic but conventionally acceptable. Full title is "The Elements of Algebra, in Ten Books." |
| `dickson2005` | VERIFIED (minor) -- Dickson, Dover 2005 reprint. ISBN 0486442330 confirmed. URL stale but redirects. |
| `ramsden2013` | VERIFIED (minor) -- Ramsden & Sharipov, arXiv:1303.0765, 2013. Middle initial "R." for Ramsden unconfirmed but not incorrect. |
| `sharipov2020` | VERIFIED (minor) -- Sharipov, J. Math. Sci. 252:266-282. Online 2020, print 2021; citing 2020 is defensible. |

#### Errors Found (8/27)

| Key | Severity | Issue |
|-----|----------|-------|
| `spohn1966` | **HIGH** | Year, volume, AND pages are ALL wrong. Should be: 1972, vol. 79, pp. 57-59 (not 1966, vol. 73, pp. 718-719). Confirmed via MathWorld and Semantic Scholar. |
| `korec1992` | **HIGH** | Title missing "rational" (should be "Lower bounds for perfect **rational** cuboids"). Issue No. 2 → No. 5. Pages 145-152 → 565-582. Confirmed via Springer and van Luijk's thesis. |
| `butler2004` | **HIGH** | URL is entirely wrong: `dvd3000.ca` is an unrelated website. Correct URL: `https://www.durangobill.com/IntegerBrick.html`. Title should be "The 'Integer Brick' Problem (The Euler Brick Problem)". |
| `elementary2026` | **MODERATE** | Missing author entirely. The paper is by **Stephane Yelle** (arXiv:2602.00239). |
| `kraitchik1953` | **MODERATE** | Year is wrong: should be **1947** (Tome III: Analyse Diophantine), not 1953. |
| `knill2013` | **MODERATE** | Year is wrong: should be **2009** (dated February 24, 2009 on Harvard page), not 2013. |
| `sharipov2015` | **MODERATE** | Missing co-author: should be **Masharov, A. A. and Sharipov, R. A.** (confirmed on arXiv). |
| `vanluijk2000` | **LOW** | Thesis is from **Utrecht University**, not Leiden University. Van Luijk later moved to Leiden where the PDF is now hosted. |

### C. In-Text Citation Cross-Check

All `\cite` commands in the LaTeX source have corresponding entries in `sources.bib`. No orphan citations detected. No bibliography entries are unused. The `\cite{sharipov2012b}` entry is used only in the Related Work section (line 182), which is appropriate.

### D. Figure Quality Assessment

| Figure | Quality | Notes |
|--------|---------|-------|
| Fig. 1 (Pythagorean graph, TikZ) | Good | Hand-crafted TikZ diagram with custom colors, clean layout. |
| Fig. 2 (Cuboid diagram, TikZ) | Good | Clear 3D representation with labeled edges, diagonals. |
| Fig. 3 (Scaling + Coverage) | Good | Custom colors, fitted regression lines, distinct markers. Log-log scaling properly presented. |
| Fig. 4 (Near-miss distribution) | Adequate | Proper labels but plain histogram bars. **Shows n=527, contradicting paper's claim of 620.** Could benefit from KDE overlay and confidence intervals. |
| Fig. 5 (Ablation) | Good | Two-panel with annotations (data values), proper axes. Clean presentation. |

### E. Technical Observations

1. The Pythagorean graph reformulation (Section 4.4) is a genuine contribution. The graph-theoretic perspective of finding triangles in the Pythagorean graph is elegant. The 35% coverage limitation is honestly disclosed.

2. The modular sieve ablation (Section 6.4) provides useful practical guidance, showing diminishing returns after 10 primes. This is a solid empirical contribution.

3. The paper correctly identifies that parametric families (Saunderson, Bremner) are provably incapable of producing perfect cuboids, citing Knill. This is an important caveat.

4. The discussion of Brauer-Manin obstructions on the K3 surface (Section 7) is well-informed and identifies the right theoretical direction.

5. The necessary conditions (C1-C5 in Section 3) are correctly stated and properly attributed.

---

## Specific, Actionable Revision Requirements

### Must Fix (Blocking)

1. **Reconcile sample size**: Determine whether 527 or 620 (or some other number) is the correct count of unique Euler bricks analyzed. Update ALL references in the paper (abstract, Section 6.5, Figure 4 caption) and regenerate the histogram figure if needed.

2. **Fix chi-squared value**: Report the correct χ² statistic from the actual data (6.72, not 4.45). Update abstract, Section 6.5, and Figure 4 caption.

3. **Fix ablation table / main text contradiction**: Either rerun the ablation at N=5000 or correct the table caption to indicate the actual bound used. Reconcile the exact-check count (69 in main text vs. 23 in table).

4. **Fix speedup factor**: Recompute from actual timing data and report correctly.

5. **Fix near-miss table source**: Change Rank #3 source from "Saunderson" to "Bremner" (or the correct family).

6. **Fix 8 bibliography entries** with errors as detailed above:
   - `spohn1966` → year 1972, vol 79, pp 57-59
   - `korec1992` → add "rational" to title, issue 5, pp 565-582
   - `butler2004` → URL to durangobill.com, fix title
   - `elementary2026` → add author Stephane Yelle
   - `kraitchik1953` → year 1947
   - `knill2013` → year 2009
   - `sharipov2015` → add co-author Masharov
   - `vanluijk2000` → institution Utrecht University

### Should Fix (Recommended)

7. **Improve near-miss histogram**: Add KDE overlay, confidence band for uniform distribution, and ensure the sample size in the figure legend matches the text.

8. **Clarify scaling data**: In the extrapolation table (Table 3), clarify whether estimates use the empirical exponent from 3 data points only. Note the statistical uncertainty in the fitted exponents.

9. **Add DOIs**: Where available (leech1977, leech1981, bremner1988, sharipov2020, etc.), add DOI fields to the bibliography entries.

10. **Minor text**: The abstract says "69 Euler bricks... and 517 parametric-family bricks" (total ≤ 586), but later says "620 Euler bricks from all sources." Verify unique-after-dedup count.

---

## Summary

This is a well-structured computational study with genuine algorithmic contributions. The writing quality is high, the methodology is sound, and the figures are adequate. However, **multiple numerical contradictions between the actual result data and the paper text** undermine confidence in the reported findings. The bibliography, while containing no fabricated entries, has several errors including wrong years, wrong page numbers, and incorrect URLs.

All issues are correctable through careful proofreading and data reconciliation. After revision, this paper would be a solid contribution to the computational number theory literature on the perfect cuboid problem.

**Verdict: REVISE**
