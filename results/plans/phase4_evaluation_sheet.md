# Phase 4 Evaluation Sheet

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Active hypothesis: `H1`

## 1. Experiment Entry Reframe

Source:
- `results/concept_evolve/reframings.json`

Use the reframe pass only to sharpen the existing promoted folders:

- orbit-quotiented atlas construction
- canonical core compression
- leave-one-parent-out validation
- witness-safe filter auditing

Do not widen the route set during Phase 4.

## 2. Fastest Invalidators

Start from the cheapest falsifiers named by the current falsifier and probe artifacts:

1. `anti_exoo_holdout`: if held-out coverage collapses on the most non-Exoo-like family, kill or demote `H1`.
2. `witness_pressure`: if any core-derived filter kills a known `42`- or `43`-vertex witness, kill or demote `H1`.
3. `rare_core_tail`: if the first atlas pass leaves a large uncovered tail with no dominant second cluster, do not scale up.

## 3. Exact Experiment Ladder

`Rung 0` — frontier reconstruction pass
- Goal: reconstruct the Exoo/Ge/Lehavi packet as local `frontier_parent`, `extension_case`, and `failure_witness` records.
- Expected artifact: `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, `results/h1/failure_witnesses.jsonl`

`Rung 1` — atlas pass
- Goal: canonicalize the first obstruction atlas over the reconstructed packet.
- Expected artifact: `results/h1/obstruction_cores.jsonl`, `results/h1/atlas_summary.md`

`Rung 2` — held-out transfer pass
- Goal: rerun the atlas with one parent family held out and measure coverage retention.
- Expected artifact: `results/h1/transfer_records.jsonl`

`Rung 3` — witness-safety pass
- Goal: run the witness-survival matrix and per-filter ablations before any expansion.
- Expected artifact: `results/h1/witness_safety_audit.md`

Expansion gate:

- No broader compute, no H2 opening, and no structural claim beyond intermediate evidence before all four rungs complete cleanly.
