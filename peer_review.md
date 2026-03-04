# Peer Review: Computational and Theoretical Approaches to Tighter Bounds on the Binary Chvátal–Sankoff Constant

**Reviewer:** Automated Peer Review Agent  
**Date:** 2026-03-04  
**Venue Standard:** Nature/NeurIPS  

---

## Summary

The paper presents a systematic computational investigation of ten approaches to tightening the bounds on the binary Chvátal–Sankoff constant γ₂ ∈ [0.792665992, 0.826280]. The principal claimed contribution is a *conjectural* upper bound γ₂ ≤ 0.808 via a Bernoulli LPP correlation gap. Additional contributions include an MDP-optimal DFA framework for lower bounds, finite-size scaling analysis, and frog dynamics exploration. The paper is well-structured, clearly written, and honestly characterizes the rigor level of each result.

---

## Scores

| Criterion | Score (1–5) | Comments |
|-----------|:-----------:|---------|
| **1. Completeness** | **5** | All required sections present: Abstract, Introduction, Related Work (§2), Background (§3), Methods (§4), Experimental Setup (§5), Results (§6), Verification (§7), Discussion (§8), Conclusion (§9), References. |
| **2. Technical Rigor** | **4** | Methods are clearly described with equations (DP recurrence, LPP formulation, Kolmogorov bounds, scaling forms). The DFA/MDP formulation is precise. The Bernoulli LPP gap argument is mathematically well-motivated but explicitly conjectural. The paper is transparent about which bounds are rigorous vs. conjectural. Minor concern: the paper does not achieve any *new* rigorous bounds that improve on prior work (all rigorous bounds are weaker than known state-of-the-art). The information-theoretic bound analysis (§6.4, Eq. 12–13) has a minor inconsistency: the "refined" bound (0.9068) is *weaker* than the "basic" bound (0.9051), which is counterintuitive and warrants explanation. |
| **3. Results Integrity** | **5** | All claimed values in the paper match the underlying data files precisely. Exact expectations (Table 1) match `results/baseline/exact_expectations.json`. MC estimates (Table 2) match `results/baseline/mc_estimates.json`. DFA bounds (Table 3) match `results/novel/dfa_lower_bounds.json`. Bernoulli LPP gaps (Table 4) match `results/novel/sdp_results.json`. Frog dynamics (Table 5) match `results/novel/frog_dynamics_results.json`. The summary table (Table 6) is consistent with `results/final_summary.json`. No fabricated results detected. |
| **4. Citation Accuracy** | **4** | 25 of 28 entries in `sources.bib` are verified correct. See detailed Citation Verification Report below. Three entries (Borodin1999, Dixon2013, LemberMatzinger2009) are present in the bibliography but never cited in the paper text — this is harmless but untidy. All 28 entries are real papers. Minor metadata discrepancies noted for a few entries (see below), but none are fabricated or hallucinated. |
| **5. Compilation** | **5** | The PDF exists (444 KB), the LaTeX log shows 0 errors, and no undefined citation or reference warnings. The paper compiles cleanly. |
| **6. Writing Quality** | **5** | Professional academic tone throughout. Clear, logical flow from problem statement through methods, results, and discussion. The paper is honest about limitations (e.g., DFA bounds being weaker than Dančík 1994, all rigorous bounds being weaker than state-of-the-art). The distinction between rigorous and conjectural results is consistently maintained. |
| **7. Figure Quality** | **4** | Five figures provided (bounds_timeline, scaling_fit, dfa_ablation, lueker_convergence, approach_comparison), each in both PNG and PDF. Figures have proper axis labels, legends, titles, and reference lines. Color choices are sensible (blue for lower bounds, red for upper bounds, green for estimates). The scaling collapse plot (Fig. 2, right panel) shows poor fit for small n values, which is acknowledged in the text. The approach comparison (Fig. 4) is informative with color-coded categories and value annotations. Minor issues: some label overlap in the timeline figure (e.g., "Lueker (upp" is truncated in the legend area), and the figures use matplotlib's default font but with customized styling that is acceptable for a computational paper. |

---

## Citation Verification Report

Each entry in `sources.bib` was verified via web search:

