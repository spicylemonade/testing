# Mathematical Formalization of the Chvátal–Sankoff Bound-Tightening Problem

## 1. Precise Definition of γ₂ with Superadditivity Proof Sketch

Let $X = X_1 X_2 \cdots X_n$ and $Y = Y_1 Y_2 \cdots Y_n$ be two independent, uniformly random binary strings of length $n$. Let $\text{LCS}(X, Y)$ denote the length of their longest common subsequence.

**Definition.** The Chvátal–Sankoff constant for binary alphabet is:
$$\gamma_2 := \lim_{n \to \infty} \frac{\mathbb{E}[\text{LCS}(X, Y)]}{n}.$$

**Existence via Superadditivity.** Define $a_n = \mathbb{E}[\text{LCS}(X, Y)]$ for strings of length $n$. The key observation is *superadditivity*: for any $m, n \geq 1$,
$$a_{m+n} \geq a_m + a_n.$$
This follows because an LCS of two $(m+n)$-length strings can be constructed by independently finding LCS of the first $m$ and last $n$ characters. By Fekete's lemma (or equivalently Kingman's subadditive ergodic theorem applied to $-a_n$), $a_n/n$ converges to $\sup_n a_n/n = \gamma_2$ [CS1975, Steele1997].

**Rate of convergence.** Alexander (1994) showed $|a_n/n - \gamma_2| = O(n^{-1/3+\varepsilon})$ for any $\varepsilon > 0$. The KPZ universality conjecture predicts the sharper $a_n = \gamma_2 n + c_1 n^{2/3} + O(n^{1/3})$ [Bundschuh2001].

## 2. Lueker's Lower Bound Framework (DFA + Certificate Vector)

Lueker [L2009] established the most general framework for computer-assisted lower bounds, extending Dancík's earlier work [D1994].

**Framework.** Consider a deterministic finite automaton (DFA) that processes two strings character-by-character and outputs match/no-match decisions. The DFA has state set $S$ and transition function $\delta: S \times \{0,1\} \times \{0,1\} \to S$, with output function $f: S \to \{0, 1\}$.

A *certificate vector* $u: S \to \mathbb{R}$ and rate $r \geq 0$ form a valid lower bound certificate if for all states $x \in S$:
$$\mathbb{E}_{a,b \sim \text{Uniform}(\{0,1\})}[u(\delta(x, a, b))] + f(x) \geq u(x) + r.$$

This ensures that $r$ is a lower bound on $\gamma_2$: by induction, $\mathbb{E}[\text{output after } n \text{ steps}] \geq rn + u(x_0) - \max_{x} u(x)$, giving $\gamma_2 \geq r$.

The optimization problem is:
$$\gamma_2 \geq \max_{u, r} \left\{ r : \mathbb{E}[u(\delta(x, a, b))] + f(x) \geq u(x) + r, \;\forall x \in S \right\}.$$

This is a linear program (LP) in $(u, r)$. The state space grows exponentially with the DFA's buffer size $h$: $|S| = O(2^{2h})$ for binary strings with buffer size $h$.

**Heineman et al. (2024)** [H2024] achieved $\gamma_2 \geq 0.792665992$ by:
- Parallelizing the DFA search across multiple cores
- Implementing efficient recursive memory reading/writing
- Optimizing the feasible triplet enumeration for larger buffer sizes

## 3. Dančík-Paterson / Lueker Upper Bound Framework

The upper bound framework [DP1995, L2009] is based on eigenvalue analysis of a recurrence system.

**Framework.** For a system of size $s$, define a matrix $M$ of dimension $s \times s$ encoding the expected LCS growth rates between string fragments. The recurrence system satisfies:
$$\vec{v}_{t+1} = M \cdot \vec{v}_t + \vec{b}_t$$
where $\vec{v}_t$ tracks the state vector and $\vec{b}_t$ is a source term from character matches.

The upper bound on $\gamma_2$ is determined by the dominant eigenvalue $\lambda_{\max}(M)$:
$$\gamma_2 \leq g(\lambda_{\max}(M))$$
where $g$ is a function depending on the specific recurrence formulation.

