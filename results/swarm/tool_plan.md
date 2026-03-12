# Tool Plan

## Active Routing

- Champion: `H1_confidence_gated_abstention`
- Backup: `H1_restart_scrub_handoff`
- Parked third: `H1_reverse_port_sentinel`
- Parked bridge lanes: spread-spectrum admittance probing, cryogenic sequential-evidence support blocks, and high-temperature pilot-tone estimation
- Governance:
  - stay inside `H1_multisource_cold_start` until the champion and backup clear or fail their kill gates
  - do not reopen broad literature search, generic MPPT work, or fresh architecture families
  - keep one experimental lane active at a time

## Orchestrator

- Tool routing:
  - shell repo reads
  - existing manifests, notes, and tables
  - targeted literature lookup only when a named blocker triggers it
- Budget envelope:
  - `<=2h` synthesis and setup per gate decision
  - `<=6` targeted queries or papers per active lane
  - `0` experiments
- Responsibilities:
  - freeze the claim, baselines, metrics, and kill rule before any run
  - keep the champion active and the other lanes parked unless a formal kill or saturation decision is recorded
  - resolve the `startup_ok` metric contract before any lane is promoted out of experiment mode
  - stop any draft that drifts into generic startup, generic PMU, or generic anti-backdrive novelty

## Researcher

- Tool routing:
  - `ngspice`
  - existing H1 netlists and helper scripts
  - shell inspection
- Budget envelope:
  - champion: `<=12h`, `<=16` near-tie cases, `<=1` added confidence mechanism, `3` compared designs
  - backup: `<=10h`, `<=12` repeated-collapse cases, `<=1` restart-scrub controller, `3` compared designs, only if activated
  - parked third: `<=8h`, `<=12` parasitic cases, `<=1` sentinel variant, `3` compared designs, only if activated
- Responsibilities:
  - reuse the existing packet-gated scaffold instead of starting a fresh PMU architecture
  - maintain equal pre-handoff accounting across all compared designs
  - stop when the pre-registered kill rule trips instead of widening the matrix

## Falsifier

- Tool routing:
  - adversarial repo review
  - targeted overlap lookup
  - benchmark and verification note review
- Budget envelope:
  - champion: `<=4h`, `<=6` targeted papers or review sections
  - backup: `<=3h`, `<=6` targeted papers or review sections, only if activated
  - parked third: `<=3h`, `<=6` targeted papers or review sections, only if activated
- Responsibilities:
  - for the champion, try to show that `source_blind` already saturates the near-tie regime or that an abstention-like control is already covered
  - for the backup, try to collapse the lane to known restart-safe intermittent-power supervisors
  - for the parked third, try to show that a plain back-to-back switch or existing reverse-current-blocking literature already closes the gap

## Writer

- Tool routing:
  - markdown only
  - approved result tables and claim matrices
- Budget envelope:
  - `<=3h` after a lane clears its go/kill gate
- Responsibilities:
  - write only the surviving narrow claim
  - include the kill-rule outcome and why the rejected storylines failed
  - avoid unsupported words such as `first`, `best`, or `novel`

## Reviewer

- Tool routing:
  - shell diff inspection
  - evidence-note cross-check
- Budget envelope:
  - `<=3h` per drafted lane
- Responsibilities:
  - reject claim inflation or contradictions between summary and evidence
  - block any writeup that confuses store-voltage proxies with explicit handoff or restart events
  - send back any lane that lacks the required strong baseline

## Citation Auditor

- Tool routing:
  - claim-to-source cross-check
  - bibliography and claim-matrix review
- Budget envelope:
  - `<=2h` per active lane
  - `<=10` audited claims per lane
- Responsibilities:
  - verify every novelty, overlap, and benchmark sentence against an actual source or repo artifact
  - block paper-level novelty wording on the backup or parked third until the targeted overlap blockers are closed

## Benchmark Auditor

- Tool routing:
  - benchmark checklist review
  - manifest, hook, and baseline audit
- Budget envelope:
  - champion: `<=4h`
  - backup: `<=3h`, only if activated
  - parked third: `<=3h`, only if activated
- Responsibilities:
  - for the champion, require `source_blind`, `time_constant_ranked`, and one confidence-gated variant under equal `e_ctrl` accounting
  - for the backup, require a fixed hysteretic scrub baseline plus explicit second-rise and re-arm metrics
  - for the parked third, require a plain back-to-back switch baseline plus a bounded nonideal parasitic envelope
  - stop any lane that relies only on store-threshold proxies when the written claim depends on explicit handoff or restart events
  - block any packet-gating mechanism claim that does not either execute a same-scaffold no-packet control or stay explicitly bounded away from that causal claim

## Exit Rules

- If the champion does not beat `source_blind` on the pre-registered near-tie matrix, kill it and activate the backup.
- If the champion saturates the matrix but still cannot support a differentiated claim, activate the backup instead of widening the search.
- Activate the parked third only if both earlier lanes fail and the benchmark auditor confirms that the anti-backdrive question is still open under realistic parasitics.
- If a targeted overlap screen closes the gap for any lane, stop and record the blocker instead of broadening the search.
