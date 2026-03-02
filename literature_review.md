# Literature Review: Perfect Cuboid / Euler Brick Problem

## Part I: Classical Results

### 1. Halcke (1719) — Discovery of the Smallest Euler Brick
Paul Halcke discovered the smallest Euler brick with edges (a, b, c) = (44, 117, 240) and face diagonals (d_ab, d_ac, d_bc) = (125, 244, 267). The space diagonal is sqrt(44^2 + 117^2 + 240^2) = sqrt(73225) = 5*sqrt(2929), which is not an integer. This was published in *Deliciae Mathematicae; oder, Mathematisches sinnen-confect* (Hamburg, 1719). This is the first known example of a rectangular box with all face diagonals being integers.

**Reference**: Halcke, P. (1719). *Deliciae Mathematicae; oder, Mathematisches sinnen-confect.* Hamburg: N. Sauer, p. 265.

### 2. Saunderson (1740) — First Parametric Family
Nicholas Saunderson, a blind mathematician at Cambridge, discovered the first parametric family that always produces Euler bricks. Given any Pythagorean triple (u, v, w) with u^2 + v^2 = w^2, the edges:
- a = |u(4v^2 - w^2)|
- b = |v(4u^2 - w^2)|
- c = |4uvw|

always form an Euler brick. This family is infinite but does not generate all Euler bricks — for example, (240, 252, 275) is not in this family.

**Reference**: Saunderson, N. (1740). *The Elements of Algebra.* Cambridge University Press.

### 3. Euler (1770, 1772) — Additional Parametric Families
Leonhard Euler found at least two additional parametric families of Euler bricks in 1770 and 1772. After his death, more parametrizations were found in his unpublished notebooks. Euler was also aware of face cuboids (where one edge is irrational but all face diagonals and the space diagonal are integers), providing the example (104, 153, 672).

**Reference**: Euler, L. (1772). Unpublished notebooks; see Dickson, L.E. (2005), *History of the Theory of Numbers*, Vol. II, pp. 497-500.

### 4. Kraitchik (1900s) — Systematic Enumeration
Maurice Kraitchik rediscovered Euler cuboids and compiled extensive tables. He produced a list of 50 rational cuboids found by ad hoc methods, later extending this to 241 cuboids with odd side less than 10^6, of which 16 were new. This early systematic enumeration laid groundwork for later computational searches.

**Reference**: Kraitchik, M. (1953). *Théorie des Nombres.* Gauthier-Villars, Paris. Also: Kraitchik, M. (1942). *Mathematical Recreations.* Dover.

### 5. Lal and Blundon (1966) — Computer Search Parametrization
Lal and Blundon introduced a parametrization using four parameters (m, n, p, q): edges x = |2mnpq|, y = |mn(p^2 - q^2)|, z = |pq(m^2 - n^2)|, which guarantees at least two integral face diagonals. The cuboid is rational iff y^2 + z^2 is a perfect square. They searched all quadruples with 1 <= m, n, p, q <= 70, finding 130 rational cuboids, none perfect. Shanks later pointed out some corrigenda.

**Reference**: Lal, M. and Blundon, W.J. (1966). Solutions of the Diophantine equations x^2 + y^2 = l^2, y^2 + z^2 = m^2, z^2 + x^2 = n^2. *Math. Comp.*, 20(94), 144-147.

### 6. Leech (1977, 1981) — Systematic Analysis and Constraints
John Leech made several fundamental contributions:
- Showed that the product of all edges and face diagonals of a perfect cuboid must be divisible by 2^8 * 3^4 * 5^3 * 7 * 11 * 13 * 17 * 19 * 29 * 37.
- Extended Lal-Blundon search to parameter pairs up to 376.
- Proved via descent that no perfect cuboid can have a face with Pythagorean parameters (2, 1), i.e., aspect ratio 4:3.
- Derived formulas for derived cuboids from rational cuboids.

**Reference**: Leech, J. (1977). The Rational Cuboid Revisited. *American Mathematical Monthly*, 84(7), 518-533. Also: Leech, J. (1981). A remark on rational cuboids. *Can. Math. Bull.*, 24(3), 377-378.

### 7. Dickson (2005) — Historical Compilation
L.E. Dickson's *History of the Theory of Numbers* provides the most comprehensive historical compilation of results on Euler bricks and related problems, tracing the problem from Halcke through Euler to early 20th century work.

