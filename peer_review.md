# Peer Review: "The Branchless Binary GCD: A Combined Algorithm with Modular Reduction and Lookup Table Acceleration for 64-bit Integers"

**Review Date**: 2026-03-03
**Reviewer**: Automated Peer Review (Nature/NeurIPS Standards)

---

## Overall Verdict: **REVISE**

The paper presents a well-structured and technically sound contribution combining three orthogonal optimizations (initial modular reduction, LUT early termination, and branchless inner loop) into a GCD algorithm that outperforms standard baselines on 64-bit inputs. The experimental methodology is rigorous, with proper statistical testing. However, several issues require revision before acceptance: LaTeX compilation errors, minor citation issues, and some data discrepancies between the paper tables and the underlying CSV data.

---

## Scores by Criterion

| Criterion | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| 1. Completeness | **5** | All required sections present: Abstract, Introduction, Related Work, Background, Method, Experimental Setup, Results, Discussion (with Negative Results), Conclusion, References. Exceptionally thorough. |
| 2. Technical Rigor | **5** | Methods described with formal algorithms (Algorithm 1, 2), equations, critical-path analysis, loop invariant proofs, and termination bounds. Ablation study isolates contributions. Reproducible setup documented. |
| 3. Results Integrity | **4** | Results largely match underlying data (see detailed analysis below). Minor numeric discrepancies between paper tables and CSV data due to different benchmark runs, but all are within reasonable margins and do not affect conclusions. |
| 4. Citation Accuracy | **3** | 15 of 17 cited entries verified. Two issues: (1) `bonzini2024` is unverifiable as a standalone publication; (2) `shallit1993` venue listed as "SIGS" rather than "SIGSAM Bulletin." No fabricated citations. Two entries in sources.bib (`shallit1993`, `skarupke2023`) are never cited in the paper. |
| 5. Compilation | **2** | LaTeX compilation produces 4 errors (missing `$` in .bbl file for `2^{255}-19` in the `pornin2020` note field). PDF is generated (16 pages) but with corrupted rendering near the bibliography. Several overfull hbox warnings. |
| 6. Writing Quality | **5** | Professional academic tone throughout. Clear logical flow from motivation through method to results. Excellent negative results section (Section 7.2). Honest about limitations. Well-structured paragraphs and transitions. |
| 7. Figure Quality | **4** | Publication-quality figures with proper labels, error bars, annotations, consistent color schemes, and meaningful captions. The heatmap (Fig 4) and violin plots (Fig 5) are particularly effective. Minor: Fig 5 (violin) is not referenced in the paper text. |

---

## Detailed Analysis

### 1. Completeness (5/5)

All required sections are present and substantive:
- **Abstract**: Concise, quantitative, with key result (13.7% speedup, 64.8% on skewed).
- **Introduction**: Well-motivated with four clearly stated contributions.
- **Related Work**: Comprehensive coverage of classical GCD, branchless optimizations, and cryptographic GCD.
- **Background**: Includes formal equations, critical-path analysis, and misprediction analysis.
- **Method**: Detailed four-phase algorithm with pseudocode, correctness proof, and termination bound.
- **Experimental Setup**: Five distributions, four baselines, statistical methodology described.
- **Results**: Six tables, four figures, ablation study, 128-bit results, cross-platform analysis.
- **Discussion**: Includes why the algorithm works, six negative results, comparison with prior work, and four stated limitations.
- **Conclusion**: Summarizes findings with future work directions.
- **References**: 17 entries in sources.bib; 15 cited in the paper text.

### 2. Technical Rigor (5/5)

Strengths:
- Formal algorithms (Algorithm 1, 2) with explicit pseudocode.
- Critical-path latency analysis (Equation 4) grounded in real instruction timings.
- Loop invariant proof (Theorem 1) with initialization, maintenance, and termination arguments.
- Termination bound (Theorem 2) via the potential function Phi(a,b) = a+b.
- Ablation study (Table 4) isolating the marginal contribution of each technique.
- Per-iteration cost analysis (Table 6) confirming speedup comes from iteration reduction, not faster iterations.
- Six documented negative results with quantitative explanations.

