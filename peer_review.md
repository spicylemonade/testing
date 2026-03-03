# Peer Review: The Univalent Bloch Constant — A Multi-Method Investigation

**Reviewer:** Automated Peer Review System (Nature/NeurIPS standards)  
**Date:** March 3, 2026

---

## Criterion Scores (1–5)

| Criterion | Score | Comments |
|---|---|---|
| **1. Completeness** | 5 | All required sections present: Abstract, Introduction, Related Work, Background, Method, Experimental Setup, Results, Discussion, Conclusion, References. Well-structured with subsections. |
| **2. Technical Rigor** | 3 | Methods are described with equations and references. However, the "new" extremal length inequality (Prop. 3.1) is only a proof sketch, the bound it yields is no better than Koebe 1/4, and the upper bounds obtained do not improve the state of the art. See detailed comments. |
| **3. Results Integrity** | 3 | Claims match the data in `results/` files. The paper honestly reports failure to improve the lower bound. Upper bounds (0.6808, 0.6833) are verified against `verification_report.json`. However, there is one factual error in Table 1 (Ahlfors-Grunsky row). The optimization landscape figure has a significant discrepancy (see below). |
| **4. Citation Accuracy** | 4 | All 27 bibliography entries in the .bbl resolve to real, verified papers. No fabricated citations detected. Minor issues: (a) the `goodman1945` author is listed as "Ruth E. Goodman" — verified correct; (b) some DOIs verified correct. One content error: the Ahlfors-Grunsky bound in Table 1 is incorrectly attributed to $B_u$ when it pertains to $B$. See detailed citation report below. |
| **5. Compilation** | 4 | PDF compiles successfully. No LaTeX errors. Minor warnings only: 3 overfull hboxes and 5 underfull hboxes in the techniques table. Two hyperref warnings about tokens in PDF strings. |
| **6. Writing Quality** | 4 | Professional academic tone throughout. Clear logical flow from motivation through methods to results and discussion. Honest assessment of negative results. Minor issues: some redundancy between the Introduction "Our Contributions" list and the Conclusion. |
| **7. Figure Quality** | 4 | Figures use seaborn styling with proper labels, titles, legends, and color palettes. The bounds_timeline and method_comparison figures are publication-quality. The extremal_function figure effectively shows the image domain. The optimization_landscape heatmap is informative. One issue: the optimization landscape shows B_f values of order 0.0001–0.009, which appear to be the distance from 0 to the nearest boundary point on the *starlike-constrained* family, not the actual inradius — this needs clarification/correction. |

---

## Citation Verification Report

### Verified (all correct):

