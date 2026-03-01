# Survey of Open-Source Shortest Path Implementations and Benchmark Suites

## 1. Open-Source Implementations

### 1.1 NetworkX (Python)
- **Language:** Pure Python
- **URL:** https://networkx.org
- **Algorithms:** Dijkstra, Bellman-Ford, Floyd-Warshall, A*, bidirectional Dijkstra, Johnson
- **Performance:** Slowest among major libraries (10-250x slower than C/C++ implementations)
- **Strengths:** Excellent API, rich algorithm library, widespread adoption, easy prototyping
- **Weaknesses:** Pure Python overhead makes it impractical for large graphs (>100K nodes)
- **Shortest path API:** `nx.shortest_path()`, `nx.dijkstra_path()`, `nx.astar_path()`

### 1.2 igraph (C with Python/R bindings)
- **Language:** C core with Python (`python-igraph`) and R bindings
- **URL:** https://igraph.org
- **Algorithms:** Dijkstra, Bellman-Ford, unweighted BFS
- **Performance:** Very fast; 10-50x faster than NetworkX for shortest path queries
- **Strengths:** Memory-efficient, handles millions of nodes, good for social network analysis
- **Weaknesses:** Smaller algorithm library than NetworkX; less Pythonic API

### 1.3 graph-tool (C++ with Python bindings)
- **Language:** C++ with Boost Graph Library backend, OpenMP support
- **URL:** https://graph-tool.skewed.de
- **Algorithms:** Dijkstra, Bellman-Ford, A*, all-pairs
- **Performance:** Fastest general-purpose graph library; 3-10x faster than igraph with OpenMP
- **Strengths:** Publication-quality visualization, parallel algorithms, statistical inference
- **Weaknesses:** Complex installation (C++ compilation), GPL license

### 1.4 Boost Graph Library (BGL) (C++)
- **Language:** C++
- **URL:** https://www.boost.org/doc/libs/release/libs/graph/
- **Algorithms:** Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, A*
- **Performance:** Good but implementation-dependent; hashtable-based approaches can beat it
- **Strengths:** Header-only C++, highly generic, template-based design
- **Weaknesses:** Steep learning curve, verbose template syntax

### 1.5 OSRM (Open Source Routing Machine)
- **Language:** C++
- **URL:** https://project-osrm.org / https://github.com/Project-OSRM/osrm-backend
- **Algorithms:** Contraction Hierarchies (CH), Multi-Level Dijkstra (MLD)
- **Performance:** Sub-millisecond queries on continental road networks after preprocessing
- **Strengths:** Production-ready routing engine, HTTP API, OpenStreetMap integration
- **Weaknesses:** Specialized for road networks; heavy preprocessing (minutes to hours)

### 1.6 NetworKit (C++ with Python bindings)
- **Language:** C++ with Python interface
- **URL:** https://networkit.github.io
- **Algorithms:** Dijkstra, BFS, bidirectional BFS, SSSP, APSP
- **Performance:** Competitive with graph-tool; optimized for large-scale network analysis
- **Strengths:** Parallel algorithms, good scalability to billion-edge graphs
- **Weaknesses:** Less well-known than NetworkX/igraph

### 1.7 RoutingKit (C++)
- **Language:** C++
- **URL:** https://github.com/RoutingKit/RoutingKit
- **Algorithms:** Contraction Hierarchies, Customizable Contraction Hierarchies
- **Performance:** State-of-the-art for road network routing
- **Strengths:** Clean C++ implementation of CH, reference implementation of CRP
- **Weaknesses:** Specialized for road network routing

## Performance Comparison Summary

| Library | Language | SSSP Speed (relative) | Scale | License |
|---------|----------|----------------------|-------|---------|
| graph-tool | C++ | 1x (reference) | 10M+ nodes | GPL |
| igraph | C | ~3x slower | 10M+ nodes | GPL |
| NetworKit | C++ | ~1-2x slower | 1B+ edges | MIT |
| Boost BGL | C++ | ~2-5x slower | 1M+ nodes | Boost |
| OSRM | C++ | <1ms queries | Continental | BSD |
| RoutingKit | C++ | <1ms queries | Continental | BSD |
| NetworkX | Python | ~100x slower | 100K nodes | BSD |

## 2. Standard Benchmark Graph Datasets

### 2.1 DIMACS Shortest Path Challenge Graphs
- **URL:** http://www.diag.uniroma1.it/challenge9/download.shtml
- **Description:** Standard benchmark suite for shortest path algorithms since 2005
- **Graph types:** USA road networks at various scales
  - NY (264K nodes, 733K edges) — New York City
  - BAY (321K nodes, 800K edges) — San Francisco Bay Area
  - COL (436K nodes, 1M edges) — Colorado
  - FLA (1.07M nodes, 2.7M edges) — Florida
  - CAL (1.89M nodes, 4.7M edges) — California/Nevada
  - E-USA (3.6M nodes, 8.8M edges) — Eastern USA
  - W-USA (6.3M nodes, 15.2M edges) — Western USA
  - CTR (14.1M nodes, 34M edges) — Central USA
  - USA (23.9M nodes, 58.3M edges) — Full USA
- **Format:** DIMACS graph format (edge list with header)
- **Widely used in:** CH, hub labeling, CRP, and transit node papers

### 2.2 SNAP (Stanford Network Analysis Project) Datasets
- **URL:** https://snap.stanford.edu/data/
- **Description:** Diverse real-world network datasets
- **Graph types:**
  - Social networks: Facebook (4K nodes), Twitter (81K nodes), Pokec (1.6M nodes)
  - Web graphs: Google (876K nodes), Berkely-Stanford (685K nodes)
  - Road networks: California, Pennsylvania, Texas
  - Citation networks: HepPh, HepTh, Patents
- **Format:** Edge lists (text, TSV)
- **Strengths:** Diverse graph structures (heavy-tailed, small-world, spatial)

### 2.3 OpenStreetMap (OSM) Extracts
- **URL:** https://download.geofabrik.de
- **Description:** Real road network data from OpenStreetMap
- **Graph types:** Road networks of any region worldwide
- **Strengths:** Realistic, includes edge attributes (speed limits, road types)
- **Weaknesses:** Requires preprocessing to extract graph structure

### 2.4 Network Repository
- **URL:** https://networkrepository.com
- **Description:** Large collection of network datasets across many domains
- **Graph types:** Social, biological, infrastructure, web, collaboration networks
- **Format:** Various (edge list, matrix market, etc.)

## 3. Benchmark Methodology Notes

For our experiments, we will use:
1. **Synthetic graphs** generated programmatically (Erdős-Rényi, grid, Barabási-Albert, complete)
2. **SNAP datasets** for real-world social/web graph benchmarks (easily downloadable)
3. **DIMACS road networks** for spatial graph benchmarks (standard in the field)

Our Python implementation will benchmark against NetworkX as the primary comparison
baseline, since both use Python. For absolute performance context, we will reference
published numbers from C++ implementations (graph-tool, OSRM, RoutingKit).
