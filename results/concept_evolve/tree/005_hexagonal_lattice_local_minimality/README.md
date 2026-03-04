# 005: Hexagonal Lattice Local Minimality

## Topic Context

Ahlfors and Grunsky (1937) constructed a specific function — the universal covering map of the complement of a hexagonal lattice — and conjectured it achieves the Bloch constant B. The conjectured value is approximately 0.4719.

Baernstein and Vinson (1995) proved that this function gives a **local minimum** for the Bloch functional among all ramified coverings branched over lattice points. However, global optimality remains open — one of the longest-standing conjectures in geometric function theory.

## Key Facts

- Ahlfors-Grunsky conjecture: B = Gamma(1/3)*Gamma(11/12) / (sqrt(1+sqrt(3)) * Gamma(1/4))
- Best lower bound: B > sqrt(3)/4 + 3*10^{-4} (Xiong 1998)
- Local minimality proved within the lattice covering class
- The hexagonal lattice has the densest circle packing in 2D (Hales)

## Implementation Backlog

1. [ ] Implement Weierstrass P-function for hexagonal lattice
2. [ ] Compute Ahlfors-Grunsky Bloch constant to high precision
3. [ ] Perturb lattice parameters and compute B_f
4. [ ] Verify second-order local minimality numerically
5. [ ] Test non-lattice branch point configurations
6. [ ] Compare with square and rectangular lattices
7. [ ] Investigate connection to Viazovska's sphere packing methods