| # | BibTeX Key | Verification |
|---|---|---|
| 1 | `bloch1925` | **VERIFIED.** André Bloch, 1925, Annales Fac. Sci. Toulouse, vol. 17, pp. 1–22. Confirmed via Numdam. |
| 2 | `landau1929` | **VERIFIED.** Edmund Landau, 1929, Math. Z., vol. 30, pp. 608–634. DOI 10.1007/BF01187791 resolves correctly on EuDML. |
| 3 | `robinson1935` | **VERIFIED.** R. M. Robinson, 1935, Bull. AMS, vol. 41, pp. 535–540. DOI 10.1090/S0002-9904-1935-06138-5 confirmed via AMS. |
| 4 | `ahlfors1937` | **VERIFIED.** Ahlfors & Grunsky, 1937, Math. Z., vol. 42, pp. 671–673. DOI 10.1007/BF01160101 confirmed. |
| 5 | `ahlfors1938` | **VERIFIED.** Ahlfors, 1938, Trans. AMS, vol. 43, pp. 359–364. DOI 10.1090/S0002-9947-1938-1501949-6 confirmed. |
| 6 | `goodman1945` | **VERIFIED.** Ruth E. Goodman, 1945, Bull. AMS, vol. 51, pp. 234–239. Confirmed via Project Euclid. |
| 7 | `reich1956` | **VERIFIED** (unused in paper). Edgar Reich, 1956, Proc. AMS, vol. 7, pp. 75–76. DOI confirmed via AMS. |
| 8 | `jenkins1961` | **VERIFIED.** James A. Jenkins, 1961, J. Math. Mech., vol. 10, pp. 729–734. Confirmed via Google Scholar/zbMATH. |
| 9 | `toppila1969` | **VERIFIED** (unused in paper). Sakari Toppila, 1968/1969, Ann. Acad. Sci. Fenn. A I, no. 423. Confirmed via acadsci.fi. |
| 10 | `beller1985` | **VERIFIED.** E. Beller & J. A. Hummel, 1985, Complex Variables, vol. 4, pp. 243–252. DOI 10.1080/17476938508814109 confirmed via SciSpace/Taylor & Francis. |
| 11 | `fedorov1985` | **VERIFIED.** S. I. Fedorov, 1985, Math. USSR-Sb., vol. 52, pp. 115–133. DOI 10.1070/SM1985V052N01ABEH002880 confirmed via IOPscience and MathNet.ru. |
| 12 | `yamada1986` | **VERIFIED** (unused in paper). Akira Yamada, 1986, Kodai Math. J., vol. 9, pp. 145–153. DOI confirmed. |
| 13 | `bonk1990` | **VERIFIED.** Mario Bonk, 1990, Proc. AMS, vol. 110, pp. 889–894. DOI confirmed; full PDF accessible. |
| 14 | `jenkins1992` | **VERIFIED.** James A. Jenkins, 1992, Kodai Math. J., vol. 15, pp. 79–81. DOI 10.2996/kmj/1138039528 confirmed; full PDF accessible via Project Euclid. |
| 15 | `yanagihara1995` | **VERIFIED.** Hiroshi Yanagihara, 1995, J. Anal. Math., vol. 65, pp. 1–17. DOI 10.1007/BF02788763 confirmed via Springer. |
| 16 | `bonkmindayanagihara1996` | **VERIFIED.** Bonk, Minda & Yanagihara, 1996, J. Anal. Math., vol. 69, pp. 73–95. DOI 10.1007/BF02787103 confirmed via Springer/ResearchGate. |
| 17 | `chengauthier1996` | **VERIFIED.** Chen & Gauthier, 1996, J. Anal. Math., vol. 69, pp. 275–291. DOI 10.1007/BF02787110 confirmed via Springer. |
| 18 | `bonkmindayanagihara1997` | **VERIFIED.** Bonk, Minda & Yanagihara, 1997, Pacific J. Math., vol. 179, pp. 241–262. DOI 10.2140/pjm.1997.179.241 confirmed via MSP. |
| 19 | `baernsteinvinson1998` | **VERIFIED.** Baernstein & Vinson, 1998, in Quasiconformal Mappings and Analysis, Springer, pp. 55–89. Confirmed via Springer chapter DOI 10.1007/978-1-4612-0605-7_7. |
| 20 | `jenkins1998` | **VERIFIED.** Jenkins, 1998, Indiana Univ. Math. J., vol. 47, pp. 1059–1064. DOI 10.1512/iumj.1998.47.1519 confirmed. |
| 21 | `xiongchen2004` | **VERIFIED.** Xiong & Chen, 2004, Comput. Math. Appl., vol. 47, pp. 931–946. DOI 10.1016/S0898-1221(04)90077-6 confirmed via ScienceDirect. |
| 22 | `chenshiba2004` | **VERIFIED** (unused in paper). Chen & Shiba, 2004, J. Anal. Math., vol. 94, pp. 159–170. DOI 10.1007/BF02789045 confirmed via Springer. |
| 23 | `bishop2007` | **VERIFIED.** Christopher J. Bishop, 2007, Ann. of Math., vol. 166, pp. 613–656. DOI 10.4007/annals.2007.166.613 confirmed via Annals of Mathematics website. |
| 24 | `carroll2008extension` | **VERIFIED.** Tom Carroll, 2008, Comput. Methods Funct. Theory, vol. 8, pp. 159–165. DOI 10.1007/BF03321679 confirmed via Springer. |
| 25 | `carrollortegacerda2009` | **VERIFIED.** Carroll & Ortega-Cerdà, 2009, J. Math. Pures Appl., vol. 92, pp. 396–406. DOI 10.1016/j.matpur.2009.05.008 confirmed via ScienceDirect; arXiv:0806.2282 confirmed. |
| 26 | `skinner2009` | **VERIFIED.** Brian Skinner, 2009, Complex Var. Elliptic Equ., vol. 54, pp. 951–955. DOI 10.1080/17476930903197199 confirmed. |
| 27 | `chengauthierhengartner2000` | **VERIFIED** (unused in paper). Chen, Gauthier & Hengartner, 2000, Proc. AMS, vol. 128, pp. 3231–3240. DOI 10.1090/S0002-9939-00-05590-8 confirmed. |
| 28 | `chengauthier2000several` | **VERIFIED.** Chen & Gauthier, 2000, Trans. AMS, vol. 353, pp. 1371–1386. DOI 10.1090/S0002-9947-00-02734-3 confirmed. |
| 29 | `finch2003` | **VERIFIED** (unused in paper). Steven R. Finch, Mathematical Constants, Cambridge Univ. Press, 2003. DOI confirmed. |
| 30 | `kudryavtsevasolodov2022` | **VERIFIED** (unused in paper). Kudryavtseva & Solodov, 2022, Russ. Math. Surv., vol. 77, pp. 177–179. DOI 10.1070/RM10042 confirmed via IOPscience. |
| 31 | `bhowmiksen2023` | **VERIFIED.** Bhowmik & Sen, 2023, Canad. Math. Bull., vol. 66, pp. 1269–1273. DOI 10.4153/S0008439523000346 confirmed. |
| 32 | `bhowmiksen2024` | **VERIFIED.** Bhowmik & Sen, 2024, arXiv:2404.04596. URL confirmed. (Preprint, not peer-reviewed.) |
| 33 | `banuelos1994` | **VERIFIED.** Bañuelos & Carroll, 1994, Duke Math. J., vol. 75, pp. 575–602. DOI 10.1215/S0012-7094-94-07517-0 confirmed via Project Euclid. |
| 34 | `hamada2019` | **VERIFIED.** Hidetaka Hamada, 2019, J. Anal. Math., vol. 137, pp. 663–677. DOI 10.1007/s11854-019-0005-y confirmed via Springer/ResearchGate. |

