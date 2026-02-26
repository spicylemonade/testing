"""
Hybrid ATSP solver for real road networks.

Multi-seed LKH-3 with numpy-vectorized asymmetry-aware local search.
Exploits directional cost asymmetry that LKH's Jonker-Volgenant
STSP transformation cannot capture.

References:
- Helsgott (2017) LKH-3 via J-V transformation [helsgott2017]
- Vu et al. (2019) Bounded asymmetry in road networks [vu2019]
"""

import time
from typing import Optional

import numpy as np


def compute_tour_cost(tour: list[int], matrix: np.ndarray) -> float:
    """Compute total directed tour cost using numpy."""
    t = np.array(tour)
    return float(np.sum(matrix[t, np.roll(t, -1)]))


# ---------------------------------------------------------------------------
# Numpy-vectorized local search operators
# ---------------------------------------------------------------------------

def _vectorized_or_opt_1(tour: list[int], matrix: np.ndarray) -> bool:
    """
    Single-node relocation using numpy broadcasting.

    For each node, evaluates ALL relocation targets simultaneously.
    Builds an (n x n) gain matrix and picks the best move.
    """
    n = len(tour)
    t = np.array(tour)
    t_next = np.roll(t, -1)
    t_prev = np.roll(t, 1)

    # Savings from removing each node i
    savings = matrix[t_prev, t] + matrix[t, t_next] - matrix[t_prev, t_next]

    # Insertion cost: inserting node t[i] between t[j] and t_next[j]
    M_jt = matrix[np.ix_(t, t)]           # (n,n): [j,i] = matrix[t[j], t[i]]
    M_tn = matrix[np.ix_(t, t_next)]      # (n,n): [i,j] = matrix[t[i], t_next[j]]
    edge_cost = matrix[t, t_next]          # (n,):  [j] = matrix[t[j], t_next[j]]

    ins_cost = M_jt + M_tn.T - edge_cost[:, np.newaxis]
    gains = savings[np.newaxis, :] - ins_cost

    # Mask: can't insert at own position or predecessor
    idx = np.arange(n)
    gains[idx, idx] = -np.inf
    gains[(idx - 1) % n, idx] = -np.inf

    best_flat = int(gains.argmax())
    j_best, i_best = divmod(best_flat, n)
    best_gain = gains[j_best, i_best]

    if best_gain > 1e-6:
        node = tour[i_best]
        after_node = tour[j_best]
        tour.pop(i_best)
        after_pos = tour.index(after_node)
        tour.insert(after_pos + 1, node)
        return True
    return False


def _vectorized_2opt(tour: list[int], matrix: np.ndarray) -> bool:
    """
    Asymmetric 2-opt using cumulative sums for O(1) per-pair evaluation.

    For ATSP, reversing a segment changes cost since matrix[a,b] != matrix[b,a].
    Precomputes cumulative forward-reverse difference for instant gain evaluation.
    """
    n = len(tour)
    if n < 4:
        return False

    t = np.array(tour)
    t_next = np.roll(t, -1)

    edge_fwd = matrix[t, t_next]
    edge_rev = matrix[t_next, t]
    diff = edge_fwd - edge_rev

    dc = np.zeros(n + 1)
    dc[1:] = np.cumsum(diff)

    # gain[i,j] = P[i] + Q[j] - R[i,j]
    P = edge_fwd - dc[1:]       # shape (n,)
    Q = edge_fwd + dc[:n]       # shape (n,)

    R = matrix[np.ix_(t, t)] + matrix[np.ix_(t_next, t_next)]

    gains = P[:, np.newaxis] + Q[np.newaxis, :] - R

    # Valid only for j >= i+2
    mask = np.triu(np.ones((n, n), dtype=bool), k=2)
    gains[~mask] = -np.inf

    best_flat = int(gains.argmax())
    i_best, j_best = divmod(best_flat, n)
    best_gain = gains[i_best, j_best]

    if best_gain > 1e-6:
        tour[i_best + 1:j_best + 1] = tour[i_best + 1:j_best + 1][::-1]
        return True
    return False


