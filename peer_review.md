# Peer Review

## Major Findings

1. **Citation accuracy fails the zero-tolerance bar.** `sources.bib` contains five local `archivara2026*` entries that are not externally web-verifiable, one clear metadata mismatch (`hernandez2013tegboost`), and six real papers whose BibTeX author fields are truncated with `and others`, so the author metadata does not fully match the actual paper records. Under the stated review rules, that alone blocks acceptance.
2. **The work is not strong enough as a novel circuit paper.** The repository supports a narrow same-family falsification/simplification result: in this helper-free model, explicit pre-handoff ranking was not necessary, and a blind packet gate matched or beat the ranked design on the executed falsifiers. That is interesting, but it is not a genuinely new multi-source energy-harvesting architecture.
3. **The surviving positive mechanism claim is not causally isolated.** The repo's own benchmark audit notes that `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/blind_packet_merge/blind_packet_merge.cir` exists but was not run. Without that same-scaffold no-packet-gate control, the claim "packet-gated isolation matters" still rests on comparisons that change more than one mechanism at once.
4. **The quantitative core is mostly real, but two reporting issues remain.** The bottom-right energy panel in the ablation tradeoff figure uses all-row medians from `tools/analyze_h1_results.py:317`, while the surrounding text and Table 2 use successful-case medians from `startup_summary.json`. Also, `nonzero_backdrive_cases` in `falsifier_summary.json` is thresholded rather than literal, which obscures positive raw back-drive values in several `nonaware` falsifier rows.
5. **The paper compiles, but not cleanly enough to call the presentation finished.** I ran `pdflatex -> bibtex -> pdflatex -> pdflatex` on March 12, 2026. The build succeeded and produced `research_paper.pdf`, but the log still contains overfull/underfull box warnings and `T1/cmr/m/scit` font fallback warnings.

## Scorecard

| Criterion | Score | Rationale |
| --- | ---: | --- |
| Completeness | 5/5 | The manuscript contains Abstract, Introduction, Related Work, Background/Preliminaries, Method, Experimental Setup, Results, Discussion, Conclusion, and References. |
| Technical Rigor | 3/5 | The paper is reproducible and equation-heavy, but rigor is limited by the aliased 24-case startup matrix, the unexecuted same-scaffold control, proxy handoff/chatter measurements, and undocumented thresholding in back-drive summaries. |
| Results Integrity | 4/5 | The main headline counts and several raw spot-checks match the tables and raw JSON/log artifacts. Two reporting inconsistencies remain: the ablation energy panel uses a different statistic than the text, and `nonzero_backdrive_cases` is mislabeled. |
| Citation Accuracy | 1/5 | Multiple entries are incorrect or non-verifiable under the stated rules. Citation accuracy is the weakest part of the package. |
| Compilation | 4/5 | The PDF exists and the full LaTeX pipeline succeeds, but the build still emits formatting warnings and font-shape fallbacks. |
| Writing Quality | 4/5 | The prose is clear, professional, and well-structured, but several novelty and mechanism claims are overstated relative to the evidence. |
| Figure Quality | 3/5 | The figures are readable and export well, but several are still stock seaborn/matplotlib report figures rather than publication-finished visuals, and one panel uses the wrong statistic. |
| Novelty & Creative Contribution | 2/5 | The paper's best contribution is a narrow negative-result simplification study. It does not yet demonstrate a genuinely new architecture, surprising new operating regime, or a creative CE-derived mechanism that materially changes the state of the art. |

## Citation Verification Report

I verified every `sources.bib` entry via web search plus DOI resolution where available. I also checked the manuscript's in-text citations: all in-text `\cite` keys resolve to entries in `sources.bib`; there are no dangling cite keys. There are 38 in-text citations spanning 16 unique bibliography keys.

