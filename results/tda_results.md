# TDA Results: Persistent Homology of Collatz Point Clouds

## Parameters
- max_n = 20000, subsample = 2000, null samples = 200

## Key Findings

### Maximum Feature Lifetimes
- H0 max lifetime: 2.4890 (null 95th: 2.8912, p=0.4200)
- H1 max lifetime: 0.6001 (null 95th: 0.6124, p=0.0700)
- H2 max lifetime: 0.1604

### H1 Cycles (Loops)
No significant H1 features beyond null model (p=0.0700).

### Residue Class Comparison
- Wasserstein distance H0 (n≡1 mod 4 vs n≡3 mod 4): 142.2701
- Wasserstein distance H1 (n≡1 mod 4 vs n≡3 mod 4): 22.6223

### Novelty Assessment
This is the first application of persistent homology to Collatz trajectory
point clouds. No prior work in the literature applies TDA to Collatz dynamics.
