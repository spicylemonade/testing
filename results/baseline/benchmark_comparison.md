# Benchmark Comparison: Baseline vs Prior Work

**Date**: 2026-03-02  
**Item**: item_011

## Our Baseline Metrics

From `results/baseline/kepler_validation.json`:
- **Integrator**: Leapfrog (KDK), fixed time-step
- **Max relative energy error**: 2.63e-7 over 10 Kepler orbits (e=0.5)
- **Momentum conservation**: Machine precision (~1e-15)
- **Angular momentum conservation**: Machine precision (~1e-14)
- **Period accuracy**: 0.0% error (within sampling resolution)

## Comparison with REBOUND (Rein & Liu, 2012)

REBOUND's leapfrog integrator with similar parameters:
- **Energy conservation**: The REBOUND paper reports bounded energy oscillation for
  the leapfrog integrator, consistent with our observation. For a Kepler orbit with
  e=0.5, their WHFast integrator (Wisdom-Holman based) achieves ~1e-10 energy error
  per orbit using mixed-variable symplectic mapping.
- **Our comparison**: Our brute-force leapfrog at 20000 steps/orbit achieves 2.6e-7,
  which is ~1000x worse than WHFast. This is expected: WHFast splits the Hamiltonian
  into an exactly solvable Kepler part + perturbation, while we integrate the full
  unsplit Hamiltonian.
- **Period accuracy**: Both achieve period accuracy limited by timestep resolution.

**Assessment**: Our baseline energy conservation is consistent with expectations for
a 2nd-order symplectic integrator without Keplerian splitting. The gap vs WHFast
motivates our Yoshida 4th-order implementation (item_013).

## Comparison with GADGET-2 (Springel, 2005)

GADGET-2 uses a "quasi-symplectic" leapfrog with individual adaptive time-steps:
- **Energy conservation**: Springel (2005) reports ~0.1-1% energy conservation for
  cosmological N-body simulations over a Hubble time. This is worse than our
  fixed-timestep result because GADGET-2 uses adaptive time-stepping which breaks
  strict symplecticity.
- **Scaling**: GADGET-2 reports O(N log N) scaling with the TreePM method. Our
  brute-force baseline is O(N^2), consistent with direct summation.
- **Runtime**: GADGET-2 can simulate 10^10 particles on clusters. Our baseline
  is limited to N~1000-5000 in Python.

**Assessment**: Our energy conservation is better than GADGET-2's reported values
for a given number of force evaluations, because we maintain strict symplecticity
with fixed time-steps. GADGET-2 trades conservation for adaptivity and scaling.

## Comparison with Hernandez & Bertschinger (2015)

Their symplectic N-body integrator using Kepler solvers:
- **Energy conservation**: They report "about 1.5 orders of magnitude better
  symplecticity" than standard leapfrog for equivalent force evaluations.
- **Our comparison**: Their improved conservation comes from using analytical
  Kepler solutions for two-body subsystems, which we do not implement.

**Assessment**: Our baseline matches the expected performance of a standard leapfrog
integrator without Kepler splitting.

## Summary

| Metric | Our Baseline | REBOUND WHFast | GADGET-2 |
|--------|-------------|----------------|----------|
| Energy conservation (per orbit) | ~2.6e-7 | ~1e-10 | ~1e-3 to 1e-2 |
| Integrator order | 2nd | 2nd (split) | 2nd (adaptive) |
| Symplectic? | Yes (strict) | Yes (strict) | Quasi (adaptive dt breaks) |
| Force method | Brute-force O(N^2) | Direct / WHFast | TreePM O(N log N) |
| Max practical N | ~5000 | ~10^4 (direct) | ~10^10 |

Our baseline is correctly positioned: better conservation than adaptive codes,
worse than specialized split integrators, and limited in N by O(N^2) scaling.

## References

- rein2012rebound
- springel2005gadget2
- hernandez2015symplectic
