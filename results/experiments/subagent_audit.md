# Experiment Matrix Reproducibility Audit

Audit date: 2026-03-03

Scope: phase-4 experiment-matrix artifacts under `results/experiments/`, with spot checks against generation scripts in `scripts/` and runtime entrypoints in `src/gravity_sim/`.

## Reproducibility checklist

| Checklist item | Status | Evidence | Remediation notes |
| --- | --- | --- | --- |
| Preregistered protocol exists with methods, scenarios, dt values, seeds, stopping criteria, and metric rules. | PASS | `results/experiments/protocol.md` | Keep protocol as single source of truth for matrix changes. |
| Controlled matrix coverage is complete (3 methods x 3 scenarios x 5 seeds). | PASS | `results/experiments/raw/coverage_summary.json` (`total_runs: 45`), `results/experiments/raw/run_manifest.jsonl` | No remediation required for current batch. |
| Per-run provenance includes command, seed, method, runtime environment, commit hash, artifact path, and artifact hash. | PASS | `results/experiments/raw/run_manifest.jsonl` | Add explicit schema version field in future manifests to harden long-term compatibility. |
| Artifact files referenced by manifest all exist and hash-check clean. | PASS | `results/experiments/raw/run_manifest.jsonl` + artifact tree under `results/experiments/raw/` (audit check: 45/45 files present, 45/45 SHA-256 matches) | No remediation required for current batch. |
| Statistics artifacts are traceable to the same matrix commit. | PASS | `results/experiments/statistics.json`, `results/experiments/statistics.md`, `results/experiments/raw/run_manifest.jsonl` (commit `0a455b418f75f4256b1015701caf74cb8d723c7a`) | Continue enforcing commit pinning in downstream reports. |
| Sampled run is reproducible for deterministic dynamics (non-runtime metrics + trajectory state). | PASS | `results/experiments/raw/symplectic/two_body/symplectic__two_body__seed42.json`, `scripts/run_experiment_matrix.py` | Runtime metrics vary by host load; treat runtime as bounded variance, not bitwise-invariant. |
| Manifest replay command is directly executable in a fresh shell as written. | PARTIAL | `results/experiments/raw/run_manifest.jsonl`, `scripts/run_experiment_matrix.py`, `src/gravity_sim/cli.py` | Current command string assumes package import context and does not match matrix writer schema exactly; document/emit an executable replay command (for example `PYTHONPATH=src ...`) in final reproducibility docs. |

## Resolved action items

| ID | Action item | Resolution | Concrete artifact references | Remediation note |
| --- | --- | --- | --- | --- |
| RA-01 | Upgrade from single-seed reporting to seeded matrix execution. | Completed with fixed seeds `{42,43,44,45,46}` across every method-scenario pair. | `results/experiments/raw/coverage_summary.json`, `results/experiments/raw/run_manifest.jsonl` | Keep seed set frozen for strict comparability across reruns. |
| RA-02 | Add audit-grade per-run manifest metadata. | Completed with per-run command, environment, commit hash, artifact path, and hash. | `results/experiments/raw/run_manifest.jsonl` | Add `schema_version` and optional hostname/container-id fields for stronger provenance. |
| RA-03 | Preserve raw per-run outputs for independent verification. | Completed with structured raw outputs under method/scenario folders. | `results/experiments/raw/baseline/`, `results/experiments/raw/symplectic/`, `results/experiments/raw/barnes_hut/` | Retain folder schema unchanged to avoid breaking analysis tooling. |
| RA-04 | Publish statistical robustness outputs (CI/effect sizes/sensitivity/threshold checks). | Completed with machine-readable and markdown reports tied to matrix commit. | `results/experiments/statistics.json`, `results/experiments/statistics.md`, `results/experiments/sensitivity_dt_softening.json` | Standardize commit-hash format across all auxiliary artifacts (short vs full SHA). |
| RA-05 | Independently reproduce a sampled experiment result. | Completed via spot re-run of `symplectic/two_body/seed42`; deterministic state trajectory and drift metrics matched, runtime metric differed as expected. | `results/experiments/raw/symplectic/two_body/symplectic__two_body__seed42.json`, `scripts/run_experiment_matrix.py` | For future audits, store replay script output in a dedicated `results/experiments/audit_replays/` folder. |

## Targeted remediation notes (remaining hardening)

1. **Replay command portability**: commands in `results/experiments/raw/run_manifest.jsonl` are not universally runnable without an import-path setup step; include explicit environment bootstrap in reproducibility docs.
2. **Command-to-artifact schema alignment**: manifest command currently references CLI output format from `src/gravity_sim/cli.py`, while matrix artifacts are written by `scripts/run_experiment_matrix.py`; align these so replayed commands regenerate equivalent artifact schema.
3. **Provenance format consistency**: `results/experiments/sensitivity_dt_softening.json` uses a short commit string while matrix/statistics use full SHA; normalize on full SHA-1 for joins and audits.
