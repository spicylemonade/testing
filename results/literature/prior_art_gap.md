# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## 1. Cellular Automata Applications in Shortest Path Problem (2017)
- Paper ID: 4b85674750c1ad93a8d26427e52e7bec82d7e392
- Why it is close: It is a generic cellular-automata search / optimization paper, so it is the closest watchlist item if the current branch were to make the overbroad claim "CA search itself is novel."
- Differentiation hypothesis: The active branch is not a shortest-path or generic optimization application. It targets either the exact 167/80 cyclic obstruction or the specific 64-modular 668 seed with exact Hadamard-specific verifiers and matched direct-search controls.
- Evidence artifact(s): `results/analysis/branch_brief.md`; `results/literature/literature_snapshot.json`; `results/swarm/falsifier.md`
- Pivot decision (if any): Keep as an explicit novelty-collision check only. Do not cite it as methodological support for solving Hadamard 668.

## 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)
- Paper ID: 74159b79e948de4dd6fab33ecd01d4a0c96a51c5
- Why it is close: The overlap is almost entirely lexical (`automata`, `solve`) rather than mathematical. It is an optimization / scheduling application with no combinatorial-design or Hadamard structure.
- Differentiation hypothesis: The current work should remain materially different by staying on exact cyclic-autocorrelation and modular-Hadamard certificates rather than generic performance optimization.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/branch_brief.md`
- Pivot decision (if any): Treat as false-positive watchlist noise. No pivot needed, but avoid any wording that makes the branch sound like generic CA optimization.

## 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)
- Paper ID: 4c744f3e519204bac75f7a99661bbe3491393fc1
- Why it is close: It is another lexical false positive created by the seed query. The only real overlap is the phrase `cellular automata`.
- Differentiation hypothesis: Any novelty or methods discussion should explicitly ground itself in CA design-generation, CA controllability, and Hadamard search literature instead of biomedical CA simulation.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/falsifier.md`
- Pivot decision (if any): Marked non-competitive. Keep only as evidence that the original seed query needed curation.

## 4. Engineering Societies in the Agents World (2000)
- Paper ID: 094836f18350868a0b8cfe57a127906496120841
- Why it is close: It is not actually close; it entered the watchlist through weak term overlap from the initial seed search.
- Differentiation hypothesis: The active branch is a combinatorial-design / exact-search project and should not inherit novelty language from agent-society or multi-agent systems literature.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/research_context.md`
- Pivot decision (if any): Non-competitive false positive. Keep as a cautionary example of why the initial broad seed search is not trustworthy.

## 5. Learning Automata-Based Solutions to the Multi-Elevator Problem (2019)
- Paper ID: 9a8e718e861bc6a07be3b5cee1fa506c7f413b3d
- Why it is close: Like the single-elevator paper, it is only close if the branch makes a generic learning-automata claim.
- Differentiation hypothesis: The project remains distinct by evaluating exact-hit, closest-target, and modulus-lift metrics on Hadamard-specific artifacts rather than average waiting-time objectives on elevator scheduling.
- Evidence artifact(s): `results/analysis/branch_brief.md`; `results/literature/literature_snapshot.json`
- Pivot decision (if any): Keep on the watchlist as terminology noise; do not treat it as substantive prior art.

## 6. An Intelligent Tutoring System for Automata Theory : A Proposed Framework (2019)
- Paper ID: e1c5a794c53841d2e139f360bcff49e049455fb6
- Why it is close: It is not mathematically close at all; it is another seed-query lexical false positive caused by the word `automata`.
- Differentiation hypothesis: The branch should remain anchored to exact Hadamard and CA-design literature so that educational-software papers never appear adjacent to the active evidence packet.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/research_context.md`
- Pivot decision (if any): Non-competitive false positive. No pivot required.

## Active Basis Addendum

The six watchlist papers above remain useful as lexical-noise guards, but they are not the main citation burden anymore. The active branch now has to differentiate itself against the exact Hadamard and structured-CA papers that actually shape the search space.

