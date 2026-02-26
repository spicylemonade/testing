# Literature Review: Voxel Grid Traversal Algorithms

## 1. Classic Voxel Grid Traversal Algorithms

### 1.1 Amanatides & Woo DDA (1987)

**Reference:** Amanatides & Woo, "A Fast Voxel Traversal Algorithm for Ray Tracing," Eurographics 1987 \cite{amanatides1987fast}

**Algorithm Overview:**
The Amanatides-Woo algorithm is a 3D Digital Differential Analyzer (DDA) that incrementally identifies all voxels intersected by a ray in a uniform grid. It is the most widely-cited voxel traversal method (>950 citations).

**Pseudocode Analysis:**
```
Input: ray origin u, direction v, grid bounds
1. INITIALIZATION:
   - Compute entry point into grid and initial voxel (X, Y, Z)
   - stepX = sign(v.x), stepY = sign(v.y), stepZ = sign(v.z)
   - tDeltaX = |gridSpacing / v.x|  (t to cross one voxel in X)
   - tDeltaY = |gridSpacing / v.y|
   - tDeltaZ = |gridSpacing / v.z|
   - tMaxX = t at next X boundary, tMaxY, tMaxZ similarly

2. INCREMENTAL TRAVERSAL (inner loop):
   while voxel is within grid:
     process_voxel(X, Y, Z)
     if tMaxX < tMaxY:
       if tMaxX < tMaxZ:
         X += stepX; tMaxX += tDeltaX
       else:
         Z += stepZ; tMaxZ += tDeltaZ
     else:
       if tMaxY < tMaxZ:
         Y += stepY; tMaxY += tDeltaY
       else:
         Z += stepZ; tMaxZ += tDeltaZ
```

**Complexity:**
- Time: O(N) per ray, where N is the number of voxels traversed (proportional to grid diagonal)
- Per-step operations: 2 floating-point comparisons + 1 floating-point addition
- Space: O(1) auxiliary (just tMax and tDelta vectors)

**Limitations:**
- Requires floating-point arithmetic (potential for numerical drift on very long traversals)
- Branch-heavy inner loop (3 conditional branches per step) → branch misprediction penalty
- Cannot skip empty regions; visits every voxel along the ray regardless of occupancy
- No vectorization-friendly structure (serial ray-by-ray processing)

---

### 1.2 3D Bresenham Line Algorithm

**Reference:** Bresenham, "Algorithm for computer control of a digital plotter," IBM Systems Journal, 1965 \cite{bresenham1965algorithm}

**Algorithm Overview:**
The 3D extension of Bresenham's line algorithm uses only integer arithmetic (additions and comparisons) to voxelize a line segment between two endpoints. It produces a 26-connected chain of voxels.

**Pseudocode Analysis:**
```
Input: start voxel (x0,y0,z0), end voxel (x1,y1,z1)
1. dx = |x1-x0|, dy = |y1-y0|, dz = |z1-z0|
2. Identify dominant axis (largest of dx, dy, dz)
3. Compute error terms: err1, err2
4. For each step along dominant axis:
   - Output current voxel
   - Update error terms by 2*secondary_delta
   - If error > threshold: step in secondary axis, adjust error
```

**Complexity:**
- Time: O(max(dx,dy,dz)) — proportional to the longest axis span
- Per-step: 2 integer comparisons, 2-4 integer additions
- Space: O(1) auxiliary

**Voxel Traversal Variant (Supercover):**
Standard Bresenham produces a 26-connected line (thin), which may miss voxels that the continuous line actually intersects. The supercover variant visits ALL voxels touched by the line, producing a 6-connected thick line. This requires additional checks at voxel corners and edges where the line crosses multiple boundaries simultaneously.

**Limitations:**
- Not a true ray traversal (no t-parameter or intersection distances)
- Standard version misses voxels → not suitable for accurate ray casting
- Supercover variant is more expensive per step
- Integer-only: requires grid-aligned endpoints
- No occupancy awareness or empty-space skipping

---

### 1.3 Cleary & Wyvill Algorithm (1988)

