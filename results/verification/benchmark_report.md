# Benchmark Report

Verification phase: `review_round_1`

## Verdict

- Internal branch-gating verdict: `supported`.
- Publication-quality benchmark verdict: `not supported`.

The current pack supports one narrow benchmark claim: on the canonical frontier seed `results/frontier/order_668_64m/seed_sequences.json`, under the shared q/s representation, `evaluation_budget = 80`, requested `restart_count = 3`, RNG seed `17`, and `restart_packet_flips = 2`, no method reached `exact_hit`, and `H1_defect_syndrome_ca_64m` never improved the seed objective `13/2880/512`.

It does not support broader claims that H1 is generally inferior to non-CA search, that H1 failed specifically because locality or the one-packet basis is wrong, that the runtime artifacts are fully auditable, or that this is a literature-level benchmark relative to `suksmono2018`, `suksmono2019`, or `bright2019`.

## Evidence Reviewed

This audit re-read:
- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/verification/benchmark_spec.md`
- `results/verification/benchmark_gate.md`
- `results/verification/runtime_audit.md`
- `results/verification/runtime_benchmark_note.md`
- `results/experiments/controls/summary.md`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/summary.md`
- `results/experiments/order_668_64m/summary.json`
- `results/experiments/order_668_64m/configs/H1_defect_syndrome_ca_64m.json`
- `results/branches/H1_precheck.md`
- `results/branches/H1_frontier_sensitivity_probe.json`
- `results/writeup/claims_table.md`
- raw run JSONs under `results/experiments/controls/runs/` and `results/experiments/order_668_64m/runs/`

Primary experiment groups reviewed:
- `control_n5_q0:*`
- `control_n7_q0:*`
- `order_668_64m:*`

## Missing Baselines

### 1. No CA-off mechanism baseline

The frontier roster compares H1 only against `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb`. There is no matched variant that keeps H1's packet-delta scorer but removes CA-specific coupling or refractory behavior.

Why this matters:
- The current negative result can eliminate the branch.
- It cannot distinguish `CA dynamics add nothing` from `the H1 implementation is simply a poor local-search policy`.

Missing falsifiable test:
- Re-run the full control batch and the canonical frontier seed with:
  - full H1
  - zero-coupling H1 (`same_channel_weight = 0`, `cross_channel_weight = 0`)
  - zero-refractory H1 (`refractory_steps = 0`, `refractory_penalty = 0`)
  - scorer-only / fallback-disabled H1 (`fallback_best_packet = false`)

Decision rule:
- If full H1 does not beat its CA-off variants on `exact_hit` or on median terminal support plus `max_abs`, drop any CA-mechanism claim.

### 2. No chance or recoverability anchors on the easy controls

The only solved controls are `control_n5_q0` and `control_n7_q0`. They establish that the harness works, but they do not bound chance performance or optimal recoverability on the tiny cases.

Missing falsifiable test:
- Add a random-walk baseline on the tiny controls.
- Add an explicit recoverability/oracle reference for the same controls.

Decision rule:
- If H1 only beats random walk on tiny one-flip controls, treat those wins as scaffold validation, not as evidence of frontier relevance.

### 3. No publication-level proxy baseline beyond same-coordinate local search

The current roster is intentionally narrow and same-representation. That is acceptable for the first kill test, but it is not enough to support benchmark language implying competitiveness with broader search families discussed in `suksmono2018`, `suksmono2019`, or `bright2019`.

Missing falsifiable test:
- Either keep the claim narrow to `same-representation negative pilot`
- Or add at least one stronger exact or certificate-oriented baseline on tractable proxy instances before making literature-level benchmark claims.

## Missing Controls

### 1. Restart fairness is matched in config, not in executed evidence

Every method requests `restart_count = 3`, but the frontier batch does not execute matched restart coverage:
- `order_668_64m:H1_defect_syndrome_ca_64m`: `3/3`
- `order_668_64m:stochastic_hillclimb`: `3/3`
- `order_668_64m:greedy`: `1/3`
- `order_668_64m:tabu`: `1/3`
- `order_668_64m:simulated_annealing`: `1/3`

The same issue appears on controls: `control_n5_q0:tabu` completes `2/3`, and `control_n7_q0:simulated_annealing` completes `1/3`.

Why this matters:
- The current result is still valid for internal branch elimination.
- If anything, the imbalance favors H1: H1 completed more frontier restarts than `greedy`, `tabu`, and `simulated_annealing` and still never improved the seed objective.
- It is not publication-grade evidence for restart-robust method ordering.

Missing falsifiable test:
- Re-run with a fixed per-restart budget, or keep running until every method completes the same number of restarts.

