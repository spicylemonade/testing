# Anisotropic Particle-Current Encoding

Status: rejected

## Source Inspiration

- `results/concept_evolve/tree/001_anisotropic_current_screening/concept.json`

## Encoding

Treat each nonzero label in `X` as a particle species and summarize trajectories through directional current or transport statistics. Candidate witnesses are then decoded only from top-ranked trajectories.

## Rejection Reason

- This encoding is too close to a bounded-slope / low-rational-complexity story.
- The state space is naturally small and directional, which is exactly the regime Tao's 2025 warning makes suspect.
- It also invites decoder leakage because the arithmetic content can migrate into the trajectory-to-witness extractor rather than live in the CA state.

## Decision

Reject as a baseline-compatible main encoding. Keep only as a negative-control idea for later novelty-risk discussion.
