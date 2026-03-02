# BARNES_HUT_TREE

Hierarchical quadtree/octree spatial decomposition enabling O(N log N) force approximation. Treats distant particle clusters as single pseudoparticles. The canonical scaling breakthrough for N-body problems.

## Mathematical Formalization

For each body i, traverse tree. At node n with center-of-mass r_n, total mass M_n, size s_n: if s_n/|r_i - r_n| < theta, treat n as point mass. Else recurse into children. Error ~ O(theta^2). Complexity: O(N log N) for theta > 0.

## Analogical Connections

- Barnes-Hut <-> level-of-detail rendering in games (far objects rendered at lower resolution)
- Theta parameter <-> compression ratio (controls accuracy-vs-speed tradeoff)
- Quadtree <-> k-d tree in nearest-neighbor search (spatial indexing with logarithmic lookup)
- Multipole expansion <-> Taylor series (approximate a complex field with a truncated polynomial)

## Implementation Hypothesis

Quadtree node: {center_of_mass, total_mass, bounds, children[4]}. Build tree: O(N log N). Walk tree per body: O(log N) average. Total: O(N log N). ~200 lines for full implementation with insertion, COM update, and force walk.

## Experiment Seed

Compare brute-force vs Barnes-Hut (theta=0.5) for N=100,500,1000,5000. Plot wall-time and force RMS error. Identify crossover N where Barnes-Hut becomes faster (expected ~300-500).
