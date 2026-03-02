# Peer Review: "The 2-adic Linear Variance Law: Quantifying Determinism in Collatz Dynamics via Arithmetic Variance Decomposition"

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-03-02
**Verdict:** **REVISE**

---

## Scores (1--5)

| Criterion | Score | Notes |
|---|---|---|
| 1. Completeness | **4** | All required sections present and well-structured |
| 2. Technical Rigor | **3** | Methods sound, but key claims have scientific issues (see below) |
| 3. Results Integrity | **2** | Internal data inconsistencies; central claim's robustness is overstated |
| 4. Citation Accuracy | **2** | Multiple factual errors in sources.bib (wrong author initials, wrong DOI, wrong entry types) |
| 5. Compilation | **5** | LaTeX compiles without errors or warnings; PDF is well-formatted |
| 6. Writing Quality | **4** | Professional tone, clear arguments, logical flow, good use of tables |
| 7. Figure Quality | **3** | Figures are adequately styled with labels/legends, but key Lyapunov figure is misleading |

**Overall: 4 + 3 + 2 + 2 + 5 + 4 + 3 = 23/35 (avg 3.3). Two criteria below 3 => REVISE.**

---

## 1. Completeness (Score: 4/5)

All required sections are present: Abstract, Introduction, Related Work (Section 2), Background & Preliminaries (Section 3), Method (Section 4), Experimental Setup (Section 5), Results (Section 6), Discussion (Section 7), Conclusion (Section 8), Acknowledgments, References, and Appendix. The paper is well-organized with clear signposting between sections.

**Minor:** The Related Work section is thorough but could benefit from a more explicit discussion of existing ANOVA/variance decomposition work in number theory beyond the Collatz domain to contextualize the methodology.

---

## 2. Technical Rigor (Score: 3/5)

### Strengths
- The ANOVA variance decomposition methodology (Section 4.1) is clearly described with proper equations.
- The Lyapunov exponent definition (Equation 3, Algorithm 1) is rigorous and reproducible.
- The null-model debunking of modular resonance (Section 6.4) is methodologically excellent and a genuine contribution to computational number theory practice.
- Bonferroni correction is properly applied across 7 comparisons.

### Weaknesses

**W1: The "Linear Variance Law" may be a finite-size artifact.** The slope alpha decreases monotonically with n_max (Table 5):
- n=10^4: 0.0371
- n=5x10^4: 0.0209
- n=10^5: 0.0191
- n=5x10^5: 0.0130
- n=10^6: 0.0119

The slope has NOT stabilized at n=10^6 -- it dropped from 0.0130 to 0.0119 between 5x10^5 and 10^6 (an 8.5% decrease). The paper claims "The slope stabilizes near 0.012 for n_max >= 5x10^5" but this is not supported by the data. The slope could plausibly converge to 0 as n_max -> infinity, which would mean the "law" is a finite-size effect rather than an asymptotic property. This possibility is not adequately discussed.

**W2: Linearity breaks down for k > 12.** The paper restricts the linear fit to k=1..12 (R^2 of fit = 0.994), but the actual data (deep_dive.json) shows the marginal R^2 increases dramatically for k > 12:
- k=12: marginal R^2 = 0.0127
- k=13: marginal R^2 = 0.0142
- k=14: marginal R^2 = 0.0177
- k=15: marginal R^2 = 0.0235
- k=16: marginal R^2 = 0.0367
- k=17: marginal R^2 = 0.0614

The full-range fit (k=1..17) has R^2 = 0.9355, substantially lower than the selective k=1..12 fit. This super-linear growth for large k undermines the "linear law" claim. It may indicate that the relationship is actually sub-linear with eventual super-linear correction -- qualitatively different from the conjecture stated.

**W3: The Terras connection understates prior knowledge.** The paper acknowledges (Section 7.1) that Terras (1976) proved the first k bits of n determine the first k steps. This is a DETERMINISTIC relationship. The ANOVA R^2 growing with k is a natural and expected consequence. The novelty claim rests on the linearity, which (per W1 and W2) is not robustly established.

---

## 3. Results Integrity (Score: 2/5)

### Data Inconsistencies

