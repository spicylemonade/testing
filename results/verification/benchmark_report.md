# Benchmark Report

Date: 2026-03-12
Review round: review_round_1
Scope: benchmark audit of the H1 `001_packet_scout_handoff_root` evidence pack, limited to baselines, controls, ablations, error analysis, and stress coverage
Status: BLOCK for publication-quality benchmark claims; PASS only as an internal falsification package

## Executive Gate

- The current package is strong enough to reject the original RC-ranked champion story.
- It is not yet strong enough to publish a benchmark-centered positive claim about packet-gated isolation or superiority to prior work.
- The blocking gaps are concrete:
  - no executed same-scaffold no-packet-gate control
  - no literature-faithful executed comparator
  - handoff/chatter metrics still use a store-voltage proxy rather than a validated `n_handoff` event
  - decisive separator cases are not covered by robustness reruns
  - back-drive reporting uses an undocumented threshold that hides raw nonzero values

## Reviewed Artifacts

- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/startup_matrix_manifest.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_comparison.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_pairwise.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_results.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_sensitivity.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item011_signoff.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/blind_packet_merge/blind_packet_merge.cir`
- `tools/run_h1_matrix.py`
- `tools/run_h1_falsifier.py`

## Findings

### 1. Baselines are adequate for internal screening, but not for publication-grade comparison

- The executed design set is `champion`, `fixed`, `nonaware`, `source_blind`, and `time_constant_ranked`.
- That is enough to reject weak internal comparisons such as open-loop-only or fixed-threshold-only baselines.
- It is not enough to support any claim against the closest literature families:
  - `benchmark_comparison.csv` maps regimes to prior work, but no recovered literature-family comparator is executed under the shared hooks.
  - Any statement beyond within-repo ranking remains structural, not measured.
- Publication consequence:
  - block any claim of superiority over recent multi-input, dual-polarity, or batteryless startup interfaces.

### 2. Same-family ablations are present, but the key positive control is still missing

- The executed same-family ablations are useful and load-bearing:
  - `source_blind` removes ranking while keeping the packet scaffold
  - `time_constant_ranked` keeps source awareness with lower overhead
- Those runs are sufficient to falsify the original RC-ranking mechanism claim:
  - primary matrix: all five designs tie at `17/24`
  - falsifier suite: `source_blind = 10/10`, `time_constant_ranked = 9/10`, `champion = 8/10`
- The remaining positive story in the repo is now "packet-gated isolation matters."
- That positive story is not isolated by an executed same-scaffold control:
  - `blind_packet_merge.cir` exists, but it is absent from the startup and falsifier manifests and from all summary tables.
  - The current packet-gating claim therefore depends on comparisons to `nonaware`, which changes more than one mechanism at once.
- Publication consequence:
  - block any causal claim that packet gating itself is the surviving mechanism until a no-packet-gate same-scaffold control is executed.

### 3. The metric contract is still not aligned tightly enough for handoff or chatter claims

- `experiment_spec.md` defines `startup_ok` and `t_handoff` using both `V(n_store)` and `V(n_handoff)`.
- `measurement_hooks.inc` measures:
  - `t_handoff` when `V(n_store)` crosses `V_HANDOFF`
  - `t_handoff_fall` when `V(n_store)` falls through `V_HANDOFF_FALL`
  - `t_handoff_rise2` when `V(n_store)` crosses `V_HANDOFF` a second time
- `n_handoff` is used only to stop pre-handoff integration, not to define the reported event times.
- That means the decisive chatter and handoff metrics are still proxy measurements unless the repo shows that `V(n_store)` and `V(n_handoff)` transitions coincide for every design.
- There is also a reporting lag:
  - `item018_benchmark_note.md` still reports the pre-repair three-design benchmark and the older full-window control-energy numbers.
  - `item019_falsifier_note.md` still describes the earlier six-case suite with "none" for fall/rise2 events.
- Publication consequence:
  - block any benchmark claim about handoff correctness or UVLO chatter until actual `n_handoff` event traces are reported and the stale benchmark/falsifier notes are synchronized.

### 4. Back-drive evidence is numerically ambiguous and thresholded without justification

- `falsifier_summary.json` reports `nonzero_backdrive_cases = 0` for every design.
- `falsifier_results.csv` still contains positive pre-handoff `e_backdrive_j` values for `nonaware` in multiple cases, including `fa_001`, `fa_004`, `fa_005`, `fa_006`, `fa_007`, and `fa_008`.
- `tools/run_h1_falsifier.py` counts a case as nonzero only when `e_backdrive_j > 1e-12`.
- That threshold is not documented in the experiment spec, the table README, or the benchmark notes.
- The result is a benchmark ambiguity:
  - the raw table says "some wrong-way energy exists"
  - the summary says "zero nonzero cases"
- Publication consequence:
  - block any strong back-drive narrative until the report states the simulator noise floor and publishes both raw and thresholded counts.

### 5. Stress coverage improved materially, but the decisive claims are still supported by too few uncertainty-qualified cases

- The falsifier suite now spans `10` attack classes, which is materially better than the earlier six-case pack.
- The robustness runner adds `24` samples per design-case, but only for:
  - `fa_001`
  - `fa_004`
  - `fa_005`
  - `sm_015`
- The decisive cases are missing from robustness:
  - the champion losses to `source_blind` are `fa_002` and `fa_006`
  - the leak-path boundary used in the current narrowed story is `fa_009` and `fa_010`
- Those claims are therefore still deterministic one-off results, not uncertainty-qualified effects.
- The primary matrix is also a coverage screen, not a causal sensitivity study:
  - executed cases: `24`
  - full cross-product implied by the frozen factor levels: `4 voltages x 4 ramps x 3 ratios x 2 polarities = 96`
  - current grouped summaries cannot isolate interaction effects well enough for a publication-quality sensitivity claim
- Publication consequence:
  - block any strong claim that explicit ranking is harmful, or that packet gating survives leak-path stress, until the separator cases receive the same robustness treatment as `fa_001` and `fa_005`.

### 6. Error analysis is still too thin for a paper benchmark section

- The primary matrix leaves `7` failed cases per design, but there is no case-level failure taxonomy across the full table.
- The current artifacts do not separate:
  - no-start due to shared source scarcity
  - wrong-branch startup
  - collapse-after-latch
  - leak-dominated failure
  - proxy-measurement artifacts
- Without that taxonomy, the observed five-way tie in the main matrix could still be dominated by shared model limits rather than by a proven mechanism equivalence.
- Publication consequence:
  - block any causal explanation of the primary-matrix null until the failed cases are explicitly classified and linked to waveform evidence.

## Claim Gate

- Supported now:
  - the current benchmark falsifies the original RC-ranked champion claim inside this repo
  - `source_blind` and `time_constant_ranked` are stronger benchmark lines than the original champion
  - the present evidence package is useful for internal simplification decisions

- Not yet publication-quality:
  - packet-gated isolation as a causally isolated positive mechanism
  - any superiority claim over the closest literature families
  - any benchmark claim that depends on back-drive separation
  - any handoff/chatter claim that depends on the current store-threshold proxy
  - any sensitivity statement that depends on the aliased 24-case matrix

## Required Next Actions

1. Execute `blind_packet_merge` under the shared measurement hooks on at least `fa_001`, `fa_002`, `fa_005`, `fa_006`, `fa_009`, `fa_010`, plus matched primary-matrix cases.
2. Add one literature-faithful comparator from the recovered overlap set and run it on the same load-bearing cases before making any prior-art performance claim.
3. Emit explicit `n_handoff` rise, fall, and second-rise measurements, then rerun the decisive falsifier cases to verify that the current store-voltage proxy does not change the conclusions.
4. Reissue the back-drive summaries with a documented noise floor and publish both raw and thresholded counts side by side.
5. Extend robustness sampling to `fa_002`, `fa_006`, `fa_009`, and `fa_010`; if the current winners persist with confidence intervals, the narrowed mechanism story becomes materially stronger.
6. Add a case-level failure taxonomy for all failed startup-matrix rows and the decisive falsifier losses, with one waveform-backed reason code per failure.

## Bottom Line

- The repo has enough benchmark evidence to kill the original champion story.
- It does not yet have enough benchmark evidence to publish the surviving positive story without another control pass.
- The fastest route to a defensible paper benchmark is not a broader sweep; it is a tighter control package around packet-gating causality, handoff metric validity, and robustness on the already-identified separator cases.
