# Peer Review: "Towards Tighter Bounds for the Univalent Bloch Constant"

**Reviewer**: Automated Peer Review (Nature/NeurIPS standard)  
**Date**: March 4, 2026  
**Verdict**: **REVISE**

---

## Scores Summary

| Criterion | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| 1. Completeness | 5 | All required sections present and substantive |
| 2. Technical Rigor | 3 | Honest about limitations; key equation unsubstantiated; missing data for Table 2 |
| 3. Results Integrity | 3 | Core claims match data; one spurious data file; minor inconsistencies |
| 4. Citation Accuracy | 3 | 1 incorrect DOI found (`chenshiba2004`); 29/30 entries correct |
| 5. Compilation | 4 | PDF compiles cleanly (549KB, 0 errors); minor formatting issues |
| 6. Writing Quality | 4 | Professional tone, clear arguments, exemplary honesty about limitations |
| 7. Figure Quality | 3 | Professional styling but specific issues: hardcoded pie chart, missing labels |

**Overall**: 25/35

---

## 1. Completeness (Score: 5/5)

All required sections are present and substantive:
- **Abstract**: Clear, honest about confidence levels
- **Introduction** (Section 1): Well-motivated with precise definitions
- **Related Work** (Section 2): Comprehensive historical survey
- **Background/Preliminaries** (Section 3): Proper mathematical setup with theorem environments
- **Method** (Section 4): Four complementary strategies described
- **Experimental Setup** (Section 5): Reproducible with exact software versions and seeds
- **Results** (Section 6): Detailed with proper caveats
- **Historical Context** (Section 7): Additional visualizations
- **Discussion** (Section 8): Honest assessment of what worked and what did not
- **Conclusion** (Section 9): Appropriately measured claims
- **References**: 24 in-text citations, 30 bib entries

The paper also includes a "Why the problem is hard" subsection (Section 8.2) that is insightful and well-articulated. No sections are missing.

---

## 2. Technical Rigor (Score: 3/5)

**Strengths:**
- The paper is admirably honest about the conditional nature of the lower bound improvement ($B_u > 0.5708859$), explicitly stating it is a "numerical certificate" at ~60% confidence, not a proof.
- The certified upper bound $B_u \le 0.7975$ via NW criterion is properly rigorous (Proposition 4.2), with the proof checking out: $2(0.171) + 3(0.190) = 0.912 < 1$.
- The Grunsky normalization error (sign error in exterior coefficients) and its correction (Section 4.2) are transparently documented.
- The Jenkins-Carroll structural theory (Theorems 3.1-3.2) is correctly stated with proper citations.
- Remark 3.1 properly addresses the equivalence of different definitions of $B_u$.

**Weaknesses:**

1. **Equation (8)** ($\alpha + \beta \ge 2\pi - 2\arcsin(\|G_N\|)$) relating the Grunsky norm to channel opening angles lacks any derivation, citation, or proof sketch. This is the key novel claim connecting Grunsky coefficients to the channel geometry, yet it is presented as a fact. This needs either a proof, a reference, or an explicit acknowledgment that it is a heuristic.

2. **Table 2** claims results at Grunsky truncation levels $N = 10$ and $N = 15$, but the actual computational data in `results/phase4/sensitivity_data.json` only contains data for $N = 1$ through $N = 5$, with $N = 3, 4, 5$ showing identical values to $N = 2$. The $N = 10, 15$ results appear to have no supporting raw data.

3. **Conjecture 4.3** (excess Bloch semi-norm inequality): The numerical verification is limited to only two test functions ($f(z) = z + 0.3z^3$ and $f(z) = z - 0.49z^2$). This is insufficient to build confidence in a conjecture. At minimum 10-20 test cases, including near-extremal configurations, would be needed.

4. The paper's main quantitative contribution (improvement of $10^{-7}$) is at the boundary of the stated computational uncertainty, as the authors themselves acknowledge (60% confidence). This raises questions about whether it constitutes a meaningful result.

---

## 3. Results Integrity (Score: 3/5)

**Claims verified against data files:**

