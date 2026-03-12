# Research Context

- Date: `2026-03-12`
- Stage: `phase_5_h1_narrowed_finalization`
- Active lane: `H1_multisource_cold_start`
- Backup lane: `H2_cryo_support_blocks`
- Reserve lane: `H3_dynamic_source_impedance`
- Current lane verdict: `H1 narrowed, not promoted, not killed`

## One-Paragraph Restart Summary

The H1 lane implemented and benchmarked a helper-free packet-scout cold-start interface under weak two-source startup stress. The `24`-case primary startup matrix did **not** show a general correctness or back-drive advantage over the fixed or nonaware baselines: all three designs finished at `17/24` startup successes and zero primary-matrix back-drive separation. The `6`-case falsifier suite did expose a narrow surviving claim boundary in `fa_001` and `fa_005`, where the champion avoids some nonaware mixed-source failure modes under collapse and mixed-polarity stress. The lane therefore survives only as a narrowed adversarial-startup result. H2 and H3 remain unactivated.

## Start Here

1. Read `research_rubric.json` to confirm every item is closed.
2. Read `results/verification/final_research_brief.md`.
3. Read `results/verification/verification_summary.md`.
4. Read `results/concept_evolve/tree/001_packet_scout_handoff_root/README.md`.

## Canonical Artifact Map

### Literature And Novelty

- `sources.bib`
- `results/literature/prior_art_gap.md`
- `results/literature/prior_art_watchlist.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
- `results/verification/novelty_report.md`

### Champion Root

- `results/concept_evolve/tree/001_packet_scout_handoff_root`

### Netlists

- Champion:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Baselines:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/baselines/fixed_startup_path/fixed_startup_path.cir`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir`
- Shared source and measurement models:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`

### Results

- Startup manifests and run log:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/startup_matrix_manifest.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/startup_runlog.jsonl`
- Falsifier manifests and run log:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_runlog.jsonl`
- Primary tables:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`
- Falsifier and analysis tables:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_summary.json`
- Figures:
  - `figures/h1_startup_sensitivity.svg`
  - `figures/h1_falsifier_boundary.svg`

### Verification

- Lane-local verification:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md`
- Repo-level verification pack:
  - `results/verification/novelty_report.md`
  - `results/verification/benchmark_report.md`
  - `results/verification/citation_audit.md`
  - `results/verification/verification_summary.md`
  - `results/verification/final_research_brief.md`

## Minimal Regeneration Commands

- Rebuild startup summaries from existing raw files:
  - `python3 tools/run_h1_matrix.py summarize`
- Rebuild literature-mapped benchmark tables:
  - `python3 tools/run_h1_matrix.py benchmark`
- Rerun the falsifier suite:
  - `python3 tools/run_h1_falsifier.py run`
- Regenerate sensitivity tables and figures:
  - `python3 tools/analyze_h1_results.py`

## Final Claim Boundary

- Allowed:
  - helper-free pre-arbitration source awareness can avoid some nonaware mixed-source startup failures under collapse and mixed-polarity stress
- Blocked:
  - broad superiority over the fixed startup path
  - `first`, `novel`, or `best` language
  - steady-state efficiency claims
  - minimum-startup-voltage claims

## Open Kill Conditions

1. A stronger fixed-path or minimally corrected nonaware baseline reproduces `fa_001` and `fa_005` under equal accounting.
2. A direct-overlap paper is recovered that already demonstrates helper-free pre-arbitration mixed-source startup with the same stress boundary.
3. A materially stronger collapse or chatter model removes the `fa_001` and `fa_005` separation on rerun.
