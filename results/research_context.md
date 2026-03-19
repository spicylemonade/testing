# Research Context

- Stage: post_director_swarm
- Model: gpt-5.4
- Codex model ref: openai/gpt-5.4
- Reasoning effort: xhigh
- Note: gap_queries=4, swarm_agents=4
- Rubric progress: 25/25 completed
- Known papers tracked: 106
- `sources.bib` entries: 14
- Swarm hypotheses: 3
- Verification summary present: yes

## Closest Prior Art
- 
 
 
 
 $$\mathbf {2\times 2}$$
 
 
 2
 ×
 2
 
 
 -Convexifications for convex quadratic optimization with indicator variables (2023)
- On Hopf hypersurfaces of the homogeneous nearly Kähler $${\mathbf {S}}^3\times {\mathbf {S}}^3$$ (2019)
- Continued $\mathbf{A_2}$-fractions and singular functions (2022)
- $\mathbf{\mu}$-Hybrid Inflation and Metastable Cosmic Strings in $\mathbf{SU(3)_c\times SU(2)_L\times SU(2)_R \times U(1)_{B-L}}$ (2025)

## Recent Semantic Scholar Activity
- bibtex :: dc13ea1d96ee60bfaa7a2148e4b5369216f8cd23 (results=1, cache_hits=0, network_calls=1)
- bibtex :: 22a58310070e99febbbe49d0472691a961bb1c70 (results=1, cache_hits=0, network_calls=1)
- search :: Mathematical exploration and discovery at scale (results=5, cache_hits=1, network_calls=0)
- search :: Improved Bounds for Szemeredi's Theorem (results=5, cache_hits=0, network_calls=1)
- search :: Leng Sah Sawhney Kakeya (results=0, cache_hits=0, network_calls=0)

## 2026-03-19 Exact Trace Pivot

- The project now has a working exact rational-span verifier and synchronous
  trace engine in `tools/kakeya_ca_exact.py`.
- The first theory artifact is no longer blocker-shaped: the exact-valid `2x2`
  micro-regime has been exhaustively enumerated in
  `results/theory/forcing_traces/tiny_2x2_full_seeds_le3/`.
- That corpus is rigid: all exact-valid witnesses there have score `7/4` and
  the same two-layer nucleation trace up to the choice of initial corner.
- The one-sided strip-local CA lane has a checked obstruction in widths `2` and
  `3`; see `results/theory/forcing_trace_normal_form.md` and
  `results/theory/local_rule_no_go_atlas.md`.
- The active search question is now narrower:
  can a coupled, non-unilateral strip or macrocell family produce a
  `<= 1.675` witness, or does the local obstruction extend further?
