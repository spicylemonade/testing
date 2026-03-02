# Future Research Directions

The following directions are motivated by findings from this computational investigation and by gaps in the current literature.

## Direction 1: GPU-Accelerated Modular Sieve Search

### Problem Statement
Current CPU-based searches reach edges of approximately 10^13 [matson2014]. Extending the verified non-existence bound by 2-3 orders of magnitude would strengthen the computational evidence for non-existence.

### Why Current Methods Are Insufficient
Our combined search achieves >10^6x speedup over brute force but is still limited by single-core throughput. The modular filter (99.8% rejection) and triple decomposition are inherently parallelizable but have not been implemented on GPU hardware.

### Proposed Approach
Implement the multi-modulus quadratic residue sieve on GPU (CUDA/OpenCL). The sieve's structure — checking residue membership in precomputed tables for each of 50 primes — maps naturally to SIMD parallelism. Each GPU thread evaluates one candidate triple against all sieve stages. With modern GPUs achieving 10^12 integer operations/second, this could extend the verified bound to edges of 10^16 or beyond. **Estimated feasibility:** High. The modular sieve requires only integer arithmetic and table lookups, ideal for GPU execution.

### References
[matson2014], [roberts2009], [butler_web]

---

## Direction 2: Brauer-Manin Obstruction Computation

### Problem Statement
Determine whether the Stoll-Testa cuboid surface exhibits a Brauer-Manin obstruction to the existence of rational points, which would definitively prove non-existence.

### Why Current Methods Are Insufficient
Stoll and Testa [stolltesta2010] proved the cuboid surface is of general type with Picard rank 64, implying (under Bombieri-Lang) that rational points are confined to finitely many curves. However, this does not prove non-existence: it only constrains where solutions could lie. Computing the Brauer group Br(S)/Br(Q) would determine whether local-global obstructions exist.

### Proposed Approach
1. Compute the Brauer group of the cuboid surface using the etale cohomology data from [stolltesta2025].
2. For each non-trivial Brauer class, evaluate the local invariants at all primes p and at the real place.
3. If the sum of local invariants is non-zero for any Brauer class, this proves the Brauer-Manin obstruction exists — and thus no perfect cuboid exists.

This requires expertise in computational algebraic geometry (Magma/SageMath). The L-function data computed by Stoll-Testa [stolltesta2025] provides necessary inputs. **Estimated feasibility:** Medium. The surface's complexity (48 singularities, Picard rank 64) makes explicit Brauer group computation challenging but within reach of current tools.

### References
[stolltesta2010], [stolltesta2025], [vanluijk2000]

---

## Direction 3: Machine Learning for Near-Miss Pattern Recognition

### Problem Statement
Identify structural patterns in near-miss Euler bricks that could either (a) guide search toward a solution or (b) reveal an algebraic obstruction.

### Why Current Methods Are Insufficient
Our near-miss analysis found a weak power-law trend (R^2 = 0.025) and no clear prime factorization pattern. Human analysis of 1,714 near-misses cannot detect subtle high-dimensional patterns.

### Proposed Approach
1. Train a graph neural network on the Euler brick constraint graph (edges as nodes, Pythagorean relations as edges) to predict near-miss scores from edge parametrization data (m, n values of constituent Pythagorean triples).
2. Use the trained model to identify "anomalous" Euler bricks — those the model predicts should have very low near-miss scores — and prioritize these for deeper analysis.
3. Apply symbolic regression (e.g., PySR) to discover closed-form relationships between near-miss scores and edge parameters.
4. If the model reveals that near-miss scores are bounded away from zero by a discoverable function, this provides heuristic evidence for non-existence.

**Estimated feasibility:** Medium-high. Requires ML infrastructure but the dataset (1,714+ labeled examples) is sufficient for initial experiments.

### References
[matson2014], [rathbun2017]

---

## Direction 4: Formal Verification of Proof Attempts

### Problem Statement
Multiple non-existence proofs have been claimed [lloyd2022, wyss2015, yelle2026] but none has been accepted through peer review. Formal verification could definitively validate or refute these claims.

### Why Current Methods Are Insufficient
Manual peer review of number theory proofs is slow and error-prone. The critical steps in the claimed proofs involve subtle algebraic manipulations (coprimality arguments, unit handling in Z[i], divisibility propagation) where human reviewers may miss gaps.