The statistical methodology is exemplary:
- 50 independent trials per configuration with 100,000 input pairs each.
- Bootstrap 95% confidence intervals (10,000 resamples).
- Wilcoxon signed-rank tests with p < 8.9e-16.
- Cohen's d effect sizes (25.7 to 417.4, all far exceeding d > 0.8).
- One-way ANOVA across distributions.

### 3. Results Integrity (4/5)

**Data verification against results/phase4/full_benchmarks.csv:**

| Paper Claim | CSV Data | Match? |
|-------------|----------|--------|
| Combined uniform: 86.6 ns | `combined,64,uniform,median_ns=86.57` | Yes (rounded) |
| Stein's Classic uniform: 100.4 ns | `stein_classic,64,uniform,median_ns=100.35` | Yes (rounded) |
| Combined skewed: 27.8 ns | `combined,64,skewed,median_ns=27.78` | Yes (rounded) |
| Euclidean uniform: 175.3 ns | `euclid,64,uniform,median_ns=175.26` | Yes (rounded) |
| Combined 128-bit uniform: 601.1 ns | `combined_128,128,uniform,median_ns=601.07` | Yes (rounded) |
| Stein 128-bit uniform: best baseline at 568.7 ns | `stein_classic,128,uniform,median_ns=619.54` | **Minor discrepancy** |

**Issue**: Table 5 (128-bit) claims "568.7 (Stein)" as the best baseline for 128-bit uniform, but `full_benchmarks.csv` shows `stein_classic,128,uniform,median_ns=619.54`. The 568.7 figure is not found in the CSV. This may come from the statistical_analysis.md which reports 568.68 for stein_classic 128-bit uniform. The discrepancy appears to be between two different benchmark runs (20 trials in full_benchmarks.csv vs 50 trials in raw_trials.csv). This should be reconciled.

**Verification against results/phase4/statistical_analysis.md:**

The statistical analysis document shows:
- combined uniform: 86.89 ns (median from 50-trial raw data)
- stein_classic uniform: 99.00 ns (median from 50-trial raw data)

The paper reports 86.6 and 100.4 respectively. These differ because the paper appears to use the 20-trial full_benchmarks.csv while the statistical analysis uses 50-trial raw_trials.csv. The speedup ratio is consistent: 1.139x (statistical_analysis) vs 1.139x (paper Table 2). The difference in absolute numbers (86.6 vs 86.89, 100.4 vs 99.0) is within normal run-to-run variation.

**Figure verification**: Figures 1-4 visually match the data in the CSV files. The bar heights in Fig 1 match the values annotated on the bars (175.3, 100.3, 189.7, 190.2, 91.2, 92.5, 87.2, 86.7, 91.8, 86.6), which align with full_benchmarks.csv within rounding.

### 4. Citation Accuracy (3/5)

#### Citation Verification Report

