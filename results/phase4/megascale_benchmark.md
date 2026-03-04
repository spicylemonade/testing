# Mega-scale Multi-Mutant Benchmark Results

**Date:** 2026-03-04
**Dataset:** Mega-scale (Tsuboyama et al. 2023)
**Total variants:** 607,839
**Double mutants evaluated:** 131,143
**Proteins analyzed:** 30

## Overall Results

| Metric | Value |
|--------|-------|
| Spearman rho (doubles) | 0.8086 |
| Precision@10 | 1.0000 |
| Precision@20 | 1.0 |
| Enrichment@10 | 1.3036861045390382 |
| RMSE | 1.2857 |
| MAE | 0.9823 |
| N (valid pairs) | 131,143 |

## Epistasis Analysis

- Mean epistasis (observed - additive): 0.8937 kcal/mol
- Std epistasis: 0.9243 kcal/mol
- Fraction with |epistasis| > 0.5 kcal/mol: 64.2%
- Fraction with |epistasis| > 1.0 kcal/mol: 39.7%

## Comparison with Published Methods

| Method | Spearman rho (doubles) | Source |
|--------|----------------------|--------|
| Additive (ESM-2 singles sum) | 0.8086 | This work |
| ESM-2 zero-shot (single mutations) | N/A | Brandes et al. 2023 (reported ~0.45 on DMS) |
| ThermoMPNN-D (double mutants) | 0.4800 | Dieckhaus et al. 2024 |
| Mutate Everything | N/A | Ouyang-Zhang et al. 2023 (reported ~0.47 on ProteinGym singles) |

## Per-Protein Results (top 10 by sample size)

| Protein | N doubles | Spearman rho | Precision@10 | RMSE |
|---------|-----------|-------------|-------------|------|
| 1QP2 | 2631 | 0.8209 | 1.0000 | 1.4772 |
| 1GL5 | 2575 | 0.8328 | 1.0000 | 1.0545 |
| 1TUD | 1946 | 0.8803 | 1.0000 | 1.0027 |
| 1UFM | 1944 | 0.7860 | 1.0000 | 0.7334 |
| 1PV0 | 1937 | 0.7265 | 1.0000 | 1.0962 |
| 1QKH | 1333 | 0.7022 | 1.0000 | 0.8401 |
| 1ORC | 1084 | 0.8913 | 1.0000 | 1.3175 |
| 1LP1 | 1071 | 0.6061 | 1.0000 | 0.7760 |
| 1H92 | 838 | 0.7129 | 1.0000 | 1.1516 |
| 1UZC | 825 | 0.4529 | 1.0000 | 1.2979 |

## References

- Tsuboyama et al. (2023) Nature. Mega-scale experimental analysis of protein folding stability.
- Brandes et al. (2023) Genome-wide prediction of disease variant effects with a deep protein language model.
- Dieckhaus et al. (2024) ThermoMPNN-D for double-mutant stability prediction.
- Ouyang-Zhang et al. (2023) NeurIPS. Mutate Everything: parallel decoding for protein fitness prediction.
- Faure et al. (2024) Nature. The genetic architecture of protein stability.
