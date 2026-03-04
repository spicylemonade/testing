# Peer Review: A Computational Study of Bounds on the Chvátal–Sankoff Constant for the Binary Alphabet

**Reviewer:** Automated Peer Review Agent (Round 1)  
**Date:** March 4, 2026  
**Paper:** "A Computational Study of Bounds on the Chvátal–Sankoff Constant for the Binary Alphabet: Six Approaches and Their Limitations"

---

## Scores

| Criterion | Score (1–5) | Comments |
|---|---|---|
| **1. Completeness** | 4 | All required sections present: Abstract, Introduction, Related Work, Background, Method, Experimental Setup, Results, Discussion, Conclusion, References. No supplementary materials section despite reference to "supplementary materials" in §7.3. |
| **2. Technical Rigor** | 4 | Methods are well-described with equations (certificate condition, LCS recurrence, KPZ scaling forms). Experiments are reproducible (seed=42, wall-clock times reported). The DFA lower bound implementation is acknowledged as simplified (online matching, not full Lueker LP). The entropy bound derivation is sound. One concern: the strip transfer matrix result (trivial γ_s=1.0 for all s) is correctly diagnosed but indicates a fundamental implementation gap rather than a meaningful experimental result. |
| **3. Results Integrity** | 4 | Results in the paper match actual data in `results/`. MC estimates in Table 2 match `results/baselines/mc_estimates.json`. Frog dynamics results in Table 1 match `results/novel/frog_results.json`. Scaling fits match `results/experiments/scaling_fit.json`. The KPZ 3-parameter fit gives γ₂≈0.8132±0.0002, consistent across data files and paper text. No fabricated results detected. Minor discrepancy: paper claims γ(W=100110)=0.800±0.001 but the refined n=5000 result is 0.7994, so the "0.800" is from n=2000 only. |
| **4. Citation Accuracy** | 3 | See detailed Citation Verification Report below. All 21 entries are real, verifiable papers. However, there are several metadata errors: (a) HoudreIslak2014 has wrong year (2022 instead of 2023), wrong volume (27 instead of 28), wrong pages (1-33 instead of 1-24); (b) KiwiLobelMatousek2005 uses wrong entry type (@inproceedings instead of @article), wrong DOI (Springer LNCS doi instead of Elsevier doi); (c) KiwiSoto2009 has wrong page numbers (571-591 instead of 517-532); (d) BaezaYates1999 title/venue mismatch (the title given is for a different paper by these authors). No fabricated citations. Five bib entries are unused in the text. |
| **5. Compilation** | 5 | PDF compiles cleanly. Only 4 minor hyperref warnings about Unicode tokens in PDF strings. No errors. Well-formatted 12-page document. |
| **6. Writing Quality** | 5 | Excellent academic writing. Clear, precise, and well-organized. The paper's structure is logical: it honestly acknowledges that no rigorous bound improvement was achieved, then systematically diagnoses why each approach failed. The bottleneck analysis table (Table 3) is particularly valuable. The discussion of the absorbing-state barrier and entropy vs. eigenvalue structure is insightful. |
| **7. Figure Quality** | 3 | Mixed quality. The two multi-panel figures (convergence_analysis.png, particle_convergence.png) are professional with proper labels, legends, shaded bands for rigorous bounds, and KPZ fit overlays. The bar charts (lower_bound_comparison.png, upper_bound_comparison.png) are adequate but have issues: x-axes start at 0 for values clustered near 0.8, compressing meaningful variation; zero-value bars for failed methods look like rendering bugs. frog_gamma_by_period.png is sparse (6 points, no error bars, no word annotations). scaled_upper_bound.png shows a flat line at γ_s=1.0 for all strip widths, which is scientifically uninformative and should either be removed or heavily annotated. |
| **8. Novelty & Creative Contribution** | 2 | See detailed Novelty Assessment below. The paper presents no new rigorous bounds and no genuinely novel algorithmic contributions. The six approaches are either standard implementations of known methods (MC simulation, DFA online matching), simplified versions that are acknowledged to be weaker (neural certificate with count-based states), or known methods that fail for known reasons (strip eigenvalue absorbing state). The KPZ scaling estimate of γ₂≈0.813 is consistent with Bundschuh (2001) and adds marginal precision. The frog dynamics lower bound of 0.800 from period-6 words is valid but weaker than the 2024 SOTA. |

---

## Citation Verification Report

Each entry in `sources.bib` was verified via web search:

