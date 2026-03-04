# Adaptive Sieve Depth Scaling

## Topic Context

A remarkable property of Angeltveit's algorithm is that it becomes MORE efficient for larger N. The fraction of integers that survive all four sieves (Descent, Path-Merging, OEE, and mod-9) decreases exponentially with N — approximately by a factor of 1.9 for each additional bit. This means verifying up to 2^{N+1} takes less than twice the time of verifying up to 2^N.

This is connected to Tao's 2022 result that almost all Collatz orbits attain almost bounded values, and to the random walk interpretation of Collatz dynamics (Lagarias-Weiss 1992).

## Cross-Domain Bridges

- **Concentration of measure**: Random variables cluster near expectations in high dimensions
- **Phase transitions**: Sharp qualitative changes as parameters grow
- **Information theory**: More data enables better compression ratios

## Implementation Backlog

- [ ] Collect survival rate data for N=35..55
- [ ] Fit exponential model S(N) = C * alpha^N
- [ ] Predict computation time for N=72, 75, 77, 80
- [ ] Implement adaptive parameter selection based on calibration
- [ ] Analyze theoretical survival rate using random walk CLT
- [ ] Compare predictions against actual running time for N=50..55
- [ ] Estimate when verification of 2^80 becomes computationally feasible
