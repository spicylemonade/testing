# Small Fixed-Slope Particle CA

Status: `rejected`

This encoding maps a tiny fixed set of slopes in `X` to particle species in a conservative or additive CA and lets local collisions propose witness structure. It is attractive computationally, but it is the clearest embodiment of the bounded-slope / low-rational-complexity trap highlighted by Tao (2025) and the falsifier memo. Even if it produces tidy patterns, it is too likely to optimize the wrong corner of the arithmetic-Kakeya landscape.

Why rejected:
- high bounded-slope risk
- fixed small alphabet biases the search toward low rational complexity
- likely to produce modular or periodic artifacts rather than exact witness gains