### A. Convolution numbers: the cyclic case (2025)
- Paper ID: af20a0b3ccef66fad2a0a1e9f11011eb99194784
- Why it is close: This is the exact source of the unresolved `167/80` cyclic obstruction used by `H1`.
- Differentiation hypothesis: The project does not claim a new cyclic reduction. It only tests whether a CA-style local search on the exact obstruction reaches better states than matched direct search on the same support representation.
- Evidence artifact(s): `results/artifacts/target_167_weight_80.json`; `results/analysis/branch_brief.md`; `results/analysis/baseline_benchmark_sheet.md`
- Pivot decision (if any): Keep as the central exact anchor. Any claim broader than “local search on this exact obstruction” should be treated as novelty collapse.

### B. A 64-modular Hadamard matrix of order 668 (2025)
- Paper ID: ajc_v93_p422
- Why it is close: This is the exact source of the published order-668 seed used by `H2`.
- Differentiation hypothesis: The project does not claim a new 64-modular construction. It only tests whether a defect-transport CA can repair structured perturbations of the published seed under the same `s`-flip neighborhood as a non-CA baseline.
- Evidence artifact(s): `results/artifacts/seed_668_mod64.json`; `results/analysis/baseline_benchmark_sheet.md`; `results/analysis/kill_rules.md`
- Pivot decision (if any): Keep as the positive anchor for `H2`, but kill `H2` if the CA cannot beat the same-neighborhood greedy baseline.

### C. A SAT+CAS Method for Enumerating Williamson Matrices of Even Order (2018)
- Paper ID: eec5b2d83d3853c24cf070b4701fc2c86b594222
- Why it is close: It is a strong exact-search competitor for structured Hadamard-family problems.
- Differentiation hypothesis: The active branch must stay in a strictly local CA neighborhood and use the exact solver only as a verifier, not as a hidden search oracle.
- Evidence artifact(s): `results/analysis/baseline_benchmark_sheet.md`; `results/analysis/kill_rules.md`; `results/swarm/falsifier.md`
- Pivot decision (if any): Treat this as a hard competitor baseline family. If the CA branch reduces to exact pruning with local packaging, stop claiming CA novelty.

### D. Williamson type Hadamard matrices with circulant components (2023) and Goethals--Seidel Difference Families with Symmetric or Skew Base Blocks (2018)
- Paper IDs: e517b186e1edfb3a865cb4eabbdd4e0f8570d2a3; 09ffbc2db12a717278cb6ab7782bdc54d975138b
- Why it is close: These are the family-level references most likely to absorb a weakly specified “CA for Hadamard search” claim into existing circulant / Goethals-Seidel work.
- Differentiation hypothesis: The project must define its state and neighborhood as support-space or defect-space local dynamics, not as a restatement of family parameters.
- Evidence artifact(s): `results/analysis/branch_brief.md`; `results/analysis/verifier_contracts.md`; `sources.bib`
- Pivot decision (if any): Keep as an explicit collapse check. If the implementation starts exploiting family-specific parameter search rather than local dynamics, pivot or stop.

