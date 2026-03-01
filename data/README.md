# Real-World Proxy Datasets

## Overview
Since DIMACS and SNAP datasets cannot be downloaded in the current environment,
we generate proxy graphs with matching structural properties.

## Dataset 1: Road Network Proxy
- **Generator:** `Graph.grid(100, 100, seed=42)` with random weight perturbation
- **Properties:** 10,000 nodes, ~19,800 edges, planar, avg degree ~4
- **Mimics:** DIMACS NY road network (264K nodes, 733K edges)
- **Key structural match:** Planarity, low degree, spatial locality

## Dataset 2: Social Network Proxy
- **Generator:** `Graph.barabasi_albert(5000, m=5, seed=42)`
- **Properties:** 5,000 nodes, ~24,985 edges, power-law degree distribution
- **Mimics:** SNAP Facebook ego-net (4K nodes) and similar social networks
- **Key structural match:** Power-law degree, small-world, high-degree hubs

## Reproduction
To download actual DIMACS/SNAP datasets for full evaluation:
1. DIMACS: http://www.diag.uniroma1.it/challenge9/download.shtml
   - Download NY.gr.gz, extract, use `Graph.from_dimacs("NY.gr")`
2. SNAP: https://snap.stanford.edu/data/
   - Download edge list, use `Graph.from_edgelist("dataset.txt")`
