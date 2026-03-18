# Non-CA Comparator: Decoder-Matched Witness Search

Status: `comparator`

This branch is the explicit non-CA comparison class required for any future experiment claim. It uses the same compiler, extractor, legality filter, and exact score, but replaces the CA with direct proposal search over the witness parameterization. Its role is not to win on novelty, but to prevent decoder leakage and compute-parity mistakes.
