# Literature Review: Better Heuristics for TSP on Real Road Networks

## 1. Classical TSP Solvers and Their Limitations on Non-Euclidean Instances

### 1.1 LKH: The Lin-Kernighan-Helsgaun Heuristic

The Lin-Kernighan-Helsgaun (LKH) algorithm is the state-of-the-art heuristic solver for the Traveling Salesman Problem. Helsgaun's original implementation \cite{helsgaun2000} introduced the alpha-value candidate set construction method based on minimum 1-trees. For each city, a candidate set is formed from edges with the smallest alpha-values, and during k-opt search, only candidate edges are considered for improving the current solution.

**Euclidean bias in candidate sets:** The alpha-value method works well for Euclidean instances because the minimum 1-tree structure correlates strongly with the geometric proximity of points. For non-Euclidean and asymmetric instances, this correlation weakens. Additionally, LKH supports Delaunay triangulation for candidate generation, but this method is restricted to Euclidean instances only \cite{helsgaun2009}. The POPMUSIC candidate generation method is more general but still relies on structural assumptions that may not hold for real road networks.

**Fixed guidance limitation:** The alpha-value used in LKH to evaluate edge quality is fixed during the search. This single, static guidance metric can trap the algorithm in local optima, particularly on instances whose cost structure deviates from Euclidean geometry \cite{zheng2022vsr}.

**LKH-3 extensions:** Helsgaun extended LKH to handle constrained TSP variants and vehicle routing problems \cite{helsgaun2017}. LKH-3 solves approximately 40 different problem types including ATSP by transforming them into symmetric TSPs using the Jonker-Volgenant or Rao transformation. While effective, this transformation approach introduces overhead and does not directly exploit asymmetric structure.

### 1.2 Concorde: Exact Solver for Symmetric TSP

Concorde is the leading exact solver for symmetric TSP, based on branch-and-cut with cutting planes from the traveling salesman polytope \cite{applegate2006}. However, Concorde **cannot directly solve asymmetric TSP**. The standard approach is the Jonker-Volgenant (1983) transformation \cite{jonker1983}, which converts an n-city ATSP into a 2n-city symmetric TSP by introducing ghost nodes. This transformation:

1. **Doubles problem size**: An n-city ATSP becomes a 2n-city symmetric TSP, significantly increasing computational cost.
2. **Confuses heuristics**: The dummy cities introduced by the transformation degrade heuristic performance, making this approach practical only with exact solvers.
3. **Loses asymmetric structure**: The transformation encodes asymmetric costs into a symmetric framework, preventing exploitation of directional cost patterns.

For the Amazon Last Mile instances, Concorde with Jonker-Volgenant transformation solved instances in an average of 142 seconds on a single core \cite{merchan2022}.

### 1.3 Christofides Algorithm

The Christofides-Serdyukov algorithm \cite{christofides1976} provides a 3/2-approximation guarantee for metric TSP. However, it **requires the triangle inequality** to hold. For non-metric instances (which include many real road network scenarios with time-dependent costs), no polynomial-time approximation with bounded ratio exists unless P=NP. The recent improvement by Karlin, Klein, and Gharan (2021) achieves a ratio of 3/2 - 10^{-36} but still requires metric distances \cite{karlin2021}.

### 1.4 Summary of Limitations

| Solver | ATSP Support | Key Limitation for Road Networks |
|--------|-------------|----------------------------------|
| LKH/LKH-3 | Via transformation | Alpha-value candidate sets biased toward Euclidean structure |
| Concorde | Via J-V transformation | Problem size doubles; symmetric-only architecture |
| Christofides | No (metric only) | Requires triangle inequality; no asymmetric support |

## 2. Neural and Learned Heuristics for Combinatorial Optimization

### 2.1 Construction Heuristics

**Attention Model (AM):** Kool et al. (2019) introduced the Attention Model using an encoder-decoder Transformer architecture trained with REINFORCE and a greedy rollout baseline \cite{kool2019}. AM autoregressively constructs TSP tours by attending to node embeddings and achieves competitive results on small instances (n <= 100).

**POMO:** Kwon et al. (2020) proposed Policy Optimization with Multiple Optima, exploiting the symmetry of TSP solutions by solving each instance from multiple starting points \cite{kwon2020}. POMO achieves a 0.14% gap from optimum on TSP-100, making it the strongest pure neural construction method. POMO remains the standard backbone for RL-based construction solvers.

### 2.2 Improvement Heuristics and Hybrid Methods

**NeuroLKH:** Xin et al. (2021) combined a Sparse Graph Network (SGN) with LKH, using supervised learning for edge scores and unsupervised learning for node penalties to generate candidate sets and transform edge distances \cite{xin2021}. NeuroLKH significantly outperforms vanilla LKH and generalizes across problem sizes. However, it was primarily evaluated on Euclidean instances.

**VSR-LKH:** Zheng et al. (2022) proposed replacing LKH's fixed alpha-value with an adaptive Q-value learned via reinforcement learning, allowing dynamic edge evaluation during search \cite{zheng2022vsr}. This addresses the fixed-guidance limitation but adds computational overhead.

**Embed-LKH:** A recent approach (2024) enhances LKH with graph embedding techniques for general TSP where distances can be non-metric and asymmetric \cite{embedlkh2024}. It transforms distances to transition probabilities, learns embeddings to construct "ghost distances," then uses LKH with these ghost distances for candidate generation while searching on original distances. Embed-LKH shows improvements over vanilla LKH across six distance distributions including asymmetric ones.

### 2.3 Divide-and-Conquer Approaches

