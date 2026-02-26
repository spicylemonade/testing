"""Tests for Barnes-Hut tree-based force computation."""

import numpy as np
from src.bodies import Body, System
from src.forces.barnes_hut import (
    QuadTreeNode, build_tree, compute_forces_barnes_hut,
    _quadrant, _child_center,
)
from src.forces.brute_force_vec import compute_forces_vectorized


def make_two_body():
    bodies = [
        Body(mass=1.0, position=[0.0, 0.0], velocity=[0.0, 0.0]),
        Body(mass=1.0, position=[1.0, 0.0], velocity=[0.0, 0.0]),
    ]
    return System(bodies=bodies, G=1.0, epsilon=1e-10)


def test_quadrant_assignment():
    center = np.array([0.0, 0.0])
    assert _quadrant(np.array([-1.0, 1.0]), center) == 0  # NW
    assert _quadrant(np.array([1.0, 1.0]), center) == 1  # NE
    assert _quadrant(np.array([-1.0, -1.0]), center) == 2  # SW
    assert _quadrant(np.array([1.0, -1.0]), center) == 3  # SE


def test_child_center():
    center = np.array([0.0, 0.0])
    size = 2.0
    c0 = _child_center(center, size, 0)  # NW
    assert c0[0] < 0 and c0[1] > 0
    c3 = _child_center(center, size, 3)  # SE
    assert c3[0] > 0 and c3[1] < 0


def test_build_tree_two_body():
    sys = make_two_body()
    tree = build_tree(sys)
    assert tree.total_mass == 2.0
    np.testing.assert_allclose(tree.com, [0.5, 0.0], atol=1e-10)


def test_build_tree_preserves_mass():
    np.random.seed(42)
    bodies = [Body(mass=1.0, position=np.random.randn(2), velocity=[0, 0]) for _ in range(50)]
    sys = System(bodies=bodies)
    tree = build_tree(sys)
    assert abs(tree.total_mass - 50.0) < 1e-10


def test_barnes_hut_two_body_matches_exact():
    sys = make_two_body()
    acc_exact = compute_forces_vectorized(sys)
    # theta=0 means no approximation — always recurse to leaves
    acc_bh = compute_forces_barnes_hut(sys, theta=0.0)
    np.testing.assert_allclose(acc_bh, acc_exact, atol=1e-8)


def test_barnes_hut_accuracy_n100():
    """Barnes-Hut with theta=0.5 should be within 1% RMS of exact for N=100."""
    np.random.seed(42)
    bodies = [Body(mass=1.0, position=np.random.randn(2) * 5, velocity=[0, 0]) for _ in range(100)]
    sys = System(bodies=bodies, epsilon=0.01)

    acc_exact = compute_forces_vectorized(sys)
    acc_bh = compute_forces_barnes_hut(sys, theta=0.5)

    norms = np.linalg.norm(acc_exact, axis=1)
    mask = norms > 1e-12
    rel_err = np.linalg.norm(acc_bh[mask] - acc_exact[mask], axis=1) / norms[mask]
    rms_err = np.sqrt(np.mean(rel_err ** 2))
    assert rms_err < 0.01, f"RMS error {rms_err:.4f} >= 1%"


def test_node_is_empty():
    node = QuadTreeNode(np.array([0.0, 0.0]), 1.0)
    assert node.is_empty()
    assert node.is_leaf()
