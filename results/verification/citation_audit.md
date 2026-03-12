# Citation Audit

Date: 2026-03-12
Phase: post_deepen
Scope: evidence traceability and citation support for `research_paper.tex`
Verdict: REVISE (targeted). The empirical claim spine is supported, but several literature-boundary sentences still overreach their citation support.

## Inputs Reviewed

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`
- `results/literature/prior_art_gap.md`
- `results/verification/novelty_report.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_results.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`

## What Clears

- All in-manuscript citation keys resolve.
  - `research_paper.tex` uses 18 unique citation keys.
  - All 18 keys are present in `sources.bib`.
  - No broken `\cite...{}` commands were found.
- The headline quantitative claims are traceable to generated result artifacts.
  - The five-way `17/24` startup tie and the context medians in the abstract, introduction, results, and conclusion are supported by `tables/startup_summary.json`.
  - The `9/10`, `8/10`, `7/10`, `5/10`, `5/10` falsifier frontier and the named separator failures (`fa_001`, `fa_005`, `fa_006`, `fa_009`, `fa_010`) are supported by `tables/falsifier_summary.json` and `tables/falsifier_results.csv`.
  - The DEEPEN near-tie claims, including `0/6` commits on static cases, `6/6` commits on late-arrival cases, `0.30882 s` median gain over `source_blind`, and the `time_constant_ranked` non-superiority guardrail, are supported by `tables/deepen_summary.json`.
  - The robustness statements about `fa_001` and `fa_005` are supported by `tables/robustness_summary.json`.
- The scoped novelty sentence is supportable if it stays scoped.
  - The sentence `the recovered overlap set did not reveal a close same-family abstention-like pre-handoff controller` is defensible as a retrieval-scoped claim because `results/literature/semantic_scholar_manifest.json`, `results/literature/prior_art_gap.md`, and `results/verification/novelty_report.md` all frame it that way.
  - It is not supportable as a field-wide absence claim.
- No obvious citation hallucinations were found in the cited bibliography.
  - The newer 2024-2025 overlap anchors appear internally consistent across `sources.bib`, the manifest, and spot checks of titles/venues.

## Findings

### 1. High: `research_paper.tex:80` makes two different claims, and only one is currently supported

- Supported part:
  - `tang2018dualsource`, `liu2018`, and `li2022multiinputplatform` do support the general idea that some designs push more source intelligence before or during startup.
- Unsupported or weakly supported part:
  - The sentence currently says that dual-source tracking, polarity detection, and autonomous multi-input routing all embody the same intuition: `identify the stronger source early and then favor it aggressively`.
  - That overstates what the polarity papers support. `alhawari2017polaritydetection`, `cao2019bipolarinput`, and `kuai2022dualpolarityjssc` are good support for polarity handling and startup conditioning, but they are not clean support for stronger-source ranking.
- Missing-support clause in the same paragraph:
  - `Many papers compare a new source-aware controller against a weak open-loop baseline, a different topology, or a fully integrated platform with several changes at once. It is rarer to execute the same-family "do less" alternative...`
  - No source in the current bibliography directly supports that field-level benchmarking/rarity claim.
- Required fix:
  - Split the sentence into separate literature buckets.
  - Narrow the ranking claim to the actual tracking papers.
  - Either delete the `It is rarer...` sentence or scope it explicitly to the recovered overlap set unless a review or mini-survey citation is added.

### 2. High: `research_paper.tex:110` and Table row `research_paper.tex:128` over-compress heterogeneous prior art

- The current PMU-overlap bucket mixes at least three different families:
  - battery-less or self-powered multi-source interface circuits,
  - self-powered piezoelectric multi-input front ends,
  - autonomous multi-input PMU or distributed-PMU platforms.
- The grouped citation list is real prior art, but the prose overstates what the family establishes in one breath:
  - `routing, energy sharing, cold startup, and distributed power management at system scale`
  - `Autonomous multi-input PMUs`
- The problem is not that the sources are fake; the problem is that the grouping makes the overlap look more homogeneous and more directly comparable than it is.
- Required fix:
  - Split the prose and the prior-work table row into at least two buckets:
    - self-powered or multi-source interface circuits: `alghisi2017batteryless`, `wang2023serialstack`, `chen2024collaborative`, `weng2024osece`
    - autonomous multi-input PMU platforms: `li2022multiinputplatform`, `liu2024`, `liu2024distributedpmu`, `gogolou2025multisourcereview`
  - Keep the claim at `broader PMU/platform overlap`, not `close controller-level comparator`.

### 3. Medium: `research_paper.tex:78` uses mixed source types to support one sentence, but the citation placement is loose

- The sentence starts with a multi-harvester motivation:
  - `Batteryless sensor nodes increasingly aggregate several harvesters because no single transducer is reliable across every environmental state.`
- The attached citation bundle includes two single-source thermoelectric startup papers plus one multi-source review.
- This is not a broken citation, but the support is uneven:
  - the multi-source integration trend is supported by `gogolou2025multisourcereview`,
  - the weak-startup difficulty is supported by `goppert2016startup70mv` and `das2017selfstarter`.
- Required fix:
  - Either split the sentence so the multi-source motivation cites multi-source literature and the weak-startup claim cites startup papers, or add one stronger multi-input review directly at this location.

### 4. Medium: `research_paper.tex:105` uses a superlative that is only justified later, not locally

- `The closest direct overlap for any source-aware startup story is the adaptive dual-source line.` is stronger than what the immediate citations prove by themselves.
- `tang2018dualsource` and `liu2018` do support adaptive startup/source-tracking overlap.
- They do not, by themselves, prove `closest direct overlap` across the whole literature.
- The manuscript later repairs this by using the retrieval-scoped qualifier at `research_paper.tex:1096`, but that qualifier arrives too late.
- Required fix:
  - Move the retrieval scope forward:
    - e.g. `Within the recovered overlap set, the closest direct adaptive-startup overlap is the dual-source line.`

### 5. Medium: provenance metadata is stale in `results/research_context.md`

- `results/research_context.md:10` says `sources.bib entries: 28`.
- The current `sources.bib` contains 18 entries.
- This does not break the manuscript's citations, but it does weaken traceability because the context file is now out of sync with the actual bibliography used by the paper.
- Required fix:
  - Update the context metadata or regenerate the file so the bibliography count matches the current artifact.

### 6. Low: two optional citation-hygiene gaps remain

- `research_paper.tex:856` names `Wilson 95% intervals` without a methods citation.
  - This is standard enough that it does not block the paper, but a citation would improve methods hygiene.
- `research_paper.tex:908` makes a broad sociological claim:
  - `Circuit papers often reward only positive stories...`
  - This is not load-bearing for the technical contribution and can be deleted if no source is added.

## Most Important Sources To Add

### 1. Highest priority

- Estrada-Lopez, Abuellil, Zeng, Sanchez-Sinencio, `Multiple Input Energy Harvesting Systems for Autonomous IoT End-Nodes` (2018).
- Why it matters:
  - it is the best concrete addition for the multi-input motivation at `research_paper.tex:78`
  - it also supports the narrower methodological point that cross-paper comparison is hard because works differ in transducers, technologies, and operating assumptions
- Best use:
  - add near `research_paper.tex:78`
  - optionally use it to soften and partially support the benchmarking sentence at `research_paper.tex:80`

### 2. High priority

- Shi, Cai, Jiang, `Key Role of Cold-Start Circuits in Low-Power Energy Harvesting Systems: A Research Review` (2024).
- Why it matters:
  - it strengthens `research_paper.tex:100` so `mature design domain` rests on a review rather than only four primary papers
  - it also gives cleaner survey support for general cold-start framing in the introduction

### 3. High priority if the PMU/interface bucket stays broad

- Al Ghazi et al., `Advances in Interface Circuits for Self-Powered Piezoelectric Energy Harvesting Systems: A Comprehensive Review` (2025).
- Why it matters:
  - it gives review-level support for the piezoelectric self-powered interface family currently represented only by primary papers
  - it helps separate `self-powered interface overlap` from `autonomous PMU platform overlap`

### 4. Optional hygiene source

- Wilson, `Probable Inference, the Law of Succession, and Statistical Inference` (1927), or a modern equivalent methods reference for Wilson score intervals.
- Why it matters:
  - only for the named `Wilson 95% intervals` method callout

## Bottom Line

- The measured result does not have a citation-support problem.
- The remaining citation risk is concentrated in the introduction and related-work framing:
  - one unsupported benchmarking/rarity claim,
  - one miscitation-by-aggregation at `research_paper.tex:80`,
  - one over-compressed PMU/interface overlap bucket at `research_paper.tex:110` and `research_paper.tex:128`.
- If those sentences are split or narrowed, and the stale bibliography count in `results/research_context.md` is corrected, the manuscript should clear a citation audit for its bounded final claim.
