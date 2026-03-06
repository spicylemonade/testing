# event_sparse_far_field

## Context
Cache far-field multipole summaries and refresh them on predicted error events instead of every tick. This reframes tree maintenance as an event-driven problem, borrowing the sparsity mindset of event-driven molecular dynamics for a force law that is otherwise continuously evaluated.

## Domains
- event_driven_simulation
- performance_engineering
- astrophysics

## Mathematical Formalization
Schedule refresh tau_c = min{t : ||M_c(t) - M_c(t_last)|| > delta_M or topology(c) changes}; use a_i(t) = a_near(t) + a_far(M(t_last)) until t >= tau_c

## Closest Prior Art
- Application of event-driven molecular dynamics approach to rarefied gas dynamics problems (`bf741d3dc8d599d9b42d19125a11b1141a805174`)
- Cold atom-ion systems in radio-frequency multipole traps: Event-driven molecular dynamics and stochastic simulations (`9650464407bda642ed29f83febd4b967cf19f591`)
- A hierarchical O(N log N) force-calculation algorithm (`fce7fd98928ab9bf3e4e919e108c48fc1040f569`)

## Novelty
The novelty is not event-driven pairwise gravity, but event-driven maintenance of approximate distant structure, which matches the update patterns of interactive scenes.

## Differentiation
Event-driven molecular dynamics papers schedule actual collisions or interaction events. This concept schedules when a cached approximation becomes too stale, so it changes the bookkeeping layer rather than the physical force law itself.

## Experiment Seed
Use a quasi-stable solar-system scene and a chaotic scattering scene; measure tree-refresh count, wall-clock time, and trajectory error versus rebuilding every frame.

## Implementation Backlog
1. Store per-cell center-of-mass, multipole, and motion bounds.
2. Estimate stale-summary error over time.
3. Schedule refresh events in a priority queue.
4. Measure rebuild savings on quasi-stable scenes.
5. Fallback to full rebuild on pathological invalidation rates.

## Planned Paths
- `results/concept_evolve/tree/006_event_sparse_far_field/concept.json`
- `results/concept_evolve/tree/006_event_sparse_far_field/README.md`
- `results/concept_evolve/tree/006_event_sparse_far_field/literature.json`
- `prototypes/minigrav/force/event_sparse_far_field.py`
- `prototypes/minigrav/benchmarks/tree_refresh_profile.py`
