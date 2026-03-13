# Tool Plan

## Global Governance

- Operate in synthesis-only mode. Do not run new benchmark scripts, solver explorations, constructive algorithm searches, notebooks, or broad literature expansion in this stage.
- Treat [gap_map.md](/home/archivara/work/repo/results/swarm/gap_map.md) as the main usable positive signal, but cap all novelty claims at provisional because `results/swarm/hypothesis_bridge.md`, `results/swarm/hypothesis_negative_space.md`, and `results/swarm/falsifier.md` are missing.
- Run quick kill checks before deepening any direction. Only the champion hypothesis receives researcher time unless it is falsified.
- Use the current watchlist and frontier files mainly as evidence of query drift. Do not let off-target `gravity` matches become the effective bibliography for the gravity-sim problem.
- Honor the budget envelope: synthesize specialist outputs and avoid rerunning wide searches unless a blocker makes a narrow correction pass unavoidable.

## Role Routing

### Orchestrator

- Route `H1` as champion and `H2` as backup. Keep `H3` parked unless both earlier directions fail.
- Enforce the blocker gate: if the missing scout files remain absent, require every downstream role to preserve the provisional label on novelty claims.
- Stop any role that drifts from synthesis into implementation or wide exploration.
- Budget envelope: 1 coordination pass, 1 blocker-resolution check, 0 wide-search passes.

### Researcher

- Work only on the champion unless the orchestrator explicitly promotes the backup.
- First task is narrow evidence collection for the chosen hypothesis and explicit blocker logging around the missing scout artifacts, not breadth-first implementation.
- Keep the evidence plan closed-set: one feature matrix and up to three canonical scenarios.
- Budget envelope: 1 closed-set feature audit, up to 3 canonical scenarios, 1 targeted prior-art correction pass, 0 broad search passes.

### Falsifier

- Try to kill the champion quickly by finding an existing system that already satisfies the proposed differentiation or by showing that the claim collapses under a simple counterexample.
- If the champion survives, repeat once on the backup. Do not spend cycles on `H3` unless both higher-priority directions survive.
- Escalate immediately if the missing `results/swarm/falsifier.md` artifact prevents a clear kill or survive judgment.
- Budget envelope: 2 short passes total, 1 pass per live hypothesis, stop at first decisive kill.

### Writer

- Write only after the falsifier pass.
- Frame the contribution as a scoped systems claim for a gravity simulator, not as a first-ever gravity-sim claim.
- Carry the blocker note forward if the missing scout files are still unresolved.
- Budget envelope: 1 draft and 1 revision, champion-first, no speculative expansion.

### Reviewer

- Review for claim inflation, hidden assumptions, ignored overlap with mature N-body ecosystems, and any attempt to smuggle implementation work into synthesis.
- Reject drafts that do not state kill criteria or that omit the missing-input blocker.
- Budget envelope: 1 red-team review pass.

### Citation Auditor

- Replace off-target `gravity` keyword matches with directly relevant N-body or orbital-simulation references before any external-facing write-up.
- Require each novelty claim to name the closest real overlap system and a concrete differentiation sentence.
- Budget envelope: 1 closed citation pass on the champion and backup only, no bibliography sprawl.

### Benchmark Auditor

- Define evaluation obligations only. Do not run scripts in this stage.
- For `H1`, require long-horizon invariants, close-encounter detection, and intervention-correctness metrics.
- For `H2`, require replay determinism under declared runtime conditions and explicit fidelity-envelope reporting.
- For `H3`, require event-class coverage and explicit gradient-trust or fallback criteria if it is ever promoted.
- Budget envelope: 1 metric-spec pass, 0 execution passes.