### E. Combinatorial Designs and Cellular Automata: A Survey (2025), Bent Functions from Cellular Automata (2020), and Heuristic search of (semi-)bent functions based on cellular automata (2021)
- Paper IDs: 44871e8b22b10f05e8ff1eaec72e3fe125c83c50; 792b2568f1335f14e5282dd837943d109fbb4b85; d0ef2d96e201af37ae7bf3535d21a4ac29c6f6b3
- Why it is close: These are the strongest CA-side anchors for combinatorial design and cryptographic search problems.
- Differentiation hypothesis: The work remains distinct only if it stays tied to the exact `167/80` obstruction or the published `64`-modular seed and reports matched same-representation baselines.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/phase1_multiagent_synthesis.md`; `results/analysis/baseline_benchmark_sheet.md`
- Pivot decision (if any): Use as methodological context, not as proof that CA novelty for Hadamard search survives by default.

### F. Finding a Hadamard matrix by simulated annealing of spin vectors (2016), Finding a Hadamard Matrix by Simulated Quantum Annealing (2018), Quantum computing formulation of some classical Hadamard matrix searching methods (2022), and A quantum approximate optimization method for finding Hadamard matrices (2025)
- Paper IDs: b01723f49ef6134f64d4675cc9a0d747eb29350b; d98246df005a52ff9a5e99b6c5f548c1def1ba12; 1fd50d1147b7684686e533886b44a9e92ac2e807; 8a06d7ef189e83b6ac474ddbcb623f02a635e286
- Why it is close: These are the strongest direct heuristic competitors already aimed at Hadamard search.
- Differentiation hypothesis: The CA branch must beat or at least alter reachability relative to same-neighborhood local search; otherwise it is only another heuristic wrapper.
- Evidence artifact(s): `results/analysis/baseline_benchmark_sheet.md`; `results/analysis/kill_rules.md`; `results/swarm/falsifier.md`
- Pivot decision (if any): Keep as the comparator family behind the stop/go decision. If the CA does not outperform its direct local-search analogue, stop.

## Final Execution Audit

The literature and experiment packets now support final pass or fail calls on the actual executed branches.

### Executed `H1` support-space CA
- Differentiation call: pass against the lexical watchlist and against family-parameter restatement risk.
- Contribution call: fail as a surviving method claim.
- Evidence artifact(s): `results/analysis/h1_design_brief.md`; `results/analysis/experiment_readout.md`; `results/analysis/phase2_baseline_review.md`
- Final decision: retire. The branch was specific enough to test fairly, but matched direct search beat it on both decisive sweeps.

### Executed `H2` structured defect-transport CA
- Differentiation call: pass against the lexical watchlist and against the claim that it merely republishes Eliahou's seed.
- Contribution call: fail as a surviving method claim.
- Evidence artifact(s): `results/analysis/h2_design_brief.md`; `results/analysis/experiment_readout.md`; `results/analysis/phase2_baseline_review.md`
- Final decision: retire. The toy ladder is weakly positive at best, while the decisive order-`668` attempt ties the matched non-CA baseline exactly.

### Literal `cellar` / pushdown reserve branch
- Differentiation call: pass relative to the executed CA branches.
- Contribution call: fail as a surviving method claim under the exact tail-panel encoding that was actually executed.
- Evidence artifact(s): `results/analysis/cellar_design_brief.md`; `results/analysis/cellar_prefix_complexity.md`; `results/analysis/cellar_no_go.md`; `results/experiments/cellar_phase6.json`
- Final decision: retire under the implemented exact encoding. The matched static boundary-debt residual state already closes the solved `4 x 79` control exactly, and the real `167/80` plus degraded `668` anchor panels do not expose any stack-only advantage. Reopen only if a future branch changes the value proposition from raw stack memory to compression, transfer, or proof-carrying feedback under a different comparator.

### `convolution_slice_ca` reserve branch
- Differentiation call: pass if and only if the liability-field state is treated as the primary object, not as a relabeling of raw support search.
- Contribution call: unresolved and unvalidated.
- Evidence artifact(s): `results/concept_evolve/probe_result.json`; `results/analysis/phase3_hypothesis_selection.md`
- Final decision: keep as reserve. It is the cleanest H1-side reopen candidate, but only with a same-representation non-CA comparator.

### `sat_user_propagator_ca` reserve branch
- Differentiation call: borderline.
- Contribution call: unresolved and unvalidated.
- Evidence artifact(s): `results/concept_evolve/probe_result.json`; `results/analysis/phase3_hypothesis_selection.md`
- Final decision: keep as reserve only if exact conflicts are recycled into online proposal updates; otherwise retire it as SAT+CAS with CA branding.
