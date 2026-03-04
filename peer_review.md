# Peer Review: Algebraic Sieving and Lookup-Table Acceleration for Collatz Delay Record Search

**Reviewer:** Automated Peer Review Agent (Nature/NeurIPS standard)  
**Date:** March 4, 2026  
**Paper:** "Algebraic Sieving and Lookup-Table Acceleration for Collatz Delay Record Search: A Reproducible Framework with Independent Verification Through 10^{12}"

---

## Criterion Scores (1-5)

| Criterion | Score | Notes |
|-----------|-------|-------|
| 1. Completeness | **5/5** | All required sections present: Abstract, Introduction, Related Work, Background & Preliminaries, Method, Experimental Setup, Results, Discussion, Conclusion, References |
| 2. Technical Rigor | **4/5** | Methods properly described with equations (Eqs. 1-5), formal definitions, lemma with proof, algorithm pseudocode. Minor: no formal complexity analysis of the combined pipeline |
| 3. Results Integrity | **5/5** | All 12 per-decade records independently verified by this reviewer via deterministic Python computation. Figures match data in results/. No fabricated results |
| 4. Citation Accuracy | **4/5** | All 19 citations verified via web search. One minor issue: Tao (2019) year is the arXiv date, but journal publication was 2022 (Forum Math Pi Vol 10, e12). DOI correctly points to 2022 publication. See detailed report below |
| 5. Compilation | **5/5** | PDF compiled cleanly (1.33 MB, 12 pages). Only 2 minor hyperref warnings about Unicode tokens in PDF strings. Zero errors, zero undefined citations |
| 6. Writing Quality | **5/5** | Professional academic tone throughout. Clear logical flow from background to method to experiments to discussion. Honest about limitations (not exhaustive beyond 10^7, no new records claimed). Well-structured paragraphs with proper transitions |
| 7. Figure Quality | **4/5** | Three publication-quality figures with proper labels, legends, color palettes, and captions. Non-default matplotlib styling used (seaborn-like palette). Minor: stopping_time_distribution.png right panel (scatter) could benefit from a denser color map rather than flat green dots |

**Overall Score: 32/35 (91.4%)**

---

## Overall Verdict: **ACCEPT**

### Justification

This is a well-crafted, technically sound paper that makes a clear methodological contribution: a reproducible, zero-dependency Python framework for Collatz delay record search and verification. The paper is honest about what it does and does not achieve — it explicitly disclaims discovery of new records and positions itself as an independent verification and reference implementation study. All numerical claims have been independently verified by this reviewer through deterministic computation. The writing is clean, the figures are publication-quality, all 19 citations are real and correctly attributed (with one minor year discrepancy), and the paper compiles without errors.

---

## Detailed Review

### Strengths

1. **Exceptional reproducibility.** The paper provides a 3-line Python one-liner that anyone can use to verify the headline result (989,345,275,647 → 1,348 steps). The standalone verification script has zero dependencies. This is the gold standard for computational reproducibility.

