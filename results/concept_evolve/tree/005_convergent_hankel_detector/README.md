# Convergent Hankel Detector

## Topic context
A hidden homogeneous recurrence leaves a low-rank Hankel fingerprint, even when viewed through sparse or irregular samples. This card samples floor(n*r) on continued-fraction convergents and feeds the samples to Prony or Hankel machinery, betting that quadratic or Pisot-type r expose exact low-rank blocks while generic r only show noisy near-rank deficiency.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Let q_j be denominators of convergents to r and define x_j = floor(q_j*r) or x_j^(m,ell) = floor(q_{m*j+ell}*r). Search for d such that the Hankel matrices H_d(a,b) = x_{a+b} have bounded exact rank. Exact rank collapse implies that the sampled subsequence satisfies a homogeneous linear recurrence.

## Cross-domain analogies
- Use Hankel rank as a seismograph for arithmetic self-similarity.
- Treat convergents as compressed sensors tuned to the slope.
- Turn continued fractions into an adaptive acquisition protocol.

## Novel move
The novelty is to redirect Prony-style recovery from classical exponential sums to convergent-sampled Beatty arithmetic.

## Why this is not just a reimplementation
Signal-processing papers reconstruct sparse exponential models from samples. This card instead derives the samples from continued fractions and uses low-rank detection to hunt hidden recurrences inside floor(n*r).

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Compute convergent blocks for candidate r, build exact integer Hankel matrices, and run matrix-pencil or Prony reconstruction. If an annihilating polynomial emerges, validate it symbolically on longer blocks and map the witness back to the original Beatty subsequence.
2. Run the first experiment: Benchmark rational, quadratic irrational, plastic-constant, and random-real inputs. Record exact Hankel rank, recovered order, and failure modes under different block choices (m, ell).
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Learning algebraic decompositions using Prony structures (a87683c0a5bfd0d50927b45c7994b04cc1088c64, 2019, Advances in Applied Mathematics): General Prony framework for exact low-rank recovery from structured samples.
- The Generalized Operator Based Prony Method (342ed71a75d859bb7830916a589af527aa3f8296, 2019, Constructive Approximation): Operator-based Prony variant that suggests more flexible sampling schemes.
- Sampling and Super Resolution of Sparse Signals Beyond the Fourier Domain (46972284777ce742297550ab926d7d83f2ab5cf3, 2018, IEEE Transactions on Signal Processing): Super-resolution perspective on sparse recovery beyond standard Fourier sampling.
- Linear fractional transformations of continued fractions with bounded partial quotients (475c339b02716f45ddc460b6966ca95179b0cd1d, 1997, Journal de Theorie des Nombres de Bordeaux): Continued-fraction boundedness result that motivates convergent-block sampling.

