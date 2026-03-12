# Final Research Brief

Date: 2026-03-12
Scope: final validated H1 brief after novelty, benchmark, citation, and run-governance review
Status: PASS for a narrowed result only

## Writer (`writer`)

- Question:
  - can a helper-free multi-source harvester cold-start more safely when source selection happens before normal arbitration is alive
- Closest prior-work family:
  - integrated weak-source startup papers such as `goppert2016startup70mv`, `quintero2019cmosstartup`, and `coustans2019coldstart60mv`
  - multi-source harvesting and self-powered interface papers such as `alghisi2017batteryless`, `wang2023serialstack`, `chen2024collaborative`, and `weng2024osece`
- Implemented design:
  - a packet-scout RC-ranked gate that samples both source branches, admits only one branch into the startup pump, and keeps the lane helper-free
- Validated result:
  - the `24`-case primary startup matrix does **not** show a general correctness win over the fixed or nonaware baselines
  - the `6`-case falsifier suite does show a narrow adversarial boundary where the champion avoids some nonaware mixed-source failure modes
- Evidence anchors:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_summary.json`
  - `figures/h1_startup_sensitivity.svg`
  - `figures/h1_falsifier_boundary.svg`

## Reviewer (`reviewer`)

- The fixed startup path remains too competitive for a broader H1 story.
- The primary matrix ties all three designs at `17/24` startup successes and shows no primary-matrix back-drive separation.
- Lower control energy is real but not sufficient:
  - the champion lowers `e_ctrl` in many cases without converting that into broad startup wins
- Rejected storylines:
  - `general superiority over the fixed path`
  - `general superiority over the 2023-2024 multi-input interface family`
  - `minimum startup voltage advance`
  - `steady-state efficiency advance`

## Citation Auditor (`citation_auditor`)

- `results/verification/citation_audit.md` clears only the narrowed claim set.
- Allowed statements are limited to the `PASS` rows in that audit.
- Blocked wording remains blocked:
  - `first`
  - `novel`
  - `best`
  - broad fixed-baseline superiority
  - steady-state efficiency claims
- Bibliography scope:
  - `21` total entries in `sources.bib`
  - `16` relevant papers
  - `5` repo or local-documentation entries

## Benchmark Auditor (`benchmark_auditor`)

- Benchmark integrity passes:
  - startup and falsifier manifests are complete
  - run logs and summaries are internally consistent
- Benchmark promotion gate blocks:
  - the primary matrix is a null on startup-count advantage
  - the primary matrix is a null on back-drive separation
- The only benchmark boundary that survives is the two-case falsifier subset:
  - `fa_001`
  - `fa_005`
- No new broad sweep is justified from the current evidence.

## Integrator (`integrator`)

- Final integrated verdict:
  - H1 is **not promoted**
  - H1 is **not killed**
  - H1 is reportable only as a narrowed adversarial-startup result
- Allowed final claim:
  - helper-free pre-arbitration source awareness can avoid some nonaware mixed-source startup failures under collapse and mixed-polarity stress
- Open kill conditions:
  - a stronger fixed-path or minimally corrected nonaware baseline reproduces `fa_001` and `fa_005` under equal accounting
  - a direct-overlap paper is recovered that already demonstrates helper-free pre-arbitration mixed-source startup with the same stress boundary
  - a materially improved collapse or chatter model removes the `fa_001` and `fa_005` separation on rerun
- Lane-routing consequence:
  - H2 and H3 remain unactivated because H1 narrowed rather than collapsed, and the run audit already blocks another broad sweep
