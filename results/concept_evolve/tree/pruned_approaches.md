# Concept Tree Pruning: Failed Branches and Structural Insights

Following the experimental evaluations and the ConceptEvolve reframing phase, we must prune several initial conceptual pathways that failed to yield actionable bounds for $R(5,5)$ and consolidate the structural insights gained.

## Pruned Branch 1: Pure Algebraic Curves / Finite Geometries (e.g., Hermitian Matrices over $\mathbb{F}_q$)
* **Original Hypothesis**: The highly symmetric intersection properties of finite geometries natively construct optimal Ramsey graphs without brute force.
* **Why it Failed**: As seen in `experiments/baseline_evaluation_results.md` and `experiments/candidate_evaluation.md`, purely symmetric algebraic structures (like the Paley graph $P(41)$) intrinsically lock the density of the graph at $0.5$ and enforce uniform distributions of triangles. This uniform symmetry, while mathematically beautiful, rigidly enforces the creation of macroscopic cliques ($K_5$) at sizes $N \ge 41$. The structure is mathematically 'too perfect', leaving no degrees of freedom to avoid the inevitable combinatorics of $K_5$.
* **Structural Insight**: Optimal Ramsey constructions for $R(5,5)$ MUST break global symmetries. They cannot be vertex-transitive or strongly regular in the classic sense. This led directly to our "Twisted Algebraic Generator" which breaks orbits.

## Pruned Branch 2: Continuous Relaxation via Spectral / SDP Bounds (Lovász $\vartheta$)
* **Original Hypothesis**: We can use continuous spectral bounds (Hoffman bound or an SDP relaxation of Lovász $\vartheta$) to analytically prove $K_5$-freeness on unverified target matrices $N=43$.
* **Why it Failed**: The relaxation gap. For small graphs ($N < 25$), $\vartheta(G) \approx \omega(G)$. But as $N \to 43$, a perfectly valid $K_5$-free graph might have an algebraic relaxation bound of $\vartheta = 6.0$. Because $6.0 > 5$, the continuous math fails to certify the discrete reality.
* **Structural Insight**: We cannot replace discrete constraint checking with continuous spectral bounding when hunting for exact proofs near the critical threshold. Spectral bounds are merely fast *filters*, not *certifiers*. The absolute constraint must be embedded discretely (e.g., inside the spin values of a Tensor Network) to avoid the relaxation gap.

## Pruned Branch 3: Holographic Bulk Reconstruction (AdS/CFT analogy)
* **Original Hypothesis**: Embed $K_N$ into a discrete hyperbolic lattice and calculate minimal spanning volumes to find 'entanglement wedges' signaling $K_5$.
* **Why it Failed**: The mathematical formalization of discrete boundary states to bulk topological holes was too far removed from the strict Boolean satisfiability needed to actually prove a bound. It remained an abstract analogy without a computable matrix form.
* **Structural Insight**: Focus strictly on the partition function of the Boolean state, not geometrical embeddings of the edges.

## The Surviving Core
By pruning these, we converge exclusively on the Thermodynamic Machine Learning Chain (GFlowNet learning $Z(N)$) and Quantum Tensor Networks (contracting the exact norm of the constraint space). Both methods explicitly address the symmetry failure and the continuous relaxation gap.
