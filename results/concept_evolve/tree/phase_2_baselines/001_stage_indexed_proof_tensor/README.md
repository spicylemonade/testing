# Stage-Indexed Proof Tensor

Status: `promoted`

This encoding treats each product-grid cell as a structured state containing stage-local edge-label proposals, sparse proof-support summaries, and explicit seed channels for `R` and `T`. It is baseline-compatible because the representation is already aligned with the six-line witness format and can be decoded without heuristic repair. Among the candidate encodings considered so far, this is the cleanest match to the witness spec and the easiest to compare against a decoder-matched non-CA baseline.

Why promoted:
- direct path to legal `(X,G,R,T)` decoding
- explicit room for proof-carrying state
- easiest compute-parity comparison against non-CA search
