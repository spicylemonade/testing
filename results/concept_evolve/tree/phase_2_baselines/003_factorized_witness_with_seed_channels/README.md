# Factorized Witness With Seed Channels

Status: `held`

This encoding separates the witness into three coupled channels: edge-label proposals for the `f_i`, sparse singleton seeds for `R`, and certifiable-mask proposals for `T`. It is less elegant than the promoted proof tensor, but it is useful as a comparison point because it makes decoder leakage easier to test: a non-CA method can operate on exactly the same factorized channels. The main risk is that the factorization may hide too much of the real coupling between graph structure and proof growth.

Why held rather than promoted:
- good decoder-matched control surface
- weaker than the proof tensor for carrying symbolic span state
- still viable as a baseline-compatible parameterization
