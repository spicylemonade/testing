# Rigidity Time Selector

## Topic context
Rigidity and Bohr-time sequences in rotations describe when fractional parts nearly return to a prescribed phase. This card uses those times as selector candidates for Beatty subsequences, because clustered residues can convert the floor nonlinearity into a bounded-remainder correction on top of a simpler recurrent backbone.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Choose n_k with ||n_k*r - theta|| tending to 0, or with n_k drawn from a Bohr set around theta. Then floor(n_k*r) = n_k*r - theta - eta_k with eta_k small or bounded by a bounded-remainder window. If n_k also tracks a recurrence numeration or substitution scale, exact recurrence may emerge after correcting by the bounded remainder term.

## Cross-domain analogies
- Sample only when the torus orbit nearly hits the same gate.
- Use rigidity times as a phase-locked loop for the floor map.
- Bounded remainder sets act like error-correcting buffers.

## Novel move
Rigidity times are used here as explicit selector generators for Beatty-LRS hunting.

## Why this is not just a reimplementation
Prior rigidity and discrepancy papers study orbit-return statistics, not exact arithmetic subsequences inside floor(n*r).

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Construct selectors from convergent denominators, Bohr neighborhoods, and bounded-remainder windows, then test exact recurrences on the induced Beatty values. Prioritize badly approximable r where discrepancy control is strongest, and compare with Liouville-type controls where near-returns are frequent but unstable.
2. Run the first experiment: For r = phi, sqrt(2), a random badly approximable slope, and a Liouville-style proxy, collect rigidity-based selectors and measure exact recurrence hit rates. Compare against random selector baselines of the same density.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Rigidity times for a weakly mixing dynamical system which are not rigidity times for any irrational rotation (f20ac9ecd9f1da69b6ffbb9a21b9af9f15078a27, 2014, Ergodic Theory and Dynamical Systems): Provides rigidity-time constructions that inspire selector families.
- New Kronecker-Weyl type equidistribution results and Diophantine approximation (b1e853dbd63122efc55109f7df7f95feabce45da, 2021, European Journal of Mathematics): Gives quantitative equidistribution tools for irrational rotations.
- Equidistribution of continued fraction convergents in SL(2,Z_m) with an application to local discrepancy (ab6f688459638f15ea7e1668e078e529ac5a0ea6, 2023, Journal of Modern Dynamics): Adds convergent-distribution information useful for Bohr-set selector calibration.
- Generalized Rauzy tilings and linear recurrence sequences (0354e145b397be098c4ddcecd337be8455e59486, 2021, Chebyshevskii Sbornik): Supplies bounded-remainder geometry that can stabilize near-returns.