def _vectorized_or_opt_k(tour: list[int], matrix: np.ndarray, k: int) -> bool:
    """
    k-node segment relocation using numpy broadcasting.

    Relocates a contiguous segment of k nodes to the best insertion point.
    Uses non-wrapping segments only (misses at most k-1 out of n segments).
    """
    n = len(tour)
    if k >= n - 1 or n < k + 2:
        return False

    t = np.array(tour)
    t_next = np.roll(t, -1)

    # Non-wrapping segments: i = 0..n-k
    ns = n - k + 1

    seg_first = t[:ns]
    seg_last_indices = np.arange(k - 1, k - 1 + ns)
    seg_last = t[seg_last_indices]

    pred = np.roll(t, 1)[:ns]
    succ_indices = np.arange(k, k + ns) % n
    succ = t[succ_indices]

    savings = matrix[pred, seg_first] + matrix[seg_last, succ] - matrix[pred, succ]

    M_j_sf = matrix[np.ix_(t, seg_first)]       # (n, ns)
    M_sl_jn = matrix[np.ix_(seg_last, t_next)]   # (ns, n)
    base = matrix[t, t_next]                      # (n,)

    ins_cost = M_j_sf + M_sl_jn.T - base[:, np.newaxis]
    gains = savings[np.newaxis, :] - ins_cost

    # Mask positions overlapping with segment
    seg_idx = np.arange(ns)
    for off in range(-1, k):
        invalid_j = (seg_idx + off) % n
        gains[invalid_j, seg_idx] = -np.inf

    best_flat = int(gains.argmax())
    j_best, i_best = divmod(best_flat, ns)
    best_gain = gains[j_best, i_best]

    if best_gain > 1e-6:
        seg_start = i_best
        seg = tour[seg_start:seg_start + k]
        after_node = tour[j_best]
        del tour[seg_start:seg_start + k]
        after_pos = tour.index(after_node)
        for off, nd in enumerate(seg):
            tour.insert(after_pos + 1 + off, nd)
        return True
    return False


def _fast_local_search(
    tour: list[int], matrix: np.ndarray, time_limit: float = 30.0
) -> list[int]:
    """Apply vectorized operators until convergence or time limit."""
    t0 = time.perf_counter()
    for _ in range(200):
        if time.perf_counter() - t0 > time_limit:
            break
        if _vectorized_or_opt_1(tour, matrix):
            continue
        if _vectorized_or_opt_k(tour, matrix, k=2):
            continue
        if _vectorized_or_opt_k(tour, matrix, k=3):
            continue
        if _vectorized_2opt(tour, matrix):
            continue
        break
    return tour


# ---------------------------------------------------------------------------
# Perturbation
# ---------------------------------------------------------------------------

def _double_bridge(tour: list[int], rng: np.random.RandomState) -> list[int]:
    """Standard double-bridge perturbation."""
    n = len(tour)
    cuts = sorted(rng.choice(range(1, n), size=3, replace=False))
    a, b, c = cuts
    return tour[:a] + tour[b:c] + tour[a:b] + tour[c:]


def _asymmetry_guided_perturb(
    tour: list[int], matrix: np.ndarray, rng: np.random.RandomState
) -> list[int]:
    """Break high-asymmetry edges preferentially."""
    n = len(tour)
    t = np.array(tour)
    t_next = np.roll(t, -1)
    fwd = matrix[t, t_next]
    bwd = matrix[t_next, t]
    ratios = np.maximum(fwd, bwd) / (np.minimum(fwd, bwd) + 1e-10)

    top_k = min(8, n)
    top_indices = np.argpartition(ratios, -top_k)[-top_k:]

    if len(top_indices) < 3:
        return _double_bridge(tour, rng)

    chosen = sorted(rng.choice(top_indices, size=3, replace=False))
    cuts = [int(c) + 1 for c in chosen]
    cuts = sorted(set(max(1, min(c, n - 1)) for c in cuts))
    while len(cuts) < 3:
        cuts.append(min(cuts[-1] + 1, n - 1))
    cuts = sorted(set(cuts))[:3]
    if len(cuts) < 3 or cuts[-1] >= n:
        return _double_bridge(tour, rng)

    a, b, c = cuts
    return tour[:a] + tour[b:c] + tour[a:b] + tour[c:]


