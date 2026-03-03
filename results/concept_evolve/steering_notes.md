# Steering Notes

ConceptEvolve kickoff command was executed:

`python3 .archivara/concept_evolve.py evolve "create a minimal gravity sim"`

Observed artifacts (`tree/index.json`, `walk_paths.json`, `steering_directions.json`) are currently sparse, so steering was synthesized from available outputs plus repository/rubric constraints.

## Direction 1: Deterministic baseline-first pipeline

- **Concrete direction:** Build a deterministic O(N^2) Newtonian baseline with fixed-step integration, explicit CLI contract, and seeded scenario generation before advanced methods.
- **Informs rubric items:** `item_006`, `item_007`, `item_008`, `item_016`, `item_017`.
- **Expected signal:** Stable reproducibility (identical hashes under seed=42) and complete baseline metric coverage.

## Direction 2: Stability vs throughput dual-track research

- **Concrete direction:** Split innovation into two orthogonal tracks: (a) symplectic stability improvements and (b) scalable force approximation for large N.
- **Informs rubric items:** `item_011`, `item_012`, `item_013`, `item_019`.
- **Expected signal:** Lower energy drift with symplectic updates plus throughput gains for N>=512 under bounded force error.

## Direction 3: Evidence and reproducibility as first-class outputs

- **Concrete direction:** Treat literature graphing, citations, manifest logging, and figure generation as required modules (not post-hoc docs), with explicit links into final claims.
- **Informs rubric items:** `item_003`, `item_004`, `item_005`, `item_018`, `item_021`, `item_022`, `item_025`.
- **Expected signal:** Every major claim in final findings references numeric artifacts, figure paths, and BibTeX keys.

## Prioritized direction

**Prioritized:** Direction 1 (deterministic baseline-first pipeline).

**Why:** It unlocks downstream comparability across all later methods and phases; without a deterministic baseline, performance, stability, and ablation claims are not falsifiable.
