# 009 — Self-Organized Criticality

## Concept

Self-organized criticality (SOC) describes systems that naturally evolve toward a critical state where scale-free, power-law-distributed events emerge without any external tuning. The canonical example is the Bak-Tang-Wiesenfeld sandpile model, where grains of sand dropped onto a pile produce avalanches whose sizes follow a power law.

The Collatz conjecture exhibits a strikingly similar signature: the distribution of stopping delays (the number of steps before reaching 1) appears to follow a power law. For integers up to large bounds, the complementary cumulative distribution function (CCDF) of delays approximates P(delay > d) ~ d^{-alpha} with alpha in the range 2–3. This mirrors the Gutenberg-Richter law for earthquake magnitudes and the avalanche size distribution in sandpile models.

The key insight is that the Collatz map, like SOC systems, produces scale-free behavior without any parameter tuning — the rules are fixed, yet the delay distribution spans many orders of magnitude with no characteristic scale.

## Cross-Domain Connections

- **Statistical physics / sandpile models**: The BTW sandpile model is the prototypical SOC system. Collatz delays may share the same universality class as sandpile avalanche durations.
- **Seismology / Gutenberg-Richter law**: Earthquake magnitude distributions follow power laws with exponents near 2. If Collatz delays exhibit a similar exponent, common mechanisms (threshold dynamics, cascading events) may be at play.
- **Scale-free networks**: Networks with power-law degree distributions (Barabási-Albert model) arise from preferential attachment. The Collatz trajectory graph may have analogous preferential merging dynamics driving scale-free delay statistics.
- **Extremal statistics**: Record-breaking delays are extreme events in a heavy-tailed distribution. SOC framing connects delay records to return-time statistics in critical systems.

## Implementation Backlog

1. **Compute delay distribution up to 10^8** — Enumerate all delays for n = 1 to 10^8 using GPU-accelerated or batched computation. Store as histogram and raw sorted array.
2. **CCDF power-law analysis** — Plot CCDF on log-log axes. Apply Clauset-Shalizi-Newman maximum likelihood estimation (MLE) to fit the power-law exponent alpha and determine the lower cutoff x_min.
3. **Goodness-of-fit testing** — Use the KS statistic and likelihood-ratio test against competing distributions (lognormal, stretched exponential) to assess whether a power law is the best model.
4. **Importance sampling via SOC prior** — Use the fitted power-law tail to construct an importance-sampling distribution that preferentially samples integers in high-delay regions, accelerating the search for delay records.
5. **Universality class comparison** — Compare the fitted exponent to known SOC universality classes (mean-field sandpile alpha = 3/2 for avalanche size, directed percolation exponents) to determine if Collatz delays fall into an existing class.
