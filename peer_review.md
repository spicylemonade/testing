# Peer Review: A Multi-Method Computational Investigation of the Perfect Cuboid Problem

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-03-02
**Verdict:** **REVISE**

---

## Criterion Scores

| # | Criterion | Score (1-5) |
|---|-----------|:-----------:|
| 1 | Completeness | 5 |
| 2 | Technical Rigor | 4 |
| 3 | Results Integrity | 3 |
| 4 | Citation Accuracy | 2 |
| 5 | Compilation | 4 |
| 6 | Writing Quality | 4 |
| 7 | Figure Quality | 4 |

**Overall: REVISE** (Citation Accuracy score below 3; Results Integrity borderline)

---

## 1. Completeness (5/5)

All required sections are present and substantive:
- **Abstract**: Concise, quantitative, well-structured summary (lines 62-88).
- **Introduction**: Problem statement with formal equations, historical context, and contributions list.
- **Related Work**: Comprehensive coverage of parametric families, modular constraints, algebraic geometry, computational searches, and proof attempts.
- **Background & Preliminaries**: Formal definitions (perfect cuboid, Euler brick, near-miss score), notation table, Pythagorean parametrization.
- **Method**: Five search strategies described with algorithms, equations, and pseudocode.
- **Experimental Setup**: Implementation details, hardware, search parameters table, evaluation metrics.
- **Results**: Consolidated results table, filter effectiveness, benchmarks, near-miss analysis, verification against published catalogs, top near-misses table.
- **Discussion**: Evidence synthesis, proof assessment, methodological contributions, limitations.
- **Conclusion**: Summary of findings, six future directions.
- **References**: 23 BibTeX entries.

The paper also includes a TikZ cuboid diagram (Fig. 1), a pipeline architecture diagram (Fig. 2), and four data figures. This is thorough and well-organized.

---

## 2. Technical Rigor (4/5)

**Strengths:**
- The Diophantine system is formally specified (Eqs. 1-4) with proper definitions.
- Algorithm 1 (Triple Decomposition Search) is clearly presented with complexity analysis.
- The Saunderson family parametrization (Eq. 6) is correctly stated with the Pocklington non-existence result cited.
- The multi-stage modular sieve is well-described with four cascaded stages.
- The quadratic residue sieve with 50 primes is a sound approach.
- The near-miss score (Eq. 5) is a well-defined metric.
- The power-law regression is appropriately presented with low R^2 acknowledged.

**Issues:**
- The paper describes `src/elliptic_families.py` in the rubric context as implementing elliptic curve methods (Colman/Ramsden-Sharipov), but the actual implementation uses Brahmagupta-Fibonacci triple composition (extended multi-hop search). The paper correctly describes this as "Euler two-triple family" (Section 4.1), which is honest, but the claimed 1,238 "additional Euler bricks not found by classical families" needs clearer verification methodology.
- The complexity claim of O(T^2/V) for triple decomposition (line 453) is stated without derivation. A brief justification would strengthen the claim.
- The "cross-domain concept evolution" section (4.7) is vague. The connection between "treewidth-3 hypergraph CSP" and the actual sieve design, and between "spectral gap framing" and power-law regression, are asserted but not substantiated.

---

## 3. Results Integrity (3/5)

**Verified claims (match actual data):**
- 1,714 Euler bricks found by combined search: matches `results/metrics.json` (1714) and `results/search_summary.md` (1714).
- 0 perfect cuboids: confirmed across all results files.
- Wall-clock time ~4.5s: paper says 4.49s, `metrics.json` says 4.59s, `search_summary.md` says 4.59s. The paper's 4.49s is from `results/benchmark_comparison.md`. Minor rounding discrepancy but acceptable.
- Best near-miss (43440, 45612, 49775) with score 2.98e-08: matches `results/near_misses.csv` (2.9790e-08).
- Regression slope -0.30, R^2=0.025, p=0.024: matches `results/near_miss_statistics.md` (-0.2997, 0.0254, 2.4196e-02).
- Filter rejection rates in Table 3 are consistent with `results/sieve_analysis.md`.

**Issues found:**

### Table 5 (Verification) contains incorrect space diagonal approximations:

| Euler Brick | Paper claims | Actual (from `results/search_log.jsonl`) | Error |
|---|---|---|---|
| (85, 132, 720) | 738.0 | 736.9 | off by 1.1 |
| (140, 480, 693) | 864.0 | 854.5 | off by 9.5 |
| (160, 231, 792) | 849.9 | 840.4 | off by 9.5 |

Three of five space diagonal values in Table 5 are incorrect. The values for (44,117,240) = 270.6 and (240,252,275) = 443.6 are approximately correct.

