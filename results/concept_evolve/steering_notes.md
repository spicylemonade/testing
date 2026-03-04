# Steering Notes — Chvátal–Sankoff Constant Research

## Direction 1: Multi-Spin Monte Carlo + KPZ Finite-Size Scaling

**Concept Card:** `finite_size_scaling_extrapolation` (card #009)
- **Implementation Hypothesis:** Combine multi-spin coding with GPU parallelism. Run for n up to 10^7. Apply both polynomial and KPZ-informed scaling ansätze. Compare γ₂ estimates from different extrapolation methods.
- **What I will implement:** A bit-parallel LCS computation using 64-bit multi-spin coding. Generate massive Monte Carlo data for n ∈ {100, 500, 1000, 5000, 10000, 50000}. Fit three finite-size scaling models: (a) γ_n = γ₂ + c₁/n^{1/3}, (b) γ_n = γ₂ + c₁/n^{1/3} + c₂/n^{2/3}, (c) polynomial 1/n. Use the best fit to extrapolate γ₂.

**Bridge Chains Used:**
1. `statistical_mechanics_to_computation`: stochastic_particle_lcs → LPP → KPZ → finite_size_scaling → monte_carlo_multi_spin
2. `probability_to_algorithms`: subadditive_ergodic → KPZ → LPP → OT → LP

**Rubric Items Informed:** item_007, item_011, item_014, item_020

## Direction 2: Frog Dynamics + Periodic Word Optimization for Lower Bounds

**Concept Card:** `frog_dynamics_pushtasep` (card #002)
- **Implementation Hypothesis:** Extend frog dynamics to handle random-vs-random case. Search over periodic words of increasing period to tighten bounds. The constant γ(W*) for the best periodic word W* serves as a lower bound on γ₂.
- **What I will implement:** Simulate frog dynamics on a ring for all binary periodic words of period p ≤ 12. For each word, compute γ(W) via long-run simulation. Track the maximum γ(W) across all words and periods. This directly produces a provable lower bound on γ₂.

**Bridge Chain Used:**
1. `particle_systems_loop`: frog_dynamics ↔ stochastic_particle_lcs ↔ cellular_automata ↔ frog_dynamics

**Novel Twist:** Instead of just enumerating periodic words, use a gradient-free optimization (simulated annealing) over the space of periodic words to find the optimal word W* more efficiently. Also test whether palindromic words (Briggs et al. 2024) yield systematically better bounds.

**Rubric Items Informed:** item_017, item_012, item_018

## Direction 3: Information-Theoretic Upper Bound via Deletion Channel Connection

**Concept Card:** `information_bottleneck_bounds` (card #005)
- **Implementation Hypothesis:** Formulate γ₂ as the solution to an information-theoretic optimization. Use the Blahut-Arimoto algorithm to numerically solve the mutual information maximization.
- **What I will implement:** Map LCS to a channel coding problem where the "channel" is defined by the LCS alignment. Use entropy chain rule to derive H(LCS alignment | X, Y) bound. Numerically compute the bound for increasing Markov chain orders.

**Bridge Chain Used:**
1. `information_theory_to_optimization`: information_bottleneck → optimal_transport → LP_relaxation → monte_carlo
2. `dynamical_systems_to_bounds`: cellular_automata → stochastic_particle → mean_field_cavity → information_bottleneck

**Novel Twist:** Combine the deletion channel connection (Kash-Mitzenmacher 2011) with modern capacity bounds (Rubinstein-Con 2023) to derive a new upper bound on γ₂. The key insight: if we model LCS as a communication channel, known capacity upper bounds constrain γ₂.

**Rubric Items Informed:** item_015, item_013, item_019
