# Novelty Report

Date: 2026-03-12
Scope: post-verification novelty review of the H1 weak-source cold-start lane after the executed ablations, expanded falsifier suite, and robustness study
Status: PASS as a boundary and falsification paper; BLOCK as a broad architecture-novelty paper

## Reviewed Material

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/verification/final_research_brief.md`
- `results/verification/benchmark_report.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/robustness_summary.json`
- `sources.bib`

## Executive Assessment

- The lane is **not** distinct as another generic multi-source cold-start interface, another self-powered multi-input harvester, or another broad anti-backdrive architecture.
- The lane **is** distinct as a narrower and more interesting result:
  - a helper-free weak-source startup study that explicitly tests whether pre-handoff source ranking is necessary
  - a same-family ablation result showing that blind packet gating dominates explicit RC ranking under expanded adversarial stress
  - a simplified follow-on control (`time_constant_ranked`) that preserves most of the boundary while halving pre-handoff control energy
- The novelty therefore shifts from a new architecture claim to a falsification claim:
  - the field-level assumption under test is that more elaborate pre-handoff source awareness is the natural path to robustness
  - the executed evidence shows that, in this lightweight packet-gated family, isolation is the load-bearing ingredient and explicit ranking is not

## Claim-By-Claim Comparison

| Candidate framing | Closest prior papers | Overlap judgment | Honest novelty judgment |
| --- | --- | --- | --- |
| Another weak-source integrated startup circuit | `goppert2016startup70mv`, `das2017selfstarter`, `quintero2019cmosstartup`, `coustans2019coldstart60mv` | Heavy overlap | Not novel on this framing. |
| Another adaptive dual-source startup path | `tang2018dualsource` | Direct overlap | Not novel on this framing either. |
| Another bipolar / dual-polarity startup interface | `cao2019bipolarinput`, `kuai2022dualpolarityjssc`, `alhawari2017polaritydetection` | Direct overlap on polarity handling | Mixed-polarity support alone is not a novelty moat. |
| Another autonomous multi-input harvester platform | `alghisi2017batteryless`, `li2022multiinputplatform`, `wang2023serialstack`, `chen2024collaborative`, `weng2024osece` | Strong overlap on multi-input and self-powered routing | Not novel as a broad platform paper. |
| A helper-free falsification study of pre-handoff ranking vs. minimal packet gating | no direct paper in the current set makes this negative-result claim | Lower overlap | This is the defensible novelty core. |

## What Actually Differs From Prior Work

1. The contribution is evaluation-first and mechanism-first rather than headline-architecture-first.
   - The paper does not claim a new best startup path.
   - It asks a sharper question: under simultaneous weak sources, does explicit pre-handoff ranking buy anything beyond packet-gated isolation?

2. The same-family ablation is load-bearing.
   - Prior work usually argues for a new selector or interface mode.
   - This lane executes the simpler within-family alternative and shows that the simpler alternative is at least as good and sometimes better.

3. The metric contract is helper-free and pre-handoff specific.
   - The study explicitly repairs the accounting so control energy is measured before first handoff, not over the full transient window.
   - That makes the remaining energy claim interpretable and prevents a false overhead narrative.

4. The claim is tied to adversarial simultaneous-source stress, not to minimum startup voltage or steady-state efficiency.
   - The strongest evidence comes from collapse, leak-path, unequal-`VOC`, and real chatter cases.
   - That is a narrower but more defensible contribution than a generic multi-input PMU story.

## What Is No Longer Defensible

- `source-aware startup interface` as the main headline
- `novel multi-input PMU`
- `anti-backdrive architecture`
- `best` or `first` language
- any suggestion that the RC-ranked selector itself is the important new mechanism

## Best Final Novelty Narrative

- The publishable result is that helper-free packet-gated isolation matters, but explicit source ranking does not survive the ablation screen.
- `source_blind` is the dominant design on the expanded falsifier suite, and `time_constant_ranked` keeps nearly all of that benefit at much lower control cost than the original RC-ranked design.
- The paper therefore contributes a falsification result plus a simplified design-space map, not a broad new startup architecture.

## Bottom Line

- Write the paper as a circuit-level falsification study with a bounded engineering takeaway.
- The most honest subtitle is some version of:
  - `minimal packet gating falsifies pre-handoff source ranking in weak multi-source cold start`
- Anything broader than that would collapse into prior work too quickly.
