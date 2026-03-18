# Verification Summary

## Decision

Current work should: `REVISE`

The evidence packet supports only a narrow negative-result claim: the implemented `H1` and `H2` cellular-automata branches were benchmarked against matched non-CA controls and did not beat those controls. The packet does not support a broader novelty claim, a broad `CA for Hadamard search` claim, or a publication-grade benchmark claim without further cleanup and expansion.

## Must-Fix Issues

1. Narrow the claim everywhere to the supported no-go result.
   - Remove or rewrite any language implying positive method novelty, broad CA novelty, or a validated route to order `668`.
   - Keep the contribution tied to the exact `H1` `167/80` cyclic obstruction and the exact `H2` mod-`64` seed benchmark under matched controls.

2. Repair the citation layer before any manuscript-facing use.
   - Add the missing `Suksmono 2019` quantum-annealing source if that comparison remains.
   - Fix or delete the misattributed reserve-memo references in `results/swarm/gap_map.md` and `results/swarm/hypothesis_negative_space.md`.
   - Replace unsupported anchors such as OEIS where an in-scope primary source already exists.
   - Mark literature-search statements as scoped search conclusions unless they are backed by a concrete cited source.

3. State the benchmark limits explicitly in downstream prose.
   - `H1` has a fair matched comparison, but the solved same-template control does not recover an exact certificate under the locked budget.
   - `H2` is only tested on one real degraded `668` start and only for the executed `s`-local-repair branch.
   - The packet has no CA ablation matrix, no budget ladder, and only one serious non-CA comparator (`direct_greedy`).

4. Keep reserve branches out of the validated contribution unless they are separately executed.
   - `autocorrelation_debt_pushdown`, `sat_user_propagator_ca`, and `convolution_slice_ca` remain hypotheses, not verified methods.
   - Do not let naming or speculative mechanism language drift into the final verified claim.

## Optional Improvements

These are optional for a narrow negative-result packet, but they become required if the goal shifts toward a broader publication-facing benchmark contribution.

1. Make at least one solved same-template positive control recover exactly under the published evaluation stack.
2. Expand `H2` to a prespecified panel of degraded real `668` starts, including stronger perturbations and, if relevant, `q`-only or mixed `(q,s)` variants.
3. Run a preregistered CA ablation matrix over `window`, `min_gain`, `phase_move_cap`, and budget.
4. Add at least one stronger same-representation non-CA heuristic baseline per branch.
5. Improve artifact auditability by serializing fairness parameters for every method and reporting paired wins/losses, orbit coverage, and best-vs-final tradeoff diagnostics.
6. If reserve branches stay in scope, formalize their source maps and benchmark them against matched non-CA comparators instead of discussing them only at the concept level.

## Actionable Bottom Line

- Acceptable after revision: a narrow branch-specific no-go packet.
- Not acceptable yet: a broader novelty claim or a publication-grade benchmark paper.
- Next gate: revise the narrative and citation layer first; only deepen the experiments if the project still wants a broader claim than the current negative-result packet can support.