**I1: Lyapunov exponent mean -- contradictory data files.** The paper (Section 6.2) reports mean lambda = 1.2 x 10^-4 at n_max = 10^5, consistent with `results/lyapunov_results.json` (mean_lyapunov = 0.000123). However, `results/scale_invariance.json` reports mean_lyapunov = -0.126 at the SAME scale (n_max = 100,000). These differ by three orders of magnitude and have opposite signs. This indicates two different Lyapunov computations were used (likely the derivative-based formula in the paper vs. the transfer matrix approach), but the paper does not acknowledge or reconcile this inconsistency. The skewness/kurtosis values are consistent between the two, so the non-Gaussianity finding is robust, but the mean value discrepancy is concerning.

**I2: Figure/text mismatch for R^2 fit.** The main R^2 figure (deep_dive_r2.png) displays the fit line "R^2 = 0.0147k + -0.0173" (the k=1..17 fit with R^2 = 0.9355), but the paper text states "The linear fit R^2(k) = 0.0119k - 0.0011 achieves R^2 = 0.994 for k=1,...,12." The figure shows one fit; the text describes a different one. This is confusing and potentially misleading -- readers will see data clearly deviating from the line at k > 12 while reading about R^2 = 0.994.

**I3: Scale slope at n=10^4 -- inconsistent data sources.** `deep_dive.json` reports slope = 0.02882 at n=10^4, while `scale_invariance.json` reports slope = 0.03708 at n=10^4. The paper's Table 5 uses 0.0371 (matching scale_invariance.json). The 29% discrepancy between two data files at the same scale is unexplained.

### Verified Claims
- R^2 values in Table 2 match `deep_dive.json` r2_by_k entries exactly.
- 3-adic control values (Table 3) match `deep_dive.json` r2_3adic entries.
- Phase transition data (Table 6) is consistent with `results/phase_transition.json`.
- Modular resonance debunking data (Table 7) matches `results/significance.json`.
- KS statistics and skewness in Table 4 match `results/scale_invariance.json`.

---

## 4. Citation Accuracy (Score: 2/5)

### Citation Verification Report

Each of the 16 entries in `sources.bib` was verified via web search. Results below.

#### Fully Verified (4/16)

| Key | Status |
|---|---|
| `lagarias2021` | CORRECT. arXiv preprint, all fields accurate. |
| `siegel2024` | CORRECT. arXiv preprint, all fields accurate. |
| `santana2026` | CORRECT. arXiv preprint, all fields accurate. Note: unreviewed preprint. |
| `barina2025` | CORRECT. All fields verified against published article. |

#### Verified with Minor Issues (9/16)

| Key | Issue |
|---|---|
| `tao2019` | Year 2019 is the preprint date; the journal publication in *Forum of Mathematics, Pi* is 2022 (DOI: 10.1017/fmp.2022.8). Entry lists journal name but uses preprint year -- inconsistent. |
| `lagarias1985` | Missing `journal` field. Should be "The American Mathematical Monthly." |
| `kontorovich2009` | Entry type `@article` is incorrect; this is a book chapter in *The Ultimate Challenge: The 3x+1 Problem* (AMS, 2010). Should be `@incollection`. |
| `terras1976` | Missing `journal` field. Should be "Acta Arithmetica." |
| `wirsching1998` | Entry type `@article` is incorrect; this is a **book** (Lecture Notes in Mathematics, Vol. 1681, Springer, 1998). Should be `@book`. |
| `barina2020` | Year 2020 is the online-first date; volume year is 2021 (J. Supercomput. 77). Minor. |
| `mori2024` | Year 2024 is the preprint date; the journal publication in *Advances in Operator Theory* is 2025. Entry lists journal name but uses preprint year. |
| `lagarias2005` | Year 2005 is the preprint date; journal publication in *J. London Math. Soc.* is 2006. Missing `journal` field. |
| `applegate2001` | Year 2001 is the preprint date; journal publication in *Math. Comp.* is 2003. Entry lists journal but uses preprint year. |

#### Critical Errors (3/16)

| Key | Issue | Severity |
|---|---|---|
| `polli2024` | **Wrong author initials.** Lists "M. D. da Luz" but the actual author is "M. G. E. da Luz" (Marcos Gomes Eleuterio da Luz). | **HIGH** |
| `lagarias2011` | **Wrong DOI.** DOI 10.5860/choice.48-6964 points to a *Choice Reviews* book review, NOT the book itself. **Wrong entry type:** should be `@book`, not `@article`. **Wrong role:** Lagarias is the editor, not author. **Year:** copyright year is 2010, not 2011. | **HIGH** |
| `siegel2020` | Minor title difference ("and" vs. "&"). Acceptable. | LOW |

