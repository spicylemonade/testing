# H1 Dependency Map

Champion root: `results/concept_evolve/tree/001_packet_scout_handoff_root`

All later H1 artifacts must link back to this folder, even when a result is summarized in repo-level notes or `results/verification/*`.

## Shared Subcircuits

- `netlists/shared/source_pair_models.inc`
  - Parameterized two-source Thevenin source models with ramp, polarity, and impedance controls.
- `netlists/shared/startup_cells.inc`
  - Common polarity-routing switch model and abstract startup-pump block reused by baselines, champion, and ablation decks.
- `netlists/shared/packet_scout_blocks.inc`
  - Shared packet-scout ranking core for the champion and the source-blind ablation.
- `netlists/shared/measurement_hooks.inc`
  - Common `.measure` blocks for startup success, time-to-handoff, back-drive loss, and startup-control energy.

## Source Model Contract

- Source family: two-source weak-energy Thevenin pair with parameterized open-circuit voltage, source resistance, polarity, and ramp rate.
- Planned top-level parameters:
  - `VOC_A`, `VOC_B`
  - `R_A`, `R_B`
  - `POL_B`
  - `RAMP_MVPS`
  - `C_STORE`
  - `V_HANDOFF`

## Control Blocks

- Scout pulse injector
- Probe sample capacitors
- Reverse-blocking startup OR path
- Packet store capacitor
- Handoff latch and gate
- Main arbiter enable

## Baseline And Research Folders

- Strong baseline A:
  - `netlists/baselines/fixed_startup_path/`
- Strong baseline B:
  - `netlists/baselines/nonaware_multi_input_startup/`
- Champion family:
  - `netlists/champion/packet_scout_handoff/`
- Required ablation family:
  - `netlists/ablations/source_blind_packet_gate/`

## Result Tables And Manifests

- Raw waveforms and numeric dumps:
  - `results/raw/`
- Case manifests and sweep definitions:
  - `results/manifests/`
- Comparison tables and regime summaries:
  - `tables/`

## Verification Outputs

- Lane-local experiment checks, benchmark notes, and overlap notes:
  - `verification/`
- Repo-level verification pack that must cross-link back here:
  - `results/verification/novelty_report.md`
  - `results/verification/benchmark_report.md`
  - `results/verification/citation_audit.md`
  - `results/verification/verification_summary.md`
