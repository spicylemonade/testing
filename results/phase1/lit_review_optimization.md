# Literature Review: Combinatorial Optimization for Protein Engineering

**Date:** 2026-03-04
**Scope:** Algorithmic approaches for optimizing multi-site protein mutations

---

## 1. Epistasis and Genetic Architecture

### 1a. The Genetic Architecture of Protein Stability

**Title:** The genetic architecture of protein stability
**Authors:** Andre J. Faure, Aina Marti-Aranda, Cristina Hidalgo-Carcedo, Antoni Beltran, Jorn M. Schmiedel, Ben Lehner
**Year:** 2024
**Venue:** Nature, Vol. 634, pp. 995-1003
**DOI:** 10.1038/s41586-024-07966-0

**Key Findings:**
- Experimentally sampled sequence spaces larger than 10^10 for multiple protein domains
- **Critical discovery:** The genetic architecture of protein stability is remarkably simple
- Most mutational effects are well-described by additive (first-order) models
- Pairwise epistasis accounts for nearly all remaining variance — higher-order terms are negligible
- Epistatic interactions are strongly distance-dependent: >90% of significant pairwise effects involve residues with Calpha distance < 10 Angstroms
- Additive + pairwise models can predict stability of combinatorial variants with high accuracy (R^2 > 0.9 for some proteins)
- **Implications for our pipeline:** Validates the additive+pairwise energy model; distance-filtering of epistasis pairs is both computationally efficient and biologically sound
- Simple energy decomposition: ddG(S) = sum_i(ddG_i) + sum_{i<j in contact}(epsilon_{ij})

### 1b. Thermodynamic Couplings in the Mega-scale Dataset

**Title:** Mega-scale experimental analysis of protein folding stability in biology and design
**Authors:** Kotaro Tsuboyama, Justas Dauparas, Jonathan Chen, Elodie Laine, Yasser Mohseni Behbahani, Jonathan J. Weinstein, Niall M. Mangan, Sergey Ovchinnikov, Gabriel J. Rocklin
**Year:** 2023
**Venue:** Nature, Vol. 620, pp. 434-444
**DOI:** 10.1038/s41586-023-06328-6

**Key Findings:**
- cDNA display proteolysis method measures thermodynamic folding stability for up to 900,000 protein domains
- Curated ~776,000 high-quality folding stabilities covering all single amino acid variants and selected double mutants
- 331 natural + 148 de novo designed protein domains, 40-72 amino acids in length
- Quantified environmental factors influencing amino acid fitness
- Measured thermodynamic couplings between protein sites, including unexpected long-range interactions
- **Double mutant data:** Provides ground truth for validating pairwise epistasis predictions
- **Multi-mutant subsets:** Limited but present — enables validation of combinatorial predictions

---

## 2. Bayesian Optimization for Protein Design

### 2a. GameOpt: Combinatorial Bayesian Optimization

**Title:** Optimistic Games for Combinatorial Bayesian Optimization with Application to Protein Design
**Authors:** Melis Ilayda Bal, Pier Giuseppe Sessa, Mojmir Mutny, Andreas Krause
**Year:** 2025
**Venue:** ICLR 2025

**Key Findings:**
- Novel game-theoretic approach to combinatorial Bayesian optimization (BO)
- Establishes a cooperative game between different optimization variables (positions in a protein)
- Selects points that are game equilibria of an upper confidence bound (UCB) acquisition function
- Equilibria are stable configurations from which no variable has incentive to deviate — analogous to local optima
- Breaks down combinatorial domain complexity into individual decision sets
- Scalable to large combinatorial spaces (up to 20^X configurations)
- Validated on four real-world protein datasets
- Iteratively selects informative configurations, discovers highly active variants quickly
- **Relevance to our pipeline:** The game-theoretic decomposition into per-position decisions directly inspires our beam search and evolutionary optimizer designs. The best-response dynamics approach could serve as an alternative optimizer.

---

## 3. ML-Assisted Directed Evolution

### 3a. MLDE: Machine Learning-Assisted Directed Evolution

**Title:** Informed training set design enables efficient machine learning-assisted directed protein evolution
**Authors:** Bruce J. Wittmann, Yisong Yue, Frances H. Arnold
**Year:** 2021
**Venue:** Cell Systems, Vol. 12, Issue 11
**DOI:** 10.1016/j.cels.2021.07.008

