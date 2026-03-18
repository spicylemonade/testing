# Stage-Indexed Certificate Tensor

Status: retained fallback

## Encoding

Represent the witness directly as sparse channels over the product grid: channels for candidate nonzero `f_i` entries, singleton-supported `R` seeds, and initial `T` markers. This is less compressed than the macrocell encoding, but it is transparent and easy to hand to non-CA baselines.

## Why It Matters

- It minimizes decoder ambiguity because the parameterization is already close to the six-line witness.
- It supports fair decoder-matched search and whole-witness mutation baselines.
- It is less expressive than the macrocell library, but more auditable.

## Decision

Keep as the fallback parameterization if the promoted macrocell encoding proves too indirect for a future exact verifier.
