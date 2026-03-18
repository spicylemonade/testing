# Benchmark Report

## Scope

This audit re-read:

- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/verification/benchmark_spec.md`
- `results/verification/benchmark_gate.md`
- `results/verification/runtime_audit.md`
- `results/verification/runtime_benchmark_note.md`
- `results/writeup/claims_table.md`
- `results/experiments/controls/summary.md`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/summary.md`
- `results/experiments/order_668_64m/summary.json`
- raw run JSONs under `results/experiments/controls/runs/` and `results/experiments/order_668_64m/runs/`
- `results/branches/H1_frontier_sensitivity_probe.json`

Primary experiment IDs reviewed:

- `control_n5_q0:H1_defect_syndrome_ca_64m`
- `control_n5_q0:greedy`
- `control_n5_q0:simulated_annealing`
- `control_n5_q0:stochastic_hillclimb`
- `control_n5_q0:tabu`
- `control_n7_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:greedy`
- `control_n7_q0:simulated_annealing`
- `control_n7_q0:stochastic_hillclimb`
- `control_n7_q0:tabu`
- `order_668_64m:H1_defect_syndrome_ca_64m`
- `order_668_64m:greedy`
- `order_668_64m:simulated_annealing`
- `order_668_64m:stochastic_hillclimb`
- `order_668_64m:tabu`

Paper keys used to bound benchmark claim strength:

- `eliahou2025_64mod668` :: *A 64-Modular Hadamard Matrix of Order 668*
- `tsompanas2017` :: *Cellular Automata Applications in Shortest Path Problem*
- `suksmono2018` :: *Finding a Hadamard Matrix by Simulated Quantum Annealing*
- `suksmono2019` :: *Finding Hadamard Matrices by a Quantum Annealing Machine*
- `bright2019` :: *The SAT+CAS method for combinatorial search with applications to best matrices*

## Bottom Line

- Adequate for internal branch elimination: `yes`.
- Adequate for publication-quality benchmark claims: `no`.

The saved pack is strong enough to support one narrow statement: under one canonical order-`668` frontier seed, one RNG seed, one budget (`80`), and one shared q/s harness, `H1_defect_syndrome_ca_64m` fails the first kill test and does not earn broad continuation.

The same pack is not strong enough to support stronger claims such as:

- `H1` is broadly worse than non-CA search.
- `H1` failed specifically because the locality / actuator basis is wrong.
- the runtime package is fully auditable.
- the frontier comparison is restart-robust or seed-robust.
- the current roster is competitive with the broader Hadamard-search literature represented by `suksmono2018`, `suksmono2019`, and `bright2019`.

## Existing Coverage

- Representation control is real: all frontier methods operate in the same compact q/s coordinates on the canonical seed from `eliahou2025_64mod668`.
- Exactness control is real: all saved runs report the shared `exact_hit` gate plus support, `l1`, and `max_abs`.
- Small solved controls exist: `control_n5_q0:*` and `control_n7_q0:*`.
- One H1 sensitivity artifact exists: `results/branches/H1_frontier_sensitivity_probe.json`.

This is enough for a negative pilot. It is not enough for publication-grade performance or mechanism claims.

## Missing Baselines

### 1. Mechanism baseline

There is no CA-off counterpart that keeps H1's exact packet-delta machinery but removes CA-specific coupling or refractory behavior. The current matched roster compares H1 only against `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb`. That is enough to test whether H1 beats standard local heuristics under one shared representation, but it does not test whether the CA-specific parts of H1 matter.

Missing falsifiable test:

- rerun the controls and canonical frontier seed with:
  - full H1
  - H1 with `same_channel_weight = 0` and `cross_channel_weight = 0`
  - H1 with `refractory_steps = 0` and `refractory_penalty = 0`
  - H1 with `fallback_best_packet = false`

If full H1 does not beat these CA-off variants on exact-hit or median terminal support / `max_abs`, the CA-mechanism claim fails.

### 2. Difficulty-matched control baseline

The only solved controls are tiny deterministic q0-flip seeds: `control_n5_q0` and `control_n7_q0`. Those are useful sanity checks, not frontier-like controls. There is no intermediate control ladder closer to `seed_length = 167`, to support `13`, or to the defect profile of the canonical order-`668` seed.

Missing falsifiable test:

- add multi-flip and frontier-style synthetic controls with larger `seed_length` and higher initial support.
- require H1 to preserve any control advantage once the controls are no longer one-flip toy cases.

### 3. Seed-robustness baseline

The frontier batch uses one seed file, `results/frontier/order_668_64m/seed_sequences.json`, and one RNG seed, `17`. There is no frontier perturbation suite, no equivalent-seed sweep, and no multi-seed stochastic replication.

Missing falsifiable test:

- run the same frontier protocol on a perturbation suite around the canonical seed, including both q-flip and s-flip perturbations.
- repeat the batch across several RNG seeds.

If the negative H1 result does not survive those replications, the current branch-kill claim should remain internal only.

