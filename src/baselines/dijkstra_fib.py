"""Dijkstra's SSSP algorithm with a Fibonacci heap.

Implements the classic O(m + n log n) algorithm of Fredman & Tarjan (1987)
with instrumented operation counters for comparisons, additions, and
decrease-key calls.

Graph representation: adjacency list as dict[int, list[tuple[int, float]]].
  adj[u] = [(v, w), ...] means edge u->v with weight w.
"""

import math

# ---------------------------------------------------------------------------
# Fibonacci Heap
# ---------------------------------------------------------------------------

class _FibNode:
    __slots__ = ('key', 'value', 'degree', 'mark', 'parent', 'child',
                 'left', 'right')

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self


class FibonacciHeap:
    """Min-Fibonacci-heap with operation counters."""

    def __init__(self):
        self.min_node = None
        self.n = 0
        self.comparisons = 0
        self.decrease_key_calls = 0

    # -- list helpers --

    @staticmethod
    def _add_to_root_list(heap_min, node):
        if heap_min is None:
            node.left = node
            node.right = node
            return node
        node.right = heap_min.right
        node.left = heap_min
        heap_min.right.left = node
        heap_min.right = node
        return heap_min

    @staticmethod
    def _remove_from_list(node):
        node.left.right = node.right
        node.right.left = node.left

    # -- public API --

    def insert(self, key, value):
        node = _FibNode(key, value)
        self.min_node = self._add_to_root_list(self.min_node, node)
        self.comparisons += 1
        if node.key < self.min_node.key:
            self.min_node = node
        self.n += 1
        return node

    def extract_min(self):
        z = self.min_node
        if z is None:
            return None
        # add children to root list
        if z.child is not None:
            child = z.child
            while True:
                nxt = child.right
                child.parent = None
                self.min_node = self._add_to_root_list(self.min_node, child)
                child = nxt
                if child is z.child:
                    break
        self._remove_from_list(z)
        if z is z.right:
            self.min_node = None
        else:
            self.min_node = z.right
            self._consolidate()
        self.n -= 1
        return z

    def decrease_key(self, node, new_key):
        self.decrease_key_calls += 1
        self.comparisons += 1
        if new_key > node.key:
            return
        node.key = new_key
        parent = node.parent
        if parent is not None:
            self.comparisons += 1
            if node.key < parent.key:
                self._cut(node, parent)
                self._cascading_cut(parent)
        self.comparisons += 1
        if node.key < self.min_node.key:
            self.min_node = node

    def is_empty(self):
        return self.min_node is None

    # -- internals --

    def _cut(self, node, parent):
        if node.right is node:
            parent.child = None
        else:
            if parent.child is node:
                parent.child = node.right
            node.left.right = node.right
            node.right.left = node.left
        parent.degree -= 1
        node.parent = None
        node.mark = False
        node.left = node
        node.right = node
        self.min_node = self._add_to_root_list(self.min_node, node)

    def _cascading_cut(self, node):
        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def _consolidate(self):
        max_degree = int(math.log(self.n) * 2.1) + 1 if self.n > 0 else 1
        A = [None] * (max_degree + 1)

        # collect root nodes
        roots = []
        if self.min_node is not None:
            node = self.min_node
            while True:
                roots.append(node)
                node = node.right
                if node is self.min_node:
                    break

        for w in roots:
            x = w
            d = x.degree
            while d < len(A) and A[d] is not None:
                y = A[d]
                self.comparisons += 1
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            if d >= len(A):
                A.extend([None] * (d - len(A) + 1))
            A[d] = x

        self.min_node = None
        for node in A:
            if node is not None:
                node.left = node
                node.right = node
                self.min_node = self._add_to_root_list(self.min_node, node)
                self.comparisons += 1
                if node.key < self.min_node.key:
                    self.min_node = node

    def _link(self, child, parent):
        self._remove_from_list(child)
        child.left = child
        child.right = child
        child.parent = parent
        if parent.child is None:
            parent.child = child
        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child
        parent.degree += 1
        child.mark = False


# ---------------------------------------------------------------------------
# Dijkstra's Algorithm
# ---------------------------------------------------------------------------

class DijkstraResult:
    """Container for SSSP results with operation counts."""
    __slots__ = ('dist', 'pred', 'comparisons', 'additions', 'decrease_keys')

    def __init__(self, dist, pred, comparisons, additions, decrease_keys):
        self.dist = dist
        self.pred = pred
        self.comparisons = comparisons
        self.additions = additions
        self.decrease_keys = decrease_keys


def dijkstra_fibonacci(adj, source, n=None):
    """Run Dijkstra's algorithm with Fibonacci heap.

    Parameters
    ----------
    adj : dict[int, list[tuple[int, float]]]
        Adjacency list. adj[u] = [(v, w), ...].
    source : int
        Source vertex.
    n : int, optional
        Number of vertices (inferred from adj keys if None).

    Returns
    -------
    DijkstraResult with dist, pred, and operation counters.
    """
    if n is None:
        n = max(adj.keys()) + 1 if adj else 0

    INF = float('inf')
    dist = [INF] * n
    pred = [-1] * n
    dist[source] = 0.0

    heap = FibonacciHeap()
    nodes = [None] * n
    additions = 0

    nodes[source] = heap.insert(0.0, source)
    for v in range(n):
        if v != source:
            nodes[v] = heap.insert(INF, v)

    while not heap.is_empty():
        u_node = heap.extract_min()
        u = u_node.value
        d_u = u_node.key

        if d_u == INF:
            break

        for v, w in adj.get(u, []):
            additions += 1
            new_dist = d_u + w
            heap.comparisons += 1
            if new_dist < dist[v]:
                dist[v] = new_dist
                pred[v] = u
                heap.decrease_key(nodes[v], new_dist)

    return DijkstraResult(
        dist=dist,
        pred=pred,
        comparisons=heap.comparisons,
        additions=additions,
        decrease_keys=heap.decrease_key_calls,
    )


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Small test graph
    adj = {
        0: [(1, 4.0), (2, 1.0)],
        1: [(3, 1.0)],
        2: [(1, 2.0), (3, 5.0)],
        3: [],
    }
    res = dijkstra_fibonacci(adj, 0, n=4)
    print(f"Distances: {res.dist}")
    print(f"Predecessors: {res.pred}")
    print(f"Comparisons: {res.comparisons}, Additions: {res.additions}, "
          f"Decrease-keys: {res.decrease_keys}")
    assert res.dist == [0.0, 3.0, 1.0, 4.0], f"Wrong distances: {res.dist}"
    print("Self-test PASSED")
