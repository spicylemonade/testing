# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## 1. Leading change (2018)
- Paper ID: 789ba356e469b65f4a2743925a5e725b27cc61d6
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It is not technically close. It only appeared because the original seed query used generic words like `new`, `interesting`, and `important`.
- Differentiation hypothesis:
  - The H1 lane is a circuit-level cold-start interface problem in weak multi-source energy harvesting, not an organizational-change or leadership paper.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 section.
  - `results/research_context.md` repo-reality note on the polluted seed watchlist.
- Pivot decision (if any):
  - Keep as an explicit false-neighbor watchlist item only; do not use it to guide technical novelty.

## 2. Fostering STEAM through challenge-based learning, robotics, and physical devices: A systematic mapping literature review (2020)
- Paper ID: bb5f0ca5ea0f4ec1d056bd26d6e931939923bb38
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It is not close to the active circuit thesis. It only overlaps the vague seed-query language and the word `engineering`.
- Differentiation hypothesis:
  - The research contribution here is an analog/power-management architecture and `ngspice` evidence package, not an education or robotics pedagogy review.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 section.
  - `results/swarm/gap_map.md` ranked-gap rationale.
- Pivot decision (if any):
  - Keep as a negative control showing why the seed-watchlist needed repair.

## 3. Artificial Intelligence, Cognitive Robotics and Nature of Consciousness (2022)
- Paper ID: 9484853109ff9e699f37deebeb99d9e39221868d
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It is another false-neighbor artifact from the original broad query and has no direct relation to weak-source cold start or multi-input power interfaces.
- Differentiation hypothesis:
  - H1 is a constrained mixed-source startup problem with measurable analog metrics; there is no AI or consciousness claim in the active lane.
- Evidence artifact(s):
  - `results/research_context.md` module inventory and lane freeze.
  - `results/literature/literature_snapshot.json` focused H1 paper set.
- Pivot decision (if any):
  - Explicitly deprioritized. No overlap beyond bootstrap noise.

## 4. The north wing of the Musin-Pushkin estate in Moscow: historical, architectural and field studies (2022)
- Paper ID: 046229ca8e89c0b6e71c8fdcfcaa9a45914693df
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It is not technically close. It entered through generic terms like `something new` and `interesting`.
- Differentiation hypothesis:
  - H1 is a low-voltage energy-harvesting interface problem; this paper is architectural heritage research.
- Evidence artifact(s):
  - `results/research_context.md` repo-reality note on polluted watchlist.
  - `results/literature/literature_snapshot.json` focused H1 section.
- Pivot decision (if any):
  - Kept only because the rubric asks for an explicit differentiation note.

## 5. Sign To Speech Conversion And Home Automation Control Using Smart Gloves (2024)
- Paper ID: 98075209e5cc71b2ea93039d439127b984d9c0e9
- Dated differentiation note: 2026-03-12
- Why it is close:
  - Another false-neighbor from generic task language; not an overlap risk for the H1 circuit thesis.
- Differentiation hypothesis:
  - H1 is about source-aware cold-start sequencing and anti-backdrive in analog power interfaces, not gesture sensing or home automation.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 section.
- Pivot decision (if any):
  - No technical overlap. Keep only as a watchlist cleanup record.

## 6. Decentralized Interleaving of Parallel-connected Buck Converters (2019)
- Why it is close:
  - This line of work already uses decentralized coupled oscillators to control phase relationships among parallel buck cells, which substantially overlaps any generic `firefly` or `quorum-sensing` pitch for multiphase converter synchronization.
- Differentiation hypothesis:
  - The only version that may still survive is an explicitly spectral controller that keeps the converter near cluster synchrony on purpose to flatten EMI peaks under changing loads, rather than simply achieving stable interleaving.
- Evidence artifact(s):
  - `Decentralized Interleaving of Parallel-connected Buck Converters`.
  - `A Distributed Phase Management Scheme for Interleaved Buck Converters`.
- Pivot decision (if any):
  - Pivoted away from oscillator-based interleaving as a headline bridge hypothesis because the novelty margin looked weak relative to existing coupled-oscillator converter control.

## 7. Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting (2016)
- Paper ID: c75c82be2e98a8d66907742a89b886902c1a0162
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It is a canonical low-voltage TEG cold-start paper and therefore one of the most direct overlaps on the startup side of H1.
- Differentiation hypothesis:
  - H1 must stay explicitly on *heterogeneous multi-source* startup correctness, mixed polarity/impedance stress, and anti-backdrive accounting before normal arbitration is alive. A single-source low-voltage TEG startup result is not enough to kill H1 by itself, but it kills any claim framed as merely `lower startup voltage`.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `goppert2016startup70mv`.
- Pivot decision (if any):
  - Do not claim novelty on absolute startup voltage or generic integrated startup alone.

## 8. A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems (2019)
- Paper ID: d9415d1253fb75da110cffc9d1ab87509010d30e
- Dated differentiation note: 2026-03-12
- Why it is close:
  - Another direct overlap on fully integrated startup circuitry for weak thermoelectric sources.
- Differentiation hypothesis:
  - H1 must differentiate on source heterogeneity, arbitration sequencing, and preventing one weak source from back-driving another during startup.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `quintero2019cmosstartup`.
- Pivot decision (if any):
  - Treat as a startup-baseline anchor, not a novelty target.

