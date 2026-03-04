# Evaluation Metrics and Benchmark Protocol

**Date:** 2026-03-04
**Purpose:** Define all metrics for evaluating StabOpt multi-mutant stability predictions

---

## 1. Primary Metric: Predicted ddG of Best Multi-Mutant Combination

The primary metric is the predicted ddG (kcal/mol) of the highest-scoring multi-mutant combination found by each optimization method.

$$\text{ddG}_{\text{best}}(k) = \min_{S \subseteq \mathcal{M},\, |S|=k} \hat{f}(S)$$

where $\hat{f}(S) = \sum_{i \in S} \Delta\Delta G_i + \sum_{\{i,j\} \subseteq S} \varepsilon_{ij}$ is the energy model score, $\mathcal{M}$ is the candidate mutation pool, and $k$ is the target combination size (3-8).

**Interpretation:** More negative ddG indicates greater predicted stabilization. We compare best-found ddG across optimizers (brute-force, greedy, beam search, evolutionary) to quantify search quality.

---

## 2. Secondary Metrics

### 2a. Spearman Rank Correlation with Experimental ddG

For proteins with experimental multi-mutant data (Mega-scale double/triple mutants), compute:

$$\rho = 1 - \frac{6 \sum_i d_i^2}{n(n^2 - 1)}$$

where $d_i = \text{rank}(\hat{y}_i) - \text{rank}(y_i)$ is the rank difference between predicted and experimental ddG for the $i$-th variant, and $n$ is the number of variants.

**Targets:**
- Double mutants: $\rho \geq 0.50$
- Triple+ mutants: $\rho \geq 0.40$

These targets are based on published baselines: ThermoMPNN-D achieves ~0.48 Spearman on double mutants (Dieckhaus et al., 2024), and the additive approximation from Faure et al. (2024) achieves ~0.45 on doubles before epistasis correction.

### 2b. Enrichment of Experimentally Stabilizing Variants in Top-10 Predictions

For each test protein, define stabilizing variants as those with experimental $\Delta\Delta G < -1.0$ kcal/mol. Compute:

$$\text{Enrichment@}k = \frac{|\{v \in \text{Top-}k : \Delta\Delta G_{\text{exp}}(v) < -1.0\}| / k}{|\{v : \Delta\Delta G_{\text{exp}}(v) < -1.0\}| / N}$$

where $k = 10$ and $N$ is the total number of scored variants.

**Interpretation:** Enrichment > 1 means the method places stabilizing variants in the top-k more often than random. Target: Enrichment@10 > 5.0.

### 2c. Precision@k for Stabilizing Variants

$$\text{Precision@}k = \frac{|\{v \in \text{Top-}k : \Delta\Delta G_{\text{exp}}(v) < -1.0\}|}{k}$$

Complements enrichment by measuring the absolute fraction of true stabilizing variants in the top-k predictions. Report for $k \in \{5, 10, 20\}$.

### 2d. Normalized Discounted Cumulative Gain (NDCG)

For ranking quality across the full predicted list:

$$\text{DCG@}k = \sum_{i=1}^{k} \frac{\text{rel}_i}{\log_2(i+1)}, \qquad \text{NDCG@}k = \frac{\text{DCG@}k}{\text{IDCG@}k}$$

where $\text{rel}_i = \max(0, -\Delta\Delta G_{\text{exp},i})$ is the relevance (higher for more stabilizing variants) and IDCG is the ideal (perfectly sorted) DCG.

### 2e. Recovery Fraction

Fraction of known experimentally stabilizing single mutations recovered in the top-$N$ predictions:

$$\text{Recovery@}N = \frac{|\{m \in \text{Top-}N : \Delta\Delta G_{\text{exp}}(m) < 0\}|}{|\{m : \Delta\Delta G_{\text{exp}}(m) < 0\}|}$$

Report at $N \in \{10, 20, 50\}$.

---

## 3. Efficiency Metrics

### 3a. Wall-Clock Time

Total time from PDB input to ranked output, broken down by stage:

| Stage | Description | Budget Target |
|-------|-------------|---------------|
| Single-mutation scoring (ESM-2) | Score all $N \times 19$ single mutations | < 60s for 300-residue protein |
| Epistasis scoring | Pairwise epistasis for top-$K$ candidates | < 180s for $K=50$ |
| Optimization | Search for best $k$-combination | < 300s for $k=6$, $K=50$ |
| Consensus re-ranking | ProteinMPNN re-ranking of top candidates | < 120s for 100 candidates |
| **Total pipeline** | End-to-end | **< 15 minutes (900s)** |

### 3b. GPU Memory Usage

