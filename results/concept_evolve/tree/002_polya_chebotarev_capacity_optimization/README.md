# 002: Polya-Chebotarev Capacity Optimization

## Topic Context

The Polya-Chebotarev problem, suggested by Chebotarev to Polya in the 1920s, asks: given a finite set of points E in C, find the compact connected set K of minimal logarithmic capacity such that E is a subset of K. The solution consists of analytic arcs that are critical trajectories of a quadratic differential.

Fedorov gave an explicit solution for 4 symmetrically placed points using elliptic functions. Ortega-Cerda and Pridhnani (2008) described numerical methods for the general case and connected it to Bloch-Landau constant bounds and Brownian motion lifetime.

## Key Mathematical Objects

- **Logarithmic capacity**: cap(K) = exp(-inf_mu int int log(1/|z-w|) dmu(z) dmu(w))
- **Quadratic differential**: Q(z)dz^2 whose horizontal trajectories form the extremal continuum
- **Laurentiev's theorem**: characterizes the extremal domain for the Polya-Chebotarev problem

## Implementation Backlog

1. [ ] Implement Fedorov's explicit solution for n=4 symmetric points
2. [ ] Generalize to n=5,6 using numerical ODE integration of quadratic differential trajectories
3. [ ] Optimize point positions to minimize capacity
4. [ ] Connect minimal capacity to B_u bounds via inradius
5. [ ] Test asymmetric point configurations
6. [ ] Verify results with interval arithmetic
7. [ ] Visualize extremal continua for different configurations
