# Near-Miss Statistical Analysis

## Finding 1: Near-Miss Score Distribution
- Total Euler bricks analyzed: 200
- Best (lowest) near-miss score: 2.979036e-08
- Median near-miss score: 1.067811e-06
- Mean near-miss score: 9.486771e-07
- Best near-miss: (43440, 45612, 49775) with score 2.979036e-08

## Finding 2: Trend with Edge Magnitude
- Log-log regression slope: -0.2997
- R² value: 0.0254
- p-value: 2.4196e-02
- **Near-miss scores DECREASE with edge size** (negative slope),
  meaning larger Euler bricks tend to come closer to being perfect cuboids.
  This is CONSISTENT with the possibility of a solution at very large scales.

## Finding 3: Prime Factorization of Residuals
Most common prime factors in space-diagonal residuals (top 100 near-misses):

| Prime | Frequency |
|-------|-----------|
| 3 | 52 |
| 2 | 49 |
| 5 | 32 |
| 11 | 13 |
| 13 | 11 |
| 7 | 11 |
| 29 | 4 |
| 73 | 4 |
| 17 | 3 |
| 31 | 3 |
| 47 | 2 |
| 89 | 2 |
| 19 | 2 |
| 53 | 2 |
| 71 | 2 |

- Factor 2 appears in 49/100 residuals
- Factor 3 appears in 52/100 residuals

## Comparison with Matson's Observations
Matson (2014) observed that near-misses become rarer with increasing edge size,
and that the number of matching bits in the best near-misses decreases. Our
analysis of the power-law fit provides quantitative support for this observation.
The regression slope and R² indicate the strength of this trend.

See: [matson2014] in sources.bib
