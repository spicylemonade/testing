# algebraic_geometry_syzygies

## Context
Casts the Ramsey problem as finding the roots of a system of polynomial equations in characteristic 2. By computing the minimal free resolution of the corresponding ideal, we extract the Betti numbers. The projective dimension of the module changes suddenly at the Ramsey boundary.

## Domains
Commutative Algebra, Algebraic Geometry, Combinatorics

## Math
Variables x_e \in \{0,1\}. Ideal I = \langle x_{e_1}\dots x_{e_{10}}, (1-x_{e_1})\dots(1-x_{e_{10}}) \rangle. Compute the free resolution. R(5,5) is where 1 \notin I becomes false.

## Analogies
Like shining a light through a crystal to see its diffraction pattern (syzygies). When the crystal's structure becomes impossible (hitting the Ramsey bound), the diffraction pattern shatters or becomes trivial.

## Implementation Backlog
- Use randomized algebraic algorithms to find the degree of the Hilbert polynomial for varying N. Analyze the length of the free resolution as N approaches 43.
- Run Macaulay2 to compute the Betti tables for R(3,3)=6 and R(4,3)=9. Look for a predictive algebraic invariant in the Betti table that scales with N and collapses at the bound.
