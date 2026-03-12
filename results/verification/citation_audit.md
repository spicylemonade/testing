# Citation Audit

Date: 2026-03-12
Scope: audit claim support and literature traceability for the narrowed H1 manuscript after bibliography repair and the post-ablation reruns
Status: PASS for the falsification/simplification manuscript; BLOCK for broad novelty or literature-superiority wording

## Audit Basis

- `sources.bib`
- `results/literature/prior_art_gap.md`
- `results/swarm/hypotheses.json`
- `results/swarm/gap_map.md`
- `results/verification/benchmark_report.md`
- `results/verification/novelty_report.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`

## Supported Claim Set

| ID | Claim | Verdict | Evidence |
| --- | --- | --- | --- |
| S01 | The primary 24-case startup matrix is tied at `17/24` startup successes for all five executed designs. | PASS | `tables/startup_summary.json` |
| S02 | The expanded falsifier suite contains `10` cases and ranks the designs `source_blind 10/10`, `time_constant_ranked 9/10`, `champion 8/10`, `fixed 7/10`, `nonaware 5/10`. | PASS | `tables/falsifier_summary.json`; `tables/ablation_summary.json` |
| S03 | The blind packet-gate ablation falsifies the claim that explicit source awareness is the causal mechanism in the current model family. | PASS | `tables/startup_summary.json`; `tables/falsifier_summary.json`; `netlists/shared/packet_scout_blocks.inc` |
| S04 | The time-constant-ranked arbiter preserves the primary startup count and reduces median successful-case pre-handoff control energy relative to the original RC-ranked champion. | PASS | `tables/startup_summary.json`; `tables/ablation_summary.json`; `netlists/shared/packet_scout_blocks.inc` |
| S05 | The repaired measurement contract distinguishes pre-handoff control energy from full-window control energy, and the difference is large enough to alter the old narrative. | PASS | `netlists/shared/measurement_hooks.inc`; `tables/startup_summary.json`; `figures/h1_metric_accounting.pdf` |
| S06 | `fa_004` now produces actual handoff fall and second-rise events for every design except `source_blind`. | PASS | `tables/falsifier_summary.json`; `tables/falsifier_results.csv` |
| S07 | The robustness study confirms that the surviving adversarial distinctions are not one-shot deterministic artifacts. | PASS | `tables/robustness_summary.json`; `figures/h1_robustness_ci.pdf` |
| S08 | The literature-overlap screen now rests on real recovered citations rather than unresolved placeholder titles. | PASS | `sources.bib`; `results/swarm/hypotheses.json`; `results/swarm/gap_map.md` |

## Findings

### 1. The placeholder-title problem is fixed for the active manuscript path

- The swarm-era unresolved anchors have been removed from the active citation spine and replaced with recovered papers:
  - `tang2018dualsource`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `alhawari2016multisourcepmu`
  - `alghisi2017batteryless`
  - `wang2023serialstack`
  - `chen2024collaborative`
  - `weng2024osece`
  - `li2022multiinputplatform`
  - `gogolou2025multisourcereview`
- Audit consequence:
  - the manuscript can now make an overlap argument without relying on hallucinated titles

### 2. The bibliography is manuscript-usable, with one quarantined record

- `sources.bib` now contains the required overlap papers and DOI repairs for the actively cited multi-input interface family.
- `hernandez2013tegboost` remains metadata-suspicious, but it is now explicitly annotated as unresolved and can simply remain uncited.

### 3. Literature comparison is structural, not reproduced benchmark comparison

- The repository can support statements like:
  - "the current evidence does not justify claiming superiority over recent dual-source, bipolar-input, or multi-input interface papers"
- The repository cannot support statements like:
  - "the blind packet gate outperforms Tang 2018" or
  - "the time-constant ranker beats Chen 2024 on efficiency"
- Audit consequence:
  - the manuscript must keep literature comparison qualitative and mechanism-focused

## Allowed Wording

- Allowed:
  - `falsifies`
  - `simplifies`
  - `narrows`
  - `within the tested model`
  - `the repository evidence does not justify`
- Blocked:
  - `first`
  - `novel`
  - `best`
  - `state of the art`
  - any direct paper-to-paper performance superiority claim

## Clearance

- CLEAR for a manuscript that says:
  - the broad source-aware architecture story failed
  - blind packetized isolation outperformed explicit source ranking in the executed adversarial suite
  - a lower-overhead time-constant ranker recovered most of the benefit within the source-aware family
- BLOCK for a manuscript that says:
  - the RC-ranked design is the winning architecture
  - the repository proved literature-wide superiority
  - no close prior art exists
