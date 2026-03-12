# Benchmark Report

Date: 2026-03-12
Review round: novelty_deepening_final
Scope: benchmark audit of the H1 `001_packet_scout_handoff_root` evidence pack after metric repair and the DEEPEN near-tie matrix
Status: PASS for a bounded internal frontier claim; BLOCK for literature-performance claims

## Executive Gate

- The benchmark now clears the core internal debt that blocked the earlier positive story:
  - same-scaffold no-packet control executed
  - explicit `n_handoff`-based timing repaired
  - near-tie late-arrival cases executed under equal accounting
- The benchmark still does not clear any measured claim against prior silicon because no literature-faithful executed comparator exists.

## Reviewed Artifacts

- `research_rubric.json`
- `results/research_context.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/startup_cells.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/blind_packet_merge/blind_packet_merge.cir`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_04_confidence_gated_abstention/confidence_gated_abstention.cir`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item028_metric_control_repair.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item029_confidence_variant.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item030_deepen_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_results.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/deepen_near_tie_manifest.json`
- `tools/run_h1_matrix.py`
- `tools/run_h1_falsifier.py`
- `tools/run_h1_robustness.py`
- `tools/run_h1_deepen.py`

## Findings

### 1. The handoff and control-energy contract is now materially repaired

- `startup_cells.inc` now latches `n_handoff` explicitly instead of relying on the earlier effectively-high switch proxy.
- `measurement_hooks.inc` reports:
  - `t_handoff`
  - `t_handoff_fall`
  - `t_handoff_rise2`
  from the repaired handoff node, while keeping store-threshold crossings only as diagnostics.
- `startup_ok` now requires both stored energy and observed handoff activity.
- Benchmark consequence:
  - the DEEPEN timing claims are no longer resting on the old store-voltage proxy alone

### 2. The same-scaffold no-packet control is now executed and informative

- `blind_packet_merge` is no longer a hypothetical control.
- On the four decisive control cases:
  - `blind_packet_merge` median `t_handoff = 4.67638 s`
  - `blind_packet_merge` median `e_backdrive = 1.54753e-09 J`
  - `confidence_gated` median `t_handoff = 4.85884 s`, `e_backdrive = 0`
  - `source_blind` median `t_handoff = 5.01093 s`, `e_backdrive = 0`
- Benchmark consequence:
  - the repo now has a measured speed-versus-backdrive frontier rather than a one-sided packet-gating claim

### 3. The DEEPEN matrix supports a bounded positive claim

- Static near ties:
  - `confidence_gated` and `source_blind` both succeed `6/6`
  - `confidence_gated` median gain versus `source_blind` is only `-0.000545 s`
  - commit count is `0/6`
- Late-arrival near ties:
  - `confidence_gated` and `source_blind` both succeed `6/6`
  - `confidence_gated` median gain versus `source_blind` is `+0.30882 s`
  - commit count is `6/6`
  - median `t_commit = 1.02799 s`
- Benchmark consequence:
  - the executed evidence supports one bounded statement:
    - confidence gating is useful only when ambiguity resolves temporally

### 4. `time_constant_ranked` prevents any best-overall claim

- `time_constant_ranked` remains faster than `confidence_gated` in both static and late families.
- The DEEPEN lane therefore does not produce a new universal winner.
- Benchmark consequence:
  - the final package is a tradeoff/frontier paper, not a champion benchmark paper

### 5. Remaining benchmark limits are real but narrower now

- No literature-faithful executed comparator exists.
- The DEEPEN matrix is intentionally small and focused:
  - `12` core cases
  - `4` decisive controls
- Robustness intervals were not rerun for every DEEPEN separator case.
- Historical notes such as `item018_benchmark_note.md` and `item019_falsifier_note.md` should be read as superseded by `item028_metric_control_repair.md` and `item030_deepen_matrix.md`.

## Claim Gate

- Supported now:
  - explicit handoff timing and pre-handoff accounting are repaired for the final lane
  - `blind_packet_merge` defines a measured speed/backdrive frontier
  - `confidence_gated` beats `source_blind` on late-arrival near ties without reopening backdrive
  - `confidence_gated` correctly abstains on static near ties

- Not supported:
  - any claim that `confidence_gated` is best overall
  - any measured superiority claim against recovered prior-art families
  - any general startup-envelope map for the field

## Required Next Actions If The Project Continues

1. Execute one literature-faithful comparator under the repaired hooks.
2. Add robustness intervals for the decisive DEEPEN late-arrival cases.
3. Translate the behavioral confidence node into a hardware-plausible implementation if the goal moves beyond mechanism discovery.

## Bottom Line

- The repo now has enough benchmark evidence to publish a bounded internal frontier:
  - merge is fastest but leaky
  - blind packet isolation is safe but slow on late arrival
  - confidence-gated abstention recovers part of the lost speed without reopening backdrive
- It still does not have enough benchmark evidence for measured claims against prior literature.
