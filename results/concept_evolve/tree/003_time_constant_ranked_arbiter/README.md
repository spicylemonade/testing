# Concept: time_constant_ranked_arbiter

- Rank: 3
- Description: Infer which weak source should be granted the first startup shot by comparing its response through two RC windows with different time constants, giving a coarse impedance classification without a powered comparator.
- Key mechanism: A pair of passive time-constant sniffers plus dynamic sense switches can estimate whether a source is low-Z enough to survive a startup pulse.
- Predicted failure mode: Under ultra-slow ramps the RC signatures collapse together and ranking becomes too noisy to matter.

## Dependencies
- fast RC sniffer
- slow RC sniffer
- rank latch
- grant gating

## First Experiment
- Hold source voltages equal and sweep impedance 1:1 to 1:20 to see whether the ranker chooses the source that actually minimizes startup delay and back-drive loss.

## Novelty Guard
- Potentially novel only if the RC ranker materially improves cold-start correctness while costing less than active arbitration or full source comparators.

## Closest Overlap
- Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems (9fd5e15b)
- Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting (254a50d3)
- Multi-Source Energy Harvesting Systems Integrated in Silicon: A Comprehensive Review (6461dab6)