**Summary:** All 34 entries in `sources.bib` are real, verified papers. 27 are cited in the paper and appear in the compiled bibliography. 7 are unused but not fabricated. No hallucinated references detected.

---

## Detailed Technical Issues

### Issue 1: Factual Error in Table 1 (Historical Bounds)

**Line 178:** The entry "1937 | Ahlfors-Grunsky | $B_u \le \sqrt{3}/4 + 2^{-7/3} \approx 0.657$ | Upper" is **incorrect**.

- The Ahlfors-Grunsky (1937) result establishes an upper bound on the **general Bloch constant** $B$, not on the **univalent Bloch constant** $B_u$.
- The conjectured value of $B$ from Ahlfors-Grunsky is $B \le \Gamma(1/3)\Gamma(11/12)/(\sqrt{1+\sqrt{3}}\Gamma(1/4)) \approx 0.4719$.
- The formula $\sqrt{3}/4 + 2^{-7/3}$ does not correspond to any known result. Computing it: $\sqrt{3}/4 \approx 0.4330$, $2^{-7/3} \approx 0.1984$, sum $\approx 0.6314$, which does not even match the stated $\approx 0.657$.
- **Action required:** Remove or correct this row. The first explicit upper bound on $B_u$ below 1 in the literature is Goodman (1945) with $B_u \le 0.6564$ (approximately). The Carroll-Ortega-Cerdà (2009) bound $B_u \le 0.6564$ is the state of the art.

### Issue 2: Extremal Length Inequality (Proposition 3.1) — Proof Incompleteness

The paper's "main theoretical contribution" (Prop. 3.1: $B_f \ge r \cdot e^{\pi M(r)}/4$) is presented only as a proof sketch. Key issues:

- The invocation of the "Grötzsch modulus theorem" with reference to "[Chapter 4] of [ahlfors1938]" is inaccurate — Ahlfors (1938) is a 6-page paper on Schwarz's lemma, not a textbook with chapters. The Grötzsch modulus theorem is found in textbooks (e.g., Ahlfors' *Conformal Invariants*, 1973), not in the 1938 paper.
- The claim about the "midline at modular distance $M(r)/2$" needs more rigorous justification. The argument as stated is plausible but incomplete.
- The inequality recovers only $B_u \ge 1/4$ (the Koebe bound), providing no numerical improvement. While the paper acknowledges this, the characterization as a "main theoretical contribution" is overstated for a result that produces no improvement over a century-old bound.

### Issue 3: Optimization Landscape Figure Discrepancy

The optimization landscape figure (Fig. 2b) shows $B_f$ values in the range 0.0001–0.009 for degree-3 polynomials $f(z) = z + az^2 + bz^3$. However:
- These extremely small values are inconsistent with the known bound $B_u > 0.57$.
- The paper's own text (line 675) refers to $B_f = 0.7877$ for degree-5 starlike subfamilies.
- This discrepancy suggests the plotted quantity may be the distance from the origin to the nearest boundary point (the Koebe radius), not the inradius of the image domain. The figure caption does not clarify this distinction.

### Issue 4: Upper Bound Claims Need Qualification

The paper claims "independent upper bounds $B_u \le 0.6808$ (coefficient optimization) and $B_u \le 0.6833$ (close-to-convex construction)." These are valid upper bounds since any explicit univalent function with $f'(0)=1$ gives $B_u \le B_f$. However:
- These do not improve the known best upper bound of $0.6564$ (Carroll-Ortega-Cerdà).
- The paper correctly states this in Table 2 and elsewhere, but the abstract's phrasing "independent upper bounds" might mislead casual readers into thinking these are improvements.

