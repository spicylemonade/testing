# Raw Slope Species Grid

Status: rejected

## Encoding

Each cell stores one symbol from `{0} U (X \\ {0})`, so the CA state is just a direct slope or particle-species label field. Decoding reads those labels as local edge or flow suggestions.

## Why It Was Considered

This is the simplest CA-native encoding and it lines up with the generated `anisotropic_current_screening` concept from `results/concept_evolve/tree/001_anisotropic_current_screening/`.

## Why It Is Rejected

- It is exactly the encoding most likely to collapse into bounded-slope or low-rational-complexity behavior.
- It encourages directional-current proxies instead of proof-carrying witness state.
- It is too easy for apparent signal to survive because of transport geometry rather than arithmetic structure.

## Decision

Reject for baseline work. Keep only as a negative-control encoding.
