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


def _cheapest_insertion(matrix: np.ndarray, seed: int = 42) -> list[int]:
    """
    Cheapest insertion heuristic for ATSP.

    Start with the shortest edge, then repeatedly insert the node
    that causes the smallest increase in tour cost.
    """
    n = matrix.shape[0]
    rng = np.random.RandomState(seed)

    # Start with 3 random nodes forming a mini-tour
    starts = rng.choice(n, size=min(3, n), replace=False).tolist()
    tour = starts[:]
    in_tour = set(tour)

    while len(tour) < n:
        best_cost = np.inf
        best_node = -1
        best_pos = -1

        # Find cheapest insertion among all unvisited nodes
        for node in range(n):
            if node in in_tour:
                continue
            for pos in range(len(tour)):
                prev = tour[pos]
                nxt = tour[(pos + 1) % len(tour)]
                cost = matrix[prev, node] + matrix[node, nxt] - matrix[prev, nxt]
                if cost < best_cost:
                    best_cost = cost
                    best_node = node
                    best_pos = pos + 1

        if best_node < 0:
            break
        tour.insert(best_pos, best_node)
        in_tour.add(best_node)

    return tour


def _farthest_insertion(matrix: np.ndarray, seed: int = 42) -> list[int]:
    """
    Farthest insertion heuristic for ATSP.

    Start from a random node, then repeatedly insert the node farthest from
    the current partial tour at its cheapest insertion position.
    """
    n = matrix.shape[0]
    rng = np.random.RandomState(seed)

    start = rng.randint(0, n)
    tour = [start]
    in_tour = set(tour)

    # Find the node farthest from start
    dists = matrix[start].copy()
    dists[start] = -np.inf
    farthest = int(np.argmax(dists))
    tour.append(farthest)
    in_tour.add(farthest)

    while len(tour) < n:
        # Find farthest unvisited node (min distance to any tour node)
        min_dist_to_tour = np.full(n, np.inf)
        for t_node in tour:
            min_dist_to_tour = np.minimum(min_dist_to_tour, matrix[t_node])
        for t_node in in_tour:
            min_dist_to_tour[t_node] = -np.inf
        node = int(np.argmax(min_dist_to_tour))

        # Find cheapest insertion position
        best_cost = np.inf
        best_pos = 0
        for pos in range(len(tour)):
            prev = tour[pos]
            nxt = tour[(pos + 1) % len(tour)]
            cost = matrix[prev, node] + matrix[node, nxt] - matrix[prev, nxt]
            if cost < best_cost:
                best_cost = cost
                best_pos = pos + 1

        tour.insert(best_pos, node)
        in_tour.add(node)

    return tour


def _generate_initial_tours(
    matrix: np.ndarray, max_tours: int = 8, seed: int = 42,
) -> list[list[int]]:
    """Generate diverse initial tours for LKH warm-starting."""
    rng = np.random.RandomState(seed)
    n = matrix.shape[0]
    tours = []

    # Directed NN from multiple random starts (3 tours)
    starts = sorted(set([0] + rng.choice(n, size=min(4, n), replace=False).tolist()))
    for s in starts[:3]:
        tours.append(_directed_nn(matrix, start=s))

    # Asymmetry-penalized NN with focused penalty weights (2 tours)
    for pw in [0.25, 0.5]:
        s = rng.randint(0, n)
        tours.append(_asymmetry_penalized_nn(matrix, start=s, penalty=pw))

    # Inbound-aware NN from multiple starts (2 tours)
    for _ in range(2):
        s = rng.randint(0, n)
        tours.append(_inbound_aware_nn(matrix, start=s))

    # Cheapest insertion (1 tour)
    tours.append(_cheapest_insertion(matrix, seed=seed))

    # Deduplicate by cost (keep unique tours)
    seen_costs = set()
    unique_tours = []
    for t in tours:
        c = round(compute_tour_cost(t, matrix), 2)
        if c not in seen_costs:
            seen_costs.add(c)
            unique_tours.append(t)

    # Sort by cost - best tours first for warm-starting
    unique_tours.sort(key=lambda t: compute_tour_cost(t, matrix))

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


