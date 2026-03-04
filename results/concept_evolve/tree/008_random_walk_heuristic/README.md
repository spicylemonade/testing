# 008 — Random Walk Heuristic

## Concept

Models the Collatz trajectory as a random walk on log-scale and uses the Chinese Remainder Theorem (CRT) to explicitly construct integers with provably long runs of consecutive odd steps. Each odd step multiplies by approximately 3/2 (since n -> (3n+1)/2^v with v=1), so k consecutive odd steps cause growth by roughly (3/2)^k. Under the random walk heuristic, such runs occur with probability ~(1/2)^k, making them large deviation events.

The shortcut Collatz map:

```
n -> (3n+1) / 2^{v_2(3n+1)}
```

where v_2(m) is the 2-adic valuation. Forcing v_2(3n+1) = 1 for k consecutive iterates requires n to satisfy simultaneous congruences, solvable by CRT. The resulting numbers have engineered long trajectories, and among them we search for delay record candidates.

## Cross-Domain Connections

| Source Domain | Analogy | Mapping |
|---|---|---|
| Queuing theory | Large deviations in queue length | Consecutive odd steps ~ consecutive arrivals exceeding service rate; trajectory length ~ queue buildup |
| Rare event simulation | Importance sampling for rare events | CRT construction ~ importance sampling that biases toward the rare event (long odd runs) |
| Meteorology | Extreme weather as large deviations | Sustained trajectory growth ~ sustained atmospheric blocking; both are persistent anomalies in a stochastic system |

The random walk heuristic is the standard probabilistic model for Collatz dynamics. This concept goes beyond passive modeling to active construction: rather than waiting for rare events, we engineer them via number-theoretic tools and study whether the resulting trajectories achieve genuinely extreme delays.

## Implementation Backlog

1. **CRT solver** — Given target k, compute the system of congruences ensuring v_2(3n_i+1) = 1 for i = 0..k-1 along the trajectory; solve via CRT.
2. **Minimal solution finder** — For each k in 10..30, find the smallest positive integer satisfying the k-step odd-run constraint.
3. **Trajectory analyzer** — Compute full Collatz trajectory for each constructed n; measure total delay, peak value, and trajectory structure beyond the forced segment.
4. **Delay comparison** — Compare achieved delays against known records and against random integers of the same bit-length.
5. **Scaling law extraction** — Fit delay vs. k to determine whether CRT-constructed numbers achieve delays scaling better than the (3/2)^k lower bound.

## References

- Dembo, A. & Zeitouni, O. (2010). *Large Deviations Techniques and Applications.* Springer.
- Kontorovich, A.V. (2006). "Syracuse conjecture and continued fractions." arXiv.
- Rozier, O. & Terracol, A. (2025). "Paradoxical behavior in Collatz sequences." arXiv.
