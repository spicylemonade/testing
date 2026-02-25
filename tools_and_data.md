# Tools and Data Survey

## 1. Routing Engines

### 1.1 OSRM (Open Source Routing Machine)
- **URL:** https://project-osrm.org/
- **GitHub:** https://github.com/Project-OSRM/osrm-backend
- **Language:** C++
- **Data source:** OpenStreetMap
- **Algorithms:** Multi-Level Dijkstra (MLD), Contraction Hierarchies (CH)
- **Key API endpoints:**
  - `/table/v1/{profile}/{coordinates}` — Computes duration/distance matrices (asymmetric by default)
  - `/route/v1/{profile}/{coordinates}` — Point-to-point routing
  - `/trip/v1/{profile}/{coordinates}` — TSP solver (farthest-insertion heuristic)
- **Matrix limits:** Up to 10,000 coordinates per request (CH mode)
- **Installation:** Docker (`docker pull osrm/osrm-backend`), or compile from source
- **Public demo:** `https://router.project-osrm.org/table/v1/driving/{coords}`

### 1.2 OpenRouteService (ORS)
- **URL:** https://openrouteservice.org/
- **GitHub:** https://github.com/GIScience/openrouteservice
- **Language:** Java
- **Data source:** OpenStreetMap
- **Key API endpoints:**
  - `/v2/matrix/{profile}` — Duration/distance matrices (asymmetric)
  - `/v2/directions/{profile}` — Point-to-point routing
  - `/v2/optimization` — VRP solver (VROOM backend)
- **Matrix limits:** 3,500 elements (e.g., 50x50) per request on public API
- **Installation:** Docker or self-hosted; free API key for public endpoint
- **Python client:** `pip install openrouteservice`

### 1.3 GraphHopper
- **URL:** https://www.graphhopper.com/
- **GitHub:** https://github.com/graphhopper/graphhopper
- **Language:** Java
- **Data source:** OpenStreetMap
- **Key features:** Matrix API, route optimization, isochrones
- **Matrix limits:** Custom limits on self-hosted
- **Installation:** Docker or JAR; commercial cloud API available

### 1.4 Google OR-Tools Routing
- **URL:** https://developers.google.com/optimization/routing
- **GitHub:** https://github.com/google/or-tools
- **Language:** C++ with Python bindings
- **Key features:** Constraint programming solver for VRP/TSP with arbitrary cost matrices
- **Installation:** `pip install ortools`
- **Notes:** Works with any distance matrix (not tied to OSM); supports time windows, capacity, pickup-delivery

## 2. Open-Source TSP/VRP Solvers

### 2.1 LKH-3 (Lin-Kernighan-Helsgaun)
- **URL:** http://webhotel4.ruc.dk/~keld/research/LKH-3/
- **Language:** C
- **Problem types:** ~40 TSP/VRP variants including ATSP
- **Installation:**
  ```bash
  wget http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3.0.10.tgz
  tar xzf LKH-3.0.10.tgz
  cd LKH-3.0.10
  make
  ```
- **Input format:** TSPLIB format (.atsp, .tsp, .vrp)
- **Quality:** State-of-the-art heuristic; typically finds optimal or near-optimal solutions
- **License:** Free for academic and non-commercial use

### 2.2 VROOM (Vehicle Routing Open-source Optimization Machine)
- **URL:** https://github.com/VROOM-Project/vroom
- **Language:** C++20
- **Python wrapper:** `pip install pyvroom`
- **Problem types:** TSP, CVRP, VRPTW, multi-depot
- **Installation:**
  ```bash
  pip install pyvroom
  # Or compile from source:
  git clone https://github.com/VROOM-Project/vroom.git
  cd vroom && mkdir build && cd build && cmake .. && make
  ```
- **Performance:** +2.47% mean gap from optimal on TSPLIB; millisecond solve times
- **Notes:** Requires OSRM or ORS backend for road network routing; can also take custom matrices

### 2.3 Concorde
- **URL:** https://www.math.uwaterloo.ca/tsp/concorde/
- **Language:** C
- **Problem types:** Symmetric TSP only (exact solver)
- **Installation:** Download from UWaterloo; compile with LP solver (CPLEX recommended)
- **Notes:** Exact solver via branch-and-cut; handles ATSP only through Jonker-Volgenant transformation (2n cities). Python wrapper: `pip install pyconcorde`

### 2.4 Google OR-Tools
- **Installation:** `pip install ortools`
- **Problem types:** VRP, TSP, ATSP with arbitrary constraints
- **Notes:** Supports custom distance matrices, time windows, capacities. Uses metaheuristics (guided local search, simulated annealing, tabu search).

## 3. Benchmark Datasets

### 3.1 TSPLIB / TSPLIB95
- **URL:** http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
- **Type:** Symmetric TSP (113 instances) + Asymmetric TSP (19 instances)
- **Size range:** TSP: 14–85,900 nodes; ATSP: 17–443 nodes
- **Format:** Custom TSPLIB format
- **Notes:** The standard benchmark since 1991 \cite{reinelt1991tsplib}. All optimal solutions known since 2007. ATSP instances include ftv-series (real-world) and ry48p (random).
- **Python reader:** `pip install tsplib95`

### 3.2 Amazon Last Mile Routing Challenge Dataset
- **URL:** https://www.math.uwaterloo.ca/tsp/amz/data.html
- **Type:** Asymmetric TSP with time windows
- **Size:** 9,184 instances (6,112 training + 3,072 evaluation)
- **Size range:** 32–237 stops per instance (mean 148)
- **Format:** JSON with travel times, coordinates, time windows, package data
- **Notes:** Largest collection of real-world ATSP instances \cite{merchan2022}. Asymmetry from one-way streets and traffic patterns. Includes actual driver routes for comparison.

### 3.3 OSRM-Generated Custom Instances
- **Type:** Asymmetric TSP from real road networks
- **Size range:** Arbitrary (limited by OSRM Table API capacity)
- **Generation:** Sample random coordinates within a city bounding box, query OSRM Table API for full asymmetric duration matrix
- **Notes:** This project will generate custom instances across multiple cities and size categories. See item_008 in research_rubric.json.

### 3.4 National TSP Instances
- **URL:** https://www.math.uwaterloo.ca/tsp/world/countries.html
- **Type:** Symmetric TSP (Euclidean)
- **Size range:** 29 (Djibouti) to 71,009 (China)
- **Notes:** Real geographic coordinates but Euclidean distances; does not capture road network asymmetry. Useful for scalability testing.

## 4. Frameworks for Neural Combinatorial Optimization

### 4.1 RL4CO
- **URL:** https://github.com/ai4co/rl4co
- **Installation:** `pip install rl4co`
- **Features:** 27 CO problem environments, 23 baselines (AM, POMO, etc.), PyTorch-based
- **Notes:** Unified benchmark for fair comparison of neural CO methods \cite{berto2023rl4co}

### 4.2 GLOP
- **URL:** https://github.com/henry-yeh/GLOP
- **Features:** Divide-and-conquer neural solver for large-scale TSP/ATSP/CVRP
- **Notes:** First neural solver to scale to TSP-100K \cite{ye2024glop}
