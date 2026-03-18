# Macrocell Curriculum Nca

Use a neural cellular automaton whose cell states are not raw edges but small verified gadget fragments with conservation flags. Training proceeds by size curriculum and only rewards outputs that decode exactly, forcing the model to learn reusable local proof-growth rules rather than memorize single witnesses.

## Context
Each macrocell state z_t(v) lies in a simplex over a fragment library \mathcal{G}. A local update z_{t+1}(v)=\Phi_\theta(\{z_t(u):u\in N(v)\}) evolves the board. A discretizer D maps z_T to a witness W, and training minimizes \mathbb{E}[S(W)+\mu\,1_{W\ \mathrm{invalid}}] with held-out larger boards used as the generalization test.

## Implementation Backlog
- Prototype the bridge: Build a library of tiny exact gadgets, use them as the NCA alphabet, train with straight-through or Gumbel-style discretization, and let the exact verifier score only the discretized outputs.
- Run the seed test: Train on witnesses with n<=36 and test on n around 64. Run label-shuffle and geometry-shuffle ablations to distinguish arithmetic learning from symmetry matching.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Growing Neural Cellular Automata (10.23915/distill.00023)
- Mathematical discoveries from program search with large language models (10.1038/s41586-023-06924-6)
- AlphaEvolve: A coding agent for scientific and algorithmic discovery (arXiv:2506.13131)

## Novelty Delta
The macrocell representation and exact discrete decode loop make the NCA learn proof growth, not just generic spatial pattern formation.

## Why It Is Distinct
This is not the standard neural-CA image-growth setup and not generic program search; the alphabet is proof-carrying and success is exact arithmetic score.