**Reference:** Cleary & Wyvill, "Analysis of an algorithm for fast ray tracing using uniform space subdivision," The Visual Computer, 1988 \cite{cleary1988analysis}

**Algorithm Overview:**
Cleary & Wyvill proposed a ray traversal algorithm for uniform space subdivision with a focus on skipping empty cells efficiently. The algorithm uses integer arithmetic for the skip operation ("can be done very quickly, using only integer addition and comparison") and provides theoretical analysis of performance vs. scene complexity.

**Key Contributions:**
- Theoretical analysis showing how time/space requirements scale with object count
- Empty cell skipping using integer arithmetic
- Framework for analyzing traversal efficiency in scenes of varying density

**Complexity:**
- Time: O(N) per ray in worst case, better in sparse scenes
- Empty-space skip: O(1) per skip step (integer addition + comparison)
- Space: O(grid_size) for the grid structure

**Limitations:**
- Specific to the uniform grid partitioning scheme
- Limited acceleration in dense scenes where few cells are empty
- Less commonly implemented than Amanatides-Woo despite similar performance characteristics

---

### 1.4 Siddon's Algorithm (1985)

**Reference:** Siddon, "Fast calculation of the exact radiological path for a three-dimensional CT array," Medical Physics, 1985 \cite{siddon1985fast}

**Algorithm Overview:**
Siddon's algorithm computes the exact radiological path length through a 3D CT voxel array by reformulating the problem in terms of intersections with three orthogonal sets of equally-spaced parallel planes, rather than considering individual voxels.

**Pseudocode Analysis:**
```
Input: ray from point P1 to P2, CT array of N^3 voxels
1. PLANE INTERSECTIONS:
   - For each axis (X, Y, Z), compute parametric t-values where
     the ray intersects each parallel plane
   - alpha_x(i) = (x_plane(i) - P1.x) / (P2.x - P1.x) for i=0..Nx
   - Similarly for Y and Z planes
2. MERGE SORTED LISTS:
   - Merge the three sorted lists of t-values into one sorted sequence
   - Each consecutive pair [alpha_i, alpha_{i+1}] defines a voxel
3. ACCUMULATE:
   - path_length(voxel) = (alpha_{i+1} - alpha_i) * |P2 - P1|
   - Total radiological path = sum of density(voxel) * path_length(voxel)
```

**Complexity:**
- Time: O(3N) = O(N) where N is the grid side length — a dramatic improvement over O(N³) naive approaches
- Per-voxel: 1 comparison (merge step) + 1 multiplication + 1 addition
- Space: O(N) for the sorted plane intersection lists

**Limitations:**
- Designed for radiological path accumulation, not for general traversal with early termination
- Requires pre-computation of all plane intersections (no incremental/streaming variant)
- The merge step has overhead that may exceed DDA for short rays
- Specific to regular grids with uniform spacing

---

## Summary Comparison Table

| Algorithm | Year | Operations/Step | Arithmetic | Empty Skip | t-values | Citations |
|-----------|------|----------------|------------|------------|----------|-----------|
| Amanatides-Woo DDA | 1987 | 2 cmp + 1 add (FP) | Float | No | Yes | ~958 |
| 3D Bresenham | 1965/ext | 2 cmp + 2-4 add (Int) | Integer | No | No | ~4500 |
| Cleary-Wyvill | 1988 | Integer add + cmp | Mixed | Partial | Yes | ~150 |
| Siddon | 1985 | 1 cmp + 1 mul + 1 add | Float | No | Yes | ~1581 |
| Liu et al. One-Pass | 2004 | 1-3 voxels/iter (Int) | Integer | No | No | ~30 |

---

## 2. Hierarchical and Acceleration-Structure-Based Methods

### 2.1 Sparse Voxel Octrees — Laine & Karras (2010)

**Reference:** Laine & Karras, "Efficient Sparse Voxel Octrees," IEEE TVCG / I3D 2010 \cite{laine2010efficient}