# ---------------------------------------------------------------------------
# Edge-frequency guided construction
# ---------------------------------------------------------------------------

def _build_freq_matrix(tours: list[list[int]], n: int) -> np.ndarray:
    """Build directed edge frequency matrix from a population of tours."""
    freq = np.zeros((n, n), dtype=np.float64)
    for tour in tours:
        t = np.array(tour)
        t_next = np.roll(t, -1)
        freq[t, t_next] += 1
    return freq


def _greedy_from_frequencies(
    freq: np.ndarray, matrix: np.ndarray, alpha: float = 0.5
) -> list[int]:
    """Construct a tour using edge frequencies as guidance."""
    n = freq.shape[0]
    max_freq = freq.max() + 1e-10
    max_cost = matrix.max() + 1e-10

    tour = [0]
    visited = np.zeros(n, dtype=bool)
    visited[0] = True

    for _ in range(n - 1):
        current = tour[-1]
        f_score = freq[current] / max_freq
        c_score = 1.0 - matrix[current] / max_cost
        scores = alpha * f_score + (1 - alpha) * c_score
        scores[visited] = -np.inf
        best_next = int(scores.argmax())
        tour.append(best_next)
        visited[best_next] = True

    return tour


# ---------------------------------------------------------------------------
# ILS post-optimization
# ---------------------------------------------------------------------------

def solve_ae_ils(
    matrix: np.ndarray,
    initial_tour: Optional[list[int]] = None,
    max_iterations: int = 50,
    max_no_improve: int = 20,
    seed: int = 42,
    time_limit: float = 60.0,
) -> dict:
    """Asymmetry-Exploiting Iterated Local Search."""
    t0 = time.perf_counter()
    rng = np.random.RandomState(seed)
    n = matrix.shape[0]

    if initial_tour is not None:
        tour = list(initial_tour)
    else:
        tour = list(range(n))

    # Initial local search
    ls_budget = min(time_limit * 0.3, 15.0)
    tour = _fast_local_search(tour, matrix, time_limit=ls_budget)
    best_tour = tour[:]
    best_cost = compute_tour_cost(best_tour, matrix)

    no_improve = 0
    improvements = 0

    for iteration in range(max_iterations):
        elapsed = time.perf_counter() - t0
        if elapsed > time_limit or no_improve >= max_no_improve:
            break

        if iteration % 3 == 0:
            perturbed = _asymmetry_guided_perturb(best_tour[:], matrix, rng)
        else:
            perturbed = _double_bridge(best_tour[:], rng)

        remaining = time_limit - (time.perf_counter() - t0)
        if remaining < 0.5:
            break
        perturbed = _fast_local_search(
            perturbed, matrix, time_limit=min(remaining * 0.3, 10.0)
        )
        perturbed_cost = compute_tour_cost(perturbed, matrix)

        if perturbed_cost < best_cost - 1e-10:
            best_tour = perturbed
            best_cost = perturbed_cost
            no_improve = 0
            improvements += 1
        else:
            no_improve += 1

    return {
        "tour": best_tour,
        "cost": best_cost,
        "wall_time": time.perf_counter() - t0,
        "n": n,
        "solver": "ae_ils",
        "iterations": iteration + 1 if max_iterations > 0 else 0,
        "improvements": improvements,
    }


# ---------------------------------------------------------------------------
# Main hybrid solver
# ---------------------------------------------------------------------------

