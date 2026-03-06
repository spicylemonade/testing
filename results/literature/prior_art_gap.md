# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## 1. Data-constrained Solar Modeling with GX Simulator (2023)
- Paper ID: bd50997571a7999ceaf12197ab820c425631421f
- Why it is close: keyword overlap on `simulator` made it look relevant, and it is a real physics simulator with a modular pipeline.
- Differentiation hypothesis: GX Simulator is a domain-specific solar modeling framework with 3D plasma and emission pipelines, while this project is a tiny Newtonian reference kernel for 2-body, 3-body, and small-N audit controls.
- Evidence artifact(s): `results/problem_statement.md`, `results/repository_map.md`, `results/literature/literature_snapshot.json`
- Pivot decision (if any): 2026-03-06 - treat GX Simulator as evidence that domain-specific simulator breadth is crowded, and pivot away from solar-application claims.

## 2. Three‐axis borehole gravity monitoring for CO2 storage using machine learning coupled to fluid flow simulator (2023)
- Paper ID: 3ddfb5c4a4c83fcd45bd80b426cca5d0913876ce
- Why it is close: the title contains both `gravity` and `simulator`, so naive term matching surfaced it despite the application mismatch.
- Differentiation hypothesis: the borehole paper solves a geophysical inverse problem with fluid-flow and machine-learning coupling, whereas our contribution is a deterministic orbital reference kernel with invariant and reproducibility audits.
- Evidence artifact(s): `results/problem_statement.md`, `results/literature/literature_snapshot.json`
- Pivot decision (if any): 2026-03-06 - explicitly drop reservoir-monitoring and inversion branches from scope because they do not constrain the Newtonian orbital simulator wedge.

## 3. Trajectories of Bright Stars and Shadows around Supermassive Black Holes as Tests of Gravity Theories (2023)
- Paper ID: c9a20991b1b285556a28f638ae035c08a1299dfe
- Why it is close: it studies gravity trajectories and could be mistaken for a close astrophysical neighbor if one ignores regime and theory differences.
- Differentiation hypothesis: that paper tests relativistic and alternative-gravity behavior around supermassive black holes, while this project stays in the Newtonian regime and claims novelty only in auditability, benchmark discipline, and reproducibility.
- Evidence artifact(s): `results/problem_statement.md`, `results/research_context.md`, `results/literature/literature_snapshot.json`
- Pivot decision (if any): 2026-03-06 - keep strong-gravity and relativistic claims out of scope and use this paper only as a reminder not to overstate physical regime coverage.

## 4. Gravity-perfused airway-on-a-chip optimized for quantitative BSL-3 studies of SARS-CoV-2 infection: barrier permeability, cytokine production, immunohistochemistry, and viral load assays (2024)
- Paper ID: 69513a76597e491bea90b256f0289cdc8b3b4c67
- Why it is close: only because the keyword `gravity` appears in the title; scientifically it is an unrelated biomedical microfluidics system.
- Differentiation hypothesis: the airway-on-a-chip work has no overlap with Newtonian orbital integration, so its value is as a diagnostic failure case for bad search recall rather than as a near-neighbor method.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/literature/prior_art_watchlist.md`
- Pivot decision (if any): 2026-03-06 - record this as a false-positive watchlist hit and pivot the literature program toward REBOUND, poliastro, PhET, Orekit, and determinism sources.

## 5. Virtual cone-beam computed tomography simulator with human phantom library and its application to the elemental material decomposition. (2023)
- Paper ID: 820f018732b9de1cfb9bc740b24b1cbb428cd34a
- Why it is close: another false positive produced by the word `simulator` without meaningful gravitational or orbital overlap.
- Differentiation hypothesis: this is a medical imaging simulator, not a gravity dynamics system, so it serves only as evidence that generic task-string search was too noisy.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/literature/prior_art_watchlist.md`
- Pivot decision (if any): 2026-03-06 - retire this branch and rely on targeted gravity-simulation neighbors for all future novelty checks.
