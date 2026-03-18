# Problem Statement

The target of this run is an **exact real Hadamard matrix of order `668`**, not a modular relaxation, not a near-Hadamard object, and not a new construction claim for Hadamard matrices in general.

The current frontier anchor is the 2025 paper **A 64-Modular Hadamard Matrix of Order 668**. That object is a strong near-solution and a valid research seed, but it is **not** an exact Hadamard matrix. The run therefore treats the frontier object as input state for search, not as a solved endpoint.

The user phrase `cellar automata` is treated here as `cellular automata` unless a different technical meaning is later supplied. No separate `cellar automata` method family is evidenced in the repo context or the targeted literature recovered so far.

The narrow branch claim is:

- Use cellular automata as a **seeded repair dynamic** on the published order-`668` frontier object.
- Keep the search state in a compressed defect or generating-sequence representation rather than on a raw `668 x 668` sign lattice.
- Judge the method by exact-feasibility outcomes under seed-matched controls, not by prettier defect traces or smaller modular residuals alone.

This means the concrete research question is not "can CA construct Hadamard matrices in general?" It is:

> Can a compressed, genuinely local cellular-automaton repair dynamic, seeded from the published `64`-modular order-`668` object, reach exact orthogonality or at least outperform matched non-CA repair baselines on the same seed?

Success criteria for this run:

- Recover and canonicalize the published `64`-modular order-`668` seed data.
- Implement one CA repair branch and matched non-CA baselines in the same coordinates.
- Evaluate exact-hit rate first, with defect metrics only as secondary diagnostics.

Non-success conditions:

- Any result that improves defect count or modular structure without reaching exact orthogonality remains a near-solution result, not a solution of Hadamard `668`.
- Any branch that collapses into ordinary local search or optimizer-over-known-family wording loses the intended novelty claim and must be relabeled accordingly.
