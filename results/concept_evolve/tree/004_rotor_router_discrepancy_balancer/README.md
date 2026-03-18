# Rotor Router Discrepancy Balancer

Use rotor-router dynamics to deterministically balance how nonzero slopes are deployed across copies of a recursive gadget. The hypothesis is that low discrepancy in slope exposure can flatten non-target projections while preserving repeatable cancellation patterns that are useful for arithmetic forcing.

## Context
Assign each interface vertex v a rotor state \rho(v)\in X\setminus\{0\}. Each launch increments \rho(v) cyclically and routes a token along label \rho(v). Let D_x(U) be the discrepancy of visits along slope x inside region U. Search periodic rotor schedules minimizing \max_x D_x while the decoded witness score S remains small.

## Implementation Backlog
- Prototype the bridge: Fix a recursive scaffold, replace free nonzero labels by rotor schedules with short periods, decode one rotor period into f_i dictionaries, and test whether low-discrepancy schedules yield better forcing coverage than random label placement.
- Run the seed test: Use layered-square-lattice style rotors on d_1 x d_2 witnesses with 3-4 nonzero slopes. Compare periodic rotor schedules, random schedules, and label shuffles at equal density.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Rotor-Router Aggregation on the Layered Square Lattice (10.37236/424)
- Abelian Networks I. Foundations and Examples (10.1137/15M1030984)
- Bounds on arithmetic projections, and applications to the Kakeya conjecture (10.4310/MRL.1999.v6.n6.a3)

## Novelty Delta
The new move is to treat rotor discrepancy as a design variable for arithmetic projection control rather than as a deterministic random-walk surrogate.

## Why It Is Distinct
Classical rotor-router work studies shape and load balancing. Here the rotor phase is decoded into exact witness data and judged only by arithmetic score.