**Results:**
- Dančík–Paterson [DP1995]: $\gamma_2 \leq 0.837623$ using a relatively small system
- Lueker [L2009]: $\gamma_2 \leq 0.826280$ using larger systems and computer-assisted verification

The upper bound improves as $s$ increases, but the computational cost grows as $O(s^3)$ for the eigenvalue computation, limiting practical scaling.

## 4. Tiskin's Algebraic Characterization

Tiskin [Tiskin2022] reformulated the problem using stochastic particle processes and cellular automata.

**Particle Process.** The LCS computation can be encoded as an interacting particle system on $\mathbb{Z}$. Particles represent the "wavefront" of the LCS dynamic programming computation. In the stationary regime, the particle density $\rho$ determines $\gamma_2$:
$$\gamma_2 = \frac{1 - \rho}{2} + \frac{1}{2}$$
(exact relationship depends on the particle encoding).

The particle dynamics are related to TASEP (Totally Asymmetric Simple Exclusion Process) and PushTASEP:
- Without labels: the dynamics reduce to a variant of PushASEP [BukhCox2022]
- For periodic initial conditions: exact stationary distributions are known for specific word structures

**Cellular Automaton Formulation.** The LCS computation can also be viewed as a deterministic cellular automaton (CA) applied to random initial conditions. The constant $\gamma_2$ corresponds to the asymptotic slope of the "height function" in the CA spacetime diagram.

**Polynomial System.** For finite system widths $w$, the exact growth rate $\gamma_2(w)$ can be expressed as the root of a polynomial system of equations derived from the transfer matrix of the CA. As $w \to \infty$, $\gamma_2(w) \to \gamma_2$.

## 5. Gap Analysis

### Current State of the Art

| Type | Value | Source | Year |
|------|-------|--------|------|
| Best rigorous lower bound | 0.792665992 | Heineman et al. [H2024] | 2024 |
| Best rigorous upper bound | 0.826280 | Lueker [L2009] | 2009 |
| Best empirical estimate | ~0.8119 | Bundschuh [Bundschuh2001] | 2001 |

**Current gap:** $0.826280 - 0.792666 = 0.033614$

### Theoretical Limits of Each Approach

1. **DFA Lower Bounds (Lueker/Heineman framework):**
   - Provably converge to $\gamma_2$ as buffer size $h \to \infty$
   - Practical limit: $h \approx 16-18$ due to exponential state space growth ($4^h$ states)
   - Estimated achievable improvement: ~0.001-0.005 with massive computation (pushing to h=16-18)
   - **Bottleneck:** Exponential growth of state space in buffer size

2. **Eigenvalue Upper Bounds (Dančík-Paterson/Lueker framework):**
   - Also converge as system size increases
   - Not improved since 2009; the 0.826280 bound uses significant computation
   - Estimated achievable improvement: unclear, possibly 0.001-0.005
   - **Bottleneck:** Matrix dimension growth and numerical stability

3. **Particle Process (Tiskin):**
   - Non-rigorous but potentially high precision via simulation
   - Could inform the search for better certificates
   - **Bottleneck:** No known exact solution for the stationary distribution

4. **Frog Dynamics (Bukh-Cox):**
   - Yields $\gamma_W$ for periodic word $W$ as lower bound on $\gamma_2$
   - Periodic words can be "more random-like than random"
   - **Bottleneck:** Only applies to periodic-vs-random, not random-vs-random

5. **Information-Theoretic Methods:**
   - Deletion channel connections provide structural constraints
   - Entropy-based arguments give concentration bounds
   - **Bottleneck:** Known bounds are weaker than combinatorial methods

### References
- [CS1975] Chvátal & Sankoff 1975
- [D1994] Dancík 1994
- [DP1995] Dančík & Paterson 1995
- [L2009] Lueker 2009
- [H2024] Heineman et al. 2024
- [Tiskin2022] Tiskin 2022
- [BukhCox2022] Bukh & Cox 2022
- [Bundschuh2001] Bundschuh 2001
- [Steele1997] Steele 1997
- [HoudreIslak2014] Houdré & Işlak 2014
- [HauserMartinezMatzinger2006] Hauser, Martínez & Matzinger 2006
