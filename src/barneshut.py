"""
Barnes-Hut Quadtree for O(N log N) Gravitational Force Computation
===================================================================

Implements the Barnes & Hut (1986) hierarchical force-calculation algorithm
for 2D gravitational simulations using a quadtree spatial decomposition.

Reference:
    Barnes, J. & Hut, P. (1986). A hierarchical O(N log N) force-calculation
    algorithm. Nature, 324, 446-449.

Usage:
    from barneshut import compute_forces_barneshut
    acc = compute_forces_barneshut(positions, masses, G=1.0, softening=0.01, theta=0.5)
"""

import numpy as np


class QuadTreeNode:
    """
    A node in the Barnes-Hut quadtree.

    Each node represents a square region of 2D space and contains either:
    - A single body (leaf node)
    - No body (empty node)
    - Multiple bodies (internal node with 4 children: NW, NE, SW, SE)

    Internal nodes store the total mass and center of mass of all contained bodies.
    """
    __slots__ = [
        "center_x", "center_y", "half_size",  # region geometry
        "total_mass", "com_x", "com_y",  # center of mass
        "body_index",  # index of body if leaf, -1 otherwise
        "children",  # [NW, NE, SW, SE] or None if leaf/empty
        "is_leaf", "n_bodies",
    ]

    def __init__(self, center_x, center_y, half_size):
        self.center_x = center_x
        self.center_y = center_y
        self.half_size = half_size
        self.total_mass = 0.0
        self.com_x = 0.0
        self.com_y = 0.0
        self.body_index = -1
        self.children = None
        self.is_leaf = True
        self.n_bodies = 0


def _get_quadrant(node, x, y):
    """Return quadrant index (0=NW, 1=NE, 2=SW, 3=SE) for position (x,y)."""
    if x < node.center_x:
        return 0 if y >= node.center_y else 2  # W
    else:
        return 1 if y >= node.center_y else 3  # E


def _create_child(node, quadrant):
    """Create a child node for the given quadrant."""
    hs = node.half_size / 2.0
    if quadrant == 0:  # NW
        return QuadTreeNode(node.center_x - hs, node.center_y + hs, hs)
    elif quadrant == 1:  # NE
        return QuadTreeNode(node.center_x + hs, node.center_y + hs, hs)
    elif quadrant == 2:  # SW
        return QuadTreeNode(node.center_x - hs, node.center_y - hs, hs)
    else:  # SE
        return QuadTreeNode(node.center_x + hs, node.center_y - hs, hs)


def insert(node, index, positions, masses, depth=0, max_depth=50):
    """
    Insert body 'index' into the quadtree rooted at 'node'.

    Parameters
    ----------
    node : QuadTreeNode
    index : int, body index
    positions : ndarray (N, 2)
    masses : ndarray (N,)
    depth : current recursion depth
    max_depth : maximum tree depth (prevent infinite recursion for coincident bodies)
    """
    if depth > max_depth:
        # Safety: stop subdividing for coincident bodies
        # Just accumulate mass at this node
        m = masses[index]
        old_mass = node.total_mass
        node.total_mass += m
        if node.total_mass > 0:
            node.com_x = (node.com_x * old_mass + positions[index, 0] * m) / node.total_mass
            node.com_y = (node.com_y * old_mass + positions[index, 1] * m) / node.total_mass
        node.n_bodies += 1
        return

    x, y = positions[index, 0], positions[index, 1]
    m = masses[index]

    if node.n_bodies == 0:
        # Empty node: store body directly
        node.body_index = index
        node.total_mass = m
        node.com_x = x
        node.com_y = y
        node.n_bodies = 1
        node.is_leaf = True
        return

    if node.is_leaf:
        # Leaf with one body: need to subdivide
        node.children = [None, None, None, None]
        node.is_leaf = False

        # Re-insert existing body
        old_idx = node.body_index
        node.body_index = -1
        old_q = _get_quadrant(node, positions[old_idx, 0], positions[old_idx, 1])
        if node.children[old_q] is None:
            node.children[old_q] = _create_child(node, old_q)
        insert(node.children[old_q], old_idx, positions, masses, depth + 1, max_depth)

    # Insert new body into appropriate quadrant
    q = _get_quadrant(node, x, y)
    if node.children[q] is None:
        node.children[q] = _create_child(node, q)
    insert(node.children[q], index, positions, masses, depth + 1, max_depth)

    # Update center of mass
    old_mass = node.total_mass
    node.total_mass += m
    node.com_x = (node.com_x * old_mass + x * m) / node.total_mass
    node.com_y = (node.com_y * old_mass + y * m) / node.total_mass
    node.n_bodies += 1