### Issue 5: The Extremal Function Figure Shows a Nearly-Circular Domain

Figure 2a shows the image of $f(z) = z - 0.21z^3$, which is nearly circular with $r_B \approx 0.0007$ (as labeled). This is clearly not a near-extremal function for $B_u$. The caption claims it's from "coefficient optimization (degree 7)" achieving $B_f = 0.6808$, but the plotted function is $z - 0.21z^3$ (degree 3) with a tiny inscribed disk. This appears to be a mismatch between the caption and the actual plotted function.

### Issue 6: Minor Technical Issues

- **Line 130:** The definition of $B_u$ uses $f \in \mathcal{S}$ (which includes $f(0) = 0$), but the task description says $f \in \mathcal{F}$ with $f'(0)=1$ and $f$ univalent. These are equivalent by translation, but the normalization should be stated more carefully.
- **Line 178:** The Landau row states "$B_u \ge 0.5$ (approx.)" for 1929. The standard reference is that Landau proved the existence of a universal covering disk, not specifically $B_u \ge 0.5$.

---

## Strengths

1. **Comprehensive and honest:** The paper candidly reports failure to improve the lower bound and provides a thoughtful analysis of why existing methods are limited.
2. **Strong literature coverage:** The related work section is thorough, covering the full historical development from Bloch (1925) through Bhowmik-Sen (2023/2024).
3. **All citations are genuine:** Every bibliography entry was verified to be a real, correctly attributed paper.
4. **Useful synthesis:** The 11-technique catalog (Table 4) and the identification of the binding constraint (conformal radius normalization) provide genuine value to researchers in the field.
5. **Reproducible computations:** Code, data, and verification scripts are provided.

---

## Weaknesses

1. **No new tighter bounds achieved:** The paper's stated goal was to improve bounds on $B_u$. Neither the lower bound nor the upper bound was improved beyond the 2009 state of the art. The paper is fundamentally a survey/computational study rather than a contribution of new bounds.
2. **Factual error in Table 1:** The Ahlfors-Grunsky entry is incorrectly stated as an upper bound on $B_u$.
3. **Incomplete proof:** Proposition 3.1 is only a sketch with an incorrect reference.
4. **Figure-text mismatch:** The extremal function figure appears to show a different function than described in the caption.
5. **Optimization landscape figure:** The $B_f$ values shown (order $10^{-4}$ to $10^{-2}$) are inconsistent with known bounds and likely represent a different quantity than the inradius.

---

## Overall Verdict: **REVISE**

### Required Changes for Acceptance:

1. **Fix the Ahlfors-Grunsky row in Table 1.** Either remove it (it pertains to $B$, not $B_u$) or clearly label it as a bound on the general Bloch constant $B$ rather than $B_u$. The formula $\sqrt{3}/4 + 2^{-7/3}$ does not correspond to any known result and must be corrected.

2. **Fix the Proposition 3.1 proof reference.** The citation "[Chapter 4] of [ahlfors1938]" is incorrect — Ahlfors (1938) is a 6-page paper, not a textbook. Reference the correct source (likely Ahlfors' *Conformal Invariants*, 1973, or another standard text on extremal length).

3. **Fix the extremal function figure (Fig. 2a).** The plotted function $f(z) = z - 0.21z^3$ with $r_B \approx 0.0007$ does not match the caption's claim of a degree-7 polynomial achieving $B_f = 0.6808$. Either plot the actual near-extremal degree-7 polynomial, or correct the caption.

4. **Clarify the optimization landscape figure (Fig. 2b).** Explain why $B_f$ values are orders of magnitude below $0.57$. If the plotted quantity is not the inradius but rather the minimum distance from 0 to the boundary, state this explicitly and relabel accordingly.

5. **Temper the "main theoretical contribution" claim.** Proposition 3.1 yields only $B_u \ge 1/4$, the same as the Koebe theorem. While the extremal length framework may be useful for future work, calling it a "main contribution" when it produces no numerical improvement is an overstatement. Reframe it as a "potential framework for future improvement."

6. **Minor fixes:**
   - Verify the Landau 1929 entry in Table 1 ("$B_u \ge 0.5$ (approx.)") — provide a specific reference or soften the attribution.
   - Remove or explain unused bib entries (7 entries in `sources.bib` not cited in text).

### Note on Figures:
The figures generally use professional styling (seaborn, proper colorbars, legends, LaTeX-rendered labels). The bounds_timeline and method_comparison figures are of good quality. The main concern is the content accuracy of Figures 2a and 2b, not their styling.
