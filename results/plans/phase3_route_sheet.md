# Phase 3 Route Sheet

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Champion route: `H1`

## 1. `H1` Route Identity

Active label:
- `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`

Non-claims:

- This is not a new one-vertex extension algorithm.
- This is not a generic improved lower-bound search engine.
- This is not a new emptiness checker for `R(5,5,43)`.
- This route gets structural credit only if the obstruction objects transfer across parent families and survive witness-safety audits.

## 2. Canonical `H1` Data Model

| Object | Required fields | Source of truth at `Rung 0` | Planned artifact |
| --- | --- | --- | --- |
| `frontier_parent` | `parent_id`, provenance paper, source encoding, canonical label, automorphism order, orbit partition, degree profile, seed family, known status | Exoo 1989, Ge et al. 2022, Lehavi 2024, fixed Ramsey corpus | `results/h1/frontier_parents.jsonl` |
| `extension_case` | `extension_id`, `parent_id`, orbit class id, neighborhood signature, color pattern to parent vertices, symmetry representative, generation rule, status | Orbit-distinct `42 -> 43` extension reconstruction | `results/h1/extension_cases.jsonl` |
| `failure_witness` | `witness_id`, `extension_id`, monochromatic color, forced `K_5` vertex set, minimality check status, local pattern hash, extraction method | Witness extractor over failed extensions | `results/h1/failure_witnesses.jsonl` |
| `minimal_obstruction_core` | `core_id`, canonical core encoding, support size, color pattern, canonical hash, supporting witness ids, minimality proof status | Canonicalization pass over failure witnesses | `results/h1/obstruction_cores.jsonl` |
| `transfer_record` | `core_id`, held-out parent id, recurrence outcome, coverage fraction, witness-safety status, failure reason | Leave-one-parent-out evaluation | `results/h1/transfer_records.jsonl` |

## 3. Explicit Input Artifacts

Existing repo inputs:

- `results/literature/literature_snapshot.json`
- `results/swarm/phase1_cleanup.md`
- `results/plans/phase2_baseline_sheet.md`
- `results/plans/ramsey_research_program.md`
- `results/literature/ss_search_vertex_extension.json`
- `results/concept_evolve/tree/001_orbit_stable_obstruction_atlas/concept.json`
- `results/concept_evolve/tree/002_minimal_core_canonicalization/concept.json`
- `results/concept_evolve/tree/003_leave_one_parent_out_transfer/concept.json`
- `results/concept_evolve/tree/004_witness_safe_filter_bank/concept.json`

External source packets to reconstruct into local artifacts:

- Exoo 1989 lower-bound witness family
- Ge et al. 2022 study of Exoo's lower bound
- Lehavi 2024 one-vertex extension and counterexample checking line

## 4. Explicit Output Artifacts

- `results/h1/frontier_parents.jsonl`
- `results/h1/extension_cases.jsonl`
- `results/h1/failure_witnesses.jsonl`
- `results/h1/obstruction_cores.jsonl`
- `results/h1/transfer_records.jsonl`
- `results/h1/atlas_summary.md`
- `results/h1/witness_safety_audit.md`

## 5. Falsifiable `H1` Claims

- Recurrence claim: after canonicalization, a dictionary of at most 25 obstruction cores covers at least 30 percent of failed orbit-distinct `42 -> 43` extensions across at least 3 non-isomorphic parent families.
- Transfer claim: under leave-one-parent-out evaluation, at least half of the training-side coverage achieved by the recurring cores survives on the held-out parent family.
- Witness-safety claim: every core-derived pruning rule preserves all known `42`- and `43`-vertex witnesses.
- Reuse claim: at least one recurring core family is reusable both as lower-bound pruning evidence and as an upper-bound lemma candidate without changing its canonical identity.

## 6. Immediate `Rung 0` Deliverable

Before any scale-up, materialize the schema itself:

- reconstruct a local packet of `frontier_parent` records from the Exoo, Ge, and Lehavi line
- reconstruct orbit-distinct `extension_case` records for the first decisive parent packet
- extract `failure_witness` examples with canonical hashes
- confirm that every planned field can be filled from a local artifact or a reproducible import step
