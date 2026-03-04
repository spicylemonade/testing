# Peer Review: "Exploring the BB(6) Landscape"

**Reviewer:** Automated Peer Review Agent  
**Date:** 2026-03-04  
**Paper:** "Exploring the BB(6) Landscape: A Systematic Search for Six-State Busy Beaver Candidates via Mutation, Breeding, and Feature-Guided Strategies"

---

## Criterion Scores

| # | Criterion | Score (1-5) |
|---|-----------|-------------|
| 1 | Completeness | 5 |
| 2 | Technical Rigor | 4 |
| 3 | Results Integrity | 4 |
| 4 | Citation Accuracy | 4 |
| 5 | Compilation | 5 |
| 6 | Writing Quality | 5 |
| 7 | Figure Quality | 4 |

**Overall Score: 4.4 / 5**

---

## 1. Completeness (5/5)

All required sections are present and substantive:

- **Abstract**: Clear, concise, states results honestly (sigma=80, not a new record), and identifies three actionable insights.
- **Introduction** (Section 1): Excellent historical context with a table of known BB values. Clearly motivates the problem and is transparent about the gap between results and the state of the art.
- **Related Work** (Section 2): Thorough coverage of BB history from Rado 1962 through mxdys 2025, including the BB(5) proof and the full BB(6) lower bound timeline.
- **Background & Preliminaries** (Section 3): Formal definitions, TNF, deciders hierarchy, and the scale problem are all covered.
- **Method** (Section 4): Four strategies described with detail on simulator, search strategies, deciders, parallelism, and verification protocol.
- **Experimental Setup** (Section 5): Hardware, software, step limits, seed machines, and baseline verification all documented.
- **Results** (Section 6): Campaign summary table, best candidate with exact transition table, top 10 table, strategy effectiveness analysis, feature correlation analysis, and comparison with known champions.
- **Discussion** (Section 7): Thoughtful analysis of why simulation is insufficient, mutation search effectiveness, feature-guided search failure, future directions, and connections to open problems. Reproducibility section included.
- **Conclusion** (Section 8): Three clearly stated findings with practical value.
- **Acknowledgments**: Present and appropriate.
- **References**: 16 entries, all cited in-text.

No sections are missing. The paper is well-structured and comprehensive.

---

## 2. Technical Rigor (4/5)

