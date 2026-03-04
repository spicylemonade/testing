# Tropical Geometry of Extremal Functions

## Topic Context

Tropical geometry provides a combinatorial framework for studying algebraic varieties by replacing classical operations with the tropical semiring (max, +). The amoeba of an algebraic variety V ⊂ (C*)^n is the image of V under the component-wise log-modulus map. The tropical variety is the "skeleton" of the amoeba.

## Connection to Bloch Constant

For a polynomial f(z) = z + a_2z^2 + ... + a_Nz^N:
- The discriminant locus {(a_2,...,a_N,w) : f(z) = w has multiple roots} is an algebraic variety
- Its complement contains the region where f is locally univalent at a given w
- The Newton polytope and tropical variety of the discriminant encode the scaling regimes of the coefficients and target values

The covering radius is the minimum |w| on the boundary of f(D), which relates to the boundary of the amoeba of the discriminant.

## Implementation Backlog

1. **[P0]** Compute discriminant of f for N=3,4
2. **[P1]** Compute Newton polytope using polymake
3. **[P2]** Compute tropical variety using Gfan
4. **[P2]** Visualize amoeba numerically for N=3
5. **[P3]** Identify coefficient scaling regimes that maximize covering radius
