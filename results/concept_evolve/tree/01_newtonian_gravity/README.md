# SOFTENED_GRAVITY

Plummer softening replaces the 1/r^2 singularity with 1/(r^2 + epsilon^2), preventing infinite forces at close approach while preserving long-range Newtonian behavior. The minimal regularization.

## Mathematical Formalization

F_ij = -G * m_i * m_j * (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^(3/2).  Potential: Phi(r) = -G*m / sqrt(r^2 + eps^2).  Recovers Newtonian gravity for r >> eps.

## Analogical Connections

- Plummer softening <-> L2 regularization in ML (adds eps to prevent divergence)
- Softened gravity <-> Lennard-Jones potential at long range (attractive 1/r^6 vs 1/r^2)
- Epsilon parameter <-> kernel bandwidth in KDE (controls resolution scale)

## Implementation Hypothesis

Brute-force O(N^2) double loop with softening. For N<500, this is real-time at 60fps. The softening epsilon should be ~1% of the mean inter-particle distance to avoid artificial smoothing.

## Experiment Seed

Fix two bodies at distance d, sweep eps/d from 0.001 to 1.0, plot force magnitude vs eps/d. Identify the crossover where softening distorts the force by >5% (expected at eps/d ~ 0.1).