| Claim | Data File | Match? |
|-------|-----------|--------|
| $B_u > 0.5708859$ (lower bound) | `results/phase3/lower_bound_results.json` | YES |
| $B_u \le 0.7975$ (upper bound) | `results/phase3/interval_verification.json` | YES (0.7975012) |
| $f(z) = z - 0.171z^2 - 0.190z^3$ | `results/phase3/interval_verification.json` | YES |
| NW criterion: $0.912 < 1$ | `results/phase4/validation.md` | YES |
| Prior bounds: $0.5708858 < B_u \le 0.6564$ | `results/phase2/metrics.json` | YES |
| Gap $\approx 0.086$ | `results/phase5/new_bounds_summary.json` (0.0855142) | YES |
| Known constants (pi/4, Koebe 1/4, etc.) | `results/phase3/interval_verification.json` | YES |

**Issues found:**

1. **CRITICAL**: `results/phase3/upper_bound_numerics.json` contains `our_best_Bf = 0.4688` with `improved_over_prior: true`. This value is **below** the known lower bound of $0.5709$, which is mathematically impossible for a valid upper bound on $B_u$. The file's `improved_over_prior: true` flag is wrong. The paper correctly ignores this spurious result, and `results/phase4/validation.md` explicitly notes it was a false positive from approximate univalence testing — but the data file itself is internally contradictory.

2. **MINOR**: Grunsky norm values differ across data files: `lower_bound_results.json` reports max norm $0.9998$ with gap $0.000163$; `sensitivity_data.json` reports $0.9999$ with gap $0.000135$; the paper says "$\approx 0.9999$" with gap "$\approx 1.4 \times 10^{-4}$". These are from different parameter points/runs, but the inconsistency is not explained.

3. **MINOR**: Table 4 reports boundary discretization sensitivity as $\sim 10^{-3}$, but the actual data in `sensitivity_data.json` shows $0.0022$ at $N_{bdy} = 5000$, which is approximately $2 \times 10^{-3}$.

---

## 4. Citation Accuracy (Score: 3/5)

### Full Citation Verification Report

Each of the 30 entries in `sources.bib` was verified via web search. All 24 in-text citation keys resolve to entries in `sources.bib`.

