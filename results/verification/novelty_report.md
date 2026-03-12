# Novelty Report

Date: 2026-03-12
Phase: novelty_deepening_final
Scope: closest-prior-art screen for the final H1 artifact pack after the DEEPEN lane execution
Status: PASS for a bounded operating-regime contribution; not materially distinct as a broad architecture-novelty paper

## Reviewed Material

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/literature/semantic_scholar_manifest.json`
- `results/verification/final_research_brief.md`
- `results/verification/verification_summary.md`
- `results/verification/benchmark_report.md`
- `results/verification/citation_audit.md`
- `sources.bib`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item028_metric_control_repair.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item029_confidence_variant.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item030_deepen_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_results.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`

## Executive Assessment

- The package is still not meaningfully new as another weak-source startup circuit, another adaptive dual-source tracker, or another autonomous multi-input PMU.
- The targeted overlap pass tightened the closest external anchors to:
  - `liu2018`
  - `liu2024`
  - `liu2024distributedpmu`
- Those anchors already occupy adaptive source tracking, multi-input autonomy, and all-rail cold-start framing.
- The surviving novelty is narrower and more interesting:
  - inside the executed helper-free packet-gated startup family, the correct response to static near ties is abstention, while temporally resolving ambiguity should trigger a later commitment
- That is materially different from broad adaptive tracking because it is a measured abstain-to-commit rule, not continuous source optimization.

## Closest Overlap Families That Still Bound The Paper

### 1. Weak-source and polarity-aware startup papers

- Closest papers:
  - `goppert2016startup70mv`
  - `das2017selfstarter`
  - `quintero2019cmosstartup`
  - `coustans2019coldstart60mv`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `alhawari2017polaritydetection`
- Novelty consequence:
  - the paper cannot claim novelty on cold-start difficulty, low-voltage startup, or mixed-polarity handling by themselves

### 2. Adaptive source-tracking startup papers

- Closest papers:
  - `tang2018dualsource`
  - `liu2018`
- What they already cover:
  - explicit adaptive source selection
  - source-tracking control during energy-harvesting operation
- Novelty consequence:
  - the paper is not distinct as another source-aware ranking controller
  - it survives only if the claim is about abstaining from ranking until separability is real

### 3. Autonomous multi-input PMU papers

- Closest papers:
  - `li2022multiinputplatform`
  - `liu2024`
  - `liu2024distributedpmu`
  - `chen2024collaborative`
  - `weng2024osece`
- What they already cover:
  - autonomous multi-input harvesting
  - cold-start-capable multi-input PMUs
  - adaptive conversion and distributed energy sharing
- Novelty consequence:
  - the paper is not distinct as another multi-input platform or autonomous PMU
  - it survives only as a same-family startup-control insight under one narrow contract

## Material Differentiation That Survives

### 1. The result is about temporal separability, not better ranking

- On static near ties, `confidence_gated` commits `0/6` and effectively becomes `source_blind`.
- On late-arrival near ties, `confidence_gated` commits `6/6` and improves median `t_handoff` over `source_blind` by `0.30882 s`.
- This is the core design law supported by the executed matrix:
  - do not rank unresolved ambiguity
  - do commit when ambiguity resolves over time

### 2. The no-packet control makes the tradeoff scientifically useful

- `blind_packet_merge` is faster on decisive controls but produces measurable wrong-way energy.
- `confidence_gated` recovers part of that speed advantage without reopening backdrive.
- This creates a real three-way frontier:
  - fastest but leaky merge
  - slow safe blind isolation
  - intermediate abstain-to-commit isolation

### 3. The claim is materially different from the closest adaptive tracking anchors

- Relative to `liu2018`:
  - this package is not continuous cycle-by-cycle source tracking or adaptive peak-current control
  - it is a pre-handoff commitment rule that explicitly chooses not to infer a winner under static ambiguity
- Relative to `liu2024` and `liu2024distributedpmu`:
  - this package is not a general triple-input or distributed PMU platform
  - it is a two-source same-scaffold startup controller with a bounded operating-regime result

## Claims That Do Not Survive

- `first` or `best` language
- any `general multi-input PMU` framing
- any claim that `confidence_gated` beats `time_constant_ranked`
- any claim that the literature broadly lacks such comparisons
- any broad architecture claim built on mixed polarity, low-voltage startup, or helper-free operation alone

## Residual Gaps

- The targeted overlap pass did not recover a close same-family abstention-like controller, but that is still a scoped retrieval result, not a field-wide absence proof.
- No literature-faithful executed comparator exists yet.
- The DEEPEN matrix is intentionally bounded to near-tie and late-arrival regimes, so the contribution is not a universal startup-envelope map.

## Final Verdict

- The manuscript has a real contribution, but the contribution is narrow by design.
- The materially distinct part is:
  - in the executed helper-free packet-gated startup family, abstain on static near ties and commit only when temporal separability appears
- That is worth reporting as a bounded operating-regime result.
- It should not be framed more broadly than that.
