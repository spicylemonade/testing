# Integrator Note

This note audits the current `item_023` drafts against the verification pack and `sources.bib`.

## Files Checked

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`
- `results/verification/verification_summary.md`
- `results/verification/runtime_audit.md`
- `results/analysis/prior_work_comparison.md`
- `sources.bib`
- `results/writeup/methods_brief.md`
- `results/writeup/claims_table.md`

## Integrator Decision

- Every explicit claim in `results/writeup/claims_table.md` is tied to at least one verification artifact or BibTeX key.
- Every explicit claim in `results/writeup/methods_brief.md` is also tied to at least one verification artifact or BibTeX key.
- No row-level evidence link is missing in the current drafts.
- The remaining issues are coverage and wording issues, not missing citations at the row level.

## `claims_table.md` Audit

| ID | Claim summary | Evidence link check | Status |
| --- | --- | --- | --- |
| C1 | Seed provenance is tied to the published order-668 near-solution. | `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `eliahou2025_64mod668` | OK |
| C2 | H1 executes on matched solved controls. | `results/verification/verification_summary.md`; `results/verification/novelty_report.md` | OK |
| C3 | First frontier kill test is negative for H1. | `results/verification/verification_summary.md`; `results/verification/benchmark_report.md`; `results/verification/novelty_report.md` | OK |
| C4 | Exactness result is negative for both a new order-668 hit and an exact improvement over the seed. | `results/verification/verification_summary.md`; `results/verification/benchmark_report.md`; `eliahou2025_64mod668` | OK |
| C5 | H1 does not earn continuation through partial objective changes. | `results/verification/benchmark_report.md`; `results/verification/novelty_report.md` | OK |
| C6 | Novelty claim is narrow and excludes broader CA-newness language. | `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `tsompanas2017`; `eliahou2025_64mod668` | OK |
| C7 | Benchmark is good enough for elimination, not for literature-level competitiveness. | `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `suksmono2018`; `suksmono2019`; `bright2019` | OK |
| C8 | Runtime package is auditable across all `15` saved runs. | `results/verification/runtime_audit.md` | OK |
| C9 | Next action is `pivot to H2`, with the H2 family-leakage guard still in force. | `results/verification/verification_summary.md`; `results/verification/novelty_report.md` | OK, but keep the rationale narrow |

## `methods_brief.md` Coverage

All claims in `results/writeup/methods_brief.md` have evidence links. Most of them collapse cleanly into `C1` through `C9`.

The following evidence-linked claims appear in the brief but do not yet have standalone rows in `results/writeup/claims_table.md`:

- The decisive comparison is against `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb` under one shared harness.
- All order-668 runs use the same q/s representation and the same frontier seed file.
- The saved pilot accounting is fixed at budget `80`, requested restarts `3`, RNG seed `17`, `restart_packet_flips = 2`, and a common `exact_hit` gate.
- The H1 frontier runtime detail (`32` objective evaluations, `2.129s`) is part of the readout and is interpreted as CA field-evaluation cost rather than better objective outcome.

## Missing Evidence Links And Weak Links

- No explicit claim in the current drafts is missing an evidence pointer.
- If one-to-one claim inventory is required, add the four `methods_brief.md` claims listed above to `results/writeup/claims_table.md`.
- Keep the H2 rationale phrased as a verification-pack interpretation. The stronger wording about a locality or actuator-basis mismatch is linked, but it is still an inference in the current writeup set rather than a separately established mechanism.