### 4. Broader literature baseline

The current roster is intentionally narrow. That is fine for internal gating, but it is not a literature-level benchmark against the broader search families represented by `suksmono2018`, `suksmono2019`, or `bright2019`.

Missing falsifiable test:

- either keep the claim narrow to "seed-matched negative pilot against same-representation local heuristics"
- or add at least one stronger exact or certificate-oriented baseline on tractable proxy instances before claiming literature competitiveness

### 5. Chance / oracle anchors on tiny controls

There is no explicit uninformed baseline and no explicit oracle-style recoverability baseline in the saved benchmark tables, even though the only solved controls are tiny. That leaves no anchor for chance performance or optimal recoverability on the easy cases.

Missing falsifiable test:

- add a random-walk baseline on the tiny controls
- add an explicit optimal recoverability reference for those controls

## Missing Ablations

### 1. H1 component ablations are not benchmark-quality yet

`results/experiments/order_668_64m/configs/H1_defect_syndrome_ca_64m.json` exposes many H1-specific knobs:

- `lag_neighborhood_radius`
- `packet_neighborhood_radius`
- `same_channel_weight`
- `cross_channel_weight`
- `active_lag_bonus`
- `spill_l1_penalty`
- `spill_support_penalty`
- `activation_threshold`
- `max_active_packets`
- `refractory_steps`
- `refractory_penalty`
- `stagnation_limit`
- `fallback_best_packet`

Only one setting is benchmarked. `results/branches/H1_frontier_sensitivity_probe.json` is useful engineering reconnaissance, but it is not a publication-quality ablation pack because it uses:

- one seed
- `restart_count = 1`
- no matched baseline comparators
- no confidence or variance estimate

It also does not isolate the most important causal questions:

- no zero-coupling run
- no zero-refractory run
- no `spill_support_penalty = 0` run
- no CA-off / scorer-only run

### 2. Actuator-basis ablation is missing

The current frontier result does not distinguish "bad CA rule" from "bad one-packet actuator basis." The falsifier and follow-on writeups infer a locality / actuator-basis mismatch, but the benchmark itself does not isolate that cause.

Missing falsifiable test:

- compare the current H1 packet basis against at least one alternative basis under the same harness and accounting
- require the representation-changing variant to outperform tuning-only variants before claiming the failure is representation-level

### 3. Synchrony / sparsity ablation is effectively missing

The saved H1 configs keep `max_active_packets = 1`, so the benchmark never tests whether sparse asynchronous activation is necessary, whether broader synchronized updates help, or whether H1 collapses into a burst heuristic when multiple packets are active.

Missing falsifiable test:

- run matched H1 variants with `max_active_packets > 1`
- compare them against the current sparse setting on both controls and frontier perturbations

## Missing Controls

### 1. Restart-coverage control is incomplete

The frontier protocol requests `restart_count = 3`, but the executed restart coverage is not actually matched:

- `order_668_64m:H1_defect_syndrome_ca_64m` completes `3/3`
- `order_668_64m:stochastic_hillclimb` completes `3/3`
- `order_668_64m:greedy` completes `1/3`
- `order_668_64m:simulated_annealing` completes `1/3`
- `order_668_64m:tabu` completes `1/3`

This does not invalidate the negative pilot, but it does make the existing distributional wording too strong. A one-seed frontier batch with unequal executed restart coverage is not publication-grade evidence for restart-robust comparisons.

Missing falsifiable test:

- either equalize executed restarts
- or switch to a fixed per-restart budget and report the full replicated restart distribution

### 2. Symmetry / equivalence control is partial

The current canonical fingerprint only quotients by global q/s sign flips. There is no full Hadamard-equivalence control over row/column permutations or broader structured-family symmetries.

That is acceptable for the current narrow negative pilot. It is not enough for stronger novelty or uniqueness claims.

Missing falsifiable test:

- either implement broader equivalence handling
- or run an explicit family-leakage audit on every reported near-best frontier state

### 3. Provenance control is incomplete

The run JSONs record seed paths and embedded config values, but not:

- closed seed hashes
- config checksums
- code revision identifiers

This is exactly the gap already flagged in `results/verification/runtime_benchmark_note.md`.

Missing falsifiable test:

- require a third party to reconstruct every restart terminal and rerun all `15` saved experiments from recorded code, config, and seed digests alone

Until that test passes, "fully auditable" is too strong.

### 4. Cost control is incomplete for runtime claims

Evaluation budgets are matched, but the internal work accounting is not symmetric:

- H1 logs `ca_field_evaluations = 10354` and takes about `2.13s`
- the non-CA baselines expose no comparable internal-work counter and finish in about `0.08s` to `0.14s`

The current pack supports one narrow statement: H1 is much slower despite using fewer objective evaluations. It does not isolate CA field evaluation as the cause.

Missing falsifiable test:

- instrument wall time by component
- or add a cached-delta / profiling ablation that shows the wall-time gap tracks field-evaluation work across variants

## Missing Error Analysis