### Internal data inconsistency:
`results/benchmark_comparison.md` reports the combined search best near-miss quality as "Best: 3.99e-14", but `results/search_summary.md` and `results/near_misses.csv` both show 2.98e-08. The paper correctly reports 2.98e-08, but the inconsistency in the results directory undermines confidence.

### Action required:
- Recompute and correct all space diagonal approximations in Table 5.
- Reconcile the near-miss score discrepancy in `results/benchmark_comparison.md`.

---

## 4. Citation Accuracy (2/5) -- CRITICAL

**Methodology:** Every entry in `sources.bib` was individually verified via web search against arXiv, publisher databases, library catalogs, and scholarly indices.

### Citation Verification Report

#### VERIFIED (10/23) -- All details correct

| Key | Citation | Status |
|-----|----------|--------|
| `stolltesta2010` | Stoll & Testa, "The surface parametrizing cuboids", arXiv:1009.0388, 2010 | **VERIFIED** -- confirmed on arXiv |
| `sharipov2021` | Sharipov, "Symmetry-Based Approach...", J. Math. Sci., 2021 | **VERIFIED** -- confirmed on Springer (vol. 252, pp. 266-282) |
| `matson2014` | Matson, "Results of computer search for a perfect cuboid", 2014 | **VERIFIED** -- confirmed at unsolvedproblems.org |
| `kraitchik1945` | Kraitchik, "On certain rational cuboids", Scripta Math., 1945 | **VERIFIED** -- confirmed via Rathbun's catalog and multiple secondary sources |
| `lloyd2022` | Lloyd, "There is no Perfect Cuboid", arXiv:2206.06160, 2022 | **VERIFIED** -- confirmed on arXiv |
| `yelle2026` | Yelle, "An Elementary Obstruction...", arXiv:2602.00239, 2026 | **VERIFIED** -- confirmed on arXiv |
| `rathbun2017` | Rathbun, "The Integer Cuboid Table", arXiv:1705.05929, 2017 | **VERIFIED** -- confirmed on arXiv |
| `maiti2023` | Maiti, "Multiple New Important Conjectures...", arXiv:2312.09091, 2023 | **VERIFIED** -- confirmed on arXiv (not cited in paper text) |
| `butler_web` | Butler, "The Integer Brick Problem", durangobill.com | **VERIFIED** -- website confirmed with computational results |
| `guy2004` | Guy, "Unsolved Problems in Number Theory", 3rd ed., Springer, 2004 | **VERIFIED** -- confirmed; Problem D18 is the perfect cuboid |

#### PARTIALLY VERIFIED WITH ERRORS (11/23)

