"""PDB file parsing utilities."""

from __future__ import annotations

from typing import Dict, Any, List, Tuple
import warnings


# Standard amino acid 3-letter to 1-letter mapping
AA3TO1 = {
    "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F",
    "GLY": "G", "HIS": "H", "ILE": "I", "LYS": "K", "LEU": "L",
    "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R",
    "SER": "S", "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y",
}

AA1TO3 = {v: k for k, v in AA3TO1.items()}

AMINO_ACIDS = sorted(AA3TO1.values())  # 20 standard amino acids


def parse_pdb(pdb_path: str, chain_id: str = "A") -> Dict[str, Any]:
    """Parse a PDB file and extract sequence, coordinates, and metadata.

    Returns a dict with:
        - sequence: str (1-letter amino acid sequence)
        - residues: list of dicts with position, resname, ca_coords, cb_coords
        - ca_coords: numpy array of CA coordinates (N x 3)
        - chain_id: str
    """
    import numpy as np

    residues: List[Dict[str, Any]] = []
    ca_coords: List[List[float]] = []
    cb_coords: List[List[float]] = []
    sequence_chars: List[str] = []
    seen_positions: set = set()

    with open(pdb_path, "r") as f:
        for line in f:
            if not line.startswith(("ATOM", "HETATM")):
                continue
            atom_chain = line[21].strip()
            if atom_chain != chain_id:
                continue

            resname = line[17:20].strip()
            if resname not in AA3TO1:
                continue

            resseq = int(line[22:26].strip())
            icode = line[26].strip()
            pos_key = (resseq, icode)

            atom_name = line[12:16].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])

            if pos_key not in seen_positions:
                seen_positions.add(pos_key)
                aa1 = AA3TO1[resname]
                residues.append({
                    "position": resseq,
                    "resname": resname,
                    "aa": aa1,
                    "ca_coords": None,
                    "cb_coords": None,
                })
                sequence_chars.append(aa1)
                ca_coords.append([0.0, 0.0, 0.0])
                cb_coords.append([0.0, 0.0, 0.0])

            idx = len(residues) - 1
            if residues[idx]["position"] == resseq:
                if atom_name == "CA":
                    residues[idx]["ca_coords"] = [x, y, z]
                    ca_coords[idx] = [x, y, z]
                elif atom_name == "CB":
                    residues[idx]["cb_coords"] = [x, y, z]
                    cb_coords[idx] = [x, y, z]

    # For glycine, use CA as CB
    for i, res in enumerate(residues):
        if res["cb_coords"] is None:
            res["cb_coords"] = res["ca_coords"]
            if res["ca_coords"] is not None:
                cb_coords[i] = res["ca_coords"]

    sequence = "".join(sequence_chars)
    ca_array = np.array(ca_coords, dtype=np.float32)
    cb_array = np.array(cb_coords, dtype=np.float32)

    return {
        "sequence": sequence,
        "residues": residues,
        "ca_coords": ca_array,
        "cb_coords": cb_array,
        "chain_id": chain_id,
        "n_residues": len(residues),
    }


def compute_distance_matrix(coords: "np.ndarray") -> "np.ndarray":
    """Compute pairwise Euclidean distance matrix from coordinates."""
    import numpy as np
    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt(np.sum(diff ** 2, axis=-1))


def get_contact_pairs(
    coords: "np.ndarray", threshold: float = 10.0
) -> List[Tuple[int, int]]:
    """Get pairs of residue indices within distance threshold (Angstroms)."""
    dist_matrix = compute_distance_matrix(coords)
    pairs = []
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            if dist_matrix[i, j] < threshold:
                pairs.append((i, j))
    return pairs
