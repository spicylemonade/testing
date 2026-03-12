# Novelty Report

Date: 2026-03-12
Phase: review_round_1
Scope: closest-prior-art screen for the current H1 manuscript and artifact pack
Status: materially distinct only as a narrow falsification/simplification paper; not materially distinct as a broad architecture-novelty paper

## Reviewed Material

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/literature/gap_frontier.md`
- `results/literature/gap_frontier.json`
- `results/swarm/director_brief.md`
- `results/verification/final_research_brief.md`
- `results/verification/verification_summary.md`
- `results/verification/benchmark_report.md`
- `research_paper.tex`
- `sources.bib`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_comparison.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`

## Executive Assessment

- The manuscript is not meaningfully new as another weak-source startup circuit, another adaptive dual-source starter, another mixed-polarity interface, or another autonomous multi-input harvester. The closest cited lines of work already cover those spaces: `goppert2016startup70mv`, `das2017selfstarter`, `quintero2019cmosstartup`, `coustans2019coldstart60mv`, `tang2018dualsource`, `cao2019bipolarinput`, `kuai2022dualpolarityjssc`, `alghisi2017batteryless`, `li2022multiinputplatform`, `wang2023serialstack`, `chen2024collaborative`, and `weng2024osece`.
- The surviving novelty is narrower and mostly methodological: a helper-free, same-family ablation showing that packet-gated isolation appears load-bearing in the executed model, while explicit pre-handoff source ranking is not.
- That narrower result is interesting enough to write, but the manuscript still overstates the external novelty in a few places. The weakest sentence is the literature-gap claim that same-family falsification of ranking is "not well represented" in prior work. The repo does not actually prove that gap.
- The right publication posture is therefore: negative-result and simplification paper, with tighter wording and clearer separation between internal mechanism claims and field-level novelty claims.

## Major Claims vs Closest Prior Art

| Major claim in the current paper | Closest paper or line of work | Overlap signal | Novelty judgment |
| --- | --- | --- | --- |
| Helper-free simultaneous weak-source cold start is the problem of interest | `tang2018dualsource`, `alghisi2017batteryless`, `li2022multiinputplatform`, `gogolou2025multisourcereview` | Dual-source startup, multi-source PMUs, autonomous multi-input cold start, and the broader multi-source integration problem are already established. | Weak as an architecture claim. Distinct only because the manuscript narrows to pre-handoff mechanism testing under one shared contract. |
| Mixed-polarity and heterogeneous-source stress are central | `cao2019bipolarinput`, `kuai2022dualpolarityjssc`, `alhawari2017polaritydetection` | Bipolar or dual-polarity startup/polarity-detection interfaces already exist. | Not a novelty moat. Mixed polarity is a valid stress axis, not a stand-alone contribution. |
| Packet-gated isolation, not explicit ranking, is the real load-bearing ingredient | Adaptive/source-aware startup and multi-input interface line: `tang2018dualsource`, `wang2023serialstack`, `chen2024collaborative`, `weng2024osece` | Those papers motivate added routing, adaptation, or self-powered multi-input control. The manuscript's distinct move is to test whether explicit ranking is necessary once isolation already exists. | This is the best surviving novelty claim. Materially distinct enough to matter, but only as a narrow same-family falsification result. |
| The paper contributes a unified helper-free benchmark with repaired pre-handoff accounting | Multi-source PMU/platform line: `alghisi2017batteryless`, `li2022multiinputplatform`, plus review framing in `gogolou2025multisourcereview` | Prior work already evaluates multi-input harvesters, cold start, and interface tradeoffs. | Moderate as a repo artifact, weak as a field-level novelty claim. The benchmark is internal, aliased, and not literature-faithful. |
| `time_constant_ranked` is a valuable lower-overhead source-aware alternative | Adaptive dual-source startup / arbitration line led by `tang2018dualsource` and the broader multi-input routing family | It is another source-aware selector variant inside an already crowded family. | Weak as a major claim. Keep as a secondary internal design-space result, not as a novelty headline. |
| The paper proves exact control-energy and branch-join facts for the implemented netlists | No named external paper is the right comparator; this is an internal theorem about the executed decks | The theorem is about the repo's behavioral netlists, not a field-level architectural differentiation claim. | Strong inside the model, but not a material prior-art differentiator by itself. |

## Closest Overlap Families That Still Bound The Paper

### 1. Weak-source cold-start papers

- Closest papers:
  - `goppert2016startup70mv`
  - `das2017selfstarter`
  - `quintero2019cmosstartup`
  - `coustans2019coldstart60mv`
- What they already cover:
  - integrated weak-source startup
  - low-startup-voltage framing
  - self-starting cold-start circuitry
- Novelty consequence:
  - the manuscript cannot claim novelty on startup difficulty, cold-start integration, or low-voltage operation alone

### 2. Adaptive dual-source and polarity-aware startup

- Closest papers:
  - `tang2018dualsource`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `alhawari2017polaritydetection`
- What they already cover:
  - adaptive dual-source startup
  - bipolar or dual-polarity startup handling
  - polarity detection during harvesting startup
- Novelty consequence:
  - "source-aware startup" and "mixed-polarity support" are overlap-heavy framings
  - the manuscript survives only by claiming that extra ranking logic is unnecessary within the tested family

