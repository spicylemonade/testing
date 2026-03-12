# divisor_window_density_control

## Context
Ford-style divisor-window asymptotics give a natural control model for how densely a sparse product set can fill short intervals. The idea is to compare the mex-generated frontier to an exogenous multiplication table with the same divisor-profile statistics and use that as a benchmark for gap growth.

## Mathematical Sketch
For x near r_n, define H_n(x)=\sum_{d\mid x} 1_{d\in R_n}1_{x/d\in C_n}. Then x\in P_n iff H_n(x)\ge 1. Approximate \mathbb{P}[H_n(x)=0] via divisor-window densities for d in [x/y, x/z], and bound \max\{h:[x,x+h]\cap P_n=\emptyset\} using local estimates for H_n.

## Why This Bridge Might Matter
The literature analyzes product coverage for exogenous factor sets; here the sets are adaptively chosen to repair the leftmost holes, so the asymptotics become a feedback-controlled coverage model.

## Implementation Backlog
- analysis/divisor_window_fit.ipynb
- experiments/local_intensity_scan.py
- data/divisor_window_features.parquet

## Starting Experiment
For n up to 6000, regress observed uncovered-block lengths against empirical divisor-window intensity and compare with a null model built from shuffled R_n and C_n of the same size.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- Integers with a divisor in (y,2y] (openalex:W2111749106)
- The distribution of integers with a divisor in a given interval (openalex:W2159774990)
- The multiplication table problem for bipartite graphs (openalex:W2487318500)
