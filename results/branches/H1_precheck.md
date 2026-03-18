# H1 Precheck

This precheck is for the implemented branch in `hadamard_ca/h1_ca.py` under `results/branches/H1_defect_syndrome_ca_64m_config.json`, not for the abstract H1 idea.

It synthesizes:

- `results/swarm/falsifier.md`
- `results/swarm/hypotheses.json`
- `results/swarm/hypothesis_negative_space.md`
- `results/swarm/hypothesis_bridge.md`
- `results/verification/benchmark_spec.md`
- `results/verification/benchmark_gate.md`
- `results/branches/H1_smoke_control.json`
- `results/branches/H1_smoke_cli.json`
- `results/branches/H1_frontier_micro_smoke.json`
- `results/branches/H1_frontier_sensitivity_probe.json`

## Predicted Failure Modes

1. The current single-bit packet basis may already be frozen.
   - `results/concept_evolve/probe_result.json` reports no improving one-packet or two-packet moves on the canonical seed in the present q/s packet basis.
   - If that probe result is directionally correct, rule tuning alone cannot rescue H1; the actuator basis itself is the blocker.

2. Support diffusion under local pressure.
   - `results/branches/H1_frontier_micro_smoke.json` shows the concrete danger already: support can grow far beyond the seed's `13` active lags even while `l1` and `max_abs` improve temporarily.
   - If this persists under matched controls, H1 fails because it is optimizing the wrong local proxy.

3. Plateau at the seed after spill control.
   - `results/branches/H1_frontier_sensitivity_probe.json` shows the opposite failure mode: 8 small parameter variants all stay at the original seed objective.
   - If stronger spill control only freezes H1 at the frontier seed, the branch is too conservative to be useful.

4. Local-rule leakage into global move scoring.
   - `_packet_pressures(...)` computes an exact delta for every packet at every view.
   - That keeps the branch compressed, but if the neighborhood terms are not doing real work, H1 collapses into packetwise local search with CA vocabulary.

5. Oscillation and refractory miscalibration.
   - If `refractory_steps` and `refractory_penalty` are too weak, packets chatter around the same defect cluster.
   - If they are too strong, the branch freezes before any productive defect transport can happen.

6. Synchrony can destroy locality.
   - If `max_active_packets` or the coupling weights are too high, H1 stops looking like a sparse asynchronous repair process and becomes a correlated burst heuristic.
   - That both weakens the CA claim and increases the risk of defect diffusion.

## Parameter Axes Worth Exploring

1. Spill control.
   - `spill_l1_penalty`
   - `spill_support_penalty`
   - `active_lag_bonus`
   - Reason: these determine whether H1 tolerates support spill or becomes too conservative to move.

2. Neighborhood geometry.
   - `lag_neighborhood_radius`
   - `packet_neighborhood_radius`
   - `same_channel_weight`
   - `cross_channel_weight`
   - Reason: these determine how local the defect-syndrome coupling really is.

3. Activation sparsity.
   - `activation_threshold`
   - `max_active_packets`
   - `fallback_best_packet`
   - Reason: these decide whether H1 behaves as a sparse CA update or as a broad synchronized perturbation rule.

4. Refractory and stagnation control.
   - `refractory_steps`
   - `refractory_penalty`
   - `stagnation_limit`
   - `restart_packet_flips`
   - Reason: these control oscillation, restart fragility, and how quickly the branch abandons a bad basin.

## Minimal Kill Test

Run one matched frontier batch on `results/frontier/order_668_64m/seed_sequences.json` with:

- the locked non-CA budget/restart policy from `results/verification/benchmark_spec.md`
- the current H1 branch
- `greedy`
- `tabu`
- `simulated_annealing`
- `stochastic_hillclimb`

Kill H1 immediately if all of the following hold in that first batch:

- `exact_hit_rate = 0`
- the best H1 objective never beats the seed objective
- the median terminal support is not strictly better than the best matched non-CA baseline, or H1 diffuses support above the seed support on most restarts

If that happens, do not broaden the H1 sweep. Only move to the H2 gate if the failure looks principled and locality-driven rather than like a weak implementation.

## Local Readout Before Matched Runs

- `results/branches/H1_smoke_control.json` and `results/branches/H1_smoke_cli.json` confirm that H1 is executable and can repair the shared small non-exact control.
- `results/concept_evolve/probe_result.json` adds a stronger structural warning: the current single-bit q/s packet basis appears frozen on the canonical seed, so H1 may need a different actuator library rather than just different rule weights.
- `results/branches/H1_frontier_micro_smoke.json` shows the first frontier-side failure mode: temporary `l1` / `max_abs` improvement paired with support diffusion well beyond the seed support.
- `results/branches/H1_frontier_sensitivity_probe.json` shows the second frontier-side failure mode: stronger spill control avoids diffusion but leaves H1 pinned to the original seed objective across 8 small variants.
- The immediate branch risk is therefore bifurcated: H1 currently oscillates between diffusion and paralysis on the real order-668 seed.

## Anti-Pattern

H1 collapses into generic local search if it becomes:

- exact per-packet move scoring over all `334` packets at every step
- followed by selecting the best packet or best few packets
- with the neighborhood smoothing and refractory terms acting only as tie-breakers

At that point the method is no longer a distinct CA repair dynamic. It is a greedy/tabu-style move evaluator with CA vocabulary pasted over it.

## Immediate Next Experiment

Use the current H1 config and the locked baseline accounting on:

1. the two solved smaller controls, then
2. the canonical order-668 frontier seed

Report exact-hit rate first. Treat lower `l1`, lower `max_abs`, or prettier traces as diagnostic only unless they survive `results/verification/benchmark_gate.md`.
