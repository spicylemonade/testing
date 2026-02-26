"""SIMD-vectorized DDA traversal using NumPy.

Processes batches of N rays simultaneously through the same grid.
The inner traversal step operates entirely on NumPy arrays with no
per-ray Python loops in the hot path.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray


def simd_dda_traversal(grid: VoxelGrid, ray: Ray):
    """Single-ray wrapper for benchmark interface compatibility."""
    results_dict = simd_dda_batch(grid, [ray])
    return results_dict[0]


def simd_dda_batch(grid: VoxelGrid, rays):
    """Batch-vectorized DDA traversal for N rays.

    All rays advance simultaneously in each step using vectorized NumPy
    operations. No per-ray Python loops in the traversal hot path.

    Args:
        grid: VoxelGrid to traverse
        rays: list of Ray objects

    Returns:
        dict mapping ray index -> list of (voxel_tuple, t_enter, t_exit)
    """
    N = len(rays)
    size = grid.size
    origins = np.array([r.origin for r in rays], dtype=np.float64)
    directions = np.array([r.direction for r in rays], dtype=np.float64)

    return _simd_dda_core(size, origins, directions, N)


def _simd_dda_core(size, origins, directions, N):
    """Core vectorized DDA — separated for profiling."""
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

    results = {i: [] for i in range(N)}
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

    step = np.sign(v_dir).astype(np.int64)
    step[step == 0] = 1

    with np.errstate(divide='ignore'):
        t_delta = np.abs(1.0 / v_dir)
    t_delta[~np.isfinite(t_delta)] = 1e30

    tma = np.empty((V, 3), dtype=np.float64)
    for ax in range(3):
        pos = v_dir[:, ax] > 0
        boundary = np.where(pos, voxel[:, ax] + 1.0, voxel[:, ax].astype(np.float64))
        with np.errstate(divide='ignore', invalid='ignore'):
            tma[:, ax] = v_tmin + (boundary - entry[:, ax]) / v_dir[:, ax]
        zero = v_dir[:, ax] == 0.0
        tma[zero, ax] = 1e30

    t_current = v_tmin.copy()
    active = np.ones(V, dtype=bool)
    max_steps = size * 3

    # Pre-allocate flat output arrays
    cap = V * max_steps
    # Use chunked approach: collect voxel indices and metadata
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

        # Vectorized: find min axis, compute t_next
        min_axis = np.argmin(tma, axis=1)
        t_next = np.minimum(tma[arange_V, min_axis], v_tmax)

        # Vectorized in-bounds check
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

        # Vectorized termination
        done = t_next >= v_tmax - eps
        active &= ~done
        if not np.any(active):
            break

        # FULLY VECTORIZED STEP (no per-ray loop)
        a_idx = np.where(active)[0]
        axes = min_axis[a_idx]
        voxel[a_idx, axes] += step[a_idx, axes]
        t_current[a_idx] = tma[a_idx, axes]
        tma[a_idx, axes] += t_delta[a_idx, axes]
        oob = (voxel[a_idx, axes] < 0) | (voxel[a_idx, axes] >= size)
        active[a_idx[oob]] = False

    # Reconstruct results from flat arrays
    if all_vx:
        rids = np.concatenate(all_rid)
        vxs = np.concatenate(all_vx)
        vys = np.concatenate(all_vy)
        vzs = np.concatenate(all_vz)
        tes = np.concatenate(all_te)
        txs = np.concatenate(all_tx)

        # Group by ray index using sorting
        order = np.argsort(rids, kind='stable')
        rids = rids[order]
        vxs = vxs[order]
        vys = vys[order]
        vzs = vzs[order]
        tes = tes[order]
        txs = txs[order]

        # Find boundaries between ray groups
        breaks = np.where(np.diff(rids))[0] + 1
        starts = np.concatenate([[0], breaks])
        ends = np.concatenate([breaks, [len(rids)]])
        unique_rids = rids[starts]

        for k in range(len(unique_rids)):
            rid = unique_rids[k]
            s, e = starts[k], ends[k]
            results[rid] = [
                ((int(vxs[j]), int(vys[j]), int(vzs[j])), float(tes[j]), float(txs[j]))
                for j in range(s, e)
            ]

    return results


def simd_dda_count_batch(grid: VoxelGrid, rays):
    """Fast batch traversal returning only voxel count per ray.

    Optimized for throughput benchmarking — no result collection overhead.
    """
    N = len(rays)
    size = grid.size
    origins = np.array([r.origin for r in rays], dtype=np.float64)
    directions = np.array([r.direction for r in rays], dtype=np.float64)

    with np.errstate(divide='ignore', invalid='ignore'):
        inv_dir = 1.0 / directions

    t0 = (0.0 - origins) * inv_dir
    t1 = (float(size) - origins) * inv_dir
    t_enter = np.minimum(t0, t1)
    t_exit_arr = np.maximum(t0, t1)
    t_min = np.max(t_enter, axis=1)
    t_max_limit = np.min(t_exit_arr, axis=1)

    for ax in range(3):
        zm = directions[:, ax] == 0.0
        out = zm & ((origins[:, ax] < 0.0) | (origins[:, ax] > size))
        t_min[out] = np.inf
        t_max_limit[out] = -np.inf

    t_min = np.maximum(t_min, 0.0)
    valid = t_min <= t_max_limit
    valid_idx = np.where(valid)[0]

    counts = np.zeros(N, dtype=np.int64)
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

    step = np.sign(v_dir).astype(np.int64)
    step[step == 0] = 1

    with np.errstate(divide='ignore'):
        t_delta = np.abs(1.0 / v_dir)
    t_delta[~np.isfinite(t_delta)] = 1e30

    tma = np.empty((V, 3), dtype=np.float64)
    for ax in range(3):
        pos = v_dir[:, ax] > 0
        boundary = np.where(pos, voxel[:, ax] + 1.0, voxel[:, ax].astype(np.float64))
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
        voxel[a_idx, axes] += step[a_idx, axes]
        tma[a_idx, axes] += t_delta[a_idx, axes]
        oob = (voxel[a_idx, axes] < 0) | (voxel[a_idx, axes] >= size)
        active[a_idx[oob]] = False

    counts[valid_idx] = v_counts
    return counts
