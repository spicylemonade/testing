"""Collatz predecessor graph construction and graph Laplacian computation."""

import networkx as nx
import numpy as np
from scipy import sparse


def build_predecessor_graph(max_n):
    """Build directed graph where edge (a, b) means b = T(a) (b is successor of a)."""
    G = nx.DiGraph()
    for n in range(1, max_n + 1):
        G.add_node(n)
    for n in range(2, max_n + 1):
        if n % 2 == 0:
            succ = n // 2
        else:
            succ = 3 * n + 1
        if succ <= max_n:
            G.add_edge(n, succ)
        # Even if succ > max_n, node n still exists
    return G


def build_collatz_tree(root, depth):
    """Build the inverse Collatz tree from root upward to given depth.

    At each node m, predecessors are:
      - 2*m (always a predecessor, since T(2m) = m)
      - (m-1)/3 if (m-1) % 3 == 0 and (m-1)//3 is odd and (m-1)//3 > 0
    """
    G = nx.DiGraph()
    G.add_node(root)
    frontier = {root}
    for _ in range(depth):
        next_frontier = set()
        for m in frontier:
            # Predecessor 1: 2*m
            p1 = 2 * m
            G.add_edge(p1, m)
            next_frontier.add(p1)
            # Predecessor 2: (m-1)/3 if valid
            if (m - 1) % 3 == 0:
                p2 = (m - 1) // 3
                if p2 > 0 and p2 % 2 == 1:
                    G.add_edge(p2, m)
                    next_frontier.add(p2)
        frontier = next_frontier
    return G


def graph_laplacian(G):
    """Return the normalized graph Laplacian as a sparse matrix.

    L_norm = I - D^{-1/2} A D^{-1/2} for the undirected version.
    """
    # Convert to undirected for Laplacian
    U = G.to_undirected()
    A = nx.adjacency_matrix(U, dtype=float)
    n = A.shape[0]
    degrees = np.array(A.sum(axis=1)).flatten()
    # Avoid division by zero
    degrees[degrees == 0] = 1.0
    D_inv_sqrt = sparse.diags(1.0 / np.sqrt(degrees))
    L_norm = sparse.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt
    return L_norm


if __name__ == "__main__":
    # Test predecessor graph
    G = build_predecessor_graph(100)
    assert G.number_of_nodes() == 100  # nodes 1..100
    print(f"Predecessor graph (max_n=100): {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Test inverse tree
    # Depth 20 gives ~342 nodes; depth 25 gives ~1095 nodes
    tree = build_collatz_tree(1, 25)
    n_nodes = tree.number_of_nodes()
    print(f"Inverse tree (root=1, depth=25): {n_nodes} nodes")
    assert n_nodes >= 1000, f"Tree has only {n_nodes} nodes, expected >= 1000"

    # Test Laplacian
    G_small = build_predecessor_graph(50)
    L = graph_laplacian(G_small)
    print(f"Laplacian shape: {L.shape}")
    assert L.shape[0] == 50

    print("All tests passed!")