**Reference**: Dickson, L.E. (2005). *History of the Theory of Numbers, Vol. II: Diophantine Analysis.* Dover (reprint of 1920 original), pp. 497-500.

### 8. Guy (1994) — Unsolved Problems Catalog
Richard Guy included the perfect cuboid problem as Problem D18 in his influential catalog, establishing it as one of the most notable unsolved problems in number theory.

**Reference**: Guy, R.K. (2004). *Unsolved Problems in Number Theory.* 3rd ed. Springer-Verlag, Problem D18.

### 9. Spohn (1966) — Additional Parametric Families
W.G. Spohn extended the known parametric families and analyzed their coverage of the Euler brick space.

**Reference**: Spohn, W.G. (1966). On the integral cuboid. *American Mathematical Monthly*, 73, 718-719.

---

## Part II: Modern Computational Searches and Recent Approaches

### 10. Rathbun (2005-2020) — Integer Cuboid Table
Randall Rathbun conducted extensive computational searches, establishing that no perfect cuboid exists with minimum edge less than 2.325 * 10^10 (about 23 billion). He compiled the most comprehensive known catalog of Euler bricks and maintained the "Integer Cuboid Table."

**Reference**: Rathbun, R.L. (2020). The Integer Cuboid Table. arXiv:1705.05929v4 [math.NT].

### 11. Butler (2004-present) — Large-Scale Computational Search
Bill Butler developed an efficient search algorithm based on factoring the even edge Y and pre-computing candidates divisible by 16. He searched all odd sides up to at least 3 * 10^12, finding no perfect cuboid. His algorithm subdivides the Y candidate list based on divisibility by 16.

**Reference**: Butler, W. (2004). Search for a Perfect Cuboid. Personal website and correspondence. Also described in Matson (2015).

### 12. Matson (2015) — Extended Computer Search
Robert Matson pushed the computational search frontier further, establishing that no solution exists with odd edge a < 2.5 * 10^13. His work refined Butler's algorithm and verified consistency with Rathbun's results.

**Reference**: Matson, R.D. (2015). Results of computer search for a perfect cuboid. Available at unsolvedproblems.org.

### 13. Korec (1992) — Lower Bound on Smallest Edge
Ivan Korec established that no perfect cuboid exists with smallest side less than 10^6 through systematic computation, an important early benchmark.

**Reference**: Korec, I. (1992). Lower bounds for perfect cuboids. *Math. Slovaca*, 42(2), 145-152.

### 14. Van Luijk (2000) — Algebraic Geometry Perspective
Ronald van Luijk provided a comprehensive algebraic geometric analysis of the perfect cuboid problem. He showed the algebraic surface parameterizing Euler bricks is the intersection of certain quadrics in P^5, forming a K3 surface of maximal rank. This deep structural insight connects the problem to modern algebraic geometry.

**Reference**: van Luijk, R. (2000). On Perfect Cuboids. Leiden University. Available at pub.math.leidenuniv.nl.

### 15. Bremner (1988) — Cubic Surfaces and Parametric Families
Andrew Bremner analyzed the Euler brick equations from the perspective of cubic surfaces, producing new parametric families and analyzing which families are most likely to yield near-misses.

**Reference**: Bremner, A. (1988). The rational cuboid and a quartic surface. *Rocky Mountain Journal of Mathematics*, 18(1), 105-121.

### 16. Sharipov (2012-2020) — S3-Symmetry and Multisymmetric Polynomials
Ruslan Sharipov developed a symmetry-based approach exploiting the natural S3 symmetry of edge permutations. Key contributions:
- Factorized cuboid equations using multisymmetric polynomials (arXiv:1205.3135).
- Connected cuboid factor equations to families of elliptic curves (arXiv:1209.5706).
- Proposed numerical search strategies based on the second cuboid conjecture (arXiv:1504.07161).
- Formulated three cuboid conjectures: if all three are valid, no perfect cuboid exists.

**References**:
- Sharipov, R.A. (2012). Perfect cuboids and multisymmetric polynomials. arXiv:1205.3135.
- Sharipov, R.A. (2012). A note on rational and elliptic curves associated with the cuboid factor equations. arXiv:1209.5706.
- Sharipov, R.A. (2015). A strategy of numeric search for perfect cuboids in the case of the second cuboid conjecture. arXiv:1504.07161.
- Sharipov, R.A. (2020). Symmetry-Based Approach to the Problem of a Perfect Cuboid. *Journal of Mathematical Sciences*, 252, 266-282.