### 3. Autonomous multi-input interface papers

- Closest papers:
  - `alghisi2017batteryless`
  - `li2022multiinputplatform`
  - `wang2023serialstack`
  - `chen2024collaborative`
  - `weng2024osece`
- What they already cover:
  - self-powered multi-input harvesting
  - routing/isolation/arbitration across multiple inputs
  - cold-start-capable multi-input platform framing
- Novelty consequence:
  - the manuscript is not distinct as "another multi-input harvester interface"
  - it is distinct only if it stays explicitly on the ablation question: does ranking buy anything once branch isolation already exists

### 4. Helper-assisted ultra-low-startup papers

- Closest paper:
  - `lu2024tegassist`
- Why it matters:
  - it narrows any claim that quietly relies on one source behaving like an unstated helper rail
- Novelty consequence:
  - the helper-free condition is important, but it is a guardrail, not the main novelty

## Novelty Illusions

### 1. "This is a new multi-source startup architecture"

- Why it is an illusion:
  - `tang2018dualsource`, `alghisi2017batteryless`, `li2022multiinputplatform`, `wang2023serialstack`, `chen2024collaborative`, and `weng2024osece` already occupy that design space.
- Repo signal:
  - `claim_matrix.md` explicitly blocks `new general-purpose multi-input PMU` and `first helper-free multi-source cold-start interface`.

### 2. "Mixed polarity is the novelty moat"

- Why it is an illusion:
  - `cao2019bipolarinput`, `kuai2022dualpolarityjssc`, and `alhawari2017polaritydetection` already establish polarity-aware startup/interface work.
- Repo signal:
  - the paper itself uses mixed polarity mainly as a falsifier stress, which is the correct posture.

### 3. "Minimal packet gating" already means a practically simpler circuit

- Why it is an illusion:
  - `source_blind_packet_gate` in `packet_scout_blocks.inc` still instantiates scout RC observation branches and uses the same `G_SCOUT_CTRL=40n` control conductance as the RC-ranked gate.
- Concrete overlap signal:
  - the blind packet gate is a selector-ablation inside the same scaffold, not yet a stripped-down hardware-minimal implementation.
- Novelty consequence:
  - the title/message should be read as a mechanism simplification claim, not as proof that the final hardware is already the simplest realizable packet-gated circuit.

### 4. "`source_blind` is the dominant design" in a broad sense

- Why it is an illusion:
  - `source_blind` leads only on the 10-case falsifier suite; all five designs tie at `17/24` in the primary matrix.
- Repo signal:
  - `benchmark_report.md` blocks broad superiority and limits the claim to the adversarial boundary.
- Novelty consequence:
  - words like `dominates`, `dominant design`, or `often better` need tighter scope.

## Weak Differentiation

- The paper's strongest sentence, "packet-gated isolation matters, explicit pre-handoff source ranking does not," is defensible only with the built-in limiter "in the executed helper-free weak-source model."
- The time-constant-ranked branch is not a second novelty claim. It is a good internal tradeoff point, but it sits too close to already-known adaptive startup/arbitration work to carry headline novelty by itself.
- Theorems about conductance and branch joining are useful and correct at the model level, but they do not by themselves differentiate the paper from prior interface families.

## Missing Gap Evidence

### 1. The gap-first search is effectively empty

- `gap_frontier.md` contains no substantive frontier papers.
- `gap_frontier.json` records zero useful results for the gap/open-problem queries.
- Consequence:
  - the manuscript does not yet have a strong evidence base for the claim that same-family falsification of startup ranking is absent or rare in the literature.

### 2. No literature-faithful executed comparator exists

- `benchmark_report.md` states that literature comparison remains structural rather than measured.
- Consequence:
  - the paper can claim internal mechanism falsification, but not measured superiority or clean external separation from the closest silicon papers.

### 3. The benchmark is narrower than the rhetoric

- The primary matrix is aliased rather than factorial, and the robustness study covers four load-bearing cases rather than the full manifest.
- Consequence:
  - the benchmark is good enough for a bounded negative-result paper, but not strong enough to claim a general startup-envelope map for the field.

## Required Revisions To Clear Novelty

- Recast the novelty sentence from "not well represented in the literature" to a weaker, auditable form such as "the recovered prior-art set did not reveal a close same-family falsification study."
- Keep the headline on falsification of ranking, not on a new architecture or platform.
- Remove or soften manuscript phrases that broaden the claim past the validated scope:
  - `dominates it`
  - `dominant design`
  - `the selector was never the real ingredient`
  - `a blind packet gate is sufficient and often better`
- Keep mixed polarity, leak paths, chatter, and unequal-`VOC` framed as stress tests, not as novel mechanisms.
- If more budget appears later, spend it on one of two things:
  - a literature-faithful executed comparator
  - a stronger gap note showing that the ablation/falsification angle is genuinely underrepresented

## Bottom Line

- The manuscript has a real contribution, but it is narrower than the field-level framing still implies.
- The materially distinct part is the same-family negative result:
  - under one helper-free multi-source startup contract, explicit pre-handoff ranking is empirically unnecessary once packet-gated isolation exists
- That is publishable as a bounded falsification/simplification paper.
- It is not yet cleanly justified as a stronger novelty claim than that.

REVISE
