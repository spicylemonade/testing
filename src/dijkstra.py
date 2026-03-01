"""Dijkstra's algorithm with Fibonacci heap and binary heap variants.

Both implementations are instrumented with OpCounter for comparison-addition
model operation counting.
"""

import heapq
import math

from src.fibonacci_heap import FibonacciHeap
from src.op_counter import OpCounter


INF = float('inf')


def dijkstra_fibonacci(graph, source, counter=None):
    """Dijkstra's algorithm using a true Fibonacci heap.

    O(m + n log n) in the comparison-addition model.

    Args:
        graph: Graph object with .n, .neighbors(u) methods.
        source: Source vertex (integer).
        counter: OpCounter instance (created if None).

    Returns:
        (dist, counter): dist[v] = shortest distance from source to v,
                         counter = OpCounter with operation counts.
    """
    if counter is None:
        counter = OpCounter()

    n = graph.n
    dist = [INF] * n
    dist[source] = 0
    finalized = [False] * n
    nodes = [None] * n  # FibNode references for decrease_key

    heap = FibonacciHeap(counter=counter)
    nodes[source] = heap.insert(0, source)

    nodes_expanded = 0

    while not heap.is_empty():
        d_u, u = heap.extract_min()
        if finalized[u]:
            continue
        finalized[u] = True
        nodes_expanded += 1

        for v, w in graph.neighbors(u):
            new_dist = counter.add(d_u, w)
            if counter.less_than(new_dist, dist[v]):
                dist[v] = new_dist
                if nodes[v] is None:
                    nodes[v] = heap.insert(new_dist, v)
                else:
                    heap.decrease_key(nodes[v], new_dist)

    return dist, counter, nodes_expanded


def dijkstra_binary(graph, source, counter=None):
    """Dijkstra's algorithm using Python's heapq (binary heap).

    O((m + n) log n) in the comparison-addition model.

    Args:
        graph: Graph object with .n, .neighbors(u) methods.
        source: Source vertex (integer).
        counter: OpCounter instance (created if None).

    Returns:
        (dist, counter): dist[v] = shortest distance from source to v,
                         counter = OpCounter with operation counts.
    """
    if counter is None:
        counter = OpCounter()

    n = graph.n
    dist = [INF] * n
    dist[source] = 0
    finalized = [False] * n

    # (distance, vertex) pairs
    pq = [(0, source)]
    nodes_expanded = 0

    while pq:
        d_u, u = heapq.heappop(pq)
        counter.record_extract_min()

        if finalized[u]:
            continue
        finalized[u] = True
        nodes_expanded += 1

        # Check if this is a stale entry
        if counter.less_than(dist[u], d_u):
            continue

        for v, w in graph.neighbors(u):
            new_dist = counter.add(d_u, w)
            if counter.less_than(new_dist, dist[v]):
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
                counter.record_insert()

    return dist, counter, nodes_expanded
