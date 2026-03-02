# Concept: Conservation Laws

- Topic Context: Minimal gravity simulation
- Domains: classical mechanics, numerical analysis, diagnostics
- Purpose: Track physical conservation quantities as simulation quality metrics.

## Conservation Quantities

1. **Total energy**: E = T + V (kinetic + gravitational potential)
2. **Linear momentum**: p = sum(m_i * v_i) -- exactly conserved with paired forces
3. **Angular momentum**: L = sum(m_i * (r_i x v_i)) -- conserved for central forces

## Implementation Backlog
- [x] Define minimal executable artifact for this concept.
- [x] Connect to particle_data_structures (reads state), numerical_integration (quality metric).
- [ ] Add measurable experiment and result file under this folder.
- [x] Add citations from literature.json to sources.bib.
