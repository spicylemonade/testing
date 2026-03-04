# 007 — Extremal Statistics Predictor

## Concept

Applies extreme value theory (EVT) to the sequence of known Collatz delay records. The delay of record-holding integers can be modeled as draws from a generalized extreme value (GEV) distribution, whose parameters evolve with the search frontier. By fitting GEV parameters to the 131 known records, we can predict the expected delay of the next record and the optimal numerical range in which to search.

The GEV cumulative distribution function:

```
P(D_n <= d) ~ exp(-(1 + xi * (d - mu_n) / sigma_n)^{-1/xi})
```

where mu_n is the location parameter (growing with log(n)), sigma_n is the scale, and xi is the shape parameter governing tail behavior. A positive xi (Frechet-type) implies heavier-than-exponential tails — meaning records grow faster than naive expectation.

## Cross-Domain Connections

| Source Domain | Analogy | Mapping |
|---|---|---|
| Hydrology | Flood return level prediction | Delay records ~ annual maximum flood levels; GEV fit predicts 100-year delay |
| Seismology | Maximum earthquake magnitude prediction | Record delays ~ max magnitude in a region; tail shape xi determines extremal growth |
| Climatology | Record temperature analysis | Successive delay records ~ successive temperature records; non-stationarity handled via trending mu_n |

The unifying principle is that record-breaking events in any stationary or slowly-varying process obey universal statistical laws. EVT provides distribution-free guarantees about the behavior of maxima, making it a natural framework for predicting the next Collatz delay record without requiring a mechanistic model of the dynamics.

## Implementation Backlog

1. **Data preparation** — Compile all 131 known delay records as (n, delay(n)) pairs; compute log(n) as the covariate.
2. **GEV fitting** — Fit GEV distribution to delay values using maximum likelihood, with location parameter mu as a function of log(n).
3. **Cross-validation** — Remove last 10 records, fit on first 121, predict records 122–131; measure prediction error.
4. **Return level prediction** — Compute expected delay and 95% confidence interval for record #132; translate to optimal search range in n.
5. **Shape parameter analysis** — Interpret fitted xi: determine whether Collatz delay records follow Gumbel (xi=0), Frechet (xi>0), or Weibull (xi<0) tail behavior.

## References

- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values.* Springer.
- Beirlant, J. et al. (2006). *Statistics of Extremes.* Wiley.
- Roosendaal, E. "Delay records of the 3x+1 problem." [www.ericr.nl/wondrous/](http://www.ericr.nl/wondrous/)
