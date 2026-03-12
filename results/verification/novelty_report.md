# Novelty Report

Date: 2026-03-12
Phase: post_deepen
Scope: closest-prior-art screen for the final H1 artifact pack after the DEEPEN lane execution
Status: materially distinct only as a bounded same-family abstain-to-commit result; revise any broader novelty framing

## Materials Reviewed

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/literature/semantic_scholar_manifest.json`
- `results/swarm/director_brief.md`
- `research_paper.tex`
- `sources.bib`
- `results/verification/verification_summary.md`
- `results/verification/final_research_brief.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item028_metric_control_repair.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item029_confidence_variant.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item030_deepen_matrix.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/deepen_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`

## Executive Assessment

- The package is not materially distinct as another low-voltage cold-start paper, another mixed-polarity startup paper, another adaptive source-tracking controller, or another autonomous multi-input PMU.
- The only clearly surviving literature-facing novelty is narrower:
  - inside the executed helper-free packet-isolated startup family, the controller should abstain on static near ties and commit only when temporal separability appears
- That result is materially different from the closest adaptive-tracking papers because it is not a continuous optimizer; it is a conditional pre-handoff commit rule that intentionally collapses to the blind posture when the evidence stays ambiguous.
- Even that novelty is still small-scope:
  - same scaffold, not a new topology
  - behavioral macro, not a hardware-plausible circuit implementation
  - no literature-faithful executed comparator
  - retrieval-limited gap argument rather than a field-wide absence proof

## Claim-By-Claim Comparison

| Major claim as the paper could be read | Closest paper or line of work | Overlap signal | Novelty judgment | Required boundary |
| --- | --- | --- | --- | --- |
| `helper-free multi-source cold start` as a new architecture class | Weak-source startup line: `goppert2016startup70mv`, `das2017selfstarter`, `quintero2019cmosstartup`, `coustans2019coldstart60mv`; multi-source PMU line: `alghisi2017batteryless`, `li2022multiinputplatform`, `liu2024` | Low-voltage startup, cold-start autonomy, and helper-free operation are already occupied | Not materially distinct if framed as a new cold-start architecture or helper-free PMU | Do not claim novelty on low startup voltage, helper-free operation alone, or generic multi-source cold start |
| `mixed polarity` as a differentiator | `alhawari2017polaritydetection`, `cao2019bipolarinput`, `kuai2022dualpolarityjssc` | Prior work already handles polarity detection or dual-polarity startup | Not materially distinct | Use mixed polarity only as a stress regime, not as novelty |
| `better source-aware pre-handoff ranking` or `better selector` | `tang2018dualsource`, especially `liu2018` | Prior work already performs adaptive dual-source startup and cycle-by-cycle source tracking | Not materially distinct | Do not position H1 as a generally better ranking controller; `time_constant_ranked` is still faster internally |
| `confidence-gated abstention` / temporal-separability rule | Closest line is still `liu2018`; adjacent adaptive PMU line includes `liu2024` and `liu2024distributedpmu` | Same family of pre-handoff source inference, but prior art optimizes continuously while H1 explicitly refuses to commit under static ambiguity | Materially distinct, but only as a bounded same-family control-law result | Claim only: abstain on static near ties, commit when ambiguity resolves over time |
| `speed/backdrive frontier` from blind packet isolation vs confidence vs no-packet merge | Multi-input self-powered interface line: `wang2023serialstack`, `chen2024collaborative`, `weng2024osece`, plus the repo's same-scaffold `blind_packet_merge` control | Literature already covers coordinated multi-input routing and startup-capable interfaces; the executed frontier here is mainly an internal causal comparison | Useful internal differentiation, not strong external novelty | Present as same-scaffold evidence for the bounded claim, not as superiority over literature families |
| `proofs` and `repaired evidence pack` as major contributions | Internal verification / same-family ablation line of work rather than a specific external paper | Handoff repair, equal accounting, and no-packet controls make the result credible but do not create a literature moat | Supporting rigor, not material novelty | Keep these as validity enablers, not headline novelty claims |

## Closest Prior Art That Actually Bounds The Paper

### 1. Weak-source startup already occupies the low-voltage story

- The direct startup line is already mature:
  - `goppert2016startup70mv`
  - `das2017selfstarter`
  - `quintero2019cmosstartup`
  - `coustans2019coldstart60mv`
- Consequence:
  - H1 cannot claim novelty on absolute startup voltage, on the generic difficulty of weak-source startup, or on cold start by itself

### 2. Mixed-polarity handling already occupies that axis

- The closest polarity-aware anchors are:
  - `alhawari2017polaritydetection`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
- Consequence:
  - mixed polarity is a valid stress case, but it is not a novelty anchor

### 3. Adaptive pre-handoff source ranking is the sharpest overlap threat

- The closest single paper is `liu2018`
- The next closest same-problem anchor is `tang2018dualsource`
- These papers already occupy the broad idea that startup should infer the stronger source and act on that inference
- Consequence:
  - any H1 claim that sounds like `a generally better adaptive startup selector` is not materially distinct

### 4. Multi-input autonomy and PMU-scale framing are already crowded

- The closest platform and interface anchors are:
  - `alghisi2017batteryless`
  - `li2022multiinputplatform`
  - `wang2023serialstack`
  - `chen2024collaborative`
  - `weng2024osece`
  - `liu2024`
  - `liu2024distributedpmu`
  - `gogolou2025multisourcereview`
- Consequence:
  - H1 is not materially distinct as another multi-input PMU, all-rail cold-start platform, or autonomous multi-source architecture

### 5. Helper-assisted extreme startup already blocks easy voltage rhetoric

- `lu2024tegassist` is the overlap-bound paper here
- Consequence:
  - helper-free operation only matters as a boundary condition; it is not enough by itself to establish novelty

## What Is Actually New Enough To Keep

### 1. The abstain-to-commit rule is the one real positive novelty claim

- On static near ties:
  - `confidence_gated` and `source_blind` both start `6/6`
  - `confidence_gated` commits `0/6`
  - median handoff gap is only `-0.000545 s`
- On late-arrival near ties:
  - `confidence_gated` and `source_blind` both start `6/6`
  - `confidence_gated` commits `6/6`
  - median `t_handoff` improves by `0.30882 s`
  - median `t_commit = 1.02799 s`
- Distinctness judgment:
  - this is materially different from continuous adaptive tracking because the controller's defining action is deliberate abstention under unresolved ambiguity

### 2. The internal frontier is scientifically useful, but still bounded

- `blind_packet_merge` is faster on the decisive controls, but it reopens measurable wrong-way energy
- `confidence_gated` recovers part of that speed while preserving zero measured backdrive
- Distinctness judgment:
  - this is a useful same-scaffold causal frontier, not a new literature-level platform category

## Novelty Illusions And Weak Differentiation

- The paper really has one positive novelty claim and one useful falsification result. Packaging the manuscript as `five contributions` inflates novelty density.
- `multi-source`, `helper-free`, `cold start`, and `mixed polarity` are all occupied descriptors on their own. Combining them does not automatically create a new contribution.
- The confidence controller is incrementally distinct, not architecturally distinct:
  - it is the existing packet-isolated scaffold plus a normalized separability integrator and commit blend
- `time_constant_ranked` remains faster than `confidence_gated` on both static and late DEEPEN families, so the result is not `better selection`
- The theorem layer is mostly a formal restatement of behavior already built into the RC and tanh macro:
  - useful for rigor
  - weak as independent novelty
- The repaired evidence pack and same-scaffold no-packet control are important validity repairs, but they are not prior-art differentiation by themselves

## Missing Gap Evidence

- The strongest surviving novelty sentence is still retrieval-scoped:
  - `the recovered overlap set did not reveal a close same-family abstention-like pre-handoff controller`
- That sentence is acceptable only because it is narrow. It is not a field-wide absence proof.
- The abstention gap depends on targeted, non-exhaustive retrieval centered on:
  - `liu2018`
  - `liu2024`
  - `liu2024distributedpmu`
- `results/literature/semantic_scholar_manifest.json` is a query log, not a preserved result archive rich enough to independently prove absence
- Some earlier saved anchors were not recovered as exact-title matches; the report is relying on closest recovered substitutes such as `gogolou2025multisourcereview`
- No literature-faithful executed comparator has been run under the repaired measurement hooks
- The confidence node remains a behavioral macro rather than a transistor-level or hardware-plausible analog implementation
- DEEPEN robustness was not rerun across every decisive separator case, so the result is best read as an operating-regime insight, not a general startup law

## Acceptable Final Claim Boundary

- Safe:
  - in the executed helper-free packet-isolated startup family, the correct response to static near ties is abstention, while temporal separability justifies a later commitment
- Safe:
  - confidence gating recovers part of the late-arrival penalty carried by `source_blind` without reopening the backdrive seen in `blind_packet_merge`
- Not safe:
  - `first`
  - `best`
  - `general multi-input PMU`
  - `new architecture`
  - `better selector`
  - field-wide absence claims
  - literature-performance superiority claims

Verdict: REVISE
