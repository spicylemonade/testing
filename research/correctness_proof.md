# Correctness Proof for BALT-H

## Theorem
BALT-H returns the exact shortest path distance `d(s,t)` for any pair of vertices
`(s,t)` in a graph with non-negative edge weights, or `∞` if `t` is unreachable
from `s`.

## Proof Sketch

The proof proceeds by establishing three properties: (1) admissibility of the
landmark lower bounds, (2) correctness of the bidirectional Dijkstra with
g-value ordered heaps, and (3) safety of the pruning optimizations.

### Property 1: Landmark Lower Bounds Are Admissible

**Claim:** For any vertex `v` and target `t`, `lower_bound_forward(v, t) ≤ d(v, t)`.

**Proof:** By the triangle inequality on shortest path distances:
- For any landmark `L`: `d(L, t) ≤ d(L, v) + d(v, t)`, hence `d(L, t) - d(L, v) ≤ d(v, t)`
- For any landmark `L`: `d(v, L) ≤ d(v, t) + d(t, L)`, hence `d(v, L) - d(t, L) ≤ d(v, t)`

The lower bound is `max(0, max_L(d(L,t) - d(L,v), d(v,L) - d(t,L)))`, which is
the maximum of values each ≤ `d(v,t)`, hence the bound is admissible. An analogous
argument holds for `lower_bound_backward`. ∎

### Property 2: Bidirectional Dijkstra with G-Value Ordering Is Correct

**Claim:** The bidirectional search with termination condition `g_min_f + g_min_b ≥ μ`
returns the exact shortest path distance.

**Proof:** This follows the standard correctness proof of bidirectional Dijkstra
(Pohl, 1971; Nicholson, 1966):

1. **Monotonicity:** Because heaps are ordered by g-values (not f-values), the
   sequence of g-values extracted from each heap is monotonically non-decreasing.
   This is a fundamental property of Dijkstra's algorithm with non-negative weights.

2. **Upper bound maintenance:** `μ` is maintained as `min(μ, g_f(u) + g_b(u))`
   whenever vertex `u` is discovered by both search directions (via dist_f/dist_b
   checks). Hub precomputation initializes μ, which can only decrease. Therefore
   μ is always a valid upper bound on d(s,t) — it represents the length of an
   actual s-t path through some vertex.

3. **Termination soundness:** When `g_min_f + g_min_b ≥ μ`, any unsettled vertex `v`
   satisfies `d(s,v) ≥ g_min_f` and `d(v,t) ≥ g_min_b` (since g-values are
   non-decreasing and Dijkstra settles vertices in order of true distance from source).
   Therefore any path through an unsettled vertex has length ≥ `g_min_f + g_min_b ≥ μ`,
   so no shorter path can be found. ∎

### Property 3: Pruning Preserves Correctness

**Landmark pruning:** When a node `u` is settled with g-value `g` and
`g + lb(u) ≥ μ`, we skip expanding u's neighbors. Since `lb(u) ≤ d(u, t)` (Property 1),
we have `g + d(u, t) ≥ μ`. Any path from s to t through u has length
≥ `d(s, u) + d(u, t) = g + d(u, t) ≥ μ`. Since μ is already achieved by some
known path, skipping u cannot miss the optimal path. ∎

**Settled node pruning:** Skipping relaxation to already-settled vertices is
safe because Dijkstra guarantees that a settled vertex has its optimal distance
from the respective source (forward) or target (backward). Re-relaxation cannot
improve the distance. ∎

**Active landmark selection:** Using a subset of landmarks only affects which
nodes get pruned (fewer landmarks → weaker bounds → fewer nodes pruned). It does
NOT affect which paths are discoverable — it only means some nodes that could have
been pruned will be expanded instead. The search still finds all shortest paths.
Hence correctness is preserved. ∎

### Property 4: Hub Upper Bound Safety

**Claim:** The hub-initialized μ is a valid upper bound on d(s,t).

**Proof:** For each hub h, `d(h, s) + d(h, t)` is the length of a path from s to t
via h (in undirected graphs where d(h,v) = d(v,h)). For directed graphs, this
requires d(s,h) + d(h,t), which needs additional preprocessing (hub_dist_to). The
minimum over all hubs is a valid upper bound since it corresponds to an actual path.
Since μ can only decrease during search, this initialization can only help (not
hurt) correctness. ∎

## Completeness

If t is unreachable from s, no hub can provide a finite upper bound (d(h,s) or
d(h,t) = ∞), so μ remains ∞. The search exhausts all reachable vertices without
finding t, and returns ∞. ∎

## Summary

BALT-H is correct because:
1. It is built on bidirectional Dijkstra with g-value ordering (provably correct)
2. All pruning criteria are safe (landmark bounds are admissible, settled nodes
   have optimal distances)
3. The hub upper bound provides a valid initial μ (corresponds to actual paths)
4. Active landmark selection only weakens pruning, never misses paths