**GLOP:** Ye et al. (2024) introduced GLOP (Global and Local Optimization Policies), a hierarchical framework that partitions large routing problems into sub-TSPs and further into Shortest Hamiltonian Path Problems \cite{ye2024glop}. It hybridizes non-autoregressive global partitioning with autoregressive local construction. GLOP is the first neural solver to scale to TSP-100K and handles ATSP.

**UDC:** Zheng et al. (2024) proposed a Unified Neural Divide-and-Conquer framework with a Divide-Conquer-Reunion training method \cite{zheng2024udc}. UDC was evaluated on 10 CO problems including ATSP, employing a sliding-window mechanism to correct partition errors end-to-end.

### 2.4 LLM-Based Heuristic Design

**Evolution of Heuristics (EoH):** Liu et al. (2024) proposed an evolutionary paradigm leveraging LLMs to automatically design heuristics for combinatorial optimization \cite{liu2024eoh}. EoH evolves both natural-language "thoughts" and executable code, achieving competitive performance with only thousands of LLM queries versus millions required by FunSearch.

### 2.5 Frameworks and Benchmarks

**RL4CO:** Berto et al. (2023/2025) developed a unified reinforcement learning library for combinatorial optimization, providing 27 problem environments and 23 baselines \cite{berto2023rl4co}. RL4CO standardizes evaluation and enables fair comparison of neural CO methods.

## 3. Real Road Network Routing, Asymmetric TSP, and Time-Dependent Travel

### 3.1 Asymmetry in Real Road Networks

Vu et al. (2019) introduced the **asymmetry factor** as a graph measure for directed networks and analyzed road networks from 12 diverse cities \cite{vu2019}. Key findings:

- Real road networks exhibit **bounded but non-trivial asymmetry** — the time to travel A→B differs from B→A due to one-way streets, turn restrictions, and varying congestion.
- The asymmetry factor enables a symmetrization procedure that allows black-box use of symmetric TSP approximation algorithms with provable guarantees proportional to the asymmetry factor.
- For ridesharing and delivery applications, ATSP on subsets of the road network is the natural formulation.

### 3.2 OSRM-Derived TSP Instances

The **Open Source Routing Machine (OSRM)** is a C++ routing engine using OpenStreetMap data, supporting multi-level Dijkstra and contraction hierarchies \cite{luxen2011osrm}. Its Table API computes full distance/duration matrices, which are inherently asymmetric for road networks. OSRM's built-in trip plugin solves TSP using farthest-insertion heuristic but provides only approximate solutions.

### 3.3 Amazon Last Mile Routing Challenge

The 2021 Amazon Last Mile Routing Research Challenge released **9,184 real-world ATSP instances** (6,112 training + 3,072 evaluation), making it the largest collection of real-world TSP instances \cite{merchan2022}. Key properties:

- Instance sizes range from 32 to 237 stops (mean 148).
- Each instance includes point-to-point travel times, coordinates, time windows, and the actual driver-chosen sequence.
- Asymmetry arises from one-way streets, turn penalties, and traffic patterns.
- LKH-3 typically finds optimal tours for these instances, though without optimality proof.

### 3.4 Time-Dependent and Dynamic TSP

Recent work addresses the Dynamic TSP with Time-Dependent and Stochastic travel times using deep RL \cite{zhang2025dtsp}. A dynamic encoder and temporal pointer handle time-dependent costs, with strong generalization across scenarios. This represents an emerging frontier where classical solvers have even greater limitations, as travel times change based on departure time.

### 3.5 Quantified Gaps in Solver Performance

On real road network instances, the performance hierarchy is generally:
1. LKH-3 produces near-optimal solutions but does not exploit asymmetric structure directly.
2. VROOM achieves ~2-3% gap from LKH-3 on TSPLIB instances in milliseconds.
3. Nearest-neighbor and insertion heuristics produce 15-25% gaps.

The key observation is that LKH-3's alpha-value candidate sets are designed for symmetric/Euclidean structure. On high-asymmetry instances, there should be room for improvement by designing candidate sets that account for directional cost differences.

## 4. Key Findings Summary

1. **LKH's Euclidean bias is addressable**: The alpha-value candidate set construction assumes structural properties that weaken on asymmetric road networks. Methods like NeuroLKH and Embed-LKH show that learned candidate sets can outperform alpha-values.

2. **Real road networks have bounded asymmetry**: Vu et al. (2019) showed asymmetry factors are moderate but consistent across diverse cities, suggesting targeted exploitation is feasible.

3. **Divide-and-conquer scales neural methods**: GLOP and UDC demonstrate that hierarchical decomposition allows neural solvers to handle instances with 1000+ nodes.

4. **Amazon Last Mile provides ground truth**: 9,184 real-world instances with known driver routes provide realistic evaluation data.

5. **Hybrid approaches are most promising**: Methods combining learned guidance with LKH-style search (NeuroLKH, Embed-LKH, VSR-LKH) consistently outperform pure neural or pure classical approaches.

## 5. Open Questions

1. **Can asymmetry-aware candidate sets outperform LKH defaults on real road networks?** No existing work specifically designs candidate sets for road network asymmetry patterns.

2. **What is the achievable improvement over LKH-3 on OSRM-derived instances?** The 0.5% target improvement is plausible given Embed-LKH's results on general ATSP, but unverified on real road data.

3. **How does asymmetry level correlate with improvement potential?** Higher asymmetry should yield larger gains from asymmetry-aware methods, but this has not been systematically studied.

4. **Can local search operators designed for directed graphs improve over symmetric 2-opt?** Standard 2-opt reverses segments, which changes traversal direction and may increase cost in asymmetric networks.

5. **Does geographic decomposition preserve asymmetric structure?** Divide-and-conquer on road networks should respect road connectivity, not just geometric proximity.

## References

See `sources.bib` for complete bibliography.