**Key Findings:**
- Investigates ML-assisted directed evolution (MLDE) protocol for in silico screening of full combinatorial libraries
- Evaluates importance of protein encoding strategies, training procedures, models, and training set design
- Key finding: most important consideration is reducing "holes" (zero-fitness variants) in training data
- Zero-shot prediction strategies enable construction of informative training sets
- On epistatic 4-site combinatorial landscape: MLDE achieved global fitness maximum 81-fold more frequently than single-step greedy optimization
- **Relevance:** Demonstrates superiority of ML-guided combinatorial search over greedy approaches; validates our goal of outperforming naive greedy search

### 3b. Evaluation of MLDE Across Diverse Landscapes

**Title:** Evaluation of machine learning-assisted directed evolution across diverse combinatorial landscapes
**Authors:** Francesca-Zhoufan Li, Jason Yang, Kadina E. Johnston, Emre Gursoy, Yisong Yue, Frances H. Arnold
**Year:** 2025
**Venue:** Cell Systems, Vol. 16, Issue 9
**DOI:** 10.1016/j.cels.2025.101387

**Key Findings:**
- Systematic analysis of multiple MLDE strategies across 16 diverse protein fitness landscapes
- Active learning and focused training using zero-shot predictors improve MLDE
- Strategy selection guidance based on landscape attributes and resources
- ML methods provide greater advantages on challenging epistatic landscapes
- **Relevance:** Validates that combining zero-shot predictors (like ESM-2) with ML-guided search outperforms brute-force approaches

---

## 4. Continuous Relaxation and Gradient-Based Optimization

### 4a. Gradient-Based Discrete Sequence Optimization

Various approaches have explored continuous relaxation of the discrete protein sequence optimization problem:

- **Gumbel-Softmax relaxation:** Treat amino acid identities as categorical variables, relax to continuous simplex, optimize via gradient descent
- **MCMC with learned proposals:** Use PLM log-likelihoods to guide Markov chain Monte Carlo sampling of mutation sets
- **Differentiable protein design:** End-to-end differentiable pipelines that backpropagate through structure prediction to sequence

### 4b. Relevant Continuous Optimization Tools

**RSO (Regularized Sequence Optimization):**
- Continuous relaxation of discrete sequence optimization
- L1 regularization encourages sparse mutation sets (few mutations from wildtype)
- Gradient-based optimization with projected gradient descent

**mosaic:**
- Multi-objective sequence optimization with integrated constraints
- Handles multiple scoring functions simultaneously (stability + activity + expression)
- Pareto front exploration for multi-objective protein design

---

## 5. Existing Tools and Software

### 5a. MLDE Software Package

**Repository:** https://github.com/fhalab/MLDE
- Implements the Wittmann et al. (2021) protocol
- Supports multiple encoding strategies and ML models
- Focused on 4-site combinatorial libraries
- Limitation: requires experimental training data, not zero-shot

### 5b. mosaic

- Multi-objective sequence optimization tool
- Pareto front exploration
- Integrates multiple fitness predictors
- Not specifically optimized for stability

### 5c. OSPREY

**Title:** OSPREY: Protein Design with Ensembles, Flexibility, and Provably Efficient Algorithms
- Physics-based protein design using dead-end elimination and A* search
- Provably optimal within Rosetta energy function
- Limitation: extremely slow for combinatorial mutations (hours to days)
- Uses rotamer libraries and explicit energy functions rather than ML models

### 5d. Caliby

- Calibrated Bayesian optimization for protein engineering
- Provides uncertainty quantification for predictions
- Limited to low-dimensional combinatorial spaces

---

## 6. Submodular Optimization and Approximation Guarantees

### 6a. Submodularity in Protein Stability

The protein stability optimization problem under additive+pairwise models can exhibit approximate submodularity:
- **Definition:** A set function f is submodular if f(A + {x}) - f(A) >= f(B + {x}) - f(B) for A subset B
- **Intuition:** Adding a stabilizing mutation has diminishing returns as more mutations are added (epistatic saturation)
- **Guarantee:** Greedy maximization of a submodular function achieves (1 - 1/e) ≈ 0.63 approximation ratio
- **Lazy greedy:** Evaluates only candidates whose marginal gain could exceed current best; reduces evaluations by 10-50x

