# Benchmark Report

Date: 2026-03-12
Scope: audit the executed H1 evidence pack after the same-family ablations, metric-contract repair, expanded falsifier suite, and robustness reruns
Status: PASS for a falsification and simplification paper; BLOCK for any claim that RC-ranked source awareness is the winning architecture

## Bottom Line

- The executed benchmark is now strong enough to support a publication-quality boundary result.
- The primary startup matrix remains a null on startup-envelope advantage:
  - all five designs start in `17/24` cases
  - all five designs report `0` pre-handoff back-drive in the primary matrix
- The original mechanism claim is falsified by the executed same-family ablation:
  - `source_blind` matches the champion on all `24/24` startup-matrix outcomes
  - `source_blind` improves falsifier startup from `8/10` to `10/10`
  - the deterministic gaps versus the champion are `fa_002` and `fa_006`, both won by `source_blind`
- A lower-overhead source-aware control still survives as a useful engineering point:
  - `time_constant_ranked` preserves `17/24` startup-matrix success and reaches `9/10` falsifier successes
  - its median successful-case pre-handoff control energy is `1.11852e-13 J` versus `2.37717e-13 J` for the RC-ranked champion, a `52.9%` reduction
- The expanded falsifier suite now contains real chatter, unequal-`VOC`, and leak-path stress, and the robustness study adds confidence intervals on the remaining boundary cases.

## Reviewed Artifacts

- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/tool_plan.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/dependency_map.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/startup_matrix_manifest.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_summary.json`
- `figures/h1_primary_matrix_heatmap.pdf`
- `figures/h1_falsifier_boundary.pdf`
- `figures/h1_metric_accounting.pdf`
- `figures/h1_ablation_tradeoff.pdf`
- `figures/h1_robustness_ci.pdf`
- `tools/run_h1_matrix.py`
- `tools/run_h1_falsifier.py`
- `tools/run_h1_robustness.py`
- `tools/analyze_h1_results.py`

## Findings

### 1. The primary startup matrix is a five-way tie

- `champion`, `fixed`, `nonaware`, `source_blind`, and `time_constant_ranked` each start in `17/24` cases.
- Grouped counts by polarity, impedance ratio, and ramp rate are identical across all five designs.
- The primary matrix therefore cannot support any claim of a broader startup-envelope win for explicit source ranking.

### 2. The executed ablation falsifies explicit source ranking as the causal mechanism

- The previously missing `source_blind_packet_gate` ablation has now been executed on the full startup matrix and the expanded falsifier suite.
- On the startup matrix, `source_blind` matches the RC-ranked champion exactly on startup success.
- On the falsifier suite, `source_blind` is the strongest design in the pack:
  - `source_blind`: `10/10`
  - `time_constant_ranked`: `9/10`
  - `champion`: `8/10`
  - `fixed`: `7/10`
  - `nonaware`: `5/10`
- Because the packet-gated isolation topology is shared between `champion`, `source_blind`, and `time_constant_ranked`, while only the selector law changes, the new evidence rules out a narrative where explicit RC-based branch ranking is the load-bearing reason for robustness.

### 3. The lower-overhead time-constant control is the strongest positive design point that remains

- The new `time_constant_ranked` arbiter preserves the startup-matrix boundary and reaches `9/10` falsifier successes.
- Its successful-case pre-handoff control-energy median is `1.11852e-13 J`, compared with `2.37717e-13 J` for the RC-ranked champion.
- The measured reduction is close to the conductance-ratio prediction implied by the netlists, which makes the energy result mechanistically interpretable rather than anecdotal.

### 4. The falsifier package now measures the stresses it claims to measure

- The suite has expanded from `6` to `10` cases.
- It now contains:
  - source-collapse cases in same and mixed polarity
  - a real UVLO chatter case with measured `fall` and `rise2` events (`fa_004`)
  - unequal-`VOC` cases (`fa_007`, `fa_008`)
  - finite off-isolation leak-path cases (`fa_009`, `fa_010`)
- `source_blind` is the only design with `0` measured `fall` and `0` measured `rise2` events across the full falsifier suite.

### 5. Robustness evidence now exists for the surviving claim boundary

- The robustness runner executed `24` random samples per design-case over `fa_001`, `fa_004`, `fa_005`, and `sm_015`.
- The strongest load-bearing outcomes are:
  - `fa_001`: `fixed` is `0.000` (`0/24`), `nonaware` is `0.875` (`21/24`), while `champion`, `source_blind`, and `time_constant_ranked` are all `1.000` (`24/24`)
  - `fa_005`: `nonaware` is `0.000` (`0/24`), while the other four designs are all `1.000` (`24/24`)
  - `fa_004` and `sm_015`: all five designs are `1.000` (`24/24`)
- These runs do not make the primary matrix causal, but they do upgrade the adversarial boundary from a single deterministic anecdote to a small uncertainty-qualified result.

### 6. Remaining limits are now limitations, not blockers

- The primary startup matrix is still aliased rather than factorially crossed.
- There is still no literature-faithful executed comparator; literature comparison should remain structural rather than measured.
- Robustness coverage is focused on four load-bearing cases rather than the full manifest.
- None of these limits blocks the narrower falsification paper, but all of them block any attempt to restate the result as a broad architecture win.

## Evidence Boundary

- Supported now:
  - the primary startup matrix is a null on startup-count advantage
  - packet-gated isolation matters against the `nonaware` join topology in adversarial cases
  - explicit RC-style source ranking is not required for the surviving boundary and is empirically dominated by `source_blind`
  - `time_constant_ranked` preserves most of the adversarial benefit with materially lower pre-handoff control energy than the RC-ranked champion

- Not supported now:
  - broad superiority over the fixed startup path
  - measured superiority over the closest literature families
  - causal sensitivity claims from the aliased 24-case matrix
  - any statement that the RC-ranked selector is itself the winning new architecture

## Publication Gate

- Write the paper as a helper-free falsification and simplification study.
- Do not write it as a source-aware champion paper.
- Treat the strongest final claim as:
  - minimal packet gating preserves the adversarial startup boundary, while explicit pre-handoff ranking is unnecessary and can be harmful under expanded stress.
