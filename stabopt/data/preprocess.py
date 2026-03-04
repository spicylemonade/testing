"""Preprocess downloaded datasets into analysis-ready parquet files.

Produces:
- results/data/megascale_processed.parquet
- results/data/fireprotdb_processed.parquet
- results/data/multimutant_subset.parquet

Reference: Tsuboyama et al. (2023), Stourac et al. (2021)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from stabopt.data.download import DATA_DIR, download_megascale, download_fireprotdb


def preprocess_megascale(
    input_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> pd.DataFrame:
    """Preprocess the Mega-scale dataset into standardized format.

    Handles the real Tsuboyama et al. 2023 Dataset2/3 format from Zenodo,
    which has columns: name, mut_type, WT_name, aa_seq, ddG_ML, deltaG, etc.

    Args:
        input_path: Path to raw CSV. If None, looks for extracted Zenodo data.
        output_dir: Output directory for parquet. If None, uses DATA_DIR.

    Returns:
        Processed DataFrame
    """
    out = Path(output_dir) if output_dir else DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    # Try to find the real Tsuboyama dataset first
    zenodo_path = out / "Processed_K50_dG_datasets" / "Tsuboyama2023_Dataset2_Dataset3_20230416.csv"

    if input_path is not None:
        raw_path = Path(input_path)
    elif zenodo_path.exists():
        raw_path = zenodo_path
    else:
        raw_path = download_megascale(str(out))

    print(f"Reading Mega-scale data from {raw_path}...")
    df = pd.read_csv(raw_path, low_memory=False)
    print(f"  Raw rows: {len(df):,}")
    print(f"  Columns: {list(df.columns)}")

    # Check if this is the real Tsuboyama dataset
    if "WT_name" in df.columns and "mut_type" in df.columns:
        processed = _process_tsuboyama_format(df)
    else:
        # Fallback to generic detection
        col_map = _detect_megascale_columns(df)
        processed = _process_generic_format(df, col_map)

    # Drop rows with missing ddG
    initial_len = len(processed)
    processed = processed.dropna(subset=["ddG"]).reset_index(drop=True)
    print(f"  After dropping NaN ddG: {len(processed):,} (removed {initial_len - len(processed):,})")

    # Save
    dest = out / "megascale_processed.parquet"
    processed.to_parquet(dest, index=False)
    print(f"  Saved to {dest}")

    # Print summary
    _print_summary("Mega-scale", processed)

    return processed


def _process_tsuboyama_format(df: pd.DataFrame) -> pd.DataFrame:
    """Process the real Tsuboyama et al. 2023 Dataset 2/3 format."""
    processed = pd.DataFrame()

    # Protein identifier (WT_name contains PDB names like "1A32.pdb")
    processed["pdb_id"] = df["WT_name"].astype(str).str.replace(".pdb", "", regex=False)
    processed["chain"] = "A"

    # Mutation string from mut_type (format: "A10G" or "A10G:L20F")
    processed["mutations"] = df["mut_type"].astype(str).str.replace(":", "+")

    # ddG value — use ddG_ML (ML-corrected stability change)
    processed["ddG"] = pd.to_numeric(df["ddG_ML"], errors="coerce")

    # Also keep deltaG (experimental) if available
    if "deltaG" in df.columns:
        processed["deltaG_exp"] = pd.to_numeric(df["deltaG"], errors="coerce")

    # Number of mutations
    processed["num_mutations"] = df["mut_type"].apply(
        lambda x: 0 if str(x) in ("wt", "nan", "NaN")
        else str(x).count(":") + 1 if ":" in str(x)
        else (1 if re.match(r"^[A-Z]\d+[A-Z]", str(x)) else 0)
    )

    # Wild-type sequence
    if "aa_seq" in df.columns:
        processed["wt_sequence"] = df["aa_seq"].astype(str)

    # Stabilizing flag
    if "Stabilizing_mut" in df.columns:
        processed["is_stabilizing"] = df["Stabilizing_mut"]

    return processed


def _process_generic_format(df: pd.DataFrame, col_map: dict) -> pd.DataFrame:
    """Process generic format using auto-detected column mapping."""
    processed = pd.DataFrame()

    if "protein_name" in col_map:
        processed["pdb_id"] = df[col_map["protein_name"]].astype(str)
    else:
        processed["pdb_id"] = "unknown"

    if "chain" in col_map:
        processed["chain"] = df[col_map["chain"]].astype(str)
    else:
        processed["chain"] = "A"

    if "mutations" in col_map:
        processed["mutations"] = df[col_map["mutations"]].astype(str)
    elif "mut_type" in col_map:
        processed["mutations"] = df.apply(
            lambda row: _reconstruct_mutation_str(row, col_map), axis=1
        )
    else:
        processed["mutations"] = ""

    if "ddG" in col_map:
        processed["ddG"] = pd.to_numeric(df[col_map["ddG"]], errors="coerce")
    else:
        processed["ddG"] = np.nan

    if "n_mut" in col_map:
        processed["num_mutations"] = pd.to_numeric(
            df[col_map["n_mut"]], errors="coerce"
        ).fillna(1).astype(int)
    else:
        processed["num_mutations"] = processed["mutations"].apply(_count_mutations)

    if "sequence" in col_map:
        processed["wt_sequence"] = df[col_map["sequence"]].astype(str)
    elif "aa_seq" in col_map:
        processed["wt_sequence"] = df[col_map["aa_seq"]].astype(str)

    return processed


def preprocess_fireprotdb(
    input_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> pd.DataFrame:
    """Preprocess FireProtDB data into standardized format.

    Args:
        input_path: Path to raw JSON. If None, downloads first.
        output_dir: Output directory for parquet. If None, uses DATA_DIR.

    Returns:
        Processed DataFrame
    """
    out = Path(output_dir) if output_dir else DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    if input_path is None:
        raw_path = download_fireprotdb(str(out))
    else:
        raw_path = Path(input_path)

    print(f"Reading FireProtDB data from {raw_path}...")
    with open(raw_path) as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = data.get("data", data.get("results", [data]))

    print(f"  Raw entries: {len(data)}")

    records = []
    for entry in data:
        record = {}

        # PDB ID
        record["pdb_id"] = str(
            entry.get("pdb_id", entry.get("structure", entry.get("protein_name", "unknown")))
        ).upper()[:4]

        # Chain
        record["chain"] = str(entry.get("chain", entry.get("chain_id", "A")))

        # Mutation string
        mutation_str = _extract_fireprotdb_mutation(entry)
        record["mutations"] = mutation_str

        # ddG
        ddG = entry.get("ddG", entry.get("delta_delta_G", entry.get("ddg", None)))
        if ddG is not None:
            try:
                record["ddG"] = float(ddG)
            except (ValueError, TypeError):
                record["ddG"] = np.nan
        else:
            # Try dTm as fallback (approximate conversion: ddG ~ -0.1 * dTm)
            dTm = entry.get("dTm", entry.get("delta_Tm", None))
            if dTm is not None:
                try:
                    record["ddG"] = -0.1 * float(dTm)
                except (ValueError, TypeError):
                    record["ddG"] = np.nan
            else:
                record["ddG"] = np.nan

        record["num_mutations"] = _count_mutations(mutation_str)
        records.append(record)

    processed = pd.DataFrame(records)

    # Drop rows with missing ddG
    initial_len = len(processed)
    processed = processed.dropna(subset=["ddG"]).reset_index(drop=True)
    print(f"  After dropping NaN ddG: {len(processed)} (removed {initial_len - len(processed)})")

    # Save
    dest = out / "fireprotdb_processed.parquet"
    processed.to_parquet(dest, index=False)
    print(f"  Saved to {dest}")

    _print_summary("FireProtDB", processed)

    return processed


def create_multimutant_subset(
    megascale_path: Optional[str] = None,
    fireprotdb_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    min_mutations: int = 2,
) -> pd.DataFrame:
    """Create a subset of multi-mutant entries from both datasets.

    Args:
        megascale_path: Path to processed Mega-scale parquet
        fireprotdb_path: Path to processed FireProtDB parquet
        output_dir: Output directory
        min_mutations: Minimum number of mutations to include

    Returns:
        Combined multi-mutant DataFrame
    """
    out = Path(output_dir) if output_dir else DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    frames = []

    # Mega-scale multi-mutants
    mega_path = Path(megascale_path) if megascale_path else out / "megascale_processed.parquet"
    if mega_path.exists():
        mega_df = pd.read_parquet(mega_path)
        mega_multi = mega_df[mega_df["num_mutations"] >= min_mutations].copy()
        mega_multi["source"] = "megascale"
        frames.append(mega_multi)
        print(f"Mega-scale multi-mutants (>={min_mutations} mutations): {len(mega_multi)}")
    else:
        print(f"Warning: {mega_path} not found. Run preprocess_megascale first.")

    # FireProtDB multi-mutants
    fire_path = Path(fireprotdb_path) if fireprotdb_path else out / "fireprotdb_processed.parquet"
    if fire_path.exists():
        fire_df = pd.read_parquet(fire_path)
        fire_multi = fire_df[fire_df["num_mutations"] >= min_mutations].copy()
        fire_multi["source"] = "fireprotdb"
        frames.append(fire_multi)
        print(f"FireProtDB multi-mutants (>={min_mutations} mutations): {len(fire_multi)}")
    else:
        print(f"Warning: {fire_path} not found. Run preprocess_fireprotdb first.")

    if not frames:
        print("No data available for multi-mutant subset.")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    # Standardize columns
    standard_cols = ["pdb_id", "chain", "mutations", "ddG", "num_mutations", "source"]
    for col in standard_cols:
        if col not in combined.columns:
            combined[col] = np.nan

    combined = combined[standard_cols].reset_index(drop=True)

    dest = out / "multimutant_subset.parquet"
    combined.to_parquet(dest, index=False)
    print(f"\nCombined multi-mutant subset: {len(combined)} entries")
    print(f"Saved to {dest}")

    # Breakdown
    if len(combined) > 0:
        print(f"\nBreakdown by num_mutations:")
        for n, group in combined.groupby("num_mutations"):
            print(f"  {n} mutations: {len(group)} entries")

    return combined


# --- Helper functions ---


def _detect_megascale_columns(df: pd.DataFrame) -> dict:
    """Auto-detect column mapping for Mega-scale dataset.

    The dataset has varying column names depending on the download source.
    """
    col_map = {}
    columns_lower = {c.lower(): c for c in df.columns}

    # Protein name / ID
    for key in ["wt_name", "protein_name", "name", "pdb_id", "domain", "protein"]:
        if key in columns_lower:
            col_map["protein_name"] = columns_lower[key]
            break

    # Chain
    for key in ["chain", "chain_id"]:
        if key in columns_lower:
            col_map["chain"] = columns_lower[key]
            break

    # Mutations
    for key in ["mutations", "mutation", "mut_name", "variant", "mutant"]:
        if key in columns_lower:
            col_map["mutations"] = columns_lower[key]
            break

    # Mutation type
    for key in ["mut_type", "mutation_type", "type"]:
        if key in columns_lower:
            col_map["mut_type"] = columns_lower[key]
            break

    # Number of mutations
    for key in ["n_mut", "num_mutations", "n_mutations", "nmut"]:
        if key in columns_lower:
            col_map["n_mut"] = columns_lower[key]
            break

    # ddG value
    for key in ["ddg_ml", "ddg", "score_ml", "stability_score", "delta_delta_g"]:
        if key in columns_lower:
            col_map["ddG"] = columns_lower[key]
            break

    # Sequence
    for key in ["aa_seq", "sequence", "wt_seq", "wt_sequence"]:
        if key in columns_lower:
            col_map["sequence"] = columns_lower[key]
            break

    print(f"  Detected column mapping: {col_map}")
    return col_map


def _reconstruct_mutation_str(row: pd.Series, col_map: dict) -> str:
    """Reconstruct mutation string from row data."""
    # If there's a direct mutation column, use it
    if "mutations" in col_map:
        return str(row[col_map["mutations"]])

    # Otherwise try to construct from components
    # This is a fallback for non-standard formats
    return str(row.get("mutation", row.get("variant", "")))


def _extract_fireprotdb_mutation(entry: dict) -> str:
    """Extract mutation string from a FireProtDB entry."""
    # Try direct mutation field
    if "mutation" in entry and isinstance(entry["mutation"], str):
        return entry["mutation"]

    # Construct from components
    wt = entry.get("wild_type", entry.get("wt", "X"))
    pos = entry.get("position", entry.get("pos", 0))
    mut = entry.get("mutation", entry.get("mutant", entry.get("mut", "X")))

    # Handle case where 'mutation' is the full mutation string
    if isinstance(mut, str) and len(mut) > 1:
        return mut

    return f"{wt}{pos}{mut}"


def _count_mutations(mutation_str: str) -> int:
    """Count number of mutations in a mutation string.

    Handles formats like:
    - "A10G" (single)
    - "A10G+L20F" (double, plus-separated)
    - "A10G/L20F" (double, slash-separated)
    - "A10G:L20F" (double, colon-separated)
    """
    if not mutation_str or mutation_str == "nan" or mutation_str == "":
        return 0

    # Count separators
    for sep in ["+", "/", ":", ";"]:
        if sep in mutation_str:
            return mutation_str.count(sep) + 1

    # Single mutation or unknown format
    # Check if it matches single mutation pattern
    if re.match(r"^[A-Z]\d+[A-Z]$", mutation_str):
        return 1

    return 1


def _print_summary(name: str, df: pd.DataFrame) -> None:
    """Print summary statistics for a processed dataset."""
    print(f"\n  === {name} Summary ===")
    print(f"  Total variants: {len(df)}")

    if "pdb_id" in df.columns:
        print(f"  Unique proteins: {df['pdb_id'].nunique()}")

    if "num_mutations" in df.columns:
        print(f"  Mutation count distribution:")
        for n, count in df["num_mutations"].value_counts().sort_index().items():
            print(f"    {n} mutation(s): {count}")

    if "ddG" in df.columns:
        print(f"  ddG range: [{df['ddG'].min():.2f}, {df['ddG'].max():.2f}] kcal/mol")
        print(f"  ddG mean: {df['ddG'].mean():.2f} kcal/mol")
        stabilizing = (df["ddG"] < -1.0).sum()
        print(f"  Stabilizing (ddG < -1.0): {stabilizing} ({100*stabilizing/len(df):.1f}%)")


def preprocess_all(output_dir: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run full preprocessing pipeline.

    Returns:
        Tuple of (megascale_df, fireprotdb_df, multimutant_df)
    """
    print("=" * 60)
    print("StabOpt Data Preprocessing Pipeline")
    print("=" * 60)

    mega_df = preprocess_megascale(output_dir=output_dir)
    print()
    fire_df = preprocess_fireprotdb(output_dir=output_dir)
    print()
    multi_df = create_multimutant_subset(output_dir=output_dir)

    print("\n" + "=" * 60)
    print("Preprocessing complete!")
    print("=" * 60)

    return mega_df, fire_df, multi_df


if __name__ == "__main__":
    preprocess_all()
