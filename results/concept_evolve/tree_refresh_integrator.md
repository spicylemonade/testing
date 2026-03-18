# Tree Refresh Integrator

## Recommended Champion Branch

Promote `002_lag-residue-ca-167` as the refreshed champion branch.

Why this is the honest refresh:

- The H1 controls show `001_defect-syndrome-ca-64m` is executable, so the kill result is not a trivial implementation failure.
- The frontier evidence and the probe agree on the failure mode: the current q/s packet basis is fake-local and frozen on the canonical seed. The probe reports a median one-packet splash over about `51` lag slots, no improving one-packet or two-packet moves, and the verification pack shows H1 never beats the published order-668 seed objective.
- `results/branches/H2_gate.md` says that locality / actuator-basis mismatch is exactly the condition that justifies opening H2.
- `002_lag-residue-ca-167` moves the state onto the lag-defect object over the prime core `167`, which is the narrowest next branch that still matches the observed failure signature without widening into H3.

## Promoted Bridges

1. `008_ldpc-hadamard-decoder-graph` should be promoted as a bridge into `002`, not as a standalone champion.
   - Carry over sparse-syndrome graphing, weighted or collective local flips, defect voting, cluster labels, and message-passing style controls.
   - Do not let this become generic decoder-over-global-score search; its role is local mechanism support for H2.

2. `001_defect-syndrome-ca-64m` should be kept only as an evidence bridge into `002`.
   - Preserve the falsification lessons: raw q/s adjacency is not honest locality, hidden local state is mandatory, synchronous monotone updates are dead on the canonical seed, and locality has to be audited by instrumentation rather than asserted rhetorically.

## Retired Branches

- Retire `001_defect-syndrome-ca-64m` as an active frontier branch. Keep it as the archived falsification record for the single-packet q/s CA hypothesis.
- Retire `008_ldpc-hadamard-decoder-graph` as an independent branch candidate. Its value after the H1 kill test is bridge value, not tree-top value.
- Keep `011_spacetime-row-emission-search` closed and retired from the active refresh. The novelty pack says H3 remains shut, and the tree should not spend new budget there unless H2 also fails for representation reasons and the direct CA-construction overlap audit is passed.

## Backlog Themes The Refresh Should Encode

1. `Lag-space locality first`
   - Rewrite the surviving branch backlog around lag residues, defect cells, or a derived defect-actuator influence graph over the prime core `167`, not raw q/s index neighborhoods.

2. `Family-leakage audit before budget`
   - Make Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant leakage checks the first gate on H2. If the branch depends on any of them, relabel it as optimizer-over-known-family instead of a new CA branch.

3. `One representation, one matched control, smaller first budget`
   - Open H2 with exactly one lag-space representation, one matched non-CA lag-space control, and a tighter budget than H1 until locality survives the first audit.

4. `Decoder-style local memory, not decoder takeover`
   - Import from `008` only the local mechanisms that match the evidence: signed defect votes, collective flips, defect aging, cluster labels, and message passing on sparse defect graphs.

5. `Asynchronous updates and bounded local barrier crossing`
   - Encode refractory timers, local auctions, or capped worsening bursts as first-class backlog items, because strict monotone and synchronous updates are already falsified on the canonical seed.

6. `Explicit locality instrumentation as a kill switch`
   - Track changed-lag footprint, touched-edge count, active neighborhood size, message count, scan width, and dependence on global objective queries on every serious run. If these drift toward whole-state behavior, stop or relabel the branch early.

7. `Canonical-seed discipline`
   - Keep the refreshed backlog anchored to the real order-668 frontier seed and matched controls. Do not treat success on lightly perturbed near-solutions as evidence that the real bottleneck is solved.

8. `No H3 backlog expansion`
   - Under `011`, encode only the closed-status marker and its reopen condition. Do not add generative or spacetime-rule buildout tasks in this refresh.

## Net Refresh Decision

The tree should now read as: `002` becomes champion, `008` survives as a bridge-only mechanism donor, `001` is retired as an active branch but retained as the falsification record, and `011` stays closed.
