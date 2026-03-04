# Peer Review: "Extending OEIS A284668: Identifying the Collatz Delay Champion Below 10^19"

**Reviewer:** Automated Peer Review Pipeline  
**Date:** 2026-03-04  
**Venue Standard:** Nature/NeurIPS-tier rigor

---

## Summary

The paper identifies the number n* = 9,781,262,575,275,081,247 as the candidate a(19) for OEIS sequence A284668 (the number below 10^19 with the largest Collatz total stopping time), with delay 2,426 steps. The result is sourced from Roosendaal's comprehensive database and independently verified by naive Python iteration. The paper also provides a statistical analysis of all 148 known delay records, a k-step shortcut engine for accelerated Collatz computation, and a complete verification suite.

---

## Criterion Scores

### 1. Completeness: **5/5**

All required sections are present and substantive:
- Abstract (clear, quantitative, self-contained)
- Introduction (motivation, context, contribution list)
- Related Work (verification frontier, delay records, algorithms, theory)
- Background & Preliminaries (formal definitions, stochastic heuristic)
- Method (shortcut engine, lookup table, parallel framework, verification)
- Experimental Setup (hardware, software, parameters, search budget)
- Results (central finding, A284668 verification, intermediate records, performance, statistics, trajectories, certificate)
- Discussion (nature of result, comparison with prior art, structural observations, limitations)
- Conclusion (summary, future work)
- Acknowledgments
- References (18 entries)

The paper is thorough and well-structured. The inclusion of formal definitions (Definitions 1-5), propositions, conjectures, and a code listing is commendable.

### 2. Technical Rigor: **4/5**

**Strengths:**
- The k-step shortcut engine is properly formalized (Proposition 1, Equation 2) with clear notation.
- The experimental methodology is well-documented: shortcut parameter k benchmarked at 4 values, parallel search described with chunk sizes and worker counts.
- The verification protocol is exemplary: naive Python script independent of the optimized engine, SHA-256 certificate hash for reproducibility.
- The paper is refreshingly transparent about its limitations (Section 7.3): non-exhaustive search, reliance on Roosendaal's database, no novel algorithmic contribution.

**Weaknesses:**
- Proposition 1 lacks a formal proof. While the claim follows from standard modular arithmetic reasoning, a brief proof sketch or citation to a prior formalization would strengthen rigor.
- The stochastic heuristic (Section 3) is somewhat hand-wavy in the derivation of the "37-42 bits" prediction. The connection between the random-walk model and the observed 41.9 coefficient deserves more careful treatment.
- The regression analysis (Eq. 3) reports R^2 = 0.99 without confidence intervals on the slope/intercept or residual analysis. For a statistical claim this strong, standard errors should be reported.

### 3. Results Integrity: **4/5**

**Verified claims:**
- **Central claim independently verified:** I ran the naive Collatz iteration on n* = 9,781,262,575,275,081,247 and confirmed delay = 2,426 steps. Also confirmed 64-bit length.
- **A284668 terms verified:** I independently verified a sample of 10 A284668 entries (a(1) through a(9) and a(18)), all matching the paper's Table 1.
- **Intermediate records verified:** I verified Roosendaal record at n = 2,678,604,327,232,691,454, confirming delay = 2,331 as claimed in Table 2.
- **Verification certificate (`results/final/verification_certificate.json`):** Contains 29 records, all showing match = true, consistent with paper claims.
- **Figures match data:** The delay_vs_bitlength figure shows the regression line delay = 41.9 * bits - 271, consistent with the paper. The trajectory figures show correct starting values and delay counts.

**Issues found:**
- **Roosendaal record numbering is incorrect.** The paper consistently labels the records in [10^18, 10^19) as #141 through #148 (Table 2). However, cross-referencing against the actual Roosendaal database (`delays.txt` from ericr.nl/wondrous/), these records are numbered #138 through #145. The offset is exactly 3. Specifically:
  - Paper says n* = 9,781,262,575,275,081,247 is Roosendaal record #148; it is actually #145.
  - Paper says 1,278,775,404,785,934,855 is #141; it is actually #138.
  - All eight entries in Table 2 are off by +3.
  
  This does NOT affect the central claim (the number and its delay are correct), but it is a factual error in metadata.