Peak GPU memory (in GB) during each pipeline stage. Must not exceed 40 GB (A100 80GB safely; A100 40GB variant hard limit).

Measured via `torch.cuda.max_memory_allocated()` after each stage.

### 3c. Number of Model Forward Passes

Count of neural network inference calls:

| Component | Formula |
|-----------|---------|
| ESM-2 single scoring | $L$ passes (one per position, masked marginal) |
| Epistasis scoring | $2 \times |\text{contact\_pairs}|$ passes (batched) |
| ProteinMPNN re-ranking | $N_{\text{rerank}}$ passes |
| **Total** | $L + 2|\text{contacts}| + N_{\text{rerank}}$ |

This metric captures computational cost independently of hardware and batching.

### 3d. Search Efficiency Ratio

$$\text{SER} = \frac{\text{ddG}_{\text{best}}(\text{method}) - \text{ddG}_{\text{best}}(\text{random})}{\text{ddG}_{\text{best}}(\text{brute-force}) - \text{ddG}_{\text{best}}(\text{random})}$$

where random baseline samples $B = 10{,}000$ random $k$-combinations. SER = 1.0 means the method matches brute-force optimality; SER close to 0 means no better than random. Only computable when brute-force is tractable (typically $k \leq 4, K \leq 30$).

---

## 4. Comparison Protocol Against Baselines

### 4a. Baselines

1. **Brute-force enumeration** (`stabopt/optimization/brute_force.py`): Exhaustive search over all $\binom{K}{k}$ combinations. Gold standard for $k \leq 4$ and $K \leq 30$.
2. **Greedy search** (`stabopt/optimization/greedy.py`): Iterative best-addition. $O(k \times K)$ evaluations.
3. **Random sampling**: Sample 10,000 random $k$-combinations, report best. Establishes lower bound.
4. **Additive-only model**: Use energy model with `mode="additive_only"` (no epistasis). Isolates value of pairwise terms.
5. **ESM-2 zero-shot single-mutation ranking**: Rank by single-mutation LLR only (no combinatorial search). Establishes PLM baseline.

### 4b. Published Baselines (from Literature)

| Method | Reference | Metric | Reported Value |
|--------|-----------|--------|----------------|
| Mutate Everything | Ouyang-Zhang et al., 2023 | Spearman (single) | ~0.47 on ProteinGym |
| ThermoMPNN-D | Dieckhaus et al., 2024 | Spearman (double) | ~0.48 on Mega-scale doubles |
| ESM-2 zero-shot | Brandes et al., 2023 | Spearman (single) | ~0.45 on DMS benchmarks |
| RaSP | Blaabjerg et al., 2023 | Spearman (single) | ~0.42 (structure-based) |
| MLDE | Wittmann et al., 2021 | Enrichment | >3x in directed evolution |

### 4c. Comparison Protocol

For each test protein:

1. **Run all methods** (brute-force where tractable, greedy, beam search, evolutionary) on the same candidate pool and energy model.
2. **Record primary metric** (best ddG found) and timing for each method.
3. **Compute suboptimality gap** vs brute-force: $\text{gap} = (\text{ddG}_{\text{method}} - \text{ddG}_{\text{BF}}) / |\text{ddG}_{\text{BF}}|$ (for $k \leq 4$).
4. **Statistical testing:** Bootstrap 95% confidence intervals on Spearman $\rho$ over proteins. Use paired Wilcoxon signed-rank test ($\alpha = 0.05$) for method comparisons.
5. **Scalability sweep:** Vary $K \in \{20, 30, 50, 100\}$ and $k \in \{3, 4, 5, 6, 8\}$. Report wall-clock time and solution quality as heatmaps.

### 4d. Test Proteins

Select 10+ representative proteins from Mega-scale dataset:
- Varying sizes: 40-72 residues (Mega-scale domain range), plus larger FireProtDB proteins
- Mix of all-alpha, all-beta, alpha/beta topologies
- Must have multi-mutant experimental data available

Select 5+ proteins from FireProtDB:
- Well-characterized proteins with many known stabilizing mutations
- Include both enzymes and non-enzymes
- Prefer proteins with PDB structures available

---

## 5. Ablation Dimensions

The following ablation dimensions will be evaluated (see item_022):

| Dimension | Variants |
|-----------|----------|
| Energy model mode | additive_only, additive_pairwise, full_pairwise |
| Optimizer | greedy, beam_search, evolutionary |
| Base scorer | ESM-2, ProteinMPNN |
| Consensus re-ranking | with, without |
| Beam width | 10, 50, 100, 500 |
| Distance threshold | 8A, 10A, 12A, 15A |
| Candidate pool size $K$ | 20, 30, 50, 100 |
| Epistasis method | conditional_llr, additive_deviation |