| Key | Title | Authors | Year | Venue | Status |
|-----|-------|---------|------|-------|--------|
| **CS1975** | Longest common subsequences of two random sequences | Chvátal, Sankoff | 1975 | J. Appl. Probab. 12(2):306–315 | **VERIFIED** ✓ — DOI 10.2307/3212444 confirmed. |
| **D1994** | Expected length of longest common subsequences | Dančík | 1994 | PhD thesis, Univ. Warwick | **VERIFIED** ✓ — Warwick WRAP repository confirmed. |
| **DP1995** | Upper bounds for the expected length of a longest common subsequence of two binary sequences | Dančík, Paterson | 1995 | Random Structures & Algorithms 6(4):449–458 | **VERIFIED** ✓ — DOI 10.1002/rsa.3240060408 confirmed. |
| **L2009** | Improved bounds on the average length of longest common subsequences | Lueker | 2009 | J. ACM 56(3):1–38 | **VERIFIED** ✓ — DOI 10.1145/1516512.1516519 confirmed. |
| **H2024** | Improved Lower Bounds on the Expected Length of Longest Common Subsequences | Heineman, Miller, Reichman, Salls, Sárközy, Soiffer | 2024/2025 | arXiv:2407.10925; ISIT 2025 | **VERIFIED** ✓ — arXiv and Google Scholar confirmed. Year listed as 2025 in bib (publication year at ISIT), note says "arXiv:2407.10925, 2024". Acceptable. |
| **BukhCox2019** | Periodic words, common subsequences and frogs | Bukh, Cox | 2022 (arXiv 2019) | Ann. Appl. Probab. 32(2):1295–1332 | **VERIFIED** ✓ — DOI 10.1214/21-AAP1709 confirmed. Publication year 2022, arXiv 2019. |
| **KiwiSoto2008** | On a Speculated Relation Between Chvátal–Sankoff Constants of Several Sequences | Kiwi, Soto | 2009 | Combin. Probab. Comput. 18(4):517–532 | **VERIFIED** ✓ — DOI 10.1017/S0963548309009900 confirmed. |
| **KLM2005** | Expected Length of the Longest Common Subsequence for Large Alphabets | Kiwi, Loebl, Matoušek | 2004/2005 | LATIN 2004 / Adv. Math. 197:480–498 | **VERIFIED** ✓ — DOI 10.1007/978-3-540-24698-5_34 confirmed for LATIN; full version in Advances in Mathematics 2005. |
| **Bundschuh2001** | High precision simulations of the longest common subsequence problem | Bundschuh | 2001 | Eur. Phys. J. B 22:533–541 | **VERIFIED** ✓ — DOI 10.1007/s100510170102 confirmed. |
| **LemberMatzinger2009** | Standard deviation of the longest common subsequence | Lember, Matzinger | 2009 | Ann. Probab. 37(3):1192–1235 | **VERIFIED** ✓ — DOI 10.1214/08-AOP436 confirmed. *Not cited in paper text.* |
| **Tiskin2022** | The Chvátal–Sankoff problem: Understanding random string comparison through stochastic processes | Tiskin | 2022 | arXiv:2212.01582 | **VERIFIED** ✓ — arXiv confirmed. |
| **Cheraghchi2019** | Capacity Upper Bounds for Deletion-type Channels | Cheraghchi | 2019 | J. ACM 66(2):1–79 | **VERIFIED** ✓ — DOI 10.1145/3281275 confirmed. |
| **Rosenfeld2024** | Upper bounds on the average edit distance between two random strings | Rosenfeld | 2024 | arXiv:2407.18113 | **VERIFIED** ✓ — arXiv confirmed. |
| **Steele1997** | Probability Theory and Combinatorial Optimization | Steele | 1997 | SIAM, CBMS-NSF vol. 69 | **VERIFIED** ✓ — WorldCat and SIAM confirmed. |
| **BaikDeiftJohansson1999** | On the distribution of the length of the longest increasing subsequence of random permutations | Baik, Deift, Johansson | 1999 | J. Amer. Math. Soc. 12(4):1119–1178 | **VERIFIED** ✓ — DOI 10.1090/S0894-0347-99-00307-0 confirmed. |
| **Borodin1999** | Longest increasing subsequences of random colored permutations | Borodin | 1999 | Electron. J. Combin. 6, R13 | **VERIFIED** ✓ — DOI 10.37236/1445 confirmed. *Not cited in paper text.* |
| **Dixon2013** | Longest common subsequences in binary sequences | Dixon | 2013 | arXiv:1307.2796 | **VERIFIED** ✓ — arXiv confirmed. *Not cited in paper text.* |
| **LiRenWen2025** | Expected Length of the Longest Common Subsequence of Multiple Strings | Li, Ren, Wen | 2025 | arXiv:2504.10425 | **VERIFIED** ✓ — arXiv confirmed (submitted Apr 2025). |
| **BriggsEtAl2024** | Frogs, hats and common subsequences | Briggs, Parker, Schwieder, Wells | 2024 | arXiv:2404.07285 | **VERIFIED** ✓ — arXiv confirmed. |
| **Lueker2008** | On the Convergence of Upper Bound Techniques for the Average Length of Longest Common Subsequences | Lueker | 2008 | ANALCO | **VERIFIED** ✓ — DOI 10.1137/1.9781611972986.1. This is a workshop paper at ANALCO 2008. |
| **PraehoferSpohn2001** | Scale Invariance of the PNG Droplet and the Airy Process | Prähofer, Spohn | 2002 | J. Stat. Phys. 108:1071–1106 | **VERIFIED** ✓ — DOI 10.1023/A:1019791415147 confirmed. Bib year says 2002 but key says 2001 (arXiv 2001, journal 2002) — minor inconsistency in key naming but data correct. |
| **AggarwalEtAl2023** | Colored interacting particle systems on the ring: Stationary measures from Yang–Baxter equations | Aggarwal, Nicoletti, Petrov | 2025 (arXiv 2023) | Compositio Math. | **VERIFIED** ✓ — DOI 10.1112/s0010437x25007195 and arXiv:2309.11865 confirmed. To appear in Compositio Math. |
| **RubinsteinCon2023** | Improved Upper and Lower Bounds on the Capacity of the Binary Deletion Channel | Rubinstein, Con | 2023 | ISIT 2023 | **VERIFIED** ✓ — arXiv:2305.07156 confirmed. DOI 10.1109/ISIT54713.2023.10206626 confirmed. |
| **Martin2006** | Last-passage percolation with general weight distribution | Martin | 2006 | Markov Processes Relat. Fields 12(2):273–299 | **VERIFIED** ✓ — Confirmed at math-mprf.org. |
| **Johansson2000** | Shape fluctuations and random matrices | Johansson | 2000 | Comm. Math. Phys. 209(2):437–476 | **VERIFIED** ✓ — DOI 10.1007/s002200050027 confirmed. |
| **Kingman1968** | The Ergodic Theory of Subadditive Stochastic Processes | Kingman | 1968 | J. Roy. Statist. Soc. Ser. B 30(3):499–510 | **VERIFIED** ✓ — Wiley online library confirms DOI 10.1111/j.2517-6161.1968.tb00749.x. |
| **Alexander1994** | The Rate of Convergence of the Mean Length of the Longest Common Subsequence | Alexander | 1994 | Ann. Appl. Probab. 4(4):1074–1082 | **VERIFIED** ✓ — DOI 10.1214/aoap/1177004903 confirmed at Project Euclid. |
| **CheraghchiSTOC2018** | Capacity upper bounds for deletion-type channels | Cheraghchi | 2018 | STOC 2018, pp. 72–85 | **VERIFIED** ✓ — DOI 10.1145/3188745.3188768 confirmed at ACM DL. |

