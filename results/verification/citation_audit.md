# Citation Audit

Date: 2026-03-12
Scope: audit the load-bearing H1 claims against `sources.bib`, the lane-local verification notes, and the repo-level experiment artifacts
Status: PASS with blocked wording

## Bibliography Scope

- `sources.bib` currently contains:
  - `16` relevant paper entries
  - `5` repository or local-documentation entries
- Metadata basis used in this run:
  - recovered paper titles and paper IDs tracked in `results/literature/prior_art_gap.md`
  - the repo-local governing documents cited below through the `archivara2026*` entries

## Audit Rule

- Only `PASS` claims may appear in the final brief as affirmative statements.
- Any row marked `BLOCKED` is disallowed wording and must remain out of the final brief.

## Claim Matrix

| ID | Claim | Support | Status | Audit note |
| --- | --- | --- | --- | --- |
| C01 | The closest technical overlap is the integrated TEG startup family plus the recent self-powered multi-input interface family, not the polluted seed-watchlist papers. | `goppert2016startup70mv`; `quintero2019cmosstartup`; `coustans2019coldstart60mv`; `alghisi2017batteryless`; `wang2023serialstack`; `chen2024collaborative`; `weng2024osece`; `results/literature/prior_art_gap.md`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md` | PASS | Load-bearing overlap framing is supported. |
| C02 | The only allowed H1 contribution boundary is helper-free pre-arbitration source-aware startup sequencing under heterogeneous weak sources. | `archivara2026toolplan`; `archivara2026directorbrief`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md` | PASS | This is the narrow novelty boundary carried into final reporting. |
| C03 | The champion topology is helper-free and uses RC-ranked packet selection before handoff. | `archivara2026experimentspec`; `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`; `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir` | PASS | Structural claim is directly supported by the netlist and experiment contract. |
| C04 | The champion and both baselines were measured under the same startup, back-drive, and control-energy accounting contract. | `archivara2026experimentspec`; `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item011_signoff.md` | PASS | Equal accounting is essential to every benchmark claim. |
| C05 | The primary startup matrix executed `24` cases across `3` designs for `72` logged rows. | `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/startup_matrix_manifest.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item020_run_audit.md` | PASS | Coverage claim is directly supported by manifests and audit note. |
| C06 | The primary startup matrix shows `17/24` startup successes for champion, fixed, and nonaware. | `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json` | PASS | This claim is stable and repeated consistently across artifacts. |
| C07 | The primary startup matrix shows no back-drive separation for the champion relative to either baseline. | `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_comparison.csv`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md` | PASS | This negative result is load-bearing and must remain explicit. |
| C08 | The champion lowers measured startup-control energy in `13/24` cases versus fixed and `22/24` cases versus nonaware. | `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md` | PASS | Allowed as a bounded metric statement only. |
| C09 | The falsifier suite spans source collapse, mixed polarity, extreme asymmetry, and chatter-intended stress with `6` cases and `18` total rows. | `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md` | PASS | Required adversarial coverage is documented. |
| C10 | No measured handoff-fall or second-rise events occurred in the falsifier suite. | `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md` | PASS | Chatter-intended cases became no-start behavior instead of measured chatter. |
| C11 | The smallest surviving claim boundary is the two-case subset `{fa_001, fa_005}`. | `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_results.csv`; `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md` | PASS | This is the narrowest condition set supported by the evidence. |
| C12 | The surviving H1 story is mainly against the nonaware baseline under collapse and mixed-polarity stress, not a general win over the fixed startup path. | `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md` | PASS | This wording is validated and should anchor the final brief. |
| C13 | The champion beats the fixed startup path broadly. | `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md` | BLOCKED | Unsupported by the primary matrix and contradicted by the decision memo. |
| C14 | This design is the `first`, `novel`, or `best` helper-free multi-source cold-start interface. | `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`; `results/literature/prior_art_gap.md` | BLOCKED | Explicitly forbidden wording. No priority claim is supported. |
| C15 | The champion improves steady-state harvesting efficiency. | `archivara2026experimentspec`; `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md` | BLOCKED | No steady-state efficiency experiment was run. |

## Next Required Action

- Use only the `PASS` rows above in `results/verification/final_research_brief.md`.
- Keep all `BLOCKED` wording out of the final brief and the repo-level summary.