| Entry Key | Title | Authors | Year | Venue | DOI/URL | Status |
|-----------|-------|---------|------|-------|---------|--------|
| `stein1967` | "Computational Problems Associated with Racah Algebra" | Josef Stein | 1967 | J. Computational Physics, 1(3):397-405 | 10.1016/0021-9991(67)90047-2 | **VERIFIED** via ScienceDirect. Correct title, author, year, journal, pages, DOI. |
| `bernsteinyang2019` | "Fast Constant-Time GCD Computation and Modular Inversion" | Daniel J. Bernstein, Bo-Yin Yang | 2019 | TCHES 2019(3):340-398 | 10.46586/tches.v2019.i3.340-398 | **VERIFIED** via TCHES, ePrint, ResearchGate. All fields correct. |
| `pornin2020` | "Optimized Binary GCD for Modular Inversion" | Thomas Pornin | 2020 | ePrint 2020/972 | eprint.iacr.org/2020/972 | **VERIFIED** via IACR ePrint. Correct title, author, year, URL. 6253 cycles claim confirmed. |
| `knuth1997` | "The Art of Computer Programming, Vol. 2" | Donald E. Knuth | 1997 | Addison-Wesley, 3rd ed. | N/A | **VERIFIED**. Standard reference, correct edition and publisher. |
| `sreedhar2022` | "A Fast Large-Integer Extended GCD Algorithm and Hardware Design..." | Kavya Sreedhar, Mark Horowitz, Christopher Torng | 2022 | TCHES 2022(4):163-187 | 10.46586/tches.v2022.i4.163-187 | **VERIFIED** via TCHES. All fields correct. |
| `bos2014` | "Constant Time Modular Inversion" | Joppe W. Bos | 2014 | J. Cryptographic Engineering, 4(4):275-281 | 10.1007/s13389-014-0084-8 | **VERIFIED** via Springer. All fields correct. |
| `slotin2022` | "Binary GCD" | Sergey Slotin | 2022 | Algorithmica.org | en.algorithmica.org/hpc/algorithms/gcd/ | **VERIFIED** via Algorithmica.org. URL resolves, content matches description. |
| `lemire2013` | "Fastest Way to Compute the Greatest Common Divisor" | Daniel Lemire | 2013 | Blog post | lemire.me/blog/2013/12/26/... | **VERIFIED** via Lemire's blog. URL resolves, 55% speedup claim present. |
| `lemire2024` | "Greatest Common Divisor, the Extended Euclidean Algorithm, and Speed!" | Daniel Lemire | 2024 | Blog post | lemire.me/blog/2024/04/13/... | **VERIFIED** via Lemire's blog. URL resolves, mentions binary GCD and Bonzini variant. |
| `zeng2016` | "lib: GCD: Use binary GCD algorithm instead of Euclidean" | Zhaoxiu Zeng | 2016 | Linux kernel patch V4 | marc.info/?t=146252829800002 | **VERIFIED** via Linux kernel mailing lists (MARC, spinics.net). Correct author, title, year. |
| `libcxxD145982` | "[libc++] Implement std::gcd using the binary version" | Serge Sans Paille | 2023 | LLVM Phabricator | reviews.llvm.org/D145982 | **VERIFIED** via LLVM Phabricator. Correct author, patch number, year. |
| `libstdcxxgcd2024` | "[PATCH] libstdc++: Optimize std::gcd" | Stephen Face | 2024 | GCC mailing list | gcc.gnu.org/pipermail/libstdc++/2024-June/058977.html | **VERIFIED** via GCC mailing list. Correct author (Stephen Face, shpface@gmail.com), URL resolves, 2024 date confirmed. |
| `fog2024` | "Instruction Tables: Lists of Instruction Latencies..." | Agner Fog | 2024 | agner.org | agner.org/optimize/instruction_tables.pdf | **VERIFIED** via agner.org. Standard reference, continuously updated (latest version is 2025). Year "2024" is acceptable for the version consulted. |
| `intel2024` | "Intel 64 and IA-32 Architectures Optimization Reference Manual" | Intel Corporation | 2024 | Intel | intel.com/content/... | **VERIFIED** via Intel. Standard reference. URL resolves to Intel's download page. |
| `abel2022` | "uops.info: Characterizing Latency, Throughput, and Port Usage..." | Andreas Abel, Jan Reineke | 2022 | uops.info | uops.info/ | **VERIFIED** with caveat. The actual ASPLOS paper is from 2019 (ASPLOS '19, DOI 10.1145/3297858.3304062). The bib entry lists year 2022, referring to the website. This is acceptable for a continuously-updated web resource, but the publication year is technically 2019. |
| `bonzini2024` | "Binary GCD No-Swap Variant" | Paolo Bonzini | 2024 | N/A (no URL, no DOI) | N/A | **UNVERIFIABLE**. No standalone publication found. Paolo Bonzini is a known QEMU/KVM developer and GCC contributor, and the "no-swap variant" is referenced in Lemire's 2024 blog post as an informal contribution. There is no URL, DOI, or publication venue. This appears to be a personal communication or informal contribution rather than a published work. |
| `barenghi2020` | "A Comprehensive Analysis of Constant-time Polynomial Inversion for Post-quantum Cryptosystems" | Alessandro Barenghi, Gerardo Pelosi | 2020 | ACM Computing Frontiers (CF '20) | 10.1145/3387902.3397224 | **VERIFIED** via ACM, Politecnico di Milano. Correct title, authors, year, DOI. |

**Uncited entries in sources.bib** (present in .bib but never `\cite`d in paper):
- `shallit1993`: "A Binary Algorithm for the Jacobi Symbol" by Shallit and Sorenson. **VERIFIED** as a real paper (SIGSAM Bulletin, 27(1):4-11, 1993), but the venue in the bib entry is listed as "SIGS" rather than "SIGSAM Bulletin." Since it's uncited, this is a minor housekeeping issue.
- `skarupke2023`: "Beautiful Branchless Binary Search" by Malte Skarupke. **VERIFIED** via probablydance.com (April 27, 2023). Not cited in the paper but present in sources.bib.

#### Summary of Citation Issues:
1. `bonzini2024` cannot be verified as a standalone published work. It should either be given a URL (e.g., to a specific commit, email, or code comment) or cited as a personal communication.
2. `abel2022` lists year 2022 but the publication (ASPLOS) is from 2019. Acceptable for a web resource reference, but worth noting.
3. `shallit1993` venue should be "SIGSAM Bulletin" not "SIGS" (minor, and uncited in paper anyway).
4. Two unused bib entries (`shallit1993`, `skarupke2023`) could be removed for cleanliness.

### 5. Compilation (2/5)

**Critical Issue**: The LaTeX log reveals 4 compilation errors:

```
! Missing $ inserted.
l.114   2^{255}-19 on Coffee Lake.
! Missing $ inserted.
l.115
! Missing } inserted.
l.115
! Extra }, or forgotten \endgroup.
```

These errors originate from the `note` field of the `pornin2020` entry in `sources.bib`, which contains `2^{255}-19` without proper LaTeX math mode escaping. The text should be `$2^{255}-19$` or the braces should be escaped.

The PDF is generated (16 pages, 380KB) despite these errors, but the bibliography rendering near the `pornin2020` entry is corrupted. Additionally, there are 5 overfull hbox warnings, one of which is significant (78pt too wide at line 558-559 for the `-march=native/skylake/znver2` text).

**Action Required**: Fix the `pornin2020` note field in `sources.bib` to use proper math mode for `$2^{255}-19$`, then recompile. Fix the overfull hbox at line 558 with a line break or rewording.

### 6. Writing Quality (5/5)

The writing is clear, precise, and professional:
- Technical claims are well-supported with quantitative evidence.
- The paper honestly reports where the combined algorithm loses (e.g., Euclidean beats it on coprime inputs; 128-bit results are mixed).
- The negative results section (Section 7.2) is exemplary -- six approaches that failed, each with quantitative explanation. This is rarely seen and highly valuable.
- The limitations section is frank and comprehensive.
- Future work directions are concrete and well-motivated.

Minor suggestions:
- The abstract states "13.7% speedup" while the paper body consistently reports values between 12.2% (Table 2) and 13.7% (abstract). The 13.7% matches the Fibonacci distribution speedup, but the uniform distribution speedup is 12.2%. The abstract should clarify which distribution the 13.7% refers to, or use "12-14%."
- Figure 5 (violin distributions) is generated but never referenced in the paper text. Either add a reference or remove it.

### 7. Figure Quality (4/5)

The figures are well above average quality:
- **Fig 1** (64-bit uniform bar chart): Clean, annotated with exact values, error bars showing p5-p95 range, dashed reference line for Stein's baseline, consistent color scheme progressing from dark (baselines) to warm (novel).
- **Fig 2** (distribution comparison): Grouped bar chart with 4 algorithms x 5 distributions, error bars, legend, clear labels.
- **Fig 3** (128-bit uniform): Same style as Fig 1, honest about the combined algorithm not winning at 128-bit uniform.
- **Fig 4** (speedup heatmap): Excellent use of diverging color scale (green = faster, orange/red = slower), annotations with exact speedup ratios and percentages, dual-row layout for 64-bit vs 128-bit.
- **Fig 5** (violin plots): Good use of violin/KDE distributions showing trial-level variance. Shows the low variance and clear separation between algorithms.

The only minor issue is that Fig 5 is never referenced in the paper text.

---

## Specific Actionable Feedback for Revision

### Must Fix (Blocking)

1. **Fix LaTeX compilation errors**: In `sources.bib`, the `note` field of `pornin2020` entry contains `2^{255}-19` without math mode. Change to `$2^{255}-19$` (wrapped in braces for BibTeX: `{$2^{255}-19$}`). Recompile with `pdflatex -> bibtex -> pdflatex -> pdflatex`.

2. **Fix overfull hbox at line 558**: The `-march=native/skylake/znver2` text extends 78pt beyond the margin. Add a line break or rephrase (e.g., use `\mbox{\texttt{-march=\{native, skylake, znver2\}}}`).

3. **Reconcile 128-bit data discrepancy**: Table 5 claims "568.7 (Stein)" as best baseline for 128-bit uniform, but `full_benchmarks.csv` shows 619.5 ns. Clarify which benchmark run is being referenced, or update the table to match the CSV.

### Should Fix (Important)

4. **Fix `bonzini2024` citation**: Add a URL or other verifiable reference (e.g., a link to the specific code, commit, or Lemire blog post where this variant is described). Alternatively, cite it as "personal communication" or fold the reference into the `lemire2024` citation.

5. **Reference Fig 5**: The violin distribution plot is generated and included in figures/ but never referenced in the paper text. Add a reference in Section 6.2 (Statistical Significance) or Section 6.1.

6. **Clarify abstract speedup figure**: The abstract says "13.7% speedup" which matches Fibonacci, not uniform (12.2%). Either specify the distribution or use a range "12-65%."

### Nice to Fix (Minor)

7. **Fix `abel2022` year**: The ASPLOS paper is from 2019. Consider citing as `abel2019` with the ASPLOS venue, or keeping as 2022 with explicit "website, accessed 2022" language.

8. **Remove unused bib entries**: `shallit1993` and `skarupke2023` are defined in `sources.bib` but never cited. Remove for cleanliness, or cite them somewhere (e.g., Related Work).

9. **Fix `shallit1993` venue**: Change "SIGS" to "SIGSAM Bulletin" if this entry is retained.

10. **Add author information**: The `\author{}` field in the .tex file is empty. Add author names and affiliations for a complete paper.

---

## Summary

This is a strong engineering contribution with rigorous experimental methodology, honest reporting of both positive and negative results, and clear writing. The combined algorithm's approach of targeting different phases of the GCD computation (initial convergence, middle phase, final convergence) with different techniques is well-motivated and convincingly evaluated.

The main reasons for the REVISE verdict are:
1. LaTeX compilation errors that corrupt the bibliography (Score 2/5 on Compilation -- below the 3+ threshold).
2. An unverifiable citation (`bonzini2024`) that lacks any URL, DOI, or publication venue.
3. A data discrepancy in the 128-bit results table.

All issues are straightforward to fix. After addressing items 1-5 above, the paper would meet the acceptance threshold.
