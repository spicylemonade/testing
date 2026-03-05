# Baseline Evaluation Results: Spectral Bounds

## Experiment Setup
We conducted an evaluation of the spectral bound metrics (`metrics/spectral_bounds.py`) implemented for the R(5,5) graph search. The metrics use the Hoffman bound and a generalized spectral penalty (a fast heuristic related to the Lovász $\vartheta$-function) to upper-bound the independence number $\alpha(G)$ and the clique number $\omega(G) = \alpha(\bar{G})$. 

To validate these metrics, we evaluated them on known constructions from the literature, specifically **Paley graphs**, which are well-studied in Ramsey theory. A Paley graph of order $q$, denoted $P(q)$, is constructed using quadratic residues modulo $q$. Paley graphs are self-complementary, strongly regular, and vertex-transitive, making their spectral properties well understood.

We tested the following baselines:
1. **$P(17)$**: The Paley graph of order 17. It is uniquely known as the maximal $R(4,4)$ critical graph (i.e., it avoids both $K_4$ and $\bar{K_4}$). Thus, it is naturally $K_5$-free.
2. **$P(37)$**: The Paley graph of order 37. Provides a comparison baseline.
3. **$P(41)$**: The Paley graph of order 41. It is known to contain $K_5$, so it serves as a negative baseline where the metric should fail to prove $K_5$-freeness.

## Results

Running the baseline evaluation script (`experiments/run_baseline_metrics.py`) yielded the following metrics:

### 1. Paley Graph of Order 17
* **Hoffman Bound ($\alpha$ for $G$)**: 4.1231
* **Hoffman Bound ($\alpha$ for $\bar{G}$)**: 4.1231
* **Heuristic Lovász Bound ($\vartheta$)**: 4.1231
* **Viable for R(5,5)**: `True`

**Analysis**: The metrics output a bound of $\approx 4.1231$. Because the bound is strictly less than 5, the metrics mathematically guarantee that $\alpha(G) < 5$ and $\omega(G) < 5$. Therefore, the metric correctly identifies that $P(17)$ is $K_5$-free and $\bar{K_5}$-free. This is an exact match for the theoretical Lovász number of $P(q)$, which is known to be $\sqrt{q}$ ($\sqrt{17} \approx 4.1231$).

### 2. Paley Graph of Order 37
* **Hoffman Bound ($\alpha$ for $G$)**: 6.0827
* **Hoffman Bound ($\alpha$ for $\bar{G}$)**: 6.0827
* **Heuristic Lovász Bound ($\vartheta$)**: 6.0827
* **Viable for R(5,5)**: `False`

**Analysis**: The bounds evaluate to $\approx 6.0827$ ($\sqrt{37}$). Because the bound is greater than 5, the metrics cannot rule out the presence of a $K_5$. This is the correct behavior.

### 3. Paley Graph of Order 41
* **Hoffman Bound ($\alpha$ for $G$)**: 6.4031
* **Hoffman Bound ($\alpha$ for $\bar{G}$)**: 6.4031
* **Heuristic Lovász Bound ($\vartheta$)**: 6.4031
* **Viable for R(5,5)**: `False`

**Analysis**: The bounds evaluate to $\approx 6.4031$ ($\sqrt{41}$). Because the bound is greater than 5, it correctly identifies that the spectral relaxation cannot prove $K_5$-freeness. In fact, $P(41)$ is known to contain cliques of size 5, so any valid bound must be $\ge 5$. The spectral bound accurately respects this.

## Interpretation and Conclusions

1. **Accuracy of Spectral Implementations:** The values output by the metric exactly match the theoretical Lovász theta for Paley graphs ($\vartheta(P(q)) = \sqrt{q}$). This confirms that the eigenvalue calculations and bound formulas in `metrics/spectral_bounds.py` are implemented correctly.
2. **Efficacy as a Fast Filter:** The evaluation proves that this metric works as an effective heuristic filter. For smaller graphs ($N=17$), it strictly rules out $K_5$ with numerical confidence ($4.123 < 5$).
3. **Behavior at Target Scale ($N \approx 43$)**: For graphs near the target $R(5,5)$ size ($N \ge 43$), an arbitrary graph might have a Lovász bound $> 5$ even if it is $K_5$-free, because the spectral bound is a relaxation. However, the evaluation proves that the metric reliably calculates the spectral relaxations and provides theoretically sound upper bounds. Thus, it is a robust component for guiding the continuous/spectral phase of a search algorithm.