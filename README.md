# Minimal Gravity Simulator

This repo contains an audit-first minimal gravity simulator research kernel plus the benchmark and verification artifacts used to test it.

## Setup

```bash
./scripts/setup_research_tools.sh
```

For the optional calibration stack:

```bash
./scripts/setup_research_tools.sh --with-calibration
```

## Run The Simulator Bundle

```bash
./.venv/bin/python scripts/run_baseline_scenarios.py
./.venv/bin/python scripts/run_audit_bundle.py
```

Outputs:

- baseline trajectories: `results/baseline/`
- audit summaries: `results/audit/`
- scenario definitions: `scenarios/`

## Run The Benchmark Suite

```bash
./.venv/bin/python scripts/run_analytic_controls.py
./.venv/bin/python scripts/run_long_horizon_checks.py
./.venv/bin/python scripts/run_benchmark_report.py
./.venv/bin/python scripts/run_reproducibility_report.py
```

Verification artifacts:

- analytic controls: `results/verification/analytic_controls.md`
- long-horizon drift: `results/verification/long_horizon_drift.md`
- benchmark comparison: `results/verification/benchmark_report.md`
- cross-runtime replay and close-encounter envelope: `results/verification/reproducibility_report.md`
- novelty and citation audits: `results/verification/novelty_report.md`, `results/verification/citation_audit.md`, `results/verification/verification_summary.md`

Figures:

- `figures/long_horizon_drift.png`
- `figures/long_horizon_drift.pdf`

## Research Notes

- problem statement: `results/problem_statement.md`
- concept steering and deltas: `results/concept_evolve/steering_notes.md`, `results/concept_evolve/concept_delta.md`
- phase summaries: `results/phase1_synthesis.md`, `results/phase3_decision_log.md`