### 6b. Feature Selection Analogies

The problem of selecting k mutations from N candidates is structurally identical to feature selection:
- k-sparse optimization: select k features (mutations) to maximize a model objective
- Forward stepwise selection = greedy mutation addition
- Branch and bound = systematic enumeration with pruning
- LASSO relaxation = L1-penalized continuous optimization

---

## 7. Search Algorithms for Combinatorial Protein Design

### 7a. Beam Search

- Maintains B best partial solutions at each depth
- Expansion: each partial solution proposes adding each candidate mutation
- Pruning: keep top-B expansions by score
- Complexity: O(B * K * depth) energy evaluations
- Tradeoff: beam width B controls speed vs solution quality
- Well-suited for GPU: batch scoring of B candidates in parallel

### 7b. Genetic/Evolutionary Algorithms

- Population of mutation sets evolves over generations
- Crossover: exchange mutations between high-scoring sets
- Mutation: randomly add/remove/replace mutations
- Selection: tournament or rank-based
- Elitism: preserve top solutions across generations
- Advantage: explores diverse regions of search space simultaneously
- Well-suited for escaping local optima when epistasis creates rugged landscapes

### 7c. Monte Carlo Tree Search (MCTS)

- Builds search tree incrementally by simulation
- UCB1 or PUCT selection balances exploration and exploitation
- Rollout policy: random or heuristic completion of partial mutation sets
- Backpropagation: update value estimates along visited path
- Advantage: asymptotically optimal; handles complex interaction patterns
- Used in AlphaGo and related game-playing agents; applicable to combinatorial optimization

---

## 8. Computational Budget Analysis

### 8a. Brute-Force Scaling

For selecting k mutations from top-N candidates:

| N | k | C(N,k) | Estimated Time (additive scoring) |
|---|---|--------|-----------------------------------|
| 20 | 3 | 1,140 | <1 second |
| 20 | 4 | 4,845 | ~2 seconds |
| 30 | 5 | 142,506 | ~1 minute |
| 50 | 6 | 15,890,700 | ~2 hours |
| 50 | 8 | 536,878,650 | ~70 hours |
| 100 | 6 | 1,192,052,400 | ~150 hours |

For N=50, k>=6, brute-force exceeds the 15-minute budget by orders of magnitude, motivating smarter search.

### 8b. GPU Budget Allocation

For a 15-minute total budget on A100:
- Single-mutation scoring (ESM-2): ~30 seconds
- Epistasis matrix computation: ~2-3 minutes
- Combinatorial optimization: ~5-8 minutes
- Re-ranking top candidates: ~2 minutes
- Overhead: ~1-2 minutes

---

## 9. Summary: Algorithm Design Space

Based on this review, the key design decisions for our optimizer are:

1. **Energy model:** Additive + distance-filtered pairwise (justified by Faure et al. 2024)
2. **Primary optimizer:** Beam search (GPU-friendly, tunable, proven effective)
3. **Alternative optimizer:** Evolutionary search (diversity preservation, escape local optima)
4. **Scoring pipeline:** ESM-2 prescreening -> pairwise epistasis -> beam search -> ProteinMPNN re-ranking
5. **Theoretical backing:** Approximate submodularity provides greedy baseline guarantee; GameOpt provides game-theoretic perspective
6. **Budget allocation:** Most time on single-mutation scoring and epistasis; optimization itself is fast with precomputed energy model

---

## 10. Gap Analysis

| Gap | Our Solution |
|-----|-------------|
| No tool combines ML scoring with combinatorial optimization | StabOpt pipeline |
| Pairwise epistasis estimation is expensive per pair | Structural distance filtering (Faure et al.) |
| Brute-force fails for k >= 6 | Beam search + evolutionary optimizer |
| Greedy is suboptimal on epistatic landscapes | Multi-strategy approach with re-ranking |
| Existing tools require training data | Zero-shot ESM-2 + ProteinMPNN scoring |
| No validated multi-mutant optimization tool | Validation against Mega-scale + FireProtDB |

---

*12 papers/tools reviewed. References tracked in sources.bib.*
