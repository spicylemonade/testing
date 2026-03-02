# Analysis of Recent Non-Existence Proof Attempts

## 1. Lloyd (arXiv:2206.06160) — "There is no Perfect Cuboid" (2022)

### Proof Strategy
Lloyd claims to show that the internal (space) diagonal of an Euler brick cannot be an odd integer. Since Roberts (2009) proved that in any primitive perfect cuboid the space diagonal must be odd, this would imply non-existence.

### Method
1. Assumes a primitive perfect cuboid exists with edges (a, b, c), face diagonals (d, e, f), and space diagonal g.
2. Uses the parity constraints: a ≡ 0 mod 16, b ≡ 0 mod 4, c odd.
3. Works with the equation g² = a² + b² + c² = d² + c² (since d² = a² + b²).
4. Performs algebraic manipulations involving the factorizations of d² + c² and d² - c² to derive constraints on g.
5. Claims to derive a contradiction showing g cannot be odd.

### Critical Step
The critical claim is in the transition from properties of the factorization d ± c to properties of g. The argument relies on showing that certain coprimality conditions between d, c, and g cannot all be satisfied simultaneously.

### Assessment
- The paper was withdrawn (v2) and resubmitted (v3, January 2024).
- Multiple mathematicians have examined the argument informally.
- The paper has not been published in a peer-reviewed journal.
- The core algebraic manipulation in the critical step has been questioned — specifically, the handling of the case where gcd(d-c, d+c) might not behave as assumed.
- **Status: Unverified.** The mathematical community does not consider this a settled proof.

### Cite: [lloyd2022]

## 2. Yelle (arXiv:2602.00239) — "An Elementary Obstruction" (2026)

### Proof Strategy
Yelle introduces an "additive parametrization" of right triangles using a concept called the "triangular remainder." Unlike classical multiplicative parametrizations (a = m² - n², b = 2mn, c = m² + n²), this additive encoding naturally couples the three faces of a cuboid through their shared space diagonal.

### Method
1. Defines the "triangular remainder" r(a,b) for a right triangle with legs a, b as a specific function of the Pythagorean triple parameters.
2. Shows that for a cuboid's three face triangles, the triangular remainders are coupled through the common edge structure.
3. Chooses a minimal odd prime p dividing one of the triangular remainders.
4. Shows that the constraints from the three faces force p to propagate: it must divide the remainders of all three faces, then all edge lengths, then all diagonal lengths.
5. This propagation contradicts the minimality assumption (infinite descent), proving no solution exists.

### Critical Step
The propagation mechanism: showing that a prime dividing one triangular remainder must divide all triangular remainders via the cuboid face coupling. This requires careful tracking of divisibility through the additive parametrization.

### Assessment
- Very recent preprint (January 30, 2026, revised February 9, 2026).
- Classified as math.GM (General Mathematics) rather than math.NT (Number Theory), which may indicate it has not been endorsed by an arXiv-recognized number theorist.
- The "additive parametrization" approach is novel and not standard in the literature.
- The infinite descent argument structure is classically sound, but the correctness depends on whether the propagation lemma (prime divisibility transfer between triangular remainders) is valid.
- **Status: Too recent for evaluation.** Needs careful peer review.

### Cite: [yelle2026]

## 3. Wyss (2015) — "On Perfect Cuboids" / "No Perfect Cuboid"

### Proof Strategy
Wyss attempted to prove non-existence using properties of Gaussian integers and the norm structure of the Pythagorean system.

### Method
1. Reformulates the cuboid equations over Z[i] (Gaussian integers).
2. Uses factorization properties of Gaussian integers to constrain the form of solutions.
3. Claims certain norm conditions are incompatible.

### Critical Step
The factorization of the hypotenuse in Z[i] and the compatibility conditions when three such factorizations share legs.

### Assessment
- The most-cited paper on the topic (24 citations on Semantic Scholar).
- **Sharipov (2017)** published a detailed critique [sharipov2017] identifying specific gaps in the argument, particularly in the handling of units and associates in Z[i].
- The paper has spawned significant follow-up discussion but the proof is not accepted.
- **Status: Refuted** (specific errors identified by Sharipov).

### Cite: [wyss2015, sharipov2017]

## 4. Computational Constraints Suggested by Proof Attempts

### From Lloyd's Approach
If the odd-space-diagonal constraint could be tightened (e.g., showing g must satisfy additional congruence conditions), this could be implemented as an additional filter in the search.

### From Yelle's Approach
The "triangular remainder" concept suggests a new filter: compute the triangular remainder for each face triple and check whether the divisibility propagation condition is satisfiable. If certain prime structures are forced, this could eliminate candidates earlier in the pipeline.

### From Algebraic Geometry (Stoll-Testa)
The fact that the cuboid surface is of general type (Picard rank 64) suggests that any solution, if it exists, must lie on a very specific sublocus. Computing the Brauer group of the surface could definitively settle the question via the Brauer-Manin obstruction.

## 5. Overall Assessment

| Paper | Year | Claim | Status | Key Issue |
|-------|------|-------|--------|-----------|
| Wyss | 2015 | Non-existence | Refuted | Gaussian integer argument gaps (Sharipov) |
| Lloyd | 2022 | Non-existence | Unverified | Critical step questioned, withdrawn once |
| Yelle | 2026 | Non-existence | Too recent | Novel method, awaiting peer review |
| Maiti | 2020 | Non-existence | Unverified | Not widely examined |

**The problem remains open.** The strongest theoretical argument for non-existence comes not from these proof attempts but from Stoll-Testa's result that the cuboid surface is of general type, which (assuming the Bombieri-Lang conjecture) implies rational points are extremely rare.

## References
All cited keys refer to entries in sources.bib.