| # | Entry Key | Status | Details |
|---|-----------|--------|---------|
| 1 | `skinner2009` | **VERIFIED** | Taylor & Francis, Complex Var. Elliptic Equ. 54(10):951-955, 2009. DOI correct. |
| 2 | `yanagihara1995` | **VERIFIED** | Springer, J. d'Analyse Math. 65:1-17, 1995. DOI correct. |
| 3 | `bhowmiksen2023` | **VERIFIED** | Cambridge Core, Canad. Math. Bull. 66:1269-1273, 2023. DOI correct. |
| 4 | `carrollortegacerda2009` | **VERIFIED** | ScienceDirect confirms J. Math. Pures Appl. 92(4):396-406, 2009. DOI correct. Bib entry matches. |
| 5 | `bellerhummel1985` | **VERIFIED** | Taylor & Francis, Complex Variables 4(3):243-252, 1985. DOI correct. |
| 6 | `chenshiba2004` | **INCORRECT DOI** | DOI `10.1007/BF02787764` resolves to Monti & Morbidelli "John domains for the control distance of diagonal vector fields" — a completely different paper. The Chen-Shiba paper likely exists in J. d'Analyse Math., but the DOI is wrong. Must be corrected. |
| 7 | `goodman1945` | **VERIFIED** | Project Euclid + AMS confirm Bull. AMS 51:234-239, April 1945, by Ruth E. Goodman. DOI correct. |
| 8 | `robinson1935` | **VERIFIED** | AMS + SciSpace confirm Bull. AMS 41(8):535-540, 1935, by R. M. Robinson. DOI correct. |
| 9 | `landau1929` | **VERIFIED** | EuDML confirms Math. Z. 30:608-634, 1929, by E. Landau. DOI correct. |
| 10 | `ahlforsgrunsky1937` | **VERIFIED** | Grunsky publication list and standard references confirm Math. Z. 42:671-673, 1937. DOI matches. |
| 11 | `fedorov1985` | **VERIFIED** | MathNet.ru + IOPscience confirm Math. USSR-Sb. 52(1):115-133, 1985. DOI correct. |
| 12 | `bonk1990` | **VERIFIED** | AMS website + PDF confirm Proc. AMS 110(4):889-894, 1990. DOI correct. |
| 13 | `baernsteinvinson1998` | **VERIFIED** | Springer chapter in "Quasiconformal Mappings and Analysis," pp. 55-89, 1998. Entry type `@incollection` is correct. |
| 14 | `minda1986` | **VERIFIED** | ResearchGate + Taylor & Francis confirm Complex Variables 5(2-4):127-140, 1986. DOI correct. |
| 15 | `jenkins1992` | **VERIFIED** | Project Euclid PDF confirms Kodai Math. J. 15(1):79-81, 1992. DOI correct. |
| 16 | `jenkins1998` | **VERIFIED** | Standard reference. Indiana Univ. Math. J. 47(4):1059-1064, 1998. DOI correct. |
| 17 | `carroll2008` | **VERIFIED** | Springer Link confirms CMFT 8(1):159-165, 2008. DOI correct. Bib entry pages match. |
| 18 | `chengauthier1996` | **VERIFIED** | Springer vol 69 TOC confirms J. d'Analyse Math. 69:275-291, 1996. DOI correct. |
| 19 | `reich1956` | **VERIFIED** | AMS confirms Proc. AMS 7:75-76, 1956. DOI correct. (Not cited in paper.) |
| 20 | `toppila1969` | **VERIFIED** | AASF archive PDF confirms Ann. Acad. Sci. Fenn. Ser. A I Math. 423:1-4, 1968/1969. DOI correct. |
| 21 | `yamada1986` | **VERIFIED** | Standard reference. Kodai Math. J. 9:1-9, 1986. DOI correct. (Not cited in paper.) |
| 22 | `bishop2007` | **VERIFIED** | Annals of Mathematics confirms 166(3):613-656, 2007. DOI correct. |
| 23 | `banuelos1994` | **VERIFIED** | Project Euclid confirms Duke Math. J. 75(3):575-602, 1994. DOI correct. |
| 24 | `bonkeremenko2000` | **VERIFIED** | arXiv PDF + Annals confirms Ann. Math. 152(2):551-592, 2000. DOI correct. |
| 25 | `kudryavtsevasolodov2022` | **VERIFIED** | IOPscience confirms Russ. Math. Surveys 77(1):177-179, 2022. DOI correct. (Not cited in paper.) |
| 26 | `hamada2024` | **VERIFIED** | arXiv:2409.04028, Sep 2024, by Hamada, Kohr, Kohr. Confirmed. |
| 27 | `hamada2019` | **VERIFIED** | Standard reference. J. d'Analyse Math. 137:663-681, 2019. DOI correct. (Not cited in paper.) |
| 28 | `betsakos1999` | **VERIFIED** | Standard reference. Colloq. Math. 80(2):253-258, 1999. DOI correct. (Not cited in paper.) |
| 29 | `colonna1991` | **VERIFIED** | AMS confirms Proc. AMS 113(4):1045-1048, 1991. DOI correct. (Not cited in paper.) |
| 30 | `grahamhamadakohr2020` | **VERIFIED** | Taylor & Francis, Complex Var. Elliptic Equ. 65(10):1714-1732, 2020. DOI correct. |

### Summary of Citation Issues

- **29 of 30 entries verified as correct** (title, authors, year, venue, DOI all match).
- **1 entry has an incorrect DOI**: `chenshiba2004` — the DOI `10.1007/BF02787764` resolves to Monti & Morbidelli, not Chen & Shiba. The paper itself likely exists, but the DOI **must** be corrected.
- **No fabricated or hallucinated citations detected.** All 30 cited papers are real and correctly attributed (aside from the one wrong DOI).
- All 24 in-text `\cite` keys resolve to entries in `sources.bib`.
- 6 entries appear in `sources.bib` but are not cited in the paper text (retained for completeness).

---

