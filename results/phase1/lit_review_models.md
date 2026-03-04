# Literature Review: Protein Stability Prediction Models

**Date:** 2026-03-04
**Scope:** Computational models for predicting protein thermostability (ddG) from sequence and structure

---

## 1. ESM-2: Evolutionary Scale Modeling

### 1a. ESM-2 Foundation Model

**Title:** Evolutionary-scale prediction of atomic-level protein structure with a language model
**Authors:** Zeming Lin, Halil Akin, Roshan Rao, Brian Hie, Zhongkai Zhu, Wenting Lu, Nikita Smetanin, Robert Verkuil, Ori Kabeli, Yaniv Shmueli, Allan dos Santos Costa, Maryam Fazel-Zarandi, Tom Sercu, Salvatore Candido, Alexander Rives
**Year:** 2023
**Venue:** Science, Vol. 379, Issue 6637
**DOI:** 10.1126/science.ade2574

**Key Findings:**
- ESM-2 is a protein language model trained on millions of protein sequences using masked language modeling
- Scaled up to 15 billion parameters; the 650M parameter version (esm2_t33_650M_UR50D) is the practical workhorse
- Learns evolutionary statistics that encode structural and functional information
- Can be used for zero-shot mutation effect prediction via log-likelihood ratios: score(mutation) = log P(mutant_aa | context) - log P(wildtype_aa | context)
- The masked marginal approach provides a computationally efficient way to score all possible single mutations at a position in one forward pass

### 1b. ESM-2 for Disease Variant Prediction

**Title:** Genome-wide prediction of disease variant effects with a deep protein language model
**Authors:** Nadav Brandes, Grant Goldman, Charlotte H. Wang, Chun Jimmie Ye, Vasilis Ntranos
**Year:** 2023
**Venue:** Nature Genetics, Vol. 55, pp. 1512-1522
**DOI:** 10.1038/s41588-023-01465-0

**Key Findings:**
- Demonstrated ESM-2's effectiveness for predicting pathogenicity of missense variants genome-wide
- ESM-2 log-likelihood ratios correlate with experimental measurements of protein function and stability
- Zero-shot performance competitive with supervised methods trained on specific protein families
- Validated on ClinVar pathogenic/benign classification and deep mutational scanning datasets
- Performance scales with model size, with 650M providing best cost/accuracy tradeoff

### 1c. ESM-1v for Zero-Shot Mutation Effect Prediction

**Title:** Language models enable zero-shot prediction of the effects of mutations on protein function
**Authors:** Joshua Meier, Roshan Rao, Robert Verkuil, Jason Liu, Tom Sercu, Alexander Rives
**Year:** 2021
**Venue:** NeurIPS 2021
**DOI:** 10.1101/2021.07.09.450648

**Key Findings:**
- Introduced the masked marginal scoring approach for zero-shot mutation prediction
- ESM-1v (precursor to ESM-2) achieves state-of-the-art zero-shot performance on deep mutational scanning benchmarks
- Key insight: evolutionary fitness encoded in PLM log-likelihoods correlates with protein stability and function
- Scoring formula: effect(x_i -> x_j) = log p(x_j | x_{mask_i}) - log p(x_i | x_{mask_i})
- This approach requires only 1 forward pass per position (not per mutation)

---

## 2. ProteinMPNN: Structure-Based Sequence Design

### 2a. Core ProteinMPNN Paper

**Title:** Robust deep learning-based protein sequence design using ProteinMPNN
**Authors:** Justas Dauparas, Ivan Anishchenko, Nathaniel Bennett, Hua Bai, Robert J. Ragotte, Lukas F. Milles, Basile I. M. Wicky, Alexis Courbet, Rob J. de Haas, Nate Bethel, Philip J. Y. Leung, Timothy F. Huddy, Sam Pellock, Doug Tischer, Frederick Chan, Brian Koepnick, Hannah Nguyen, Alex Kang, Banumathi Sankaran, Aloke Kumar Bera, Neil P. King, David Baker
**Year:** 2022
**Venue:** Science, Vol. 378, Issue 6615
**DOI:** 10.1126/science.add2187