| Key | Cited in text | Status | Verification result |
| --- | --- | --- | --- |
| `hernandez2013tegboost` | no | **Incorrect** | DOI `10.1007/S10470-014-0472-0` resolves to *Fully integrated boost converter for thermoelectric energy harvesting in 180 nm CMOS* in *Analog Integrated Circuits and Signal Processing* with publication year 2015, not a 2013 IEEE LASCAS paper. Year and venue do not match the BibTeX entry. |
| `goppert2016startup70mv` | yes | **Verified** | DOI resolves to the 2016 IEEE JSSC paper; title, year, venue, and authors are consistent. |
| `das2017selfstarter` | yes | **Verified** | DOI resolves to the 2017 IEEE TCAS-I paper; title, year, venue, and authors are consistent. |
| `tang2018dualsource` | yes | **Verified** | DOI resolves to the 2018 IEEE CICC conference paper; title, year, venue, and author list are consistent. |
| `quintero2019cmosstartup` | yes | **Verified** | DOI resolves to the 2019 IEEE Latin America Transactions paper; title, year, venue, and authors are consistent. |
| `coustans2019coldstart60mv` | yes | **Verified** | DOI resolves to the 2019 IEEE TCAS-II paper; title, year, venue, and authors are consistent. |
| `alhawari2016multisourcepmu` | no | **Incorrect** | The paper exists, but the BibTeX entry uses an incomplete author field (`and others`). Under the stated rule that authors must match, this entry is inaccurate. |
| `alghisi2017batteryless` | yes | **Verified** | DOI resolves to the 2017 *Sensors and Actuators A: Physical* paper; title, year, venue, and authors are consistent. |
| `wang2021serialsshi` | no | **Incorrect** | The paper exists, but the BibTeX entry truncates the author list with `and others`, so the author metadata does not fully match the paper record. |
| `xia2022dualinductor` | no | **Incorrect** | The paper exists, but the BibTeX entry truncates the author list with `and others`, so the author metadata does not fully match the paper record. |
| `zheng2023sharedinductor` | no | **Verified** | DOI resolves to the 2023 IEEE PEAS conference paper; title, year, venue, and authors are consistent. |
| `wang2023serialstack` | yes | **Incorrect** | The paper exists, but the BibTeX entry truncates the author list with `and others`, so the author metadata does not fully match the paper record. |
| `lu2024tegassist` | no | **Incorrect** | The paper exists, but the BibTeX entry truncates the author list with `and others`, so the author metadata does not fully match the paper record. |
| `chen2024collaborative` | yes | **Incorrect** | The paper exists, but the BibTeX entry truncates the author list with `and others`, so the author metadata does not fully match the paper record. |
| `weng2024osece` | yes | **Verified** | Web results and DOI metadata both resolve to the 2024 IEICE Electronics Express paper; title, year, venue, and authors are sufficiently consistent. |
| `gogolou2025multisourcereview` | yes | **Verified** | DOI resolves to the 2025 *Electronics* review article; title, year, venue, and authors are consistent. |
| `archivara2026repo` | yes | **Incorrect** | Local repository artifact only; no external web-verifiable paper/report record. Under the stated review rule, non-verifiable entries must be flagged incorrect. |
| `archivara2026rubric` | no | **Incorrect** | Local repository artifact only; no external web-verifiable paper/report record. |
| `archivara2026toolplan` | no | **Incorrect** | Local repository artifact only; no external web-verifiable paper/report record. |
| `archivara2026directorbrief` | no | **Incorrect** | Local repository artifact only; no external web-verifiable paper/report record. |
| `archivara2026experimentspec` | yes | **Incorrect** | Local repository artifact only; no external web-verifiable paper/report record. |
| `cao2019bipolarinput` | yes | **Verified** | DOI resolves to the 2019 IEEE JSSC paper; title, year, venue, and authors are consistent. |
| `kuai2022dualpolarityjssc` | yes | **Verified** | DOI resolves to the 2022 IEEE JSSC paper; title, year, venue, and authors are consistent. |
| `alhawari2017polaritydetection` | yes | **Verified** | DOI resolves to the 2017 IEEE TCAS-I paper; title, year, venue, and authors are consistent. |
| `li2022multiinputplatform` | yes | **Verified** | DOI resolves to the 2022 ISSCC paper; title, year, venue, and authors are consistent. |

## Novelty Assessment

What is genuinely interesting here is narrow: the executed same-family ablation suggests that, in this specific helper-free weak-source model, explicit pre-handoff source ranking is not the ingredient that preserves the startup boundary. That is a useful negative result and a legitimate simplification insight. What is **not** genuinely novel is the broader framing as a new multi-source harvesting architecture, a new mixed-polarity interface concept, or a new autonomous startup platform. Those spaces are already populated by the cited prior-art families, and the repo's own novelty artifacts say as much. The CE evidence also does not establish a strong cross-domain creative contribution: the concept tree mostly remains boilerplate, all inspected `concept.json` files leave `experimental_result` as `null`, only `time_constant_ranked_arbiter` clearly survives into the experiment pack, and the decisive winner (`source_blind`) is an internal ablation rather than a bridge-chain concept. As a result, the novelty ceiling here is a bounded falsification/simplification paper, not a publishable new circuit architecture.

## Overall Verdict

**DEEPEN**

This would already be a mandatory **REVISE** on citation hygiene alone, but the deeper issue is that the contribution is only a 2/5 on novelty in its current form. Per the stated verdict rules, that makes the correct outcome **DEEPEN** rather than merely REVISE.

## What Is Lacking, And What Would Elevate It

To become genuinely novel in this domain, the next cycle needs more than paper cleanup. It needs a contribution that changes what an expert would learn about weak multi-source cold start.

1. **Produce a causally isolated new mechanism, not just a simplification of the current one.** At minimum, run the missing same-scaffold no-packet-gate control (`blind_packet_merge`) on the separator cases. Better yet, design a new helper-free startup mechanism that beats the blind packet gate on the hard mixed-polarity/collapse/leak cases rather than only proving that RC ranking was unnecessary.
2. **Show a surprising boundary, not just a tie plus a narrow ablation win.** A stronger paper would identify a counterintuitive regime shift or a new design law that does not already read as an obvious "simpler nearby variant works too" result.
3. **Turn CE into actual experimental novelty or drop it from the novelty story.** If CE is meant to matter, the bridge concepts need real experimental outcomes in their `concept.json` files and real execution in the artifact pack. Otherwise, the CE machinery is not evidence of creative research.
4. **Upgrade the benchmark to publication-grade causality.** Add the missing same-scaffold control, run at least one literature-faithful comparator, emit explicit `n_handoff` rise/fall/rise2 events rather than store-threshold proxies, document the back-drive threshold, and extend robustness to the actual separator cases (`fa_002`, `fa_006`, `fa_009`, `fa_010`).
5. **Repair the bibliography completely.** Remove local repo artifacts from `sources.bib` or clearly separate them from externally verifiable literature, fix `hernandez2013tegboost`, and replace every truncated `and others` author field with a correct full author list.
6. **Finish the figures for publication.** Correct the ablation energy statistic, make the back-drive reporting explicit, and regenerate the report-style seaborn panels into a more publication-finished figure set with consistent statistics and clearer emphasis on the real separator cases.

## Bottom Line

The paper is technically organized, mostly honest about the negative result, and backed by real simulation artifacts. But the current package does not clear the novelty bar for a top-tier venue, and the bibliography does not clear the citation-accuracy bar. The fastest path forward is to treat this as a deepening cycle aimed at either:

1. a stronger, causally isolated and genuinely new startup mechanism, or
2. a much more tightly scoped negative-result paper with fully repaired citations and benchmark controls.
