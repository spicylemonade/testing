# Hypothesis Negative Space

Date: 2026-03-12
Scope: candidate EE directions chosen to avoid the repo's already crowded solution families and to stay inside a realistic `ngspice`-first budget.

## Negative-Space Filter

- Do not reopen broad `weak-source startup`, `lower startup voltage`, `generic dual/multi-source PMU`, or `steady-state extraction` claims. The repo already narrowed H1 to a helper-free packet-gated boundary and falsified the stronger source-ranking story.
- Do not spend the next budget on metaphor-heavy branches already screened by `results/swarm/falsifier.md`.
- Do not hide a helper rail, precharge node, or one source acting as an assistant.
- If a direction reduces to `another smarter selector`, `another UVLO tweak`, or `another anti-backdrive block`, pivot instead of polishing it.

## 1. Ignored: Confidence-Gated Abstention When Sources Are Not Separably Rankable

- Working name: `confidence_gated_blind_fallback`
- Core hypothesis:
  - the next useful startup circuit is not a better ranker; it is an analog separability detector that decides when *not* to trust ranking
  - under near-tied weak sources, a confidence gate that falls back to blind packet isolation should outperform always-rank variants on startup correctness per unit `e_ctrl`
- Why this is negative space:
  - the executed repo result already says packet-gated isolation survives while explicit RC ranking is not causal
  - what remains under-served is the abstention problem: detecting when analog evidence is too weak or inconsistent to justify a winner-take-all commit
- Angle to avoid:
  - avoid framing this as `a smarter source-aware startup architecture`
  - avoid claiming better source ranking in general; the point is confidence-aware refusal to over-infer
- First `ngspice` slice:
  - add one confidence node to the existing packet-gate scaffold using `|env_a - env_b|`, dual-window slope spread, or packet-to-packet consistency
  - sweep near-tie cases with small `VOC` offsets, `1:1` to `1:3` impedance spread, and unequal ramp arrival
  - compare against `source_blind` and `time_constant_ranked` on `startup_ok`, `t_handoff`, and `e_ctrl`
- Kill rule:
  - if the confidence-gated version never beats `source_blind` on the near-tie slices under equal accounting, kill it
- Repo anchors:
  - `results/swarm/gap_map.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`

## 2. Failed To Test: Restart-Safe Handoff After Collapse, Recovery, And Partial-Store Memory

- Working name: `restart_scrub_handoff_controller`
- Core hypothesis:
  - a handoff controller that explicitly scrubs stale winner state, quarantines collapsing sources, and re-arms only after both source ports and the store recover will beat one-shot startup logic on restart correctness
  - the interesting metric is not first handoff alone; it is correct second and third starts after partial brownout memory
- Why this is negative space:
  - most current evidence in the repo still centers on first successful handoff
  - real batteryless nodes do not get one clean cold start; they repeatedly collapse, recover, and retry from a partially charged reservoir
- Angle to avoid:
  - avoid turning this into `another UVLO deglitcher` or `another one-shot cold-start paper`
  - the thesis must stay on restart correctness under repeated collapse, not just chatter cosmetics
- First `ngspice` slice:
  - extend the falsifier deck to force repeated collapse and recovery windows after first handoff
  - add explicit stale-state scrub, loser quarantine, and re-arm timing logic
  - report `startup_ok`, `fall_count`, `rise2_ok`, restart latency, and restart-control energy against a fixed hysteretic baseline
- Kill rule:
  - if repeated-collapse cases are handled just as well by a simple fixed hysteretic path once equal control-energy accounting is restored, kill it
- Repo anchors:
  - `results/swarm/gap_map.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`

## 3. Could Not Scale: Device-Faithful Anti-Backdrive Once Ideal Switches Are Removed

- Working name: `reverse_port_sentinel_isolation`
- Core hypothesis:
  - the current anti-backdrive story is still too idealized
  - once finite off-isolation, body paths, charge injection, and route asymmetry are modeled, a source-referenced reverse-port sentinel plus back-to-back gated isolation may open a real correctness gap that the clean behavioral decks cannot show
- Why this is negative space:
  - the primary matrix reports zero back-drive for every design, which is a warning that the active models are too clean rather than proof that the problem is closed
  - the repo only probes leakage with coarse falsifier settings, not a device-faithful parasitic envelope
- Angle to avoid:
  - avoid selling this as `generic anti-backdrive` or `a better ideal diode`
  - the claim only survives if the win appears under realistic leakage and routing nonidealities with equal overhead
- First `ngspice` slice:
  - replace the near-ideal startup switch assumptions with finite leakage, body-diode, charge-injection, and route-asymmetry sweeps
  - compare three cases: plain back-to-back switch, current blind packet gate, and reverse-port sentinel isolation
  - report `e_backdrive`, false source re-energization events, and startup success under the same control monitor path
- Kill rule:
  - if a simpler back-to-back switch matches the result once realistic parasitics are included, kill it
- Repo anchors:
  - `results/swarm/gap_map.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/startup_cells.inc`

## Pivot Notes

- Focused external checks kept `H2_cryo_support_blocks` alive only as a backup because the model gate is still real; avoid another `cryo reference` or `cryo bandgap replacement` story unless sub-10 K uncertainty is the actual test target.
- Focused external checks kept `H3_dynamic_source_impedance` alive only as a reserve because recent variable-impedance work narrows the novelty margin; avoid generic `impedance-aware MPPT` framing.
- The three directions above are the best immediate negative-space bets because they grow out of the executed H1 falsification, reuse existing startup scaffolding, and can be killed quickly with disciplined `ngspice` experiments.
