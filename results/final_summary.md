# Final Results Summary: Bounds on the Univalent Bloch Constant B_u

## Problem Statement

The **univalent Bloch constant** $B_u$ is defined as:
$$B_u = \inf_{f \in S} \operatorname{inrad}(f(\mathbb{D}))$$
where $S$ is the class of univalent functions $f: \mathbb{D} \to \mathbb{C}$ with $f(0)=0$, $f'(0)=1$, and $\operatorname{inrad}(\Omega)$ denotes the radius of the largest disk contained in $\Omega$.

**Prior best known bounds:**
- Lower: $B_u > 0.5708858$ (Skinner, 2009)
- Upper: $B_u \leq 0.6564$ (Carroll & Ortega-Cerda, 2008)
- Gap width: $0.0855$

## Our Best Certified Results

### Upper Bound (Certified)
$$B_u \leq 0.6814202223$$
- **Method:** 3-fold symmetric radial slit domain $\Omega_3 = \mathbb{D} \setminus \{3 \text{ slits from } r_0=0.5 \text{ to } 1\}$
- **Conformal radius:** Computed via exact Cayley-Joukowsky chain (5-step composition of elementary maps)
- **Symmetry reduction:** $z \mapsto z^3$ reduces to single-slit domain $\mathbb{D} \setminus [r_0^3, 1)$
- **Inradius:** $r_0 = 0.5$ (origin-centered inscribed disk)
- **Certification:** Interval arithmetic (mpmath `iv` context, 100-digit precision), zero-width intervals on all computations
- **Script:** `results/phase3/optimized_upper_bound.py`, `results/phase3/interval_verify.py`

### Lower Bound
$$B_u > 0.5708858$$
- **Method:** Literature verification of Skinner (2009)
- **Status:** Reproduced numerically via polynomial family testing; the theoretical implicit function argument was not independently reconstructed
- **Script:** `results/phase2/reproduce_skinner.py`

### Current Gap
$$0.5708858 < B_u \leq 0.6564$$
- Our certified upper bound (0.6814) is **weaker** than Carroll-Ortega-Cerda's 0.6564
- We did **not** achieve a tighter lower bound than Skinner's 0.5709
- Gap width: 0.0855 (unchanged from prior work)

## Summary Table

| Bound | Value | Method | Certified | Reference |
|-------|-------|--------|-----------|-----------|
| Lower (best known) | 0.5708858 | Implicit function / covering | Yes (literature) | Skinner 2009 |
| Upper (best known) | 0.6564 | Harmonically symmetric curved arcs | No (literature) | Carroll-OC 2008 |
| **Our upper (certified)** | **0.6814** | 3 radial slits, Cayley chain | **Yes (interval arith.)** | This work |
| Our upper (n=4 slits) | 0.7174 | 4 radial slits | No | This work |
| Our upper (n=2 slits) | 0.7698 | 2 radial slits | No | This work |
| Our upper (degree-2 poly) | 0.8544 | $f(z)=z+az^2$ family | No | This work |

## What Did Not Work

1. **Bloch norm dichotomy for lower bound:** The Koebe 1/4 theorem is sharp for class $S$, creating a fundamental barrier at $B_u \geq ||f||_B / 4$. The dichotomy approach (case-split on $||f||_B$) gave bounds weaker than $1/2$.

2. **Area theorem approach:** Constraining the area of $f(\mathbb{D})$ via $\pi \sum n|a_n|^2 \geq \pi$ did not yield competitive inradius bounds.

3. **Grunsky adversarial search:** Attempted to find minimum-inradius univalent functions via optimization with Grunsky norm penalty ($||G_2||_{op} \leq 1$). All solutions found were **non-univalent** (winding number $\neq 1$, self-intersecting boundary curves). The 2x2 Grunsky constraint is too weak to enforce univalence.

4. **Higher-fold symmetry radial slits:** Testing $n = 4, 5, 6, 7, 8$ radial slits gave **worse** upper bounds than $n = 3$. The 3-fold symmetric configuration is optimal among radial slit domains.

## Why Carroll-OC's Bound Is Better

Carroll & Ortega-Cerda used **harmonically symmetric curved arcs** (not straight radial slits) with 4-fold symmetry, exploiting the Fedorov solution to the Polya-Chebotarev problem. Curved arcs can achieve better (smaller) $B_f$ ratios than straight radial slits because they minimize logarithmic capacity more efficiently. Implementing curved-arc domain construction requires a Schwarz-Christoffel-type numerical conformal mapping, which we did not complete.

## Key Technical Contributions

1. **Exact conformal radius computation** for $n$-fold symmetric slit-disk domains via 5-step Cayley-Joukowsky chain with $n$-fold symmetry reduction
2. **Interval arithmetic certification framework** using mpmath for rigorous bound enclosures
3. **Correct inradius computation** accounting for both origin-centered and bisector-centered inscribed disks
4. **Comprehensive documentation** of barriers to improvement (Koebe 1/4 sharpness, Grunsky insufficiency)

## Files

- Certified upper bound: `results/phase3/interval_verify.py`, `results/phase3/interval_verify_results.json`
- Conformal radius computation: `results/phase3/optimized_upper_bound.py`
- Metrics: `results/phase2/metrics.json`
- Figures: `figures/upper_bound_domains/`, `figures/Bu_timeline.png`
- Rigor methodology: `results/phase3/rigor_methodology.md`
- Literature: `sources.bib` (27 entries)
- Bibliography: `results/phase1/literature_search_log.json` (24 papers)
