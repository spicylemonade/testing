# Reproducibility Package

This guide is designed for a fresh user to run one baseline workflow and one advanced workflow in <=30 minutes.

## Runtime budget

| Stage | Command | Target time |
| --- | --- | --- |
| Setup | `bash scripts/setup_research_tools.sh` | 5-10 min |
| Baseline run | `python3 scripts/run_baseline_smoke.py` | 2-5 min |
| Advanced run (symplectic) | `python3 scripts/collect_symplectic_eval.py` | 10-15 min |
| Verification checks | small JSON checks below | 2-3 min |

## Setup instructions

```bash
git clone <REPO_URL>
cd <REPO_DIR>
python3 -m venv .venv
source .venv/bin/activate
bash scripts/setup_research_tools.sh
```

Sanity check:

```bash
python3 -c "import numpy, psutil, matplotlib, seaborn, scipy; print('deps-ok')"
```

## Baseline reproducibility run

```bash
python3 scripts/run_baseline_smoke.py
```

Verification:

```bash
python3 -c "import json; d=json.load(open('results/baseline/hash_check.json')); print({'two_body': d['two_body']['deterministic'], 'random_n64': d['random_n64']['deterministic']})"
```

Expected: both values are `True`.

## Advanced reproducibility run (symplectic)

```bash
python3 scripts/collect_symplectic_eval.py
```

Verification:

```bash
python3 -c "import json; d=json.load(open('results/research/symplectic_eval.json')); print(d['acceptance']['flags'])"
```

Expected: `rubric_acceptance_pass` is `true`.

## Configuration table

| Workflow | Script | Methods | Scenarios / N | Seeds | dt | Steps | Softening |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline smoke | `scripts/run_baseline_smoke.py` | `baseline` | `two_body` (`N=2`), `random` (`N=64`) | `42` | `0.002` (two-body), `0.001` (random) | `400` (two-body), `200` (random) | default (`1e-3`) |
| Advanced evaluation | `scripts/collect_symplectic_eval.py` | `baseline`, `symplectic` | `two_body`, `three_body`, `random_n64` | `42-46` | two-body `0.002`, others `0.001` | `1200` (two/three-body), `300` (random) | two-body `1e-4`, others `1e-3` |

## Artifact index

- `results/baseline/hash_check.json` - deterministic hash checks for baseline smoke runs.
- `results/baseline/trajectories/two_body_seed42_run_a.json` - baseline two-body trajectory sample.
- `results/baseline/trajectories/random_n64_seed42_run_a.json` - baseline random-N trajectory sample.
- `results/research/symplectic_eval.json` - seeded baseline vs symplectic evaluation and acceptance flags.
- `results/research/scaling_eval.json` - optional advanced scaling run output (Barnes-Hut path).
- `results/experiments/raw/run_manifest.jsonl` - controlled experiment matrix provenance.

## Optional advanced alternative (Barnes-Hut)

```bash
python3 scripts/collect_scaling_eval.py
```

This writes `results/research/scaling_eval.json`.