| Key | Title | Authors | Year | Venue | Verified? | Notes |
|---|---|---|---|---|---|---|
| CS1975 | Longest common subsequences of two random sequences | Chvátal, Sankoff | 1975 | J. Appl. Probab. 12(2):306-315 | **VERIFIED** | DOI 10.2307/3212444 correct |
| D1994 | Expected length of longest common subsequences | Dančík | 1994 | PhD thesis, U. Warwick | **VERIFIED** | URL to WRAP repository correct |
| DP1995 | Upper bounds for the expected length... | Dančík, Paterson | 1995 | Random Struct. Alg. 6(4):449-458 | **VERIFIED** | DOI 10.1002/rsa.3240060408 correct |
| L2009 | Improved bounds on the average length... | Lueker | 2009 | JACM 56(3):1-38 | **VERIFIED** | DOI 10.1145/1516512.1516519 correct |
| H2024 | Improved Lower Bounds on the Expected Length... | Heineman et al. | 2024 | arXiv:2407.10925 | **VERIFIED** | Authors match. DOI 10.1109/ISIT63088.2025.11195592 is for the conference version (ISIT 2025) |
| Tiskin2022 | The Chvátal–Sankoff problem... | Tiskin | 2022 | arXiv:2212.01582 | **VERIFIED** | Note: paper had errata; revised v2 appeared 2024 |
| BukhCox2022 | Periodic words, common subsequences and frogs | Bukh, Cox | 2022 | Ann. Appl. Probab. 32(2):1295-1332 | **VERIFIED** | DOI 10.1214/21-AAP1709 correct |
| LiRenWen2025 | Expected Length of the LCS of Multiple Strings | Li, Ren, Wen | 2025 | arXiv:2504.10425 | **VERIFIED** | Authors at Santa Clara University |
| Bundschuh2001 | High precision simulations of the LCS problem | Bundschuh | 2001 | Eur. Phys. J. B 22:533-541 | **VERIFIED** | DOI 10.1007/s100510170102 correct |
| BaezaYates1999 | Analysis of the expected number of symbol comparisons... | Baeza-Yates, Gavaldà, Navarro, Scheihing | 1999 | Pattern Matching | **VERIFIED with ISSUES** | Not cited in paper. The title in bib ("Analysis of the expected number of symbol comparisons in string searching algorithms") and venue ("Pattern Matching") are vague. The actual publication is in "Bounding the Expected Length of Longest Common Subsequences and Forests" in Theory of Computing Systems 32:435-452 (1999). The bib title may refer to a different paper by these authors. |
| HoudreIslak2014 | A central limit theorem for the length of the LCS... | Houdré, Işlak | 2022 (bib) | Electron. J. Probab. | **VERIFIED with ERRORS** | (1) Year in bib is 2022, but paper was published 2023 (EJP Vol 28, 2023). (2) Volume listed as 27, should be 28. (3) Pages listed as 1-33, should be 1-24. Cite key "2014" reflects arXiv date (1408.1559). |
| HauserMartinezMatzinger2006 | Large deviations-based upper bounds... | Hauser, Martínez, Matzinger | 2006 | Adv. Appl. Probab. 38(3):827-852 | **VERIFIED** | DOI 10.1239/aap/1158685004 correct |
| KiwiSoto2009 | On a Speculated Relation Between Chvátal–Sankoff Constants... | Kiwi, Soto | 2009 | Comb. Probab. Comput. 18(4) | **VERIFIED with ERROR** | Pages listed as 571-591 in bib, but actual paper is pages 517-532 (per arXiv journal reference). DOI 10.1017/S0963548309009900 is correct. |
| KiwiLobelMatousek2005 | Expected Length of the LCS for Large Alphabets | Kiwi, Loebl, Matoušek | 2005 | Advances in Mathematics | **VERIFIED with ERRORS** | (1) Entry type should be @article, not @inproceedings. (2) DOI 10.1007/978-3-540-24698-5_34 is for a Springer LNCS conference version, not the journal article (correct journal DOI: 10.1016/j.aim.2005.01.005). |
| BriggsEtAl2024 | Frogs, hats and common subsequences | Briggs, Parker, Schwieder, Wells | 2024 | arXiv:2404.07285 | **VERIFIED** | Correct |
| Rosenfeld2024 | Upper bounds on the average edit distance... | Rosenfeld | 2024 | arXiv:2407.18113 | **VERIFIED** | Correct |
| Steele1997 | Probability Theory and Combinatorial Optimization | Steele | 1997 | SIAM CBMS-NSF | **VERIFIED** | DOI 10.1137/1.9781611970029 correct |
| AggarwalNicolettiPetrov2023 | Colored interacting particle systems on the ring... | Aggarwal, Nicoletti, Petrov | 2023 | Compositio Math. | **VERIFIED** | arXiv:2309.11865 correct. DOI 10.1112/s0010437x25007195 correct (published in Compositio Math 161(8), 2025) |
| FertonaniDuman2010 | Novel Bounds on the Capacity of the Binary Deletion Channel | Fertonani, Duman | 2010 | IEEE Trans. Inform. Theory 56(6):2753-2765 | **VERIFIED** | DOI 10.1109/TIT.2010.2046210 correct |
| KashMitzenmacher2011 | On the zero-error capacity threshold for deletion channels | Kash, Mitzenmacher, Thaler, Ullman | 2011 | ITA Workshop | **VERIFIED** | arXiv:1102.0040 correct. DOI 10.1109/ITA.2011.5743594 correct |
| LiuHoudre2017 | Simulations, Computations, and Statistics for LCS | Liu, Houdré | 2017 | arXiv:1705.06826 | **VERIFIED** | Not cited in paper |
| BoothMacNamara2004 | An Iterative Approach to Determining the Length of the LCS... | Booth, MacNamara, Nielsen, Wilson | 2004 | Meth. Comp. Appl. Probab. 6:401-421 | **VERIFIED** | DOI 10.1023/B:MCAP.0000045088.88240.3A correct. Not cited in paper |

