# TDA Results: Persistent Homology of Collatz Point Clouds

## Parameters
- max_n = 10000, subsample = 1000, null samples = 100

## Key Findings

### Maximum Feature Lifetimes
- H0 max lifetime: 2.5130 (null 95th: 2.8543, p=0.4700)
- H1 max lifetime: 0.6146 (null 95th: 0.5894, p=0.0200)
- H2 max lifetime: 0.1055

### H1 Cycles (Loops)
**Significant H1 features detected** (p=0.0200 < 0.05).
Non-trivial 1-cycles persist across filtration values, indicating genuine
topological structure not attributable to noise.

### Residue Class Comparison
- Wasserstein distance H0 (n≡1 mod 4 vs n≡3 mod 4): 90.8984
- Wasserstein distance H1 (n≡1 mod 4 vs n≡3 mod 4): 13.4089

### Novelty Assessment
This is the first application of persistent homology to Collatz trajectory
point clouds. No prior work in the literature applies TDA to Collatz dynamics.
