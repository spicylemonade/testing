"""Coherent ray batching with shared traversal state.

Clusters rays by direction similarity (octant + angular bin), then
processes each cluster with a specialized vectorized DDA that exploits
the shared step direction.  Within a coherent group every ray has the
same sign-step vector, so the inner SIMD loop replaces per-ray step
lookups with a single broadcast step, reducing memory traffic and
improving NumPy vectorisation efficiency.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray
from .branchless import branchless_dda_traversal


# ---------------------------------------------------------------------------
# Direction hashing / sorting — fully vectorised
# ---------------------------------------------------------------------------

def _direction_hash(direction, n_bins=8):
    """Hash a single ray direction into an octant + finer bin."""
    octant = 0
    if direction[0] >= 0: octant |= 1
    if direction[1] >= 0: octant |= 2
    if direction[2] >= 0: octant |= 4

    d = np.abs(direction)
    norm = np.sum(d)
    if norm < 1e-10:
        return 0
    d = d / norm

    bx = min(int(d[0] * n_bins), n_bins - 1)
    by = min(int(d[1] * n_bins), n_bins - 1)

    return octant * n_bins * n_bins + bx * n_bins + by


def _direction_hash_batch(directions, n_bins=8):
    """Vectorised direction hashing for an (N,3) direction array."""
    octant = np.zeros(len(directions), dtype=np.int64)
    octant += (directions[:, 0] >= 0).astype(np.int64) * 1
    octant += (directions[:, 1] >= 0).astype(np.int64) * 2
    octant += (directions[:, 2] >= 0).astype(np.int64) * 4

    d = np.abs(directions)
    norm = np.sum(d, axis=1, keepdims=True)
    norm[norm < 1e-10] = 1.0
    d = d / norm

    bx = np.clip((d[:, 0] * n_bins).astype(np.int64), 0, n_bins - 1)
    by = np.clip((d[:, 1] * n_bins).astype(np.int64), 0, n_bins - 1)

    return octant * n_bins * n_bins + bx * n_bins + by


def sort_rays_by_coherence(rays, n_bins=8):
    """Sort/cluster rays by direction similarity.

    Returns:
        sorted_rays: list of Ray objects sorted by direction bucket
        groups: list of (start_idx, end_idx, bucket_id) tuples
        original_indices: mapping from sorted position to original index
    """
    N = len(rays)
    hashes = np.array([_direction_hash(r.direction, n_bins) for r in rays])

    order = np.argsort(hashes, kind='stable')
    sorted_rays = [rays[i] for i in order]
    sorted_hashes = hashes[order]

    groups = []
    if N > 0:
        start = 0
        current_hash = sorted_hashes[0]
        for i in range(1, N):
            if sorted_hashes[i] != current_hash:
                groups.append((start, i, int(current_hash)))
                start = i
                current_hash = sorted_hashes[i]
        groups.append((start, N, int(current_hash)))

    return sorted_rays, groups, order


def sort_rays_by_coherence_arrays(origins, directions, n_bins=8):
    """Sort/cluster rays given as (N,3) arrays.  Returns arrays + groups."""
    N = len(origins)
    hashes = _direction_hash_batch(directions, n_bins)
    order = np.argsort(hashes, kind='stable')
    sorted_origins = origins[order]
    sorted_dirs = directions[order]
    sorted_hashes = hashes[order]

    groups = []
    if N > 0:
        changes = np.where(np.diff(sorted_hashes))[0] + 1
        starts = np.concatenate([[0], changes])
        ends = np.concatenate([changes, [N]])
        bucket_ids = sorted_hashes[starts]
        groups = list(zip(starts.tolist(), ends.tolist(), bucket_ids.tolist()))

    return sorted_origins, sorted_dirs, groups, order


# ---------------------------------------------------------------------------
# Single-ray interface (benchmark compatibility)
# ---------------------------------------------------------------------------

def coherent_batch_traversal(grid: VoxelGrid, ray: Ray):
    """Single-ray interface for benchmark compatibility."""
    return branchless_dda_traversal(grid, ray)


# ---------------------------------------------------------------------------
# Vectorised per-group DDA with shared step direction
# ---------------------------------------------------------------------------

def _coherent_group_dda(size, origins, directions, shared_step):
    """Vectorised DDA for a coherent group sharing the same step signs.

    Because every ray in the group has the same step vector, we avoid
    per-ray step lookups in the inner loop — step is broadcast from a
    single (3,) array.

    Args:
        size: int, grid side length
        origins: (M, 3) float64 array of ray origins
        directions: (M, 3) float64 array of ray directions
        shared_step: (3,) int64 array, sign-step shared by all rays

    Returns:
        dict mapping local index -> list of (voxel_tuple, t_enter, t_exit)
    """
    M = origins.shape[0]
    if M == 0:
        return {}

    with np.errstate(divide='ignore', invalid='ignore'):
        inv_dir = 1.0 / directions

    t0 = (0.0 - origins) * inv_dir
    t1 = (float(size) - origins) * inv_dir
    t_enter = np.minimum(t0, t1)
    t_exit = np.maximum(t0, t1)
    t_min = np.max(t_enter, axis=1)
    t_max_limit = np.min(t_exit, axis=1)

    for ax in range(3):
        zm = directions[:, ax] == 0.0
        out = zm & ((origins[:, ax] < 0.0) | (origins[:, ax] > size))
        t_min[out] = np.inf
        t_max_limit[out] = -np.inf

    t_min = np.maximum(t_min, 0.0)
    valid = t_min <= t_max_limit
    valid_idx = np.where(valid)[0]

    results = {i: [] for i in range(M)}
    if len(valid_idx) == 0:
        return results

    V = len(valid_idx)
    v_orig = origins[valid_idx]
    v_dir = directions[valid_idx]
    v_tmin = t_min[valid_idx].copy()
    v_tmax = t_max_limit[valid_idx]

    eps = 1e-10
    entry = v_orig + (v_tmin + eps)[:, None] * v_dir

    voxel = np.floor(entry).astype(np.int64)
    voxel = np.clip(voxel, 0, size - 1)

    # Shared step — broadcast (3,) across all rays
    step = shared_step  # (3,) int64

    with np.errstate(divide='ignore'):
        t_delta = np.abs(1.0 / v_dir)
    t_delta[~np.isfinite(t_delta)] = 1e30

    tma = np.empty((V, 3), dtype=np.float64)
    for ax in range(3):
        if step[ax] > 0:
            boundary = voxel[:, ax] + 1.0
        else:
            boundary = voxel[:, ax].astype(np.float64)
        with np.errstate(divide='ignore', invalid='ignore'):
            tma[:, ax] = v_tmin + (boundary - entry[:, ax]) / v_dir[:, ax]
        zero = v_dir[:, ax] == 0.0
        tma[zero, ax] = 1e30

    t_current = v_tmin.copy()
    active = np.ones(V, dtype=bool)
    max_steps = size * 3

    all_vx = []
    all_vy = []
    all_vz = []
    all_rid = []
    all_te = []
    all_tx = []

    arange_V = np.arange(V)

    for _ in range(max_steps):
        n_active = np.count_nonzero(active)
        if n_active == 0:
            break

        min_axis = np.argmin(tma, axis=1)
        t_next = np.minimum(tma[arange_V, min_axis], v_tmax)

        in_bounds = (
            active &
            (voxel[:, 0] >= 0) & (voxel[:, 0] < size) &
            (voxel[:, 1] >= 0) & (voxel[:, 1] < size) &
            (voxel[:, 2] >= 0) & (voxel[:, 2] < size)
        )
        ib_idx = np.where(in_bounds)[0]
        if len(ib_idx) > 0:
            all_vx.append(voxel[ib_idx, 0].copy())
            all_vy.append(voxel[ib_idx, 1].copy())
            all_vz.append(voxel[ib_idx, 2].copy())
            all_rid.append(valid_idx[ib_idx].copy())
            all_te.append(t_current[ib_idx].copy())
            all_tx.append(t_next[ib_idx].copy())

        done = t_next >= v_tmax - eps
        active &= ~done
        if not np.any(active):
            break

        # Shared-step advancement — step is broadcast, no per-ray lookup
        a_idx = np.where(active)[0]
        axes = min_axis[a_idx]
        voxel[a_idx, axes] += step[axes]  # broadcast shared step
        t_current[a_idx] = tma[a_idx, axes]
        tma[a_idx, axes] += t_delta[a_idx, axes]
        oob = (voxel[a_idx, axes] < 0) | (voxel[a_idx, axes] >= size)
        active[a_idx[oob]] = False

    # Reconstruct results
    if all_vx:
        rids = np.concatenate(all_rid)
        vxs = np.concatenate(all_vx)
        vys = np.concatenate(all_vy)
        vzs = np.concatenate(all_vz)
        tes = np.concatenate(all_te)
        txs = np.concatenate(all_tx)

        order_r = np.argsort(rids, kind='stable')
        rids = rids[order_r]
        vxs = vxs[order_r]
        vys = vys[order_r]
        vzs = vzs[order_r]
        tes = tes[order_r]
        txs = txs[order_r]

        breaks = np.where(np.diff(rids))[0] + 1
        starts = np.concatenate([[0], breaks])
        ends = np.concatenate([breaks, [len(rids)]])
        unique_rids = rids[starts]

        for k in range(len(unique_rids)):
            rid = unique_rids[k]
            s, e = starts[k], ends[k]
            results[rid] = [
                ((int(vxs[j]), int(vys[j]), int(vzs[j])),
                 float(tes[j]), float(txs[j]))
                for j in range(s, e)
            ]

    return results


# ---------------------------------------------------------------------------
# Main batch interface
# ---------------------------------------------------------------------------

def coherent_batch_process(grid: VoxelGrid, rays):
    """Process rays with coherent batching + vectorised per-group DDA.

    1. Sort rays by direction similarity (octant + angular bin)
    2. For each coherent group, run a vectorised DDA that exploits the
       shared step direction (broadcast step instead of per-ray lookup)
    3. Reassemble results in original ray order

    Args:
        grid: VoxelGrid
        rays: list of Ray objects

    Returns:
        dict mapping original ray index -> list of (voxel, t_enter, t_exit)
    """
    N = len(rays)
    if N == 0:
        return {}

    size = grid.size

    # Vectorised sorting — avoids per-ray Python hash loop
    all_origins = np.array([r.origin for r in rays], dtype=np.float64)
    all_directions = np.array([r.direction for r in rays], dtype=np.float64)
    all_origins, all_directions, groups, order = sort_rays_by_coherence_arrays(
        all_origins, all_directions
    )

    results = [None] * N

    for start, end, bucket_id in groups:
        grp_origins = all_origins[start:end]
        grp_directions = all_directions[start:end]

        # Compute shared step from group representative direction
        rep_dir = grp_directions[0]
        shared_step = np.array([
            1 if rep_dir[0] >= 0 else -1,
            1 if rep_dir[1] >= 0 else -1,
            1 if rep_dir[2] >= 0 else -1,
        ], dtype=np.int64)

        grp_results = _coherent_group_dda(
            size, grp_origins, grp_directions, shared_step
        )

        for local_i in range(end - start):
            orig_idx = order[start + local_i]
            results[orig_idx] = grp_results[local_i]

    return {i: results[i] for i in range(N)}


# ---------------------------------------------------------------------------
# Count-only coherent batch — for throughput benchmarking
# ---------------------------------------------------------------------------

def _coherent_group_count(size, origins, directions, shared_step):
    """Vectorised count-only DDA for a coherent group.

    Same as _coherent_group_dda but only counts voxels per ray — no
    result-list construction, so the hot loop stays fully in NumPy.
    """
    M = origins.shape[0]
    if M == 0:
        return np.zeros(0, dtype=np.int64)

    with np.errstate(divide='ignore', invalid='ignore'):
        inv_dir = 1.0 / directions

    t0 = (0.0 - origins) * inv_dir
    t1 = (float(size) - origins) * inv_dir
    t_enter = np.minimum(t0, t1)
    t_exit = np.maximum(t0, t1)
    t_min = np.max(t_enter, axis=1)
    t_max_limit = np.min(t_exit, axis=1)

    for ax in range(3):
        zm = directions[:, ax] == 0.0
        out = zm & ((origins[:, ax] < 0.0) | (origins[:, ax] > size))
        t_min[out] = np.inf
        t_max_limit[out] = -np.inf

    t_min = np.maximum(t_min, 0.0)
    valid = t_min <= t_max_limit
    valid_idx = np.where(valid)[0]

    counts = np.zeros(M, dtype=np.int64)
    if len(valid_idx) == 0:
        return counts

    V = len(valid_idx)
    v_orig = origins[valid_idx]
    v_dir = directions[valid_idx]
    v_tmin = t_min[valid_idx].copy()
    v_tmax = t_max_limit[valid_idx]

    eps = 1e-10
    entry = v_orig + (v_tmin + eps)[:, None] * v_dir

    voxel = np.floor(entry).astype(np.int64)
    voxel = np.clip(voxel, 0, size - 1)

    step = shared_step  # (3,) broadcast

    with np.errstate(divide='ignore'):
        t_delta = np.abs(1.0 / v_dir)
    t_delta[~np.isfinite(t_delta)] = 1e30

    tma = np.empty((V, 3), dtype=np.float64)
    for ax in range(3):
        if step[ax] > 0:
            boundary = voxel[:, ax] + 1.0
        else:
            boundary = voxel[:, ax].astype(np.float64)
        with np.errstate(divide='ignore', invalid='ignore'):
            tma[:, ax] = v_tmin + (boundary - entry[:, ax]) / v_dir[:, ax]
        zero = v_dir[:, ax] == 0.0
        tma[zero, ax] = 1e30

    active = np.ones(V, dtype=bool)
    v_counts = np.zeros(V, dtype=np.int64)
    max_steps = size * 3
    arange_V = np.arange(V)

    for _ in range(max_steps):
        if not np.any(active):
            break

        min_axis = np.argmin(tma, axis=1)
        t_next = np.minimum(tma[arange_V, min_axis], v_tmax)

        in_bounds = (
            active &
            (voxel[:, 0] >= 0) & (voxel[:, 0] < size) &
            (voxel[:, 1] >= 0) & (voxel[:, 1] < size) &
            (voxel[:, 2] >= 0) & (voxel[:, 2] < size)
        )
        v_counts[in_bounds] += 1

        done = t_next >= v_tmax - eps
        active &= ~done
        if not np.any(active):
            break

        a_idx = np.where(active)[0]
        axes = min_axis[a_idx]
        voxel[a_idx, axes] += step[axes]  # broadcast shared step
        tma[a_idx, axes] += t_delta[a_idx, axes]
        oob = (voxel[a_idx, axes] < 0) | (voxel[a_idx, axes] >= size)
        active[a_idx[oob]] = False

    counts[valid_idx] = v_counts
    return counts


def coherent_batch_count(grid: VoxelGrid, rays):
    """Count-only coherent batch — returns voxel count per ray.

    Optimised for throughput benchmarking: no result-list construction.
    Uses vectorised hashing and shared-step DDA per coherent group.
    """
    N = len(rays)
    if N == 0:
        return np.zeros(0, dtype=np.int64)

    origins = np.array([r.origin for r in rays], dtype=np.float64)
    directions = np.array([r.direction for r in rays], dtype=np.float64)
    size = grid.size

    sorted_origins, sorted_dirs, groups, order = sort_rays_by_coherence_arrays(
        origins, directions
    )

    counts = np.zeros(N, dtype=np.int64)
    for start, end, bucket_id in groups:
        grp_orig = sorted_origins[start:end]
        grp_dir = sorted_dirs[start:end]

        rep = grp_dir[0]
        shared_step = np.array([
            1 if rep[0] >= 0 else -1,
            1 if rep[1] >= 0 else -1,
            1 if rep[2] >= 0 else -1,
        ], dtype=np.int64)

        grp_counts = _coherent_group_count(size, grp_orig, grp_dir, shared_step)
        counts[order[start:end]] = grp_counts

    return counts
