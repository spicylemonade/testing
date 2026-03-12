# H1 Champion Root: packet_scout_handoff_root

This folder is the canonical restart point for the `H1_multisource_cold_start` lane.

- Current status:
  - `narrowed result`
- Current verdict:
  - not promoted
  - not killed
  - reportable only as a helper-free adversarial-startup result against some nonaware mixed-source failure modes

## Netlists

- Champion:
  - [netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir](netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir)
- Baselines:
  - [netlists/baselines/fixed_startup_path/fixed_startup_path.cir](netlists/baselines/fixed_startup_path/fixed_startup_path.cir)
  - [netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir](netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir)
- Shared blocks:
  - [netlists/shared/source_pair_models.inc](netlists/shared/source_pair_models.inc)
  - [netlists/shared/measurement_hooks.inc](netlists/shared/measurement_hooks.inc)
  - [netlists/shared/packet_scout_blocks.inc](netlists/shared/packet_scout_blocks.inc)

## Manifests And Results

- Dependency map:
  - [dependency_map.md](dependency_map.md)
- Experiment specification:
  - [experiment_spec.md](experiment_spec.md)
- Startup manifest and run log:
  - [results/manifests/startup_matrix_manifest.json](results/manifests/startup_matrix_manifest.json)
  - [results/manifests/startup_runlog.jsonl](results/manifests/startup_runlog.jsonl)
- Falsifier manifest and run log:
  - [results/manifests/falsifier_cases.json](results/manifests/falsifier_cases.json)
  - [results/manifests/falsifier_runlog.jsonl](results/manifests/falsifier_runlog.jsonl)
- Primary tables:
  - [tables/startup_summary.json](tables/startup_summary.json)
  - [tables/benchmark_summary.json](tables/benchmark_summary.json)
- Falsifier and analysis tables:
  - [tables/falsifier_summary.json](tables/falsifier_summary.json)
  - [tables/analysis_summary.json](tables/analysis_summary.json)
- Local indexes:
  - [netlists/README.md](netlists/README.md)
  - [results/README.md](results/README.md)
  - [tables/README.md](tables/README.md)
  - [verification/README.md](verification/README.md)

## Verification Reports

- Lane-local:
  - [verification/claim_matrix.md](verification/claim_matrix.md)
  - [verification/item021_decision_memo.md](verification/item021_decision_memo.md)
  - [verification/item022_analysis_package.md](verification/item022_analysis_package.md)
- Repo-level:
  - [../../../verification/novelty_report.md](../../../verification/novelty_report.md)
  - [../../../verification/benchmark_report.md](../../../verification/benchmark_report.md)
  - [../../../verification/citation_audit.md](../../../verification/citation_audit.md)
  - [../../../verification/verification_summary.md](../../../verification/verification_summary.md)
  - [../../../verification/final_research_brief.md](../../../verification/final_research_brief.md)

## Allowed Claim

- helper-free pre-arbitration source awareness can avoid some nonaware mixed-source startup failures under collapse and mixed-polarity stress

## Blocked Claim Families

- broad superiority over the fixed startup path
- `first`, `novel`, or `best` wording
- steady-state efficiency improvement
- minimum-startup-voltage superiority

## Unresolved Blockers

1. A stronger fixed-path or minimally corrected nonaware baseline may still erase the surviving `fa_001` and `fa_005` boundary.
2. A closer direct-overlap paper may still collapse the narrowed novelty margin.
3. Improved collapse or chatter modeling may still remove the current adversarial separation.

## Regeneration Commands

- `python3 tools/run_h1_matrix.py summarize`
- `python3 tools/run_h1_matrix.py benchmark`
- `python3 tools/run_h1_falsifier.py run`
- `python3 tools/analyze_h1_results.py`