2. **Honest framing.** The paper does not overclaim. It clearly states that no new delay records were found and explains why (Roosendaal's project has exhaustively searched to ~3.59 × 10^16). The contribution is methodological, not record-breaking.

3. **Strong related work.** 19 references covering foundational theory (Lagarias, Wirsching, Tao), computational verification (Barina, Honda, Silva), probabilistic models (Sinai, Polli), and modern sieving (Dutta, Getachew, Angeltveit). The coverage is comprehensive and up-to-date through 2026.

4. **Sound methodology.** The three-pronged optimization (mod-9 filter, algebraic sieve at depth k=15, 16-bit lookup table) is well-motivated and correctly described. The symbolic simulation of Collatz steps via the (a, b, e) coefficients in Eq. (3) is standard but clearly presented. Algorithm 1 is reproducible pseudocode.

5. **Verified numerical claims.** This reviewer independently computed:
   - All 12 per-decade champions (Table 4) match exactly
   - Peak values for path coalescence claim verified (63,728,127 and 670,617,279 both peak at 966,616,035,460)
   - The 205-step improvement claim for #59 verified (previous record 36,791,535 has st=744)
   - Neighbor record 9,780,657,631 confirmed at st=1,132

### Weaknesses

1. **Tao (2019) year attribution.** The BibTeX entry lists year=2019 (arXiv submission date) but the DOI `10.1017/fmp.2022.8` points to the 2022 journal publication in Forum of Mathematics, Pi, Vol. 10, e12. The volume=10 and pages=e12 metadata are from the 2022 publication, creating an inconsistency. This should be updated to year=2022 with a note about the 2019 arXiv preprint, or the entry should be split into arXiv (2019) and journal (2022) versions.

2. **Benchmark range limitations.** The 13.3× speedup is measured only on [1, 10^7]. For larger ranges where big-integer arithmetic dominates, the lookup table speedup may degrade due to Python's arbitrary-precision integer overhead. The paper acknowledges this ("dominated by big-integer multiplication for large values") but does not provide empirical measurements at larger ranges.

3. **No comparison with same-language baselines.** The paper compares Python throughput against C/CUDA implementations (Barina, Honda, Dutta), which conflates algorithmic vs. language-level differences. A more informative comparison would port the same sieve+lookup algorithm to C to isolate the algorithmic contribution.

4. **"Concept evolution tree" discussion.** Section 6 mentions a "concept evolution tree" that identified 12 techniques, of which 7 were implemented. This reads as process documentation rather than scientific contribution and is somewhat out of place in a research paper. Consider moving to an appendix or removing.

5. **Missing formal analysis.** The paper lacks a formal theorem or proposition establishing the sieve's correctness (i.e., that no delay record is eliminated). While Lemma 1 provides the foundation and the empirical check passes, a formal correctness proof for the combined sieve+mod-9 filter would strengthen the paper.

### Minor Issues

- Table 4, row for 10^9: peak value 966,616,035,460 matches 10^8 champion. This is correctly noted in the Observations section but could be annotated directly in the table.
- The paper states the verification script is 149 lines (abstract, Sec 5) but the code files in the repository show different sizes for different versions. Ensure consistency.
- Line 156: "Barina 2025" verified convergence to 2^71 but the paper says 2^71 ≈ 2.36 × 10^21. Correct: 2^71 ≈ 2.361 × 10^21. ✓

---

## Citation Verification Report

All 19 entries in `sources.bib` were verified via web search. Results:

| # | Citation Key | Title | Authors | Year | Venue | Verification |
|---|-------------|-------|---------|------|-------|-------------|
| 1 | `lagarias1985` | The 3x+1 problem and its generalizations | Jeffrey C. Lagarias | 1985 | American Mathematical Monthly 92(1):3-23 | **VERIFIED** ✓ — Found on JSTOR, DOI 10.2307/2322189 matches |
| 2 | `lagarias2010` | The Ultimate Challenge: The 3x+1 Problem | Jeffrey C. Lagarias (editor) | 2010 | AMS Press | **VERIFIED** ✓ — Found on AMS bookstore, Google Books. ISBN 978-0-8218-4940-8 |
| 3 | `lagarias2021overview` | The 3x+1 Problem: An Overview | Jeffrey C. Lagarias | 2021 | arXiv:2111.02635 | **VERIFIED** ✓ — Found on arXiv, submitted Nov 4 2021 |
| 4 | `wirsching1998` | The Dynamical System Generated by the 3n+1 Function | Günther J. Wirsching | 1998 | Springer LNM vol. 1681 | **VERIFIED** ✓ — Found on Springer, DOI 10.1007/BFb0095985 matches |
| 5 | `tao2019` | Almost all orbits of the Collatz map attain almost bounded values | Terence Tao | 2019 (arXiv) / 2022 (journal) | Forum of Mathematics, Pi, 10:e12 | **VERIFIED with NOTE** — Paper exists. arXiv preprint Sept 2019, published in journal 2022. Year should be 2022 for journal version. DOI 10.1017/fmp.2022.8 correct |
| 6 | `silva1999` | Maximum excursion and stopping time record-holders for the 3x+1 problem | Tomás Oliveira e Silva | 1999 | Mathematics of Computation 68(225):371-384 | **VERIFIED** ✓ — Found on AMS, DOI 10.1090/S0025-5718-99-01031-5 matches |
| 7 | `barina2021` | Convergence verification of the Collatz problem | David Bařina | 2021 | J. Supercomputing 77(3):2681-2688 | **VERIFIED** ✓ — Found on Springer, DOI 10.1007/s11227-020-03368-x matches |
| 8 | `barina2025` | Improved verification limit for the convergence of the Collatz conjecture | David Bařina | 2025 | J. Supercomputing 81(7) | **VERIFIED** ✓ — Found on Springer (open access), DOI 10.1007/s11227-025-07337-0 matches. Published May 2025 |
| 9 | `angeltveit2026` | An improved algorithm for checking the Collatz Conjecture for all n < 2^N | Vigleik Angeltveit | 2026 | arXiv:2602.10466 | **VERIFIED** ✓ — Found on arXiv, submitted Feb 11 2026 |
| 10 | `honda2017` | GPU-accelerated Exhaustive Verification of the Collatz Conjecture | Takumi Honda, Yasuaki Ito, Koji Nakano | 2017 | Int. J. Networking & Computing 7(1):69-85 | **VERIFIED** ✓ — Found on J-STAGE, DOI 10.15803/ijnc.7.1_69 matches |
| 11 | `czarnul2023` | A multithreaded CUDA and OpenMP based power-aware programming framework for multi-node GPU systems | Paweł Czarnul | 2023 | Concurrency and Computation: Practice and Experience | **VERIFIED** ✓ — Found on ResearchGate/Wiley, DOI 10.1002/cpe.7897 matches. Uses Collatz as benchmark application |
| 12 | `getachew2025` | Efficient Computation of Collatz Sequence Stopping Times: A Novel Algorithmic Approach | Eyob Getachew, Beakal Gizachew Assefa | 2025 | IEEE Access | **VERIFIED** ✓ — Found on arXiv (2501.04032) and IEEE Access, DOI 10.1109/ACCESS.2025.3548031 matches |
| 13 | `dutta2025` | Chronological Verification of the Collatz Conjecture Using Theoretically Proven Sieves | Samrat Dutta | 2025 | EJMAA 13(1) | **VERIFIED** ✓ — Found on EJMAA journal and ResearchGate. DOI 10.21608/ejmaa.2025.334871.1289 |
| 14 | `leavens1992` | 3x+1 Search Programs | Gary T. Leavens, Mike Vermeulen | 1992 | Computers & Mathematics with Applications 24(11):79-99 | **VERIFIED** ✓ — Found on ScienceDirect, DOI 10.1016/0898-1221(92)90034-F matches |
| 15 | `polli2024` | Stochastic-like characteristics of arithmetic dynamical systems: the Collatz hailstone sequences | J.G. Polli, E.P. Raposo, G.M. Viswanathan, M.D. da Luz | 2024 | Journal of Physics: Complexity | **VERIFIED** ✓ — Found on IOP/ADS, DOI 10.1088/2632-072X/ad271f matches |
| 16 | `sinai2003` | Uniform Distribution in the (3x+1)-Problem | Yakov G. Sinai | 2003 | Moscow Mathematical Journal 3(4):1429-1440 | **VERIFIED** ✓ — Found on mathnet.ru, DOI 10.17323/1609-4514-2003-3-4-1429-1440 matches |
| 17 | `roosendaal2025` | On the 3x+1 Problem: Delay Records | Eric Roosendaal | 2025 | Online: ericr.nl/wondrous/delrecs.html | **VERIFIED** ✓ — Website live, last modified December 24, 2025 |
| 18 | `oeis_a006877` | OEIS A006877 | OEIS Foundation | 2024 | oeis.org/A006877 | **VERIFIED** ✓ — Sequence exists with 148 terms. Description matches: "values set new records for number of steps to reach 1" |
| 19 | `oeis_a284668` | OEIS A284668 | OEIS Foundation | 2024 | oeis.org/A284668 | **VERIFIED** ✓ — Sequence exists with 18 terms. Data matches paper's Table 4 exactly |

**Citation Summary:** 18/19 citations fully verified. 1/19 has a minor year discrepancy (Tao 2019 vs 2022) but the paper itself, DOI, and all other metadata are correct. **No fabricated, hallucinated, or incorrect citations found.**

---

## Independent Numerical Verification

The reviewer independently computed the following using `n = X; steps = 0; while n != 1: n = 3*n+1 if n%2 else n//2; steps += 1`:

| N | Paper claims st= | Reviewer computed st= | Match |
|---|---|---|---|
| 9 | 19 | 19 | ✓ |
| 27 | 111 | 111 | ✓ |
| 97 | 118 | 118 | ✓ |
| 871 | 178 | 178 | ✓ |
| 6,171 | 261 | 261 | ✓ |
| 77,031 | 350 | 350 | ✓ |
| 837,799 | 524 | 524 | ✓ |
| 8,400,511 | 685 | 685 | ✓ |
| 63,728,127 | 949 | 949 | ✓ |
| 670,617,279 | 986 | 986 | ✓ |
| 9,780,657,630 | 1,132 | 1,132 | ✓ |
| 9,780,657,631 | 1,132 | 1,132 | ✓ |
| 75,128,138,247 | 1,228 | 1,228 | ✓ |
| 989,345,275,647 | 1,348 | 1,348 | ✓ |

**Peak value verification:**
- 63,728,127 → max = 966,616,035,460 ✓ (matches paper)
- 670,617,279 → max = 966,616,035,460 ✓ (path coalescence confirmed)
- 989,345,275,647 → max = 1,219,624,271,099,764 ✓ (matches 1.22 × 10^15)
- 36,791,535 → st = 744, confirming 205-step improvement to 949 ✓

**All results verified. Zero discrepancies found.**

---

## Recommendations for Improvement (non-blocking)

1. Fix Tao year: Change `year={2019}` to `year={2022}` in `sources.bib` and add `note={arXiv preprint September 2019}`.
2. Add a larger-range benchmark (e.g., [1, 10^9]) to characterize how the speedup degrades with big-integer arithmetic overhead.
3. Remove or relocate the "concept evolution tree" paragraph from the Discussion section.
4. Add a formal correctness proposition for the combined sieve, proving zero false negatives for delay records above n_min.
5. Consider adding error bars or timing variance to the throughput benchmarks in Table 2.

---

## Figures Assessment

1. **trajectory_comparison.png** — Publication quality. Three trajectories with distinct colors (blue/orange/green), log₂ scale y-axis, proper axis labels, legend with stopping times. Clean seaborn-style aesthetic.

2. **records_scaling.png** — Publication quality. Semi-log scale, blue dots for data points, dashed gray heuristic line, clean legend. Effectively communicates the logarithmic scaling relationship.

3. **stopping_time_distribution.png** — Good quality. Two-panel figure (histogram + scatter). Histogram uses warm orange with proper axis labels and a red dashed max line. Scatter panel uses green dots. Minor: scatter panel could use density coloring for better readability.

All three figures use non-default styling and are suitable for publication.

---

**Final Verdict: ACCEPT**

This paper meets all criteria for acceptance at a score of 3+ across all seven dimensions. It is a well-executed, honest, reproducible study that independently verifies known Collatz delay records through a novel combination of algebraic sieving and lookup-table acceleration. The citations are comprehensive and verified. The results are deterministically reproducible. The writing is professional.
