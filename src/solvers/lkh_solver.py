"""
LKH-3 solver wrapper for Asymmetric TSP instances.

Converts numpy distance matrices to TSPLIB ATSP format, runs the LKH-3 binary,
and parses the output tour back into Python.
"""

import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

# Default LKH binary path
LKH_BINARY = os.environ.get(
    "LKH_PATH",
    str(Path(__file__).parent.parent.parent / "bin" / "LKH"),
)

# Scale factor: LKH uses integer distances, so we multiply float durations
SCALE_FACTOR = 1000  # 0.001 second precision for finer LKH discrimination


def matrix_to_tsplib_atsp(matrix: np.ndarray, name: str = "instance") -> str:
    """Convert a numpy distance matrix to TSPLIB ATSP format string."""
    n = matrix.shape[0]
    # Scale to integers for LKH
    int_matrix = np.round(matrix * SCALE_FACTOR).astype(np.int64)
    # Set diagonal to 0 (no self-loops)
    np.fill_diagonal(int_matrix, 0)
    # Use large value for infinity
    int_matrix = np.where(int_matrix < 0, 99999999, int_matrix)

    lines = [
        f"NAME: {name}",
        "TYPE: ATSP",
        f"DIMENSION: {n}",
        "EDGE_WEIGHT_TYPE: EXPLICIT",
        "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
        "EDGE_WEIGHT_SECTION",
    ]
    for i in range(n):
        row_str = " ".join(str(int(v)) for v in int_matrix[i])
        lines.append(row_str)
    lines.append("EOF")
    return "\n".join(lines)


def _write_initial_tour_file(tour_0indexed: list, n: int, filepath: str):
    """Write TSPLIB tour file for LKH initial tour (n-node, 1-indexed)."""
    lines = [
        "NAME: initial",
        "TYPE: TOUR",
        f"DIMENSION: {n}",
        "TOUR_SECTION",
    ]
    for node in tour_0indexed:
        lines.append(str(node + 1))
    lines.append("-1")
    lines.append("EOF")
    with open(filepath, "w") as f:
        f.write("\n".join(lines))


def write_par_file(
    problem_file: str,
    tour_file: str,
    max_trials: int = 1000,
    runs: int = 5,
    time_limit: float = 0,
    seed: int = 42,
    initial_tour_file: str = None,
    extra_params: dict = None,
) -> str:
    """Generate LKH-3 parameter file content."""
    lines = [
        f"PROBLEM_FILE = {problem_file}",
        f"OUTPUT_TOUR_FILE = {tour_file}",
        f"MAX_TRIALS = {max_trials}",
        f"RUNS = {runs}",
        f"SEED = {seed}",
    ]
    if time_limit > 0:
        lines.append(f"TIME_LIMIT = {time_limit}")
    if initial_tour_file:
        lines.append(f"INITIAL_TOUR_FILE = {initial_tour_file}")
    if extra_params:
        for k, v in extra_params.items():
            lines.append(f"{k} = {v}")
    return "\n".join(lines)


def parse_tour_file(tour_file: str) -> tuple[list[int], int]:
    """
    Parse LKH output tour file.

    Returns
    -------
    tour : list of int
        0-indexed tour as ordered list of node indices.
    cost : int
        Tour cost as reported by LKH (in scaled integer units).
    """
    with open(tour_file) as f:
        content = f.read()

    # Extract tour cost from header
    cost_match = re.search(r"COMMENT\s*:\s*Length\s*=\s*(\d+)", content)
    cost = int(cost_match.group(1)) if cost_match else -1

    # Extract dimension
    dim_match = re.search(r"DIMENSION\s*:\s*(\d+)", content)
    n = int(dim_match.group(1)) if dim_match else 0

    # Extract tour (between TOUR_SECTION and -1)
    tour_match = re.search(r"TOUR_SECTION\s*\n([\s\S]*?)\s*-1", content)
    if not tour_match:
        raise ValueError(f"Could not parse tour from {tour_file}")

    tour_1indexed = [int(x.strip()) for x in tour_match.group(1).strip().split("\n") if x.strip()]
    # Convert to 0-indexed
    tour = [x - 1 for x in tour_1indexed]

    return tour, cost


def compute_tour_cost(tour: list[int], matrix: np.ndarray) -> float:
    """Compute the actual tour cost from the distance matrix."""
    cost = 0.0
    for i in range(len(tour)):
        j = (i + 1) % len(tour)
        cost += matrix[tour[i], tour[j]]
    return cost


