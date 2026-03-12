# Concept: divisor_window_density_control

- Topic Context:  First, decree that T(1,1) = 1. Then for n > 0, let S(n) = {(i,j) : 1 <= i <= n, 1 <= j <= n},
and let

T(1,n+1) = least positive integer not among T(i,j) for (i,j) in S(n);
T(n+1,1) = least positive integer not among T(i,j) for (i,j) in S(n) and not (T,n+1);
T(m,n+1) = T(m,1)*T(1,n+1).

These rules generate an array T which starts out like this:

T = [
    [1, 2, 4, 7, 9, 13, 15, 18, 23, 25, 29],
    [3, 6, 12, 21, 27, 39, 45, 54, 69, 75, 87],
    [5, 10, 20, 35, 45, 65, 75, 90, 115, 125, 145],
    [8, 16, 32, 56, 72, 104, 120, 144, 184, 200, 232],
    [11, 22, 44, 77, 99, 143, 165, 198, 253, 275, 319]
]

Every prime is in row 1 of T or column 1, but not both.

The difference sequence of row 1 starts with

1,2,3,2,4,2,3,5,2,4,2,5,4,2,4,3,2,4,3,2,2,4,4,7,2,3,2,4,3,5,5,3,4.

Here's the problem: prove (or disprove) that this difference sequence bounded.

More terms of the array T and its first row are given at A129258 and A129259. 
- Domains: analytic number theory, multiplication tables, asymptotic analysis

## Implementation Backlog
- [ ] Define minimal executable artifact for this concept.
- [ ] Connect this concept to at least one sibling concept in the bridge graph.
- [ ] Document how this differs from the closest prior-art paper.
- [ ] Add measurable experiment and result file under this folder.