Decision rule:
- Do not claim restart-robust comparisons until the negative H1 result survives equal executed restart coverage.

### 2. The control ladder is too small and too easy

The only matched solved controls are two deterministic q0-flip seeds with `seed_length` `5` and `7`. On these toy cases, H1, greedy, and tabu all achieve `exact_hit_rate = 1.00`, while simulated annealing and stochastic hillclimb hit `0.50`.

Why this matters:
- These are sanity controls, not difficulty-matched proxies for the `seed_length = 167` frontier seed.
- They do not show that any apparent H1 advantage persists once the defect profile becomes frontier-like.

Missing falsifiable test:
- Add multi-flip and higher-support controls in the same q/s representation.
- Add a scale bridge between the current solved controls and the frontier seed.

Decision rule:
- If H1's apparent control advantage vanishes once initial support and seed length increase, demote the current control wins to harness-validation evidence only.

### 3. Hold-out tuning control is missing

`results/branches/H1_frontier_sensitivity_probe.json` tunes or probes H1 on the frontier seed itself. There is no held-out control family used for hyperparameter selection.

Why this matters:
- The same artifact is being used both to shape the H1 explanation and to benchmark the frontier behavior.
- That is not acceptable for a publication-quality method study.

Missing falsifiable test:
- Freeze H1 parameters on a held-out synthetic/control ladder before rerunning the frontier batch.

Decision rule:
- Do not use frontier-seed sensitivity observations as mechanism evidence unless the same parameter choice is frozen before frontier evaluation.

### 4. Equivalence control is still representation-local

The current `canonical_fingerprint` only quotients by global q/s sign flips. That is enough for the present negative pilot, but not enough for stronger uniqueness, diversity, or structured-family claims.

Missing falsifiable test:
- If future runs produce any improved frontier states, perform a family-leakage / equivalence audit before counting them as distinct benchmark outcomes.

## Missing Ablations

### 1. The saved H1 sensitivity probe is not a benchmark-grade ablation pack

`results/branches/H1_frontier_sensitivity_probe.json` is useful reconnaissance, but it is not a publication-quality ablation:
- one frontier seed
- one RNG seed
- `restart_count = 1`
- no matched baseline comparators
- no uncertainty estimate

All eight saved rows stay pinned to the seed objective `13/2880/512`, which is informative engineering evidence but not enough to isolate cause.

### 2. No actuator-basis ablation

The current report logic infers that the one-packet actuator basis may be the blocker, but no matched experiment compares the current packet library against an alternative actuator basis under the same harness.

Missing falsifiable test:
- Compare the current one-packet basis against at least one alternative packet library under matched accounting on the same controls and frontier seeds.

Decision rule:
- Do not claim a representation-level failure unless an actuator-changing variant is compared directly against tuning-only variants.

### 3. No synchrony / sparsity ablation

The benchmark never tests whether sparse asynchronous activation is necessary because the saved frontier config fixes `max_active_packets = 1`.

Missing falsifiable test:
- Re-run H1 with `max_active_packets > 1` under the same accounting on the harder controls and frontier seeds.

Decision rule:
- If multi-packet activation changes the frontier behavior materially, the current CA interpretation is under-identified.

## Missing Error Analysis

### 1. Run outputs are easy to misread

The raw run JSON top level is `best_over_run`, not terminal output. Two concrete examples:
- `control_n5_q0:H1_defect_syndrome_ca_64m` is `exact_hit = true`, but its last trace point is still `support 1`, `l1 4`, `max_abs 4`.
- `order_668_64m:H1_defect_syndrome_ca_64m` keeps the seed as `best_objective` `13/2880/512`, while its three restart terminals diffuse to `33/2368/384`, `40/2356/408`, and `23/2216/384`.

Missing falsifiable test:
- Add per-restart terminal summaries and an explicit `output_semantics` field.

Decision rule:
- Treat the batch as publication-grade only if a third party can tell, from the raw artifact alone, whether a number is seed state, terminal state, or best-over-run state.

### 2. Traces are sampled accepted-state logs, not replay-complete logs

Examples from the frontier batch:
- `greedy`: `2` trace points for `80` objective evaluations
- `simulated_annealing`: `2` trace points for `80` objective evaluations
- `tabu`: `3` trace points for `80` objective evaluations

This is enough for a coarse negative readout. It is not enough for serious failure analysis or auditability claims.

Missing falsifiable test:
- Emit evaluation-complete traces, or explicitly version a sampled-trace schema that is rich enough to recover every restart terminal and accepted move sequence.

### 3. Failure clustering is unmeasured