def _or_opt_k_pass(tour: list[int], matrix: np.ndarray, k: int = 2) -> Optional[list[int]]:
    """
    Or-opt-k: relocate a segment of k consecutive nodes.

    For each segment of k nodes, try removing it and reinserting after every
    other position. Accept the best improving move if any.
    """
    n = len(tour)
    if n <= k + 2:
        return None

    best_gain = 1e-6
    best_i = -1
    best_j = -1

    for i in range(n):
        # Segment: tour[i], tour[i+1], ..., tour[(i+k-1)%n]
        seg_start = i
        seg_end = (i + k - 1) % n
        prev_seg = (i - 1) % n
        next_seg = (i + k) % n

        # Cost of removing segment
        cost_remove = matrix[tour[prev_seg], tour[seg_start]]
        for s in range(k - 1):
            cost_remove += matrix[tour[(i + s) % n], tour[(i + s + 1) % n]]
        cost_remove += matrix[tour[seg_end], tour[next_seg]]

        # Cost of bridge after removal
        cost_bridge = matrix[tour[prev_seg], tour[next_seg]]
        savings = cost_remove - cost_bridge

        if savings < 1e-6:
            continue

        # Try inserting segment after each valid position
        for j in range(n):
            # Skip positions within or adjacent to the segment
            in_segment = False
            for s in range(k):
                if j == (i + s) % n:
                    in_segment = True
                    break
            if in_segment or j == prev_seg:
                continue

            j_next = (j + 1) % n
            # Cost of inserting segment between j and j_next
            cost_insert = (
                matrix[tour[j], tour[seg_start]]
                + matrix[tour[seg_end], tour[j_next]]
                - matrix[tour[j], tour[j_next]]
            )
            # Add internal segment cost back
            for s in range(k - 1):
                cost_insert += matrix[tour[(i + s) % n], tour[(i + s + 1) % n]]

            gain = savings - cost_insert + sum(
                matrix[tour[(i + s) % n], tour[(i + s + 1) % n]] for s in range(k - 1)
            )
            # Simpler: gain = (removal savings) - (insertion penalty)
            # removal saves: cost_remove - cost_bridge = savings
            # insertion costs: matrix[j->seg_start] + matrix[seg_end->j_next] - matrix[j->j_next]
            #                  + internal segment links (same as before)
            # Net gain = savings - (matrix[j->seg_start] + matrix[seg_end->j_next] - matrix[j->j_next])
            actual_gain = savings - (
                matrix[tour[j], tour[seg_start]]
                + matrix[tour[seg_end], tour[j_next]]
                - matrix[tour[j], tour[j_next]]
            )

            if actual_gain > best_gain:
                best_gain = actual_gain
                best_i = i
                best_j = j

    if best_i < 0:
        return None

    # Apply the move: extract segment starting at best_i of length k, insert after best_j
    # Build new tour by removing segment then inserting it
    indices_to_remove = set((best_i + s) % n for s in range(k))
    segment = [tour[(best_i + s) % n] for s in range(k)]
    remaining = [tour[idx] for idx in range(n) if idx not in indices_to_remove]

    # Find where to insert in the remaining tour
    target_node = tour[best_j]
    insert_pos = remaining.index(target_node) + 1
    new_tour = remaining[:insert_pos] + segment + remaining[insert_pos:]

    return new_tour


