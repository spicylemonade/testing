# 011 — Neural Trajectory Predictor

## Concept

The neural trajectory predictor treats Collatz delay prediction as a supervised learning problem: given the binary representation of an integer n, predict its stopping delay D(n). A 1D convolutional neural network (CNN) learns to map bit patterns to delays, capturing the local and hierarchical structure in binary representations that correlates with trajectory length.

The key innovation is what happens after training: rather than merely predicting delays for known numbers, we perform gradient ascent on the continuous relaxation of the input bit vector to find inputs that maximize predicted delay. This "dreaming" procedure generates candidate high-delay numbers that the network believes will have extreme trajectories — candidates that can then be verified by direct computation.

This is analogous to AlphaFold predicting protein structure from amino acid sequence: the network learns a complex structure-function mapping, and the learned representation can be inverted to guide search. In drug discovery, similar gradient-based input optimization generates novel molecular candidates with desired properties.

## Cross-Domain Connections

- **AlphaFold / protein structure prediction**: AlphaFold learns to predict 3D structure from 1D sequence. The neural trajectory predictor learns to predict a scalar property (delay) from a 1D representation (bits). Both exploit the fact that local patterns compose hierarchically to determine global behavior.
- **Neural combinatorial optimization**: Methods like Pointer Networks and attention-based models learn heuristics for NP-hard problems (TSP, VRP) from data. The trajectory predictor similarly learns a heuristic for the computationally expensive delay function.
- **Generative drug discovery**: In molecular generation, gradient-based optimization in latent space produces molecules with desired properties. Input-space gradient ascent on the delay predictor is the discrete analog.
- **Adversarial examples**: Gradient-based input perturbation in adversarial ML reveals model sensitivities. Here, we repurpose the same technique constructively — finding inputs that maximize a desired output.

## Implementation Backlog

1. **Training data generation** — Compute (bits(n), delay(n)) pairs for 1M randomly sampled integers across multiple bit-length ranges. Store as memory-mapped dataset for efficient loading.
2. **1D CNN architecture** — Design and train a 1D CNN with residual connections, batch normalization, and multi-scale kernels. Validate on held-out test set; target R^2 > 0.85 for delay prediction.
3. **Gradient-based input optimization** — Relax binary inputs to continuous [0,1]^B. Perform projected gradient ascent to maximize predicted delay. Round to nearest binary vector and verify actual delay.
4. **Candidate scoring pipeline** — Score 10M candidate integers using the trained network. Rank by predicted delay. Compute actual delays for top 100 candidates and measure precision of the predictor at the extreme tail.
5. **Interpretability analysis** — Visualize learned CNN filters and attention maps. Identify which bit positions and local patterns the network uses to predict high delays. Compare to known modular arithmetic structure of delay champions.
