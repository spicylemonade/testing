# Phase 4 Ablations

## Command

```bash
python3 scripts/phase4_ablations.py \
  --base results/phase4_width4_seed601.json \
  --output results/phase4_ablations.json
```

Base witness:

- exact forcing control from `results/phase4_width4_seed601.json`
- score `2.0`
- parameters `m=7`, `r=5`, `n=8`, `t=2`

## Results

| Row | Outcome |
| --- | --- |
| exact elimination replacement | unchanged by design; all rows already use the exact verifier |
| isotropic top->bottom | survives, but worsens to `13/6 = 2.1666...` |
| isotropic bottom->top | exact verification failure |
| boundary seed removal | exact verification failure |
| randomize `R` | 4/4 deterministic trials failed exact verification |
| randomize `T` | 4/4 deterministic trials failed exact verification |
| randomize `X` | 3/4 deterministic trials still forced with the same score `2.0`; 1/4 failed |
| freeze `X`, scale to width `6` | no forcing witness found under the fixed-motif bounded search |
| freeze `X`, scale to width `8` | no forcing witness found under the fixed-motif bounded search |
| stage-order perturbation | not applicable once H1 died; there is no surviving substitution grammar to reorder |

## Interpretation

- The surviving direct corridor witness is not robust to seed or initial-solved perturbations.
- Boundary programming is essential: shrinking the boundary seed mass kills the witness immediately.
- The gain is not strongly tied to the specific arithmetic labels in `X`; random relabelings with the same size and coordinate-height budget often preserve the same `2.0` score.
- The fixed motif does not scale under frozen `X`, reinforcing the literature warning that this search remains trapped in a bounded-slope / low-rational-complexity corridor basin.

## Decision

No ablation preserved a route to the `1.70` neighborhood. The surviving evidence supports only a narrow negative claim: exact direct corridor witnesses around `2.0` exist, but they are boundary-sensitive and do not scale cleanly.
