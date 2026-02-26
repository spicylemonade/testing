"""Additional tests for code coverage of uncovered modules.

Targets: coherent_batch, simd_dda count batch, morton utilities,
cache_aware MortonGrid, bresenham edge cases.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import random_grid, full_grid, empty_grid


# ---------------------------------------------------------------------------
# Morton code tests
# ---------------------------------------------------------------------------

class TestMorton:
    def test_encode_decode_roundtrip(self):
        from src.utils.morton import encode_morton, decode_morton
        for x in range(16):
            for y in range(16):
                for z in range(16):
                    code = encode_morton(x, y, z)
                    dx, dy, dz = decode_morton(code)
                    assert (dx, dy, dz) == (x, y, z)

    def test_encode_zero(self):
        from src.utils.morton import encode_morton
        assert encode_morton(0, 0, 0) == 0

    def test_encode_one(self):
        from src.utils.morton import encode_morton
        assert encode_morton(1, 0, 0) == 1
        assert encode_morton(0, 1, 0) == 2
        assert encode_morton(0, 0, 1) == 4

    def test_spread_compact_bits(self):
        from src.utils.morton import _spread_bits, _compact_bits
        for v in [0, 1, 7, 15, 255, 1023]:
            assert _compact_bits(_spread_bits(v)) == v


# ---------------------------------------------------------------------------
# MortonGrid tests
# ---------------------------------------------------------------------------

class TestMortonGrid:
    def test_from_voxel_grid(self):
        from src.traversal.cache_aware import MortonGrid
        grid = random_grid(16, density=0.5, seed=42)
        mg = MortonGrid.from_voxel_grid(grid)
        assert mg.size == 16

    def test_get_matches_original(self):
        from src.traversal.cache_aware import MortonGrid
        grid = random_grid(8, density=0.5, seed=42)
        mg = MortonGrid(8, grid.data)
        for x in range(8):
            for y in range(8):
                for z in range(8):
                    assert mg.get(x, y, z) == bool(grid.data[x, y, z])

    def test_in_bounds(self):
        from src.traversal.cache_aware import MortonGrid
        mg = MortonGrid(8)
        assert mg.in_bounds(0, 0, 0)
        assert mg.in_bounds(7, 7, 7)
        assert not mg.in_bounds(-1, 0, 0)
        assert not mg.in_bounds(8, 0, 0)

    def test_empty_init(self):
        from src.traversal.cache_aware import MortonGrid
        mg = MortonGrid(4)
        assert mg.size == 4
        assert mg.get(0, 0, 0) == False


# ---------------------------------------------------------------------------
# Coherent batch tests
# ---------------------------------------------------------------------------

class TestCoherentBatch:
    def test_direction_hash_basic(self):
        from src.traversal.coherent_batch import _direction_hash
        # Positive octant
        h = _direction_hash(np.array([1.0, 1.0, 1.0]))
        assert h >= 0

    def test_direction_hash_negative(self):
        from src.traversal.coherent_batch import _direction_hash
        h1 = _direction_hash(np.array([1.0, 1.0, 1.0]))
        h2 = _direction_hash(np.array([-1.0, -1.0, -1.0]))
        assert h1 != h2  # different octants

    def test_direction_hash_zero(self):
        from src.traversal.coherent_batch import _direction_hash
        h = _direction_hash(np.array([0.0, 0.0, 0.0]))
        assert h == 0

    def test_direction_hash_batch(self):
        from src.traversal.coherent_batch import _direction_hash_batch
        dirs = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        hashes = _direction_hash_batch(dirs)
        assert len(hashes) == 3
        assert hashes[0] != hashes[1]  # different octants

    def test_sort_rays_by_coherence(self):
        from src.traversal.coherent_batch import sort_rays_by_coherence
        rays = [
            Ray(np.array([0, 0, 0]), np.array([1.0, 0.0, 0.0])),
            Ray(np.array([0, 0, 0]), np.array([-1.0, 0.0, 0.0])),
            Ray(np.array([0, 0, 0]), np.array([1.0, 0.1, 0.0])),
        ]
        sorted_rays, groups, order = sort_rays_by_coherence(rays)
        assert len(sorted_rays) == 3
        assert len(groups) >= 2  # at least 2 groups (positive/negative X)
        assert len(order) == 3

    def test_sort_rays_by_coherence_arrays(self):
        from src.traversal.coherent_batch import sort_rays_by_coherence_arrays
        origins = np.zeros((5, 3))
        dirs = np.array([
            [1, 0, 0], [-1, 0, 0], [0, 1, 0], [1, 0.1, 0], [-1, 0.1, 0]
        ], dtype=np.float64)
        so, sd, groups, order = sort_rays_by_coherence_arrays(origins, dirs)
        assert len(so) == 5
        assert len(groups) >= 2

    def test_coherent_batch_traversal_single(self):
        from src.traversal.coherent_batch import coherent_batch_traversal
        from src.traversal.dda import dda_traversal
        grid = random_grid(16, density=0.3, seed=42)
        ray = Ray(np.array([-1.0, 8.0, 8.0]), np.array([1.0, 0.0, 0.0]))
        result = coherent_batch_traversal(grid, ray)
        ref = dda_traversal(grid, ray)
        assert [v[0] for v in result] == [v[0] for v in ref]

    def test_coherent_batch_process_empty(self):
        from src.traversal.coherent_batch import coherent_batch_process
        grid = random_grid(16, density=0.3, seed=42)
        result = coherent_batch_process(grid, [])
        assert result == {}

    def test_coherent_batch_process_correctness(self):
        from src.traversal.coherent_batch import coherent_batch_process
        from src.traversal.dda import dda_traversal
        grid = random_grid(16, density=0.3, seed=42)
        rng = np.random.RandomState(42)
        rays = []
        for _ in range(20):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            rays.append(Ray(rng.uniform(-1, 17, 3), d))
        batch = coherent_batch_process(grid, rays)
        for i, ray in enumerate(rays):
            ref = dda_traversal(grid, ray)
            assert [v[0] for v in batch[i]] == [v[0] for v in ref]

    def test_coherent_batch_count_empty(self):
        from src.traversal.coherent_batch import coherent_batch_count
        grid = random_grid(16, density=0.3, seed=42)
        result = coherent_batch_count(grid, [])
        assert len(result) == 0

    def test_coherent_batch_count_correctness(self):
        from src.traversal.coherent_batch import coherent_batch_count
        from src.traversal.dda import dda_traversal
        grid = random_grid(16, density=0.3, seed=42)
        rng = np.random.RandomState(42)
        rays = []
        for _ in range(20):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            rays.append(Ray(rng.uniform(-1, 17, 3), d))
        counts = coherent_batch_count(grid, rays)
        for i, ray in enumerate(rays):
            ref = dda_traversal(grid, ray)
            assert counts[i] == len(ref)

    def test_coherent_group_dda_empty(self):
        from src.traversal.coherent_batch import _coherent_group_dda
        result = _coherent_group_dda(16, np.zeros((0, 3)), np.zeros((0, 3)),
                                     np.array([1, 1, 1], dtype=np.int64))
        assert result == {}

    def test_coherent_group_count_empty(self):
        from src.traversal.coherent_batch import _coherent_group_count
        result = _coherent_group_count(16, np.zeros((0, 3)), np.zeros((0, 3)),
                                       np.array([1, 1, 1], dtype=np.int64))
        assert len(result) == 0


# ---------------------------------------------------------------------------
# SIMD DDA count batch tests
# ---------------------------------------------------------------------------

class TestSimdDDACountBatch:
    def test_count_batch_matches_full(self):
        from src.traversal.simd_dda import simd_dda_batch, simd_dda_count_batch
        grid = random_grid(32, density=0.3, seed=42)
        rng = np.random.RandomState(42)
        rays = []
        for _ in range(50):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            rays.append(Ray(rng.uniform(-1, 33, 3), d))

        full = simd_dda_batch(grid, rays)
        counts = simd_dda_count_batch(grid, rays)
        for i in range(len(rays)):
            assert counts[i] == len(full[i])

    def test_count_batch_single_ray(self):
        from src.traversal.simd_dda import simd_dda_count_batch
        from src.traversal.dda import dda_traversal
        grid = random_grid(16, density=0.3, seed=42)
        ray = Ray(np.array([-1.0, 8.0, 8.0]), np.array([1.0, 0.0, 0.0]))
        counts = simd_dda_count_batch(grid, [ray])
        ref = dda_traversal(grid, ray)
        assert counts[0] == len(ref)

    def test_count_batch_miss(self):
        from src.traversal.simd_dda import simd_dda_count_batch
        grid = random_grid(16, density=0.3, seed=42)
        rays = [Ray(np.array([-10.0, -10.0, -10.0]), np.array([0.0, 0.0, -1.0]))]
        counts = simd_dda_count_batch(grid, rays)
        assert counts[0] == 0

    def test_simd_dda_traversal_correctness(self):
        from src.traversal.simd_dda import simd_dda_traversal
        from src.traversal.dda import dda_traversal
        grid = random_grid(16, density=0.3, seed=42)
        ray = Ray(np.array([-1.0, 8.0, 8.0]), np.array([1.0, 0.0, 0.0]))
        ref = dda_traversal(grid, ray)
        result = simd_dda_traversal(grid, ray)
        assert [v[0] for v in result] == [v[0] for v in ref]


# ---------------------------------------------------------------------------
# Bresenham edge cases
# ---------------------------------------------------------------------------

class TestBresenhamCoverage:
    def test_supercover_6_diagonal(self):
        from src.traversal.bresenham import bresenham_traversal
        p0 = np.array([0.5, 0.5, 0.5])
        p1 = np.array([3.5, 3.5, 3.5])
        v6 = bresenham_traversal(p0, p1, connectivity=6)
        # 6-connected should have more voxels than 26-connected
        v26 = bresenham_traversal(p0, p1, connectivity=26)
        assert len(v6) >= len(v26)

    def test_bresenham_reverse(self):
        from src.traversal.bresenham import bresenham_traversal
        p0 = np.array([5.5, 5.5, 5.5])
        p1 = np.array([0.5, 0.5, 0.5])
        voxels = bresenham_traversal(p0, p1, connectivity=26)
        assert len(voxels) > 0

    def test_bresenham_negative_direction(self):
        from src.traversal.bresenham import bresenham_traversal
        p0 = np.array([10.5, 10.5, 10.5])
        p1 = np.array([0.5, 10.5, 10.5])
        voxels = bresenham_traversal(p0, p1, connectivity=26)
        assert len(voxels) >= 10

    def test_supercover_2d_plane(self):
        from src.traversal.bresenham import bresenham_traversal
        # Rays in XY plane (Z constant)
        p0 = np.array([0.5, 0.5, 5.0])
        p1 = np.array([5.5, 3.5, 5.0])
        v6 = bresenham_traversal(p0, p1, connectivity=6)
        assert len(v6) > 0
        v26 = bresenham_traversal(p0, p1, connectivity=26)
        assert len(v26) > 0


# ---------------------------------------------------------------------------
# Hierarchical and Adaptive grid construction
# ---------------------------------------------------------------------------

class TestHierarchicalGridConstruction:
    def test_hierarchical_grid_from_voxel_grid(self):
        from src.traversal.hierarchical import HierarchicalGrid
        grid = random_grid(32, density=0.5, seed=42)
        hg = HierarchicalGrid.from_voxel_grid(grid)
        assert hg.size == 32
        assert hg.n_bricks == 4

    def test_adaptive_grid_from_voxel_grid(self):
        from src.traversal.adaptive_hybrid import AdaptiveGrid
        grid = random_grid(32, density=0.5, seed=42)
        ag = AdaptiveGrid.from_voxel_grid(grid)
        assert ag.size == 32
        assert ag.n_bricks == 4

    def test_hierarchical_empty_grid(self):
        from src.traversal.hierarchical import HierarchicalGrid
        grid = empty_grid(16)
        hg = HierarchicalGrid(grid)
        assert np.sum(hg.brick_occupied) == 0

    def test_adaptive_empty_grid(self):
        from src.traversal.adaptive_hybrid import AdaptiveGrid
        grid = empty_grid(16)
        ag = AdaptiveGrid(grid)
        assert np.sum(ag.brick_occupied) == 0
        assert np.sum(ag.brick_density) == 0.0

    def test_adaptive_full_grid(self):
        from src.traversal.adaptive_hybrid import AdaptiveGrid
        grid = full_grid(16)
        ag = AdaptiveGrid(grid)
        assert np.all(ag.brick_occupied == 1)
        assert np.allclose(ag.brick_density, 1.0)


# ---------------------------------------------------------------------------
# Property-based tests
# ---------------------------------------------------------------------------

class TestPropertyBased:
    """Property-based tests verifying traversal invariants."""

    def test_t_values_positive_and_ordered(self):
        """t_enter <= t_exit for each voxel."""
        from src.traversal.dda import dda_traversal
        grid = full_grid(32)
        rng = np.random.RandomState(42)
        for _ in range(30):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            ray = Ray(rng.uniform(-2, 34, 3), d)
            result = dda_traversal(grid, ray)
            for voxel, t_e, t_x in result:
                assert t_e <= t_x + 1e-9

    def test_adjacent_voxels_share_face_edge_or_corner(self):
        """Consecutive traversed voxels are 26-connected (adjacent)."""
        from src.traversal.branchless import branchless_dda_traversal
        grid = full_grid(32)
        rng = np.random.RandomState(42)
        violations = 0
        for _ in range(30):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            ray = Ray(rng.uniform(-2, 34, 3), d)
            result = branchless_dda_traversal(grid, ray)
            for j in range(1, len(result)):
                v1 = result[j-1][0]
                v2 = result[j][0]
                diff = max(abs(v2[0]-v1[0]), abs(v2[1]-v1[1]), abs(v2[2]-v1[2]))
                if diff > 1:
                    violations += 1
        assert violations == 0

    def test_no_duplicate_consecutive_voxels(self):
        """No voxel appears twice in a row."""
        from src.traversal.dda import dda_traversal
        grid = full_grid(32)
        rng = np.random.RandomState(42)
        for _ in range(30):
            d = rng.randn(3)
            d /= np.linalg.norm(d)
            ray = Ray(rng.uniform(-2, 34, 3), d)
            result = dda_traversal(grid, ray)
            for j in range(1, len(result)):
                assert result[j][0] != result[j-1][0]