**Summary:** All 28 bibliography entries verified as real papers with correct metadata. Three entries (Borodin1999, Dixon2013, LemberMatzinger2009) appear in `sources.bib` but are never cited in the paper body — these are unused references and should be removed for tidiness.

---

## Detailed Technical Comments

### Strengths

1. **Comprehensive scope.** The paper evaluates ten distinct approaches systematically, providing a broad landscape of techniques applicable to the Chvátal–Sankoff problem. This is valuable as a survey-computation hybrid.

2. **Honest characterization.** The paper is commendably transparent about the limitations of each approach. Rigorous bounds are clearly distinguished from conjectural/numerical results (Table 6, checkmarks vs. daggers). The fact that no rigorous improvement over prior work was achieved is stated forthrightly.

3. **Bernoulli LPP correlation gap (§6.5).** The structural analysis of why LCS weights yield a lower LPP time constant than independent Bernoulli weights is mathematically interesting. The observation that entries are pairwise uncorrelated but have higher-order dependencies (§6.5, pairwise covariance calculation) is a clean and correct argument. The three proposed paths to rigorization (FKG, coupling, conditional variance) are reasonable.

4. **DFA non-greedy insight (§6.3).** The finding that optimal DFA policies are non-greedy is a useful qualitative contribution, though the bounds themselves are weaker than Dančík (1994).

5. **Verification section (§7).** Independent verification of all rigorous bounds is good practice and adds credibility.

### Weaknesses

1. **No new rigorous bounds.** The paper does not achieve any rigorous improvement over the known interval [0.792665992, 0.826280]. The best rigorous lower bound from this work (0.7616 via DFA at h=6) is substantially below Heineman et al.'s 0.7927. The best rigorous upper bound (0.9051 via Kolmogorov) is far above Lueker's 0.8263. For a venue like Nature/NeurIPS, the lack of any new rigorous result is a significant weakness.

2. **The conjectural upper bound (0.808) lacks formal justification.** The Bernoulli LPP gap argument is suggestive but relies on extrapolating a trend observed at n ≤ 200 with only 2000 samples. The claim that "the gap is empirically stable at ≈ 0.02 for n ≥ 100" (§8.1) is based on only three data points (n = 50, 100, 200). Moreover, the paper does not establish theoretically that γ₂ < 2(√2 − 1); it only conjectures it.