---

## 6. Metrics from Analogous Optimization Benchmarks

Drawing from cross-domain optimization benchmarks (concept-tree-explorer analysis):

### 6a. Anytime Performance Profile
Plot best solution quality vs. wall-clock time. Useful for comparing optimizers that converge at different rates (beam search may find good solutions early, evolutionary may improve later).

### 6b. Diversity of Top Solutions
Measure pairwise Hamming distance between the top-10 predicted multi-mutant sets. High diversity indicates the optimizer explores different regions of mutation space, which is valuable for experimental validation (hedge bets across different structural mechanisms).

$$\text{Diversity} = \frac{2}{n(n-1)} \sum_{i<j} d_H(S_i, S_j)$$

### 6c. Regret vs. Oracle
Instantaneous regret: $r_t = f(S^*) - f(S_t)$ where $S^*$ is the true best (from brute-force or experimental data) and $S_t$ is the best solution found at time $t$. Cumulative regret tracks optimization efficiency over time.

### 6d. Robustness: Coefficient of Variation Across Seeds
Run each optimizer with 5 different random seeds. Report coefficient of variation (CV = std/mean) of best-found ddG. Low CV indicates robust performance.

---

## 7. Additional Metrics (from Concept-Tree-Explorer Analysis)

The following metrics were identified via concept-tree-explorer cross-domain analysis as important additions beyond standard optimization benchmarks:

### 7a. Expected Calibration Error (ECE)

Measures whether predicted ddG magnitudes are trustworthy (not just rankings):

$$\text{ECE} = \sum_{b=1}^{B} \frac{n_b}{N} \left| \overline{y}_b - \overline{\hat{y}}_b \right|$$

where predictions are binned into $B$ bins, $n_b$ is the count in bin $b$, and $\overline{y}_b, \overline{\hat{y}}_b$ are mean actual and predicted values. Critical for wet-lab go/no-go thresholds.

### 7b. Epistasis Capture Rate

Fraction of known non-additive (epistatic) mutation pairs that the optimizer correctly exploits in its top solutions:

$$\text{ECR} = \frac{|\{(i,j) \in S^* : |\varepsilon_{ij}| > \tau\}|}{|\{(i,j) : |\varepsilon_{ij}| > \tau\}|}$$

where $\tau$ is an epistasis significance threshold (e.g., 0.5 kcal/mol). Directly measures whether StabOpt navigates landscape ruggedness.

### 7c. Fold-Improvement Over Single-Mutant Additivity

$$\text{FIA} = \frac{\Delta\Delta G_{\text{combo}}}{\sum_{i \in S} \Delta\Delta G_i}$$

Values > 1 indicate the optimizer captures synergistic/epistatic effects beyond stacking known singles. This is the fundamental justification for combinatorial search.

### 7d. Experimental Hit Rate at Budget

Given a fixed experimental budget (e.g., 96 variants = one 96-well plate):

$$\text{HitRate@}B = \frac{|\{v \in \text{Top-}B : \Delta\Delta G_{\text{exp}}(v) < -1.0\}|}{B}$$

Grounded in real lab constraints. Report at $B \in \{24, 96, 384\}$ (standard plate formats).

### 7e. Hypervolume Indicator (for Multi-Objective Extension)

For future multi-objective optimization (stability + activity/expression):

$$\text{HV}(\mathcal{P}) = \text{vol}\left(\bigcup_{x \in \mathcal{P}} [f_1(x), r_1] \times [f_2(x), r_2]\right)$$

where $\mathcal{P}$ is the Pareto front and $(r_1, r_2)$ is a reference point. Currently single-objective, but architecture should support multi-objective reporting.

---

## 8. Reporting Format

All benchmark results will be saved in dual format:
- **Machine-readable:** `results/phase4/*.json` with all numeric values
- **Human-readable:** `results/phase4/*.md` with formatted tables and interpretation
- **Figures:** `figures/*.png` (300 DPI) and `figures/*.pdf` for publication

Standard table format:

| Method | Best ddG | Spearman rho | Enrichment@10 | Precision@10 | Time (s) | GPU Mem (GB) |
|--------|----------|--------------|---------------|--------------|----------|--------------|
| Brute-force | ... | ... | ... | ... | ... | ... |
| Greedy | ... | ... | ... | ... | ... | ... |
| Beam search | ... | ... | ... | ... | ... | ... |
| Evolutionary | ... | ... | ... | ... | ... | ... |

Extended table (per ablation):

| Ablation | Best ddG | Spearman rho | ECE | ECR | FIA | Time (s) |
|----------|----------|--------------|-----|-----|-----|----------|
| Baseline | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |
