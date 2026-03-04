# Stochastic Collatz Model

## Concept

Models Collatz iteration as a biased random walk on log-space. Under the
Lagarias-Weiss heuristic, each step of the Collatz map is treated as an i.i.d.
multiplicative random variable; taking logarithms converts the trajectory into
an additive random walk with negative drift mu approximately -0.2075. This predicts
that the maximum excursion of a trajectory starting at n scales as n^2 and that
the stopping time (delay) concentrates around |log_2(n)| / |mu|.

## Cross-Domain Connections

- **Brownian motion with drift** (probability theory): The log-trajectory
  behaves like a discretized Brownian motion with drift, enabling application of
  optional stopping theorems, barrier-crossing estimates, and large-deviation
  bounds.
- **Gambler's ruin** (classical probability): The question "does the trajectory
  reach 1?" maps directly to a gambler's ruin problem with biased coin flips,
  giving intuition for why almost all orbits descend.
- **Protein folding random walks** (biophysics): The energy landscape traversed
  during protein folding shares structural similarities — a biased walk through
  a rugged landscape toward a global minimum, with rare excursions to high-energy
  states analogous to high-trajectory peaks.

## Implementation Backlog

1. **Monte Carlo delay simulator** — Sample 10M random starting numbers, compute
   actual Collatz delay, compare against the predicted delay from the drift model,
   and rank anomalies by z-score.
2. **Drift estimation pipeline** — Empirically estimate the effective drift mu and
   variance sigma^2 as a function of bit-length, checking for deviations from the
   theoretical value.
3. **Excursion statistics collector** — For each trajectory, record the maximum
   value reached and compare against the n^2 prediction; build histograms of
   max(trajectory) / n^2 to characterize the tail behavior.
4. **Anomaly database** — Store numbers whose actual delay exceeds the predicted
   delay by more than 3 sigma, annotated with trajectory features for downstream
   analysis by other concept modules.

## Key References

- Lagarias, J. C., & Weiss, A. (1992). *Stochastic models for the 3x+1 and 5x+1
  problems.* In The (3x+1) Problem.
- Lagarias, J. C. (2010). *The Ultimate Challenge: The 3x+1 Problem.* AMS.
- Tao, T. (2022). *Almost all orbits of the Collatz map attain almost bounded
  values.* Forum of Mathematics, Pi.
