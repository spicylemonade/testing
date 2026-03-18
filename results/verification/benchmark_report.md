# Benchmark Report

Snapshot date: 2026-03-18 UTC

## Inputs Audited

- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`
- `results/baselines/benchmark_spec.md`
- `results/core/lane_gates.md`
- `results/verification/verification_summary.md`

## Specialist-Agent Attempt

The required specialist roles were invoked for this checkpoint via shell-level child `codex exec` runs on 2026-03-18 UTC:

- `monitor`
- `benchmark_auditor`
- `falsifier`
- `integrator`

All four child runs failed with the same transport error after repeated retries: `stream disconnected before completion`. They produced empty temporary output files and no usable memo. Per the tool-governance rule against repetitive low-signal delegation, the final audit below was completed directly from the audited artifacts.

## Audit Table

| audit question | verdict | basis |
| --- | --- | --- |
| Matched budgets preserved? | `pass` | The benchmark spec freezes the first-gate budget at at most `3` H1 families and at most `10^3` exact decodes per family and per matched baseline block. The experiment report records `0 / 3` families and `0 / 10^3` exact decodes, so no side spent hidden compute. |
| Identical decoder usage confirmed? | `blocked / not evaluable` | No exact decoder or verifier exists in the current snapshot. Because nothing ran, no baseline received a different decoder, but true decoder-parity confirmation remains unresolved until a real evaluator exists. |
| Full score accounting preserved? | `pass` | The audited artifacts retain the exact score definition `(m(G)+|R|)/(n(G)-|T|)` and explicitly refuse proxy metrics. All score fields are left `not available` or `[]` rather than replaced with heuristic values. |
| Negative results preserved? | `pass` | The artifacts explicitly record the no-run state, the unspent budgets, and the empty control or sweep distributions. No best-of-many, proxy, or partial success story was substituted. |
| Later phases correctly held closed? | `pass` | `h1_tiny_grid_report.md` explicitly closes items 017-020 to blocker-aware auditing only, and the control/sweep artifacts maintain that closure. |

## Main Findings

- Compute parity is preserved in the only honest sense available here: no H1 family and no baseline consumed exact-decode budget.
- Decoder parity is still unresolved, but not violated. The missing decoder blocks execution for all sides equally.
- Score accounting discipline is intact. The run did not smuggle in proxy objectives or partial metrics.
- Negative results were preserved cleanly. The record is a blocked experiment pass, not an experimental win.

## Risks Still Open

- The phrase "audit pass" would be misleading without qualification. This checkpoint passes integrity review for a blocked experiment phase, not benchmark execution.
- Decoder-matched fairness cannot be demonstrated positively until an actual exact decoder exists.
- If later reports omit the `0`-decode and empty-distribution facts, they will overstate what phase 4 established.

## Verdict

`Integrity pass; execution blocked.`

The current artifact set supports claims about preserved budgets, preserved exact-score discipline, and preserved negative results. It does **not** support claims about empirical benchmark superiority, decoder-parity success, or experimental signal.