### 1. Traces are not replay-complete

`results/verification/runtime_benchmark_note.md` is right: the traces are sampled accepted-state logs, not evaluation-complete logs. They are enough to see broad behavior, not enough to reconstruct every search trajectory.

### 2. Top-level outputs are `best_over_run`, not terminal-by-restart outputs

Two concrete examples matter:

- `order_668_64m:H1_defect_syndrome_ca_64m` reports the seed as `best_objective`, while its three restart terminals diffuse to support `33`, `40`, and `23`.
- `control_n5_q0:H1_defect_syndrome_ca_64m` is `exact_hit = true`, but the last trace entry is still nonzero.

Without explicit `output_semantics` and per-restart terminal summaries, the raw artifacts are easy to misread.

### 3. Failure taxonomy is too shallow

The frontier summary says H1 diffuses support and never beats the seed. That is useful, but it is still coarse. The current artifacts do not log:

- per-restart lag identities
- defect-location summaries
- failure clusters across equivalent frontier states
- whether the same defect families recur across restarts or seeds

That is not enough to defend a strong mechanism claim such as "locality failed" or "the actuator basis is wrong."

### 4. Uncertainty reporting is missing

One frontier seed, one RNG seed, and partial frontier restart coverage do not support robust variance or confidence claims. The current control summary reports variance on only two tiny controls; that is not a meaningful uncertainty story for the frontier question.

## Missing Stress Tests

### 1. Budget sweep

Only `evaluation_budget = 80` is reported.

### 2. RNG sweep

Only `seed = 17` is reported.

### 3. Restart-perturbation sweep

Only `restart_packet_flips = 2` is reported.

### 4. Frontier perturbation stress

There is no multi-flip frontier perturbation suite and no s-flip frontier perturbation suite.

### 5. Scale bridge

There are no solved or synthetic controls between `seed_length = 7` and `seed_length = 167`.

### 6. Hold-out tuning control

The saved H1 sensitivity work is on the frontier seed itself. That means there is no train/test separation for hyperparameter choice.

## Publication-Quality Claim Status

| Claim | Status | Why |
| --- | --- | --- |
| `H1` failed the first matched pilot on the canonical frontier seed. | Supported | The saved frontier batch is a clear negative result under one locked q/s contract. |
| `H1` is broadly worse than non-CA local search. | Not supported | Only one frontier seed, one RNG seed, one budget, and unequal executed restart coverage. |
| `H1` failed specifically because the locality / actuator basis is wrong. | Not supported | No matched actuator or mechanism ablations isolate that cause. |
| The runtime package is fully auditable. | Not supported | `results/verification/runtime_benchmark_note.md` explicitly says artifact completeness is still short of acceptance. |
| The current roster is competitive with broader Hadamard-search literature. | Not supported | The pack is much narrower than the benchmark expectations implied by `suksmono2018`, `suksmono2019`, and `bright2019`. |
| The current evidence is enough to reject broad H1 expansion inside this repo. | Supported | For internal branch gating, the one-seed negative pilot is good enough. |
| The current evidence is enough to justify the H2 pivot as a causal explanation. | Not supported | The H2 rationale is still an inference until tuning-only and actuator-changing ablations are compared under the same harness. |

## Falsifiable Next Tests

### 1. CA-off mechanism ablation

Re-run the controls and canonical frontier seed with:

- full H1
- zero-coupling H1
- zero-refractory H1
- scorer-only / fallback-disabled H1

Decision rule:

- if full H1 does not beat its CA-off variants on exact-hit or median terminal support / `max_abs`, drop the CA-mechanism claim

### 2. Replicated frontier batch

Repeat the frontier pilot across multiple RNG seeds and either:

- equalize executed restarts
- or use a fixed per-restart budget

Decision rule:

- only call the H1 negative result publication-grade if it survives the replicated batch on exact-hit and on terminal support / `max_abs`

### 3. Harder control ladder

Add multi-flip and frontier-style controls with larger `seed_length` and higher initial support.

Decision rule:

- if H1's apparent control advantage disappears once the controls are not one-flip toy cases, treat the current control wins as sanity checks only

### 4. Artifact-completeness test

Emit:

- per-restart terminal summaries
- explicit `output_semantics`
- defect-location summaries
- code / config / seed digests

Decision rule:

- a third party should be able to reconstruct every terminal state and rerun all `15` saved experiments from the recorded artifacts alone

### 5. Runtime-cause test

Profile or ablate cached delta / field computation.

Decision rule:

- if the wall-time gap does not track field-evaluation work after instrumentation, remove the current causal runtime explanation

## Verdict

The present benchmark is a valid falsification scaffold for the current H1 branch. It is not yet a publication-quality benchmark section.

The safe interpretation is narrow:

- seeded, representation-matched negative pilot on the canonical frontier seed from `eliahou2025_64mod668`
- useful for stopping broad H1 sweeps
- insufficient for stronger claims about mechanism, robustness, runtime causality, or broader competitiveness