## 9. Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems (2017)
- Paper ID: 9fd5e15b325f8534ee928242f7e9507a01586677
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It directly addresses single- and multi-source battery-less PMUs for piezoelectric harvesting, which makes it a strong baseline/overlap paper on the multi-input side.
- Differentiation hypothesis:
  - H1 cannot rely on `multi-source` as the differentiator. It must instead show source-aware *cold-start sequencing* under mixed voltage/ramp/polarity/impedance conditions before full PMU arbitration is alive.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `alghisi2017batteryless`.
- Pivot decision (if any):
  - Keep as a required claim-matrix comparator. Any generic multi-input PMU framing is too close.

## 10. Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting (2023)
- Paper ID: 254a50d3d11f95e13c87d5b068a92e29fb0f2dee
- Dated differentiation note: 2026-03-12
- Why it is close:
  - Strong recent multi-source interface work. It explicitly improves over TDM/DCM multi-source extraction, making it one of the sharpest overlap threats for any generalized `better multi-source harvester interface` story.
- Differentiation hypothesis:
  - H1 survives only if it is framed as a *pre-arbitration startup* problem with weak-source mixed-polarity stress, not as a steady-state extraction-efficiency improvement.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `wang2023serialstack`.
- Pivot decision (if any):
  - Do not claim better steady-state multi-source extraction as the main story.

## 11. Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (2024)
- Paper ID: 0fd827923bda6369f44527bd52fdf7b4c60e4941
- Dated differentiation note: 2026-03-12
- Why it is close:
  - This is one of the closest recent `self-powered` and `multi-input` piezoelectric interface papers and is therefore a direct threat to any weakly stated H1 novelty claim.
- Differentiation hypothesis:
  - H1 must show a materially different operating regime: mixed low-voltage source types, impedance asymmetry, polarity mismatch, and explicit anti-backdrive/UVLO-chatter handling during cold start.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `chen2024collaborative`.
- Pivot decision (if any):
  - Treat as a direct overlap screen. If the champion architecture reduces to another self-powered multi-input piezo interface, narrow or kill the claim.

## 12. A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers (2024)
- Paper ID: 6022e53796c25cba2130c9505c6e6c908fd43cb0
- Dated differentiation note: 2026-03-12
- Why it is close:
  - Recent multi-input self-powered interface work close to the saved swarm anchor `Fully Autonomous Self-Starting Interface Circuit for Piezoelectric Energy Harvesting from Multi-Source Inputs (2024)`.
- Differentiation hypothesis:
  - H1 must distinguish itself through startup sequencing logic that adapts to heterogeneous sources before the main extraction path turns on, not merely by proposing another self-powered multi-input piezo interface.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` required-anchor resolution table.
  - `sources.bib` entry `weng2024osece`.
- Pivot decision (if any):
  - Keep as a named direct-overlap paper in the later claim matrix.

## 13. Multi-Source Energy Harvesting Systems Integrated in Silicon: A Comprehensive Review (2025)
- Paper ID: 6461dab6cdfcd007d17f484bb2f28744f7b08c1c
- Dated differentiation note: 2026-03-12
- Why it is close:
  - This is the closest recovered review to the saved anchor `Power Management for Multi-Source Energy Harvesting Systems: A Review (2024)`.
- Differentiation hypothesis:
  - H1 must differentiate on a narrow failure mode that the review leaves unresolved: correct helper-free startup and handoff under heterogeneous weak-source conditions, with arbitration and anti-backdrive overhead counted.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` required-anchor resolution table.
  - `sources.bib` entry `gogolou2025multisourcereview`.
- Pivot decision (if any):
  - Use as the closest review-level overlap screen until an exact 2024 title match is independently verified.

## 14. A Thermoelectric Energy Harvesting System Assisted by a Piezoelectric Transducer Achieving 10-MV Cold-Startup and 82.7% Peak Efficiency (2024)
- Paper ID: dfecac253dbefc0807d87edafe69873b2a45bfc1
- Dated differentiation note: 2026-03-12
- Why it is close:
  - It directly attacks extremely low-voltage cold startup, but does so by using a piezoelectric transducer as a helper source.
- Differentiation hypothesis:
  - H1 should remain helper-free and source-aware during startup. If the proposed architecture quietly depends on one source to act as a helper rail, this paper narrows the novelty margin quickly.
- Evidence artifact(s):
  - `results/literature/literature_snapshot.json` focused H1 paper set.
  - `sources.bib` entry `lu2024tegassist`.
- Pivot decision (if any):
  - Keep as a falsifier for hidden-helper behavior.

## 15. H1 Claim-Matrix Consolidation (2026-03-12)
- Why it matters:
  - The saved swarm state required a narrow claim matrix before heavy execution because the original anchor set included unresolved surrogate titles and one direct-overlap family of 2023-2024 multi-input interfaces.
- Consolidated decision:
  - The H1 lane survives only as a helper-free, pre-arbitration startup-sequencing thesis under mixed polarity and impedance asymmetry.
- Evidence artifact(s):
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/experiment_spec.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/shared/packet_scout_blocks.inc`
- Pivot decision (if any):
  - Downgrade all claims about absolute startup voltage, generic multi-source PMU novelty, and steady-state extraction efficiency until the experiment matrix shows a real startup-correctness advantage against both baselines.
