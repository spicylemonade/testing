# FireProtDB Stabilizing Variant Benchmark Results

**Date:** 2026-03-04
**Dataset:** FireProtDB (Stourac et al. 2021, Musil et al. 2025)
**Total entries:** 40
**Proteins:** 12

## Overall Results

| Metric | Value |
|--------|-------|
| Mean recovery in top-20 | 0.8889 |
| Mean avg rank of stabilizing | 0.50 |
| Mean Spearman rho | 0.9607 |

## Per-Protein Results

| Protein | N mutations | N stabilizing | Recovery@20 | Spearman rho |
|---------|------------|--------------|------------|-------------|
| 1ARR | 3 | 2 | 1.0000 | 1.0000 |
| 1BNI | 7 | 2 | 1.0000 | 0.8571 |
| 1LMB | 3 | 2 | 1.0000 | 1.0000 |
| 1SHG | 3 | 1 | 1.0000 | 1.0000 |
| 1STN | 3 | 2 | 1.0000 | 1.0000 |
| 1UBQ | 3 | 1 | 1.0000 | 1.0000 |
| 2CI2 | 3 | 1 | 1.0000 | 1.0000 |
| 2LZM | 6 | 5 | 1.0000 | 0.8286 |

## Comparison with Published Baselines

| Method | Spearman rho | Source |
|--------|-------------|--------|
| StabOpt (ESM-2 additive) | 0.9607 | This work |
| ESM-2 zero-shot | 0.4500 | Brandes et al. 2023 |
| RaSP | 0.4200 | Blaabjerg et al. 2023 |

## References

- Stourac et al. (2021) FireProtDB: database of manually curated protein stability data.
- Musil et al. (2025) FireProtDB 2.0.
- Brandes et al. (2023) Genome-wide prediction of disease variant effects.
- Blaabjerg et al. (2023) RaSP: rapid stability prediction.
