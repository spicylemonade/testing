# 003: Schwarz-Christoffel Mapping with Interval Arithmetic

## Topic Context

The Schwarz-Christoffel (SC) formula provides explicit conformal maps from the unit disk to polygonal domains. The SC Toolbox (Driscoll-Trefethen) is the standard computational tool, but it uses floating-point arithmetic and cannot provide rigorous bounds.

By combining SC mappings with interval arithmetic — where every computation tracks rigorous error bounds — we can produce computer-verified bounds on the Bloch constant. This approach follows the tradition of Tucker's computer-assisted proof of the Lorenz attractor (Smale's 14th problem).

## Key Technical Components

- **SC parameter problem**: Finding the prevertices z_k given the polygon vertices (inverse problem)
- **Gauss-Jacobi quadrature**: For evaluating the SC integral with controlled error
- **Interval arithmetic**: INTLAB (MATLAB), IntervalArithmetic.jl (Julia), arb (C)
- **Validated numerics**: Rigorous enclosures ensuring mathematical correctness

## Implementation Backlog

1. [ ] Set up Julia environment with IntervalArithmetic.jl and ArbNumerics.jl
2. [ ] Implement SC mapping formula with interval coefficients
3. [ ] Solve the SC parameter problem with rigorous bounds
4. [ ] Verify: conformal map to infinite strip, inradius = pi/4
5. [ ] Approximate slit domains with high-vertex-count polygons
6. [ ] Compute rigorous enclosure of Bloch radius for each polygon
7. [ ] Compare interval-verified bounds with floating-point results
8. [ ] Produce a certificate of the rigorous bound
