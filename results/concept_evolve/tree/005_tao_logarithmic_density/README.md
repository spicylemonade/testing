# 005: Tao's Logarithmic Density Framework

## Overview

Terence Tao's 2019 breakthrough is the strongest theoretical result on the Collatz conjecture to date. He proved that for any function f going to infinity (no matter how slowly), Col_min(N) <= f(N) for almost all N in the sense of logarithmic density. This means the set of "bad" numbers (if any exist) has logarithmic density zero.

## Key Technical Ideas

1. **Syracuse formulation**: Work with Syr(n) = (3n+1)/2^{v_2(3n+1)} instead of Col(n)
2. **3-adic cyclic groups**: The Syracuse map induces dynamics on Z/3^n Z
3. **Renewal process**: Trajectory decomposition into i.i.d.-like segments
4. **Characteristic function estimation**: Control mixing via Fourier analysis on Z/3^n Z

## Implications for Delay Records

If the logarithmic density of numbers with delay > D is ~ 1/D^alpha for some alpha > 0, then:
- The k-th delay record should appear near exp(c * k) for some constant c
- Known data: 147 records up to ~2.8 * 10^19 suggests c ~ 0.28
- Prediction: 148th record near exp(0.28 * 148) ~ 4.5 * 10^17... but this is below the search frontier
- This suggests the record growth accelerated recently, consistent with the "strength level" jumps

## Implementation Backlog

1. [ ] Extract all 147 delay records into a structured dataset
2. [ ] Fit exponential, power law, and GEV distributions to record positions
3. [ ] Compute AIC/BIC model selection criteria
4. [ ] Generate predictions with uncertainty bounds for records 148-160
5. [ ] Validate retrospectively by withholding last 20 records and predicting
6. [ ] Connect to Tao's theoretical bounds on the density function