### Summary
- 3 citations have critical factual errors (wrong author name, wrong DOI, wrong metadata)
- 5 citations have inconsistent year/venue (preprint year listed alongside journal name)
- 4 citations are missing required fields (journal names)
- Only 4 of 16 citations are fully correct

**This is below the acceptable standard. The bibliography needs thorough correction.**

---

## 5. Compilation (Score: 5/5)

The LaTeX document compiles without errors via `pdflatex -> bibtex -> pdflatex -> pdflatex`. The compilation log shows zero errors and zero warnings about undefined citations or references. The PDF is 2.8 MB, 17 pages, well-formatted with proper figure placement, table formatting, and hyperlinks.

---

## 6. Writing Quality (Score: 4/5)

### Strengths
- Professional academic tone throughout
- Clear and well-structured argument flow
- Effective use of numbered contributions in the introduction
- Honest treatment of negative results (modular resonance debunking, TDA non-significance)
- The Limitations subsection (Section 7.5) is commendably honest
- Notation table (Table 1) is helpful

### Weaknesses
- The abstract and introduction use the phrase "2-adic Linear Variance Law" as if it were an established theorem, but it is an empirical observation with noted limitations. Consider more cautious language (e.g., "empirical relationship" or "observed linear trend").
- The claim that the slope "stabilizes" (Table 5 caption) when it is still decreasing is misleading.
- Some passages in the Discussion overinterpret: e.g., "computational evidence that the conjecture is fundamentally 'infinite-depth'" is a strong philosophical claim from finite data.

---

## 7. Figure Quality (Score: 3/5)

### Strengths
- Figures use non-default matplotlib styling with proper titles, axis labels, and legends
- The phase diagram (Figure 5a) is publication-quality with annotated cell values
- The mutual information decay plot (Figure 4) clearly shows the null model band
- Persistence diagrams (Figure 7) use a clean three-panel layout
- The scale invariance summary (Appendix Figure) effectively condenses three findings

### Weaknesses

**F1: Lyapunov distribution figure (Figure 3) is misleading.** The distribution is so concentrated near 0 (std = 3.7 x 10^-4) that all data appears as a single spike. The x-axis range extends to 0.2 to show the theoretical prediction, but this makes it impossible to see the claimed non-Gaussianity (skewness, kurtosis) from the figure. The normal fit curve completely overlaps the data at this scale. This figure should either (a) use a zoomed inset showing the distribution shape near the mean, or (b) show a QQ-plot or standardized residual plot that makes the non-Gaussianity visible.

**F2: R^2 figure shows wrong fit.** As noted in I2, deep_dive_r2.png shows the k=1..17 fit (alpha = 0.0147) while the paper text describes the k=1..12 fit (alpha = 0.0119). The figure should show the k=1..12 fit that the paper actually discusses, ideally with the k > 12 data shown as open circles or a different color to indicate they are outside the linear regime.

**F3: Spectral spacing histogram (Figure 6a) has low sample size.** Only ~15 bars are visible, making the comparison to Poisson/GOE unconvincing visually. More eigenvalues or a CDF comparison would strengthen this.

---

## Detailed Findings Summary

### What Works Well
1. **Modular resonance debunking (Section 6.4)** -- This is the strongest contribution. The null-model correction is methodologically rigorous and provides a valuable cautionary lesson for computational number theory. This result alone merits publication in an appropriate venue.
2. **Seven-direction survey architecture** -- The systematic exploration across TDA, spectral theory, information theory, etc., with proper significance testing, is a model for computational exploration papers.
3. **Phase diagram (Section 6.3)** -- The first systematic (a,b) phase diagram is genuinely useful and the results are clean and reproducible.
4. **Honest negative results** -- The paper responsibly reports that TDA features don't survive correction, that forbidden patterns are all trivially explained, and that mutual information confirms (rather than challenges) existing models.

### What Needs Revision
1. **Central claim robustness** -- The slope alpha has not converged; the linearity breaks down for k > 12; the relationship may be a finite-size effect. The paper must either (a) demonstrate convergence at larger scales, (b) provide a theoretical argument for why alpha should converge to a positive constant, or (c) soften the claim to "empirical observation at moderate scales."
2. **Data consistency** -- The Lyapunov mean discrepancy (10^-4 vs. -0.12) and R^2 slope discrepancy between data files must be explained.
3. **Figure/text alignment** -- The R^2 fit line in the figure must match what the paper describes.
4. **Bibliography** -- All critical citation errors must be fixed.

