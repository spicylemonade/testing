"""
Generate benchmark ATSP instances from real road network data via OSRM.

Creates instances across 3 size categories and 3 geographic types:
- Small (50-100): direct OSRM queries
- Medium (200-500): batched OSRM queries
- Large (500-1000): OSRM sample + synthetic scaling preserving asymmetry properties

All instances saved as JSON in data/benchmarks/.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.osrm_matrix import (
    CITY_BBOXES,
    compute_asymmetry_stats,
    generate_random_coords_in_bbox,
    get_duration_matrix,
)

BENCHMARKS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "benchmarks")
SEED = 42


def save_instance(name, coords, matrix, city, city_type, metadata=None):
    """Save a benchmark instance as JSON."""
    stats = compute_asymmetry_stats(matrix)
    instance = {
        "name": name,
        "city": city,
        "city_type": city_type,
        "n": len(coords),
        "coords": coords,
        "duration_matrix": matrix.tolist(),
        "asymmetry_stats": stats,
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "osrm_version": "public_demo",
            "seed": SEED,
            **(metadata or {}),
        },
    }
    filepath = os.path.join(BENCHMARKS_DIR, f"{name}.json")
    with open(filepath, "w") as f:
        json.dump(instance, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  Saved {filepath} ({instance['n']} nodes, {size_mb:.2f} MB, "
          f"asym_mean={stats['mean_ratio']:.4f}, asym_max={stats['max_ratio']:.4f})")
    return instance


def generate_osrm_instance(city, n, city_type, name_suffix=""):
    """Generate an instance by querying OSRM directly."""
    name = f"{city}_{n}{name_suffix}"
    print(f"Generating {name} ({n} nodes in {city})...")
    coords = generate_random_coords_in_bbox(n, CITY_BBOXES[city], seed=SEED + n)
    matrix = get_duration_matrix(coords, batch_size=100, timeout=60)
    return save_instance(name, coords, matrix, city, city_type)


def generate_scaled_instance(city, target_n, city_type, base_n=100, name_suffix=""):
    """
    Generate a large instance by sampling a base from OSRM and scaling.

    Strategy: Query a base_n-point OSRM matrix to learn the city's distance
    distribution and asymmetry patterns, then extrapolate to target_n points
    using geographic interpolation and realistic noise.
    """
    name = f"{city}_{target_n}{name_suffix}"
    print(f"Generating {name} ({target_n} nodes in {city}, base={base_n})...")

    bbox = CITY_BBOXES[city]
    rng = np.random.RandomState(SEED + target_n)

    # Step 1: Get real OSRM data for base sample
    base_coords = generate_random_coords_in_bbox(base_n, bbox, seed=SEED + base_n)
    base_matrix = get_duration_matrix(base_coords, batch_size=100, timeout=60)

    # Step 2: Generate all target coordinates
    all_coords = generate_random_coords_in_bbox(target_n, bbox, seed=SEED + target_n)

    # Step 3: Build the full matrix using distance-based interpolation
    # Compute geographic distances between all pairs
    coords_arr = np.array(all_coords)
    lon = coords_arr[:, 0]
    lat = coords_arr[:, 1]

    # Approximate geographic distance in meters using Haversine
    R = 6371000  # Earth radius in meters
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    dlat = lat_rad[:, None] - lat_rad[None, :]
    dlon = lon_rad[:, None] - lon_rad[None, :]
    a = np.sin(dlat / 2) ** 2 + np.cos(lat_rad[:, None]) * np.cos(lat_rad[None, :]) * np.sin(dlon / 2) ** 2
    geo_dist = 2 * R * np.arcsin(np.sqrt(np.clip(a, 0, 1)))

    # Step 4: Learn speed and asymmetry distribution from base matrix
    base_coords_arr = np.array(base_coords)
    base_geo = np.zeros((base_n, base_n))
    b_lat = np.radians(base_coords_arr[:, 1])
    b_lon = np.radians(base_coords_arr[:, 0])
    b_dlat = b_lat[:, None] - b_lat[None, :]
    b_dlon = b_lon[:, None] - b_lon[None, :]
    b_a = np.sin(b_dlat / 2) ** 2 + np.cos(b_lat[:, None]) * np.cos(b_lat[None, :]) * np.sin(b_dlon / 2) ** 2
    base_geo = 2 * R * np.arcsin(np.sqrt(np.clip(b_a, 0, 1)))

    # Compute speed factors (duration / distance) from base, excluding diagonal
    mask = base_geo > 100  # At least 100m apart
    speed_factors = np.where(mask, base_matrix / base_geo, np.nan)
    valid_speeds = speed_factors[~np.isnan(speed_factors) & (speed_factors > 0)]

    if len(valid_speeds) < 10:
        # Fallback: use average urban speed
        mean_speed_factor = 0.12  # ~30 km/h -> 0.12 s/m
        std_speed_factor = 0.03
    else:
        mean_speed_factor = np.median(valid_speeds)
        std_speed_factor = np.std(valid_speeds) * 0.5

    # Compute asymmetry ratios from base
    asym_ratios = []
    for i in range(base_n):
        for j in range(i + 1, base_n):
            if base_matrix[i, j] > 0 and base_matrix[j, i] > 0:
                ratio = base_matrix[i, j] / base_matrix[j, i]
                asym_ratios.append(np.log(ratio))  # Log-space for symmetry
    if asym_ratios:
        asym_mean = np.mean(asym_ratios)
        asym_std = np.std(asym_ratios)
    else:
        asym_mean = 0.0
        asym_std = 0.1

    # Step 5: Build target matrix
    # Base durations from geographic distance * speed factor + noise
    noise = rng.normal(0, std_speed_factor, (target_n, target_n))
    speed_matrix = np.clip(mean_speed_factor + noise, mean_speed_factor * 0.3, mean_speed_factor * 3.0)
    matrix = geo_dist * speed_matrix

    # Add realistic asymmetry
    asym_noise = rng.normal(asym_mean, asym_std, (target_n, target_n))
    asym_factor = np.exp(asym_noise)
    # Apply asymmetry: for each pair (i,j), multiply one direction by factor
    for i in range(target_n):
        for j in range(i + 1, target_n):
            mid = (matrix[i, j] + matrix[j, i]) / 2
            matrix[i, j] = mid * asym_factor[i, j]
            matrix[j, i] = mid / asym_factor[i, j]

    # Zero diagonal
    np.fill_diagonal(matrix, 0)

    # Ensure positive and convert to seconds (round to 0.1s)
    matrix = np.maximum(matrix, 0.1)
    np.fill_diagonal(matrix, 0)
    matrix = np.round(matrix, 1)

    return save_instance(
        name, all_coords, matrix, city, city_type,
        metadata={"generation_method": "osrm_scaled", "base_n": base_n},
    )


def generate_all_benchmarks():
    """Generate the full benchmark suite."""
    os.makedirs(BENCHMARKS_DIR, exist_ok=True)
    instances = []

    # Configuration: (city, n, city_type, method)
    # Small instances (50-100) - direct OSRM
    small_configs = [
        ("manhattan", 75, "grid"),
        ("paris", 75, "organic"),
        ("berlin", 75, "mixed"),
    ]

    # Medium instances (200-500) - batched OSRM
    medium_configs = [
        ("manhattan", 200, "grid"),
        ("rome", 200, "organic"),
        ("los_angeles", 200, "mixed"),
    ]

    # Large instances (500-1000) - OSRM-scaled
    large_configs = [
        ("chicago", 500, "grid"),
        ("london", 500, "organic"),
        ("tokyo", 500, "mixed"),
    ]

    print("=== Generating Small Instances (direct OSRM) ===")
    for city, n, city_type in small_configs:
        try:
            inst = generate_osrm_instance(city, n, city_type)
            instances.append(inst["name"])
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"  ERROR generating {city}_{n}: {e}")

    print("\n=== Generating Medium Instances (batched OSRM) ===")
    for city, n, city_type in medium_configs:
        try:
            inst = generate_osrm_instance(city, n, city_type)
            instances.append(inst["name"])
            time.sleep(2)  # Rate limiting
        except Exception as e:
            print(f"  ERROR generating {city}_{n}: {e}")

    print("\n=== Generating Large Instances (OSRM-scaled) ===")
    for city, n, city_type in large_configs:
        try:
            inst = generate_scaled_instance(city, n, city_type, base_n=100)
            instances.append(inst["name"])
            time.sleep(2)
        except Exception as e:
            print(f"  ERROR generating {city}_{n}: {e}")

    print(f"\n=== Generated {len(instances)} benchmark instances ===")
    return instances


def write_readme(instances):
    """Write README documenting all benchmark instances."""
    readme_path = os.path.join(BENCHMARKS_DIR, "README.md")

    lines = [
        "# Benchmark ATSP Instances",
        "",
        "Asymmetric Traveling Salesman Problem instances derived from real road networks",
        "via the OSRM (Open Source Routing Machine) Table API with OpenStreetMap data.",
        "",
        "## Instance Summary",
        "",
        "| Instance | City | Type | Nodes | Asym Mean | Asym Max | Method |",
        "|----------|------|------|-------|-----------|----------|--------|",
    ]

    for fname in sorted(os.listdir(BENCHMARKS_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(BENCHMARKS_DIR, fname)
        with open(fpath) as f:
            data = json.load(f)
        method = data.get("metadata", {}).get("generation_method", "osrm_direct")
        stats = data.get("asymmetry_stats", {})
        lines.append(
            f"| {data['name']} | {data['city']} | {data['city_type']} | "
            f"{data['n']} | {stats.get('mean_ratio', 0):.4f} | "
            f"{stats.get('max_ratio', 0):.4f} | {method} |"
        )

    lines.extend([
        "",
        "## Size Categories",
        "",
        "- **Small (50-100 stops):** Direct OSRM queries, exact road network durations",
        "- **Medium (200-500 stops):** Batched OSRM queries, exact road network durations",
        "- **Large (500-1000 stops):** OSRM-calibrated synthetic matrices preserving city-specific",
        "  speed distributions and asymmetry patterns from real data",
        "",
        "## Geographic Types",
        "",
        "- **Grid:** Cities with regular street grids (Manhattan, Chicago, Barcelona)",
        "- **Organic:** European cities with irregular medieval street layouts (Paris, Rome, London)",
        "- **Mixed:** Suburban-urban areas with mixed road patterns (Berlin, Los Angeles, Tokyo)",
        "",
        "## File Format",
        "",
        "Each `.json` file contains:",
        "- `name`: Instance identifier",
        "- `city`: City name",
        "- `city_type`: Geographic type (grid/organic/mixed)",
        "- `n`: Number of stops",
        "- `coords`: List of [longitude, latitude] pairs",
        "- `duration_matrix`: Full n x n asymmetric duration matrix (seconds)",
        "- `asymmetry_stats`: Statistics about matrix asymmetry",
        "- `metadata`: Generation parameters (timestamp, OSRM version, seed)",
        "",
        "## Reproducibility",
        "",
        "All instances generated with seed=42. Re-run `python -m src.generate_benchmarks`",
        "to regenerate (requires OSRM server access).",
    ])

    with open(readme_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {readme_path}")


if __name__ == "__main__":
    instances = generate_all_benchmarks()
    write_readme(instances)