- **`full_search_results.json` reveals the search did not independently discover n*.** The file shows the best number found by the systematic search was n = 1,000,000,003,325,573,601 with delay 1,505 — far below the claimed 2,426. The identification of n* came from cross-referencing Roosendaal's database, not from the paper's own parallel search. The paper is transparent about this in Section 7.1 ("the identification of n* relies on Roosendaal's database rather than our own exhaustive scan"), but the phrasing in the abstract and Section 6.1 could mislead a casual reader into thinking the authors computationally discovered n* themselves. The abstract says "We present a systematic computational investigation that independently verifies all 18 known terms and identifies the delay champion below 10^19" — the word "identifies" overstates the authors' computational contribution when the identification came from a pre-existing database.

### 4. Citation Accuracy: **4/5**

I verified all 18 entries in `sources.bib` via web search. Below is the per-entry verification report.

| BibTeX Key | Title Match | Author Match | Year Match | Venue Match | DOI/URL Match | Verdict |
|---|---|---|---|---|---|---|
| `tao2019` | Yes | Yes | Partial* | Yes | Yes (DOI 10.1017/fmp.2022.8 correct) | **Minor issue** |
| `barina2025` | Yes | Yes | Yes | Yes | Yes (Springer, Vol. 81, art. 810) | **Verified** |
| `barina2021` | Yes | Yes | Yes | Yes | Yes (Vol. 77, pp. 2681-2688) | **Verified** |
| `lagarias2003` | Partial** | Yes | Yes | Yes | Yes (arXiv:math/0309224) | **Minor issue** |
| `lagarias2006` | Yes | Yes | Partial*** | Yes | Yes (arXiv:math/0608208) | **Minor issue** |
| `lagarias1985` | Yes | Yes | Yes | Yes | Yes (Am Math Monthly, Vol. 92, No. 1) | **Verified** |
| `roosendaal2026` | Yes | Yes | Yes | N/A (website) | Yes (ericr.nl/wondrous/) | **Verified** |
| `oliveira2010` | Yes | Yes | Yes | Yes | Yes (AMS book chapter) | **Verified** |
| `leavens1992` | Yes | Yes | Yes | Yes | Yes (C&MA, Vol. 24, No. 11) | **Verified** |
| `kontorovich2005` | Yes | Yes | Yes | Yes | Yes (Acta Arith. 120, pp. 269-297) | **Verified** |
| `crandall1978` | Yes | Yes | Yes | Yes | Yes (Math. Comp. 32(144), pp. 1281-1292) | **Verified** |
| `applegate1995` | Yes | Yes | Yes | Yes | Yes (Math. Comp. 64(209), pp. 411-426) | **Verified** |
| `honda2017` | Yes | Yes | Yes | Yes | Yes (IJNC 7(1), pp. 69-85) | **Verified** |
| `oeis_a284668` | Yes | Yes | Yes | N/A (OEIS) | Yes (oeis.org/A284668) | **Verified** |
| `oeis_a006877` | Yes | Yes | Yes | N/A (OEIS) | Yes (oeis.org/A006877) | **Verified** |
| `terras1976` | Yes | Yes | Yes | Yes | Yes (Acta Arith. 30(3), pp. 241-252) | **Verified** |
| `rozier2025` | Yes | Yes | Yes | Yes (arXiv preprint) | Yes (arXiv:2502.00948) | **Verified** |
| `ansari2025` | Yes | Partial**** | Yes | Yes | Yes (NNTDM 31(3), pp. 471-480) | **Minor issue** |

**Notes on minor issues:**

\* `tao2019`: BibTeX lists `year={2019}` (preprint year on arXiv), but the published version appeared in 2022 (Forum of Mathematics, Pi, Vol. 10, e12). The DOI and volume/pages correspond to the 2022 publication. Using the preprint year is a common convention but technically inconsistent with the journal metadata.

