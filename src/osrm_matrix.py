"""
OSRM-based asymmetric distance/duration matrix generator.

Queries the OSRM Table API to compute full n x n asymmetric duration matrices
for a given list of (longitude, latitude) coordinates. Supports batching for
large coordinate sets (>100 points) via source/destination slicing.
"""

import argparse
import json
import math
import time
from typing import Optional

import numpy as np
import requests


DEFAULT_OSRM_URL = "https://router.project-osrm.org"
MAX_TABLE_SIZE = 100  # OSRM public server limit per dimension


def _build_coords_string(coords: list[tuple[float, float]]) -> str:
    """Convert list of (lon, lat) tuples to OSRM coordinate string."""
    return ";".join(f"{lon},{lat}" for lon, lat in coords)


def _query_table(
    osrm_url: str,
    coords: list[tuple[float, float]],
    sources: Optional[list[int]] = None,
    destinations: Optional[list[int]] = None,
    profile: str = "driving",
    annotations: str = "duration",
    timeout: float = 60.0,
    retry_count: int = 3,
    retry_delay: float = 2.0,
) -> dict:
    """Query OSRM Table API with retry logic."""
    coords_str = _build_coords_string(coords)
    url = f"{osrm_url}/table/v1/{profile}/{coords_str}"
    params = {"annotations": annotations}
    if sources is not None:
        params["sources"] = ";".join(str(s) for s in sources)
    if destinations is not None:
        params["destinations"] = ";".join(str(d) for d in destinations)

    for attempt in range(retry_count):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != "Ok":
                raise ValueError(f"OSRM error: {data.get('code')} - {data.get('message', '')}")
            return data
        except (requests.RequestException, ValueError) as e:
            if attempt < retry_count - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                raise RuntimeError(f"OSRM query failed after {retry_count} attempts: {e}")


def get_duration_matrix(
    coords: list[tuple[float, float]],
    osrm_url: str = DEFAULT_OSRM_URL,
    profile: str = "driving",
    batch_size: int = MAX_TABLE_SIZE,
    timeout: float = 60.0,
) -> np.ndarray:
    """
    Compute full asymmetric duration matrix via OSRM Table API.

    Parameters
    ----------
    coords : list of (lon, lat) tuples
        Geographic coordinates for all stops.
    osrm_url : str
        Base URL of the OSRM server.
    profile : str
        Routing profile (driving, walking, cycling).
    batch_size : int
        Maximum number of sources or destinations per API call.
    timeout : float
        HTTP request timeout in seconds.

    Returns
    -------
    np.ndarray
        Asymmetric duration matrix of shape (n, n) in seconds.
        Entry [i, j] is the travel time from coords[i] to coords[j].
    """
    n = len(coords)
    if n < 2:
        raise ValueError("Need at least 2 coordinates")

    # Small enough for single query
    if n <= batch_size:
        data = _query_table(osrm_url, coords, profile=profile, timeout=timeout)
        matrix = np.array(data["durations"], dtype=np.float64)
        # Replace None values (unreachable) with infinity
        matrix = np.where(matrix == None, np.inf, matrix)
        return matrix

    # Batch mode: send subsets of coordinates per query to avoid URL length limits.
    # Each query contains only the union of source and destination coordinates.
    matrix = np.zeros((n, n), dtype=np.float64)
    half = batch_size // 2  # Split batch between sources and destinations

    for src_start in range(0, n, half):
        src_end = min(src_start + half, n)
        src_global = list(range(src_start, src_end))

        for dst_start in range(0, n, half):
            dst_end = min(dst_start + half, n)
            dst_global = list(range(dst_start, dst_end))

            # Build the subset of coordinates (union of src and dst)
            # Use an ordered set to avoid duplicates
            idx_set = list(dict.fromkeys(src_global + dst_global))
            sub_coords = [coords[i] for i in idx_set]

            # Map global indices to local indices in sub_coords
            global_to_local = {g: l for l, g in enumerate(idx_set)}
            local_sources = [global_to_local[g] for g in src_global]
            local_dests = [global_to_local[g] for g in dst_global]

            data = _query_table(
                osrm_url,
                sub_coords,
                sources=local_sources,
                destinations=local_dests,
                profile=profile,
                timeout=timeout,
            )
            sub_matrix = np.array(data["durations"], dtype=np.float64)
            matrix[src_start:src_end, dst_start:dst_end] = sub_matrix

            # Rate limiting for public server
            time.sleep(0.5)

    # Replace None/null with infinity
    matrix = np.where(np.isnan(matrix), np.inf, matrix)
    return matrix


def compute_asymmetry_stats(matrix: np.ndarray) -> dict:
    """Compute asymmetry statistics for a distance matrix."""
    n = matrix.shape[0]
    asym_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i, j] > 0 and matrix[j, i] > 0:
                ratio = max(matrix[i, j], matrix[j, i]) / min(matrix[i, j], matrix[j, i])
                asym_pairs.append(ratio)

    if not asym_pairs:
        return {"mean_ratio": 1.0, "max_ratio": 1.0, "asymmetric_pairs_pct": 0.0}

    asym_pairs = np.array(asym_pairs)
    num_asymmetric = np.sum(np.abs(asym_pairs - 1.0) > 0.01)  # >1% difference

    return {
        "mean_ratio": float(np.mean(asym_pairs)),
        "max_ratio": float(np.max(asym_pairs)),
        "median_ratio": float(np.median(asym_pairs)),
        "asymmetric_pairs_pct": float(num_asymmetric / len(asym_pairs) * 100),
        "num_pairs_checked": len(asym_pairs),
    }


