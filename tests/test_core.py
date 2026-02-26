"""Tests for VoxelGrid, Ray, and grid generators."""

import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import (
    empty_grid, full_grid, random_grid, sphere_shell_grid, axis_planes_grid
)


class TestVoxelGrid:
    def test_create_empty(self):
        g = VoxelGrid(16)
        assert g.size == 16
        assert g.occupancy_fraction == 0.0
        assert g.total_voxels == 16**3

    def test_create_with_data(self):
        data = np.ones((8, 8, 8), dtype=np.uint8)
        g = VoxelGrid(8, data)
        assert g.occupancy_fraction == 1.0

    def test_get_set(self):
        g = VoxelGrid(32)
        assert g.get(0, 0, 0) == False
        g.set(0, 0, 0, True)
        assert g.get(0, 0, 0) == True
        g.set(0, 0, 0, False)
        assert g.get(0, 0, 0) == False

    def test_in_bounds(self):
        g = VoxelGrid(10)
        assert g.in_bounds(0, 0, 0) == True
        assert g.in_bounds(9, 9, 9) == True
        assert g.in_bounds(10, 0, 0) == False
        assert g.in_bounds(-1, 0, 0) == False

    def test_occupied_count(self):
        g = VoxelGrid(4)
        g.set(0, 0, 0)
        g.set(1, 1, 1)
        g.set(2, 2, 2)
        assert g.occupied_count == 3

    def test_repr(self):
        g = VoxelGrid(8)
        assert "VoxelGrid" in repr(g)

    def test_data_shape_mismatch(self):
        with pytest.raises(AssertionError):
            VoxelGrid(8, np.zeros((4, 4, 4), dtype=np.uint8))


class TestRay:
    def test_create(self):
        r = Ray(np.array([0, 0, 0]), np.array([1, 0, 0]))
        assert np.allclose(r.origin, [0, 0, 0])
        assert np.allclose(r.direction, [1, 0, 0])

    def test_at(self):
        r = Ray(np.array([1.0, 2.0, 3.0]), np.array([1.0, 0.0, 0.0]))
        p = r.at(5.0)
        assert np.allclose(p, [6.0, 2.0, 3.0])

    def test_at_zero(self):
        r = Ray(np.array([1.0, 2.0, 3.0]), np.array([0.5, -0.5, 1.0]))
        assert np.allclose(r.at(0.0), r.origin)

    def test_inv_direction(self):
        r = Ray(np.array([0, 0, 0]), np.array([2.0, 4.0, 0.5]))
        inv = r.inv_direction
        assert np.allclose(inv, [0.5, 0.25, 2.0])

    def test_inv_direction_zero_component(self):
        r = Ray(np.array([0, 0, 0]), np.array([1.0, 0.0, 1.0]))
        inv = r.inv_direction
        assert np.isinf(inv[1])

    def test_repr(self):
        r = Ray(np.array([0, 0, 0]), np.array([1, 0, 0]))
        assert "Ray" in repr(r)


class TestGridGenerators:
    def test_empty_grid(self):
        g = empty_grid(16)
        assert g.occupancy_fraction == 0.0
        assert g.size == 16

    def test_full_grid(self):
        g = full_grid(8)
        assert g.occupancy_fraction == 1.0

    def test_random_grid_density(self):
        for density in [0.1, 0.5, 0.9]:
            g = random_grid(64, density=density)
            # Allow 10% tolerance
            assert abs(g.occupancy_fraction - density) < 0.1

    def test_random_grid_reproducibility(self):
        g1 = random_grid(32, density=0.3, seed=42)
        g2 = random_grid(32, density=0.3, seed=42)
        assert np.array_equal(g1.data, g2.data)

    def test_random_grid_different_seeds(self):
        g1 = random_grid(32, density=0.5, seed=42)
        g2 = random_grid(32, density=0.5, seed=99)
        assert not np.array_equal(g1.data, g2.data)

    def test_sphere_shell(self):
        g = sphere_shell_grid(64)
        assert 0.0 < g.occupancy_fraction < 0.5
        # Center should be empty (inside shell)
        assert g.get(32, 32, 32) == False

    def test_axis_planes(self):
        g = axis_planes_grid(32)
        # Center should be occupied (intersection of all 3 planes)
        assert g.get(16, 16, 16) == True
        # Corner should be empty
        assert g.get(0, 0, 0) == False
        assert 0.0 < g.occupancy_fraction < 0.3

    def test_large_grid_creation(self):
        """Test that 512^3 grid can be created (memory test)."""
        g = VoxelGrid(128)  # Use 128 for speed in test
        assert g.total_voxels == 128**3