**Key Findings:**
- Message-passing neural network for protein sequence design from backbone coordinates
- Uses 3D graph representation of protein backbone (N, CA, C, O atoms + virtual CB)
- Autoregressive decoder with random decoding order: models p(sequence | structure)
- Experimental validation: designed sequences fold to intended structures ~50% of the time (vs ~10% for Rosetta)
- Can be used for stability prediction: log p(wildtype_seq | backbone) serves as a structure-sequence compatibility score
- For mutation scoring: compare log p(mutant_aa | backbone, context) vs log p(wt_aa | backbone, context)
- Code: https://github.com/dauparas/ProteinMPNN

### 2b. Inverse Folding for Stability Prediction

**Title:** Zero-shot protein stability prediction by inverse folding models: a free energy interpretation
**Authors:** Jes Frellsen, Maher M. Kassem, Tone Bengtsen, Lars Olsen, Kresten Lindorff-Larsen, Jesper Ferkinghoff-Borg, Wouter Boomsma
**Year:** 2025
**Venue:** arXiv preprint (arXiv:2506.05596)

**Key Findings:**
- Provides theoretical justification for using inverse folding log-likelihoods as stability predictors
- Shows ProteinMPNN log-likelihood ratio approximates ddG under certain thermodynamic assumptions
- The connection between inverse folding scores and free energy is through the Boltzmann distribution
- Competitive with or superior to physics-based methods for stability prediction in zero-shot setting
- Important: ProteinMPNN conditions on backbone structure, making it complementary to sequence-only methods like ESM-2

---

## 3. RaSP: Rapid Stability Prediction

**Title:** Rapid protein stability prediction using deep learning representations
**Authors:** Lasse M. Blaabjerg, Maher M. Kassem, Lydia L. Good, Nicolas Jonsson, Matteo Cagiada, Kristoffer E. Johansson, Wouter Boomsma, Amelie Stein, Kresten Lindorff-Larsen
**Year:** 2023
**Venue:** eLife, 12:e82593
**DOI:** 10.7554/eLife.82593

**Key Findings:**
- Two-stage architecture: (1) self-supervised 3D CNN learns protein structure representations, (2) supervised FCNN predicts ddG from representations
- Trained to predict Rosetta-computed ddG values (not experimental ddG directly)
- Achieves saturation mutagenesis predictions in less than 1 second per residue
- Performance on par with biophysics-based methods (FoldX, Rosetta) but orders of magnitude faster
- Applied to ~300 million stability predictions across the human proteome
- Validated against ProTherm experimental data: Pearson r ~0.5-0.6
- Code: https://github.com/ELELAB/RaSP_workflow
- Key advantage for our pipeline: very fast inference enables exhaustive single-mutation screening

---

## 4. ThermoMPNN and ThermoMPNN-D

### 4a. ThermoMPNN (Single Mutations)

**Title:** Transfer learning to leverage larger datasets for improved prediction of protein stability changes
**Authors:** Henry Dieckhaus, Michael Brocidiacono, Nicholas Randolph, Brian Kuhlman
**Year:** 2024
**Venue:** PNAS, Vol. 121
**DOI:** 10.1073/pnas.2314853121

**Key Findings:**
- Extracts learned embeddings from pretrained ProteinMPNN's decoder layers
- Light attention block reweights embeddings based on learned context
- MLP head predicts ddG from combined embeddings
- Transfer learning from sequence design to stability prediction
- Trained on Mega-scale dataset, achieves state-of-the-art on multiple test sets
- Fast inference: leverages ProteinMPNN's efficient graph neural network architecture
- Code: https://github.com/Kuhlman-Lab/ThermoMPNN

### 4b. ThermoMPNN-D (Double Mutations)