\*\* `lagarias2003`: BibTeX title says "(1963--1999)" but the actual arXiv paper title (v9) says "(1963--2000)". The range was expanded in later revisions.

\*\*\* `lagarias2006`: BibTeX says `year={2006}` which is the initial preprint year. The paper was last revised in 2012. Using the original year is standard for arXiv preprints.

\*\*\*\* `ansari2025`: BibTeX lists author as "M. Ansari"; full name is "Mohammad Ansari". Abbreviation is acceptable but not ideal.

**All 18 citations are real, verifiable papers/sources. No fabricated or hallucinated citations detected.** The minor issues are metadata inconsistencies (preprint vs publication year, title revision), not fabrication.

All 20 distinct `\citep{}` commands in the paper resolve to entries in `sources.bib`. No undefined citations.

### 5. Compilation: **5/5**

- `research_paper.pdf` exists (493,976 bytes, dated 2026-03-04).
- LaTeX log shows no errors. Only benign hyperref Unicode warnings (from math symbols in section titles).
- PDF is well-formatted: clean title page, proper equation numbering, tables with booktabs styling, figure references resolve correctly, code listing is properly formatted.

### 6. Writing Quality: **5/5**

The paper is exceptionally well-written for an automated pipeline output:
- Professional academic tone throughout.
- Clear logical flow: Background -> Method -> Setup -> Results -> Discussion -> Conclusion.
- Proper use of theorem environments (Definition, Proposition, Conjecture, Remark).
- The Erdos quote in the introduction is apt and engaging.
- The limitations section (7.3) is commendably honest, acknowledging non-exhaustive search, reliance on external database, and absence of novel algorithms.
- Mathematical notation is consistent and standard.
- The "5-line verification script" framing is excellent for accessibility and reproducibility.

### 7. Figure Quality: **4/5**

All four figures are present in both PNG and PDF formats. Quality assessment:

- **`delay_vs_bitlength.pdf`**: Good. Scatter plot with color-coded points (blue below 10^19, red above), dashed regression line, key records annotated. Proper axis labels, legend, and title. The annotations overlap slightly at high bit-lengths but are still readable.

- **`record_growth_pattern.pdf`**: Good. Two-panel figure with delay vs log10(n) and gap ratios. Proper reference lines (10^19 boundary, median ratio). The gap ratio panel uses green dots on white background — acceptable though the visual could be more polished with better color choices.

- **`trajectory_63728127.pdf`**: Good. Line plot with filled area under curve, red dashed starting-value reference line, proper log-scale y-axis. Clean and informative.

- **`trajectory_9781262575275081247.pdf`**: Good. Same style as above, consistent formatting.

All figures have proper titles, axis labels, and legends. The styling is significantly above default matplotlib — custom colors, dashed reference lines, fill_between effects, annotation callouts. However, the figures could benefit from:
- Slightly larger font sizes for axis labels.
- More refined color palette (the blue/red combination in figure 1 is functional but not publication-polished).
- The gap ratio scatter plot could use slightly larger marker sizes.

These are minor aesthetic concerns, not disqualifying.

---

## Detailed Issues

### Critical Issues

1. **Roosendaal record numbering error (Table 2).** Records in [10^18, 10^19) are numbered #141-#148 in the paper but are actually #138-#145 in the Roosendaal database. This is a systematic +3 offset. The error propagates to the abstract ("delay record #148") and Sections 6.1, 6.3, and 7.1. This must be corrected.

### Moderate Issues

2. **Ambiguous credit for discovery of n*.** The abstract says the authors "identify" the delay champion, but `full_search_results.json` reveals the authors' own search found a maximum delay of only 1,505. The number n* was obtained from Roosendaal's pre-existing database. While Section 7.1 is transparent about this, the abstract and Section 6.1 framing should be revised to make the provenance clearer. Suggested rewording: "We identify, via cross-reference with Roosendaal's database, and independently verify..." rather than just "identify."

