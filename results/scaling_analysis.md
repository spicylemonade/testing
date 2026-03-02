# Scaling Analysis and Computational Feasibility Study

## Empirical Scaling Exponents

### brute_force
- Empirical complexity: O(n^2.09)
- Reference times: n=1000: 0.558s, n=2000: 2.405s, n=5000: 16.111s

### modular_sieve
- Empirical complexity: O(n^2.01)
- Reference times: n=1000: 0.145s, n=2000: 0.544s, n=5000: 3.645s

### novel_search
- Empirical complexity: O(n^1.30)
- Reference times: n=1000: 0.002s, n=2000: 0.004s, n=5000: 0.016s

## Extrapolation to Published Search Frontiers

| Method | Edge=10^6 | Edge=10^8 | Edge=10^10 | Edge=10^13 |
|--------|----------|----------|-----------|-----------|
| brute_force | 12d | 5e+02y | 7e+06y | 1e+13y |
| modular_sieve | 2d | 5e+01y | 5e+05y | 5e+11y |
| novel_search | 15.5s | 2h | 29d | 6e+02y |

## Assessment

- **Brute force** cannot reach beyond ~10^4 edges in reasonable time.
- **Modular sieve** extends this to ~10^5 edges, a 10x improvement in reach.
- **Novel search (triple intersection)** is the fastest but misses some bricks.
- None of our methods can reach the published frontier of 10^10-10^13.
- Published algorithms (Butler, De Grey-Gibbs-Helm) use fundamentally different
  approaches (direct factorization of even edges, elliptic curve parameterization)
  that are orders of magnitude faster for very large bounds.

## Scaling Plots

See figures/scaling_comparison.png and figures/coverage_comparison.png.