# Novelty Report

Date: 2026-03-13
Owner role: `novelty_checker`
Rubric item: `item_018`
Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof
Reviewed artifacts:
- `results/plans/phase3_route_sheet.md`
- `results/swarm/phase3_stress_test.md`
- `results/swarm/phase1_cleanup.md`
- `results/literature/prior_art_gap.md`
- `results/concept_evolve/probe_result.json`
- `results/plans/ramsey_research_program.md`

## Audit Verdict

`H1` is only conditionally materially distinct from prior work on the present record. The claim is novelty-safe only if its top recurring cores cover at least 30 percent of failed orbit-distinct `42 -> 43` extensions across at least 3 non-isomorphic parent families, retain at least half of training-side coverage under leave-one-parent-out evaluation, and cause zero known-witness deletions. Without those properties, the differentiation is weak and collapses into another one-vertex-extension failure catalog.

## Closest Overlap For `H1`

The closest overlap is Lehavi 2024, `Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t`, because it occupies the same one-vertex-extension and counterexample-checking surface around failed `42 -> 43` extensions. Ge et al. 2022 remains a close lower-bound comparison row, but Lehavi is the sharper novelty threat because `H1` would look like a repackaged extension-checking workflow unless the output is a reusable cross-family obstruction object rather than more extension cases.

## Why `H2` And `H3` Are Demoted

`H2` is demoted because its nearest overlap is the split-vertex / transverse-edge gluing line, especially Gauthier 2025. Until an `H2` primitive clears the non-equivalence gate and beats that line on verified residue or certificate metrics under matched conditions, it is just the same proof object with a different solver, branch order, or decomposition presentation.

`H3` is demoted because it has no standalone novelty claim. Certificate packaging or proof logging only gets credit after an `H1` or `H2` structural object survives cross-family or cross-branch transfer and still reduces checked proof size or checker runtime. Before that, `H3` is infrastructure.

## Strongest Remaining Novelty Risk

The strongest remaining novelty risk is the `anti_exoo_holdout`: the atlas may memorize the Exoo lineage instead of discovering a reusable Ramsey object. If coverage collapses when the most Exoo-like family is held out, `H1` is not materially distinct from prior extension-checking work even if its in-family coverage looks strong.