3. **Tao (2019) year discrepancy.** The published version is Tao (2022) in Forum of Mathematics, Pi. The bib entry mixes the preprint year with the journal metadata. Should either cite as 2022 with the journal, or as 2019 with arXiv as the venue.

4. **Regression statistics incomplete.** Equation 3 gives slope 41.9 and intercept -271 with R^2 = 0.99, but no standard errors, confidence intervals, or p-values. For a Nature/NeurIPS-tier paper, even descriptive statistics should include uncertainty quantification.

### Minor Issues

5. **Lagarias (2003) title mismatch.** BibTeX says "(1963--1999)" but the paper's latest arXiv version covers 1963--2000.

6. **Inconsistency in regression slope.** The paper reports slope = 41.9 in Equation 3 and Figure 1, but the rubric notes and `trajectory_statistics.json` reference slope = 37.2. The discrepancy likely arises from different regression fits (all 148 records vs. subset), but this should be clarified.

7. **Table 2 lists only 7 intermediate records plus n*, claiming "8 intermediate delay records."** Counting the entries: 1278...855, 1339...727, 2678...454, 3571...273, 4761...697, 5065...735, 5977...855, and 9781...247. That's 8 entries including n* itself, or 7 intermediate records between a(18) and n*. The text says "8 intermediate delay records" between a(18) and n*, which should be "7 intermediate delay records" (or "8 records including n*").

8. **Proposition 1 lacks proof or citation.** The shortcut property is well-known but the paper should either prove it or cite a prior source (e.g., Crandall 1978 or Barina 2021).

---

## Citation Verification Report

| # | Key | Status | Notes |
|---|---|---|---|
| 1 | `tao2019` | **Verified with minor issue** | Real paper. Published 2022 in Forum Math Pi, not 2019. ArXiv preprint 1909.03562 from 2019 is correct. DOI 10.1017/fmp.2022.8 is correct. |
| 2 | `barina2025` | **Verified** | Real paper. J. Supercomputing Vol. 81, art. 810, 2025. DOI 10.1007/s11227-025-07337-0 confirmed on Springer. |
| 3 | `barina2021` | **Verified** | Real paper. J. Supercomputing Vol. 77, pp. 2681-2688. DOI 10.1007/s11227-020-03368-x confirmed on Springer. |
| 4 | `lagarias2003` | **Verified with minor issue** | Real paper. ArXiv math/0309224. Title range evolved from "(1963--1999)" to "(1963--2000)" in later versions. |
| 5 | `lagarias2006` | **Verified** | Real paper. ArXiv math/0608208. Title, author, venue all confirmed. |
| 6 | `lagarias1985` | **Verified** | Real paper. Am. Math. Monthly, Vol. 92, No. 1, pp. 3-23, 1985. DOI 10.2307/2322189 confirmed on JSTOR. |
| 7 | `roosendaal2026` | **Verified** | Real website. ericr.nl/wondrous/ confirmed active with delay records database. |
| 8 | `oliveira2010` | **Verified** | Real book chapter. "The Ultimate Challenge: The 3x+1 Problem," AMS, 2010, pp. 189-207. Confirmed via author's publication page. |
| 9 | `leavens1992` | **Verified** | Real paper. Computers & Mathematics with Applications, Vol. 24, No. 11, pp. 79-99, 1992. DOI 10.1016/0898-1221(92)90034-F confirmed on ScienceDirect. |
| 10 | `kontorovich2005` | **Verified** | Real paper. Acta Arithmetica, Vol. 120, pp. 269-297, 2005. DOI 10.4064/aa120-3-4 confirmed. ArXiv math/0412003 confirmed. |
| 11 | `crandall1978` | **Verified** | Real paper. Mathematics of Computation, Vol. 32, No. 144, pp. 1281-1292, 1978. DOI confirmed on AMS. |
| 12 | `applegate1995` | **Verified** | Real paper. Mathematics of Computation, Vol. 64, No. 209, pp. 411-426, 1995. DOI 10.2307/2153343 confirmed. Part I: Tree-search method. |
| 13 | `honda2017` | **Verified** | Real paper. Int. J. Networking and Computing, Vol. 7, No. 1, pp. 69-85, 2017. DOI 10.15803/ijnc.7.1_69 confirmed. Authors Honda, Ito, Nakano at Hiroshima University. |
| 14 | `oeis_a284668` | **Verified** | Real OEIS entry. oeis.org/A284668. 18 terms listed, by Rahul Chand, 2017, extended by Jens Kruse Andersen, 2021. |
| 15 | `oeis_a006877` | **Verified** | Real OEIS entry. oeis.org/A006877. Delay record holders for 3x+1 problem. 148 terms in table linked to Roosendaal. |
| 16 | `terras1976` | **Verified** | Real paper. Acta Arithmetica, Vol. 30, No. 3, pp. 241-252, 1976. DOI 10.4064/aa-30-3-241-252 confirmed via EuDML. |
| 17 | `rozier2025` | **Verified** | Real paper. ArXiv 2502.00948, submitted Feb 2, 2025, by Olivier Rozier and Claude Terracol. Title and content confirmed. |
| 18 | `ansari2025` | **Verified with minor issue** | Real paper. NNTDM Vol. 31, No. 3, pp. 471-480, 2025. DOI 10.7546/nntdm.2025.31.3.471-480 confirmed. Author abbreviated as "M. Ansari" (full: Mohammad Ansari). |

