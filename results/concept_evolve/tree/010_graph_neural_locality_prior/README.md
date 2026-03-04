# 010 — Graph Neural Locality Prior

## Topic Context

Protein mutations don't interact randomly — their epistasis is strongly correlated with structural proximity. Two mutations in the same hydrophobic core cluster interact far more than two mutations on opposite surfaces. This structural locality is well-established in biophysics but underexploited in combinatorial optimization algorithms.

Graph neural networks provide a natural framework to learn this structure-epistasis mapping. Recent structure-based stability predictors like **Stability Oracle** (Nature Communications 2024) and **Pythia** (Innovation 2025) demonstrate that GNNs can accurately predict stability effects from local structural context. Extending this to **pairwise** epistasis prediction (not just single-mutation effects) enables structure-aware decomposition of the search space.

The key computational insight: if a GNN can predict which position pairs have significant epistasis without running the expensive double-mutant evaluations, it can guide the sparse decomposition approach (Concept 002) with zero additional scorer calls. The GNN serves as a "meta-predictor" that predicts which predictions matter.

## Key Connections

- **Pre-trained structure encoders**: Frozen ProteinMPNN/GVP-GNN encoders provide rich structural features without training from scratch
- **Transfer from single-mutant to pairwise**: GNN learns structural patterns that generalize across proteins

## Implementation Backlog

1. [ ] Implement protein contact graph construction from PDB file
2. [ ] Implement feature extraction using frozen ProteinMPNN encoder
3. [ ] Design and train MLP for pairwise epistasis prediction
4. [ ] Build training pipeline on Mega-scale double mutant data
5. [ ] Evaluate epistasis prediction accuracy on held-out proteins
6. [ ] Implement position clustering from predicted interaction graph
7. [ ] Integrate with sparse decomposition search (Concept 002)
8. [ ] Compare GNN-guided vs distance-only thresholding for clustering
9. [ ] Ablate: frozen vs fine-tuned structure encoder
10. [ ] Measure end-to-end search improvement from GNN prior
