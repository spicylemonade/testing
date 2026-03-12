# Concept Evolve Tooling Blockers

## 2026-03-12: `evolve` launcher repaired, but broad-task run remained low-signal

- Original blocking defect:
  - `.archivara/concept_evolve.py` originally called `_run_sub_agent()` from `evolve()` with only `prompt` and `name`, omitting the required `command`, `fingerprint`, `topic`, and `watched_paths` arguments.
  - Impact: the mandatory `python3 .archivara/concept_evolve.py evolve ...` call would have raised a `TypeError` before any `results/concept_evolve/*` artifacts were written.
- Repair applied in this run:
  - `evolve()` now computes a fingerprint, declares watched artifacts, records cache hits, and launches the child with the full `_run_sub_agent()` contract.
  - Child prompts were also constrained to avoid recursive child-agent spawning.
- Remaining blocker after repair:
  - The mandatory broad-task `evolve` run launched successfully but produced no target artifacts (`concept_cards.json`, `semantic_bridge.json`, `introspection.json`, or `steering_directions.json`) after several minutes.
  - The child drifted across off-lane searches (oscillator synchronization, cryogenic blocks, generic cross-domain scouting) instead of converging on H1-relevant concept folders.
- Exact failing call path:
  - Command executed: `python3 .archivara/concept_evolve.py evolve "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
  - Run-state artifact: `results/concept_evolve/.state/latest_run.json`
  - Observed symptom: repeated low-signal searches, zero concept-tree artifacts, manual stop.

## Workaround Used For `item_006`

- Do not rely on the broad-task `evolve` output for the H1 concept tree.
- Use one focused child-agent layer with narrow prompts aligned to `H1_multisource_cold_start`:
  - scout concepts
  - scout novelty constraints
  - integrate the top concept folders
- Parent agent then materializes:
  - `results/concept_evolve/tree/NNN_*` concept folders
  - `results/concept_evolve/tree/index.json`
  - `results/concept_evolve/tree/adjacency.json`
  - `results/concept_evolve/tree/walk_paths.json`
  - `results/concept_evolve/integrator_selection.md`

## 2026-03-12: focused codex child-agent note pass hit response-stream disconnects

- Attempted workaround:
  - Launch three narrow `codex exec` child agents to write:
    - `results/concept_evolve/notes/explorer_h1_concepts.*`
    - `results/concept_evolve/notes/hypothesis_scout_h1_cards.*`
    - `results/concept_evolve/notes/novelty_checker_h1.*`
- Observed blocker:
  - All three child sessions failed with repeated `stream disconnected before completion` errors from the responses proxy before they wrote any note artifacts.
- Parent fallback:
  - Reconstruct the scout notes directly from the already repaired H1 literature snapshot, prior-art matrix, falsifier memo, and lane freeze.
  - Materialize the concept tree and integrator selection memo locally so the research run can continue without pretending the network-dependent child pass succeeded.
