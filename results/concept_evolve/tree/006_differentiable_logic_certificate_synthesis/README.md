# differentiable_logic_certificate_synthesis

## Topic context
Use differentiable logic cellular automata to learn discrete, asynchronous local rules that are already close to verifier-compatible behavior. The training objective is a surrogate for extracted arithmetic Kakeya score plus hard penalties for any pattern that cannot be compiled into exact singleton-supported relations.

Primary domains: neural_cellular_automata, differentiable_logic, program_synthesis.

Mathematical sketch:
Let \phi_\theta: \{0,1\}^m \to \{0,1\}^m be a local recurrent circuit with shared parameters. Unroll it on a grid to obtain states h_{v,t}; map selected channels to edge labels and seed flags. Train \theta to minimize \mathcal{L}(\theta)=\widehat{S}(\theta)+\lambda_1\,\mathrm{illegal}(\theta)+\lambda_2\,\mathrm{noncompile}(\theta), then keep only solutions whose extracted certificate is exact.

Closest prior art:
- Differentiable Logic Cellular Automata: From Game of Life to Pattern Generation (arXiv:2506.04912)
- Growing Neural Cellular Automata (DOI:10.23915/distill.00023)
- CAX: Cellular Automata Accelerated in JAX (arXiv:2410.02651)

Novelty claim:
The concept is new only if discrete learned rules can be compiled into exact arithmetic certificates, not merely into attractive visual patterns or robust memories.

Differentiation:
Unlike standard NCA work, success is not judged by reconstruction, regeneration, or aesthetic pattern quality. The only success criterion is exact extracted score under the arithmetic verifier.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
