"""
Asymmetry-Exploiting Iterated Local Search (AE-ILS) for ATSP on road networks.

Hybrid approach combining:
1. Multi-seed LKH-3 for solution diversity (different local optima)
2. Asymmetric local search operators (or-opt, node swap, asym-2opt)
3. Edge-frequency guided construction from population of LKH solutions
4. Iterated perturbation with asymmetry-guided double-bridge

The key insight is that LKH-3's Jonker-Volgenant ATSP→STSP transformation
loses directional cost information. By collecting diverse LKH solutions and
applying ATSP-native operators, we can escape LKH's local optima.

References:
- Helsgott (2017) LKH-3 via J-V transformation [helsgott2017]
- Nagata & Kobayashi (2013) EAX crossover for TSP [nagata2013]
- Vu et al. (2019) Bounded asymmetry in road networks [vu2019]
"""

import time
from typing import Optional

import numpy as np


def compute_tour_cost(tour: list[int], matrix: np.ndarray) -> float:
    """Compute total directed tour cost."""
    n = len(tour)
    cost = 0.0
    for i in range(n):
        cost += matrix[tour[i], tour[(i + 1) % n]]
    return cost


# ---------------------------------------------------------------------------
# Local search operators
# ---------------------------------------------------------------------------

def _or_opt_1_pass(tour: list[int], matrix: np.ndarray) -> bool:
    """Find and apply the best single-node relocation."""
    n = len(tour)
    best_gain = 1e-10
    best_remove = -1
    best_insert = -1

    for i in range(n):
        p = tour[(i - 1) % n]
        c = tour[i]
        s = tour[(i + 1) % n]
        saving = matrix[p, c] + matrix[c, s] - matrix[p, s]

        for j in range(n):
            if j == i or j == (i - 1) % n:
                continue
            a = tour[j]
            b = tour[(j + 1) % n]
            if b == c:
                continue
            cost = matrix[a, c] + matrix[c, b] - matrix[a, b]
            gain = saving - cost
            if gain > best_gain:
                best_gain = gain
                best_remove = i
                best_insert = j

    if best_remove >= 0:
        node = tour.pop(best_remove)
        ins = best_insert - (1 if best_insert > best_remove else 0)
        tour.insert(ins + 1, node)
        return True
    return False


def _or_opt_k_pass(tour: list[int], matrix: np.ndarray, k: int) -> bool:
    """Find and apply the best k-node segment relocation (no reversal)."""
    n = len(tour)
    if k >= n - 1:
        return False

    best_gain = 1e-10
    best_start = -1
    best_insert = -1

    for i in range(n - k + 1):
        seg_first = tour[i]
        seg_last = tour[i + k - 1]
        pred = tour[(i - 1) % n]
        succ = tour[(i + k) % n]
        saving = (
            matrix[pred, seg_first]
            + matrix[seg_last, succ]
            - matrix[pred, succ]
        )

        for j in range(n):
            if i - 1 <= j < i + k:
                continue
            a = tour[j]
            b = tour[(j + 1) % n]
            if i <= (j + 1) % n < i + k:
                continue
            cost = matrix[a, seg_first] + matrix[seg_last, b] - matrix[a, b]
            gain = saving - cost
            if gain > best_gain:
                best_gain = gain
                best_start = i
                best_insert = j

    if best_start >= 0:
        seg = tour[best_start:best_start + k]
        del tour[best_start:best_start + k]
        ins = best_insert
        if ins >= best_start + k:
            ins -= k
        for off, nd in enumerate(seg):
            tour.insert(ins + 1 + off, nd)
        return True
    return False


def _node_swap_pass(tour: list[int], matrix: np.ndarray) -> bool:
    """Find and apply the best swap of two non-adjacent nodes."""
    n = len(tour)
    best_gain = 1e-10
    best_i = -1
    best_j = -1

    for i in range(n):
        pi = tour[(i - 1) % n]
        ci = tour[i]
        si = tour[(i + 1) % n]

        for j in range(i + 2, n):
            if j == (i - 1) % n or (j + 1) % n == i:
                continue
            pj = tour[(j - 1) % n]
            cj = tour[j]
            sj = tour[(j + 1) % n]
            if pj == ci or sj == ci or pi == cj or si == cj:
                continue

            old = (
                matrix[pi, ci] + matrix[ci, si]
                + matrix[pj, cj] + matrix[cj, sj]
            )
            new = (
                matrix[pi, cj] + matrix[cj, si]
                + matrix[pj, ci] + matrix[ci, sj]
            )
            gain = old - new
            if gain > best_gain:
                best_gain = gain
                best_i = i
                best_j = j

    if best_i >= 0:
        tour[best_i], tour[best_j] = tour[best_j], tour[best_i]
        return True
    return False