**Title:** Extension of ThermoMPNN for double mutant predictions
**Authors:** Henry Dieckhaus et al.
**Year:** 2024
**Venue:** GitHub / Preprint
**Repository:** https://github.com/Kuhlman-Lab/ThermoMPNN-D

**Key Findings:**
- Siamese neural network architecture for predicting ddG of double point mutations
- Takes two mutant structures as input, processes each through ThermoMPNN, combines representations
- Captures pairwise epistatic interactions between mutations
- Critical for our pipeline: provides direct estimation of pairwise epistasis terms epsilon_{ij}
- Validates that pairwise interactions are significant for proximal mutations (Calpha < 10 Angstroms)
- Key enabler for the additive+pairwise energy model in our optimization framework

---

## 5. Mutate Everything

**Title:** Predicting a Protein's Stability under a Million Mutations
**Authors:** Jeffrey Ouyang-Zhang, Daniel J. Diaz, Adam R. Klivans, Philipp Krahenbuhl
**Year:** 2023
**Venue:** NeurIPS 2023
**arXiv:** 2310.12979

**Key Findings:**
- Simple parallel decoding algorithm: predicts effect of ALL single and double mutations in one forward pass
- Built on ESM-2 and AlphaFold representations (neither trained for stability prediction)
- Trained on Mega-scale cDNA proteolysis dataset
- State-of-the-art on S669, ProTherm, and ProteinGym benchmarks
- Key innovation: parallel decoding avoids O(N*19) forward passes for single mutations
- For double mutations: uses product of marginals approximation, valid under weak epistasis
- Can extend to higher-order mutations with minimal computational overhead
- Demonstrates that structure-aware representations (AlphaFold) improve stability prediction
- Code: https://github.com/jozhang97/MutateEverything
- **Direct relevance to our project:** Validates that ESM-2 + structural features achieve SOTA for stability prediction; the parallel decoding approach informs our efficient scoring strategy

---

## 6. SPURS: Stability Prediction Using Rewired Protein Generative Models

**Title:** Generalizable and scalable protein stability prediction with rewired protein generative models
**Authors:** Ziang Li, Yunan Luo
**Year:** 2025 (published Nature Communications, 2026, Volume 17)
**DOI:** 10.1038/s41467-025-67609-4
**Repository:** https://github.com/luo-group/SPURS

**Key Findings:**
- Rewires and integrates two complementary protein generative models: PLM (ESM-2) and inverse folding model (ProteinMPNN)
- Reprograms unified framework for stability prediction via supervised fine-tuning on mega-scale data
- Delivers accurate, efficient, and scalable stability predictions
- Generalizes to unseen proteins and mutations
- Enables zero-shot identification of functional residues
- Improved low-N protein fitness prediction
- Systematic dissection of stability-pathogenicity relationships
- **Relevance:** Validates our approach of combining ESM-2 + ProteinMPNN scores; SPURS shows this combination is more powerful than either alone

---

## 7. Additional Relevant Models

### 7a. ESM-IF1 (Inverse Folding)

**Title:** Learning inverse folding from millions of predicted structures
**Authors:** Chloe Hsu, Robert Verkuil, Jason Liu, Zeming Lin, Brian Hie, Tom Sercu, Adam Lerer, Alexander Rives
**Year:** 2022
**Venue:** ICML 2022

**Key Findings:**
- ESM-IF1 is Meta's inverse folding model trained on millions of AlphaFold-predicted structures
- GVP-Transformer architecture for structure-conditioned sequence generation
- Can be used as alternative to ProteinMPNN for structure-based mutation scoring
- Trained on much larger dataset than ProteinMPNN but similar architecture philosophy

### 7b. Stability Oracle / AlphaGMut

**Title:** Various approaches using AlphaFold representations for stability prediction
**Year:** 2023-2024

**Key Findings:**
- Multiple groups have built stability predictors on top of AlphaFold structural representations
- Structural features (pLDDT, PAE, backbone coordinates) provide complementary information to sequence-based features
- GNN architectures on structure graphs outperform sequence-only models for local stability effects

