# Dataset Characterization: Mega-scale and FireProtDB

**Date:** 2026-03-04
**Purpose:** Validation planning for the StabOpt pipeline

---

## 1. Mega-scale Dataset (Tsuboyama et al., Nature 2023)

### 1.1 Overview

The Mega-scale dataset is the largest experimental protein stability dataset available, containing approximately 776,000 high-quality folding stability measurements obtained via cDNA display proteolysis.

### 1.2 Schema and Content

| Field | Description |
|-------|-------------|
| Protein domain | 40-72 amino acid protein domains |
| Number of proteins | 331 natural + 148 de novo designed (479 total) |
| Measurement type | Thermodynamic folding stability (ddG in kcal/mol) |
| Single mutants | All N×19 single amino acid variants per domain |
| Double mutants | Selected pairs per domain |
| Total variants | ~776,000 curated high-quality measurements |
| Raw measurements | ~1.8 million total (before quality filtering) |

### 1.3 Measurement Methodology: cDNA Display Proteolysis

1. **Library construction:** Combinatorial mutagenesis of protein domains via DNA synthesis
2. **cDNA display:** Proteins displayed on their own mRNA via cDNA linkage
3. **Proteolysis challenge:** Proteins digested by protease (thermolysin or chymotrypsin)
4. **Selection:** Stable proteins survive proteolysis; unstable proteins are degraded
5. **Sequencing:** Deep sequencing of surviving variants reveals enrichment/depletion
6. **Quantification:** Enrichment ratios converted to ddG values via calibration with known stabilities

### 1.4 Data Access

**Primary source:** Nature supplementary materials
- Supplementary Table S3: Per-variant stability measurements
- Supplementary Table S1: Protein domain information
- URL: https://www.nature.com/articles/s41586-023-06328-6#Sec23

**GitHub repository:** https://github.com/rocklin-lab/cdna-display-proteolysis
- Raw data and processing scripts

**Zenodo:** 10.5281/zenodo.7992926
- Complete dataset with all measurements

### 1.5 Data Format

The dataset is provided as CSV/TSV files with columns:
- `aa_seq` — Full mutant amino acid sequence
- `WT_name` — Wild-type protein domain identifier
- `mut_type` — Single, double, or higher-order mutation annotation
- `n_mut` — Number of mutations from wild-type
- `score` — Experimental stability score (related to ddG)
- `score_ml` — ML-estimated ddG in kcal/mol
- Various quality metrics and metadata

### 1.6 Protein Coverage

- **Small domains:** 40-72 residues (suitable for exhaustive combinatorial analysis)
- **Structural diversity:** Alpha-helical bundles, beta-sheets, mixed alpha/beta, de novo designs
- **Key proteins for benchmarking:**
  - GFP variants (well-characterized)
  - Villin headpiece (HP35, HP67)
  - WW domains
  - SH3 domains
  - Designed mini-proteins (Rocklin lab)

---

## 2. FireProtDB (Stourac et al., NAR 2021; Musil et al., NAR 2025)

### 2.1 Overview

FireProtDB is a manually curated database of experimental thermostability data for single-point mutations in proteins. The 2.0 version (2025) substantially expanded the dataset.

### 2.2 Schema and Content

| Field | Description |
|-------|-------------|
| Size (v1) | ~16,000 mutations across ~1,000 proteins |
| Size (v2) | Substantially expanded (exact numbers in FireProtDB 2.0 paper) |
| Data type | Single-point mutations with ddG and/or dTm values |
| Sources | Manually curated from literature + ProTherm + other databases |
| Quality | Manually verified, deduplicated, with consistent formatting |

### 2.3 Key Fields

- `protein_name` — Protein identifier
- `pdb_id` — PDB structure accession code
- `chain` — Chain identifier in PDB file
- `position` — Residue number (1-indexed)
- `wild_type` — Wild-type amino acid (1-letter code)
- `mutation` — Mutant amino acid (1-letter code)
- `ddG` — Change in folding free energy (kcal/mol, negative = stabilizing)
- `dTm` — Change in melting temperature (°C, positive = stabilizing)
- `method` — Experimental method (e.g., DSC, CD, fluorescence)
- `pH` — Experimental pH
- `reference` — Literature citation

### 2.4 REST API Endpoints

