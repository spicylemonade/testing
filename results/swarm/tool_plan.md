# Tool Plan

## Routing Decision

- Active champion lane: **H1_multisource_cold_start**.
- Conditional backup lane: **H2_cryo_support_blocks**.
- Reserve lane: **H3_dynamic_source_impedance** only if H1 is killed early and H2 is blocked on cryogenic model access.
- Global governance rule: do not re-run broad searches. Only spend targeted literature budget when a blocker or direct-overlap question appears.
- Global blocker: `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md` are missing. Repair that traceability gap with a narrow claim matrix before heavy execution.

## Phase Budget

- **Phase A: Champion go/kill gate**
  - Envelope: `~40 hours` total.
  - Goal: decide whether H1 survives direct-overlap checking and one first ngspice evidence matrix.
- **Phase B: Backup activation gate**
  - Envelope: `~24 hours` total, only if H1 survives but stalls or if H1 is killed after the prior-art gate.
  - Goal: decide whether H2 has a credible model-backed path.
- **Phase C: Reserve activation**
  - Envelope: `~16 hours` total, only if H1 is killed and H2 is blocked on models.
  - Goal: decide whether H3 still clears the 2025 overlap risk.

## Role Routing

### Orchestrator

- Tools:
  - repo reads via shell
  - targeted literature lookup only if a blocker is triggered
  - no broad search sweeps
- Budget envelope:
  - `4h` in Phase A
  - `<=6` narrow queries per active lane
  - `0` experiments
- Responsibilities:
  - freeze the active claim, baselines, metrics, and kill rule before execution starts
  - stop any lane that drifts into generic MPPT, generic cryo references, or other cosmetic novelty

### Researcher

- Tools:
  - `ngspice`
  - existing helper scripts already in the repo
  - shell inspection tools
  - no ILP/LP/theorem-search detours
- Budget envelope:
  - H1: `20h`, one topology family, `<=24` startup cases, `2` strong baselines
  - H2: `12h`, only after the cryogenic model gate passes, one macro-concept, `<=12` widened corners
  - H3: `10h`, only if promoted from reserve, one interface concept, `<=18` cases
- Responsibilities:
  - H1: test startup correctness, handoff, anti-backdrive loss, and control energy under heterogeneous weak-source stress
  - H2: test monotonicity, power, and calibration stability under widened cryogenic uncertainty
  - H3: test net delivered energy and sensor uptime after probe overhead, not raw peak efficiency

### Falsifier

- Tools:
  - targeted prior-art checks
  - adversarial benchmark review
  - repo note review
- Budget envelope:
  - `8h` for H1
  - `4h` for H2 or H3 if activated
  - `<=8` papers per active lane
- Responsibilities:
  - find the direct-overlap paper that would kill the claim fastest
  - reject weak baselines, hidden-state leakage, and uncounted overhead
  - block any result that wins only against fixed, open-loop, or one-feature baselines

### Writer

- Tools:
  - markdown only
  - existing notes and approved result tables
- Budget envelope:
  - `4h` after a lane clears its go/kill gate
  - no expansion of scope
- Responsibilities:
  - write only the champion or activated backup story
  - keep the narrative tied to the actual failure mode, evidence matrix, and kill-rule outcome

### Reviewer

- Tools:
  - shell diff inspection
  - result-table sanity checks
- Budget envelope:
  - `4h` per drafted lane
- Responsibilities:
  - review for claim inflation, missing controls, and contradictions between summary and evidence
  - send the work back if the contribution statement drifts broader than the validated result

### Citation Auditor

- Tools:
  - source-to-claim cross-check
  - bibliography completeness checks
- Budget envelope:
  - `3h` per active lane
  - `<=12` audited claims per lane
- Responsibilities:
  - verify that every novelty, overlap, and benchmark statement maps to an actual source
  - block unsupported wording such as "first", "novel", or "under-served" unless the source matrix justifies it

### Benchmark Auditor

- Tools:
  - benchmark checklist review
  - metrics and baseline audit
- Budget envelope:
  - `6h` for H1
  - `4h` for H2 or H3 if activated
- Responsibilities:
  - approve the baseline set before large sweeps start
  - ensure H1 is compared against strong startup/arbitration baselines with equal overhead accounting
  - ensure H2 is tested across widened cryogenic uncertainty rather than nominal corners only
  - ensure H3 includes probing overhead and avoids fixed-Thevenin-only source families

## Lane-Specific Kill Rules

- **H1_multisource_cold_start**
  - Kill if helper-free multi-source cold start with source-aware arbitration is already substantially covered by prior art.
  - Kill if arbitration or anti-backdrive overhead erases the startup-correctness gain.
- **H2_cryo_support_blocks**
  - Kill if no credible cryogenic model path exists.
  - Kill if the concept fails under widened low-frequency-noise, mismatch, and threshold-shift assumptions.
- **H3_dynamic_source_impedance**
  - Kill if the 2025 variable-impedance overlap collapses the novelty margin.
  - Kill if a simple hysteretic baseline matches the result once probe overhead is counted.

## Exit Rule

- Do not advance a lane beyond its first gate unless the falsifier, benchmark auditor, and citation auditor all clear it.
- If no lane clears the gate, stop and report the blocker rather than broadening the search.
