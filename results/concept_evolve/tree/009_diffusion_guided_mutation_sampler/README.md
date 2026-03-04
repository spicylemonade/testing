# 009 — Diffusion-Guided Mutation Sampler

## Topic Context

Diffusion models generate data by learning to reverse a noise process. For protein sequences, masked diffusion models (e.g., MDLM, D3PM) progressively mask and unmask amino acid tokens. By applying guidance during the reverse (denoising) process, we can steer generation toward sequences with desired properties — in this case, high thermostability.

The key advantage over deterministic search (beam, greedy) is **diversity**: diffusion sampling generates many different solutions per run, exploring the landscape globally rather than following a single gradient path. MCTD-ME (Liu et al. 2025) demonstrated that combining masked diffusion with tree search achieves state-of-the-art on protein inverse folding tasks.

For stability optimization, we exploit a simplified variant: only mask the k mutable positions (not the entire sequence), and guide denoising using the gradient of a stability predictor. This is analogous to classifier-guided diffusion in image generation, where the class label gradient steers image generation.

## Key Connections

- **Partial masking**: Only mutating k positions out of a full sequence is equivalent to inpainting — a well-studied diffusion task
- **Guidance strength**: Lambda controls the diversity-quality trade-off, analogous to temperature in sampling

## Implementation Backlog

1. [ ] Implement masked diffusion at specified positions using ESM-2
2. [ ] Implement stability guidance gradient computation
3. [ ] Add ProteinMPNN structure-conditioned guidance
4. [ ] Implement parallel sampling of N candidates on GPU
5. [ ] Add guidance strength scheduling (anneal lambda during denoising)
6. [ ] Benchmark diversity vs quality at different lambda values
7. [ ] Compare with beam search and MCTS on same protein set
8. [ ] Implement rejection sampling post-filter for constraint satisfaction
9. [ ] Add option for iterative refinement (sample -> score -> re-noise top -> re-denoise)
10. [ ] Profile GPU memory and optimize batch size for A100