The current artifacts do not record defect-location summaries, lag identities, or per-restart failure clusters.

Missing falsifiable test:
- Add per-restart defect-location summaries and cluster whether the same lag families fail repeatedly across restarts and perturbation seeds.

Decision rule:
- Do not claim a mechanism story such as `locality failed` or `the actuator basis is wrong` until repeated failure structure is visible in the saved artifacts.

### 4. Provenance completeness is still inconsistent across verification files

`results/verification/runtime_audit.md` says runtime evidence is complete enough to satisfy the audit, while `results/verification/runtime_benchmark_note.md` says the same batch is still short because output semantics, replay completeness, and digests are missing.

Why this matters:
- The benchmark pack should not make a stronger auditability claim than its own side notes allow.

Missing falsifiable test:
- Add seed digests, config checksums, code revision identifiers, and a reproduction test that reconstructs every saved run from recorded artifacts alone.

## Missing Stress Tests

### 1. No budget sweep

Only `evaluation_budget = 80` is reported.

Missing falsifiable test:
- Repeat the frontier batch at a small grid such as `40`, `80`, and `160`.

Decision rule:
- Do not claim the negative result is budget-robust until H1 remains non-competitive across the sweep.

### 2. No RNG sweep

Only RNG seed `17` is reported.

Missing falsifiable test:
- Repeat the frontier batch across several RNG seeds with equal executed restart coverage.

Decision rule:
- Do not claim seed-robust failure until the same negative conclusion survives the RNG sweep.

### 3. No restart-perturbation sweep

Only `restart_packet_flips = 2` is reported.

Missing falsifiable test:
- Repeat with at least a small grid such as `1`, `2`, and `4`.

Decision rule:
- If H1 only fails or only works at one restart perturbation setting, the current conclusion is too configuration-specific.

### 4. No frontier perturbation suite

There is no matched q-flip / s-flip perturbation suite around the canonical frontier seed. The saved frontier batch therefore measures only one exact seed instance.

Missing falsifiable test:
- Build a small perturbation suite around `results/frontier/order_668_64m/seed_sequences.json` and run every method on the same perturbations.

Decision rule:
- Do not promote the one-seed negative pilot to a method-level benchmark claim unless it survives nearby frontier perturbations.

## Claim Status

| Claim | Status | Why |
| --- | --- | --- |
| `H1` failed the first matched pilot on the canonical frontier seed. | Supported | The saved `order_668_64m:*` batch is a clear negative result under one locked q/s contract. |
| `H1` is broadly worse than non-CA local search. | Not supported | Only one frontier seed, one RNG seed, one budget, and unequal executed restart coverage. |
| `H1` failed specifically because locality or the one-packet basis is wrong. | Not supported | No CA-off or actuator-basis ablations isolate that cause. |
| The runtime package is fully auditable. | Not supported | `runtime_audit.md` and `runtime_benchmark_note.md` disagree, and the saved traces/output semantics are incomplete for replay. |
| The current roster is a literature-level benchmark. | Not supported | The pack is narrower than the benchmark ceiling implied by `suksmono2018`, `suksmono2019`, and `bright2019`. |
| The current evidence is enough to stop broad H1 expansion inside this repo. | Supported | The one-seed matched negative pilot is sufficient for internal branch elimination. |

## Minimum Next Tests

1. CA-off mechanism ablation
- Run full H1, zero-coupling H1, zero-refractory H1, and scorer-only / fallback-disabled H1 on the current controls plus the canonical frontier seed.
- Reject CA-mechanism language if full H1 does not beat its CA-off variants.

2. Replicated frontier batch
- Repeat `order_668_64m:*` across multiple RNG seeds with equal executed restart coverage or fixed per-restart budgets.
- Promote the negative result beyond internal gating only if the same ordering survives the replicated batch.

3. Harder control ladder
- Add multi-flip, higher-support, and longer-length controls in the same q/s representation.
- Treat current control wins as sanity checks only if H1 loses its edge on the harder ladder.

4. Artifact completeness repair
- Add per-restart terminal records, `output_semantics`, trace schema/versioning, and code/config/seed digests.
- Require a third party to reconstruct all saved terminal states from the recorded artifacts.

5. Budget and perturbation stress grid
- Sweep `evaluation_budget`, `restart_packet_flips`, and nearby q/s perturbations around the canonical frontier seed.
- Keep publication claims narrow unless the H1-negative result survives those stress tests.

## Bottom Line

The current benchmark is strong enough to falsify the present H1 branch under one matched pilot. It is not strong enough to support publication-quality claims about mechanism, robustness, auditability, or broader benchmark competitiveness.