**Algorithm Overview:**
Sparse Voxel Octrees (SVOs) recursively subdivide a voxel volume into 8 child nodes. Empty nodes are culled, saving memory and allowing rays to skip large empty regions. Laine & Karras present an efficient GPU ray caster with contour-augmented voxels for increased geometric resolution.

**Key Features:**
- Compact encoding: ~1.02 bytes/voxel for ESVO
- Contour-based pruning reduces tree depth for smooth surfaces
- GPU-optimized with per-thread traversal stacks
- Competitive with triangle-based ray casting while allowing greater geometric detail

**Complexity:**
- Time: O(log N) per ray for tree descent, O(k * log N) total where k = voxels hit
- Space: O(V) where V = occupied voxels (typically << N³)

**Limitations:**
- Deep tree hierarchy (2³ branching → 10 levels for 1024³) causes cache misses from pointer chasing
- Large per-thread stack on GPU hurts occupancy
- Inherently static — rebuilding required for dynamic scenes
- Traversal overhead from ascending/descending tree often exceeds simpler methods by ~60%
- Grazing rays along axis-aligned planes are pathological

---

### 2.2 Sparse 64-Trees and Brickmap Approaches

**Reference:** dubiousconst282, "A guide to fast voxel ray tracing using sparse 64-trees," 2024 \cite{dubiousconst2024sparse64}

**Algorithm Overview:**
Sparse 64-trees use a wider branching factor (4³ = 64 children per node) instead of the octree's 2³ = 8. Each node stores a 64-bit occupancy bitmask, enabling efficient empty-space skipping via population count (popcount) instructions. The VoxelRT project implements both a brickmap (flat hash of 4³ bricks) and a hierarchical 64-tree.

**Key Features:**
- Shallow hierarchy: only 2 levels for 1024³ (vs. 9+ for octree)
- 64-bit bitmask per node enables hardware-accelerated popcount traversal
- Ray marching through bitmasks: compute next occupied child via bit manipulation
- ~0.62 bytes/voxel (vs. ~1.02 for ESVO) — roughly half the memory
- 11-15% faster traversal than ESVO for primary rays

**Brickmap Variant:**
- Flat hash table of small (4³ or 8³) voxel bricks
- O(1) brick lookup via spatial hashing
- Simpler traversal: DDA at brick level, direct indexing within brick
- Better suited for dynamic scenes (per-brick updates)

**Complexity:**
- Time: O(N^{1/3}) per ray (shallow tree descent) + O(k) for voxels in occupied bricks
- Space: O(V) with low constant overhead

---

### 2.3 Sparse Voxel DAGs — Kämpe, Sintorn & Assarsson (2013)

**Reference:** Kämpe et al., "High Resolution Sparse Voxel DAGs," ACM TOG / SIGGRAPH 2013 \cite{kampe2013high}

**Algorithm Overview:**
Sparse Voxel DAGs generalize SVOs by merging identical subtrees into shared nodes, converting the tree into a directed acyclic graph. This achieves 1-3 orders of magnitude reduction in node count vs. SVO.

**Key Features:**
- Efficient bottom-up algorithm reduces SVO to minimal DAG
- Works even when full SVO doesn't fit in memory (streaming construction)
- No decompression needed — traversed directly like an SVO
- Demonstrated 170-240 MRays/sec for ambient occlusion and shadows on GPU

**Complexity:**
- Construction: O(V log V) with sorting-based merge
- Traversal: Same as SVO O(log N) per descent
- Space: Orders of magnitude smaller than SVO for scenes with repeated geometry

**Limitations:**
- Read-only: modifications require reconstruction
- Pointer overhead per node (mitigated by massive node reduction)
- Same deep-hierarchy traversal issues as octrees

---

### 2.4 Multi-Resolution Voxel Grids with Spatial Hashing

**Reference:** Nießner et al., "Real-time 3D reconstruction at scale using voxel hashing," ACM TOG 2013 \cite{niessner2013voxelhashing}

**Algorithm Overview:**
Spatial hashing maps 3D voxel block coordinates to a flat hash table, providing O(1) average-case access without hierarchical traversal. Recent work (MrHash, 2025) extends this to multi-resolution with variance-adaptive voxel sizing.

