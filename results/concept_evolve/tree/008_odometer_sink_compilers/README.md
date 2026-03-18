# Odometer Sink Compilers

Precompile candidate witness scaffolds into abelian networks with explicit sink placements and use odometer profiles to predict which regions are close to certifiable collapse into T. The distinctive search variable is sink geometry on the product grid and how it concentrates certificate pressure.

## Context
A compiler \mathcal{C} sends a scaffold H to an abelian network A(H,s) with sink set s. Let u_s(v) be the resulting odometer. Search sink placements and local label templates that maximize \mathrm{Corr}(u_s(v),1_{v\in T_\infty}) while minimizing decoded score S.

## Implementation Backlog
- Prototype the bridge: For each small scaffold, build the abelian network once, sweep sink placements and local labels, benchmark odometer features against depth and degree baselines, and use winning sink geometries to initialize R or glue edges.
- Run the seed test: Benchmark 100-500 small scaffolds with matched depth/degree controls and label-shuffled variants. Stop immediately if odometer features do not outperform trivial graph baselines.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Abelian Networks I. Foundations and Examples (10.1137/15M1030984)
- Integral Flow and Cycle Chip-Firing on Graphs (10.1007/s00026-021-00542-7)
- Bounds on arithmetic projections, and applications to the Kakeya conjecture (10.4310/MRL.1999.v6.n6.a3)

## Novelty Delta
This turns sink placement into a tunable compiler parameter for exact arithmetic forcing rather than treating abelian dynamics as a loose analogy.

## Why It Is Distinct
The invariant is used only to choose arithmetic witness geometry and seeds; the abelian network itself is not the target object.
