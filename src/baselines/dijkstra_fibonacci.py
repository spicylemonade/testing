"""Dijkstra's SSSP algorithm using a Fibonacci heap."""


class _FibNode:
    __slots__ = ("key", "val", "deg", "mark", "p", "child", "left", "right")
    def __init__(self, key, val):
        self.key, self.val, self.deg, self.mark = key, val, 0, False
        self.p = self.child = None
        self.left = self.right = self


class FibonacciHeap:
    """Fibonacci heap: O(1) amortized insert/decrease_key, O(log n) extract_min."""
    def __init__(self):
        self.min_node = None
        self.n = 0
        self.stats = {"comparisons": 0, "heap_ops": 0}

    @staticmethod
    def _merge(a, b):
        if a is None: return b
        if b is None: return a
        a.right.left, b.left.right = b.left, a.right
        a.right, b.left = b, a
        return a

    def _detach(self, nd):
        nd.left.right, nd.right.left = nd.right, nd.left
        nd.left = nd.right = nd

    def insert(self, key, val):
        self.stats["heap_ops"] += 1
        nd = _FibNode(key, val)
        if self.min_node is None:
            self.min_node = nd
        else:
            self.min_node = self._merge(self.min_node, nd)
            self.stats["comparisons"] += 1
            if nd.key < self.min_node.key: self.min_node = nd
        self.n += 1
        return nd

    def extract_min(self):
        self.stats["heap_ops"] += 1
        z = self.min_node
        if z is None: return None
        if z.child:
            c = z.child
            while True:
                nxt = c.right; c.p = None; c = nxt
                if c is z.child: break
            self.min_node = self._merge(self.min_node, z.child)
        if z.right is z:
            self.min_node = None
        else:
            self.min_node = z.right; self._detach(z); self._consolidate()
        self.n -= 1
        return (z.key, z.val)

    def _consolidate(self):
        tbl = [None] * (int(self.n ** 0.5) + 3)
        roots, cur = [], self.min_node
        while True:
            roots.append(cur); cur = cur.right
            if cur is self.min_node: break
        for w in roots:
            x = w; x.left = x; x.right = x; d = x.deg
            while d < len(tbl) and tbl[d] is not None:
                y = tbl[d]; self.stats["comparisons"] += 1
                if x.key > y.key: x, y = y, x
                y.p, y.mark = x, False
                if x.child is None:
                    x.child = y; y.left = y; y.right = y
                else:
                    x.child = self._merge(x.child, y)
                x.deg += 1; tbl[d] = None; d += 1
            if d >= len(tbl): tbl.extend([None] * (d - len(tbl) + 1))
            tbl[d] = x
        self.min_node = None
        for nd in tbl:
            if nd is None: continue
            nd.left = nd; nd.right = nd
            if self.min_node is None:
                self.min_node = nd
            else:
                self.min_node = self._merge(self.min_node, nd)
                self.stats["comparisons"] += 1
                if nd.key < self.min_node.key: self.min_node = nd

    def decrease_key(self, nd, new_key):
        self.stats["heap_ops"] += 1; self.stats["comparisons"] += 1
        if new_key > nd.key: return
        nd.key = new_key; p = nd.p
        if p is not None:
            self.stats["comparisons"] += 1
            if nd.key < p.key: self._cut(nd, p); self._casc(p)
        self.stats["comparisons"] += 1
        if nd.key < self.min_node.key: self.min_node = nd

    def _cut(self, c, p):
        if c.right is c: p.child = None
        else:
            if p.child is c: p.child = c.right
            self._detach(c)
        p.deg -= 1; c.p, c.mark = None, False
        self.min_node = self._merge(self.min_node, c)

    def _casc(self, nd):
        p = nd.p
        if p is not None:
            if not nd.mark: nd.mark = True
            else: self._cut(nd, p); self._casc(p)


def sssp(adj, source, n):
    """Run Dijkstra with a Fibonacci heap.

    Args:
        adj: dict vertex -> [(neighbor, weight)].
        source: source vertex.  n: number of vertices.
    Returns:
        (distances dict, stats dict with comparisons/additions/heap_ops).
    """
    INF = float("inf")
    dist = {v: INF for v in adj}; dist[source] = 0
    stats = {"comparisons": 0, "additions": 0, "heap_ops": 0}
    heap = FibonacciHeap()
    nodes = {v: heap.insert(dist[v], v) for v in adj}
    while heap.n > 0:
        res = heap.extract_min()
        if res is None: break
        d_u, u = res
        if d_u == INF: break
        for v, w in adj.get(u, []):
            stats["comparisons"] += 1; stats["additions"] += 1
            nd = d_u + w
            if nd < dist[v]:
                dist[v] = nd; heap.decrease_key(nodes[v], nd)
    stats["comparisons"] += heap.stats["comparisons"]
    stats["heap_ops"] += heap.stats["heap_ops"]
    return dist, stats
