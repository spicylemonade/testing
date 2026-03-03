# Concept: CLI Manifest Reproducibility

## Role

Maintains canonical command-line and metadata conventions so runs are replayable and auditable.

## Baseline dependency notes

- Depends on `src/gravity_sim/cli.py` and `src/gravity_sim/io.py` for deterministic JSON emission.
- Depends on `results/baseline/hash_check.json` for reproducibility evidence.
- Feeds experiment manifests in later phases (`results/experiments/raw/*`).

## Validation checks

- Same command and seed must produce identical output hashes.
- Output metadata must always include method/scenario/N/dt/steps/seed/softening.
