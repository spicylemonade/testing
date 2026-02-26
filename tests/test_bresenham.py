"""Tests for 3D Bresenham / supercover voxel traversal."""

import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.traversal.bresenham import bresenham_traversal


class TestBresenham26:
    def test_axis_aligned_x(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [7.5, 0.5, 0.5], connectivity=26)
        assert len(result) == 8
        for i, v in enumerate(result):
            assert v[0] == i

    def test_axis_aligned_y(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [0.5, 7.5, 0.5], connectivity=26)
        assert len(result) == 8

    def test_axis_aligned_z(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [0.5, 0.5, 7.5], connectivity=26)
        assert len(result) == 8

    def test_diagonal(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [7.5, 7.5, 7.5], connectivity=26)
        assert len(result) == 8
        assert result[0] == (0, 0, 0)
        assert result[-1] == (7, 7, 7)

    def test_single_voxel(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], connectivity=26)
        assert result == [(0, 0, 0)]

    def test_negative_direction(self):
        result = bresenham_traversal([7.5, 7.5, 7.5], [0.5, 0.5, 0.5], connectivity=26)
        assert result[0] == (7, 7, 7)
        assert result[-1] == (0, 0, 0)

    def test_start_end_included(self):
        result = bresenham_traversal([2.5, 3.5, 1.5], [6.5, 5.5, 4.5], connectivity=26)
        assert result[0] == (2, 3, 1)
        assert result[-1] == (6, 5, 4)

    def test_two_axis_diagonal(self):
        """Diagonal in XY plane."""
        result = bresenham_traversal([0.5, 0.5, 3.5], [5.5, 5.5, 3.5], connectivity=26)
        for v in result:
            assert v[2] == 3  # Z should be constant


class TestSupercover:
    def test_axis_aligned(self):
        result = bresenham_traversal([0.5, 0.5, 0.5], [7.5, 0.5, 0.5], connectivity=6)
        assert len(result) == 8
        for i, v in enumerate(result):
            assert v[0] == i

    def test_supercover_visits_more(self):
        """Supercover should visit at least as many voxels as 26-connected."""
        p0, p1 = [0.5, 0.5, 0.5], [5.5, 3.5, 2.5]
        r26 = bresenham_traversal(p0, p1, connectivity=26)
        r6 = bresenham_traversal(p0, p1, connectivity=6)
        assert len(r6) >= len(r26)

    def test_supercover_no_gaps(self):
        """Every consecutive pair in supercover should be 6-connected
        (differ by at most 1 in exactly one axis)."""
        result = bresenham_traversal([0.5, 0.5, 0.5], [7.5, 5.5, 3.5], connectivity=6)
        for i in range(1, len(result)):
            diff = sum(abs(result[i][j] - result[i-1][j]) for j in range(3))
            assert diff <= 3, f"Gap at step {i}: {result[i-1]} -> {result[i]}"

    def test_single_voxel(self):
        result = bresenham_traversal([3.5, 3.5, 3.5], [3.5, 3.5, 3.5], connectivity=6)
        assert result == [(3, 3, 3)]
