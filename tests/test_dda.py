"""Tests for Amanatides-Woo DDA traversal."""

import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.traversal.dda import dda_traversal


def make_grid(size=8):
    return VoxelGrid(size)


class TestDDABasic:
    def test_axis_aligned_x(self):
        """Ray along +X axis through center."""
        grid = make_grid(8)
        ray = Ray(np.array([-1.0, 4.5, 4.5]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 8
        for i, (voxel, t_enter, t_exit) in enumerate(result):
            assert voxel[0] == i
            assert voxel[1] == 4
            assert voxel[2] == 4

    def test_axis_aligned_y(self):
        """Ray along +Y axis."""
        grid = make_grid(8)
        ray = Ray(np.array([3.5, -1.0, 3.5]), np.array([0.0, 1.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 8
        for i, (voxel, t_enter, t_exit) in enumerate(result):
            assert voxel[1] == i

    def test_axis_aligned_z(self):
        """Ray along +Z axis."""
        grid = make_grid(8)
        ray = Ray(np.array([3.5, 3.5, -1.0]), np.array([0.0, 0.0, 1.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 8
        for i, (voxel, t_enter, t_exit) in enumerate(result):
            assert voxel[2] == i

    def test_negative_direction_x(self):
        """Ray along -X axis."""
        grid = make_grid(8)
        ray = Ray(np.array([9.0, 4.5, 4.5]), np.array([-1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 8
        for i, (voxel, t_enter, t_exit) in enumerate(result):
            assert voxel[0] == 7 - i

    def test_diagonal_ray(self):
        """Ray along main diagonal."""
        grid = make_grid(8)
        ray = Ray(np.array([-1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0]))
        result = dda_traversal(grid, ray)
        # Should traverse approximately 3*8 - 2 = 22 voxels (diagonal path)
        assert len(result) > 8
        # First voxel should be (0,0,0)
        assert result[0][0] == (0, 0, 0)
        # Last voxel should be (7,7,7)
        assert result[-1][0] == (7, 7, 7)

    def test_ray_misses_grid(self):
        """Ray that completely misses the grid."""
        grid = make_grid(8)
        ray = Ray(np.array([10.0, 10.0, 10.0]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 0

    def test_ray_starts_inside(self):
        """Ray originating inside the grid."""
        grid = make_grid(8)
        ray = Ray(np.array([4.5, 4.5, 4.5]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) > 0
        assert result[0][0] == (4, 4, 4)

    def test_t_values_monotonic(self):
        """t_enter and t_exit should be monotonically increasing."""
        grid = make_grid(16)
        ray = Ray(np.array([-1.0, 5.3, 7.2]), np.array([1.0, 0.3, -0.2]))
        result = dda_traversal(grid, ray)
        for i in range(len(result)):
            _, t_enter, t_exit = result[i]
            assert t_exit >= t_enter, f"t_exit < t_enter at {i}"
        for i in range(1, len(result)):
            assert result[i][1] >= result[i-1][1] - 1e-10, f"Non-monotonic at {i}"


class TestDDAEdgeCases:
    def test_corner_grazing_ray(self):
        """Ray that grazes a grid corner."""
        grid = make_grid(8)
        # Ray passing very close to (4,4,4) corner
        ray = Ray(np.array([-1.0, 4.0001, 4.0001]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) == 8

    def test_face_aligned_entry(self):
        """Ray entering exactly through a grid face."""
        grid = make_grid(8)
        ray = Ray(np.array([-1.0, 4.0, 4.0]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) >= 8

    def test_two_axis_diagonal(self):
        """Ray diagonal in XY plane, constant Z."""
        grid = make_grid(8)
        ray = Ray(np.array([-1.0, -1.0, 4.5]), np.array([1.0, 1.0, 0.0]))
        result = dda_traversal(grid, ray)
        # Check all returned voxels are valid
        for voxel, _, _ in result:
            assert 0 <= voxel[0] < 8
            assert 0 <= voxel[1] < 8
            assert voxel[2] == 4

    def test_very_short_ray(self):
        """Ray that barely enters the grid."""
        grid = make_grid(8)
        ray = Ray(np.array([-0.001, 4.5, 4.5]), np.array([1.0, 0.0, 0.0]))
        result = dda_traversal(grid, ray)
        assert len(result) > 0
        assert result[0][0][0] == 0

    def test_all_octants(self):
        """Test rays in all 8 direction octants."""
        grid = make_grid(8)
        center = np.array([4.0, 4.0, 4.0])
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                for sz in [-1, 1]:
                    direction = np.array([sx, sy, sz], dtype=float)
                    origin = center - 5 * direction
                    ray = Ray(origin, direction)
                    result = dda_traversal(grid, ray)
                    assert len(result) > 0, f"No voxels for direction {direction}"


class TestDDACorrectness:
    def test_voxels_actually_intersected(self):
        """Verify each reported voxel actually contains a point on the ray."""
        grid = make_grid(16)
        ray = Ray(np.array([-1.0, 3.7, 8.2]), np.array([1.0, 0.5, -0.3]))
        result = dda_traversal(grid, ray)
        tol = 0.5  # tolerance for boundary cases
        for voxel, t_enter, t_exit in result:
            t_mid = (t_enter + t_exit) / 2.0
            point = ray.at(t_mid)
            for i in range(3):
                assert voxel[i] - tol <= point[i] <= voxel[i] + 1.0 + tol, \
                    f"Point {point} not near voxel {voxel}"

    def test_no_duplicate_voxels(self):
        """No voxel should appear twice."""
        grid = make_grid(16)
        ray = Ray(np.array([-2.0, 7.5, 3.1]), np.array([1.0, -0.2, 0.8]))
        result = dda_traversal(grid, ray)
        voxels = [v for v, _, _ in result]
        assert len(voxels) == len(set(voxels))