| Key | Claimed Details | Actual Details | Severity |
|-----|----------------|----------------|----------|
| `stolltesta2025` | **Authors: Michael Stoll, Damiano Testa**; "The L-function of the Surface Parametrizing Cuboids", arXiv:2512.22520 | **Authors: Madoka Horie, Takuya Yamauchi** (Stoll & Testa are NOT authors) | **CRITICAL -- wrong authors; paper text (line 183) falsely attributes this work to Stoll & Testa** |
| `sharipov2017` | "On Walter Wyss's no perfect cuboid paper", **arXiv:1710.07361** | Correct arXiv ID is **1704.00165**. The ID 1710.07361 points to an unrelated astrophysics paper ("A Monster CME Obscuring A Demon Star Flare" by Moschou et al.) | **CRITICAL -- wrong arXiv ID; URL leads to wrong paper** |
| `colman1971` | "A Perfect Cuboid in Gaussian Integers", **The Mathematical Gazette, vol 55, no 394, 1971, pp 455-456** | This paper was published in **Fibonacci Quarterly, vol 32, no 3, 1994** (not Math Gazette 1971) | **SIGNIFICANT -- wrong venue, wrong year, wrong pages** (not cited in paper text) |
| `spohn1972` | "On the derived cuboid", **Canadian Math. Bull., vol 15, 1972, pp 599-601** | Correct: **vol 17, 1974, pp 575-577**. The 1972 Spohn paper is a different work ("On the integral cuboid", Amer. Math. Monthly) | **SIGNIFICANT -- wrong year, volume, and pages** |
| `wyss2015` | **"On Perfect Cuboids"**, arXiv:1506.02215 | Correct title: **"No Perfect Cuboid"** | **MODERATE -- wrong title** |
| `halcke1719` | "Deliciae Mathematicae oder Mathematisches **Sinnen-Identity**", 1719 | Correct: "...Mathematisches **Sinnen-Confect**" | **MODERATE -- wrong subtitle** |
| `aleshkevich2022` | "Perfect cuboid, primitive Pythagorean triples..." by **Nikolai** Aleshkevich | Correct author: **Natalia** Aleshkevich (arXiv:2203.01149) | **MODERATE -- wrong first name** (not cited in paper text) |
| `vanluijk2000` | `@phdthesis`, Utrecht University, 2000 | Actually a **Doctoraalscriptie (master's thesis)**, not a PhD thesis. Van Luijk's PhD was from UC Berkeley in 2005 | **MINOR -- wrong thesis type** |
| `euler1770` | Publisher: **Royal** Academy of Sciences, St. Petersburg | Should be **Imperial** Academy of Sciences (Kayserliche Akademie der Wissenschaften) | **MINOR -- wrong publisher name** |
| `roberts2009` | Year: **2009** | Paper published in **March 2010** issue (vol 37, no 1) of the Gazette; received 2009 | **MINOR -- off-by-one year** |
| `pocklington1912` | Year: **1912** | Formal publication in Proc. Cambridge Phil. Soc. vol 17 was in **1914**; 1912 may be reading date | **MINOR -- year ambiguity** |

#### PARTIALLY VERIFIED -- MINOR SPELLING (2/23)

| Key | Issue |
|-----|-------|
| `kraitchik1947` | Subtitle misspellings: "Application" should be "Applications"; "Rationelles" should be "Rationnels" |
| `saunderson1740` | "Cambridge University Press" is a modernized name for what was "printed at the University-Press" -- acceptable |

### Critical Text Error Arising from Citation Error

**Line 183 of the paper states:** *"Their subsequent work computed the L-function and etale cohomology of the surface \citep{stolltesta2025}."*

This sentence falsely attributes arXiv:2512.22520 to Stoll and Testa. The actual authors are **Madoka Horie and Takuya Yamauchi**. This is a factual error in the paper body, not just a bibliography typo. The pronoun "Their" (referring to Stoll and Testa from the previous sentence) makes the misattribution explicit.

### Summary of Citation Issues

- **2 CRITICAL errors**: wrong authors on stolltesta2025, wrong arXiv ID on sharipov2017
- **2 SIGNIFICANT errors**: wrong venue/year/pages on colman1971 and spohn1972
- **3 MODERATE errors**: wrong title on wyss2015, wrong subtitle on halcke1719, wrong first name on aleshkevich2022
- **4 MINOR errors**: thesis type, publisher name, year ambiguities
- **10 VERIFIED**: no issues

With 2 critical citation errors (one causing a factual error in the paper text) and 5 additional moderate-to-significant errors, the citation accuracy is unacceptable for publication.

---

## 5. Compilation (4/5)

- `research_paper.pdf` exists and was successfully compiled.
- The paper uses appropriate LaTeX packages (amsmath, natbib, hyperref, pgfplots, tikz, booktabs, algorithm).
- TikZ diagrams (cuboid schematic, pipeline) compile inline -- good practice.
- Figures are included via `\includegraphics` from the `figures/` directory.

**Minor issue:** Cannot verify whether compilation is warning-free without recompiling. The PDF appears well-formatted based on the LaTeX source.

---

## 6. Writing Quality (4/5)

**Strengths:**
- Professional academic tone throughout.
- Clear problem statement with formal mathematical definitions.
- Logical flow from background through methods to results to discussion.
- Good use of notation summary table (Table 1).
- Limitations section is honest about the modest search range compared to state-of-the-art.
- The acknowledgment that R^2 = 0.025 provides "very little" explanatory power is appropriately cautious.

**Issues:**
- Section 4.7 (Cross-Domain Concept Evolution) reads as boilerplate. The terms "treewidth-3 hypergraph CSP" and "spectral gap framing" are introduced without sufficient context. A reader unfamiliar with the ConceptEvolve framework would find this section opaque.
- The abstract claims a "speedup exceeding 10^6x" which, while technically supported by the asymptotic argument, compares a 10^5-range combined search against an extrapolated brute-force 10^5-range search. The comparison is legitimate but should be more carefully qualified since the methods solve slightly different problems (triple decomposition finds Euler bricks, not exhaustively testing all triples).

---

## 7. Figure Quality (4/5)

All four figures were visually inspected:

- **`figures/near_miss_trend.png`** (Fig. 3a): Log-log scatter plot with dashed regression line. Labeled axes, legend with slope and R^2. Uses muted color palette. Good.
- **`figures/filter_funnel.png`** (Fig. 3b): Horizontal bar chart on log scale with count annotations. Distinct colors per stage. Clear and informative.
- **`figures/benchmark_comparison.png`** (Fig. 4): Dual-panel (Euler bricks found + efficiency). Log-scale right panel. Count annotations on bars. Reasonable quality.
- **`figures/search_coverage.png`** (Fig. 5): Scatter with colorbar (log near-miss score) + histogram of brick sizes. Two-panel layout. Adequate.

**Issues:**
- The search_coverage figure's color range is compressed (viridis from ~-7 to ~-3), making most points appear similar. A diverging colormap or manual normalization would improve readability.
- The benchmark_comparison bars could benefit from error bars or confidence intervals if multiple runs were performed.
- The filter_funnel figure correctly represents the sieve stages but the "Perfect Cuboid?" bar showing 0 is visually ambiguous at log scale (it appears as a tiny bar rather than clearly zero).

Overall the figures are above default matplotlib quality (custom colors, proper labels, DPI), but not yet at the level of top-tier venue figures. Acceptable for a technical report but could be polished.

---

## Overall Verdict: REVISE

### Reasons for REVISE (not ACCEPT):

1. **Citation accuracy is below threshold (2/5 < 3).** Two critical errors: (a) `stolltesta2025` attributes a paper to entirely wrong authors (Stoll & Testa instead of Horie & Yamauchi), causing a factual misattribution in the paper text at line 183; (b) `sharipov2017` has a wrong arXiv ID pointing to an unrelated astrophysics paper. Five additional moderate-to-significant errors in other citations.

2. **Results integrity issues.** Three of five space diagonal approximations in Table 5 are numerically incorrect (verified against `results/search_log.jsonl`). The benchmark results file has an internal inconsistency (3.99e-14 vs 2.98e-08 for best near-miss).

### Required Revisions (Actionable)

#### Must Fix (blocking acceptance):

1. **Fix `stolltesta2025` citation.** Change authors to Madoka Horie and Takuya Yamauchi. Fix the paper text at line 183: change "Their subsequent work" to "Horie and Yamauchi" (or equivalent) -- these are not Stoll & Testa's results.

2. **Fix `sharipov2017` arXiv ID.** Change from `1710.07361` to `1704.00165` and update the URL to `https://arxiv.org/abs/1704.00165`.

3. **Fix `spohn1972` metadata.** Year: 1974, volume: 17, pages: 575-577 (not 1972/15/599-601).

4. **Fix `wyss2015` title.** Change "On Perfect Cuboids" to "No Perfect Cuboid".

5. **Fix `halcke1719` subtitle.** Change "Sinnen-Identity" to "Sinnen-Confect".

6. **Fix `colman1971`.** Either correct venue to Fibonacci Quarterly vol 32 (1994) pp. 255-256, or find the correct 1971 reference if one exists.

7. **Fix `aleshkevich2022` author.** Change "Nikolai" to "Natalia".

8. **Fix Table 5 space diagonal values.** Recompute all entries against actual data:
   - (85, 132, 720): should be ~736.9 (not 738.0)
   - (140, 480, 693): should be ~854.5 (not 864.0)
   - (160, 231, 792): should be ~840.4 (not 849.9)

9. **Fix `results/benchmark_comparison.md`** near-miss value for combined search: should be 2.98e-08, not 3.99e-14.

#### Should Fix (strengthen paper):

10. **Minor citation fixes:** `vanluijk2000` thesis type (`@mastersthesis`), `euler1770` publisher ("Imperial" not "Royal"), `roberts2009` year (2010), `pocklington1912` year (1914), `kraitchik1947` subtitle spelling.

11. **Section 4.7 (Cross-Domain Concept Evolution):** Either substantiate the claims about treewidth-3 hypergraph CSP and spectral gap connections with concrete details, or reduce this section to a brief mention.

12. **Qualify the speedup claim.** The >10^6x speedup compares an Euler-brick-finding pipeline against a hypothetical brute-force exhaustive search of a different character. Acknowledge this apples-to-oranges aspect more explicitly.

### Positive Assessment

Despite the issues requiring revision, the paper has substantial merit:
- The unified framework combining five search strategies is well-conceived.
- The technical exposition of algorithms and sieve methods is clear and reproducible.
- The honest treatment of near-miss statistics (acknowledging very low R^2) demonstrates scientific integrity.
- The critical review of proof attempts (Table 7) is a valuable contribution to the literature.
- The future directions are concrete and well-motivated.
- The paper is well-written with a logical structure that would serve as a good survey/computational study of the perfect cuboid problem once the citation and data errors are corrected.

The paper should be publishable after the above revisions are addressed. The citation errors appear to be systematic AI-generation artifacts (wrong metadata, wrong authors on a thematically related paper) rather than intentional fabrication, but they must be corrected before the work meets publication standards.
