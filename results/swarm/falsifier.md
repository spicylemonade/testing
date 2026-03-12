# Falsifier Memo

Generated: 2026-03-12
Role: `falsifier`
Scope: adversarial review of the live H1 lane (`H1_multisource_cold_start`), with brief kill notes for inactive H2/H3.

Budget discipline:
- no new directions are proposed here except minimal pivots needed to explain why the current claims would otherwise fail
- prefer prior-art overlap, missing controls, benchmark traps, and literature branches that can collapse weak claims

## Executive Triage

- The easiest hostile summary of H1 is: this is another multi-input self-powered startup/isolation paper tested on a convenient internal abstraction, and its own ablation already killed the original source-ranking mechanism.
- The current repo already forces H1 into a narrow posture:
  - the five-way primary matrix ties at `17/24`
  - `source_blind` beats the original RC-ranked champion on the falsifier suite (`10/10` vs `8/10`)
  - any broad "new architecture" or "best startup strategy" story is already dead on the repo's own evidence
- H1 survives only as a bounded same-family falsification result:
  - inside the executed helper-free model, explicit pre-handoff ranking is not needed once packetized isolation is present
- H2 is blocked first by model credibility, not novelty. Without a validated cryogenic compact-model path or collaborator-backed data, it is too easy to write and too hard to falsify.
- H3 is blocked first by prior-art overlap. If it drifts into generic impedance-aware loading or source-resistance estimation, recent variable-impedance harvester work makes it look derivative.

## H1 Immediate Kill Switches

### 1. Metric-contract drift can invalidate the benchmark as stated

- `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md` says `startup_ok` requires:
  - `V(n_store) >= V_HANDOFF`
  - an actual `n_handoff` enable event
  - no auxiliary source outside the declared two-source model
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/measurement_hooks.inc` implements:
  - `startup_ok = (vstore_final >= V_HANDOFF)`
  - `t_handoff`, `t_handoff_fall`, and `t_handoff_rise2` from `V(n_store)` crossings
  - `n_handoff` only as a latch to stop the pre-handoff integrals
- A hostile reviewer can therefore say the executed package does not actually measure the contract it claims to test.

### 2. The surviving positive story still lacks the control that would isolate it

- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/ablations/blind_packet_merge/blind_packet_merge.cir` exists.
- `results/verification/benchmark_report.md` says it is absent from the manifests and shared summary tables.
- Until a no-packet same-scaffold control is repaired and run, "packet-gated isolation is the load-bearing ingredient" is still an inference, not a demonstrated causal result.

### 3. The benchmark is still internal, not literature-faithful

- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/startup_cells.inc` uses an intentionally abstract `startup_pump`:
  - behavioral load and store current sources
  - `ETA_PUMP=3`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item011_signoff.md` already warns that claims must stay about arbitration/isolation behavior, not absolute converter efficiency.
- Any measured statement that sounds like a silicon or cross-paper performance claim can be attacked as an artifact of the abstraction rather than the circuit family.

### 4. The source and switch models are optimistic enough to hide the main failure modes

- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/source_pair_models.inc` is a two-source Thevenin model with one global `RAMP_MVPS`.
- `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/startup_cells.inc` uses idealized polarity-flipping routers and leakage abstractions:
  - `RLEAK_ROUTE=1e15`
  - no body-diode physics
  - no charge-injection model
- That is acceptable for internal mechanism screening, but weak evidence for any real anti-backdrive or warm-restart claim.

## H1 Easiest Rehash Accusations

### 1. "This is another weak-source cold-start paper"

- This accusation is valid against any claim about low-voltage startup difficulty, self-starting cold start, or startup integration in general.
- Existing overlap family in the repo:
  - `goppert2016startup70mv`
  - `das2017selfstarter`
  - `quintero2019cmosstartup`
  - `coustans2019coldstart60mv`
- `lu2024tegassist` further kills any hidden-helper or ultra-low-startup bragging if one source quietly acts as an assistant.
- Invalidated weak claims:
  - `lower startup voltage`
  - `novel weak-source cold start`
  - `better low-voltage startup circuit`

### 2. "This is another adaptive dual-source / mixed-polarity startup paper"

- This accusation is valid against any claim that "source-aware startup" or "mixed polarity" is itself the novelty moat.
- Existing overlap family in the repo:
  - `tang2018dualsource`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `alhawari2017polaritydetection`
- Invalidated weak claims:
  - `source-aware startup` as a headline novelty
  - `mixed polarity` as the differentiator
  - `polarity-tolerant cold start` as a new category

### 3. "This is another autonomous multi-input self-powered interface"

- This is the most dangerous rehash accusation for the current H1 framing.
- Existing overlap family in the repo:
  - `alghisi2017batteryless`
  - `li2022multiinputplatform`
  - `wang2023serialstack`
  - `chen2024collaborative`
  - `weng2024osece`
- Extra crowding already sitting in `sources.bib`:
  - `wang2021serialsshi`
  - `xia2022dualinductor`
  - `zheng2023sharedinductor`
- Review-level overlap is now real, not hypothetical:
  - `gogolou2025multisourcereview` already makes broad multi-source integration a reviewable topic rather than a sparse frontier
  - the repo's own citation audit also flags a 2025 comprehensive review of self-powered piezoelectric interface circuits
- Invalidated weak claims:
  - `new multi-input harvester interface`
  - `new general-purpose PMU`
  - `first helper-free multi-source cold-start interface`

### 4. "This is just reverse-current blocking / power-path isolation with a prettier story"

- This accusation becomes strong if the surviving mechanism claim reduces to "do not hard-join the sources before handoff."
- External adversarial search surfaced neighboring branches on reverse-current-blocking power switches and intermittent supply switching for energy-harvesting systems.
- If a simple back-to-back switch or ideal-diode-style baseline closes the gap under equal accounting, most of the remaining H1 positive story disappears.

## H1 Missing Controls

- No executed same-scaffold no-packet control.
  - `blind_packet_merge.cir` exists but is unrun in the shared summaries.
  - Worse, its `packet_scout_frontend.inc` uses ideal clock sources `VCLK_A` and `VCLK_B`, so it also needs accounting repair before it can be trusted as a control.

- No literature-faithful executed comparator.
  - The repo repeats this in `results/verification/benchmark_report.md`, `results/verification/verification_summary.md`, and `results/verification/novelty_report.md`.
  - Every prior-art comparison therefore remains structural or rhetorical, not measured.

- No simple reverse-isolation baseline.
  - The current benchmark compares against `fixed`, `nonaware`, and same-family selector variants.
  - It does not compare against the simplest plausible physical alternative:
    - a low-overhead reverse-current-blocking / back-to-back isolation path under the same measurement hooks

- No restart-safe fixed hysteretic baseline for repeated-collapse behavior.
  - The current package still centers on first successful handoff.
  - A reviewer can reasonably ask whether a plain fixed hysteretic path with stale-state scrub would match the claimed advantage once repeated collapse and partial-store memory are modeled.

- No factor-complete heterogeneous-input matrix.
  - The frozen source contract implies `4 x 4 x 3 x 2 = 96` cases.
  - The executed primary matrix is aliased to `24`.
  - The primary matrix also uses one global `RAMP_MVPS` and mostly equal `VOC_A = VOC_B`, so it cannot honestly be sold as a broad heterogeneous-source map.

- No device-faithful leakage/body-path control.
  - `source_pair_models.inc` and `startup_cells.inc` are too clean to settle anti-backdrive claims.
  - The current leak-path falsifier is a useful stress point, not a realistic parasitic envelope.

## H1 Benchmark Traps

- `startup_ok` is weaker in code than in the written spec.
  - This is the cleanest internal inconsistency a reviewer can weaponize.

- `t_handoff` and chatter metrics are still store-voltage proxies.
  - `results/verification/benchmark_report.md` already blocks strong handoff/chatter claims on this ground.
  - If `n_handoff` traces disagree with `V(n_store)` crossings on the decisive cases, the current narrative breaks.

- Back-drive reporting is thresholded without a documented noise-floor argument.
  - `tools/run_h1_falsifier.py` treats `e_backdrive_j > 1e-12` as "nonzero."
  - `results/verification/benchmark_report.md` notes that raw falsifier tables still contain positive values even where summary tables report zero nonzero cases.
  - A hostile reader can call the back-drive story numerically massaged.

- Zero primary-matrix back-drive is probably a modeling warning, not closure.
  - `results/verification/benchmark_report.md`, `results/swarm/gap_map.md`, and `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item011_signoff.md` all point in this direction.
  - If every design shows zero wrong-way energy in the broad matrix, the model may be too sanitized to resolve the advertised mechanism.

- The decisive falsifier cases are not all uncertainty-qualified.
  - Robustness reruns do not cover every separator case called out in the narrowed story.
  - That makes some of the remaining positive narrative one-off rather than interval-backed.

- Artifact-pack drift weakens trust.
  - `item018_benchmark_note.md` and `item019_falsifier_note.md` still reflect older interpretations.
  - `benchmark_report.md` is stricter than `final_research_brief.md`.
  - A reviewer can say the claim was narrowed after the fact and the notes were not fully synchronized.

## H1 Novelty Illusions

- `helper-free` is a guardrail, not a novelty moat.
- `mixed polarity` is a stress axis, not a differentiator.
- `multi-source` is already crowded and now review-level.
- `source-aware ranking` is the story the repo already killed.
- `minimal packet gating` is overstated.
  - `source_blind_packet_gate` in `packet_scout_blocks.inc` still instantiates the scout observation branches and uses the same `G_SCOUT_CTRL=40n` control term as the RC-ranked design.
  - The executed ablation removes ranking, not the broader scout scaffold.
- `the literature rarely closes the same-family ablation loop` is unproven.
  - `results/literature/gap_frontier.md` is effectively empty.
  - several exact anchor titles were not recovered
  - the safest defensible phrasing is only:
    - the recovered overlap set did not reveal a close same-family falsification study
- `packet-gated isolation is already causally isolated` is unproven until the missing control runs.
- `startup correctness under heterogeneous weak sources` is broader than the current model support.
  - most executed cases do not test independent ramp laws, late arrival, or richer source laws beyond linear Thevenin ramps plus collapse windows

## Literature Branches That Could Still Invalidate Weak Claims

- Multi-input self-powered piezo interface line beyond the current short list.
  - `wang2021serialsshi`
  - `xia2022dualinductor`
  - `zheng2023sharedinductor`
  - 2025 review-level piezo interface surveys
  - If these contain comparable isolation-before-selection behavior or same-family ablations, the gap sentence gets weaker fast.

- Reverse-current-blocking / power-supply-switch / ideal-diode literature for energy harvesting and intermittent systems.
  - If the practical win is mainly "block wrong-way current without hard joining," the right comparator may come from power-path management rather than from multi-input harvester papers.
  - External adversarial search surfaced recent power-supply-switch and reverse-current-blocking branches close enough to matter.

- Brownout / repeated-collapse / restart-safe intermittent-power literature.
  - The current package mostly studies first handoff.
  - If restart correctness is already handled by known intermittent power-path or supervisor techniques, the next H1 extension collapses to engineering cleanup rather than a new finding.

- More realistic heterogeneous-source laws.
  - If a late-arriving or dynamically impedance-shifting source breaks the current conclusion, the paper is only about the two-source linear-Thevenin abstraction, not about multi-source cold start in practice.

## H1 Explicit Kill Rules

- Kill any claim that packet-gated isolation is the validated positive mechanism unless `blind_packet_merge` is repaired, executed, and still loses.
- Kill any field-level novelty sentence if one literature-faithful comparator from the `alghisi` / `li` / `wang` / `chen` / `weng` family matches the same separator cases.
- Kill any handoff or chatter claim if explicit `n_handoff` event traces disagree with the current store-threshold proxy on the decisive cases.
- Kill any anti-backdrive claim if realistic parasitics or a simpler back-to-back isolation path remove the measured separation.
- Kill any broad heterogeneous-source rhetoric if independent ramp, late arrival, unequal-`VOC`, and repeated-collapse cases are handled just as well by `source_blind` or a fixed hysteretic path.
- Kill the "rarely represented in the literature" sentence unless a real gap search finds better absence evidence than the current empty `gap_frontier.md`.

## H2 Brief Kill Note

- H2 fails immediately if there is no validated cryogenic model path or collaborator-backed device data.
- Even with a model path, it will look derivative if framed as another low-power cryogenic reference or comparator.
- External adversarial search confirmed that recent cryo-CMOS comparator, cryogenic reference, and low-frequency-noise papers already crowd that generic framing.
- Allowed posture at most:
  - sub-10 K uncertainty tolerance as the test target
- Kill posture:
  - generic cryo support block novelty

## H3 Brief Kill Note

- H3 fails if it reduces to "estimate source resistance and retune."
- The repo's own `results/swarm/hypothesis_bridge.md` already flags direct overlap with:
  - `A Variable Impedance and Voltage Converter for Efficiently Harvesting Energy from Time-Varying Power Sources with Varying Internal Resistance` (2025)
  - `Adaptable interface conditioning circuit for power harvesting from triboelectric nanogenerator` (2019)
  - `Impedance spectroscopy analysis of thermoelectric modules under actual energy harvesting operating conditions and a small temperature difference` (2024)
- External adversarial search supports the repo's warning:
  - variable-impedance and source-identification language is active enough that generic `impedance-aware MPPT` framing will read as a rehash
- Allowed posture at most:
  - a narrowly budgeted identification/control result with explicit probe-energy accounting
- Kill posture:
  - generic dynamic-source-impedance harvesting claim

## Bottom Line

- The easiest hostile conclusion is not "H1 is false."
- It is:
  - H1 is only a narrow same-family negative result, and every broader novelty sentence can be collapsed either by existing prior art or by the benchmark's missing controls.
- The safest surviving sentence remains:
  - in the executed helper-free model, explicit pre-handoff ranking is unnecessary inside the packet-gated family
- Everything broader than that is exposed.