def solve_atsp(
    matrix: np.ndarray,
    max_trials: int = 1000,
    runs: int = 5,
    time_limit: float = 0,
    seed: int = 42,
    lkh_binary: str = LKH_BINARY,
    verbose: bool = False,
    initial_tour: list = None,
    extra_params: dict = None,
) -> dict:
    """
    Solve an ATSP instance using LKH-3.

    Parameters
    ----------
    matrix : np.ndarray
        Asymmetric distance/duration matrix of shape (n, n).
    max_trials : int
        Maximum number of trials per run.
    runs : int
        Number of independent runs.
    time_limit : float
        Time limit in seconds (0 = unlimited).
    seed : int
        Random seed for LKH.
    lkh_binary : str
        Path to LKH-3 binary.
    verbose : bool
        Print LKH output.

    Returns
    -------
    dict with keys: tour, cost, lkh_cost, wall_time, n
    """
    if not os.path.isfile(lkh_binary):
        raise FileNotFoundError(f"LKH binary not found at {lkh_binary}")

    n = matrix.shape[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        problem_file = os.path.join(tmpdir, "instance.atsp")
        tour_file = os.path.join(tmpdir, "tour.txt")
        par_file = os.path.join(tmpdir, "params.par")

        # Write TSPLIB ATSP file
        tsplib_content = matrix_to_tsplib_atsp(matrix, name="benchmark")
        with open(problem_file, "w") as f:
            f.write(tsplib_content)

        # Write initial tour file if provided
        initial_tour_file_path = None
        if initial_tour is not None:
            initial_tour_file_path = os.path.join(tmpdir, "initial.tour")
            _write_initial_tour_file(initial_tour, n, initial_tour_file_path)

        # Write parameter file
        par_content = write_par_file(
            problem_file, tour_file, max_trials, runs, time_limit, seed,
            initial_tour_file=initial_tour_file_path,
            extra_params=extra_params,
        )
        with open(par_file, "w") as f:
            f.write(par_content)

        # Run LKH
        t0 = time.perf_counter()
        try:
            result = subprocess.run(
                [lkh_binary, par_file],
                capture_output=True,
                text=True,
                timeout=max(time_limit * 2, 300) if time_limit > 0 else 600,
            )
            wall_time = time.perf_counter() - t0

            if verbose:
                print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)

            if result.returncode != 0:
                raise RuntimeError(f"LKH failed with code {result.returncode}: {result.stderr}")
        except subprocess.TimeoutExpired:
            wall_time = time.perf_counter() - t0
            raise RuntimeError(f"LKH timed out after {wall_time:.1f}s")

        # Parse tour
        if not os.path.isfile(tour_file):
            raise RuntimeError(f"LKH did not produce tour file. stdout: {result.stdout[-200:]}")

        tour, lkh_cost = parse_tour_file(tour_file)

    # Compute actual cost from original matrix
    actual_cost = compute_tour_cost(tour, matrix)

    return {
        "tour": tour,
        "cost": actual_cost,
        "lkh_cost_scaled": lkh_cost,
        "wall_time": wall_time,
        "n": n,
        "solver": "lkh3",
        "params": {
            "max_trials": max_trials,
            "runs": runs,
            "time_limit": time_limit,
            "seed": seed,
        },
    }


if __name__ == "__main__":
    import json
    import sys

    # Test on a small benchmark instance
    benchmark_file = "data/benchmarks/manhattan_75.json"
    if len(sys.argv) > 1:
        benchmark_file = sys.argv[1]

    print(f"Testing LKH-3 wrapper on {benchmark_file}")
    with open(benchmark_file) as f:
        instance = json.load(f)

    matrix = np.array(instance["duration_matrix"])
    n = matrix.shape[0]
    print(f"Instance: {instance['name']}, n={n}")

    result = solve_atsp(matrix, max_trials=100, runs=1, seed=42)
    print(f"Tour cost: {result['cost']:.1f}s")
    print(f"LKH cost (scaled): {result['lkh_cost_scaled']}")
    print(f"Wall time: {result['wall_time']:.2f}s")
    print(f"Tour length: {len(result['tour'])} nodes")

    # Verify: manually compute tour cost
    manual_cost = sum(
        matrix[result["tour"][i], result["tour"][(i + 1) % n]]
        for i in range(n)
    )
    print(f"Manual cost verification: {manual_cost:.1f}s")
    print(f"Match: {abs(manual_cost - result['cost']) < 0.01}")