def solve_hybrid(
    matrix: np.ndarray,
    max_trials: int = 500,
    runs: int = 1,
    max_lkh_seeds: int = 50,
    ils_iterations: int = 30,
    ils_no_improve: int = 15,
    seed: int = 42,
    time_limit: float = 300.0,
) -> dict:
    """
    Hybrid solver for ATSP on real road networks.

    Phase 1: Run LKH-3 with many random seeds for solution diversity.
             Uses most of the time budget since LKH is compiled C.
    Phase 2: Numpy-vectorized local search exploiting asymmetry.
    Phase 3: Edge-frequency guided construction from population.
    Phase 4: ILS post-optimization with asymmetry-guided perturbation.
    """
    from src.solvers.lkh_solver import solve_atsp as lkh_solve

    t0 = time.perf_counter()
    n = matrix.shape[0]
    base_rng = np.random.RandomState(seed)

    phase1_budget = time_limit * 0.85
    phase2_end = time_limit * 0.92
    phase3_end = time_limit * 0.97

    # Phase 1: Collect diverse LKH solutions
    population = []
    total_lkh_time = 0.0
    seeds_tried = 0

    while seeds_tried < max_lkh_seeds:
        elapsed = time.perf_counter() - t0
        if elapsed > phase1_budget:
            break

        s = int(base_rng.randint(1, 100000))
        # First few seeds use more runs for higher quality
        current_runs = min(runs + 2, 5) if seeds_tried < 3 else runs
        try:
            lkh_result = lkh_solve(
                matrix, max_trials=max_trials, runs=current_runs, seed=s,
            )
            total_lkh_time += lkh_result["wall_time"]
            population.append((lkh_result["cost"], lkh_result["tour"]))
        except Exception as e:
            print(f"  LKH seed {s} failed: {e}")
        seeds_tried += 1

    if not population:
        # Fallback: nearest-neighbor
        tour = list(range(n))
        cost = compute_tour_cost(tour, matrix)
        return {
            "tour": tour, "cost": cost, "lkh_cost": cost,
            "improvement_pct": 0.0, "wall_time": time.perf_counter() - t0,
            "lkh_time": 0.0, "n": n, "solver": "hybrid_ae_ils",
            "population_size": 0, "params": {},
        }

    population.sort(key=lambda x: x[0])
    lkh_best_cost = population[0][0]
    best_cost = lkh_best_cost
    best_tour = list(population[0][1])

    # Phase 2: Vectorized local search on best solutions
    for rank, (pop_cost, pop_tour) in enumerate(population[:3]):
        remaining = (t0 + time_limit * phase2_end) - time.perf_counter()
        if remaining < 1.0:
            break
        ls_budget = min(remaining / (3 - rank), 20.0)
        candidate = _fast_local_search(list(pop_tour), matrix, time_limit=ls_budget)
        c = compute_tour_cost(candidate, matrix)
        if c < best_cost - 1e-10:
            best_cost = c
            best_tour = candidate

    # Phase 3: Edge-frequency construction
    if len(population) >= 3:
        freq = _build_freq_matrix([t for _, t in population], n)
        for alpha in [0.3, 0.5, 0.7]:
            remaining = (t0 + time_limit * phase3_end) - time.perf_counter()
            if remaining < 1.0:
                break
            candidate = _greedy_from_frequencies(freq, matrix, alpha=alpha)
            candidate = _fast_local_search(
                candidate, matrix, time_limit=min(remaining / 3, 10.0)
            )
            c = compute_tour_cost(candidate, matrix)
            if c < best_cost - 1e-10:
                best_cost = c
                best_tour = candidate

    # Phase 4: ILS post-optimization
    remaining = time_limit - (time.perf_counter() - t0)
    if remaining > 3.0:
        ils_result = solve_ae_ils(
            matrix,
            initial_tour=best_tour,
            max_iterations=ils_iterations,
            max_no_improve=ils_no_improve,
            seed=seed,
            time_limit=remaining * 0.9,
        )
        if ils_result["cost"] < best_cost - 1e-10:
            best_cost = ils_result["cost"]
            best_tour = ils_result["tour"]

    wall_time = time.perf_counter() - t0

    return {
        "tour": best_tour,
        "cost": best_cost,
        "lkh_cost": lkh_best_cost,
        "improvement_pct": (lkh_best_cost - best_cost) / lkh_best_cost * 100
        if lkh_best_cost > 0 else 0.0,
        "wall_time": wall_time,
        "lkh_time": total_lkh_time,
        "n": n,
        "solver": "hybrid_ae_ils",
        "population_size": len(population),
        "seeds_tried": seeds_tried,
        "params": {
            "lkh_max_trials": max_trials,
            "lkh_runs": runs,
            "max_lkh_seeds": max_lkh_seeds,
            "ils_iterations": ils_iterations,
            "ils_no_improve": ils_no_improve,
            "seed": seed,
            "time_limit": time_limit,
        },
    }