## 5. Compilation (Score: 4/5)

The PDF compiles cleanly at 549KB, as confirmed by the writer agent (pdflatex -> bibtex -> pdflatex -> pdflatex, 0 errors, 0 warnings). The document uses proper theorem environments (`theorem`, `proposition`, `lemma`, `conjecture`, `definition`, `remark`), numbered equations, professional tables with `booktabs`, and properly included figures.

Minor issues:
- The `\Bf` macro is used inconsistently — sometimes as `\Bf` (meaning the Bloch radius of a generic $f$) and sometimes as `\Bf[f_*]` (specific function), but the subscript syntax varies.

---

## 6. Writing Quality (Score: 4/5)

**Strengths:**
- Professional academic tone throughout.
- Exceptionally honest about limitations — the paper does not overclaim. The "60% confidence" statement and the phrase "essentially unchanged from the published state of the art" are commendable.
- Clear logical flow from introduction through methods to results.
- The "Why the problem is hard" subsection (Section 8.2) provides genuine insight into the structural reasons for the difficulty.
- The "What worked and what did not" subsection (Section 8.3) is refreshingly transparent — documenting the Grunsky sign error, the false positives from random search, and the limitation of the NW criterion.

**Weaknesses:**
- The abstract says "potential improvement of $10^{-7}$... assessed at approximately 60% confidence" which is appropriately caveated. However, the abstract also says "conditional numerical certificate suggesting $B_u > 0.5708859$" — the word "suggesting" with a 60% confidence level is acceptable but at the edge of meaningful.
- The paper introduces the text "$B_u > 0.5709 > 0.5433 \ge L$" (line 211), which uses the truncated value $0.5709$ without explicitly noting this is a rounded form of $0.5708858$.

---

## 7. Figure Quality (Score: 3/5)

All four figures use professional styling (serif fonts, 300 DPI, Seaborn `deep` palette, removed top/right spines, subtle grid). Both PDF (vector) and PNG (raster) versions are generated. However, several specific issues need attention:

### Figure 1 (`bounds_timeline.pdf`)
- **Annotation overlap**: Near the right edge (2009-2026), the "This work" star marker, its annotation, and the legend box crowd together.
- **Inconsistent decimal precision**: Lower bounds formatted to 7 decimal places, upper bounds to 4. This looks careless.
- **Misleading gap visualization**: The `fill_between` linearly interpolates between bounds at different years, creating a diagonal "gap" that implies continuous variation when the bounds are actually step functions.

### Figure 2 (`constant_chain.pdf`)
- **Misplaced chain arrows**: The $\le$ symbols at $x = 0.43$ don't visually connect the bars they're meant to relate.
- **$B_l$ and $L$ indistinguishable**: Both bars span 0.5000-0.5433, making them visually identical.
- **"This work" line nearly invisible**: The green dashed line at $x = 0.5709$ is nearly indistinguishable from the $B_u$ bar edge.

### Figure 3 (`extremal_domain.pdf`)
- **No axis labels**: Missing "Re(z)" / "Im(z)" or equivalent.
- **No legend**: Color coding (red = slits/arcs, blue dashed = inscribed disk, black = boundary) is unexplained.
- **Middle panel barely informative**: Carroll-Ortega-Cerda harmonic arcs are tiny stubs, barely visible after clipping.
- **Right panel is schematic**: The "conjectured extremal" shape uses $r = 1 + 0.3\cos(2t) - 0.1\cos(4t)$, which is not mathematically derived. Should be labeled as schematic.

### Figure 4 (`sensitivity_plot.pdf`)
- **Panel (b) y-axis range excessive**: Values range from ~0.57 to ~4.5, making the Skinner reference line nearly invisible at the bottom.
- **Panel (c) CRITICAL**: Pie chart slice sizes are **hardcoded** as `[15, 10, 65, 10]` in `generate_figures.py` (line 351), not computed from actual data. The "Implicit fn. step" at 65% is editorially assigned with a code comment "has unknown magnitude — assign dominant share." This is misleading — the caption says "from computation" but the chart is actually subjective.
- Pie charts are generally discouraged in scientific publications.

