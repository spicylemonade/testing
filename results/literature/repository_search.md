# Repository and Formal-Tool Search

## Query 1 - Walnut / automatic Beatty and Ostrowski proofs
- Search mode: `codesearch` plus `webfetch` on the surfaced repository.
- Relevant tool: `Walnut-Theorem-Prover/Walnut` - https://github.com/Walnut-Theorem-Prover/Walnut
- Why it matters: Walnut is the reusable automata engine behind the quadratic-Ostrowski Beatty decidability lane and explicitly supports custom numeration systems and theorem-prover style automaton synthesis.
- Supporting web evidence: https://walnut-theorem-prover.github.io/ and the Walnut 2.0 Ostrowski manual cited by the `codesearch` result.

## Query 2 - Pecan / Buchi-automata theorem proving
- Search mode: `codesearch` plus `webfetch` on the surfaced repository.
- Relevant tool: `ReedOei/Pecan` - https://github.com/ReedOei/Pecan
- Why it matters: Pecan is the tool named in `Decidability for Sturmian words` for automated proofs over numeration systems and automatic words, so it is the closest existing executable infrastructure for our selector-definability experiments.

## Negative finding
- No targeted repository search surfaced a package that already solves the exact problem of detecting homogeneous linear-recurrence subsequences inside `floor(n r)` under frozen selector classes.
- Conclusion: Walnut and Pecan are the reusable formal-tool anchors, but the Beatty-LRS checker, modular-shadow diagnostics, and Pisot endpoint experiments must be implemented in this repository.
