# Director Brief

## Champion

- `H1_confidence_gated_abstention` is the champion direction.

This is the best novelty-to-falsifiability trade in the scout set. The repo already killed the broad "better ranker" story and preserved `source_blind` as the strongest same-family baseline. That creates a sharper question: when should the startup front end refuse to rank at all? The lane stays inside the active H1 scaffold, avoids the crowded claims that the falsifier memo already rejects, and has the cleanest go/kill test.

- Why it wins:
  - highest novelty per added circuit complexity
  - fastest falsifier: it dies as soon as `source_blind` matches it on the near-tie matrix
  - clearest verification: one small matrix on the existing packet-gated scaffold can answer the question

## Backup

- `H1_restart_scrub_handoff` is the backup.

This is more important for real batteryless nodes than the parked third lane and still has a disciplined kill path, but its novelty margin is less secure because the scout set does not yet resolve restart-safe intermittent-power overlap. Keep it inactive unless the champion saturates or dies early.

- Why it is second:
  - practical importance is high
  - the metrics are clean: `rise2_ok`, restart latency, and restart-control energy
  - overlap is still an unresolved blocker, so it should not outrank the champion

## Parked Third

- `H1_reverse_port_sentinel` stays parked.

It is useful as a realism and benchmarking moat, but it is not the lead research claim unless device-faithful parasitics actually open a gap that plain back-to-back isolation cannot close. Until then it reads more like a modeling correction than a new circuit thesis.

## Out Of Scope For This Budget

- Do not activate the bridge-memo lanes in this pass:
  - spread-spectrum admittance probing
  - cryogenic sequential-evidence support blocks
  - high-temperature pilot-tone channel estimation

They may still matter later, but they would force fresh literature or model gates before the H1 negative-space shortlist is resolved.

## Blockers And Handoff

- The scout set is sufficient to choose a champion and a backup, but not to claim paper-level novelty on the parked lanes without a tighter overlap screen.
- Benchmark blocker 1:
  - `startup_ok` still drifts between the written contract and the current measurement hooks, so any next-slice success metric must be reconciled with explicit handoff events before promotion
- Benchmark blocker 2:
  - there is still no executed same-scaffold no-packet control, so any packet-gating mechanism claim has to stay bounded and cannot be promoted as a settled causal story
- Unresolved blocker 3:
  - the restart-safe lane still lacks an exact prior-art claim matrix for intermittent-power supervisors and brownout recovery
- Unresolved blocker 4:
  - the reverse-port lane depends on device-faithful parasitic modeling that the current decks do not yet provide

- Exact next experiment for the researcher on the champion:
  - run one near-tie matrix on the existing packet-gated scaffold with `source_blind`, `time_constant_ranked`, and one confidence-gated fallback variant; sweep small `VOC` offsets, `1:1` to `1:3` impedance spread, and unequal or late-arrival ramps; report `startup_ok`, `t_handoff`, `e_ctrl`, and abstain-to-commit transitions under equal accounting
- Exact next experiment for the researcher on the backup, only if the champion is killed or saturates:
  - extend the falsifier deck beyond first handoff, force repeated collapse and recovery with partial-store memory, and compare one restart-scrub controller against `source_blind` and a fixed hysteretic scrub baseline on `startup_ok`, `fall_count`, `rise2_ok`, restart latency, and restart-control energy
