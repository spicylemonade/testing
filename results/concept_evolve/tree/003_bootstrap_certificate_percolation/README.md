# Bootstrap Certificate Percolation

Approximate R/T closure by an anisotropic bootstrap-percolation rule on the product grid, where a site activates once nearby certificate templates can synthesize an (a,-a) singleton there. This gives a fast local phase diagram for which recursive geometries can sustain sparse but self-amplifying forcing growth.

## Context
On V=d_1\times\cdots\times d_k let \eta_t(v)=1_{v\in T_t}. Choose a template family \mathcal{K}. Update \eta_{t+1}(v)=1 if \eta_t(v)=1 or if there exists K\in\mathcal{K}_v and signed weights \lambda_u with \sum_{u\in K}\lambda_u R_u=(a,-a)e_v modulo already active sites. Search anisotropic template sets that fully activate V at low m+r.

## Implementation Backlog
- Prototype the bridge: Mine local certificate templates from exact small witnesses, run fast bootstrap simulations on larger geometries, and exact-verify only the geometries predicted to fully activate with sparse templates.
- Run the seed test: Fit templates from all exact witnesses with n<=25, then predict which 4x4x4 or 3x3x5 geometries fully activate. Compare exact verification hit rate to random geometry search.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Sharp metastability threshold for two-dimensional bootstrap percolation (10.1007/s00440-002-0239-x)
- Bootstrap percolation, and other automata (10.1016/j.ejc.2017.06.024)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

## Novelty Delta
This makes bootstrap-style threshold analysis depend on arithmetic certificate templates learned from exact witnesses, rather than on generic nearest-neighbor infection rules.

## Why It Is Distinct
It is not just a percolation analogy because activation kernels are derived from verifier-legal linear combinations and are tested against exact closure.
