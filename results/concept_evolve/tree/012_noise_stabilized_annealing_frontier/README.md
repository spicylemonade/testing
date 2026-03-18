# noise_stabilized_annealing_frontier

## Topic context
Use fluctuation-stabilized and noise-dependent memories as a search strategy rather than as a claim about the proof system itself. Carefully injected stochasticity may help the search escape brittle local motifs before a deterministic extraction stage decides whether anything exact and useful was found.

Primary domains: nonequilibrium_statistical_physics, stochastic_optimization, additive_combinatorics.

Mathematical sketch:
Let \rho_\eta be a stochastic local rule with noise parameter \eta. Define F(\eta)=\mathbb{E}[S_{\mathrm{extract}}(\rho_\eta)] and run an annealed search over \eta and rule parameters, keeping only motifs whose deterministic compiled core remains legal when \eta\to 0 or after freezing the discovered pattern.

Closest prior art:
- Exploring the Landscape of Non-Equilibrium Memories with Neural Cellular Automata (arXiv:2508.15726)
- A Toom rule that increases the thickness of sets (DOI:10.1007/BF01015567)
- CAX: Cellular Automata Accelerated in JAX (arXiv:2410.02651)

Novelty claim:
The novelty is methodological: use stochastic memory phenomena to improve exploration of exact certificate space, then strip the noise away before claiming success.

Differentiation:
This is not a stochastic proof system. If exact deterministic extraction does not preserve the gain, the concept fails by design.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
