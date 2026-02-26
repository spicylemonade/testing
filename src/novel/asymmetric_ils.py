"""
Improved hybrid ATSP solver for real road networks.

Strategy: Multi-configuration LKH-3 with diverse candidate sets and
asymmetry-aware initial tours for warm-starting.

Key insight: LKH's alpha-value candidate generation is Euclidean-biased.
By using multiple candidate set types (ALPHA, NEAREST-NEIGHBOR) and
warm-starting from asymmetry-aware initial tours, we guide LKH to
explore different basins of attraction in the solution space.

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
# Asymmetry-aware initial tour construction
# ---------------------------------------------------------------------------

def _directed_nn(matrix: np.ndarray, start: int = 0) -> list[int]:
    """Standard directed nearest-neighbor from given start node."""
    n = matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        costs = matrix[tour[-1]].copy()
        costs[visited] = np.inf
        nxt = int(np.argmin(costs))
        tour.append(nxt)
        visited[nxt] = True
    return tour


def _asymmetry_penalized_nn(
    matrix: np.ndarray, start: int = 0, penalty: float = 0.3,
) -> list[int]:
    """
    NN that penalizes high-asymmetry edges.

    Score = outbound_cost + penalty * |outbound - inbound|

    Edges with similar forward/reverse costs are preferred, as they
    indicate symmetric road segments more likely to appear in good tours.
    """
    n = matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        curr = tour[-1]
        outbound = matrix[curr]
        inbound = matrix[:, curr]
        score = outbound + penalty * np.abs(outbound - inbound)
        score[visited] = np.inf
        nxt = int(np.argmin(score))
        tour.append(nxt)
        visited[nxt] = True
    return tour


def _inbound_aware_nn(matrix: np.ndarray, start: int = 0) -> list[int]:
    """
    NN considering both outbound cost and how easy the next node is to leave.

    Score = outbound_cost + weight * min_outbound_from_next

    Prefers nodes that are both cheap to reach AND cheap to leave.
    """
    n = matrix.shape[0]
    # Precompute: for each node, what's the cheapest way to leave?
    min_outbound = np.partition(matrix, 1, axis=1)[:, 1]  # 2nd smallest (skip self=0)

    visited = np.zeros(n, dtype=bool)
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        curr = tour[-1]
        outbound = matrix[curr]
        score = outbound + 0.3 * min_outbound
        score[visited] = np.inf
        nxt = int(np.argmin(score))
        tour.append(nxt)
        visited[nxt] = True
    return tour


def _generate_initial_tours(
    matrix: np.ndarray, max_tours: int = 8, seed: int = 42,
) -> list[list[int]]:
    """Generate diverse initial tours for LKH warm-starting."""
    rng = np.random.RandomState(seed)
    n = matrix.shape[0]
    tours = []

    # Directed NN from multiple random starts
    starts = sorted(set([0] + rng.choice(n, size=min(4, n), replace=False).tolist()))
    for s in starts[:3]:
        tours.append(_directed_nn(matrix, start=s))

    # Asymmetry-penalized NN with different penalty weights
    for pw in [0.2, 0.5]:
        s = rng.randint(0, n)
        tours.append(_asymmetry_penalized_nn(matrix, start=s, penalty=pw))

    # Inbound-aware NN
    tours.append(_inbound_aware_nn(matrix, start=0))

    # Deduplicate by cost (keep unique tours)
    seen_costs = set()
    unique_tours = []
    for t in tours:
        c = round(compute_tour_cost(t, matrix), 2)
        if c not in seen_costs:
            seen_costs.add(c)
            unique_tours.append(t)

    return unique_tours[:max_tours]


# ---------------------------------------------------------------------------
# Correct vectorized or-opt-1 post-processing
# ---------------------------------------------------------------------------

def _or_opt_1_pass(tour: list[int], matrix: np.ndarray) -> Optional[list[int]]:
    """
    Single pass of or-opt-1: find best single-node relocation.
    Returns new tour if improved, None otherwise.
    """
    n = len(tour)
    t = np.array(tour)
    t_next = np.roll(t, -1)
    t_prev = np.roll(t, 1)

    # Savings from removing node at position i
    savings = matrix[t_prev, t] + matrix[t, t_next] - matrix[t_prev, t_next]

    # Cost of inserting node t[i] between t[j] and t_next[j]
    M_jt = matrix[np.ix_(t, t)]           # [j,i] = matrix[t[j], t[i]]
    M_tn = matrix[np.ix_(t, t_next)]      # [i,j] = matrix[t[i], t_next[j]]
    edge_cost = matrix[t, t_next]          # [j] = matrix[t[j], t_next[j]]

    ins_cost = M_jt + M_tn.T - edge_cost[:, np.newaxis]  # (n,n): [j,i]
    gains = savings[np.newaxis, :] - ins_cost

    # Mask invalid: can't insert at same position or predecessor
    idx = np.arange(n)
    gains[idx, idx] = -np.inf
    gains[(idx - 1) % n, idx] = -np.inf

    best_flat = int(np.argmax(gains))
    j_best, i_best = divmod(best_flat, n)

    if gains[j_best, i_best] > 1e-6:
        new_tour = tour[:]
        node = new_tour[i_best]
        target_node = tour[j_best]  # Value from original tour
        new_tour.pop(i_best)
        insert_pos = new_tour.index(target_node) + 1
        new_tour.insert(insert_pos, node)
        return new_tour
    return None


def _or_opt_improve(
    tour: list[int], matrix: np.ndarray,
    max_iters: int = 200, time_limit: float = 10.0,
) -> list[int]:
    """Apply or-opt-1 until convergence or time limit."""
    t0 = time.perf_counter()
    current = tour[:]
    for _ in range(max_iters):
        if time.perf_counter() - t0 > time_limit:
            break
        improved = _or_opt_1_pass(current, matrix)
        if improved is None:
            break
        current = improved
    return current


# ---------------------------------------------------------------------------
# Main hybrid solver
# ---------------------------------------------------------------------------

def solve_hybrid(
    matrix: np.ndarray,
    max_trials: int = 500,
    runs_per_seed: int = 2,
    seed: int = 42,
    time_limit: float = 300.0,
    use_initial_tours: bool = True,
) -> dict:
    """
    Multi-configuration LKH-3 solver for ATSP on real road networks.

    Phase 1: Generate asymmetry-aware initial tours (fast).
    Phase 2: Run LKH from initial tours as warm starts.
    Phase 3: Run LKH with diverse parameter configs and random seeds.
    Phase 4: Quick or-opt post-processing on best result.
    """
    from src.solvers.lkh_solver import solve_atsp as lkh_solve

    t0 = time.perf_counter()
    n = matrix.shape[0]
    rng = np.random.RandomState(seed)

    # LKH configuration variants for search diversity
    # Note: CANDIDATE_SET_TYPE=NEAREST-NEIGHBOR doesn't work with EXPLICIT matrices
    configs = [
        # Default ALPHA candidates, balanced runs
        {"label": "alpha_std", "extra_params": None, "weight": 0.35},
        # More candidates per node for better ATSP coverage
        {"label": "wide_cands", "extra_params": {
            "MAX_CANDIDATES": 10,
        }, "weight": 0.25},
        # Deeper search with more trials per run
        {"label": "deep", "max_trials": 1000, "runs": 1, "extra_params": {
            "MAX_CANDIDATES": 8,
        }, "weight": 0.20},
        # Enhanced ATSP patching
        {"label": "patching", "extra_params": {
            "PATCHING_A": 3,
            "PATCHING_C": 3,
        }, "weight": 0.20},
    ]

    population = []
    total_lkh_time = 0.0
    seeds_tried = 0
    warm_starts_tried = 0
    warm_start_used = False

    # Phase 1: Generate initial tours
    initial_tours = []
    if use_initial_tours:
        try:
            initial_tours = _generate_initial_tours(matrix, max_tours=6, seed=seed)
        except Exception as e:
            print(f"  Initial tour generation failed: {e}")

    # Phase 2: Warm-start LKH from initial tours
    warm_budget = time_limit * 0.20 if initial_tours else 0
    for init_tour in initial_tours:
        if time.perf_counter() - t0 > warm_budget:
            break
        s = int(rng.randint(1, 100000))
        try:
            result = lkh_solve(
                matrix, max_trials=max_trials, runs=runs_per_seed, seed=s,
                initial_tour=init_tour,
            )
            population.append((result["cost"], result["tour"]))
            total_lkh_time += result["wall_time"]
            warm_starts_tried += 1
            warm_start_used = True
        except Exception as e:
            # Initial tour format might not work - fall back to no warm start
            print(f"  Warm-start failed: {e}")
            if not warm_start_used:
                # Try without initial tour for remaining budget
                break

    # Phase 3: Multi-config LKH with random seeds
    remaining_budget = time_limit * 0.92 - (time.perf_counter() - t0)
    if remaining_budget < 5:
        remaining_budget = time_limit * 0.92  # reset if warm starts consumed too much

    for config in configs:
        config_time = remaining_budget * config["weight"]
        config_start = time.perf_counter()
        c_trials = config.get("max_trials", max_trials)
        c_runs = config.get("runs", runs_per_seed)
        c_extra = config.get("extra_params")

        while True:
            elapsed_config = time.perf_counter() - config_start
            elapsed_total = time.perf_counter() - t0
            if elapsed_config > config_time or elapsed_total > time_limit * 0.92:
                break

            s = int(rng.randint(1, 100000))
            try:
                result = lkh_solve(
                    matrix, max_trials=c_trials, runs=c_runs, seed=s,
                    extra_params=c_extra,
                )
                population.append((result["cost"], result["tour"]))
                total_lkh_time += result["wall_time"]
            except Exception as e:
                print(f"  LKH ({config['label']}) failed: {e}")
            seeds_tried += 1

    if not population:
        # Emergency fallback: single LKH run with defaults
        try:
            result = lkh_solve(matrix, max_trials=500, runs=3, seed=42)
            population.append((result["cost"], result["tour"]))
            total_lkh_time += result["wall_time"]
        except Exception as e:
            print(f"  Fallback LKH also failed: {e}")
            tour = list(range(n))
            cost = compute_tour_cost(tour, matrix)
            return {
                "tour": tour, "cost": cost, "lkh_cost": cost,
                "improvement_pct": 0.0, "wall_time": time.perf_counter() - t0,
                "lkh_time": 0.0, "n": n, "solver": "hybrid_multiconfig",
                "population_size": 0, "seeds_tried": 0, "warm_starts": 0,
                "params": {},
            }

    population.sort(key=lambda x: x[0])
    lkh_best_cost = population[0][0]
    best_tour = list(population[0][1])
    best_cost = lkh_best_cost

    # Phase 4: Quick or-opt post-processing
    remaining = time_limit - (time.perf_counter() - t0)
    if remaining > 2.0:
        try:
            # Try on top-3 solutions
            for rank in range(min(3, len(population))):
                r_time = time_limit - (time.perf_counter() - t0)
                if r_time < 1.0:
                    break
                candidate = _or_opt_improve(
                    list(population[rank][1]), matrix,
                    max_iters=200, time_limit=min(r_time / 3, 10.0),
                )
                c = compute_tour_cost(candidate, matrix)
                if c < best_cost - 1e-10:
                    best_cost = c
                    best_tour = candidate
        except Exception as e:
            print(f"  Or-opt failed: {e}")

    wall_time = time.perf_counter() - t0
    improvement = (
        (lkh_best_cost - best_cost) / lkh_best_cost * 100
        if lkh_best_cost > 0 else 0.0
    )

    return {
        "tour": best_tour,
        "cost": best_cost,
        "lkh_cost": lkh_best_cost,
        "improvement_pct": improvement,
        "wall_time": wall_time,
        "lkh_time": total_lkh_time,
        "n": n,
        "solver": "hybrid_multiconfig",
        "population_size": len(population),
        "seeds_tried": seeds_tried,
        "warm_starts": warm_starts_tried,
        "params": {
            "lkh_max_trials": max_trials,
            "lkh_runs_per_seed": runs_per_seed,
            "seed": seed,
            "time_limit": time_limit,
            "use_initial_tours": use_initial_tours,
            "num_configs": len(configs),
        },
    }