def build_tree(positions, masses):
    """
    Build a Barnes-Hut quadtree from body positions and masses.

    Returns the root QuadTreeNode.
    """
    N = len(masses)
    if N == 0:
        return QuadTreeNode(0, 0, 1)

    # Determine bounding box
    x_min, x_max = positions[:, 0].min(), positions[:, 0].max()
    y_min, y_max = positions[:, 1].min(), positions[:, 1].max()

    # Square bounding box centered on data
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    half_size = max(x_max - x_min, y_max - y_min) / 2.0 * 1.01 + 0.01  # small margin

    root = QuadTreeNode(cx, cy, half_size)

    for i in range(N):
        insert(root, i, positions, masses)

    return root


def compute_force_on_body(node, index, positions, masses, G, softening, theta):
    """
    Compute gravitational acceleration on body 'index' by traversing the tree.

    Parameters
    ----------
    node : QuadTreeNode
    index : int, body index
    positions : ndarray (N, 2)
    masses : ndarray (N,)
    G : float
    softening : float
    theta : float, opening angle criterion

    Returns
    -------
    ax, ay : float, acceleration components
    """
    if node.n_bodies == 0:
        return 0.0, 0.0

    dx = node.com_x - positions[index, 0]
    dy = node.com_y - positions[index, 1]
    dist_sq = dx * dx + dy * dy + softening * softening
    dist = np.sqrt(dist_sq)

    if node.is_leaf:
        if node.body_index == index:
            return 0.0, 0.0  # skip self
        # Direct force from single body
        force_mag = G * node.total_mass / dist_sq
        return force_mag * dx / dist, force_mag * dy / dist

    # Opening criterion: cell_size / distance < theta
    cell_size = 2.0 * node.half_size
    if cell_size / dist < theta:
        # Use center of mass approximation
        force_mag = G * node.total_mass / dist_sq
        return force_mag * dx / dist, force_mag * dy / dist

    # Recurse into children
    ax, ay = 0.0, 0.0
    for child in node.children:
        if child is not None:
            cax, cay = compute_force_on_body(
                child, index, positions, masses, G, softening, theta)
            ax += cax
            ay += cay
    return ax, ay


def compute_forces_barneshut(positions, masses, G=1.0, softening=0.01, theta=0.5):
    """
    Compute gravitational accelerations using Barnes-Hut algorithm.

    Parameters
    ----------
    positions : ndarray, shape (N, 2)
    masses : ndarray, shape (N,)
    G : float
    softening : float
    theta : float, opening angle (0 = exact, larger = faster but less accurate)

    Returns
    -------
    accelerations : ndarray, shape (N, 2)
    """
    N = len(masses)
    if N <= 1:
        return np.zeros_like(positions)

    root = build_tree(positions, masses)
    accelerations = np.zeros((N, 2))

    for i in range(N):
        ax, ay = compute_force_on_body(
            root, i, positions, masses, G, softening, theta)
        accelerations[i, 0] = ax
        accelerations[i, 1] = ay

    return accelerations


def _flatten_tree(node, cell_data, idx_counter):
    """Flatten tree into arrays for vectorized force computation."""
    my_idx = idx_counter[0]
    idx_counter[0] += 1

    cell_data["com_x"][my_idx] = node.com_x
    cell_data["com_y"][my_idx] = node.com_y
    cell_data["total_mass"][my_idx] = node.total_mass
    cell_data["half_size"][my_idx] = node.half_size
    cell_data["body_index"][my_idx] = node.body_index
    cell_data["n_bodies"][my_idx] = node.n_bodies
    cell_data["is_leaf"][my_idx] = node.is_leaf

    child_indices = [-1, -1, -1, -1]
    if not node.is_leaf and node.children is not None:
        for q in range(4):
            if node.children[q] is not None and node.children[q].n_bodies > 0:
                child_indices[q] = idx_counter[0]
                _flatten_tree(node.children[q], cell_data, idx_counter)

    cell_data["children"][my_idx] = child_indices
    return my_idx


def _count_nodes(node):
    """Count total nodes in tree."""
    if node is None or node.n_bodies == 0:
        return 0
    count = 1
    if not node.is_leaf and node.children:
        for c in node.children:
            if c is not None:
                count += _count_nodes(c)
    return count


