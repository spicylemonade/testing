# Analysis

The reversible micro-step wrapper is validated on the star-grazing stress case.

- At `dt = 0.02`, the plain direct kernel stays unsafe, while the encounter-aware path becomes safe and cuts final-state error versus REBOUND from `6.56e-01` to `4.55e-03`.
- At `dt = 0.04`, the wrapper still reduces error by about `4.86e+02` even though the run remains unsafe by the chosen energy-drift gate.

Result: the concept materially changes the safe operating regime and is worth promoting.
