# GPU Compute Shader Parallelism

## Topic Context

Modern GPUs contain thousands of cores designed for parallel computation. The N-body gravity problem, where each particle interacts with every other particle, is an ideal workload for GPU parallelism. Each GPU thread computes the force on one particle, and the O(N^2) work is distributed across P cores, achieving O(N^2/P) wall-clock time.

WebGPU is the modern successor to WebGL, bringing compute shaders to the browser. This enables interactive gravity simulations with 100K+ particles at 60 FPS without any installation. The tiled algorithm loads blocks of particles into fast shared memory to maximize cache utilization.

### Key Ideas
- Each GPU thread computes force on one particle
- Tiled memory access pattern for cache efficiency
- Double-buffered storage buffers avoid read-write hazards
- WebGPU brings GPU compute to the browser

### Cross-Domain Connections
- Neural network matrix multiplication (same parallel structure)
- Galaxy simulation on supercomputers (same physics, larger scale)
- Particle Life: non-physical particle simulations on GPU

## Implementation Backlog

- [ ] Set up WebGPU boilerplate (adapter, device, canvas)
- [ ] Write compute shader for all-pairs force calculation
- [ ] Implement tiled shared memory optimization
- [ ] Add Verlet position integration in compute shader
- [ ] Write vertex/fragment shaders for particle rendering
- [ ] Double-buffer position storage buffers
- [ ] Benchmark FPS vs particle count
- [ ] Add interactive mouse-based gravity source