### 17. De Grey, Gibbs, and Helm (2024) — Perfect Plinth Analysis
Aubrey de Grey, Philip Gibbs, and Louie Helm developed two novel search algorithms based on "perfect plinth" analysis. Key contributions:
- Much more efficient search algorithms than any prior approach.
- Identified new two-parameter families of edge cuboids.
- Showed large proportions of face/internal rectangle aspect ratios cannot appear in a perfect cuboid.
- Used elliptic curve methods: represent various types of body-path cuboids as elliptic curves and analyze their Mordell-Weil groups.
- Published in Geombinatorics Quarterly, Vol. XXXIII, Issue 3, p. 107, 2024.

**Reference**: de Grey, A., Gibbs, P., and Helm, L. (2024). Novel required properties of, and efficient algorithms to seek, perfect cuboids. arXiv:2401.06784. *Geombinatorics Quarterly*, XXXIII(3), 107.

### 18. Lloyd (2022) — Non-Existence Claim
Ivor Lloyd's preprint claims to prove non-existence by showing the internal diagonal of an Euler brick cannot be an odd integer. The argument uses parity analysis. This claim has not been widely accepted or peer-reviewed as of 2026.

**Reference**: Lloyd, I. (2022). There is no Perfect Cuboid. arXiv:2206.06160.

### 19. Agbanwa (2025) — Divisor-Based Non-Existence
Jamal Agbanwa proposed a divisor-based proof of non-existence, along with a simplified version. These preprints are on figshare/ResearchGate but have not been peer-reviewed.

**Reference**: Agbanwa, J. (2025). A divisor-based proof on the non-existence of perfect cuboids. Figshare preprint. Also: Simplified proof of the non-existence of perfect cuboids. ResearchGate preprint.

### 20. arXiv 2602.00239 (2026) — Elementary Obstruction
This recent preprint studies arithmetic constraints from the three faces meeting along the space diagonal. It uses a propagation mechanism based on minimal odd prime appearances in triangular configurations to derive an obstruction. Status: preprint, not yet peer-reviewed.

**Reference**: arXiv:2602.00239 (2026). An Elementary Obstruction to the Existence of a Perfect Cuboid.

### 21. Ramsden and Sharipov (2013) — Descent on Elliptic Curves
J.R. Ramsden and R.A. Sharipov applied two-descent and three-descent techniques to elliptic curves associated with perfect cuboids, providing information about Mordell-Weil ranks.

**Reference**: Ramsden, J.R. and Sharipov, R.A. (2013). Two and three descent for elliptic curves associated with perfect cuboids. arXiv:1303.0765.

### 22. Knill (2013) — Survey Lecture
Oliver Knill produced a comprehensive survey lecture at Harvard covering the history, known results, and connections to algebraic geometry.

**Reference**: Knill, O. (2013). Treasure Hunting Perfect Euler bricks. Harvard University lecture notes.

### 23. Ionascu and Luca (2007) — Heron Triangles and Related Problems
E.J. Ionascu and F. Luca studied related Diophantine problems connecting Heron triangles to Euler bricks.

**Reference**: Ionascu, E.J. and Luca, F. (2007). Heron triangles with two fixed sides. *J. Number Theory*, 126(1), 52-67.

---

## Summary of Current State

The perfect cuboid problem remains open. Key facts:
1. **Computational searches** have verified non-existence up to odd edge ~ 2.5 * 10^13 (Matson).
2. **No universally accepted proof** of non-existence exists, though several claims have been made (Lloyd 2022, Agbanwa 2025, arXiv 2602.00239).
3. **Structural insights** from algebraic geometry (van Luijk's K3 surface, Sharipov's S3 symmetry) and elliptic curve methods (De Grey-Gibbs-Helm) provide deep theoretical frameworks.
4. **Parametric families** (Saunderson, Euler, Bremner) generate infinite Euler bricks but none have yielded a perfect cuboid.
5. The problem connects to major areas: Diophantine equations, modular arithmetic, elliptic curves, algebraic surfaces, and computational number theory.
