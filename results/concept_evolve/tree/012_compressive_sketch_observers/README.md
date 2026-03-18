# Compressive Sketch Observers

Attach cheap sketching observers to CA trajectories so rules can be ranked by a compressed summary of local motif counts, directional currents, and closure precursors before full decoding. The link to spatially coupled compressive sensing is that structured sparse observers may preserve the rare signals that correlate with low witness score.

## Context
Let z(F,\Omega) be a high-dimensional vector of motif and current statistics from trajectory \Omega of rule F. Observe y=A z with a sparse spatially coupled matrix A. Fit a conservative predictor \hat{S}(y) and exact-decode only candidates with \hat{S}(y)\leq\tau. The observer is useful only if \Pr[S\leq\sigma\mid \hat{S}\leq\tau] substantially exceeds random triage.

## Implementation Backlog
- Prototype the bridge: Define 50-200 motif counters, build sparse coupled sketches, train a monotone regressor or conformal lower bound from exact small data, and use the sketch as a budgeted filter in front of SAT, NCA, or evolutionary search.
- Run the seed test: Collect a few thousand tiny CA trajectories with exact scores, compare sketch-based triage against raw-density heuristics, and keep the idea only if recall at fixed decode budget improves materially.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- The effect of spatial coupling on compressive sensing (10.1109/ALLERTON.2010.5706927)
- Threshold Saturation via Spatial Coupling: Why Convolutional LDPC Ensembles Perform So Well over the BEC (10.1109/TIT.2010.2095072)
- Mathematical discoveries from program search with large language models (10.1038/s41586-023-06924-6)

## Novelty Delta
The sketches are not trying to reconstruct a signal; they are triaging proof-search dynamics by preserving only the statistics that forecast low score.

## Why It Is Distinct
This is not standard compressive sensing or decoding because the sensed object is a search trajectory and the target is a proof-discovery budget.
