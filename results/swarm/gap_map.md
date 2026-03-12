# Gap Map

Date: 2026-03-12
Scope: negative-space mining around the active H1 lane, not a fresh broad EE idea hunt

## Selection Filter

- Read first:
  - `results/research_context.md`
  - `results/literature/prior_art_watchlist.md`
  - `results/literature/prior_art_gap.md`
  - `results/literature/gap_frontier.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
- Routing rule:
  - stay inside `H1_multisource_cold_start`
  - do not reactivate the old broad cryo/rad-hard/high-temperature branches here
- Budget rule:
  - prefer executed artifacts, manifests, netlists, and local literature notes over new search
  - only keep gaps that are both technically sharp and still plausibly under-served after the repo's overlap screen

## Explicitly Deprioritized

- Any claim framed as:
  - `lower startup voltage`
  - `better generic multi-source PMU`
  - `better steady-state extraction efficiency`
  - `first helper-free multi-source cold start`
- Generic source-aware ranking as a headline mechanism:
  - the executed lane already killed that story
- Unrelated frontier pivots:
  - cryogenic support blocks
  - radiation-tolerant bias loops
  - harsh-environment sensor interfaces

## Ranked Gaps

### 1. Confidence-Aware Arbitration When The Sources Are Not Separably Rankable

- Why this is the most interesting remaining gap:
  - the executed result shows that packet-gated isolation survives, but explicit RC ranking is not causal
  - `source_blind` matches the 24-case startup matrix and beats the RC-ranked champion on the falsifier suite (`10/10` vs `8/10`)
- Why it still looks under-served:
  - nearby work crowds generic startup and generic multi-input interfaces, but the repo record does not surface a strong comparator for pre-handoff confidence detection
  - the open problem is now narrower and less fashionable: how to decide when *not* to trust analog source ranking
- Concrete failure mode:
  - under weak or near-tied sources, the selector commits to a noisy winner, spends control energy, and gives up the robustness that the blind packet gate gets by refusing to over-infer
- Plausible circuit thesis:
  - add a separability detector based on `|env_a - env_b|`, dual-window slope spread, or packet-to-packet consistency
  - fall back to blind packet isolation until the evidence margin clears a threshold
- Fast falsifier:
  - if the confidence-gated version never beats `source_blind` on near-tie cases under equal `e_ctrl`, kill it
- Evidence in repo:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item021_decision_memo.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/ablation_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`

### 2. Restart-Safe Handoff Under Repeated Collapse, Recovery, And Partial-Store Memory

- Why this looks under-served:
  - most of the executed contract still centers on first successful handoff
  - real batteryless nodes do not live in a single cold-start event; they brown out, reappear, and try again from a partially charged store
- Concrete failure mode:
  - a design reaches the first handoff threshold once, then source collapse or recovery windows drive a fall event, leave stale selector state behind, and turn the next startup into a warm-restart trap rather than a clean retry
- Why the current repo does not close it:
  - the measurement hook latches the first handoff event for pre-handoff energy accounting
  - the falsifier summary records fall/rise2 events, but the current writeable conclusion still does not deeply characterize restart correctness after the first release
- Plausible circuit thesis:
  - a restart-safe scout and handoff controller that explicitly scrubs stale winner state, quarantines a collapsing source, and only re-enables ranking once the store and source ports both recover
- Fast falsifier:
  - if repeated-collapse cases are handled just as well by a simple fixed hysteretic path once equal control-energy accounting is restored, kill it
