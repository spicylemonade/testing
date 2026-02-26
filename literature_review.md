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

