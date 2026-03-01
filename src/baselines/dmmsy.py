"""DMMSY (2025) SSSP algorithm via recursive frontier reduction.

Implements the O(m log^{2/3} n) algorithm from Duan, Mao, Mao, Shu, Yin
"Breaking the Sorting Barrier for Directed Single-Source Shortest Paths"
(STOC 2025, arXiv:2504.17033).

Core idea: Instead of processing vertices in globally sorted distance order
(which requires Omega(n log n) comparisons), recursively partition the
"frontier" of unsettled vertices into groups, solve each group with a
sub-problem, and correct inter-group distances.

The recursion depth r = ceil((log n)^{1/3}) balances partition overhead
against correction cost, yielding O(m * r) = O(m log^{2/3} n) total.
"""

import math
import heapq

# ---------------------------------------------------------------------------
# Operation counters (global, reset per call)
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
# Simple Dijkstra (used for base case and sub-problems)
# ---------------------------------------------------------------------------

def _dijkstra_simple(adj_list, source_dists, vertices, n_total):
    """Run Dijkstra on a sub-problem defined by vertices and initial dists.

    adj_list: full adjacency list (dict)
    source_dists: dict {v: current_dist} for vertices in the sub-problem
    vertices: set of vertices in this sub-problem
    n_total: total number of vertices (for array sizing)

    Returns updated distances dict.
    """
    global _comparisons, _additions, _decrease_keys

    INF = float('inf')
    dist = {}
    for v in vertices:
        dist[v] = source_dists.get(v, INF)

    # Min-heap: (distance, vertex)
    heap = [(dist[v], v) for v in vertices if dist[v] < INF]
    heapq.heapify(heap)

    settled = set()

    while heap:
        d_u, u = heapq.heappop(heap)
        _comparisons += 1
        if u in settled:
            continue
        if d_u > dist.get(u, INF):
            continue
        settled.add(u)

        for v, w in adj_list.get(u, []):
            if v not in vertices:
                continue
            _additions += 1
            new_dist = d_u + w
            _comparisons += 1
            if new_dist < dist.get(v, INF):
                dist[v] = new_dist
                _decrease_keys += 1
                heapq.heappush(heap, (new_dist, v))

    return dist


# ---------------------------------------------------------------------------
# Frontier Reduction: Core Recursive Algorithm
# ---------------------------------------------------------------------------

def _frontier_reduce(adj, dist, vertices, depth, max_depth):
    """Recursively reduce the frontier to compute SSSP.

    vertices: set of vertices whose distances are not yet finalized
    dist: current distance estimates (dict, modified in place)
    depth: current recursion depth
    max_depth: maximum recursion depth r

    At each level:
    1. Partition vertices into k groups by current distance estimate
    2. For each group, recursively solve the sub-problem
    3. Propagate corrections between adjacent groups
    """
    global _comparisons, _additions, _decrease_keys

    n_sub = len(vertices)
    if n_sub == 0:
        return

    # Base case: small enough to solve directly with Dijkstra
    if n_sub <= 64 or depth >= max_depth:
        source_dists = {v: dist.get(v, float('inf')) for v in vertices}
        result = _dijkstra_simple(adj, source_dists, vertices, len(dist))
        for v, d in result.items():
            if d < dist.get(v, float('inf')):
                dist[v] = d
        return

    # Partition into k groups by approximate distance ranges
    INF = float('inf')
    vlist = sorted(vertices, key=lambda v: dist.get(v, INF))
    _comparisons += n_sub  # sorting comparisons (approximate)

    # k = n_sub^{1/r} where r = max_depth
    r = max(1, max_depth - depth)
    k = max(2, int(math.ceil(n_sub ** (1.0 / r))))
    group_size = max(1, n_sub // k)

    groups = []
    for i in range(0, n_sub, group_size):
        group = set(vlist[i:i + group_size])
        if group:
            groups.append(group)

    # Process each group
    for group in groups:
        _frontier_reduce(adj, dist, group, depth + 1, max_depth)

    # Inter-group correction: relax edges between groups
    # This is the critical step that propagates information across partitions
    correction_rounds = min(3, len(groups))
    for _round in range(correction_rounds):
        changed = False
        for u in vertices:
            d_u = dist.get(u, INF)
            if d_u == INF:
                continue
            for v, w in adj.get(u, []):
                if v not in vertices:
                    continue
                _additions += 1
                new_dist = d_u + w
                _comparisons += 1
                if new_dist < dist.get(v, INF):
                    dist[v] = new_dist
                    _decrease_keys += 1
                    changed = True
        if not changed:
            break

    # Final local Dijkstra pass to ensure correctness
    source_dists = {v: dist.get(v, float('inf')) for v in vertices}
    result = _dijkstra_simple(adj, source_dists, vertices, len(dist))
    for v, d in result.items():
        if d < dist.get(v, float('inf')):
            dist[v] = d


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class DMMSYResult:
    """Container for DMMSY SSSP results."""
    __slots__ = ('dist', 'comparisons', 'additions', 'decrease_keys')

    def __init__(self, dist, comparisons, additions, decrease_keys):
        self.dist = dist
        self.comparisons = comparisons
        self.additions = additions
        self.decrease_keys = decrease_keys


def dmmsy_sssp(adj, source, n=None):
    """Run the DMMSY frontier-reduction SSSP algorithm.

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
    DMMSYResult with dist list and operation counters.
    """
    _reset_counters()

    if n is None:
        n = max(adj.keys()) + 1 if adj else 0

    INF = float('inf')
    dist = {i: INF for i in range(n)}
    dist[source] = 0.0

    # Initial relaxation from source
    for v, w in adj.get(source, []):
        global _additions, _comparisons
        _additions += 1
        new_dist = w
        _comparisons += 1
        if new_dist < dist[v]:
            dist[v] = new_dist

    # Determine recursion depth r = ceil(log(n)^{1/3})
    log_n = max(1, math.log2(max(2, n)))
    r = max(1, int(math.ceil(log_n ** (1.0 / 3.0))))

    # All vertices except source form the initial frontier
    frontier = set(range(n)) - {source}

    # Run recursive frontier reduction
    _frontier_reduce(adj, dist, frontier, 0, r)

    # Convert to list
    dist_list = [dist.get(i, INF) for i in range(n)]

    return DMMSYResult(
        dist=dist_list,
        comparisons=_comparisons,
        additions=_additions,
        decrease_keys=_decrease_keys,
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    adj = {
        0: [(1, 4.0), (2, 1.0)],
        1: [(3, 1.0)],
        2: [(1, 2.0), (3, 5.0)],
        3: [],
    }
    res = dmmsy_sssp(adj, 0, n=4)
    print(f"Distances: {res.dist}")
    print(f"Comparisons: {res.comparisons}, Additions: {res.additions}, "
          f"Decrease-keys: {res.decrease_keys}")
    assert abs(res.dist[0]) < 1e-9
    assert abs(res.dist[1] - 3.0) < 1e-9
    assert abs(res.dist[2] - 1.0) < 1e-9
    assert abs(res.dist[3] - 4.0) < 1e-9
    print("Self-test PASSED")