**Key Features:**
- O(1) average-case lookup — no tree descent overhead
- Fully GPU-parallel (no pointer chasing)
- Supports dynamic updates (insert/delete/modify in O(1))
- Multi-resolution variant adapts voxel size to local detail
- Up to 13× faster than octree-based VDBFusion

**Tradeoffs:**
- Hash collisions degrade worst-case to O(n)
- No inherent hierarchy for LOD (must be added explicitly)
- Memory overhead for hash table load factor

---

### 2.5 Octree-R: Cost-Optimized Partitioning

**Concept Overview:**
Cost-optimized octree variants (sometimes called Octree-R or adaptive octrees) use surface area heuristic (SAH) or cost models to decide when to subdivide vs. stop. Unlike regular octrees that subdivide uniformly, these adapt the tree structure to the data distribution, placing more resolution where geometry is dense and less where it is sparse.

**Relation to BVH SAH:**
The idea mirrors the Surface Area Heuristic used in BVH construction for ray tracing (Goldsmith & Salmon, 1987), adapted to voxel octrees. Nodes are split only when the expected cost of traversing children is less than the cost of intersecting all objects in the current node.

**Tradeoffs:**
- Better worst-case performance on non-uniform data distributions
- Higher construction cost (must evaluate cost function at each split)
- More complex implementation than uniform octrees
- Limited adoption in voxel-specific literature (more common in general BVH/kd-tree work)

---

## Hierarchical Methods Summary

| Method | Branching | Depth (1024³) | Bytes/Voxel | Dynamic | GPU-Friendly |
|--------|-----------|---------------|-------------|---------|-------------|
| SVO (Laine-Karras) | 2³ = 8 | ~10 | ~1.02 | No | Moderate |
| Sparse 64-Tree | 4³ = 64 | ~2 | ~0.62 | Partial | Good |
| Sparse Voxel DAG | 2³ = 8 | ~10 | <<1.0 | No | Moderate |
| Spatial Hash | Flat | 1 | Variable | Yes | Excellent |
| Brickmap | Flat+brick | 1-2 | ~0.8 | Yes | Good |

---

## 3. SIMD, GPU, and Branchless Optimization Techniques

### 3.1 GPU-Mapped Grid Traversal — Es & Isler (2007)

**Reference:** Es & Isler, "Accelerated Regular Grid Traversals using Extended Anisotropic Chessboard Distance Fields on a GPU," 2007 \cite{es2007accelerated}

**Algorithm Overview:**
Es & Isler extend the DDA grid traversal to GPUs by using anisotropic chessboard distance fields to skip empty cells. Each cell stores the minimum distance to the nearest occupied cell, allowing multi-voxel jumps during traversal. The method maps naturally to GPU fragment/compute shaders where each thread processes one ray.

**Key Performance Characteristics:**
- Distance fields enable O(1)-per-skip empty space jumps
- GPU parallelism processes millions of rays simultaneously
- Anisotropic distance provides tighter bounds than isotropic variants

---

### 3.2 Branchless DDA Implementations

**Reference:** Branchless Voxel Raycasting (Shadertoy) \cite{branchlessdda2016}

**Algorithm Overview:**
The standard Amanatides-Woo DDA uses nested if-else branches to select the stepping axis. Branchless variants replace these with vectorized min/max operations:

```
// Branchless axis selection
mask = (tMax.x < tMax.y) & (tMax.x < tMax.z)  // bitmask approach
// OR equivalently:
axis = argmin(tMax)  // select minimum component
voxel[axis] += step[axis]
tMax[axis] += tDelta[axis]
```

**Performance Characteristics:**
- Eliminates 2-3 conditional branches per step
- On GPUs: may provide moderate benefit since hardware already has conditional-move instructions
- On CPUs: can reduce branch misprediction penalty by ~15-20% for incoherent rays
- Caveat: branchless versions sometimes run ~40% slower on mobile GPUs due to computing both branches

