# Reproducibility Packet

## Decision Snapshot

- Next action: `pivot to H2`
- Selected next branch: `H2_lag_space_ca_167` (`lag_residue_ca_167` in `results/concept_evolve/recurrent_state.json`)
- Exact order-668 Hadamard matrix found in this run: `no`
- Exact improvement over the published frontier seed from `eliahou2025_64mod668`: `no`

## Canonical Inputs

- Frontier seed sequence: `results/frontier/order_668_64m/seed_sequences.json`
- Frontier seed manifest: `results/frontier/order_668_64m/seed_manifest.json`
- Control seeds:
  - `results/experiments/controls/seeds/control_n5_q0.json`
  - `results/experiments/controls/seeds/control_n7_q0.json`
- Shared frontier seed identity from `results/frontier/order_668_64m/seed_manifest.json`:
  - `q_compact_rle = (83, 2, 81, 1)`
  - `s_compact_rle = (4)^5(2,1,1)^5(1,5)(4)^4(2,1,1)^6(4)^4(3)(1,2,1)^5(3)(4)^4(3)(1,2,1)^5`
  - `matrix_checksum = e75fbb67b5c89a18a579462bb4d8aac540ff05153018d664d171fc0d217a1ab3`
- Shared pilot contract:
  - evaluation budget `80`
  - requested restarts `3`
  - RNG seed `17`
  - `restart_packet_flips = 2`

## Exact Rerun Commands

### Control Batch: `control_n5_q0`

```bash
python3 scripts/run_h1_ca.py \
  --config results/experiments/controls/configs/H1_defect_syndrome_ca_64m.json \
  --seed-file results/experiments/controls/seeds/control_n5_q0.json \
  --output results/experiments/controls/runs/control_n5_q0/H1_defect_syndrome_ca_64m.json

for method in greedy tabu simulated_annealing stochastic_hillclimb; do
  python3 scripts/run_baseline.py \
    --config "results/experiments/controls/configs/${method}.json" \
    --seed-file results/experiments/controls/seeds/control_n5_q0.json \
    --output "results/experiments/controls/runs/control_n5_q0/${method}.json"
done
```

### Control Batch: `control_n7_q0`

```bash
python3 scripts/run_h1_ca.py \
  --config results/experiments/controls/configs/H1_defect_syndrome_ca_64m.json \
  --seed-file results/experiments/controls/seeds/control_n7_q0.json \
  --output results/experiments/controls/runs/control_n7_q0/H1_defect_syndrome_ca_64m.json

for method in greedy tabu simulated_annealing stochastic_hillclimb; do
  python3 scripts/run_baseline.py \
    --config "results/experiments/controls/configs/${method}.json" \
    --seed-file results/experiments/controls/seeds/control_n7_q0.json \
    --output "results/experiments/controls/runs/control_n7_q0/${method}.json"
done
```

### Frontier Batch: `order_668_64m`

```bash
python3 scripts/run_h1_ca.py \
  --config results/experiments/order_668_64m/configs/H1_defect_syndrome_ca_64m.json \
  --seed-file results/frontier/order_668_64m/seed_sequences.json \
  --output results/experiments/order_668_64m/runs/H1_defect_syndrome_ca_64m.json

for method in greedy tabu simulated_annealing stochastic_hillclimb; do
  python3 scripts/run_baseline.py \
    --config "results/experiments/order_668_64m/configs/${method}.json" \
    --seed-file results/frontier/order_668_64m/seed_sequences.json \
    --output "results/experiments/order_668_64m/runs/${method}.json"
done
```

### Structured Exploration Checkpoints

```bash
python3 .archivara/concept_evolve.py evolve "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"
python3 .archivara/concept_evolve.py reframe "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"
python3 .archivara/concept_evolve.py iterate "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"
```

The probe checkpoint is summarized in `results/concept_evolve/probe_result.json` and interpreted in `results/concept_evolve/concept_delta.md`.

## Primary Artifact Map

- Control aggregate readout:
  - `results/experiments/controls/summary.md`
  - `results/experiments/controls/summary.json`
- Frontier aggregate readout:
  - `results/experiments/order_668_64m/summary.md`
  - `results/experiments/order_668_64m/summary.json`
- Raw run files:
  - `results/experiments/controls/runs/`
  - `results/experiments/order_668_64m/runs/`
- Matched configs:
  - `results/experiments/controls/configs/`
  - `results/experiments/order_668_64m/configs/`
- Verification pack:
  - `results/verification/novelty_report.md`
  - `results/verification/citation_audit.md`
  - `results/verification/benchmark_report.md`
  - `results/verification/verification_summary.md`
  - `results/verification/runtime_audit.md`
- Concept refresh:
  - `results/concept_evolve/recurrent_state.json`
  - `results/concept_evolve/concept_delta.json`
  - `results/concept_evolve/bridge_candidates.json`

## Fixed Outcomes To Check

- Control exact fingerprints:
  - `control_n5_q0`: `41f454617c1bf06e6799d762f381869dae5d7614b0f6316a80febb801add9b5c`
  - `control_n7_q0`: `37e654cc9d22ebd353e25e1d1bf2021a6e6d0f83c215491991baf0f718941bcf`
- Frontier seed objective from `results/experiments/order_668_64m/summary.json`:
  - support `13`
  - `l1 = 2880`
  - `max_abs = 512`
- H1 frontier readout:
  - `objective_evaluations = 32`
  - `wall_seconds = 2.1292423080003573`
  - `seed_improvement = false`
  - `exact_hit = false`
- Final decision:
  - `results/verification/verification_summary.md` must still read `pivot to H2`

## Next-Agent Guardrail

Do not spend frontier budget on H2 until the family-leakage audit in `results/branches/H2_gate.md` is satisfied against `Williamson`, `Turyn`, `Goethals-Seidel`, `cocyclic`, and `block-circulant` collapse.