def compute_forces_barneshut_fast(positions, masses, G=1.0, softening=0.01, theta=0.5):
    """
    Faster Barnes-Hut using flattened tree arrays and stack-based traversal.

    Avoids Python recursion overhead per force computation.
    """
    N = len(masses)
    if N <= 1:
        return np.zeros_like(positions)

    root = build_tree(positions, masses)

    # Flatten tree into arrays
    n_nodes = _count_nodes(root)
    cell_data = {
        "com_x": np.zeros(n_nodes),
        "com_y": np.zeros(n_nodes),
        "total_mass": np.zeros(n_nodes),
        "half_size": np.zeros(n_nodes),
        "body_index": np.full(n_nodes, -1, dtype=np.int32),
        "n_bodies": np.zeros(n_nodes, dtype=np.int32),
        "is_leaf": np.zeros(n_nodes, dtype=bool),
        "children": np.full((n_nodes, 4), -1, dtype=np.int32),
    }
    _flatten_tree(root, cell_data, [0])

    com_x = cell_data["com_x"]
    com_y = cell_data["com_y"]
    total_mass = cell_data["total_mass"]
    half_size = cell_data["half_size"]
    body_index = cell_data["body_index"]
    n_bodies = cell_data["n_bodies"]
    is_leaf = cell_data["is_leaf"]
    children = cell_data["children"]

    accelerations = np.zeros((N, 2))
    soft_sq = softening * softening
    theta_sq = theta * theta  # avoid sqrt in criterion

    for i in range(N):
        px, py = positions[i, 0], positions[i, 1]
        ax, ay = 0.0, 0.0

        # Stack-based tree traversal
        stack = [0]  # start from root
        while stack:
            node_idx = stack.pop()

            if n_bodies[node_idx] == 0:
                continue

            dx = com_x[node_idx] - px
            dy = com_y[node_idx] - py
            dist_sq = dx * dx + dy * dy + soft_sq

            if is_leaf[node_idx]:
                if body_index[node_idx] == i:
                    continue
                inv_dist = 1.0 / np.sqrt(dist_sq)
                force_mag = G * total_mass[node_idx] / dist_sq
                ax += force_mag * dx * inv_dist
                ay += force_mag * dy * inv_dist
                continue

            # Opening criterion: (2*half_size)^2 / dist_sq < theta^2
            cell_size_sq = (2.0 * half_size[node_idx]) ** 2
            if cell_size_sq < theta_sq * dist_sq:
                inv_dist = 1.0 / np.sqrt(dist_sq)
                force_mag = G * total_mass[node_idx] / dist_sq
                ax += force_mag * dx * inv_dist
                ay += force_mag * dy * inv_dist
            else:
                for q in range(4):
                    c = children[node_idx, q]
                    if c >= 0:
                        stack.append(c)

        accelerations[i, 0] = ax
        accelerations[i, 1] = ay

    return accelerations


def make_barneshut_force_func(theta=0.5):
    """
    Create a force function compatible with the gravity_sim integrators.

    Usage:
        force_func = make_barneshut_force_func(theta=0.5)
        results = run_simulation(..., force_func=force_func)
    """
    def force_func(positions, masses, G=1.0, softening=0.01):
        return compute_forces_barneshut(positions, masses, G, softening, theta)
    return force_func


# ---------------------------------------------------------------------------
# Standalone validation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import time
    import sys
    sys.path.insert(0, "src")
    from gravity_sim import compute_forces_vectorized, random_initial_conditions

    N = 200
    pos, _, mass = random_initial_conditions(N, seed=42)

    # Direct summation
    t0 = time.perf_counter()
    acc_direct = compute_forces_vectorized(pos, mass, G=1.0, softening=0.1)
    t_direct = time.perf_counter() - t0

    # Barnes-Hut
    for theta in [0.0, 0.3, 0.5, 0.7, 1.0]:
        t0 = time.perf_counter()
        acc_bh = compute_forces_barneshut(pos, mass, G=1.0, softening=0.1, theta=theta)
        t_bh = time.perf_counter() - t0

        # Relative error per body
        errors = np.sqrt(np.sum((acc_bh - acc_direct) ** 2, axis=1))
        magnitudes = np.sqrt(np.sum(acc_direct ** 2, axis=1)) + 1e-30
        rel_errors = errors / magnitudes

        pct_under_5 = np.mean(rel_errors < 0.05) * 100
        print(f"theta={theta:.1f}: time={t_bh*1000:.1f}ms (direct={t_direct*1000:.1f}ms), "
              f"mean_err={np.mean(rel_errors)*100:.2f}%, "
              f"bodies<5%err: {pct_under_5:.0f}%")
