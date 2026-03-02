# Concept: Visualization

- Topic Context: Minimal gravity simulation
- Domains: scientific visualization, data presentation, publication graphics
- Purpose: Generate publication-quality figures for all experiments and benchmarks.

## Plot Types

1. **Trajectory plots**: x-y orbit paths with body markers
2. **Energy drift plots**: relative energy error vs time
3. **Convergence plots**: error vs dt on log-log scale
4. **Scaling plots**: wall-clock time vs N on log-log scale
5. **Multi-panel summary**: Combined performance figures

## Implementation Backlog
- [ ] Define matplotlib rcParams for publication styling.
- [ ] Connect to all benchmark outputs for automated figure generation.
- [ ] Generate both PNG (300 DPI) and PDF for each figure.
- [ ] Add consistent color scheme across all figures.
