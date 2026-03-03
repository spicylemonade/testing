# Energy Drift Monitor

## Topic Context

Energy conservation is the most important diagnostic for gravitational N-body simulations. A well-implemented symplectic integrator should show bounded energy oscillation around the true value, while non-symplectic methods show secular (monotonic) drift. The character of the energy error reveals both the quality of the integrator and the presence of bugs.

Brouwer's law (1937) predicts that the optimal energy error grows as sqrt(t) — a random walk. The IAS15 integrator (Rein & Spiegel 2014) achieves this optimal behavior. Monitoring energy drift in real-time provides immediate feedback on simulation quality.

### Key Ideas
- Relative energy error delta_E = |E(t) - E(0)| / |E(0)|
- Bounded oscillation → symplectic integrator
- Linear drift → non-symplectic or bug
- sqrt(t) random walk → optimal (Brouwer's law)
- Angular momentum conservation as secondary diagnostic

### Cross-Domain Connections
- Financial auditing (cumulative error tracking)
- Signal integrity monitoring (BER in communications)
- Lyapunov exponents (characterizing chaos)

## Implementation Backlog

- [ ] Implement kinetic and potential energy computation
- [ ] Compute and store relative energy error time series
- [ ] Implement angular momentum computation (vector)
- [ ] Fit log-log slope to classify drift type
- [ ] Create real-time energy drift dashboard
- [ ] Add automatic warnings when drift exceeds threshold
- [ ] Compare drift across integrators (Euler, RK4, leapfrog)
- [ ] Test on chaotic vs regular orbits