**Summary:** 18/18 citations verified as real. 0 fabricated. 3 minor metadata issues (year, title revision, author abbreviation). No missing citations.

---

## Overall Verdict: **REVISE**

### Justification

The paper is remarkably well-executed for an automated pipeline: the writing is publication-quality, the central claim is independently verifiable and correct, all citations are real, and the figures are substantially above default styling. The core contribution — identifying and verifying a(19) = 9,781,262,575,275,081,247 with delay 2,426 — is genuine and newsworthy.

However, the verdict is **REVISE** (not REJECT) due to the following issues that must be corrected before acceptance:

1. **Roosendaal record numbering is wrong by +3 throughout.** Table 2, the abstract, and multiple sections refer to records #141-#148 when they should be #138-#145. This is a factual error that undermines the paper's credibility as a careful computational study.

2. **The abstract overstates the authors' computational contribution.** The delay champion was identified by consulting Roosendaal's database, not by the authors' own search (which found a maximum delay of only 1,505). The phrasing should be revised for accuracy.

### Required Revisions (must fix)

- [ ] Fix all Roosendaal record numbers: #141→#138, #142→#139, ..., #148→#145 throughout the paper (abstract, Tables 2, Sections 6.1, 6.3, 7.1).
- [ ] Revise abstract phrasing from "identifies the delay champion" to something like "identifies, via cross-reference with Roosendaal's database, and independently verifies the delay champion."
- [ ] Fix `tao2019` BibTeX year to 2022 (or change venue to arXiv if keeping 2019).
- [ ] Fix `lagarias2003` title from "(1963--1999)" to "(1963--2000)" to match current arXiv version.

### Recommended Revisions (should fix)

- [ ] Add standard errors / confidence intervals to the regression in Equation 3.
- [ ] Resolve the slope discrepancy (41.9 vs 37.2) between the paper and the `trajectory_statistics.json` results file, or clarify which dataset each regression uses.
- [ ] Clarify "8 intermediate delay records" — either the count includes n* (making it 8 total records in the decade) or there are 7 intermediate records plus n* = 8 records.
- [ ] Add a proof sketch or citation for Proposition 1.
- [ ] Consider enlarging axis label fonts in figures for print readability.

### Score Summary

| Criterion | Score |
|---|---|
| Completeness | 5/5 |
| Technical Rigor | 4/5 |
| Results Integrity | 4/5 |
| Citation Accuracy | 4/5 |
| Compilation | 5/5 |
| Writing Quality | 5/5 |
| Figure Quality | 4/5 |
| **Overall** | **31/35** |

All scores are 4+, exceeding the 3+ threshold. The issues identified are correctable in a single revision round. Upon fixing the Roosendaal numbering and abstract phrasing, this paper would merit ACCEPT.
