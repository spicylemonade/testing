"""
Baseline heuristic solvers for Asymmetric TSP.

Implements nearest-neighbor, random-insertion, and VROOM solver wrapper.
Each solver conforms to the standard interface:
    Input: numpy distance matrix (n x n)
    Output: dict with keys 'tour' (list[int]), 'cost' (float), 'wall_time' (float)
"""

import time

import numpy as np


def compute_tour_cost(tour: list[int], matrix: np.ndarray) -> float:
    """Compute the total cost of a tour given the distance matrix."""
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += matrix[tour[i], tour[(i + 1) % n]]
    return cost


def nearest_neighbor(matrix: np.ndarray, start: int = 0, seed: int = 42) -> dict:
    """
    Nearest-neighbor heuristic for ATSP.

    Greedily visits the closest unvisited node at each step.
    """
    t0 = time.perf_counter()
    n = matrix.shape[0]
    visited = set()
    tour = [start]
    visited.add(start)

    for _ in range(n - 1):
        current = tour[-1]
        # Find nearest unvisited
        best_next = -1
        best_dist = np.inf
        for j in range(n):
            if j not in visited and matrix[current, j] < best_dist:
                best_dist = matrix[current, j]
                best_next = j
        tour.append(best_next)
        visited.add(best_next)

    wall_time = time.perf_counter() - t0
    cost = compute_tour_cost(tour, matrix)

    return {
        "tour": tour,
        "cost": cost,
        "wall_time": wall_time,
        "n": n,
        "solver": "nearest_neighbor",
        "params": {"start": start},
    }


def nearest_neighbor_best(matrix: np.ndarray, seed: int = 42) -> dict:
    """Run nearest-neighbor from every starting node and return the best tour."""
    t0 = time.perf_counter()
    n = matrix.shape[0]
    best_result = None

    for start in range(n):
        result = nearest_neighbor(matrix, start=start)
        if best_result is None or result["cost"] < best_result["cost"]:
            best_result = result

    best_result["wall_time"] = time.perf_counter() - t0
    best_result["solver"] = "nearest_neighbor_best"
    return best_result


def random_insertion(matrix: np.ndarray, seed: int = 42) -> dict:
    """
    Random-insertion heuristic for ATSP.

    Starts with a triangle of 3 nodes, then randomly inserts remaining nodes
    at the position that minimizes cost increase.
    """
    t0 = time.perf_counter()
    rng = np.random.RandomState(seed)
    n = matrix.shape[0]

    if n < 3:
        tour = list(range(n))
        return {
            "tour": tour,
            "cost": compute_tour_cost(tour, matrix),
            "wall_time": time.perf_counter() - t0,
            "n": n,
            "solver": "random_insertion",
            "params": {"seed": seed},
        }

    # Initialize with 3 random nodes
    initial = rng.choice(n, size=3, replace=False).tolist()
    tour = initial[:]
    remaining = list(set(range(n)) - set(tour))
    rng.shuffle(remaining)

    for node in remaining:
        # Find best insertion position
        best_pos = 0
        best_increase = np.inf
        for pos in range(len(tour)):
            i = tour[pos]
            j = tour[(pos + 1) % len(tour)]
            increase = matrix[i, node] + matrix[node, j] - matrix[i, j]
            if increase < best_increase:
                best_increase = increase
                best_pos = pos + 1

        tour.insert(best_pos, node)

    wall_time = time.perf_counter() - t0
    cost = compute_tour_cost(tour, matrix)

    return {
        "tour": tour,
        "cost": cost,
        "wall_time": wall_time,
        "n": n,
        "solver": "random_insertion",
        "params": {"seed": seed},
    }


def vroom_solver(matrix: np.ndarray, seed: int = 42) -> dict:
    """
    VROOM-based TSP solver using pyvroom.

    Uses VROOM's internal heuristics on a custom duration matrix.
    """
    t0 = time.perf_counter()
    n = matrix.shape[0]

    try:
        import vroom

        # Create VROOM problem with custom matrix
        problem = vroom.Input()

        # Add duration matrix
        int_matrix = np.round(matrix).astype(np.uint32)
        problem.set_durations_matrix(profile="car", matrix_input=int_matrix)

        # Add jobs (stops to visit) — pyvroom uses Job objects
        for i in range(n):
            problem.add_job(vroom.Job(id=i, location=i))

        # Add a vehicle
        problem.add_vehicle(
            vroom.Vehicle(id=0, start=0, end=0, profile="car")
        )

        # Solve
        solution = problem.solve(exploration_level=5, nb_threads=1)

        # Extract tour from solution routes DataFrame
        routes_df = solution.routes
        job_rows = routes_df[routes_df["type"] == "job"]
        tour = job_rows["id"].tolist()

        wall_time = time.perf_counter() - t0
        cost = compute_tour_cost(tour, matrix)

        return {
            "tour": tour,
            "cost": cost,
            "wall_time": wall_time,
            "n": n,
            "solver": "vroom",
            "params": {"exploration_level": 5},
        }
    except ImportError:
        raise ImportError("pyvroom not installed. Install with: pip install pyvroom")
    except Exception as e:
        wall_time = time.perf_counter() - t0
        raise RuntimeError(f"VROOM solver failed: {e}")


# Standard solver interface mapping
SOLVERS = {
    "nearest_neighbor": nearest_neighbor,
    "nearest_neighbor_best": nearest_neighbor_best,
    "random_insertion": random_insertion,
    "vroom": vroom_solver,
}


if __name__ == "__main__":
    import json
    import sys

    # Test all solvers on manhattan_75
    benchmark_file = "data/benchmarks/manhattan_75.json"
    if len(sys.argv) > 1:
        benchmark_file = sys.argv[1]

    print(f"Testing baseline solvers on {benchmark_file}")
    with open(benchmark_file) as f:
        instance = json.load(f)

    matrix = np.array(instance["duration_matrix"])
    print(f"Instance: {instance['name']}, n={matrix.shape[0]}")
    print()

    results = {}
    for name, solver_fn in SOLVERS.items():
        try:
            result = solver_fn(matrix, seed=42)
            results[name] = result
            print(f"{name:25s}: cost={result['cost']:12.1f}s  time={result['wall_time']:.4f}s")
        except Exception as e:
            print(f"{name:25s}: ERROR - {e}")

    # Compare with LKH
    print()
    print("Comparison with LKH-3 (from item_009):")
    print(f"  LKH-3 cost: 15767.9s (reference)")
    for name, result in results.items():
        gap = (result["cost"] / 15767.9 - 1) * 100
        print(f"  {name}: {result['cost']:.1f}s  (gap: +{gap:.2f}%)")