**Tradeoffs:**
- Most beneficial for incoherent ray distributions (random directions)
- For coherent rays, branch prediction already works well → minimal benefit
- Slightly more arithmetic per step (computing all 3 axes then selecting)

---

### 3.3 Axis-Normalized Ray-Box Intersection with SIMD

**Reference:** Friederichs, "Axis-Normalized Ray-Box Intersection," 2025 \cite{friederichs2025raybox}

**Algorithm Overview:**
Modern SIMD approaches normalize the ray direction to exploit vectorized min/max instructions for ray-AABB intersection tests. By pre-normalizing the ray such that the dominant axis has unit direction, the intersection computation reduces to fewer operations, and SIMD (SSE/AVX) processes 4/8 rays simultaneously.

**Key Optimizations:**
- Pre-compute 1/direction for all rays in a batch
- Use SIMD `_mm_min_ps` / `_mm_max_ps` for slab intersection
- Batch ray-box tests: 4 rays per SSE register, 8 per AVX
- Combined with grid traversal: test ray-brick intersection for 4-8 rays simultaneously

---

### 3.4 MultiDDA and XBrickMap Bitmask-Based Hierarchical Skipping

**Reference:** VoxelRT Project (dubiousconst282) \cite{dubiousconst2024sparse64}

**Algorithm Overview:**
MultiDDA uses two nested DDA loops: an outer loop at coarse block level (e.g., 8³ bricks) and an inner loop at voxel level. XBrickMap extends this with 64-bit occupancy bitmasks per brick, enabling multi-voxel skips within occupied bricks via popcount/tzcnt instructions.

**Key Features:**
- Two-level DDA: coarse (brick) + fine (voxel)
- 64-bit bitmask per brick: each bit = one 4³ sub-block occupancy
- Hardware popcount: O(1) to find next occupied sub-block
- Primary ray performance: competitive with tree-based methods
- Incoherent ray performance: degraded due to SIMD lane divergence when entering inner loop

**Performance (VoxelRT benchmarks):**
- MultiDDA: 8898 cycles/ray baseline → 7052 with bitmask coalescing (21% faster)
- Sparse 64-tree: further improvement for complex scenes
- Cache benefit from brick-aligned memory layout (brick fits in 1-2 cache lines)

---

### 3.5 Cache-Aware Memory Layouts: Morton/Z-Order and Hilbert Curves

**Key Concept:**
Space-filling curves map 3D voxel coordinates to 1D memory addresses while preserving spatial locality. This reduces cache misses during traversal since neighboring voxels in 3D space are stored nearby in memory.

**Morton (Z-Order) Curve:**
- Bit-interleaving of (x, y, z) coordinates
- Fast encoding/decoding: bit shifts + masks, or hardware BMI2 PDEP/PEXT
- Good spatial locality with occasional discontinuities at Z-boundaries
- Most popular choice for voxel engines and SVOs

**Hilbert Curve:**
- Continuous space-filling (no jumps between consecutive points)
- ~10-30% fewer cache misses than Morton in traversal benchmarks
- More expensive to compute (state-machine encoding)
- Net throughput often similar to Morton due to higher encoding overhead

**Practical Recommendation:**
- **Morton Z-order** is the default choice: fast, simple, substantial cache benefit
- **Block-linear (tiled) layouts** — small tiles (4³ or 8³) in linear order, tiles arranged in Morton order — provide the best practical balance
- Hilbert order reserved for streaming/sequential access patterns

---

## SIMD/GPU Optimization Summary

| Technique | Benefit | Best For | Overhead |
|-----------|---------|----------|----------|
| Branchless DDA | Reduces branch misprediction | Incoherent rays | Slight compute increase |
| SIMD batch ray-box | 4-8× throughput per instruction | Ray-AABB tests | Ray batching setup |
| Bitmask skipping | Multi-voxel jumps via popcount | Sparse grids | Bitmask maintenance |
| Morton layout | 30-50% fewer cache misses | Large grids (≥256³) | Encoding overhead |
| GPU parallelism | Millions of rays in parallel | All distributions | Memory bandwidth |