def _asym_2opt_pass(tour: list[int], matrix: np.ndarray) -> bool:
    """
    Asymmetric 2-opt: reverse a segment, accounting for changed costs
    due to asymmetry. In road networks, the reversed direction can be cheaper.
    """
    n = len(tour)
    best_gain = 1e-10
    best_i = -1
    best_j = -1

    for i in range(n - 2):
        for j in range(i + 2, min(i + 50, n)):  # limit range for speed
            if j == n - 1 and i == 0:
                continue

            # Edges being removed
            old_e = matrix[tour[i], tour[i + 1]] + matrix[tour[j], tour[(j + 1) % n]]
            # Edges being added
            new_e = matrix[tour[i], tour[j]] + matrix[tour[i + 1], tour[(j + 1) % n]]

            # Segment cost change: forward vs reversed
            seg_fwd = sum(matrix[tour[k], tour[k + 1]] for k in range(i + 1, j))
            seg_rev = sum(matrix[tour[k + 1], tour[k]] for k in range(i + 1, j))

            gain = (old_e + seg_fwd) - (new_e + seg_rev)
            if gain > best_gain:
                best_gain = gain
                best_i = i
                best_j = j

    if best_i >= 0:
        tour[best_i + 1:best_j + 1] = tour[best_i + 1:best_j + 1][::-1]
        return True
    return False


def _local_search(tour: list[int], matrix: np.ndarray, time_limit: float = 30.0) -> list[int]:
    """Apply all operators until no improvement."""
    t0 = time.perf_counter()
    for _ in range(200):
        if time.perf_counter() - t0 > time_limit:
            break
        if _or_opt_1_pass(tour, matrix):
            continue
        if _or_opt_k_pass(tour, matrix, k=2):
            continue
        if _or_opt_k_pass(tour, matrix, k=3):
            continue
        if _node_swap_pass(tour, matrix):
            continue
        if _asym_2opt_pass(tour, matrix):
            continue
        break
    return tour


# ---------------------------------------------------------------------------
# Perturbation strategies
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
    ratios = []
    for i in range(n):
        a, b = tour[i], tour[(i + 1) % n]
        fwd, bwd = matrix[a, b], matrix[b, a]
        ratio = max(fwd, bwd) / (min(fwd, bwd) + 1e-10)
        ratios.append((ratio, i))
    ratios.sort(reverse=True)

    top = [r[1] for r in ratios[:min(8, len(ratios))]]
    if len(top) < 3:
        return _double_bridge(tour, rng)

    chosen = sorted(rng.choice(top, size=3, replace=False))
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
# Edge-frequency guided construction (from population of solutions)
# ---------------------------------------------------------------------------

def _build_freq_matrix(tours: list[list[int]], n: int) -> np.ndarray:
    """Build directed edge frequency matrix from a population of tours."""
    freq = np.zeros((n, n), dtype=np.float64)
    for tour in tours:
        m = len(tour)
        for i in range(m):
            freq[tour[i], tour[(i + 1) % m]] += 1
    return freq


def _greedy_from_frequencies(
    freq: np.ndarray, matrix: np.ndarray, alpha: float = 0.5
) -> list[int]:
    """
    Construct a tour using edge frequencies as guidance.
    Score = alpha * normalized_freq + (1 - alpha) * (1 / normalized_cost)
    """
    n = freq.shape[0]
    max_freq = freq.max() + 1e-10
    max_cost = matrix.max() + 1e-10

    # Start from node 0
    tour = [0]
    visited = {0}

    for _ in range(n - 1):
        current = tour[-1]
        best_score = -np.inf
        best_next = -1

        for j in range(n):
            if j in visited:
                continue
            f_score = freq[current, j] / max_freq
            c_score = 1.0 - matrix[current, j] / max_cost
            score = alpha * f_score + (1 - alpha) * c_score
            if score > best_score:
                best_score = score
                best_next = j

        if best_next < 0:
            # Shouldn't happen, but fallback
            remaining = list(set(range(n)) - visited)
            best_next = remaining[0]

        tour.append(best_next)
        visited.add(best_next)

    return tour


# ---------------------------------------------------------------------------
# Main solver: AE-ILS with population
# ---------------------------------------------------------------------------

