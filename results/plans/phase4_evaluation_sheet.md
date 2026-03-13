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

## 4. Prior-Work Evaluation Matrix

Every evaluation table in this project must include the following named comparison rows:

| Prior work | Shared comparison object | Required result-type column |
| --- | --- | --- |
| Exoo 1989 lower-bound line | verified witness family or parent lineage | `improves bound` / `improves certificate path` / `improves neither` |
| Ge et al. 2022, `Study of Exoo's Lower Bound for Ramsey number R(5,5)` | Exoo-line witness analysis and low-defect near-miss structure | `improves bound` / `improves certificate path` / `improves neither` |
| Lehavi 2024, `Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t` | one-vertex extension and counterexample-checking surface area | `improves bound` / `improves certificate path` / `improves neither` |
| Aija'am 2010, `Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)` | optimizer-only or symmetry-only lower-bound claims | `improves bound` / `improves certificate path` / `improves neither` |
| McKay-Radziszowski 1992, `A new upper bound on the Ramsey number R(5,5)` | exact upper-bound case-analysis ancestor | `improves bound` / `improves certificate path` / `improves neither` |
| Angeltveit-McKay 2018, `R(5,5) <= 48` | exact upper-bound decomposition and residue line | `improves bound` / `improves certificate path` / `improves neither` |
| Angeltveit-McKay 2024, `R(5,5) <= 46` | current best published upper-bound line | `improves bound` / `improves certificate path` / `improves neither` |
| Gauthier 2025, `Decreasing the upper bound on the Ramsey number R(5,5)` | split-vertex and transverse-edge gluing successor line | `improves bound` / `improves certificate path` / `improves neither` |

Comparison-table rule:

- No row is allowed to compare an `H1` structural object to an upper-bound paper without filling the `shared comparison object` column first.

## 5. Compute Governance And Fail-Fast Pivot Map

| Stop condition | Meaning | Action |
| --- | --- | --- |
| Proxy-only gain | Better defect score, pruning count, branch count, or solver speed without a witness or certificate path | Roll back the claim to intermediate evidence only |
| Unsound pruning | Any core-derived filter kills a known `42`- or `43`-vertex witness | Shut down that branch immediately and record the failure code `witness_killed` |
| Non-transfer | Held-out coverage falls below the `H1` floor or the atlas collapses to one family | Kill or demote `H1` and keep `H2` as the only next pivot |
| Missing certificate path | Upper-bound residue cannot be rationalized, replayed, or checked | Block any upper-bound claim and relabel the artifact as `residue_only` |
| Stale baseline | Candidate and baseline use mismatched compute tuples or tuning privileges | Re-audit the comparison and invalidate the headline table until the manifest is frozen |
| Overfit seed family | Gains disappear off Exoo-like seeds or one family contributes more than half of accepted support | Demote the result to overfit evidence and stop scaling compute on that branch |
| Replay failure | Witness or certificate artifact cannot be replayed outside the generating workflow | Treat the artifact as unverified and stop any publishability claim |

Authorization rule:

- No expensive run is authorized unless the benchmark manifest, failure-code taxonomy, and replay path are fixed in advance.