def generate_random_coords_in_bbox(
    n: int,
    bbox: tuple[float, float, float, float],
    seed: int = 42,
) -> list[tuple[float, float]]:
    """
    Generate n random (lon, lat) coordinates within a bounding box.

    Parameters
    ----------
    n : int
        Number of coordinates to generate.
    bbox : tuple
        (min_lon, min_lat, max_lon, max_lat) bounding box.
    seed : int
        Random seed for reproducibility.
    """
    rng = np.random.RandomState(seed)
    min_lon, min_lat, max_lon, max_lat = bbox
    lons = rng.uniform(min_lon, max_lon, n)
    lats = rng.uniform(min_lat, max_lat, n)
    return [(float(lon), float(lat)) for lon, lat in zip(lons, lats)]


# City bounding boxes for benchmark generation
CITY_BBOXES = {
    # Grid-layout cities
    "manhattan": (-74.02, 40.70, -73.93, 40.80),
    "chicago": (-87.75, 41.83, -87.60, 41.95),
    "barcelona": (2.10, 41.36, 2.22, 41.42),
    # Organic European cities
    "paris": (2.25, 48.82, 2.42, 48.90),
    "rome": (12.42, 41.86, 12.54, 41.94),
    "london": (-0.18, 51.48, 0.02, 51.54),
    # Mixed suburban-urban
    "berlin": (13.30, 52.46, 13.50, 52.56),
    "los_angeles": (-118.35, 33.95, -118.15, 34.10),
    "tokyo": (139.65, 35.63, 139.80, 35.73),
}


def demo_50_points():
    """Demonstrate generating a 50-point asymmetric matrix from Manhattan."""
    print("=== OSRM Asymmetric Distance Matrix Demo ===")
    print("Generating 50 random points in Manhattan...")

    coords = generate_random_coords_in_bbox(50, CITY_BBOXES["manhattan"], seed=42)
    print(f"Generated {len(coords)} coordinates")
    print(f"Sample: {coords[0]}, {coords[1]}, ...")

    print("\nQuerying OSRM Table API...")
    matrix = get_duration_matrix(coords)
    print(f"Matrix shape: {matrix.shape}")
    print(f"Matrix dtype: {matrix.dtype}")

    # Check asymmetry
    stats = compute_asymmetry_stats(matrix)
    print(f"\n=== Asymmetry Statistics ===")
    print(f"Mean asymmetry ratio: {stats['mean_ratio']:.4f}")
    print(f"Max asymmetry ratio: {stats['max_ratio']:.4f}")
    print(f"Median asymmetry ratio: {stats['median_ratio']:.4f}")
    print(f"Pairs with >1% asymmetry: {stats['asymmetric_pairs_pct']:.1f}%")

    # Show a few example asymmetric pairs
    print(f"\n=== Sample Asymmetric Pairs ===")
    for i in range(min(5, len(coords))):
        j = (i + 1) % len(coords)
        print(f"  [{i}]->[{j}]: {matrix[i,j]:.1f}s  vs  [{j}]->[{i}]: {matrix[j,i]:.1f}s  "
              f"(ratio: {max(matrix[i,j], matrix[j,i]) / max(min(matrix[i,j], matrix[j,i]), 0.1):.2f})")

    return coords, matrix, stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OSRM Asymmetric Distance Matrix Generator")
    parser.add_argument("--demo", action="store_true", help="Run 50-point Manhattan demo")
    parser.add_argument("--city", type=str, choices=list(CITY_BBOXES.keys()),
                        help="City for coordinate generation")
    parser.add_argument("--n", type=int, default=50, help="Number of points")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--osrm-url", type=str, default=DEFAULT_OSRM_URL, help="OSRM server URL")
    parser.add_argument("--output", type=str, help="Output JSON file path")

    args = parser.parse_args()

    if args.demo:
        coords, matrix, stats = demo_50_points()
    elif args.city:
        coords = generate_random_coords_in_bbox(args.n, CITY_BBOXES[args.city], seed=args.seed)
        matrix = get_duration_matrix(coords, osrm_url=args.osrm_url)
        stats = compute_asymmetry_stats(matrix)
        print(f"Generated {args.n}-point matrix for {args.city}")
        print(f"Asymmetry: mean={stats['mean_ratio']:.4f}, max={stats['max_ratio']:.4f}")

        if args.output:
            output = {
                "city": args.city,
                "n": args.n,
                "seed": args.seed,
                "coords": coords,
                "duration_matrix": matrix.tolist(),
                "asymmetry_stats": stats,
            }
            with open(args.output, "w") as f:
                json.dump(output, f)
            print(f"Saved to {args.output}")
    else:
        parser.print_help()