def solve_ae_ils(
    matrix: np.ndarray,
    initial_tour: Optional[list[int]] = None,
    max_iterations: int = 100,
    max_no_improve: int = 30,
    seed: int = 42,
    time_limit: float = 120.0,
) -> dict:
    """Asymmetry-Exploiting Iterated Local Search."""
    t0 = time.perf_counter()
    rng = np.random.RandomState(seed)
    n = matrix.shape[0]

    if initial_tour is not None:
        tour = list(initial_tour)
    else:
        tour = list(range(n))

    initial_cost = compute_tour_cost(tour, matrix)

    # Initial local search
    tour = _local_search(tour, matrix, time_limit=min(time_limit * 0.3, 30.0))
    best_tour = tour[:]
    best_cost = compute_tour_cost(best_tour, matrix)

    no_improve = 0
    improvements = 0
    iteration = 0

    for iteration in range(max_iterations):
        if time.perf_counter() - t0 > time_limit or no_improve >= max_no_improve:
            break

        if iteration % 3 == 0:
            perturbed = _asymmetry_guided_perturb(best_tour[:], matrix, rng)
        else:
            perturbed = _double_bridge(best_tour[:], rng)

        remaining = time_limit - (time.perf_counter() - t0)
        if remaining < 0.5:
            break
        perturbed = _local_search(perturbed, matrix, time_limit=min(remaining * 0.5, 15.0))
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
        "initial_cost": initial_cost,
        "wall_time": time.perf_counter() - t0,
        "n": n,
        "solver": "ae_ils",
        "iterations": iteration + 1 if max_iterations > 0 else 0,
        "improvements": improvements,
    }


# ---------------------------------------------------------------------------
# Hybrid solver: Multi-seed LKH + Edge-Frequency + AE-ILS
# ---------------------------------------------------------------------------

def solve_hybrid(
    matrix: np.ndarray,
    max_trials: int = 500,
    runs: int = 5,
    num_seeds: int = 5,
    ils_iterations: int = 50,
    ils_no_improve: int = 20,
    seed: int = 42,
    time_limit: float = 600.0,
) -> dict:
    """
    Hybrid solver for ATSP on real road networks.

    Phase 1: Run LKH-3 with multiple seeds for solution diversity.
    Phase 2: Build edge-frequency matrix from population, construct
             new candidates using frequency-guided greedy.
    Phase 3: Apply AE-ILS to best candidates with asymmetric operators
             and asymmetry-guided perturbation.
    """
    from src.solvers.lkh_solver import solve_atsp as lkh_solve

    t0 = time.perf_counter()
    n = matrix.shape[0]

    # Phase 1: Collect diverse LKH solutions
    base_rng = np.random.RandomState(seed)
    seeds = [int(base_rng.randint(1, 100000)) for _ in range(num_seeds)]

    population = []  # (cost, tour)
    total_lkh_time = 0.0

    for s in seeds:
        if time.perf_counter() - t0 > time_limit * 0.7:
            break
        lkh_result = lkh_solve(matrix, max_trials=max_trials, runs=runs, seed=s)
        total_lkh_time += lkh_result["wall_time"]
        population.append((lkh_result["cost"], lkh_result["tour"]))

    population.sort(key=lambda x: x[0])
    lkh_best_cost = population[0][0]
    best_cost = lkh_best_cost
    best_tour = list(population[0][1])

    # Phase 2: Edge-frequency guided construction
    if len(population) >= 2:
        freq = _build_freq_matrix([t for _, t in population], n)
        for alpha in [0.3, 0.5, 0.7]:
            if time.perf_counter() - t0 > time_limit * 0.8:
                break
            candidate = _greedy_from_frequencies(freq, matrix, alpha=alpha)
            remaining = time_limit - (time.perf_counter() - t0)
            candidate = _local_search(candidate, matrix, time_limit=min(remaining * 0.1, 15.0))
            c = compute_tour_cost(candidate, matrix)
            if c < best_cost - 1e-10:
                best_cost = c
                best_tour = candidate

    # Phase 3: AE-ILS on best solution
    remaining = time_limit - (time.perf_counter() - t0)
    if remaining > 5.0:
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

    # Also try AE-ILS on other population members
    for _, pop_tour in population[1:3]:
        remaining = time_limit - (time.perf_counter() - t0)
        if remaining < 5.0:
            break
        ils_r = solve_ae_ils(
            matrix,
            initial_tour=list(pop_tour),
            max_iterations=max(ils_iterations // 2, 10),
            max_no_improve=max(ils_no_improve // 2, 5),
            seed=seed + 1,
            time_limit=min(remaining * 0.3, 30.0),
        )
        if ils_r["cost"] < best_cost - 1e-10:
            best_cost = ils_r["cost"]
            best_tour = ils_r["tour"]

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
        "params": {
            "lkh_max_trials": max_trials,
            "lkh_runs": runs,
            "num_seeds": num_seeds,
            "ils_iterations": ils_iterations,
            "ils_no_improve": ils_no_improve,
            "seed": seed,
        },
    }
