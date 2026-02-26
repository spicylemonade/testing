"""Comprehensive correctness and robustness stress tests for all 7 traversal algorithms.

Item 020: verify no false positives, no false negatives, and edge case handling.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.voxel_grid import VoxelGrid
from src.core.ray import Ray
from src.core.grid_generators import random_grid, full_grid, empty_grid
from src.traversal.dda import dda_traversal
from src.traversal.branchless import branchless_dda_traversal
from src.traversal.cache_aware import cache_aware_dda_traversal
from src.traversal.hierarchical import hierarchical_traversal
from src.traversal.adaptive_hybrid import adaptive_hybrid_traversal
from src.traversal.simd_dda import simd_dda_traversal
from src.traversal.bresenham import bresenham_traversal


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Algorithms that share the DDA interface: (grid, ray) -> [(voxel, t_enter, t_exit)]
DDA_ALGORITHMS = {
    'dda': dda_traversal,
    'branchless': branchless_dda_traversal,
    'cache_aware': cache_aware_dda_traversal,
    'hierarchical': hierarchical_traversal,
    'adaptive_hybrid': adaptive_hybrid_traversal,
    'simd_dda': simd_dda_traversal,
}


def _ray_actually_intersects_voxel(ray, vx, vy, vz, tol=0.5):
    """Check that the ray geometrically passes through or very near the voxel."""
    # Sample a few t-values along the ray within the reported interval
    # and verify at least one sample is inside the voxel (with tolerance).
    result = dda_traversal(VoxelGrid(max(vx, vy, vz) + 2), ray)
    # Simpler: check that the midpoint of the reported t-interval is near the voxel
    return True  # we'll use a different approach below


def _voxel_contains_point(vx, vy, vz, point, tol=0.5):
    """Check that the point is inside or near the voxel [vx, vx+1) x [vy, vy+1) x [vz, vz+1)."""
    return (vx - tol <= point[0] <= vx + 1.0 + tol and
            vy - tol <= point[1] <= vy + 1.0 + tol and
            vz - tol <= point[2] <= vz + 1.0 + tol)


def _brute_force_voxels(ray, grid_size):
    """Brute-force reference: find all voxels the ray passes through.

    Samples many t-values along the ray and collects unique voxels.
    """
    from src.traversal.dda import _ray_grid_intersection
    t_min, t_max = _ray_grid_intersection(ray, grid_size)
    if t_min is None:
        return set()

    # Dense sampling along the ray
    n_samples = max(grid_size * 20, 1000)
    ts = np.linspace(t_min + 1e-10, t_max - 1e-10, n_samples)
    points = ray.origin[None, :] + ts[:, None] * ray.direction[None, :]

    voxels = set()
    for i in range(len(points)):
        vx = int(np.floor(points[i, 0]))
        vy = int(np.floor(points[i, 1]))
        vz = int(np.floor(points[i, 2]))
        if 0 <= vx < grid_size and 0 <= vy < grid_size and 0 <= vz < grid_size:
            voxels.add((vx, vy, vz))
    return voxels


# ---------------------------------------------------------------------------
# Test: No false positives (every reported voxel actually intersected)
# ---------------------------------------------------------------------------

class TestNoFalsePositives:
    """For each algorithm, verify that every reported voxel actually intersects the ray."""

    @pytest.fixture
    def grid32(self):
        return random_grid(32, density=0.3, seed=42)

    @pytest.fixture
    def rays_random(self):
        rng = np.random.RandomState(42)
        rays = []
        for _ in range(50):
            origin = rng.uniform(-2, 34, 3)
            direction = rng.randn(3)
            direction /= np.linalg.norm(direction)
            rays.append(Ray(origin, direction))
        return rays

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_no_false_positives(self, alg_name, grid32, rays_random):
        alg_fn = DDA_ALGORITHMS[alg_name]
        false_positives = 0
        for ray in rays_random:
            result = alg_fn(grid32, ray)
            for voxel, t_enter, t_exit in result:
                t_mid = (t_enter + t_exit) / 2.0
                point = ray.origin + t_mid * ray.direction
                vx, vy, vz = voxel
                if not _voxel_contains_point(vx, vy, vz, point):
                    false_positives += 1
        assert false_positives == 0, f"{alg_name}: {false_positives} false positives"


# ---------------------------------------------------------------------------
# Test: No false negatives (no voxels missed vs. brute-force)
# ---------------------------------------------------------------------------

class TestNoFalseNegatives:
    """Verify no voxels are missed by comparing against brute-force reference."""

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_no_false_negatives_small_grid(self, alg_name):
        """Compare against brute-force reference on 16^3 grid."""
        grid = random_grid(16, density=0.3, seed=42)
        alg_fn = DDA_ALGORITHMS[alg_name]
        rng = np.random.RandomState(123)

        missed = 0
        total_checks = 0
        for _ in range(30):
            origin = rng.uniform(-1, 17, 3)
            direction = rng.randn(3)
            direction /= np.linalg.norm(direction)
            ray = Ray(origin, direction)

            result = alg_fn(grid, ray)
            reported = set(v[0] for v in result)
            reference = _brute_force_voxels(ray, 16)

            # Every brute-force voxel should be in reported set
            for voxel in reference:
                total_checks += 1
                if voxel not in reported:
                    missed += 1

        assert missed == 0, f"{alg_name}: missed {missed}/{total_checks} voxels"

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_no_false_negatives_64(self, alg_name):
        """Brute-force comparison on 64^3 grid with fewer rays."""
        grid = random_grid(64, density=0.2, seed=42)
        alg_fn = DDA_ALGORITHMS[alg_name]
        rng = np.random.RandomState(456)

        missed = 0
        for _ in range(10):
            origin = rng.uniform(-1, 65, 3)
            direction = rng.randn(3)
            direction /= np.linalg.norm(direction)
            ray = Ray(origin, direction)

            result = alg_fn(grid, ray)
            reported = set(v[0] for v in result)
            reference = _brute_force_voxels(ray, 64)

            for voxel in reference:
                if voxel not in reported:
                    missed += 1

        assert missed == 0, f"{alg_name}: missed voxels on 64^3"


# ---------------------------------------------------------------------------
# Test: Numerical edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Test numerical edge cases for robustness."""

    @pytest.fixture
    def grid64(self):
        return full_grid(64)

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_ray_on_voxel_boundary_x(self, alg_name, grid64):
        """Ray exactly on an X-boundary plane."""
        ray = Ray(np.array([-1.0, 10.0, 10.0]),
                  np.array([1.0, 0.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) > 0, f"{alg_name}: no voxels for boundary ray"
        # Should traverse roughly grid_size voxels along X
        assert len(result) >= 50

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_ray_on_voxel_boundary_y(self, alg_name, grid64):
        """Ray exactly on a Y-boundary plane (integer Y coordinate)."""
        ray = Ray(np.array([10.0, -1.0, 10.0]),
                  np.array([0.0, 1.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) >= 50

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_ray_through_grid_corner(self, alg_name, grid64):
        """Ray passing through (0,0,0) corner."""
        ray = Ray(np.array([-1.0, -1.0, -1.0]),
                  np.array([1.0, 1.0, 1.0]) / np.sqrt(3))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) > 0
        # Should start at or near (0,0,0)
        first_voxel = result[0][0]
        assert first_voxel[0] <= 1 and first_voxel[1] <= 1 and first_voxel[2] <= 1

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_near_zero_direction_x(self, alg_name, grid64):
        """Direction with near-zero X component."""
        ray = Ray(np.array([32.0, -1.0, 32.0]),
                  np.array([1e-15, 1.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        # Should traverse along Y axis at fixed X
        assert len(result) >= 50

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_near_zero_direction_yz(self, alg_name, grid64):
        """Direction with near-zero Y and Z components."""
        ray = Ray(np.array([-1.0, 32.0, 32.0]),
                  np.array([1.0, 1e-15, 1e-15]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) >= 50

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_very_long_ray_256(self, alg_name):
        """Very long diagonal ray through 256^3 grid (>10000 voxels possible)."""
        grid = full_grid(256)
        ray = Ray(np.array([-1.0, -1.0, -1.0]),
                  np.array([1.0, 1.0, 1.0]) / np.sqrt(3))
        result = DDA_ALGORITHMS[alg_name](grid, ray)
        # Diagonal through 256^3 visits roughly 3*256 = 768 voxels
        assert len(result) >= 256

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_ray_misses_grid(self, alg_name, grid64):
        """Ray that completely misses the grid."""
        ray = Ray(np.array([-10.0, -10.0, -10.0]),
                  np.array([0.0, 0.0, -1.0]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) == 0

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_ray_from_inside(self, alg_name, grid64):
        """Ray starting from inside the grid."""
        ray = Ray(np.array([32.0, 32.0, 32.0]),
                  np.array([1.0, 0.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid64, ray)
        assert len(result) > 0
        # Should start at or near voxel (32, 32, 32)
        first_v = result[0][0]
        assert first_v[0] == 32 and first_v[1] == 32 and first_v[2] == 32


# ---------------------------------------------------------------------------
# Test: t-value monotonicity
# ---------------------------------------------------------------------------

class TestTValueMonotonicity:
    """t_enter values must be monotonically non-decreasing."""

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_t_monotonic(self, alg_name):
        grid = random_grid(32, density=0.5, seed=42)
        rng = np.random.RandomState(99)

        violations = 0
        for _ in range(50):
            origin = rng.uniform(-2, 34, 3)
            direction = rng.randn(3)
            direction /= np.linalg.norm(direction)
            ray = Ray(origin, direction)
            result = DDA_ALGORITHMS[alg_name](grid, ray)
            for i in range(1, len(result)):
                if result[i][1] < result[i-1][1] - 1e-9:
                    violations += 1
        assert violations == 0, f"{alg_name}: {violations} t-monotonicity violations"


# ---------------------------------------------------------------------------
# Test: Cross-algorithm consistency
# ---------------------------------------------------------------------------

class TestCrossAlgorithmConsistency:
    """All DDA-like algorithms should report the same voxels for the same ray."""

    def test_all_algorithms_agree(self):
        grid = random_grid(32, density=0.3, seed=42)
        rng = np.random.RandomState(77)

        mismatches = 0
        ref_name = 'dda'
        ref_fn = DDA_ALGORITHMS[ref_name]

        for _ in range(50):
            origin = rng.uniform(-1, 33, 3)
            direction = rng.randn(3)
            direction /= np.linalg.norm(direction)
            ray = Ray(origin, direction)

            ref_voxels = [v[0] for v in ref_fn(grid, ray)]
            for alg_name, alg_fn in DDA_ALGORITHMS.items():
                if alg_name == ref_name:
                    continue
                test_voxels = [v[0] for v in alg_fn(grid, ray)]
                if ref_voxels != test_voxels:
                    mismatches += 1

        assert mismatches == 0, f"{mismatches} cross-algorithm mismatches"


# ---------------------------------------------------------------------------
# Test: Bresenham-specific tests
# ---------------------------------------------------------------------------

class TestBresenhamRobustness:
    """Bresenham-specific correctness tests."""

    def test_bresenham_supercover_26(self):
        """26-connected traversal visits expected voxels."""
        p0 = np.array([0.5, 0.5, 0.5])
        p1 = np.array([5.5, 3.5, 2.5])
        voxels = bresenham_traversal(p0, p1, connectivity=26)
        assert len(voxels) > 0

    def test_bresenham_supercover_6(self):
        """6-connected traversal visits more voxels than 26-connected."""
        p0 = np.array([0.5, 0.5, 0.5])
        p1 = np.array([5.5, 3.5, 2.5])
        v26 = bresenham_traversal(p0, p1, connectivity=26)
        v6 = bresenham_traversal(p0, p1, connectivity=6)
        assert len(v6) >= len(v26)

    def test_bresenham_axis_aligned(self):
        """Axis-aligned line."""
        p0 = np.array([0.5, 5.5, 5.5])
        p1 = np.array([9.5, 5.5, 5.5])
        voxels = bresenham_traversal(p0, p1, connectivity=26)
        xs = [v[0] for v in voxels]
        assert min(xs) == 0 and max(xs) == 9

    def test_bresenham_single_voxel(self):
        """Start and end in same voxel."""
        p0 = np.array([3.1, 3.1, 3.1])
        p1 = np.array([3.9, 3.9, 3.9])
        voxels = bresenham_traversal(p0, p1, connectivity=26)
        assert len(voxels) >= 1
        assert voxels[0] == (3, 3, 3)


# ---------------------------------------------------------------------------
# Test: Empty and full grids
# ---------------------------------------------------------------------------

class TestSpecialGrids:
    """Test algorithms on empty and full grids."""

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_empty_grid(self, alg_name):
        """Traversal through empty grid."""
        grid = empty_grid(32)
        ray = Ray(np.array([-1.0, 16.0, 16.0]), np.array([1.0, 0.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid, ray)
        if alg_name in ('hierarchical', 'adaptive_hybrid'):
            # These algorithms correctly skip empty bricks — 0 voxels expected
            assert len(result) == 0
        else:
            # Flat algorithms traverse regardless of occupancy
            assert len(result) >= 20

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_full_grid(self, alg_name):
        """Traversal through fully occupied grid."""
        grid = full_grid(32)
        ray = Ray(np.array([-1.0, 16.0, 16.0]), np.array([1.0, 0.0, 0.0]))
        result = DDA_ALGORITHMS[alg_name](grid, ray)
        assert len(result) >= 20


# ---------------------------------------------------------------------------
# Test: All 26 directional octants
# ---------------------------------------------------------------------------

class TestAllOctants:
    """Verify correctness across all 26 directional octants."""

    @pytest.mark.parametrize("alg_name", list(DDA_ALGORITHMS.keys()))
    def test_all_26_octants(self, alg_name):
        grid = full_grid(16)
        alg_fn = DDA_ALGORITHMS[alg_name]

        for sx in [-1, 0, 1]:
            for sy in [-1, 0, 1]:
                for sz in [-1, 0, 1]:
                    if sx == 0 and sy == 0 and sz == 0:
                        continue
                    d = np.array([float(sx), float(sy), float(sz)])
                    d /= np.linalg.norm(d)
                    # Start outside the grid, pointing inward
                    o = np.array([8.0, 8.0, 8.0]) - d * 20.0
                    ray = Ray(o, d)
                    result = alg_fn(grid, ray)
                    assert len(result) > 0, \
                        f"{alg_name}: no voxels for direction ({sx},{sy},{sz})"
