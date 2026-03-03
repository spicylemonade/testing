# Literature and Code Search Log

Date: 2026-03-03  
Scope: papers, open-source implementations, and state-of-the-art method evidence for a minimal gravity simulator.

## Executed web searches

1. **Papers / methods query**  
   `gravitational n-body symplectic integrator papers Barnes-Hut 2026`  
   Tool: `websearch` (livecrawl preferred)  
   Representative hits: A&A adaptive symplectic integrator (2025), Hernandez & Bertschinger symplectic collisional N-body (ADS), momentum-conserving N-body scheme (New Astronomy).

2. **Open-source repositories query**  
   `GitHub n-body gravity simulation Barnes-Hut repository active 2026`  
   Tool: `websearch` (livecrawl preferred)  
   Representative hits: Barnes-Hut and N-body repositories in Python/C++ (including educational and research implementations).

3. **State-of-the-art scaling query**  
   `state of the art n-body simulation benchmark TreePM fast multipole 2026`  
   Tool: `websearch` (livecrawl preferred)  
   Representative hits: Tree/FMM and cosmological code papers (Treecode2 2026, CUBE2 2025, momentum-conserving FMM 2026).

4. **Canonical algorithm verification query**  
   `Barnes Hut 1986 Nature 324 446 fast multipole Greengard Rokhlin paper`  
   Tool: `websearch` (livecrawl preferred)  
   Representative hits: Nature Barnes-Hut paper page, ADS entries, and JCP Greengard-Rokhlin record.

## Shortlisted sources (>=15)

### Papers (13)

1. Barnes, J., Hut, P. (1986). *A hierarchical O(N log N) force-calculation algorithm*. Nature. https://doi.org/10.1038/324446a0
2. Greengard, L., Rokhlin, V. (1987). *A fast algorithm for particle simulations*. Journal of Computational Physics. https://doi.org/10.1016/0021-9991(87)90140-9
3. Yoshida, H. (1990). *Construction of higher order symplectic integrators*. Physics Letters A. https://doi.org/10.1016/0375-9601(90)90092-3
4. Forest, E., Ruth, R. D. (1990). *Fourth-order symplectic integration*. Physica D. https://doi.org/10.1016/0167-2789(90)90019-L
5. Wisdom, J., Holman, M. (1991). *Symplectic maps for the n-body problem*. Astronomical Journal. https://doi.org/10.1086/115978
6. Duncan, M. J., Levison, H. F., Lee, M. H. (1998). *A Multiple Time Step Symplectic Algorithm for Integrating Close Encounters*. Astronomical Journal. https://doi.org/10.1086/300541
7. Chambers, J. E. (1999). *A hybrid symplectic integrator that permits close encounters between massive bodies*. MNRAS. https://doi.org/10.1046/j.1365-8711.1999.02379.x
8. Springel, V. (2005). *The cosmological simulation code GADGET-2*. MNRAS. https://arxiv.org/abs/astro-ph/0505010
9. Rein, H., Liu, S.-F. (2012). *REBOUND: An open-source multi-purpose N-body code for collisional dynamics*. A&A. https://arxiv.org/abs/1110.4876
10. Rein, H., Spiegel, D. (2015). *IAS15: A fast, adaptive, high-order integrator for gravitational dynamics*. MNRAS. https://arxiv.org/abs/1409.4779
11. Rein, H., Tamayo, D. (2015). *WHFast: A fast and unbiased implementation of a symplectic Wisdom-Holman integrator*. MNRAS. https://arxiv.org/abs/1506.01084
12. Ye, K., et al. (2025). *An adaptive symplectic integrator for gravitational dynamics*. Astronomy & Astrophysics. https://doi.org/10.1051/0004-6361/202451822
13. Barnes, J. E. (2026). *Treecode2: The Power of Pluralism. I. Static Tests*. arXiv. https://arxiv.org/abs/2602.06295

### Code repositories (6)

1. REBOUND (N-body integrators incl. WHFast/SABA). https://github.com/hannorein/rebound
2. SWIFT (parallel gravity + SPH solver). https://github.com/SWIFTSIM/SWIFT
3. GADGET-4 (TreePM/FMM cosmological code). https://gitlab.mpcdf.mpg.de/vrs/gadget4
4. ChaNGa (adaptive cosmological N-body/SPH). https://github.com/N-BodyShop/changa
5. Bonsai (GPU tree code). https://github.com/treecode/Bonsai
6. pytreegrav (minimal Python brute-force + tree gravity). https://github.com/mikegrudic/pytreegrav

## Notes

- The shortlist emphasizes methods transferable to a minimal simulator: deterministic baselines, symplectic integration, and scalable force approximations.
- Bibliographic validation and BibTeX normalization is performed in item_004.
