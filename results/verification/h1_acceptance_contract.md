# H1 Acceptance Contract

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Active hypothesis: `H1`

This file freezes the authoritative pass/fail contract for `H1` under the current packet.

## Current Memo-Safe State

- `H1` is a route target only.
- No bound-improvement claim is allowed.
- No established structural intermediate claim is allowed.
- The only memo-safe end product today is a constrained no-go or planning memo that reports the route, gates, blockers, and negative-control rules honestly.

## Preconditions Before Any `H1` Execution Claim

Before any memo may say that `Rung 0` has started or that an `H1` artifact exists, the packet must have:

1. A local `frontier_parent` / `extension_case` / `failure_witness` corpus.
2. An orbit-distinct `42 -> 43` extension enumerator.
3. A frozen matched-compute tuple and failure-code taxonomy.
4. A citation packet that is sufficient for the constrained memo scope.

## Structural Intermediate Result Contract

`H1` counts as a structural intermediate result only if all of the following are true:

1. `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, and `results/h1/failure_witnesses.jsonl` exist and cover at least 3 non-isomorphic parent families.
2. `results/h1/obstruction_cores.jsonl` and `results/h1/atlas_summary.md` show that the top recurring cores cover at least 30 percent of failed orbit-distinct `42 -> 43` extensions across those families.
3. `results/h1/transfer_records.jsonl` shows leave-one-parent-out held-out coverage of at least 50 percent of training-side coverage on the decisive `anti_exoo_holdout`.
4. `results/h1/witness_safety_audit.md` records zero known-witness deletions.
5. The comparison and replay metadata remain consistent with the fixed matched-compute tuple.

If any one of these fails, `H1` remains a route target or negative result, not a structural intermediate result.

## Bound-Improvement Contract

The project may claim a bound improvement only if it produces either:

- an independently verified `44`-vertex witness, or
- a machine-checkable `45`-vertex impossibility proof.

Nothing else counts as `improves bound`.

## Failure Codes That Demote Or Kill `H1`

- `anti_exoo_holdout`: held-out transfer collapses on the decisive non-Exoo-like family
- `witness_killed`: any candidate filter deletes a known `42`- or `43`-vertex witness
- `rare_core_tail`: the first atlas leaves a large uncovered tail with no dominant second cluster
- `stale_baseline`: matched-compute tuple or comparison object drifts
- `missing_certificate_path`: any upper-bound implication lacks a replayable certificate path

## Interpretation Rule

Until the `results/h1/*` artifacts above exist and pass these gates, the correct outward-facing sentence is:

`H1 remains a constrained route target for R(5,5), not an achieved structural contribution.`
