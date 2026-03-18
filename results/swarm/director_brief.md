# Director Brief

- Date: 2026-03-18
- Working interpretation: the swarm outputs consistently treat `cellar automata` as `cellular automata`. If that interpretation is wrong, pause and redefine the method family before any search work.

## Champion

`H1` Autocorrelation-Realization CA on the `167`-cycle.

This is the best first direction because it stays closest to the sharpest known obstruction in the local scout outputs: the missing length-`167`, weight-`80` support with the required autocorrelation profile. It is also the cleanest branch to falsify quickly. A matched-budget comparison against direct search on the same symmetry-reduced support space gives a clear go/no-go test, which keeps the novelty claim narrow and defensible.

Non-negotiable guardrails:

- Do not let the proposal collapse into a circulant / Williamson / Goethals-Seidel restatement with a CA wrapper.
- Do not compare only against random supports; the required control is direct search on the same structured space.
- Do not spend beyond one modest sweep unless the branch shows either an exact hit, a clear hit-rate advantage, or a reachability argument that justifies more budget.

## Backup

`H2` Defect-Transport CA lift from the `64`-modular order-`668` seed.

Keep this as the backup because it starts from the strongest known near-solution and has crisp verification metrics: modulus reached, defect count, and maximum defect magnitude. Its novelty claim is weaker than `H1`, because it can collapse into ordinary local search with CA branding, but it is still worth testing if `H1` dies early and cleanly.

Non-negotiable guardrails:

- Use the same seed, neighborhood, and move budget for the non-CA local-search baseline.
- Require solved smaller modulus-lift controls before spending on order `668`.
- Kill the branch if it cannot lift solved controls by one modulus step or cannot improve the published `64`-modular seed.

## Not Selected Now

Compressed/path-state CA variants remain on reserve only. The swarm outputs repeatedly warn that they are too easy to reinterpret as equivalence-aware branch-and-bound or SAT+CAS filtering, which weakens both the novelty claim and the falsification story.

## Blocker And Handoff

Two blockers remain before any researcher should build or run anything:

- If the user intended a literal non-cellular "`cellar automata`" model rather than cellular automata, stop and demand a one-page formal definition of that automaton and why it reaches a materially different search space.
- Even under the cellular-automata reading, the next step is still exact artifact extraction, not frontier search. The repo needs the exact `167/80` target and one solved same-template control in machine-usable form before the branch can be evaluated fairly.

## Exact Next Experiment

1. Reconstruct the exact `167/80` autocorrelation target and one solved same-template positive control.
2. Define a symmetry-aware direct-search baseline on that same support space.
3. Run one modest CA rule/seed sweep with reachability logging and compare exact-hit or closest-target performance against the matched baseline.
4. Promote `H2` only if `H1` fails that kill test without showing a nontrivial reachability advantage.
