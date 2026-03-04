"""Command-line interface for StabOpt."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="stabopt",
        description="Fast combinatorial protein stability optimization. "
        "Takes a PDB file and outputs ranked stabilizing mutation sets.",
    )
    parser.add_argument(
        "--pdb",
        type=str,
        required=True,
        help="Path to input PDB file",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=4,
        help="Number of simultaneous mutations (3-8, default: 4)",
    )
    parser.add_argument(
        "--chain",
        type=str,
        default="A",
        help="Chain ID to analyze (default: A)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="stabopt_results.csv",
        help="Output CSV file path",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=50,
        help="Number of candidate single mutations to consider (default: 50)",
    )
    parser.add_argument(
        "--beam-width",
        type=int,
        default=100,
        help="Beam width for beam search optimizer (default: 100)",
    )
    parser.add_argument(
        "--scorer",
        type=str,
        choices=["esm2", "proteinmpnn", "combined"],
        default="esm2",
        help="Primary scoring model (default: esm2)",
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        choices=["beam", "greedy", "evolutionary", "brute_force"],
        default="beam",
        help="Optimization algorithm (default: beam)",
    )
    parser.add_argument(
        "--epistasis",
        action="store_true",
        default=True,
        help="Include pairwise epistasis scoring (default: True)",
    )
    parser.add_argument(
        "--no-epistasis",
        action="store_false",
        dest="epistasis",
        help="Disable pairwise epistasis scoring",
    )
    parser.add_argument(
        "--rerank",
        action="store_true",
        default=True,
        help="Apply ProteinMPNN consensus re-ranking (default: True)",
    )
    parser.add_argument(
        "--no-rerank",
        action="store_false",
        dest="rerank",
        help="Disable ProteinMPNN re-ranking",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="PyTorch device (default: cuda)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args(argv)


def run_pipeline(args: argparse.Namespace) -> List[Dict[str, Any]]:
    """Run the full StabOpt pipeline."""
    import torch
    import numpy as np

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    pdb_path = Path(args.pdb)
    if not pdb_path.exists():
        print(f"Error: PDB file not found: {pdb_path}", file=sys.stderr)
        sys.exit(1)

    start_time = time.time()

    # Step 1: Parse PDB and extract sequence
    if args.verbose:
        print(f"[1/5] Parsing PDB: {pdb_path}")
    from stabopt.utils.pdb_utils import parse_pdb
    structure = parse_pdb(str(pdb_path), args.chain)
    sequence = structure["sequence"]
    n_residues = len(sequence)
    if args.verbose:
        print(f"  Chain {args.chain}: {n_residues} residues")

    # Step 2: Single-mutation scoring
    if args.verbose:
        print(f"[2/5] Scoring single mutations with {args.scorer}...")
    if args.scorer == "esm2":
        from stabopt.scoring.esm2 import score_single_mutations
        single_scores = score_single_mutations(sequence, device=args.device)
    elif args.scorer == "proteinmpnn":
        from stabopt.scoring.proteinmpnn import score_single_mutations
        single_scores = score_single_mutations(
            str(pdb_path), args.chain, device=args.device
        )
    else:  # combined
        from stabopt.scoring.esm2 import score_single_mutations as esm2_score
        from stabopt.scoring.proteinmpnn import score_single_mutations as mpnn_score
        esm2_df = esm2_score(sequence, device=args.device)
        mpnn_df = mpnn_score(str(pdb_path), args.chain, device=args.device)
        single_scores = esm2_df.copy()
        single_scores["score"] = 0.5 * esm2_df["score"] + 0.5 * mpnn_df["score"]

    # Get top-N candidates
    top_candidates = single_scores.nlargest(args.top_n, "score")
    if args.verbose:
        print(f"  Top {args.top_n} candidates selected")

    # Step 3: Epistasis scoring (if enabled)
    epistasis_matrix = None
    if args.epistasis and args.k >= 2:
        if args.verbose:
            print("[3/5] Computing pairwise epistasis...")
        from stabopt.scoring.epistasis import compute_epistasis_matrix
        epistasis_matrix = compute_epistasis_matrix(
            sequence, top_candidates, structure, device=args.device
        )
    elif args.verbose:
        print("[3/5] Skipping epistasis scoring")

    # Step 4: Combinatorial optimization
    if args.verbose:
        print(f"[4/5] Running {args.optimizer} optimizer (k={args.k})...")
    from stabopt.scoring.energy_model import EnergyModel
    energy_model = EnergyModel(
        single_scores=top_candidates,
        epistasis_matrix=epistasis_matrix,
    )

    if args.optimizer == "beam":
        from stabopt.optimization.beam_search import beam_search
        results = beam_search(
            energy_model=energy_model,
            candidates=top_candidates,
            k=args.k,
            beam_width=args.beam_width,
        )
    elif args.optimizer == "greedy":
        from stabopt.optimization.greedy import greedy_search
        results = greedy_search(
            energy_model=energy_model,
            candidates=top_candidates,
            k=args.k,
        )
    elif args.optimizer == "evolutionary":
        from stabopt.optimization.evolutionary import evolutionary_search
        results = evolutionary_search(
            energy_model=energy_model,
            candidates=top_candidates,
            k=args.k,
        )
    elif args.optimizer == "brute_force":
        from stabopt.optimization.brute_force import brute_force_search
        results = brute_force_search(
            energy_model=energy_model,
            candidates=top_candidates,
            k=args.k,
        )

    # Step 5: Re-ranking (if enabled)
    if args.rerank and len(results) > 0:
        if args.verbose:
            print("[5/5] Re-ranking with ProteinMPNN consensus...")
        from stabopt.scoring.consensus import rerank_candidates
        results = rerank_candidates(
            results=results,
            pdb_path=str(pdb_path),
            chain=args.chain,
            sequence=sequence,
            device=args.device,
        )
    elif args.verbose:
        print("[5/5] Skipping re-ranking")

    elapsed = time.time() - start_time
    if args.verbose:
        print(f"\nPipeline completed in {elapsed:.1f} seconds")
        if results:
            print(f"Best predicted ddG: {results[0]['predicted_ddG']:.3f} kcal/mol")

    return results


def write_output(results: List[Dict[str, Any]], output_path: str) -> None:
    """Write results to CSV."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    if not results:
        print("Warning: No results to write", file=sys.stderr)
        return

    fieldnames = ["rank", "mutations", "predicted_ddG", "confidence"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, result in enumerate(results, 1):
            writer.writerow({
                "rank": i,
                "mutations": result.get("mutations", ""),
                "predicted_ddG": f"{result.get('predicted_ddG', 0.0):.4f}",
                "confidence": f"{result.get('confidence', 0.0):.4f}",
            })
    print(f"Results written to {output_path}")


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        results = run_pipeline(args)
        write_output(results, args.output)
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