def _or_opt_improve(
    tour: list[int], matrix: np.ndarray,
    max_iters: int = 100, time_limit: float = 3.0,
) -> list[int]:
    """Apply or-opt-1 then or-opt-2 until convergence or time limit.

    Uses vectorized or-opt-1 (single node relocation) as primary move,
    then tries or-opt-2 (segment relocation) if time remains.
    """
    t0 = time.perf_counter()
    current = tour[:]
    # Phase 1: or-opt-1 (fast, vectorized)
    for _ in range(max_iters):
        if time.perf_counter() - t0 > time_limit * 0.7:
            break
        improved = _or_opt_1_pass(current, matrix)
        if improved is not None:
            current = improved
            continue
        break
    # Phase 2: or-opt-2 if time remains
    remaining = time_limit - (time.perf_counter() - t0)
    if remaining > 0.5:
        for _ in range(max_iters // 2):
            if time.perf_counter() - t0 > time_limit:
                break
            improved = _or_opt_k_pass(current, matrix, k=2)
            if improved is not None:
                current = improved
                continue
            break
    return current


# ---------------------------------------------------------------------------
# Perturbation operators for Iterated Local Search (ILS)
# ---------------------------------------------------------------------------

def _double_bridge_perturb(tour: list[int], rng: np.random.RandomState) -> list[int]:
    """
    Double-bridge perturbation for ATSP.

    Cuts tour into 4 segments at random points and reconnects as
    S1 + S3 + S2 + S4, preserving segment directions (crucial for ATSP).
    This is a standard perturbation for ILS on TSP that effectively escapes
    local optima by creating a non-sequential reconnection.
    """
    n = len(tour)
    if n < 8:
        return tour[:]
    # Pick 3 distinct cut points in [1, n-1]
    cuts = sorted(rng.choice(range(1, n), size=3, replace=False))
    a, b, c = int(cuts[0]), int(cuts[1]), int(cuts[2])
    # Reconnect: S1 + S3 + S2 + S4 (no reversal, safe for ATSP)
    return tour[:a] + tour[b:c] + tour[a:b] + tour[c:]


def _segment_relocate_perturb(
    tour: list[int], rng: np.random.RandomState, strength: int = 3,
) -> list[int]:
    """
    Perturb tour by random segment relocations.

    Each move extracts a short segment (1-3 nodes) and reinserts at a random
    position, preserving segment direction (crucial for ATSP).
    """
    n = len(tour)
    current = tour[:]
    for _ in range(strength):
        seg_len = int(rng.randint(1, min(4, max(2, n // 4)) + 1))
        seg_start = int(rng.randint(0, n))
        # Extract segment (handling wraparound)
        indices_set = set((seg_start + j) % n for j in range(seg_len))
        segment = [current[(seg_start + j) % n] for j in range(seg_len)]
        remaining = [current[i] for i in range(n) if i not in indices_set]
        # Insert at random position
        pos = int(rng.randint(0, len(remaining) + 1))
        current = remaining[:pos] + segment + remaining[pos:]
    return current


def _segment_reversal_perturb(
    tour: list[int], rng: np.random.RandomState, num_reversals: int = 2,
) -> list[int]:
    """
    ATSP-specific perturbation: reverse random segments.

    Unlike symmetric TSP, reversing a segment in ATSP changes costs because
    edge (i->j) != edge (j->i) on real road networks. This exploits the
    asymmetric structure to explore solution space regions that standard
    perturbations (double-bridge, relocate) cannot reach.
    """
    n = len(tour)
    current = tour[:]
    for _ in range(num_reversals):
        seg_len = int(rng.randint(3, max(4, n // 5) + 1))
        start = int(rng.randint(0, n))
        # Get segment indices (handling wraparound)
        indices = [(start + j) % n for j in range(seg_len)]
        values = [current[idx] for idx in indices]
        values.reverse()
        for idx, val in zip(indices, values):
            current[idx] = val
    return current


# ---------------------------------------------------------------------------
# Main hybrid solver
# ---------------------------------------------------------------------------

def solve_hybrid(
    matrix: np.ndarray,
    max_trials: int = 800,
    runs_per_seed: int = 1,
    seed: int = 42,
    time_limit: float = 300.0,
    use_initial_tours: bool = True,
    use_multiconfig: bool = True,
    use_ils: bool = True,
    use_oropt: bool = True,
    ils_perturbation_types: str = "all",
) -> dict:
    """
    Multi-configuration LKH-3 solver with ILS for ATSP on real road networks.

    Phase 1: Generate asymmetry-aware initial tours (fast).
    Phase 2: Warm-start LKH from best initial tours (3% time budget).
    Phase 3: Multi-config LKH with focused ATSP-specific parameters (68% budget).
    Phase 4: Iterated Local Search - perturb best + warm-start LKH (24% budget).
    Phase 5: Or-opt post-processing on best solution (remaining time).

    Ablation controls:
        use_multiconfig: If False, use single default LKH config instead of 5.
        use_ils: If False, skip ILS phase and give all remaining time to Phase 3.
        use_oropt: If False, skip or-opt post-processing.
        ils_perturbation_types: "all" uses all 3 perturbation types,
            "double_bridge_only" uses only double-bridge.
    """
    from src.solvers.lkh_solver import solve_atsp as lkh_solve

    t0 = time.perf_counter()
    n = matrix.shape[0]
    rng = np.random.RandomState(seed)

    # ATSP-specific LKH configurations exploiting population-based crossover,
    # backbone identification, and backtracking search strategies.
    # Key innovations:
    # - POPULATION_SIZE enables LKH-3's internal crossover (IPT) between
    #   diverse solutions, finding better combinations than single-run search.
    # - BACKBONE_TRIALS identifies "fixed" edges appearing in many good
    #   solutions, focusing search on the variable structure.
    # - BACKTRACKING enables deeper exploration of neighborhoods.
    configs = [
        # Config 1: Aggressive patching with population-based crossover
        {"label": "atsp_pop", "max_trials": 1000, "runs": 1, "extra_params": {
            "PATCHING_A": 5, "PATCHING_C": 5, "MOVE_TYPE": 5,
            "MAX_CANDIDATES": 10, "KICKS": 2,
            "POPULATION_SIZE": 5,
        }, "weight": 0.25},
        # Config 2: Deep search with backbone edge identification
        {"label": "deep_backbone", "max_trials": 1200, "runs": 1, "extra_params": {
            "MOVE_TYPE": 5, "MAX_CANDIDATES": 8, "KICKS": 1,
            "SUBGRADIENT": "YES",
            "BACKBONE_TRIALS": 5,
        }, "weight": 0.22},
        # Config 3: Wide candidates with backtracking for thorough local search
        {"label": "wide_bt", "max_trials": 800, "runs": 1, "extra_params": {
            "MAX_CANDIDATES": 15, "PATCHING_A": 4, "PATCHING_C": 4,
            "MOVE_TYPE": 5,
            "BACKTRACKING": "YES",
        }, "weight": 0.20},
        # Config 4: Patching + population for crossover diversity
        {"label": "patching_pop", "extra_params": {
            "PATCHING_A": 3, "PATCHING_C": 3, "KICKS": 1,
            "SUBGRADIENT": "YES",
            "POPULATION_SIZE": 5,
        }, "weight": 0.18},
        # Config 5: Enhanced alpha-values with more ascent candidates
        {"label": "alpha_ascent", "extra_params": {
            "MAX_CANDIDATES": 12, "SUBGRADIENT": "YES",
            "KICKS": 2,
            "ASCENT_CANDIDATES": 10,
        }, "weight": 0.15},
    ]

    population = []
    total_lkh_time = 0.0
    seeds_tried = 0
    warm_starts_tried = 0
    warm_start_used = False

    # Phase 1: Generate initial tours (very fast, < 1s)
    initial_tours = []
    if use_initial_tours:
        try:
            initial_tours = _generate_initial_tours(matrix, seed=seed)
        except Exception as e:
            print(f"  Initial tour generation failed: {e}")

    # Phase 2: Warm-start LKH from best initial tours (2% budget)
    # Reduced from 3%: warm-starts rarely succeed per empirical data
    warm_budget = time_limit * 0.02 if initial_tours else 0
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
            print(f"  Warm-start failed: {e}")
            if not warm_start_used:
                break

    # Phase 3: Multi-config LKH with random seeds
    # If ILS is disabled, give Phase 3 the full remaining time budget
    if use_ils:
        phase3_end = t0 + time_limit * 0.64
        phase3_budget = time_limit * 0.62
    else:
        phase3_end = t0 + time_limit * 0.96
        phase3_budget = time_limit * 0.94

    # Ablation: single config uses just one default LKH config
    if not use_multiconfig:
        configs = [
            {"label": "default", "max_trials": max_trials, "runs": 1, "extra_params": {
                "PATCHING_A": 3, "PATCHING_C": 3, "MOVE_TYPE": 5,
            }, "weight": 1.0},
        ]

    for config in configs:
        config_time = phase3_budget * config["weight"]
        config_start = time.perf_counter()
        c_trials = config.get("max_trials", max_trials)
        c_runs = config.get("runs", runs_per_seed)
        c_extra = config.get("extra_params")

        while True:
            elapsed_config = time.perf_counter() - config_start
            if elapsed_config > config_time or time.perf_counter() > phase3_end:
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

    # Phase 4: Iterated Local Search with adaptive perturbation (32% budget)
    # Three perturbation types including ATSP-specific segment reversal.
    # Adaptive strength: increases when stuck, resets on improvement.
    ils_end = t0 + time_limit * 0.96 if use_ils else t0  # skip if disabled
    ils_extra = {
        "PATCHING_A": 5, "PATCHING_C": 5, "MOVE_TYPE": 5,
        "KICKS": 1, "MAX_CANDIDATES": 10,
    }
    ils_trials = min(max_trials, 500)
    ils_iters = 0
    no_improve_count = 0
    pert_strength = 2  # Adaptive: starts low, grows when stuck

    while time.perf_counter() < ils_end:
        # Choose base: usually best, sometimes from top-3 for diversity
        if ils_iters % 4 == 3 and len(population) >= 3:
            base_idx = int(rng.randint(0, min(3, len(population))))
            base_tour = list(population[base_idx][1])
        else:
            base_tour = best_tour

        # Cycle through perturbation strategies
        if ils_perturbation_types == "double_bridge_only":
            perturbed = _double_bridge_perturb(base_tour, rng)
        else:
            # Full: cycle through 3 types including ATSP-specific reversal
            pert_type = ils_iters % 3
            if pert_type == 0:
                perturbed = _double_bridge_perturb(base_tour, rng)
            elif pert_type == 1:
                perturbed = _segment_relocate_perturb(base_tour, rng, strength=pert_strength)
            else:
                # ATSP-specific: segment reversal changes costs due to asymmetry
                perturbed = _segment_reversal_perturb(base_tour, rng, num_reversals=pert_strength)

        s = int(rng.randint(1, 100000))
        try:
            result = lkh_solve(
                matrix, max_trials=ils_trials, runs=1, seed=s,
                initial_tour=perturbed,
                extra_params=ils_extra,
            )
            if result["cost"] < best_cost - 1e-10:
                best_cost = result["cost"]
                best_tour = list(result["tour"])
                no_improve_count = 0
                pert_strength = max(2, pert_strength - 1)  # Reset on improvement
            else:
                no_improve_count += 1
                if no_improve_count >= 3:
                    pert_strength = min(6, pert_strength + 1)  # Intensify
                    no_improve_count = 0
            population.append((result["cost"], result["tour"]))
            total_lkh_time += result["wall_time"]
            seeds_tried += 1
        except Exception as e:
            print(f"  ILS iteration {ils_iters} failed: {e}")
        ils_iters += 1

    # Re-sort population after ILS
    population.sort(key=lambda x: x[0])

    # Phase 5: Or-opt post-processing on best solution (remaining time)
    remaining = time_limit - (time.perf_counter() - t0)
    if use_oropt and remaining > 0.5:
        try:
            candidate = _or_opt_improve(
                best_tour, matrix,
                max_iters=200, time_limit=min(remaining * 0.9, 5.0),
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
            "use_multiconfig": use_multiconfig,
            "use_ils": use_ils,
            "use_oropt": use_oropt,
            "ils_perturbation_types": ils_perturbation_types,
            "num_configs": len(configs),
            "ils_iters": ils_iters,
        },
    }