### 7c. PILOT: Deep Siamese Network with Hybrid Attention

**Title:** PILOT: Deep Siamese network with hybrid attention improves prediction of mutation impact on protein stability
**Authors:** Yuan Zhang, Junsheng Deng, Mingyuan Dong, Jiafeng Wu, Qiuye Zhao, Xieping Gao, Dapeng Xiong
**Year:** 2025
**Venue:** Neural Networks, Vol. 188

**Key Findings:**
- Siamese network architecture for stability prediction
- Hybrid attention mechanism combines local and global protein context
- Demonstrates importance of capturing mutation context beyond local neighborhood

---

## 8. Protein Language Models and Biophysics

### 8a. PLMs Capture Evolutionary Statistics

**Title:** Protein language models learn evolutionary statistics of interacting sequence motifs
**Authors:** Sergey Ovchinnikov et al.
**Year:** 2024
**Venue:** PNAS

**Key Findings:**
- ESM-2 does not require full sequence context for predicting inter-residue contacts
- PLMs learn coevolutionary statistics comparable to explicit covariance models
- Important limitation: PLMs may not capture biophysical mechanisms beyond evolutionary conservation
- Implications for stability: ESM-2 captures evolutionary constraints (fitness landscape proxy) rather than direct energetic contributions

---

## 9. Summary Table: Model Comparison for Our Pipeline

| Model | Input | Speed (300-res) | Multi-mut | Zero-shot | Trained | Our Use |
|-------|-------|-----------------|-----------|-----------|---------|---------|
| ESM-2 650M | Sequence | ~10s/saturation | Via marginals | Yes | Self-supervised | Primary single-mut scorer |
| ProteinMPNN | Structure | ~5s/saturation | Via conditional | Yes | Inverse folding | Re-ranking + consensus |
| RaSP | Structure | <1s/residue | Additive only | No (Rosetta-trained) | Supervised | Alternative fast scorer |
| ThermoMPNN | Structure | ~5s/saturation | Single only | No (Mega-scale) | Transfer learning | Benchmark comparison |
| ThermoMPNN-D | Structure | ~30s/pair | Double mutants | No | Transfer learning | Epistasis estimation |
| Mutate Everything | Seq + Struct | 1 forward pass | Up to double | No (Mega-scale) | Supervised | Benchmark comparison |
| SPURS | Seq + Struct | Fast | Single | No (Mega-scale) | Fine-tuned | Benchmark comparison |

---

## 10. Key Design Decisions for StabOpt Pipeline

Based on this literature review:

1. **Primary scorer: ESM-2 650M** — Zero-shot, no training data needed, fast masked marginal scoring, well-validated
2. **Structural scorer: ProteinMPNN** — Complementary structure-based information, validated for stability by Frellsen et al.
3. **Epistasis estimation: ESM-2 conditional scoring** — Use conditional log-likelihood shifts (mask position j, score i given mutation at j) for pairwise epistasis, following the Faure et al. (2024) insight that most epistasis is pairwise and distance-dependent
4. **Re-ranking: Combined ESM-2 + ProteinMPNN** — Following SPURS validation that combining PLM and inverse folding improves prediction
5. **Benchmark comparison: Mutate Everything and ThermoMPNN-D** — State-of-the-art supervised methods to compare against

---

## 11. Gaps and Opportunities Identified

1. **No existing tool combines multi-mutation optimization with scoring** — Mutate Everything predicts effects but doesn't optimize; MLDE optimizes but uses simpler models
2. **Pairwise epistasis is sufficient for most proteins** — Faure et al. (2024) shows higher-order epistasis is rare for stability, validating our additive+pairwise model
3. **Parallel decoding is underexploited for optimization** — Mutate Everything's parallel approach could be integrated into beam search for faster scoring
4. **GPU budget alignment** — All models (ESM-2 650M, ProteinMPNN) fit within A100 memory and can score a 300-residue protein in under 60 seconds

---

*15 papers reviewed. References are tracked in sources.bib.*
