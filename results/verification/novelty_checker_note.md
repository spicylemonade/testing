# Novelty Checker Note

## Overall Verdict

The claimed contribution is only narrowly distinct from prior work.

- The closest **true** overlap in the named list is `A 64-Modular Hadamard Matrix of Order 668 (2025)`, because every active branch is defined around that exact frontier seed and defect profile.
- The closest **method-shape** overlap in the named list is `Cellular Automata Applications in Shortest Path Problem (2017)`, because it is genuine prior art for CA as a local search / propagation heuristic on a hard combinatorial problem.
- The other named papers are mostly lexical false positives, not substantive prior art for the current branch set.

Current branch-level verdict:

- `H1_defect_syndrome_ca_64m` survives only as a **conditional** novelty claim: seeded defect-repair CA on the recovered order-668 frontier object, under matched non-CA controls, with exactness as the gate.
- In its **current implementation**, H1 does **not yet** survive as a strongly distinct CA repair method. The weak point is explicit in the repo artifacts: it computes exact per-packet deltas over all `334` packets, and the current frontier evidence shows diffusion or paralysis rather than a clear CA-specific advantage.
- `H2_lag_space_ca_167` is only potentially novel if it opens and passes the family-leakage audit; for now it is a gated backup, not an earned contribution.
- `H3_spacetime_row_emission_ca` is the most novelty-fragile branch because it sits closest to direct CA-construction literature; keeping it reserve-only is correct.

## Named-Paper Comparison

## 1. Cellular Automata Applications in Shortest Path Problem (2017)

Why it is close:

- It is real CA-for-search prior art, not just a lexical match.
- It weakens any broad claim that "using CA for hard search is new."

Material differentiation still available:

- H1 is not a graph shortest-path CA. Its state is a seeded order-668 defect field over compact q/s coordinates, with exact Hadamard certification as the gate.
- The branch is benchmarked against matched greedy/tabu/annealing controls instead of claiming CA novelty by default.

Weak differentiation to state explicitly:

- If H1 continues to work by exact per-packet scoring over all packets, with neighborhood smoothing acting mainly as a wrapper, the distinction from generic CA-flavored local search becomes weak.
- In that case, the honest claim is not "new CA method," but "domain transfer of local repair heuristics to a seeded Hadamard search problem."

Branch verdict:

- H1 is only weakly differentiated right now.
- H2 is more distinct in principle, but only if it avoids collapse into known structured-family search.
- H3 overlaps too strongly with generic CA-search rhetoric to deserve activation without tighter evidence.

## 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)

Why it is close:

- Only at the lexical level: automata-based optimization on a structured decision problem.

Material differentiation:

- This is learning automata, not cellular automata.
- It is a scheduling/control problem, not an exact combinatorial-design search problem seeded by a known near-solution.

Weak differentiation to state explicitly:

- Do not use broad "automata are untried here" language. That wording is weaker than the actual branch definition.

Branch verdict:

- No substantive novelty threat to H1/H2/H3 beyond language discipline.

## 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)

Why it is close:

- It is not genuinely close. It is a search false positive caused by the token `automata`.

Material differentiation:

- Different domain, different objective, different state, different verification regime.

Weak differentiation to state explicitly:

- None beyond acknowledging that it is not meaningful prior art for this task.

Branch verdict:

- No novelty threat. Treat as lexical noise only.

## 4. Engineering Societies in the Agents World (2000)

Why it is close:

- Only through distributed-update or agent rhetoric, not through mathematical or algorithmic overlap.

Material differentiation:

- Multi-agent systems are not cellular automata, not Hadamard search, and not exact certification from a seeded near-solution.

Weak differentiation to state explicitly:

- Avoid agent-society language when describing H1/H2/H3. That rhetoric would make the branch sound broader and weaker than it is.

Branch verdict:

- No substantive novelty threat. The risk is rhetorical drift, not prior-art collision.

## 5. A 64-Modular Hadamard Matrix of Order 668 (2025)

Why it is close:

- This is the true frontier anchor, not just a nearby paper.
- H1, H2, and H3 all inherit their legitimacy from the recovered seed and defect profile in this paper.

Material differentiation still available:

- The 2025 paper is a construction of a `64`-modular near-solution, not a CA search or exact repair method.
- The active claim is narrower: use that frontier object as the seed for an exact-search repair dynamic, with matched non-CA baselines and exact-hit reporting.

Weak differentiation to state explicitly:

- Any result short of exact orthogonality is not materially different from "another optimizer on top of the 2025 frontier object."
- If H1 only improves approximate defect behavior, or if it never beats matched baselines, then the branch does not survive as a distinct method claim.
- The current probe and precheck artifacts already point in that direction: the single-bit q/s packet basis appears frozen on the canonical seed, and the implemented H1 branch currently alternates between support diffusion and seed-preserving paralysis.

Branch verdict:

- This is the strongest overlap and the main novelty constraint.
- H1 currently survives only as a **testable hypothesis**, not as a demonstrated distinct CA repair method.

## Branch-Specific Novelty Risk

### H1

- Best-case novelty: seeded defect-repair CA on the actual order-668 frontier object, with compressed q/s + lag-syndrome state and matched controls.
- Main risk: collapse into packetwise local search due to global per-packet delta evaluation.
- Current status: novelty is **plausible but unproven**, and weakly differentiated at best.

### H2

- Best-case novelty: lag-defect field as the operative CA state, rather than raw sequence-family syntax.
- Main risk: silent collapse into Williamson/Turyn/Goethals-Seidel/cocyclic/block-circulant search.
- Current status: novelty is only hypothetical until the family-leakage audit is passed.

### H3

- Best-case novelty: compact spacetime rule family expressive enough to mimic the frontier defect profile.
- Main risk: direct overlap with existing CA-construction literature and generic rule-table search.
- Current status: not strong enough to open; reserve-only is the correct position.

## Bottom Line

The work is materially different from the named prior art **only if** it is described and evaluated narrowly:

- CA as a seeded repair heuristic on top of the recovered 2025 order-668 frontier object
- matched against non-CA controls in the same coordinates
- judged by exact hits first
- and abandoned if it collapses into local search or structured-family optimization

The weakest point is H1. Right now it does **not** yet survive as a clearly distinct CA repair method; it survives only as a narrow hypothesis that still needs matched frontier evidence to avoid collapsing into "local search with CA vocabulary."
