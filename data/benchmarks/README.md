# Benchmark ATSP Instances

Asymmetric Traveling Salesman Problem instances derived from real road networks
via the OSRM (Open Source Routing Machine) Table API with OpenStreetMap data.

## Instance Summary

| Instance | City | Type | Nodes | Asym Mean | Asym Max | Method |
|----------|------|------|-------|-----------|----------|--------|
| berlin_75 | berlin | mixed | 75 | 1.0635 | 2.7300 | osrm_direct |
| chicago_500 | chicago | grid | 500 | 1.3969 | 7.3596 | osrm_scaled |
| london_500 | london | organic | 500 | 1.1944 | 3.0513 | osrm_scaled |
| los_angeles_200 | los_angeles | mixed | 200 | 1.0499 | 14.3828 | osrm_direct |
| manhattan_200 | manhattan | grid | 200 | 1.2659 | 921.7500 | osrm_direct |
| manhattan_75 | manhattan | grid | 75 | 1.1824 | 36.2705 | osrm_direct |
| paris_75 | paris | organic | 75 | 1.1056 | 3.5390 | osrm_direct |
| rome_200 | rome | organic | 200 | 1.1248 | 30.4111 | osrm_direct |
| tokyo_500 | tokyo | mixed | 500 | 1.2035 | 3.1550 | osrm_scaled |

## Size Categories

- **Small (50-100 stops):** Direct OSRM queries, exact road network durations
- **Medium (200-500 stops):** Batched OSRM queries, exact road network durations
- **Large (500-1000 stops):** OSRM-calibrated synthetic matrices preserving city-specific
  speed distributions and asymmetry patterns from real data

## Geographic Types

- **Grid:** Cities with regular street grids (Manhattan, Chicago, Barcelona)
- **Organic:** European cities with irregular medieval street layouts (Paris, Rome, London)
- **Mixed:** Suburban-urban areas with mixed road patterns (Berlin, Los Angeles, Tokyo)

## File Format

Each `.json` file contains:
- `name`: Instance identifier
- `city`: City name
- `city_type`: Geographic type (grid/organic/mixed)
- `n`: Number of stops
- `coords`: List of [longitude, latitude] pairs
- `duration_matrix`: Full n x n asymmetric duration matrix (seconds)
- `asymmetry_stats`: Statistics about matrix asymmetry
- `metadata`: Generation parameters (timestamp, OSRM version, seed)

## Reproducibility

All instances generated with seed=42. Re-run generation script to reproduce.
