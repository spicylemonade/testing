# Concept Tree Synthesis: Cross-Domain Ideas for BB(6) Search

## 1. Overview

The ConceptEvolve tree generated 10 concept cards spanning domains from number theory and information theory to evolutionary computation, statistical physics, and neural networks. Of these, several directly influenced our implemented search strategies. This document synthesizes which concepts were most valuable, which were dead ends, and what future BB(6) researchers should prioritize.

## 2. Concept Cards and Their Outcomes

### Tier 1: Directly Implemented and Productive

| Concept | Domain | Implementation | Impact |
|---------|--------|---------------|--------|
| **Evolutionary Search Strategy** (#4) | Evolutionary computation | `src/tm_breeding.py` — TM breeding with row swap, column swap, block crossover | Medium. Found sigma=66 candidates. Breeding acts as structured mutation. |
| **Modular Arithmetic Sieving** (#5) | Number theory | `src/deciders.py` — CTL decider uses closed-form tape analysis; `results/baselines/reproduce_champion.py` — Euler's totient for Collatz verification | High. Critical for verifying Kropitz t15 algebraically. |
| **Collatz Delay Record Search** (#1) | Computational mathematics | `src/mutation_search.py` — Champion-seeded search analogous to delay record neighborhood exploration | High. Mutation search from champions was the best strategy (sigma=80). |

### Tier 2: Partially Implemented, Informative but Limited Impact

| Concept | Domain | Implementation | Impact |
|---------|--------|---------------|--------|
| **Stochastic Orbit Model** (#2) | Statistical physics | `src/guided_search.py` — Feature extraction + biased sampling, inspired by random walk with drift | Low. Guided search underperformed random (sigma=11 vs 10). |
| **Information-Theoretic Sieve** (#3) | Information theory | Feature extraction includes entropy-related metrics (write ratio, direction ratio) | Low. No strong correlation between syntactic entropy and sigma. |
| **Simulated Annealing TM Space** (tree/004) | Physics | Informed the temperature-based acceptance in guided search | Low. Did not implement full SA schedule. |

### Tier 3: Not Implemented — Future Research Directions

| Concept | Domain | Why Not Implemented | Potential |
|---------|--------|-------------------|-----------|
| **Algebraic Structure of Champions** (tree/005) | Abstract algebra | Requires symbolic simulation, not step-by-step | Very High. This is the actual path to new records. |
| **Collatz-Like Halting Analysis** (tree/006) | Number theory | Needs automated detection of Collatz rules in TM tables | Very High. Directly targets the mechanism of champion behavior. |
| **Neural Guided Search** (tree/009) | Machine learning | Training data insufficient; requires millions of labeled TMs | Medium. Could work with enough precomputation. |
| **Macro-Machine Hierarchy** (tree/010) | Computability theory | Requires macro-step detection and algebraic acceleration | High. This is what bbchallenge's accelerated simulators do. |

## 3. Ranking by Impact on Results

1. **Mutation from champions** (from Concept #1, delay record search analogy): Produced our best result (sigma=80). The key insight — that champions occupy "interesting neighborhoods" — directly parallels how Collatz delay records cluster near other high-delay numbers.

2. **Algebraic verification** (from Concept #5, modular arithmetic): Enabled the only approach that can reach the true champions. Our Kropitz t15 verification used Euler's totient theorem exactly as the concept card suggested for modular sieving.

3. **Evolutionary breeding** (from Concept #4): Produced sigma=66 candidates. The crossover strategies were directly adapted from genetic algorithm literature.

4. **Feature-guided search** (from Concepts #2, #3): Negative result, but informative. Proved that syntactic features are poor predictors — the interesting properties are semantic.

## 4. Which Analogies Were Fruitful vs Dead Ends

### Fruitful Analogies

- **Collatz delay records → TM champion neighborhoods**: Both exhibit clustering. Mutating champions is the most efficient heuristic search strategy, paralleling how delay records tend to appear near other high-delay numbers. This analogy was the most directly actionable.

- **Modular arithmetic → Algebraic TM verification**: The Collatz connection runs deep. The Kropitz t15 champion literally implements a Collatz-like function. Understanding Collatz through modular arithmetic directly translates to understanding champion TMs.

- **Genetic crossover → TM breeding**: The row/column swap strategies are natural analogues of genetic crossover. While results were modest, this established a framework for future work with larger and more diverse parent populations.

### Dead Ends

- **Random walk models → TM feature extraction**: The stochastic orbit model works well for Collatz because the dynamics have a clear drift structure. TM behavior is too heterogeneous for a simple random walk analogy to capture meaningful variation.

- **Shannon entropy → TM complexity prediction**: Information entropy of transition tables tells you about the table's structure, not the computation's complexity. A maximally entropic table is just random, not computationally interesting.

- **Simulated annealing → TM space exploration**: The TM fitness landscape is too rugged and the "temperature" concept too vague for standard SA to help. There's no smooth energy function to anneal.

## 5. Recommendations for Future BB(6) Researchers

Based on our concept tree exploration:

1. **Invest heavily in Concept tree/005 (Algebraic Structure of Champions).** The gap between simulation-reachable results (sigma ~80) and the true records (sigma > 2↑↑↑5) can only be bridged by understanding the algebraic mechanisms that produce astronomical outputs. Automated detection of Collatz-like rules, counter machines, and shift-overflow patterns in TM transition tables should be the top priority.

2. **Build on Concept tree/010 (Macro-Machine Hierarchy).** The bbchallenge project's success came from macro-step acceleration — collapsing long sequences of operations into single steps. Extending this to 6-state machines, with automated macro-rule discovery, would dramatically expand the reachable search horizon.

3. **Don't waste time on syntactic features.** Our negative result with guided search is strong evidence that graph-theoretic properties of transition tables do not predict computational power. Invest in dynamic/semantic features instead.

4. **Mutation search is the best short-term strategy.** Until algebraic methods are mature, systematic mutation from known champions with increasing step limits remains the most efficient heuristic approach.

5. **Leverage the Collatz connection.** At least two known BB(6) champions implement Collatz-like functions. Searching specifically for TMs that implement known-to-terminate generalized Collatz maps, using the modular arithmetic framework from Concept #5, is a concrete path to structured discovery.

## 6. Updated Concept Folders

The following concept folders have been updated with final status:

- `tree/001_collatz_delay_record_search/` — Status: **Directly applied**. Champion neighborhood search implemented and validated.
- `tree/004_evolutionary_search_strategy/` — Status: **Implemented**. TM breeding produced modest results.
- `tree/005_modular_arithmetic_sieving/` — Status: **Critical for verification**. Euler's totient used for Kropitz t15.
- `tree/002_genetic_evolution_of_tm/` — Status: **Implemented** as `src/tm_breeding.py`.
- `tree/003_information_theoretic_sieve/` — Status: **Tested, negative result**. Syntactic entropy does not predict sigma.
- `tree/005_algebraic_structure_of_champions/` — Status: **Not implemented, highest future potential**.
