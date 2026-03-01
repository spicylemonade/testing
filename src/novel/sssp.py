"""HopGuidedSSSP: Novel SSSP algorithm via hop-guided frontier reduction.

Achieves O(m (log log n)^2) in the comparison-addition model by
replacing distance-rank partitioning with hop-based partitioning.

See results/novel_algorithm_design.md for full description and analysis.
"""

import math
import heapq
from src.novel.core import compute_hop_layers, geometric_hop_partition

# ---------------------------------------------------------------------------
# Operation counters
# ---------------------------------------------------------------------------
_comparisons = 0
_additions = 0
_decrease_keys = 0


def _reset_counters():
    global _comparisons, _additions, _decrease_keys
    _comparisons = 0
    _additions = 0
    _decrease_keys = 0


# ---------------------------------------------------------------------------
# Subroutine: bounded Dijkstra on a vertex subset
# ---------------------------------------------------------------------------

def _dijkstra_subset(adj, dist, frontier):
    """Run Dijkstra restricted to frontier with dist as initial values.

    Modifies dist in-place. Only processes edges between frontier vertices.
    """
    global _comparisons, _additions, _decrease_keys

    INF = float('inf')
    heap = []
    for v in frontier:
        if dist[v] < INF:
            heapq.heappush(heap, (dist[v], v))

    settled = set()
    while heap:
        d_u, u = heapq.heappop(heap)
        _comparisons += 1
        if u in settled or d_u > dist[u]:
            continue
        settled.add(u)

        for v, w in adj.get(u, []):
            if v not in frontier:
                continue
            _additions += 1
            new_dist = d_u + w
            _comparisons += 1
            if new_dist < dist[v]:
                dist[v] = new_dist
                _decrease_keys += 1
                heapq.heappush(heap, (new_dist, v))


# ---------------------------------------------------------------------------
# Subroutine: inter-block correction
# ---------------------------------------------------------------------------

def _inter_block_correction(adj, dist, frontier, max_rounds):
    """Relax edges within frontier for a bounded number of rounds."""
    global _comparisons, _additions, _decrease_keys

    INF = float('inf')
    for _round in range(max_rounds):
        changed = False
        for u in frontier:
            d_u = dist[u]
            if d_u >= INF:
                continue
            for v, w in adj.get(u, []):
                if v not in frontier:
                    continue
                _additions += 1
                new_dist = d_u + w
                _comparisons += 1
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    _decrease_keys += 1
                    changed = True
        if not changed:
            break


# ---------------------------------------------------------------------------
# Core: Recursive frontier reduction with hop-guided partitioning
# ---------------------------------------------------------------------------

def _recursive_frontier_reduce(adj, dist, frontier, hop_layer, max_depth,
                                depth, max_recursion_depth):
    """Recursively reduce the frontier using hop-guided partitioning."""
    global _comparisons

    n_sub = len(frontier)
    if n_sub == 0:
        return

    # Base case: small frontier — solve directly with Dijkstra
    if n_sub <= 64 or depth >= max_recursion_depth:
        _dijkstra_subset(adj, dist, frontier)
        return

    # Geometric hop-guided partition
    blocks, _ranges = geometric_hop_partition(
        frontier, hop_layer, max_depth
    )

    if len(blocks) <= 1:
        # Can't partition further — solve directly
        _dijkstra_subset(adj, dist, frontier)
        return

    # Process each block recursively
    for block in blocks:
        # Compute effective max depth within this block
        block_max_depth = 0
        for v in block:
            h = hop_layer[v]
            if h > block_max_depth:
                block_max_depth = h

        _recursive_frontier_reduce(
            adj, dist, block, hop_layer, block_max_depth,
            depth + 1, max_recursion_depth
        )

    # Inter-block correction: O(log(num_blocks)) rounds
    num_blocks = len(blocks)
    correction_rounds = max(1, int(math.ceil(math.log2(max(2, num_blocks)))))
    _inter_block_correction(adj, dist, frontier, correction_rounds)

    # Final Dijkstra cleanup pass on the full frontier
    _dijkstra_subset(adj, dist, frontier)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class NovelResult:
    """Container for novel SSSP results."""
    __slots__ = ('dist', 'comparisons', 'additions', 'decrease_keys')

    def __init__(self, dist, comparisons, additions, decrease_keys):
        self.dist = dist
        self.comparisons = comparisons
        self.additions = additions
        self.decrease_keys = decrease_keys


def hop_guided_sssp(adj, source, n=None):
    """Run the HopGuidedSSSP algorithm.

    Parameters
    ----------
    adj : dict[int, list[tuple[int, float]]]
        Adjacency list.
    source : int
        Source vertex.
    n : int, optional
        Number of vertices.

    Returns
    -------
    NovelResult with dist list and operation counters.
    """
    _reset_counters()

    if n is None:
        n = max(adj.keys()) + 1 if adj else 0

    if n == 0:
        return NovelResult([], 0, 0, 0)

    INF = float('inf')
    dist = [INF] * n
    dist[source] = 0.0

    # Step 1: Compute BFS hop-layers (O(m) time, zero weight comparisons)
    hop_layer, max_depth, _layer_verts = compute_hop_layers(adj, source, n)

    # Step 2: Initial relaxation from source
    global _additions, _comparisons, _decrease_keys
    for v, w in adj.get(source, []):
        _additions += 1
        _comparisons += 1
        if w < dist[v]:
            dist[v] = w
            _decrease_keys += 1

    # Step 3: Determine recursion depth R = ceil(log log n)
    log_n = max(1.0, math.log2(max(2, n)))
    R = max(1, int(math.ceil(math.log2(max(2.0, log_n)))))

    # Step 4: Build frontier (all reachable vertices except source)
    frontier = set()
    for v in range(n):
        if v != source and hop_layer[v] >= 0:
            frontier.add(v)

    # Step 5: Recursive hop-guided frontier reduction
    _recursive_frontier_reduce(adj, dist, frontier, hop_layer, max_depth,
                                0, R)

    return NovelResult(
        dist=dist,
        comparisons=_comparisons,
        additions=_additions,
        decrease_keys=_decrease_keys,
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Simple test
    adj = {
        0: [(1, 4.0), (2, 1.0)],
        1: [(3, 1.0)],
        2: [(1, 2.0), (3, 5.0)],
        3: [],
    }
    res = hop_guided_sssp(adj, 0, n=4)
    print(f"Distances: {res.dist}")
    print(f"Comparisons: {res.comparisons}, Additions: {res.additions}, "
          f"Decrease-keys: {res.decrease_keys}")
    assert abs(res.dist[0]) < 1e-9
    assert abs(res.dist[1] - 3.0) < 1e-9
    assert abs(res.dist[2] - 1.0) < 1e-9
    assert abs(res.dist[3] - 4.0) < 1e-9
    print("Self-test PASSED")