- Evidence in repo:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`

### 3. Device-Faithful Anti-Backdrive Under Real Leakage, Body Paths, And Nonideal Routing

- Why this looks under-served:
  - anti-backdrive remains part of the surviving claim boundary, but the current executed models are still too clean to settle it
  - the primary matrix reports zero back-drive for every design in every case, which is useful as a warning, not as closure
- Concrete failure mode:
  - a seemingly isolated branch still leaks through body paths, finite off-isolation, charge injection, or route asymmetry and quietly re-energizes the wrong source during startup
- Why the current repo does not close it:
  - `source_pair_models.inc` uses ideal behavioral sources plus resistors
  - `startup_cells.inc` uses idealized switch models and near-infinite leakage unless the falsifier manually forces `RLEAK_ROUTE`
  - the leak-path falsifier only probes a coarse stress point, not a device-faithful parasitic envelope
- Plausible circuit thesis:
  - source-referenced active clamps or back-to-back gated isolation devices with an explicit low-energy reverse-port detector
- Fast falsifier:
  - if the apparent win disappears once realistic parasitics and equal overhead accounting are introduced, or if a simpler back-to-back switch does the same job, kill it
- Evidence in repo:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/startup_cells.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`

### 4. Truly Asynchronous Heterogeneity: Independent Ramp Rates, Unequal VOC, And Late Source Arrival

- Why this looks under-served:
  - the live lane is about heterogeneous weak sources, but most of the executed matrix still gives both sources the same ramp law and the same nominal `VOC`
  - only two falsifier cases introduce unequal `VOC`, and the shared source model has one global `RAMP_MVPS`
- Concrete failure mode:
  - a weak early source wins the scout phase, then a stronger late-arriving source appears after partial charging and destabilizes the startup path
  - or a late opposite-polarity source lands after state has already been committed and forces a reclassification penalty
- Why it matters:
  - this is closer to how ambient harvesters actually coexist than a perfectly synchronous two-source ramp
  - it is also a setting where blind packet isolation may stop being enough
- Plausible circuit thesis:
  - per-source event windows, stale-winner timeouts, and a late-arrival quarantine gate before handoff is released
- Fast falsifier:
  - if simply increasing `C_STORE` or delaying handoff matches the benefit without any smarter logic, kill it
- Evidence in repo:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/results/manifests/falsifier_cases.json`

### 5. Helper-Free Startup Beyond The Two-Source Linear-Thevenin Abstraction

- Why this still matters:
  - the current result is structurally tied to a floating two-source Thevenin model
  - that is useful for isolating mechanism, but it is not yet the same problem as real mixed-source harvesting where the source law can be charge-limited, AC-originated, history-dependent, or dynamically impedance-shifting
- Why it is under-served but risky:
  - the repo's own reserve lane `H3_dynamic_source_impedance` exists because this frontier is more novel than generic MPPT, but it also has overlap risk if phrased too broadly
  - the defensible niche is helper-free *pre-arbitration startup correctness* across source families, not another dynamic-impedance harvester paper
- Concrete failure mode:
  - a scout signal that works on a linear Thevenin source misreads a triboelectric, piezoelectric, or bursty RF-like source and spends more energy probing than the source can safely deliver
- Plausible circuit thesis:
  - a charge-domain scout that estimates `dQ/dV` or packet yield instead of assuming a fixed resistive source law
  - or a source-family front end that normalizes unlike inputs before they reach the shared startup gate
- Fast falsifier:
  - if a simple blind packet gate or hysteretic baseline matches the result once probing overhead is counted, kill it
- Evidence in repo:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc`
  - `results/swarm/tool_plan.md`
  - `results/literature/prior_art_gap.md`

## Priority Order

1. Gap 1 if the goal is a new circuit idea that grows directly out of the executed negative result.
2. Gap 2 if the goal is a stronger reliability paper with a clean falsifier path.
3. Gap 3 if the team wants the most defensible measurement-and-modeling moat.
4. Gap 4 if the next experiments should make the source model more realistic without leaving H1.
5. Gap 5 only if the program is ready to widen the source family and absorb the added overlap risk.

## Best Immediate Bet

- Most specific and non-obvious:
  - Gap 1
- Most important if the eventual target is a real batteryless node:
  - Gap 2
- Most likely to overturn the current optimistic simulator boundary:
  - Gap 3
