# ode_divisor_profile_dynamics

## Context
A fluid-limit approximation may separate average behavior from rare obstruction events. This card compresses the arithmetic state into divisor-profile buckets and fits a Wormald-style drift model that predicts how average gap and record-gap scales should evolve.

## Mathematical Sketch
Let U_n(\beta) count uncovered integers in bucket \beta, where \beta may encode smoothness, \omega(x), or observed witness multiplicity. Estimate \mathbb{E}[U_{n+1}(\beta)-U_n(\beta)\mid \mathcal{F}_n] \approx F_\beta(U_n/n), derive an ODE or mean-field map, and compare its predicted gap tails with data.

## Why This Bridge Might Matter
The novelty lies in bucketizing by arithmetic divisor profile rather than generic graph degree, letting the fluid model talk directly to product coverage.

## Implementation Backlog
- analysis/divisor_profile_buckets.py
- experiments/fluid_limit_fit.py
- data/drift_trajectories.json

## Starting Experiment
Fit drift models on the first 2000 steps, forecast the next 4000, and compare predicted record-gap counts against the exact simulation.

## Closest Prior Art
- Rectangular array, read by descending antidiagonals: a prime separator array. (oeis:A129258)
- The distribution of integers with a divisor in a given interval (openalex:W2159774990)
- The differential equation method for random graph processes and greedy algorithms (openalex:W5090298)
- Random graphs with arbitrary degree distributions and their applications (openalex:W2169015768)
