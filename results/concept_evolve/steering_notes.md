# ConceptEvolve Steering Notes

## 3 Concrete Steering Directions

### Direction 1: Mutation-Based Search from Known Champions (PRIORITIZED)
**Rubric items informed:** item_007, item_008, item_011, item_013, item_017, item_018
**Description:** Implement accelerated TM simulation, reproduce the Kropitz 10↑↑15 champion as baseline, then systematically explore its mutation neighborhood. This is the historically most productive approach — all major BB(6) records were found by perturbing known high-scoring machines.
**Why prioritized:** This is the only approach that has actually produced BB(6) records in practice. It's technically feasible within our compute budget, produces verifiable results, and builds directly on the existing literature. The mutation space is large but structured: single-transition mutations of a 6-state, 2-symbol TM produce 12 × 11 = 132 neighbors per machine.

### Direction 2: Constructive Shift-Overflow-Counter Design
**Rubric items informed:** item_006, item_012, item_015
**Description:** Rather than searching blindly, reverse-engineer the structural pattern of shift overflow counter machines and construct new TMs that implement similar counter hierarchies with different halt conditions. This is a top-down approach that could produce machines competitive with the current champion.
**Why not prioritized:** Requires deep understanding of the specific counter mechanisms used by mxdys, which are only partially documented. The algebraic analysis is complex and may not yield results within our time budget.

### Direction 3: Hybrid GA/SA Search with Fitness Landscape Analysis
**Rubric items informed:** item_012, item_014, item_015, item_016, item_021
**Description:** Apply genetic algorithms and simulated annealing to navigate the TM fitness landscape. Use structural features (transition graph topology, spectral properties) as fitness proxies to avoid expensive simulation. This is the most novel approach and the best candidate for discovering machines in under-explored regions of the search space.
**Why not prioritized:** While theoretically appealing, metaheuristic search over the BB space is largely unexplored in the literature. The fitness landscape is extremely rugged (most machines either loop forever or halt trivially), making optimization challenging. Best used as a complement to Direction 1, not as a replacement.

## Priority Ranking
1. **Direction 1** — Most likely to produce verifiable results
2. **Direction 3** — Most likely to produce novel insights
3. **Direction 2** — Highest ceiling but requires the most domain expertise
