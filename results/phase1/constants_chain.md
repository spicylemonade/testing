# The Chain B ≤ B_l ≤ L ≤ B_u: Known Bounds

## Definitions

| Constant | Symbol | Definition |
|----------|--------|------------|
| **Bloch constant** | B | $\inf\{B_f : f \in \mathcal{F}\}$ where $B_f$ = radius of largest univalent disk in $f(\mathbb{D})$ |
| **Locally univalent Bloch constant** | $B_l$ | $\inf\{B_f : f \in \mathcal{F}, f \text{ is locally univalent}\}$ |
| **Landau constant** | L | $\inf\{d(0, \partial f(\mathbb{D})) : f \in \mathcal{F}\}$ (distance from origin to boundary of image) |
| **Univalent Bloch constant** | $B_u$ | $\inf\{B_f : f \in \mathcal{F}, f \text{ is univalent in } \mathbb{D}\}$ |

Here $\mathcal{F} = \{f : \mathbb{D} \to \mathbb{C} \text{ holomorphic}, f'(0)=1\}$.

The chain $B \le B_l \le L \le B_u$ holds because:
- Adding local univalence restricts the class (increases infimum): $B \le B_l$
- For locally univalent $f$, $B_f \ge d(0, \partial f(\mathbb{D}))$ since the image contains a disk of radius $B_f$ and the boundary is at least $d(0,\partial f(\mathbb{D}))$ away: $B_l \le L$
- Univalent functions are locally univalent, and for univalent $f$, $f(\mathbb{D})$ itself is a simply connected domain containing an open disk: $L \le B_u$

## Comprehensive Bounds Table

| Constant | Best Lower Bound | Lower Ref | Best Upper Bound | Upper Ref | Conjectured Value |
|----------|-----------------|-----------|-----------------|-----------|-------------------|
| **B** | $\frac{\sqrt{3}}{4} + 2 \times 10^{-4} \approx 0.4332$ | Chen-Gauthier 1996 \cite{chengauthier1996} | $\frac{1}{\sqrt{1+\sqrt{3}}} \cdot \frac{\Gamma(1/3)\Gamma(11/12)}{\Gamma(1/4)} \approx 0.4719$ | Ahlfors-Grunsky 1937 \cite{ahlforsgrunsky1937} | $\frac{1}{\sqrt{1+\sqrt{3}}} \cdot \frac{\Gamma(1/3)\Gamma(11/12)}{\Gamma(1/4)} \approx 0.4719$ (Ahlfors-Grunsky conjecture) |
| **$B_l$** | $\frac{1}{2} + 10^{-335}$ | Yanagihara 1995 \cite{yanagihara1995} | Unknown explicit bound less than L | — | Unknown |
| **L** | $\frac{1}{2} + 10^{-335}$ | Yanagihara 1995 \cite{yanagihara1995} | $\frac{\Gamma(1/3)\Gamma(5/6)}{\Gamma(1/6)} \approx 0.5433$ | Rademacher (see \cite{bhowmiksen2023}) | $\frac{\Gamma(1/3)\Gamma(5/6)}{\Gamma(1/6)} \approx 0.5433$ (conjectured) |
| **$B_u$** | $0.5708858$ | Skinner 2009 \cite{skinner2009} | $\approx 0.6564$ | Carroll-Ortega-Cerdà 2009 \cite{carrollortegacerda2009} | Unknown |

## Detailed Bounds History

### Bloch Constant B

| Year | Bound | Author(s) | Reference |
|------|-------|-----------|-----------|
| 1925 | $B \ge 1/72$ | Bloch | (original theorem) |
| 1929 | $B \ge 1/16$ | Landau | \cite{landau1929} |
| 1937 | $B \le 0.4719...$ | Ahlfors-Grunsky | \cite{ahlforsgrunsky1937} |
| 1937 | $B \ge \sqrt{3}/4 \approx 0.4330$ | Ahlfors | (Ahlfors' method) |
| 1990 | $B > \sqrt{3}/4$ (strict) | Bonk | \cite{bonk1990} |
| 1996 | $B \ge \sqrt{3}/4 + 2 \times 10^{-4}$ | Chen-Gauthier | \cite{chengauthier1996} |

The Ahlfors-Grunsky conjecture states $B = \frac{\Gamma(1/3)\Gamma(11/12)}{\Gamma(1/4)\sqrt{1+\sqrt{3}}}$, with the extremal function arising from the hexagonal lattice universal covering. Baernstein-Vinson \cite{baernsteinvinson1998} proved local minimality.

### Locally Univalent Bloch Constant $B_l$

| Year | Bound | Author(s) | Reference |
|------|-------|-----------|-----------|
| 1995 | $B_l > 1/2 + 10^{-335}$ | Yanagihara | \cite{yanagihara1995} |

This constant is the least studied. The lower bound follows from Yanagihara's distortion theorem for locally univalent functions.

### Landau Constant L

| Year | Bound | Author(s) | Reference |
|------|-------|-----------|-----------|
| 1929 | Existence | Landau | \cite{landau1929} |
| — | $L \le \Gamma(1/3)\Gamma(5/6)/\Gamma(1/6)$ | Rademacher | (see \cite{bhowmiksen2023}) |
| 1995 | $L > 1/2 + 10^{-335}$ | Yanagihara | \cite{yanagihara1995} |

The gap between bounds is enormous: $0.5000... < L \le 0.5433...$

### Univalent Bloch Constant $B_u$

| Year | Bound | Author(s) | Reference |
|------|-------|-----------|-----------|
| 1935 | $B_u \ge 0.5$ (approx) | Robinson | \cite{robinson1935} |
| 1945 | $B_u \le 0.6565$ | Goodman | \cite{goodman1945} |
| 1969 | Improved lower | Toppila | \cite{toppila1969} |
| 1985 | $B_u > 0.5$ | Beller-Hummel | \cite{bellerhummel1985} |
| 1992 | Extremal domain criterion | Jenkins | \cite{jenkins1992} |
| 1998 | Refined criterion | Jenkins | \cite{jenkins1998} |
| 2008 | Extended Jenkins condition | Carroll | \cite{carroll2008} |
| 2009 | $B_u \le 0.6564$ | Carroll-Ortega-Cerdà | \cite{carrollortegacerda2009} |
| 2009 | $B_u > 0.5708858$ | Skinner | \cite{skinner2009} |

## Gap Analysis

| Gap | Lower | Upper | Width | Notes |
|-----|-------|-------|-------|-------|
| B | 0.4332 | 0.4719 | 0.0387 | Moderately narrow; conjecture for exact value exists |
| $B_l$ | 0.5000+ | ≤ L ≤ 0.5433 | ~0.043 | Very wide given tiny excess over 1/2 |
| L | 0.5000+ | 0.5433 | ~0.043 | Conjecture for exact value exists |
| $B_u$ | 0.5709 | 0.6564 | 0.0855 | **Widest gap; most room for improvement** |

## Implications for This Research

The $B_u$ gap is the widest in the chain at ~0.0855. This means:
1. **Lower bound improvement** is the most impactful target (Skinner's 0.5708858 could potentially be pushed significantly)
2. **Upper bound improvement** via better domain constructions also has room
3. The chain $B \le B_l \le L \le B_u$ means any improvement to $B_u$'s lower bound does NOT automatically improve bounds for B, $B_l$, or L (since $B_u$ is the largest)
4. However, if we could show $B_u = L$ (or $B_u$ close to L), this would dramatically narrow the gap
5. No conjectured exact value for $B_u$ exists, unlike B and L

The key question remains: **Is there an extremal univalent function for $B_u$, and what does its domain look like?** Jenkins' criterion \cite{jenkins1992} constrains the extremal domain structure, but doesn't determine it uniquely.
