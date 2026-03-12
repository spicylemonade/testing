# H1 Novelty Check

Date: 2026-03-12
Lane: `H1_multisource_cold_start`

Scope: this note uses only saved repo context, not a new literature sweep. The evidence base is `research_rubric.json`, `results/research_context.md`, `results/literature/literature_snapshot.json`, `results/literature/prior_art_gap.md`, `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, `results/swarm/falsifier.md`, `results/concept_evolve/tree/index.json`, `results/concept_evolve/concept_cards.json`, and `results/concept_evolve/integrator_selection.md`.

Canonical angle set: use the six concepts in `results/concept_evolve/tree/index.json`. Earlier disconnected scout aliases are superseded here.

## Closest overlap clusters

- Startup-side overlap: `Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting` (2016), `A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems` (2019), `A 220-mV Power-on-Reset Based Self-Starter With 2-nW Quiescent Power for Thermoelectric Energy Harvesting Systems` (2017), and `A fully integrated 28nm CMOS dual source adaptive thermoelectric and RF energy harvesting circuit with 110mV startup voltage` (2018). These kill any claim that is only about lower startup voltage, integrated startup, or generic dual-source adaptation.
- Multi-input overlap: `Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems` (2017), `Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting` (2023), `Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements` (2024), and `A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers` (2024). These kill any claim that is only about self-powered multi-input harvesting, anti-backdrive, or steady-state extraction after startup.
- Hidden-helper falsifier: `A Thermoelectric Energy Harvesting System Assisted by a Piezoelectric Transducer Achieving 10-MV Cold-Startup and 82.7% Peak Efficiency` (2024). Any H1 angle that quietly lets one source behave like a helper rail loses differentiation quickly.

## Summary verdict

- Keep as the only headline-worthy H1 angle: `001_packet_scout_handoff_root`
- Keep as a narrow fallback if mixed-polarity startup is the real unresolved regime: `002_dual_bucket_polarity_split_bootstrap`
- Keep only as an ablation or low-overhead comparator line: `003_time_constant_ranked_arbiter`
- Keep only as supporting sub-blocks, not thesis-level contributions: `004_reverse_leakage_vote_or`, `005_tokenized_uvlo_handoff_gate`
- Merge into the packet-scout family or retire as a separate angle: `006_comparatorless_current_probe_bootstrap`

## Per-angle assessment

### `packet_scout_handoff_root`

- Novelty call: still novel enough to lead H1, but only with a medium margin.
- Why it survives: it is the only angle that preserves the director-brief thesis intact: helper-free pre-arbitration source scouting under heterogeneous polarity, impedance, and ramp conditions before the main arbiter is alive.
- Closest startup overlap: `Fully Integrated Startup at 70 mV...` (2016) and the 2018 dual-source adaptive TEG+RF starter already cover low-voltage and adaptive startup framing.
- Closest multi-input overlap: `Configurable Hybrid Energy Synchronous Extraction...` (2023) plus the 2024 collaborative and OSECE families already cover strong self-powered multi-input interfaces.
- Weak differentiation:
  - If `packet scouting` reduces to ordinary priority OR-ing or threshold selection, the overlap with the 2018 dual-source adaptive startup paper and 2017 multi-source PMU paper becomes too strong.
  - If the experiments omit mixed-polarity cases or extreme impedance asymmetry, the concept reads like another multi-input self-powered interface.
- Collapse modes:
  - Probe energy, mirror mismatch, or sequencing delay erases the startup-correctness gain.
  - Precharged probe nodes or latches create hidden-helper behavior.
  - Equal-overhead fixed-path or non-aware OR-ing baselines match startup success and handoff time.
  - Anti-backdrive benefit disappears once realistic leakage and ultra-slow-ramp cases are included.

### `dual_bucket_polarity_split_bootstrap`

- Novelty call: still defensible only as a narrow fallback.
- Why it survives: it keeps a specific unresolved failure mode alive, namely mixed-polarity or reverse-suspect sources during cold start before the interface can safely merge rails.
- Closest startup overlap: the 2018 dual-source adaptive TEG+RF paper and the 2024 piezo-assisted TEG cold-start paper narrow the room for any claim that secretly relies on one source helping another.
- Closest multi-input overlap: the 2024 OSECE and collaborative piezo papers are already close to `self-powered multi-input startup`.
- Weak differentiation:
  - If the source set is rectified to one polarity before startup, the polarity-split story becomes unnecessary.
  - If one startup bucket effectively acts as a helper reservoir, the concept collapses toward the 2024 assisted-startup family.
- Collapse modes:
  - Extra bucket capacitance, merge clamps, and latch overhead dominate under the weakest ramps.
  - Leakage between the two buckets erases the claimed polarity safety.
  - A simple rectifier or ideal-diode baseline removes the mixed-polarity advantage.
  - Merge control chatters or creates half-on isolation states that nullify the startup win.

### `time_constant_ranked_arbiter`

- Novelty call: not strong enough as a standalone thesis; keep it as an ablation or low-overhead fallback only.
- Why it survives at all: it offers a clean low-complexity comparison against full source-aware scouting.
- Closest startup overlap: the 2018 dual-source adaptive TEG+RF starter already narrows claims about `adaptive` startup source selection.
- Closest multi-input overlap: `Single- and multi-source battery-less...` (2017) and `Configurable Hybrid Energy Synchronous Extraction...` (2023) already cover multi-input management and arbitration territory.
- Weak differentiation:
  - `RC ranking` is too close to ordinary arbitration unless its control-energy cost is materially lower than explicit comparators or active ranking.
  - If tested only in equal-polarity cases, it loses the main H1 differentiator.
- Collapse modes:
  - Under ultra-slow ramps the fast and slow signatures collapse together.
  - Switch, latch, and timing overhead approach the cost of an ordinary comparator path.
  - Ranking errors do not improve startup success or handoff time relative to strong baselines.
  - The packet-scout root or even a fixed startup path matches the result under equal accounting.

### `reverse_leakage_vote_or`

- Novelty call: not novel enough as a headline contribution; keep only as a possible sub-block.
- Why it is weak: anti-backdrive is already expected in multi-input interfaces, so the claim would rest almost entirely on a fragile implementation detail: using leakage as the direction sensor.
- Closest startup overlap: startup OR-ing and wrong-way-current suppression are already implicit in the startup/control literature, even if not presented with this exact sensing mechanism.
- Closest multi-input overlap: the 2024 collaborative and OSECE interface papers are the nearest overlap because they already live in self-powered multi-input isolation territory.
- Weak differentiation:
  - Leakage voting can easily look like a process-sensitive circuit trick rather than a materially different architecture.
  - If it only trims reverse current a little, it does not support the H1 thesis around startup correctness.
- Collapse modes:
  - Leakage signatures flip with process, temperature, or source amplitude.
  - The vote needs too many windows or too much calibration to stay useful at cold start.
  - A simple ideal-diode or latched OR-ing path matches the benefit.
  - Wrong-way current suppression does not translate into better startup success or handoff.

### `tokenized_uvlo_handoff_gate`

- Novelty call: collapses as a standalone angle; keep only as a support block if needed.
- Why it is weak: the closest startup papers already cover self-starter and startup-control overhead. A token chain is not a defensible thesis unless it unlocks a distinctly multi-source failure case.
- Closest startup overlap: `A 220-mV Power-on-Reset Based Self-Starter...` (2017) and `A CMOS Startup Circuit...` (2019).
- Closest multi-input overlap: weak direct overlap, which is itself a problem because the concept is not inherently multi-source-specific.
- Weak differentiation:
  - As a headline, this reads like a refined POR or UVLO deglitcher.
  - It only matters if tied to the H1 handoff hazard after source scouting.
- Collapse modes:
  - The token chain behaves like another hidden control rail.
  - Ordinary hysteresis or a conventional POR block achieves the same chatter suppression.
  - It reduces chatter but does not improve startup correctness in mixed-source cases.
  - The quiescent or pulse energy budget becomes comparable to the startup-control baselines.

### `comparatorless_current_probe_bootstrap`

- Novelty call: too weak as a separate angle; merge it into `packet_scout_handoff_root` unless it clearly wins on overhead.
- Why it survives at all: it is the lowest-overhead implementation hypothesis for source scouting, not a separate thesis.
- Closest startup overlap: `Fully Integrated Startup at 70 mV...` (2016) and the 2018 dual-source adaptive TEG+RF starter already narrow any broad `adaptive startup` claim.
- Closest multi-input overlap: `Single- and multi-source battery-less...` (2017) remains the nearest generic multi-source PMU threat.
- Weak differentiation:
  - Without a clear control-energy advantage, it is just another source-probing variant inside the packet-scout family.
  - If it needs explicit precharge, sense amplification, or hidden bias, the helper-free claim weakens immediately.
- Collapse modes:
  - Capacitor mismatch and injected charge loss corrupt the probe estimate.
  - The probe perturbs the weak source more than it informs the decision.
  - It fails to beat the RC ranker on startup benefit per control energy.
  - The full packet-scout root absorbs it as an implementation detail rather than a new concept angle.
