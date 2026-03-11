# Generalized Polynomial Intersection Obstruction

## Topic context
Beatty sets and many sparse recurrence-value sets live in the generalized-polynomial world, but not all such intersections are allowed. This card asks whether an LRS subsequence exists only when the LRS value set is generalized-polynomial compatible with the Beatty set, shifting the problem from direct construction to structural obstruction.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Let B_r = {floor(n*r) : n >= 1}. If an LRS subsequence y_k exists, then Y = {y_k} is an infinite subset of B_r and its indicator behaves like the intersection of a Beatty generalized-polynomial set with an LRS value set. Test whether 1_Y, or a selector surrogate for Y, can still be generalized polynomial, and use sparse-GP obstructions to rule out generic intersections.

## Cross-domain analogies
- Think of the problem as a collision of two low-complexity grammars.
- Overlay a cut-and-project set with a state-space orbit and ask when the overlap stays structured.
- Use generalized polynomials as a type system for admissible subsequence values.

## Novel move
The new angle is to treat hidden recurrences in floor(n*r) as an intersection-complexity problem between generalized-polynomial and LRS worlds.

## Why this is not just a reimplementation
Prior work classifies generalized-polynomial objects or specific LRS value sets individually. This card studies when their overlap can encode an exact subsequence inside a Beatty sequence.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Build a library of candidate LRS value sets such as Fibonacci, Lucas, Tribonacci, Pell, and Salem-type sequences, then numerically test their intersections with B_r across rational, quadratic, Pisot, and random r. Where intersections persist, attempt to reverse-engineer a generalized-polynomial selector suggested by known Pisot constructions.
2. Run the first experiment: For each candidate r, compute Y_N = B_r intersect {u_k : u_k <= N} for several LRS families. Compare the observed growth with finite, logarithmic, power-law, and substitution-like patterns.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Sparse generalised polynomials (352a36ff547769f41b9a06e2a153f14869312eb8, 2016, Transactions of the American Mathematical Society): Main obstruction source for sparse generalized-polynomial sets.
- Pisot numbers, Salem numbers, and generalised polynomials (945bf0b906b8a3273f821db634b506879566566f, 2023, arXiv.org): Shows that some Pisot or Salem recurrence-value sets are generalized polynomial.
- Bracket words: A generalisation of Sturmian words arising from generalised polynomials (3e68c8006cb2bc75d36e8bbd84fd1a82eaae702d, 2022, Transactions of the American Mathematical Society): Links generalized polynomials to combinatorics on words and finite-valued codings.
- Generalized Beatty sequences and complementary triples (99423440cb26736fac8589d091008d2118a1bcc0, 2018, Moscow Journal of Combinatorics and Number Theory): Provides Beatty-side constructions worth testing against GP compatibility.