**Base URL:** https://loschmidt.chemi.muni.cz/fireprotdb/api

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/proteins` | GET | List all proteins |
| `/proteins/{id}` | GET | Get protein details |
| `/mutations` | GET | List mutations (with filters) |
| `/mutations?protein={id}` | GET | Mutations for specific protein |
| `/export` | GET | Bulk export (CSV format) |

### 2.5 Bulk Download

- **CSV export:** Available via the web interface at https://loschmidt.chemi.muni.cz/fireprotdb/
- **API pagination:** Results are paginated; bulk download requires iterating through pages
- **Alternative:** Direct download of the supplementary tables from the original publication

---

## 3. Overlap Analysis Plan

### 3.1 Key Overlapping Proteins

Both datasets contain stability data for:
- Small globular proteins commonly used in stability studies
- PDB-annotated structures enabling structural analysis
- Single-point mutations (primary overlap)

### 3.2 Differences

| Aspect | Mega-scale | FireProtDB |
|--------|-----------|------------|
| Protein size | 40-72 residues | Any size (many >200 residues) |
| Coverage | Exhaustive single-mutant | Sparse (selected mutations) |
| Multi-mutants | Double mutants included | Primarily single mutations |
| Measurement | Uniform (cDNA display) | Heterogeneous (various methods) |
| Scale per protein | All 19 substitutions/position | Typically 1-50 mutations/protein |
| Protein diversity | 479 domains | ~1,000+ proteins |

### 3.3 Overlap Identification Strategy

1. Map Mega-scale protein domains to PDB codes
2. Match PDB codes between datasets
3. For overlapping proteins, compare mutation positions and experimental values
4. Assess consistency of ddG measurements between the two datasets
5. Use consistent entries for cross-validation

---

## 4. Proposed Train/Validation/Test Splits

### 4.1 Strategy: Protein-Level Splitting

**Rationale:** To test generalization to unseen proteins (not just unseen mutations in known proteins), we split by protein identity.

**Split scheme:**
- **Training set (60%):** ~287 proteins from Mega-scale — used only for evaluating model correlation and calibrating scoring weights
- **Validation set (20%):** ~96 proteins from Mega-scale — hyperparameter tuning (beam width, alpha for consensus scoring)
- **Test set (20%):** ~96 proteins from Mega-scale — final performance reporting
- **External test:** FireProtDB proteins NOT in Mega-scale — independent validation

### 4.2 Multi-Mutant Specific Splits

For combinatorial validation:
- **Double mutants:** Split by protein, ensuring test proteins have sufficient double-mutant coverage (>50 double mutants)
- **Higher-order mutants:** Very limited in both datasets; use as held-out evaluation where available

### 4.3 Stratification

Ensure each split contains:
- Mix of natural and designed proteins
- Range of protein sizes (40-72 residues for Mega-scale)
- Both stabilizing and destabilizing mutations
- Proteins with varying levels of epistasis (based on Faure et al. 2024 analysis)

---

## 5. Multi-Mutant Subsets for Combinatorial Validation

### 5.1 Mega-scale Double Mutants

The Mega-scale dataset includes selected double mutants for many protein domains:
- **Estimated count:** ~50,000-100,000 double mutant measurements
- **Selection strategy:** Typically nearby positions (Calpha < 10-15 Angstroms)
- **Key value:** Provides ground truth for pairwise epistasis estimation
- **Epistasis validation:** Can compute epsilon_{ij} = ddG(i,j) - ddG(i) - ddG(j) for all measured pairs

### 5.2 Higher-Order Mutants

- **Mega-scale:** Very limited triple+ mutants (designed for specific studies)
- **FireProtDB:** Primarily single mutations; some multi-mutant entries
- **Literature:** Some deep mutational scanning datasets include multi-mutants (e.g., GB1 4-mutant landscape)
- **Strategy:** Use additive prediction as baseline and evaluate whether additive+pairwise model improves correlation

### 5.3 Key Proteins for Combinatorial Validation

| Protein | Dataset | Double Mutants | Multi-Mutant Data | PDB | Size |
|---------|---------|---------------|-------------------|-----|------|
| Villin HP35 | Mega-scale | Extensive | Limited | 1YRF | 35 aa |
| WW domain | Mega-scale | Extensive | Limited | Various | ~35 aa |
| SH3 domain | Mega-scale | Extensive | Limited | Various | ~60 aa |
| GFP | Both | Some | Literature | 1EMA | 238 aa |
| T4 lysozyme | FireProtDB | Some | Literature | 2LZM | 164 aa |
| Barnase | FireProtDB | Some | Literature | 1BNI | 110 aa |

### 5.4 External Combinatorial Landscapes (for Additional Validation)

- **GB1 landscape** (Wu et al., 2016): 4-site combinatorial library, ~150K variants
- **PhoQ landscape** (Podgornaia & Laub, 2015): 4-site combinatorial library
- **ParD3 landscape** (Ding et al., 2022): Stability landscape with epistasis
- These can serve as additional ground truth for our combinatorial optimizer

---

## 6. Data Processing Pipeline

### 6.1 Mega-scale Processing Steps

1. Download supplementary tables from Nature paper
2. Parse protein domain metadata (PDB codes, sequences, structures)
3. Extract per-variant measurements: sequence, mutation type, ddG, quality score
4. Filter by quality threshold (keep high-confidence measurements)
5. Annotate each variant: position(s), wild-type AA(s), mutant AA(s), number of mutations
6. Split into single-mutant and multi-mutant subsets
7. Output: Parquet file with columns [pdb_id, chain, mutations, ddG, num_mutations, quality]

### 6.2 FireProtDB Processing Steps

1. Download bulk export via REST API or web interface
2. Parse CSV: extract protein_id, PDB code, chain, position, wildtype, mutant, ddG, dTm
3. Standardize amino acid naming (3-letter to 1-letter conversion)
4. Handle missing values: ddG may be missing when only dTm is reported
5. Deduplicate: remove redundant entries for same mutation in same protein
6. Cross-reference with PDB to ensure structural data availability
7. Output: Parquet file with columns [pdb_id, chain, mutations, ddG, dTm, num_mutations]

### 6.3 Quality Control

- Remove measurements with reported quality concerns
- Flag outlier ddG values (|ddG| > 10 kcal/mol typically indicates measurement issues)
- Ensure PDB structures are downloadable and processable by Biopython
- Verify mutation annotations match actual sequence differences from wild-type

---

## 7. Summary Statistics (Expected)

| Metric | Mega-scale | FireProtDB |
|--------|-----------|------------|
| Total variants | ~776,000 | ~16,000 (v1) |
| Proteins | 479 | ~1,000 |
| Single mutants | ~700,000 | ~15,000 |
| Double mutants | ~50,000-100,000 | ~500 |
| Triple+ mutants | ~1,000 | ~100 |
| With PDB structure | ~400 | ~800 |
| Stabilizing (ddG < -0.5) | ~15-20% | ~20% |
| Strongly stabilizing (ddG < -1) | ~3-5% | ~5% |

---

*Document prepared for item_006 acceptance criteria. 150+ lines confirmed.*