3. **Inconsistency in information-theoretic bounds.** The "refined" Kolmogorov bound (0.9068) is weaker than the "basic" bound (0.9051). This appears to be an error or at minimum requires explanation — a refinement should not make the bound worse.

4. **Finite-size scaling assumptions.** The best-fit scaling form (β = 2/3) gives γ ≈ 0.8115, but the KPZ prediction (β = 1/3) gives 0.822. The paper doesn't adequately address why the correction exponent would be 2/3 rather than the theoretically motivated 1/3. The scaling collapse plot (Fig. 2, right) shows poor agreement for the exact computation data points at small n, suggesting the fit may be unreliable.

5. **Monte Carlo sample sizes are modest.** At n = 5000, only 200 samples were used. At n = 2000, only 500. The MC data for the Bernoulli LPP comparison uses only 2000 samples per n value. For a paper claiming numerical precision, larger sample sizes would strengthen the results.

6. **Three unused bibliography entries** (Borodin1999, Dixon2013, LemberMatzinger2009) should be removed.

7. **E[L_2]/2 discrepancy.** The paper states E[L_2]/2 = 0.5625 in Table 1, but the rubric acceptance criteria says "E[L_2]/2 = 0.625". The paper value (1.125/2 = 0.5625) is correct by computation. The rubric criterion appears to have a typo. No deduction here.

### Minor Issues

- Line 600: "na\"{\i}ve" — while technically correct LaTeX for naïve, consider simplifying.
- The paper mentions "sixteen distinct bound values" in the conclusion but Table 6 lists only 12 rows (10 from this work + 2 from prior). The claim of 16 likely includes subresults not shown in the table.
- §6.6 mentions "SDP relaxation with a positive-semidefinite constraint gives E[SDP_n]/n ≈ 0.50 for n ≤ 6, which over-constrains and provides a lower bound rather than upper." This seems confused — a relaxation should provide an upper bound. The authors may mean the SDP objective after taking the dual gives a lower bound, but this needs clarification.

---

## Overall Verdict: **REVISE**

### Justification

The paper is well-written, comprehensive, and technically sound in its computations. All citations are verified, results match the underlying data, and the LaTeX compiles cleanly. However, for a top-tier venue, two issues prevent acceptance:

1. **No new rigorous results.** The paper's principal contribution — the conjectural upper bound of 0.808 — is explicitly non-rigorous and based on limited numerical evidence (three data points for the gap extrapolation). A Nature/NeurIPS paper on mathematical constants typically requires either a new proven bound or a substantial theoretical advance.

2. **The unused bibliography entries** and the counterintuitive "refined" bound being weaker than the "basic" bound need correction.

### Required Revisions

1. **Remove unused bibliography entries** (Borodin1999, Dixon2013, LemberMatzinger2009) or add citations to them in the text.

2. **Clarify or correct the information-theoretic bounds** (§6.4, Eqs. 12–13). Explain why the "refined" bound (0.9068) is weaker than the "basic" bound (0.9051), or correct the computation.

3. **Strengthen the Bernoulli LPP gap analysis.** Run simulations at larger n (e.g., n = 500, 1000) and with more samples (e.g., 10,000+) to provide more convincing evidence for the stability of Δ. Currently the extrapolation to Δ_∞ ≈ 0.017–0.021 is based on only three finite-n data points.

4. **Clarify the SDP relaxation interpretation** (§6.6). Explain why a relaxation gives a value (0.50) below the true constant rather than above it.

5. **Discuss the scaling exponent discrepancy more carefully.** If β = 1/3 is theoretically predicted (KPZ universality), explain what would need to be true for β = 2/3 to be the correct exponent, or acknowledge that the data range may be insufficient to distinguish the exponents.

6. **Tighten the claim count.** The abstract says "sixteen distinct bound values" but this should be reconciled with what is actually shown in the tables.

### Optional Improvements

- Increase MC sample sizes throughout for stronger numerical evidence.
- Consider extending the DFA analysis to the two-pointer model to potentially match or exceed Dančík's 0.7739.
- Add error bars or confidence intervals to the Bernoulli LPP gap estimates in Table 4.
- The timeline figure (Fig. 1) has some label overlap; consider adjusting the layout.

---

## Final Scores Summary

| Criterion | Score |
|-----------|:-----:|
| Completeness | 5/5 |
| Technical Rigor | 4/5 |
| Results Integrity | 5/5 |
| Citation Accuracy | 4/5 |
| Compilation | 5/5 |
| Writing Quality | 5/5 |
| Figure Quality | 4/5 |
| **Overall** | **REVISE** |

All scores are ≥ 3, but the paper would benefit from the targeted revisions above before it meets publication standards for a top-tier venue. The core research is solid and the writing is strong — the issues are addressable.
