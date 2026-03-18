# Runtime Integrator Note

This note should drive `results/verification/runtime_audit.md` for `research_rubric.json` `item_018`.

## Audit Goal

- Acceptance target: confirm that logs, seeds, restart counts, wall-clock time, objective evaluations, and canonicalized outputs are complete for every reported run.
- Scope: both completed experiment batches, `results/experiments/controls/` and `results/experiments/order_668_64m/`.
- Invalidator: missing control data fails the item, even if the frontier batch is otherwise complete.
- Emphasis: `runtime_audit.md` should be an artifact-completeness audit, not a second performance summary.

## Recommended `runtime_audit.md` Structure

### 1. Verdict And Scope

- Open with the audited run count: `15` reported runs total, split as `10` controls and `5` frontier runs.
- State the decision up front: the current artifact set appears sufficient on substance for `item_018`, with one documentation caveat explained below.
- State the caveat clearly: the markdown and JSON summaries are not enough by themselves for every required field, so the final audit must cite the raw run JSONs directly.

### 2. Artifact Inventory

- Controls inventory:
  - `results/experiments/controls/summary.md`
  - `results/experiments/controls/summary.json`
  - `results/experiments/controls/configs/*.json` (`5` files)
  - `results/experiments/controls/seeds/*.json` (`2` files)
  - `results/experiments/controls/runs/*/*.json` (`10` files)
- Frontier inventory:
  - `results/experiments/order_668_64m/summary.md`
  - `results/experiments/order_668_64m/summary.json`
  - `results/experiments/order_668_64m/configs/*.json` (`5` files)
  - `results/experiments/order_668_64m/runs/*.json` (`5` files)
  - shared seed file `results/frontier/order_668_64m/seed_sequences.json`
- Cross-reference point to include: every run path named in the two summary JSONs resolves on disk (`15/15`).

### 3. Required-Evidence Matrix

`runtime_audit.md` should include one compact table covering every reported run, with columns like:

- run ID / experiment ID
- seed file
- requested restarts
- completed restarts
- best restart
- wall-clock time
- objective evaluations
- canonical fingerprint present
- trace/log present

The table should be backed by these evidence points:

| Requirement | What to cite | Current evidence |
| --- | --- | --- |
| logs / traces | raw run JSON `trace` arrays | non-empty `trace` present in all `15/15` run files; use this as the saved raw runtime log/trace |
| seeds | raw run JSON `seed_file`; batch seed directories / frontier seed path | controls point to `2` local seed files; frontier run files all point to `results/frontier/order_668_64m/seed_sequences.json` |
| restart counts | raw run JSON `restart_statistics` | all `15/15` runs include `requested`, `completed`, and `best_restart` |
| wall-clock time | raw run JSON `wall_seconds` | present in all `15/15` runs |
| objective evaluations | raw run JSON `objective_evaluations` | present in all `15/15` runs |
| canonicalized outputs | raw run JSON `canonical_fingerprint` | present and non-empty in all `15/15` runs |

- Extra support worth noting: all run files also include `best_objective`, `objective_summary`, correlation defect fields, and Gram-defect fields, which match the reporting expectations in `benchmark_gate.md`.

### 4. Control Batch Completeness

- Cite `results/experiments/controls/summary.md` for the batch definition: two deterministic q0-flip controls (`n=5` and `n=7`), shared evaluation budget `80`, restart count `3`, and RNG seed `17`.
- Cite `results/experiments/controls/summary.json` for the run list: `10` runs total (`2` seeds x `5` methods).
- Key completeness point: all `10` referenced control run files exist, and each one contains `seed_file`, `restart_statistics`, `wall_seconds`, `objective_evaluations`, `canonical_fingerprint`, and a non-empty `trace`.
- Control-seed provenance to state explicitly:
  - `results/experiments/controls/seeds/control_n5_q0.json`
  - `results/experiments/controls/seeds/control_n7_q0.json`
- Restart-accounting point to include: control runs do not all finish `3/3` restarts, but the shortfalls are recorded rather than missing.
  - observed restart pairs in controls: `(3,1)`, `(3,2)`, `(3,3)`
  - useful concrete examples: `control_n5_q0:tabu` records `2/3`; `control_n7_q0:simulated_annealing` records `1/3`
- Sanity ranges worth citing:
  - objective evaluations in controls: `10` to `80`
  - wall-clock time in controls: about `0.034` to `0.082` seconds
- Conclusion this section should make explicit: no control artifact gap was found, so the invalidation clause is not triggered.

### 5. Frontier Batch Completeness

- Cite `results/experiments/order_668_64m/summary.md` for the matched frontier setup: canonical `64`-modular seed, shared budget `80`, restart count `3`, RNG seed `17`, and `restart_packet_flips = 2`.
- Cite `results/experiments/order_668_64m/summary.json` for the frontier run list: `5` methods, one run file per method.
- Key completeness point: all `5` referenced frontier run files exist, and each one contains `seed_file`, `restart_statistics`, `wall_seconds`, `objective_evaluations`, `canonical_fingerprint`, and a non-empty `trace`.
- Seed-provenance point: every frontier run JSON points to the same canonical seed file, `results/frontier/order_668_64m/seed_sequences.json`.
- Restart-accounting point to include: frontier restart shortfalls are recorded outcomes, not missing data.
  - observed restart pairs in frontier: `(3,1)` and `(3,3)`
  - concrete examples: `H1_defect_syndrome_ca_64m` records `3/3`, while `greedy`, `tabu`, and `simulated_annealing` record `1/3`
- Sanity ranges worth citing:
  - objective evaluations in frontier: `26` to `80`
  - wall-clock time in frontier: about `0.079` to `2.129` seconds
- Important asymmetry to mention: `results/experiments/order_668_64m/summary.json` does not surface `canonical_fingerprint`, so `runtime_audit.md` must cite the raw frontier run JSONs for canonicalized outputs.

### 6. Benchmark-Spec Alignment Notes

- Tie the runtime audit back to `results/verification/benchmark_spec.md`:
  - matched seeds are required
  - shared accounting fields (`evaluation_budget = 80`, `restart_count = 3`, `seed = 17`) are part of the fairness scaffold
  - canonicalization is currently the harness `canonical_fingerprint`, not full Hadamard equivalence
- Tie the runtime audit back to `results/verification/benchmark_gate.md`:
  - every batch is supposed to report `objective_evaluations`, `wall_seconds`, `restart_statistics`, and terminal defect metrics
  - the runtime audit should confirm that those runtime-accounting fields are actually present in the saved artifacts
- Wording guardrail to include: do not overclaim the canonicalization layer. The benchmark spec says the current fingerprint only quotients the shared q/s sign symmetries.

### 7. Sufficiency Call For `item_018`

- Recommended decision: the current evidence appears sufficient to satisfy the substance of `item_018`.
- Basis for that decision:
  - all `15` summary-referenced run files are present
  - all `15` contain seed provenance
  - all `15` contain restart statistics
  - all `15` contain wall-clock time
  - all `15` contain objective-evaluation counts
  - all `15` contain canonical fingerprints
  - all `15` contain non-empty traces that function as the saved raw logs/traces
  - no missing control artifact was found
- Required caveat to preserve: the summaries alone are under-specified for this item, especially for frontier canonicalized outputs and per-run restart accounting. `runtime_audit.md` should therefore say explicitly that it audited the raw run JSONs referenced by the summaries.
- Practical close: this is a documentation gap, not a data gap. Once `results/verification/runtime_audit.md` is written with the per-run evidence table above, `item_018` should be ready to mark complete.