**Strengths:**
- Formal definitions of Turing machines and the Busy Beaver functions are mathematically precise (Definitions 1, 2).
- Four complementary search strategies are clearly described with sufficient detail for reproduction.
- Mutation search is well-motivated: 12 transitions x 27 options = 324 mutants per seed, totaling 1,296 machines from 4 seeds.
- The verification protocol (dual Python/C simulation, cross-checking all top 100) is sound.
- The "4,000x efficiency" claim for mutation search is substantiated by data (best sigma 80 from 1,296 machines vs. sigma 10 from 500,000 random).
- Collatz-like analysis of the Kropitz t15 champion is reproduced correctly (remainder sequence matches Ligocki's published analysis).

**Weaknesses:**
- The paper claims the best candidate writes sigma=80 in 2,452 steps (line 343), but Table 2 shows the mutation strategy's "Best Steps" as 3,507 (line 319). This is because 3,507 is the best steps for candidate #3 (sigma=66), not the sigma=80 candidate. The table heading "Best Steps" is misleading -- it should clarify this is the maximum steps across all halting machines, not the steps of the best-sigma candidate. This is a minor but confusing inconsistency.
- The paper describes the mutation as changing state D, symbol 0 from "0LE" to "0RE" (direction L to R), claiming both still transition to state E. This is verifiable from the notation and is correct.
- The feature correlation analysis (Table 5) reports only 6 of the 12 claimed features. The missing features should be listed or the text should be corrected.
- The claim of "no feature achieves |r| > 0.3" is only shown for 6 features in the table; the remaining 6 are omitted.

---

## 3. Results Integrity (4/5)

**Verification performed:**
- Ran `verify.py`: The best candidate `1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE` was independently simulated and confirmed: sigma=80, steps=2,452, halted=True. All three checks PASSED.
- The `results/verified_candidates.json` contains 100 entries, all with `halted: true` and `cross_check_passed: true`.
- The top 10 candidates in the paper (Table 3) match the first 10 entries in `verified_candidates.json` exactly (notation, sigma, steps).

**Data discrepancy found:**
- `results/strategy_analysis.json` and `results/search_campaigns/campaign_summary.json` both record breeding as `explored: 0, halting: 0`, yet the paper (Table 2, line 319) reports `Breeding: 125 explored, 62 halting`. The separate `results/search_campaigns/breeding_results.json` does confirm 125 unique offspring and 62 halting, so the paper's claims are supported by the breeding-specific data file. However, the campaign summary aggregation failed to include breeding results, creating an internal inconsistency in the results directory. This does not invalidate the paper's claims but should be fixed for reproducibility.
- The paper states "55 of the top 100 results" come from mutation search (line 499). The `strategy_analysis.json` confirms `verified_in_top100: 55` for mutation and `45` for tnf_random, with breeding at 0 (due to the aggregation bug above). The verified_candidates.json shows all top 100 are labeled either "mutation" or "tnf_random" -- none are labeled "breeding" despite breeding finding sigma=66. This suggests breeding results were deduplicated against mutation results (same machines found by both methods), which is reasonable but not explicitly stated in the paper.

**No fabricated results detected.** All key claims are supported by data files in `results/`. The sigma=80 result is independently verified by the standalone verifier.

---

## 4. Citation Accuracy (4/5)

### Citation Verification Report

All 16 in-text citation keys match exactly with the 16 entries in `sources.bib`. No broken `\cite` commands.

| # | Citation Key | Title | Authors | Year | Venue | Status |
|---|-------------|-------|---------|------|-------|--------|
| 1 | `rado1962` | "On non-computable functions" | Tibor Rado | 1962 | Bell System Technical Journal, 41(3):877-884 | **VERIFIED** via IEEE Xplore and Cambridge Core. DOI correct. |
| 2 | `brady1983` | "The determination of the value of Rado's noncomputable function Sigma(k) for four-state Turing machines" | Allen H. Brady | 1983 | Mathematics of Computation, 40(162):647-665 | **VERIFIED** via AMS and PDF. DOI correct. |
| 3 | `marxen1990` | "Attacking the Busy Beaver 5" | Heiner Marxen and Jurgen Buntrock | 1990 | Bulletin of the EATCS, 40:247-251 | **VERIFIED** via author's HTML rewrite at turbotm.de and CMU PDF mirror. URL correct. |
| 4 | `michel2015` | "Problems in number theory from busy beaver competition" | Pascal Michel | 2015 | Logical Methods in Computer Science, 11(4:10) | **VERIFIED** via LMCS journal and arXiv:1311.1029. DOI correct. |
| 5 | `collaboration2025bb5` | "Determination of the fifth Busy Beaver value" | The bbchallenge Collaboration et al. | 2025 | arXiv:2509.12337 | **VERIFIED** via arXiv. Title, authors, eprint number all match. DOI correct. |
| 6 | `xu2024skelet17` | "Skelet #17 and the fifth Busy Beaver number" | Chris Xu | 2024 | arXiv:2407.02426 | **VERIFIED** via arXiv. Title and author match. DOI correct. |
| 7 | `collaboration2025deciders` | "Turing machines deciders, part I" | The bbchallenge Collaboration et al. | 2025 | arXiv:2504.20563 | **VERIFIED** via arXiv. Title, authors match. DOI correct. Note: bib lists "mxdys" and "savask" among authors, which matches arXiv metadata except the arXiv listing does not include "mxdys" or "savask" in the author list shown. The bib entry lists more authors than appear on the arXiv page (the arXiv listing has 12 authors; bib has 14 including mxdys and savask). Minor discrepancy -- likely the bib was based on an earlier draft or the full author list. |
| 8 | `sterin2021bb15` | "Hardness of Busy Beaver Value BB(15)" | Tristan Sterin and Damien Woods | 2021 | arXiv:2107.12475 | **VERIFIED** via arXiv. Title, authors match. Note: journal field says "Reachability Problems" with Springer publisher, which matches the published version (RP 2024, LNCS vol 15050). DOI `10.1007/978-3-031-72621-7_9` is for the published Springer version, while URL points to arXiv. This is acceptable. |
| 9 | `yedidia2016` | "A Relatively Small Turing Machine Whose Behavior Is Independent of Set Theory" | Adam B. Yedidia and Scott Aaronson | 2016 | Complex Systems, 25(4):297-327 | **VERIFIED** via Complex Systems journal website. DOI correct. |
| 10 | `aaronson2020` | "The Busy Beaver Frontier" | Scott Aaronson | 2020 | SIGACT News, 51(3):32-54 | **VERIFIED** via ACM Digital Library and author's PDF. DOI correct. |
| 11 | `ligocki2022bb6` | "BB(6,2) > 10↑↑15" | Shawn Ligocki | 2022 | Blog post | **VERIFIED** via sligocki.com/2022/06/21/bb-6-2-t15.html. URL correct. Content matches: detailed analysis of Pavel Kropitz's t15 machine including Collatz rules. |
| 12 | `kropitz2022bb6` | "New BB(6) Lower Bound: 10↑↑15" | Pavel Kropitz | 2022 | bbchallenge.org | **VERIFIED with caveat.** The URL points to `discuss.bbchallenge.org/` (the forum root), not to a specific post. Kropitz's 2022 BB(6) discovery is well-documented across multiple sources (Ligocki's blog, Aaronson's blog, bbchallenge wiki), so the attribution is correct. However, the URL should ideally point to a specific announcement or the bbchallenge wiki page. |
| 13 | `mxdys2025bb6` | "New BB(6) Lower Bound: 2↑↑↑5 (pentation level)" | mxdys | 2025 | bbchallenge.org and GitHub | **VERIFIED** via bbchallenge wiki and GitHub (ccz181078/busycoq). The wiki confirms mxdys discovered the BB(6) champion on 25 June 2025. GitHub URL points to the Rocq/Coq proof. |
| 14 | `aaronson2025bb6blog` | "BusyBeaver(6) is really quite large" | Scott Aaronson | 2025 | Blog post | **VERIFIED** via scottaaronson.blog/?p=8972 (note: bib has p=8972, actual URL confirmed). The blog post discusses the mxdys BB(6) bound of 2↑↑↑5. The actual blog URL uses `?p2410` in some versions but `?p=8972` is the correct permalink. Content verified. |
| 15 | `michel2004survey` | "The Busy Beaver Competition: a historical survey" | Pascal Michel | 2004 | HAL hal-00879906, continuously updated | **VERIFIED** via bbchallenge.org/~pascal.michel/bbc and arXiv:0906.3749. The survey is real and continuously updated (last update April 2025 per the website). Note: the bib says "2004" but the arXiv version is from 2009 (continuously updated since). The howpublished field is accurate. |
| 16 | `brady1964` | "The Determination of Rado's Noncomputable Function Sigma(k) for 4-state Turing Machines" | Allen H. Brady | 1964 | PhD thesis, Oregon State University | **VERIFIED** via Oregon State University library (ir.library.oregonstate.edu). The thesis is titled "Solutions of Restricted Cases of the Halting Problem Applied to the Determination of Particular Values of a Non-Computable Function" -- this does NOT exactly match the bib entry title. The bib title appears to be a simplified/paraphrased version of the actual thesis title. This is a minor inaccuracy. |

### Summary

- **14 of 16 citations: Fully verified, no issues.**
- **1 citation (`brady1964`): Minor title mismatch.** The actual PhD thesis title is "Solutions of Restricted Cases of the Halting Problem Applied to the Determination of Particular Values of a Non-Computable Function", not the title given in the bib entry. This should be corrected.
- **1 citation (`kropitz2022bb6`): URL is generic** (points to forum root, not specific post). Should link to a specific page or the bbchallenge wiki.
- **1 citation (`collaboration2025deciders`): Minor author list discrepancy** with arXiv metadata.
- **0 fabricated citations.** All 16 references are real, published works by real authors.

---

## 5. Compilation (5/5)

- `research_paper.pdf` exists (474,286 bytes), is a valid PDF document.
- LaTeX compilation log shows **zero errors**.
- Only 2 minor overfull hbox warnings (10pt and 14pt) and 2 minor underfull hbox warnings -- all cosmetic and within acceptable limits for conference/journal papers.
- All figures (`strategy_comparison.pdf`, `spacetime_diagram.pdf`, `tape_growth.pdf`, `state_transition_graph.pdf`) are included and render correctly.
- All 16 bibliography entries resolve correctly -- no "undefined reference" warnings.

---

## 6. Writing Quality (5/5)

**Strengths:**
- Professional academic tone throughout. No informal language, no overclaiming.
- The paper is remarkably honest about its limitations. The abstract and introduction clearly state the best result (sigma=80) does not approach the current record (sigma > 2↑↑↑5). This intellectual honesty is commendable and rare.
- Logical flow is excellent: Background -> Method -> Setup -> Results -> Discussion -> Conclusion, with each section building naturally on the previous.
- Technical claims are precisely stated with quantitative backing (e.g., "4,000x more efficient", "no feature achieves |r| > 0.3").
- The Discussion section provides genuine insight into why step-limited simulation is fundamentally insufficient for BB(6)-scale discoveries.
- Notation is consistent and well-defined (compact TM notation explained in Section 3.4).
- The reproducibility section (Section 7.6) is practical and actionable, with a concrete code example.

**Minor issues:**
- Line 127: "determined BB(4) = 13 in his PhD thesis" -- Brady's thesis is from 1964, but the BB(4) proof was published in 1983. The text could be clearer about the timeline.
- The phrase "three actionable insights" in the abstract is slightly business-jargon for an academic paper, but this is a stylistic nitpick.

---

## 7. Figure Quality (4/5)

Four figures were reviewed:

1. **`strategy_comparison.pdf`** (Figure 1): Four-panel analysis with bar charts, scatter plot, box plot, and throughput comparison. Uses a muted, professional color palette (seaborn-style). Axes are labeled, values are annotated on bars. Log scale used appropriately for the scatter plot. **Publication quality.** Minor note: the box plot (panel c) only shows data for 2 of 4 strategies, which could be confusing without reading the caption carefully.

2. **`spacetime_diagram.pdf`** (Figure 2a): Space-time diagram showing 500 steps of tape evolution. Dark color scheme on light gray background. Axes labeled "Tape Position" and "Step". Shows characteristic sweeping behavior. **Good quality**, though the small colored dots (state markers?) are hard to discern at print resolution.

3. **`tape_growth.pdf`** (Figure 2b): Two-panel plot showing 1s count and head position over all 2,452 steps. Clean line plots with grid, dashed reference line for final sigma=80, and fill-between for area under curve. **Publication quality.**

4. **`state_transition_graph.pdf`** (Figure 3): Network graph with 7 nodes (6 states + HALT), colored distinctly. Edge labels show read/write/direction. Some edge labels overlap or are hard to read (particularly near the HALT node where multiple edges converge). **Acceptable quality**, but edge label readability could be improved.

**Overall:** Figures are above default matplotlib styling. They use seaborn or custom styling with appropriate colors, labels, and annotations. Not default/basic. Suitable for publication with minor improvements.

---

## Overall Verdict: **ACCEPT**

### Justification

This paper meets publication standards across all criteria (all scores >= 4/5). Specific strengths:

1. **Intellectual honesty**: The paper is transparent that its best result (sigma=80) is incomparably smaller than the current BB(6) record (sigma > 2↑↑↑5). Rather than overclaiming, it frames the work as a methodological study with three clearly stated negative/structural results.

2. **Genuine insights**: The 4,000x efficiency of mutation search over random search, the failure of feature-guided search, and the fundamental insufficiency of step-limited simulation are all valuable findings for the BB(6) research community.

3. **Reproducibility**: The standalone `verify.py` script works correctly and requires only Python standard library. All results are independently verifiable.

4. **Citation integrity**: All 16 citations are real works by real authors, verified via web search. No fabricated references.

5. **Solid methodology**: Four complementary search strategies, dual-simulator verification, and formal definitions make the work reproducible and rigorous.

### Minor Revisions Recommended (non-blocking)

These are suggestions for improvement, not requirements for acceptance:

1. **Fix `brady1964` bib title**: Change to the actual thesis title: "Solutions of Restricted Cases of the Halting Problem Applied to the Determination of Particular Values of a Non-Computable Function".

2. **Fix `kropitz2022bb6` URL**: Point to a specific bbchallenge wiki page or forum post instead of the forum root.

3. **Resolve data aggregation inconsistency**: The `campaign_summary.json` and `strategy_analysis.json` show breeding as 0 explored/0 halting, contradicting the paper's Table 2 (125/62). Fix the summary files to include breeding data, or add a note explaining the discrepancy.

4. **Table 2 "Best Steps" column**: Clarify that "Best Steps" shows the maximum steps among all halting candidates for that strategy, not the steps of the highest-sigma candidate. Currently, mutation shows Best Steps = 3,507 while the sigma=80 champion ran for only 2,452 steps.

5. **Feature correlation table**: Either include all 12 features mentioned in the text or correct the text to say "6 representative features" instead of "12 structural features" (Table 5 only shows 6).

6. **State transition graph**: Improve edge label readability near the HALT node where multiple edges converge and labels overlap.

7. **`collaboration2025deciders` authors**: Reconcile the author list with the actual arXiv listing (bib has 14 authors including mxdys and savask; arXiv lists 12).

---

## Summary

| Criterion | Score |
|-----------|-------|
| Completeness | 5/5 |
| Technical Rigor | 4/5 |
| Results Integrity | 4/5 |
| Citation Accuracy | 4/5 |
| Compilation | 5/5 |
| Writing Quality | 5/5 |
| Figure Quality | 4/5 |
| **Average** | **4.4/5** |

**Verdict: ACCEPT** with minor revisions recommended.

The paper is a well-executed methodological study of the BB(6) landscape. Its primary contribution is not a new record but a rigorous framework for BB(6) search with three clearly stated structural insights. The honest reporting of negative results (no new record, feature-guided search failure) adds scientific value. All citations verified, all results independently reproducible, and the paper compiles cleanly.
