# Repository Structure and Modular Concept Layout

This repository is organized to support a non-computational, advanced multi-disciplinary approach to finding new bounds for Ramsey R(5,5). It incorporates statistical mechanics, algebraic geometry, and quantum tensor networks, all guided by the ConceptEvolve tree.

## Major Modules and Their Purposes

### `1. core/`
- **Purpose**: Defines mathematical primitives, constraint representations, and baseline graph theoretic utilities.
- **Key Components**:
  - `ramsey_constraints.py`: Mathematical formalization of K_5 avoidance.
  - `graph_utils.py`: Basic representations and utility structures for manipulating abstract constraint definitions.

### `2. metrics/`
- **Purpose**: Implements advanced spectral, algebraic, and analytical evaluators that avoid brute-force search.
- **Key Components**:
  - `spectral_bounds.py`: Calculators for Lovász Theta and related spectral invariants.
  - `algebraic_invariants.py`: Scripts evaluating graph ideals, Hilbert polynomials, or related topological homology signatures.
  - `statistical_mechanics.py`: Partition function zero approximations.

### `3. generators/`
- **Purpose**: Translates novel Ansatz ideas (such as GFlowNet distributions or tensor networks) into candidate constraint spaces or matrices.
- **Key Components**:
  - `gflownet_sampler/`: Implementation of the Thermodynamic Flow Rate analysis to learn constraint spaces.
  - `tensor_network/`: Quantum many-body formalisms applied to graph constraints.
  - `algebraic_curves/`: Generators mapping algebraic geometry over finite fields to structural candidates.

### `4. experiments/`
- **Purpose**: Isolated executable scenarios focusing on a specific ConceptEvolve branch.
- **Key Components**:
  - `run_baseline_metrics.py`: Evaluates known K_5-free constructions (like R(4,4)).
  - `tensor_scaling_experiment.py`: Checks exact norm contraction vs bond dimension to find divergences indicating a Ramsey bound.
  - `gflownet_entropy_experiment.py`: Uses generative flow networks to monitor partition function collapse.

### `5. results/concept_evolve/`
- **Purpose**: A living research document managed by `ConceptEvolve`, tracking explored cross-domain analogies.
- **Key Components**:
  - `tree/`: Individual concept folders mapping analogies to testable implementation hypotheses (e.g., `spin_glass_partition_zeros`, `tensor_network_contraction`).
  - `concept_delta.md`: Tracks hypotheses implemented, outcomes, and novel contributions.

### `6. docs/`
- **Purpose**: Analytical synthesis and mathematical documentation.
- **Key Components**:
  - `stricter_bounds_proof.md`: Accumulating proof sketch.
  - `bibliography.bib`: Managed via Semantic Scholar, containing prior literature.

This modular structure ensures that the task of developing stricter Ramsey bounds is distributed across conceptually distinct domains—statistical physics, machine learning, and quantum information—each verifiable and extensible independently.