**Summary:** All 21 citations are real papers. No fabricated references. However, there are metadata errors in 4 entries (HoudreIslak2014, KiwiSoto2009, KiwiLobelMatousek2005, BaezaYates1999), and 5 entries are unused in the text.

---

## Novelty Assessment

This paper presents a "negative results" study: six approaches to tightening bounds on the binary Chvátal–Sankoff constant γ₂, none of which improve upon the state of the art. The paper is transparent about this outcome and provides systematic diagnoses of why each approach fails.

**What is genuinely novel:**
- Very little. The Monte Carlo estimation with KPZ scaling gives γ₂ ≈ 0.813 ± 0.001, refining Bundschuh's 2001 estimate of 0.8119 by at most 0.001. This is incremental.
- The frog dynamics lower bound from the word W=100110 (γ(W)≈0.800) provides independent confirmation of the known lower bound region, but is weaker than the SOTA of 0.792666 (note: 0.800 > 0.7927, so it's a valid but non-tightest lower bound).
- The identification that the strip transfer matrix fails due to the absorbing all-ones state is a correct observation, but this is well-known in the literature — Lueker (2009) specifically uses a dual formulation to avoid this exact problem.

**What is NOT novel:**
- The online matching DFA is a simplified, weaker version of the established Lueker framework. It achieves only 0.693, far below SOTA.
- The neural certificate optimization fails completely (best_r=0). The count-based state simplification is acknowledged to lose subsequence ordering, which is the essential structure. No valid bound produced.
- The strip transfer matrix produces only the trivial bound γ₂ ≤ 1.0 for all tested strip widths.
- The entropy bounds reproduce the known Dančík-Paterson analytic bound (0.854) and fail to improve on Lueker's 0.826.
- The KPZ scaling estimation is a straightforward application of finite-size scaling with standard fitting models.

**Concept Evolve engagement:**
The concept tree (`results/concept_evolve/tree/`) contains 12 concepts across 24 folders (hyphen and underscore variants). **Not a single concept.json file contains an `experimental_result` field.** All `implementation_hypothesis` fields remain completely untested. The concept_delta.md claims partial implementation of concepts #008 (LP relaxation) and #009 (finite-size scaling), but the concept.json files themselves show no enrichment. The semantic_bridge.json describes five bridge chains connecting domains, but none were turned into genuinely novel experiments — the actual experiments are standard implementations of known techniques. The CE system was used for framing and organizing, not for generating genuinely cross-domain experimental insights.

**Bottom line:** The paper is an honest computational survey with useful negative results and bottleneck analyses, but it contributes no new bounds, no new algorithms, and no surprises. The variance scaling exponent measurement (2χ ≈ 0.75 vs KPZ prediction 0.667) is potentially interesting but insufficiently analyzed to constitute a contribution. A domain expert would learn what doesn't work from this paper, but not gain any new tool or insight for making progress.

---

## Detailed Feedback

### Strengths
1. **Intellectual honesty:** The paper clearly states that no rigorous bound improvement was achieved and systematically explains why. This is valuable.
2. **Comprehensive bottleneck analysis:** Table 3 and the discussion in §7 provide quantitative diagnoses of each approach's failure mode.
3. **Writing quality:** The paper is exceptionally well-written with clear mathematical exposition and logical flow.
4. **Reproducibility:** Seed=42, wall-clock times, and all code/data provided.
5. **Accurate literature survey:** The related work section correctly summarizes the field.

### Weaknesses
1. **No new rigorous bounds:** The gap [0.7927, 0.8263] remains unchanged.
2. **Simplified implementations:** The DFA lower bound uses online matching (O(h) states) instead of the full Lueker framework (4^h states). The strip transfer matrix uses the primal formulation known to fail. These are not genuine attempts to extend SOTA — they are pedagogical reimplementations that reproduce known limitations.
3. **The neural certificate approach is fundamentally flawed:** Using count-based states that lose ordering information guarantees failure. This could have been predicted a priori.
4. **The claim "γ₂ ≥ 0.800 from frog dynamics" is misleading in context:** While technically valid, 0.800 > 0.7927 means this is actually a *weaker* lower bound than the SOTA. The paper could more clearly frame this as "independent confirmation" rather than implying it's a contribution.
5. **The CE concept tree was not genuinely used for research:** All 24 concept.json files lack experimental_result fields. The implementation_hypotheses were not followed.

### Citation Issues to Fix
1. **HoudreIslak2014:** Change year from 2022 to 2023, volume from 27 to 28, pages from 1-33 to 1-24.
2. **KiwiSoto2009:** Change pages from 571-591 to 517-532.
3. **KiwiLobelMatousek2005:** Change entry type from @inproceedings to @article; change `booktitle` to `journal`; update DOI to 10.1016/j.aim.2005.01.005.
4. **BaezaYates1999:** Verify/correct the title and venue to match the actual paper intended to be cited.
5. Remove or cite the 5 unused bibliography entries.

### Figure Issues to Fix
1. **scaled_upper_bound.png:** The flat line at γ_s=1.0 is uninformative. Either remove this figure or add heavy annotation explaining the absorbing state.
2. **Bar charts:** Use a broken x-axis or start near 0.65 to show meaningful variation among approaches clustered near 0.8.
3. **frog_gamma_by_period.png:** Add error bars and annotate the specific periodic words.

---

## Overall Verdict: **DEEPEN**

### Rationale

The paper is technically competent and well-written (scores of 4-5 on completeness, rigor, integrity, compilation, and writing). There are some fixable citation metadata errors (score 3) and figure quality issues (score 3), but the fundamental problem is **lack of novelty** (score 2).

The Novelty score of 2 triggers the DEEPEN verdict. The research contributes no new bounds, no new algorithms, and no genuinely surprising findings. The six approaches are either known methods faithfully replicated, simplified versions that are acknowledged to be weaker, or methods that fail for well-understood reasons. The KPZ scaling estimate adds marginal precision to Bundschuh (2001). The concept evolve system was not genuinely leveraged for cross-domain experimental insights.

### What would constitute genuine novelty for this domain:

1. **A new rigorous lower bound > 0.792666:** Even a marginal improvement (e.g., 0.7927) would be significant. This could come from:
   - Actually implementing the full Lueker DFA framework at h=15 or h=16 (acknowledged in the paper as requiring ~100GB RAM)
   - A genuinely new certificate structure that achieves competitive bounds with fewer states
   - A hybrid periodic-word/DFA approach that exploits frog dynamics insights

2. **A new rigorous upper bound < 0.82628:** This would require:
   - Correctly implementing Lueker's dual potential-function formulation (not the naive primal that has the absorbing state)
   - A genuinely new proof technique, perhaps leveraging optimal transport or information-theoretic structure

3. **A rigorous proof that γ₂ lies in a narrower interval:** Even a non-constructive proof that γ₂ ∈ [0.80, 0.82] would be major progress.

4. **A surprising structural finding:** For example, proving or disproving KPZ universality for binary LCS, or finding an unexpected connection between the DFA certificate structure and particle systems that enables a fundamentally new approach.

5. **A computational breakthrough in the DFA framework:** Engineering optimizations (e.g., GPU-accelerated certificate search, novel state-space compression) that enable reaching h=15-16 within feasible compute budgets.

The paper itself correctly identifies avenues (1), (2), and (5) as the most promising. A deepening cycle should pursue at least one of these directions with genuine implementation effort, rather than surveying simplified versions of known methods.

### Quality issues to fix during deepening:
- Correct the 4 citation metadata errors listed above
- Improve figure quality (remove or annotate the trivial strip eigenvalue figure; add error bars to frog dynamics figure; fix bar chart axes)
- Remove the reference to "supplementary materials" in §7.3 or provide them
- Remove unused bib entries or cite them
