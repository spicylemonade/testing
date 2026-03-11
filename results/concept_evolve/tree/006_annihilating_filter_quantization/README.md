# Annihilating Filter Quantization

## Topic context
The floor map is a quantizer, so floor(n*r) is a linear signal plus structured clipping noise. This card searches for selectors n_k whose residue sequence {n_k*r} is itself annihilable, so that the quantized values inherit an exact homogeneous recurrence after the noise cancels.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Write y_k = floor(n_k*r) = r*n_k - eps_k with eps_k = {n_k*r} in [0,1). Seek coefficients c_i such that sum_i c_i*n_{k+i} = 0 and sum_i c_i*eps_{k+i} = 0, hence sum_i c_i*y_{k+i} = 0. The problem becomes simultaneous annihilation of a selector trajectory and its quantization residue.

## Cross-domain analogies
- Cancel clock jitter rather than model the whole waveform.
- Find a clipping pattern with a built-in inverse filter.
- Align arithmetic sampling with residue-phase locking.

## Novel move
The direct target is the quantization-error sequence, not the Beatty values alone.

## Why this is not just a reimplementation
Generalized Prony papers handle sparse signals with structured samples. This proposal treats the floor nonlinearity as a structured noise source to be neutralized by arithmetic selector design.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Generate candidate selectors from convergents, Bohr sets, and substitution blocks; compute exact residue vectors and solve small integer linear systems for annihilating filters. Use lattice reduction to prioritize selectors where residues cluster on a low-dimensional torus.
2. Run the first experiment: Compare selectors built from q_j, Fibonacci indices, and bounded-remainder windows for r in {phi, sqrt(2), plastic constant, random badly approximable}. Track exact cancellations versus near-cancellations.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Learning algebraic decompositions using Prony structures (a87683c0a5bfd0d50927b45c7994b04cc1088c64, 2019, Advances in Applied Mathematics): Prony structures suggest exact annihilating-filter workflows.
- Reconstruction of stationary and non-stationary signals by the generalized Prony method (40aa1637440fc9d10d8ffa8eeba8d9d3bb9e4568, 2019, Analysis and Applications): Shows generalized Prony methods on non-stationary and transformed signals.
- Sampling and Super Resolution of Sparse Signals Beyond the Fourier Domain (46972284777ce742297550ab926d7d83f2ab5cf3, 2018, IEEE Transactions on Signal Processing): Provides a sparse-sampling viewpoint where non-Fourier domains matter.
- Generalized Beatty sequences and complementary triples (99423440cb26736fac8589d091008d2118a1bcc0, 2018, Moscow Journal of Combinatorics and Number Theory): Supplies Beatty identities where nested floor structure already mimics filtered behavior.

