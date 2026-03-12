# Citation Audit

Date: 2026-03-12
Phase: review_round_1
Scope: evidence traceability and citation support only
Verdict: PASS for the core experimental / netlist-level claim set; REVISE for literature-framing claims

## Inputs Reviewed

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`
- local evidence pack used by the manuscript:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/startup_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_results.csv`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/baselines/fixed_startup_path/fixed_startup_path.cir`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/source_blind_packet_gate/source_blind_packet_gate.cir`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/time_constant_ranked_arbiter/time_constant_ranked_arbiter.cir`
- web spot-checks on the active citation spine and candidate additions

## Cleared Claim Support

These claims are traceable to repository artifacts and do not currently need additional literature citations.

| Claim | Verdict | Evidence |
| --- | --- | --- |
| Five-design primary startup matrix is tied at `17/24`. | PASS | `startup_summary.json` counts for `champion`, `fixed`, `nonaware`, `source_blind`, and `time_constant_ranked` are all `17` startup successes. |
| Expanded falsifier ranking is `source_blind 10/10`, `time_constant_ranked 9/10`, `champion 8/10`, `fixed 7/10`, `nonaware 5/10`. | PASS | `falsifier_summary.json`; per-case confirmation in `falsifier_results.csv`. |
| `fa_002` and `fa_006` are the only falsifier cases that separate `source_blind` from `champion`. | PASS | `falsifier_results.csv`. |
| Robustness headline claims around `fa_001`, `fa_005`, and `sm_015` are supported. | PASS | `robustness_summary.json` shows `fixed` is `0/24` on `fa_001`, `nonaware` is `0/24` on `fa_005`, and all five designs are `24/24` on `sm_015`. |
| The repaired measurement contract isolates pre-handoff energy from full-window energy. | PASS | `measurement_hooks.inc:13-32` explicitly gates `e_backdrive` and `e_ctrl` with `1 - V(handoff_latched)` and retains separate `*_full` diagnostics. |
| The control-energy law is grounded in implemented control conductances. | PASS | `fixed_startup_path.cir:36-38`, `nonaware_multi_input_startup.cir:43-46`, and `packet_scout_blocks.inc:33,52,83` expose the exact control branches used by the theorem. |
| Only `Nonaware` has an explicit pre-handoff branch join. | PASS | `nonaware_multi_input_startup.cir:36-39` contains `RJOIN_*` ties; the packet-gated decks route both sources but only connect them through behavioral current-source blocks (`source_blind_packet_gate.cir:31-35`, `time_constant_ranked_arbiter.cir:32-36`, `packet_scout_blocks.inc:27-31,46-50,77-81`). |

## Findings

### 1. Missing support for the paper's strongest literature-generalization claims

Severity: high

Affected text:
- `research_paper.tex:65-66`
- `research_paper.tex:87`

Problem:
- The manuscript asserts that the literature "rarely closes the same-family ablation loop" and that explicit falsification studies of pre-handoff ranking are "not well represented."
- Those are absence / prevalence claims about the field, but they are not currently backed by a review citation, a scoped search citation, or a representative comparison set in the text.

Why this matters:
- These sentences do real argumentative work. They justify why the paper exists.
- The current citation set supports overlap with prior work, but it does not support a field-wide statement about what is rare.

Recommended action:
- Best fix: soften the wording to a scoped observation rather than a field-level claim.
- If the wording stays strong, add at least one review source plus representative overlap papers and phrase the claim as "within the retrieved overlap set" or equivalent.

### 2. The opening motivation sentence carries more technical content than its citations support

Severity: medium

Affected text:
- `research_paper.tex:63`

Problem:
- The sentence bundles together slow ramps, asynchronous collapse, opposite polarity, helper-free startup, and avoiding source-to-source damage.
- The attached citations are mostly low-voltage startup papers plus one review (`goppert2016startup70mv`, `das2017selfstarter`, `gogolou2025multisourcereview`).
- The mixed-polarity and polarity-handling part of the claim is better supported by `cao2019bipolarinput`, `kuai2022dualpolarityjssc`, and `alhawari2017polaritydetection`, but those appear only in later text.

Why this matters:
- The sentence currently looks fully supported, but the support is uneven across its subclaims.

Recommended action:
- Split the sentence, or add the polarity-facing citations directly at this location.

### 3. Several broad prior-art category claims are under-cited or supported by a single representative paper

Severity: medium

Affected text:
- `research_paper.tex:81-85`
- `research_paper.tex:98`
- `research_paper.tex:100`

Problem:
- `research_paper.tex:81` says startup below `100 mV` has been demonstrated repeatedly, but one of the cited anchors (`das2017selfstarter`) is explicitly a `220 mV` self-starter. The sentence therefore overclaims against its own citation bundle.
- `research_paper.tex:83` says the "closest architectural overlap" is the adaptive dual-source startup line, but only `tang2018dualsource` is attached.
- `research_paper.tex:85` and Table 1's autonomous multi-input row are directionally correct, but the manuscript leaves several already-bibliographed family members uncited.
- The cited narrative is usable, but broader category statements are doing more work than the citation density warrants.

Why this matters:
- This is where novelty / overlap guardrails live. Thin support here weakens the manuscript's claim boundary.

Recommended action:
- Narrow `research_paper.tex:81` to the genuinely sub-`100 mV` papers already cited, or split `das2017selfstarter` into a separate clause about weak-source self-starting rather than sub-`100 mV` startup.
- Strengthen the multi-input family paragraph and Table 1 with already available sources:
  - `alhawari2016multisourcepmu`
  - `wang2021serialsshi`
  - `zheng2023sharedinductor`
  - optionally `xia2022dualinductor`
- Soften "closest architectural overlap" to "one close architectural overlap" unless a broader source set is added.

### 4. The discussion contains an uncited field-level comparison about publication culture

Severity: low to medium

Affected text:
- `research_paper.tex:614`

Problem:
- "Weak-source energy-harvesting interfaces are often discussed only through positive-result narratives" is a field-level sociological claim with no citation.

Why this matters:
- This is not central to the technical result, but it is still a broad comparison statement.

Recommended action:
- Either delete / soften it, or back it with review literature rather than isolated primary papers.

### 5. One bibliography record remains metadata-suspicious and should stay quarantined

Severity: low

Affected text:
- `sources.bib:1-8`

Problem:
- `hernandez2013tegboost` remains internally flagged as unresolved.
- Spot-checking indicates the DOI and the stated venue metadata do not line up cleanly.

Why this matters:
- It is not cited in the manuscript, so it is not an active blocker.
- It is still the only likely citation-hallucination / metadata-mismatch record left in `sources.bib`.

Recommended action:
- Keep it uncited or remove it from the production bibliography.

## Hallucination / Integrity Check

- No dangling citation keys were found in `research_paper.tex`; every in-text key exists in `sources.bib`.
- Spot-checks of the active citation spine found plausible title / venue / DOI matches for the manuscript-facing keys, including:
  - `tang2018dualsource`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `li2022multiinputplatform`
  - `chen2024collaborative`
  - `weng2024osece`
  - `gogolou2025multisourcereview`
- The only remaining likely hallucination risk is the already uncited `hernandez2013tegboost` entry.

## Highest-Value Sources To Add

### Add citations from the existing bibliography first

1. `alhawari2016multisourcepmu`
- Why: directly strengthens the multi-source PMU / autonomous multi-input family claim.
- Best insertion points:
  - `research_paper.tex:85`
  - `research_paper.tex:100`

2. `wang2021serialsshi`
- Why: gives the paper a stronger bridge to self-powered multi-input interface work rather than relying mostly on 2023-2024 examples.
- Best insertion points:
  - `research_paper.tex:85`
  - `research_paper.tex:100`

3. `zheng2023sharedinductor` or `xia2022dualinductor`
- Why: both strengthen the "crowded family" argument around self-powered multi-input piezo interfaces.
- Best insertion points:
  - `research_paper.tex:85`
  - `research_paper.tex:100`

4. `lu2024tegassist`
- Why: useful if the authors want to emphasize that this study is helper-free while nearby low-startup work can use an assisting source.
- Best insertion points:
  - `research_paper.tex:63`
  - `research_paper.tex:603-604`

### Add new review-level sources if the broader framing is kept

5. Eftekhar et al., *Review of Fully Integrated Startup Techniques for Thermoelectric Energy Harvesting Systems* (2023), DOI `10.1007/978-3-031-46221-1_10`
- Why: this is the cleanest review-level support for the "integrated startup is already mature / crowded enough that generic startup framing is insufficient" argument.
- Best insertion points:
  - `research_paper.tex:81-83`

6. Grossi et al., *Energy Harvesting and Autonomous Self-Powered Sensors for WSN Applications: A Review*
- Why: this would better support the system-level opening claim about batteryless sensor nodes aggregating weak transducers.
- Best insertion points:
  - `research_paper.tex:63`

7. Sheng et al., *Advances in Interface Circuits for Self-Powered Piezoelectric Energy Harvesting Systems: A Comprehensive Review* (2025), DOI `10.3390/machines13060533`
- Why: this is useful if the manuscript keeps the broader "positive-result narratives" or "crowded self-powered interface family" framing.
- Best insertion points:
  - `research_paper.tex:85`
  - `research_paper.tex:614`

## Bottom Line

- The manuscript's core empirical and structural claims are traceable to repository artifacts and currently clear citation audit.
- The remaining audit risk is not fabricated experimental support; it is over-broad literature framing.
- The highest-priority repair is to narrow or better support the two field-level absence claims at `research_paper.tex:65-66` and `research_paper.tex:87`.