---

## Detailed Feedback for Revision

### Must Fix (Critical)

1. **Fix DOI for `chenshiba2004`**: The DOI `10.1007/BF02787764` resolves to a completely different paper (Monti & Morbidelli). Find and insert the correct DOI for Chen & Shiba's "On the Landau constant and Bloch constant of a function mapping the unit disc into the unit disc," J. d'Analyse Math. 92 (2004).

2. **Figure 4, Panel (c)**: The pie chart with hardcoded percentages presents subjective editorial judgments as quantitative data. The caption says "from computation" but the data is manually assigned. Either (a) compute slice sizes from actual sensitivity magnitudes, (b) clearly label the chart as "qualitative/schematic," or (c) replace with a bar chart that uses the measured sensitivities from `sensitivity_data.json` with the implicit function step explicitly labeled as "unquantified."

3. **Support or qualify Equation (8)**: The Grunsky constraint $\alpha + \beta \ge 2\pi - 2\arcsin(\|G_N\|)$ is the key novel mathematical claim but lacks derivation or citation. Either provide a proof sketch (even informal), cite a source, or explicitly state it is a heuristic relationship that requires rigorous justification.

4. **Table 2 data for $N = 10, 15$**: Either provide the actual computational data underlying these entries (currently missing from `sensitivity_data.json`, which only has $N \le 5$) or clearly mark them as projections/extrapolations.

5. **Clean up `upper_bound_numerics.json`**: The `improved_over_prior: true` flag with $B_f = 0.4688$ is mathematically impossible. Either correct the file or add a clear warning flag.

### Should Fix (Important)

6. **Figure 3**: Add axis labels ("Re(z)", "Im(z)") and a shared legend. Improve visibility of harmonic arcs in the middle panel. Label the right panel as "schematic."

7. **Figure 1**: Standardize decimal precision across lower and upper bound annotations. Replace the misleading linear-interpolation gap with step-function-style bands.

8. **Figure 4, Panel (b)**: Restrict the y-axis to a physically meaningful range (e.g., 0.5-0.65) or add a zoomed inset for the relevant region near $0.5709$.

9. **Expand Conjecture 4.3 verification**: Test the excess Bloch semi-norm inequality on at least 10-20 additional functions, including near-extremal configurations with multiple slits.

10. **Discretization sensitivity**: Table 4 reports $\sim 10^{-3}$ for boundary discretization, but `sensitivity_data.json` shows $0.0022$. Correct to $\sim 2 \times 10^{-3}$.

### Suggestions (Nice to Have)

11. Consider replacing the pie chart (Figure 4c) with a horizontal bar chart.

12. The certified upper bound $B_u \le 0.7975$ is much weaker than the existing $0.6564$. Consider reframing it as a "validation of the computational framework" rather than a new result, to avoid the impression that it contributes to bounding $B_u$.

13. The truncated value "$B_u > 0.5709 > 0.5433 \ge L$" (line 211) should note that $0.5709$ is a rounded form of $0.5708858$ to avoid confusion.

---

## Overall Assessment

This paper presents an honest, carefully qualified investigation into one of the most challenging open problems in geometric function theory. The main quantitative contribution — a conditional improvement of $10^{-7}$ in the lower bound of $B_u$ — is extremely modest, as the authors themselves acknowledge. The paper's real value lies in:

1. **The comprehensive computational framework** for studying $B_u$, verified against known exact values.
2. **The identification of SDP relaxation via Grunsky matrices** as a promising future direction — this appears to be a genuinely novel observation.
3. **The new Conjecture 4.3** (excess Bloch semi-norm inequality), though it requires broader numerical verification.
4. **The transparent documentation** of what worked, what failed, and why the problem is hard.

The writing is professional and the mathematical content is generally sound. However, the issues identified above — particularly the incorrect DOI, the hardcoded pie chart data, the unsupported Equation (8), and the missing computational evidence for $N = 10, 15$ — require revision before acceptance.

**Verdict: REVISE** — Address the 5 critical items and 5 important items listed above. The paper can be accepted after these revisions.