### Proposed Approach
1. Formalize the most promising proof attempt (Yelle's additive parametrization [yelle2026]) in a proof assistant (Lean 4 or Coq).
2. Encode the Pythagorean triple parametrization, the triangular remainder definition, and the propagation lemma.
3. If the proof formalizes completely, we have a verified proof of non-existence. If a step fails to formalize, we have pinpointed the exact gap.
4. As a secondary target, formalize Lloyd's odd-space-diagonal argument [lloyd2022] to determine whether the critical coprimality step is valid.

**Estimated feasibility:** Medium. Lean's Mathlib already has Pythagorean triple theory and basic number theory. The novel constructions (triangular remainder) would need to be built from scratch.

### References
[lloyd2022], [yelle2026], [wyss2015], [sharipov2017]

---

## Direction 5: Triangular Remainder Sieve (from Yelle's Construction)

### Problem Statement
Yelle's "triangular remainder" [yelle2026] defines a new invariant for Pythagorean triples that couples the three faces of a cuboid. If the propagation mechanism is valid, this invariant provides a powerful new sieve; if not, understanding why may still yield improved filters.

### Why Current Methods Are Insufficient
Our modular sieve uses classical QR analysis [roberts2009] which treats each face diagonal independently. The triangular remainder is the first proposed invariant that couples all three faces through their shared edge structure, potentially capturing constraints that per-face filters miss.

### Proposed Approach
1. Implement the triangular remainder computation: for each Euler brick (a, b, c), compute the additive parametrization and the remainder r(a,b), r(b,c), r(a,c).
2. Test whether Yelle's propagation lemma holds empirically on all 1,714 known Euler bricks: does a prime dividing one remainder always divide all three?
3. If the propagation holds, implement it as an additional sieve stage and measure improvement in rejection rate beyond the current 99.8%.
4. If the propagation fails for specific examples, these counterexamples identify the exact gap in Yelle's proof.

**Estimated feasibility:** High. This is a straightforward implementation and empirical test that could be completed quickly, with high information value regardless of outcome.

### References
[yelle2026], [roberts2009], [kraitchik1945]

---

## Direction 6: Lattice Reduction and Geometry of Numbers

### Problem Statement
Characterize the lattice structure of the integer points satisfying the cuboid equations and determine whether lattice reduction algorithms (LLL, BKZ) can efficiently find solutions or prove their absence.

### Why Current Methods Are Insufficient
Current search methods enumerate candidates and test conditions. Lattice reduction takes a different approach: it finds short vectors in lattices defined by the constraint equations. For problems with multiple simultaneous Diophantine equations, lattice methods can be exponentially more efficient than enumeration.

### Proposed Approach
1. Reformulate the cuboid system as a lattice problem: the four equations a^2+b^2=d^2, b^2+c^2=e^2, a^2+c^2=f^2, a^2+b^2+c^2=g^2 define a lattice in R^7.
2. Apply LLL reduction to find short vectors, which correspond to small solutions.
3. Use Coppersmith's method or its generalizations to find small roots of the multivariate polynomial system modulo large integers.
4. Analyze the lattice's successive minima to determine whether solutions below a given bound can exist.

**Estimated feasibility:** Medium. Lattice methods for multivariate Diophantine equations are well-studied but their application to this specific system is unexplored. The high dimensionality (7 variables, 4 constraints) may limit effectiveness.

### References
[vanluijk2000], [stolltesta2010], [guy2004]

---

## Summary

| # | Direction | Type | Feasibility | Potential Impact |
|---|-----------|------|-------------|-----------------|
| 1 | GPU-accelerated sieve | Computational | High | Extend verified bound by 10^3x |
| 2 | Brauer-Manin obstruction | Algebraic geometry | Medium | Definitive proof of non-existence |
| 3 | ML pattern recognition | Cross-domain | Medium-high | Novel structural insights |
| 4 | Formal verification | Proof theory | Medium | Validate/refute claimed proofs |
| 5 | Triangular remainder sieve | Number theory | High | New coupled sieve + test of Yelle |
| 6 | Lattice reduction | Geometry of numbers | Medium | Alternative search paradigm |
