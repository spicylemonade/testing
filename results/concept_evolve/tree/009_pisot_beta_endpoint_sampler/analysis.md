# Pisot Beta Endpoint Sampler Analysis

## What was implemented

The executable proxy for the concept card was:
- build a `G_n` basis from rounded powers of the named slope,
- compute greedy digit expansions in that basis,
- enumerate endpoint-conditioned indices with digit suffix `10`,
- compare them against equal-size random-digit controls,
- run the exact Hankel and modular-shadow checks on both families.

## Result

The suffix-conditioned endpoint sampler does **not** rescue a higher-degree Pisot survivor in the current frozen panel. In particular, the plastic constant does not produce an exact low-order recurrence under this endpoint construction, and the controls do not suddenly light up either.

## Interpretation

This is a negative but useful result. It means the higher-degree Pisot exception is harder than simply picking one obvious beta-endpoint cylinder. The idea remains geometrically meaningful, but in its current concrete form it is not the mechanism behind the observed survivors.