---

## Specific Actionable Revisions Required

### Critical (must fix)

1. **Fix `polli2024` author:** Change "M. D. da Luz" to "M. G. E. da Luz" in sources.bib.
2. **Fix `lagarias2011`:** Change entry type to `@book`, change `author` to `editor`, fix DOI (current DOI 10.5860/choice.48-6964 points to a Choice Reviews review, not the book; use ISBN 978-0-8218-4940-8 or AMS publisher URL instead), and change year to 2010.
3. **Fix `wirsching1998`:** Change entry type from `@article` to `@book`.
4. **Fix `kontorovich2009`:** Change entry type from `@article` to `@incollection` and add booktitle.
5. **Add missing `journal` fields** to `lagarias1985` (The American Mathematical Monthly), `terras1976` (Acta Arithmetica), and `lagarias2005` (Journal of the London Mathematical Society).
6. **Resolve Lyapunov mean discrepancy.** Explain why `lyapunov_results.json` reports mean = 1.23 x 10^-4 while `scale_invariance.json` reports mean = -0.126 at the same n_max = 10^5. If different Lyapunov definitions were used, state this clearly.
7. **Fix R^2 figure.** Either regenerate `deep_dive_r2.png` to show the k=1..12 fit (alpha = 0.0119, R^2 = 0.994) that the paper describes, or update the paper text to reference the k=1..17 fit shown in the figure. Visually distinguish the k > 12 data points that deviate from linearity.

### Major (should fix)

8. **Address slope convergence.** Add a paragraph in the Discussion explicitly addressing whether alpha converges to a positive constant or could converge to 0. Acknowledge that at n=10^6, the slope is still declining. Consider extending computation to n=10^7 or providing a theoretical argument.
9. **Acknowledge super-linear growth for k > 12.** The marginal R^2 more than quintuples from k=12 (0.013) to k=17 (0.061). This is not linear. Discuss possible causes (e.g., finite-sample ANOVA artifact when group sizes approach observations per group, or genuine non-linearity).
10. **Improve Lyapunov figure.** Add a zoomed inset or QQ-plot that actually shows the non-Gaussianity. The current figure looks like a spike at 0.
11. **Soften the "law" language.** Replace "2-adic Linear Variance Law" with "2-adic Linear Variance Relationship" or "Empirical 2-adic Variance Trend" throughout, unless theoretical justification for asymptotic linearity is provided.

### Minor (nice to fix)

12. Resolve year inconsistencies in citations where journal name is listed alongside preprint year (tao2019, mori2024, applegate2001).
13. The spectral analysis (Section 6.6) cites a KS p-value of 0.46 against Poisson but does not note the KS statistic against Poisson shown in the figure legend (KS=0.101). Include both KS statistics (GOE and Poisson) in the text for completeness.
14. Table 5 caption claims "The slope stabilizes near 0.012 for n_max >= 5x10^5" -- change to "The slope decreases toward 0.012 as n_max increases" for accuracy.
15. The paper notes n=27 has stopping time 111 (rubric item_006), but this is the TOTAL stopping time. Clarify this definition consistently.

---

## Verdict: **REVISE**

The paper presents a well-structured computational investigation with several genuinely interesting findings. The modular resonance debunking, phase diagram, and negative results are valuable contributions. However, the central claim -- the "2-adic Linear Variance Law" -- is overstated relative to the evidence: the slope has not converged, linearity breaks down for k > 12, and the relationship may be a finite-size artifact. Combined with internal data inconsistencies (Lyapunov mean, R^2 figure/text mismatch) and critical bibliography errors (wrong author name, wrong DOI, wrong entry types in 3 citations), the paper does not yet meet the standard for publication.

A revised version that (1) honestly characterizes the limitations of the linear fit, (2) resolves the data inconsistencies, (3) corrects the bibliography, and (4) improves the Lyapunov figure would be a strong candidate for acceptance. The methodological contribution (null-model construction for modular arithmetic tests) and the systematic seven-direction survey are genuine strengths that should be highlighted more prominently in a revision.
