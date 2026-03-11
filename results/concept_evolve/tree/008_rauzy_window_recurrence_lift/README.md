# Rauzy Window Recurrence Lift

## Topic context
Rauzy tilings tie Pisot numeration, toral rotations, and bounded remainder sets to linear-recurrence geometry. This card uses self-similar windows in Rauzy space as a geometric selector for Beatty values, lifting orbit hits on tile boundaries into arithmetic subsequences that may inherit Pisot recurrences.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Embed candidate indices as orbit points under a toral rotation and choose subsequences by hits into a nested self-similar family of Rauzy windows W_k. If window endpoints or tile addresses evolve by a Pisot substitution matrix M, then the selected Beatty values y_k = floor(n_k*r) are expected to satisfy y_{k+d} = sum_{i<d} a_i*y_{k+i} along the induced symbolic itinerary.

## Cross-domain analogies
- Tile boundaries act as recurrence resonators.
- A toral orbit is cut by a fractal stencil.
- Bounded remainder windows become exact arithmetic samplers.

## Novel move
Rauzy windows are promoted from geometric background to explicit selectors for Beatty subsequence extraction.

## Why this is not just a reimplementation
Rauzy papers geometrize linear-recurrence numeration and bounded remainder sets. This proposal pulls an exact subsequence extraction problem back through that geometry.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Construct Rauzy or generalized Rauzy tiles for small Pisot units, simulate orbit hits, and collect the associated Beatty values. Fit substitution matrices on tile addresses, then verify whether the sampled values satisfy the same characteristic polynomial.
2. Run the first experiment: Use the golden ratio and plastic constant as first test cases. Compare arbitrary window hits against self-similar boundary hits to see whether only the latter produce exact low-order recurrences.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Generalized Rauzy tilings and linear recurrence sequences (0354e145b397be098c4ddcecd337be8455e59486, 2021, Chebyshevskii Sbornik): Direct geometric bridge between Rauzy tilings and linear-recurrence numeration.
- Pisot numbers, Salem numbers, and generalised polynomials (945bf0b906b8a3273f821db634b506879566566f, 2023, arXiv.org): Provides the Pisot-valued generalized-polynomial side of the story.
- Generalized Beatty sequences and complementary triples (99423440cb26736fac8589d091008d2118a1bcc0, 2018, Moscow Journal of Combinatorics and Number Theory): Supplies Beatty-side constructions to compare with geometric selectors.
- New Kronecker-Weyl type equidistribution results and Diophantine approximation (b1e853dbd63122efc55109f7df7f95feabce45da, 2021, European Journal of Mathematics): Adds modern equidistribution and discrepancy control for rotation-based sampling.

