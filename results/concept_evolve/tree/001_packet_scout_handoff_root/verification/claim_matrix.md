# H1 Claim Matrix

Date: 2026-03-12
Scope: explicit novelty and overlap screen for the H1 champion before widening experimental claims
Status: PASS with narrowed claim boundary

## Champion Under Review

- Topology:
  - `netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Mechanism summary:
  - helper-free two-source cold start
  - full-wave branch routing into a common front end
  - RC scout packets observe branch recovery
  - a tanh-ranked selector admits only one branch into the startup pump before handoff
- Key evidence artifacts:
  - `experiment_spec.md`
  - `netlists/shared/packet_scout_blocks.inc`
  - `netlists/shared/startup_cells.inc`
  - `verification/item011_signoff.md`

## Allowed Claim Boundary

- Allowed now:
  - the H1 champion is structurally different from generic single-source TEG startup paths and generic multi-input steady-state interfaces because it freezes attention on helper-free, pre-arbitration source selection under mixed polarity and impedance stress
  - the current evidence supports a design-level distinction around startup sequencing and accounting discipline
- Not allowed yet:
  - any `first`, `novel`, or `best` claim
  - any claim about absolute minimum startup voltage
  - any claim about steady-state extraction efficiency
  - any claim that the RC-ranked path already beats the closest 2023-2024 multi-input self-powered interfaces on measured performance

## Required Anchor Resolution Note

- `Review of Fully Integrated Startup Techniques for Thermoelectric Energy Harvesting Systems (2023)`:
  - not recovered exactly
  - use the recovered TEG startup family as the actual overlap evidence:
    - `goppert2016startup70mv`
    - `quintero2019cmosstartup`
    - `coustans2019coldstart60mv`
- `Power Management for Multi-Source Energy Harvesting Systems: A Review (2024)`:
  - exact title not recovered
  - use `gogolou2025multisourcereview` plus primary multi-source PMU papers as the actual overlap evidence
- `Fully Autonomous Self-Starting Interface Circuit for Piezoelectric Energy Harvesting from Multi-Source Inputs (2024)`:
  - exact title not recovered
  - use the closest recovered 2024 family:
    - `weng2024osece`
    - `chen2024collaborative`
    - `wang2023serialstack`

## Comparator Matrix

| Comparator | Why it is close | Candidate H1 difference | Evidence link(s) | Status |
| --- | --- | --- | --- | --- |
| Requested 2023 TEG startup review, screened through `goppert2016startup70mv` and `quintero2019cmosstartup` | Strong overlap on cold-start circuits for very weak sources | H1 is not another single-source low-voltage startup claim; it is a two-source helper-free startup sequencing problem with explicit mixed-polarity and impedance-asymmetry stress before arbitration turns on | `experiment_spec.md`; `netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/README.md`; `netlists/shared/packet_scout_blocks.inc` | Supported as a design-scope difference only. Any claim about lower startup voltage is downgraded and disallowed. |
| `gogolou2025multisourcereview` as the closest recovered review for the missing 2024 multi-source PMU review | Strong overlap on multi-source harvesting architectures and integration tradeoffs | H1 narrows the problem to pre-arbitration correctness under heterogeneous weak sources; it does not claim a better general multi-source PMU or a broader integration survey result | `experiment_spec.md`; `verification/item011_signoff.md`; `results/literature/prior_art_gap.md` | Supported as a framing difference. Broader PMU novelty wording is downgraded. |
| `alghisi2017batteryless` | Direct overlap on single- and multi-source battery-less PMUs for piezo harvesters | H1 only survives if source awareness is needed during cold start itself, not merely after a multi-input PMU already has energy to arbitrate | `experiment_spec.md`; `netlists/baselines/nonaware_multi_input_startup/nonaware_multi_input_startup.cir`; `netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir` | Supported as a benchmark distinction. Performance superiority remains unproven until the matrix runs. |
| `wang2023serialstack` | Very close recent multi-source interface work with explicit efficiency framing | H1 is intentionally not an extraction-efficiency story; it ranks branches before handoff instead of claiming better steady-state synchronous extraction | `netlists/shared/packet_scout_blocks.inc`; `verification/item011_signoff.md`; `results/literature/prior_art_gap.md` | Supported as a problem-definition difference. Any efficiency headline is downgraded and disallowed. |
| `weng2024osece` | Direct overlap family for self-powered multi-input startup interfaces | H1 differs structurally by using scout-packet ranking between two floating Thevenin sources before releasing handoff, rather than presenting another self-powered multi-input piezo extraction interface | `netlists/shared/packet_scout_blocks.inc`; `netlists/shared/startup_cells.inc`; `experiment_spec.md` | Supported structurally. Measured advantage over OSECE-like families is not yet established. |
| `chen2024collaborative` | Direct overlap family for recent self-powered collaborative multi-input interfaces | H1 adds explicit mixed-polarity and impedance-asymmetry stress plus equalized control-energy accounting, which the current repo artifacts treat as primary evaluation targets | `experiment_spec.md`; `verification/item011_signoff.md`; `netlists/shared/measurement_hooks.inc` | Supported as an evaluation-boundary difference. Any claim of broader applicability is downgraded. |
| `lu2024tegassist` | Close on very-low-voltage cold start | H1 must remain helper-free; it cannot quietly use one source as an unstated helper rail | `experiment_spec.md`; `netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`; `netlists/baselines/fixed_startup_path/fixed_startup_path.cir` | Supported. No helper rail exists in the current champion or baseline decks. |

## Watchlist False-Neighbor Screen

| Watchlist paper | Overlap result | Evidence link(s) | Status |
| --- | --- | --- | --- |
| `Leading change (2018)` | Not a technical overlap. The seed query pulled it in through generic words such as `new` and `interesting`. | `results/literature/prior_art_gap.md`; `results/research_context.md` | Closed as a false neighbor. |
| `Fostering STEAM through challenge-based learning, robotics, and physical devices` (2020) | Education and pedagogy review, not a startup-interface paper. | `results/literature/prior_art_gap.md`; `results/literature/literature_snapshot.json` | Closed as a false neighbor. |
| `Artificial Intelligence, Cognitive Robotics and Nature of Consciousness` (2022) | No circuit-level overlap with weak-source cold-start interfaces. | `results/literature/prior_art_gap.md`; `results/research_context.md` | Closed as a false neighbor. |
| `The north wing of the Musin-Pushkin estate in Moscow` (2022) | Architectural heritage research, not power electronics. | `results/literature/prior_art_gap.md`; `results/literature/literature_snapshot.json` | Closed as a false neighbor. |
| `Sign To Speech Conversion And Home Automation Control Using Smart Gloves` (2024) | Gesture and automation system paper, not an energy-harvesting startup interface. | `results/literature/prior_art_gap.md` | Closed as a false neighbor. |

## Claims Downgraded Or Deferred

- Downgraded now:
  - `lower startup voltage than prior work`
  - `better multi-source harvesting efficiency`
  - `new general-purpose multi-input PMU`
  - `first helper-free multi-source cold-start interface`
- Deferred until items 017-021 complete:
  - `lower back-drive loss than non-source-aware startup`
  - `faster or more reliable handoff under mixed polarity and impedance asymmetry`
  - `better startup-correctness trade than the fixed and nonaware baselines under equal control-energy accounting`

## Gate Decision

- The H1 lane survives the novelty screen only as a narrow claim:
  - source-aware pre-arbitration startup sequencing for heterogeneous weak sources with helper-free accounting
- If the upcoming experiment matrix does not show a clean advantage on `startup_ok`, `t_handoff`, or `e_backdrive` against both baselines, the contribution must be narrowed again or killed.
