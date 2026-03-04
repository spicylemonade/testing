# Frog Dynamics and PushTASEP

## Topic Context

Bukh and Cox (2022) discovered a remarkable connection between LCS of periodic-vs-random words and a new interacting particle system called "frog dynamics." In this system, labeled particles ("frogs") sit on the integers and hop over each other according to their label ordering. The unlabeled version reduces to PushTASEP, a well-studied particle system in the KPZ universality class.

For a periodic word W of period k, the LCS constant γ(W) equals the expected particle speed in the stationary distribution of the associated frog dynamics. When all symbols in W are distinct (W = 12...k), an explicit formula exists.

## Key Results

- γ(12...k) has an explicit closed-form expression
- For palindromic words W = 12...kk...21, Briggs et al. (2024) found explicit formulas
- Bukh-Cox found periodic words that are "more random-like than random" (γ(W) > γ₂ conjectured)
- The heuristic LCS algorithm of Bukh-Cox runs in O(n√n) expected time on random inputs

## Implementation Backlog

1. **Implement frog dynamics simulator** (Priority: HIGH)
   - Exact simulation for small period k ≤ 10
   - Monte Carlo for larger k
   - Compare γ(W) across all binary words of period k

2. **Search for optimal periodic words** (Priority: HIGH)
   - Enumerate binary words of period p = 1,...,20
   - Compute γ(W) for each
   - Track minimum γ(W) as p grows (lower bounds on γ₂)

3. **Extend to random-vs-random setting** (Priority: HIGH)
   - Formulate the "doubly random" frog dynamics
   - Relate to Tiskin's particle process
   - Identify which structures from periodic case survive

4. **Analyze mixing times** (Priority: MEDIUM)
   - How fast does frog dynamics converge to stationarity?
   - Determine optimal simulation length for γ(W) estimation
