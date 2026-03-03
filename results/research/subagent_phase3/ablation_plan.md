# Phase-3 Ablation Plan: Gravity Methods

This plan isolates where stability and scaling gains come from across the phase-3 methods, then tests the hybrid hypothesis under controlled changes.

## Artifact anchors

- Baseline artifact: `results/baseline/metrics.json` and `results/baseline/metrics.md`
- Symplectic artifact: `results/research/symplectic_eval.json`
- Scaling artifact: `results/research/scaling_eval.json`
- Hybrid context: `results/concept_evolve/tree/hybrid_proposal.md` and `results/concept_evolve/probe_result.json`

## Shared evaluation protocol

- Scenarios: `two_body`, `three_body`, `random` (with `n in {64, 512, 1024}` as applicable)
- Seeds: `42, 43, 44, 45, 46`
- Core metrics: max energy drift %, runtime per step (ms), throughput (steps/s), final-position error % vs direct baseline reference
- Report style: median over seeds + per-seed spread; compare each ablation arm against the nearest artifact anchor above

## Ablation matrix

| ID | Ablation | Controlled setup | Expected signal | Artifact linkage |
| --- | --- | --- | --- | --- |
| A1 | **Integrator-only swap**: `baseline` Euler vs `symplectic` under direct O(N^2) force | Match scenario/seed/dt/softening exactly to `symplectic_eval` configs | Reproduce strong drift reduction on low-body regimes (two-body near total drift suppression; three-body large reduction) with runtime ratio <= 1.5; confirms gains are from integrator, not force approximation | Anchored to `results/research/symplectic_eval.json` and baseline drift context in `results/baseline/metrics.json` |
| A2 | **dt sensitivity on random_n64**: sweep `dt = {2e-4, 5e-4, 1e-3, 2e-3}` for baseline vs symplectic | Fix `n=64`, `steps` scaled to maintain horizon, `softening=1e-3`, same seeds | At `dt=1e-3`, expect to recover current anomaly (symplectic worse than baseline in random_n64); at smaller `dt`, expect crossover where symplectic regains positive energy-drift improvement | Uses anomaly in `results/research/symplectic_eval.json` (`random_n64`) and baseline instability trend in `results/baseline/metrics.md` |
| A3 | **Softening sensitivity**: sweep `softening = {1e-4, 5e-4, 1e-3, 2e-3}` across baseline/symplectic and Barnes-Hut | Fix `dt` per scenario (`0.001` for n64, `0.0008` for high-N), fixed seeds | Expect U-shaped stability/accuracy tradeoff: very low softening increases drift spikes, moderate softening stabilizes, overly large softening lowers drift but increases position error due to over-smoothed forces | Connects baseline force policy in `results/baseline/design_spec.md`, symplectic behavior in `results/research/symplectic_eval.json`, and high-N error in `results/research/scaling_eval.json` |
| A4 | **Barnes-Hut opening angle sweep**: `theta = {0.5, 0.8, 1.2}` | Match scaling artifact config (`dt=8e-4`, `softening=1e-3`, `n={256,512,1024}`) | Throughput should increase monotonically with theta while final-position error rises; expected knee near `theta=0.8` (large speedup with sub-1% error) | Directly tied to `results/research/scaling_eval.json` tradeoff curve and per-N best-theta summaries |
| A5 | **Integrator-force coupling**: Euler+Barnes-Hut vs Symplectic+Barnes-Hut (hybrid) | Fix `theta=0.8`, `leaf_size=8`, `bh_min_n=64`, same seeds/scenarios (focus `n>=512`) | Hybrid should retain most scaling gain (>4x throughput vs direct baseline at `n=512`) while reducing max energy drift vs Euler+BH; validates phase-3 hybrid hypothesis | Uses throughput/error baseline from `results/research/scaling_eval.json`, stability expectations from `results/research/symplectic_eval.json`, and explicit hypothesis in `results/concept_evolve/probe_result.json` |

## Readout and decision rules

- Promote an ablation result to phase-4 protocol if it improves the target metric on median and does not violate runtime or reproducibility constraints.
- For A2/A3, keep parameter values that are stable across both `three_body` and `random_n64`; reject values that only help one scenario while regressing the other severely.
- For A4/A5, treat `theta=0.8` as the default candidate unless another point clearly dominates on both throughput and error.
- If A5 fails expected signal (no drift gain over Euler+BH), postpone hybrid integration and proceed with best non-hybrid Barnes-Hut point from A4.
