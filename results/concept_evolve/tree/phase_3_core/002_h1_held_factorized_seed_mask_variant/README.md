# H1 Held: Factorized Seed / Mask Variant

Status: `held`

This variant keeps the proof-carrying idea but separates edge labels, singleton seeds, and `T` masks into distinct channels. It is useful because it exposes decoder leakage more clearly than the active branch, but it also risks hiding too much of the coupling between graph structure and proof growth. It stays held as a subordinate H1 variant rather than the active branch.
