"""Tests for PDB parsing utilities."""

import os
import pytest
import numpy as np
from stabopt.utils.pdb_utils import (
    parse_pdb,
    compute_distance_matrix,
    get_contact_pairs,
    AA3TO1,
    AMINO_ACIDS,
)

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
PDB_1BNI = os.path.join(FIXTURES, "1BNI.pdb")


class TestAminoAcidMappings:
    def test_aa3to1_has_20_entries(self):
        assert len(AA3TO1) == 20

    def test_amino_acids_sorted(self):
        assert AMINO_ACIDS == sorted(AMINO_ACIDS)
        assert len(AMINO_ACIDS) == 20

    def test_all_single_letter(self):
        for aa in AMINO_ACIDS:
            assert len(aa) == 1
            assert aa.isupper()


class TestParsePDB:
    @pytest.fixture
    def structure(self):
        return parse_pdb(PDB_1BNI, "A")

    def test_parse_returns_dict(self, structure):
        assert isinstance(structure, dict)
        assert "sequence" in structure
        assert "residues" in structure
        assert "ca_coords" in structure
        assert "chain_id" in structure

    def test_sequence_not_empty(self, structure):
        assert len(structure["sequence"]) > 0
        assert all(aa in AMINO_ACIDS for aa in structure["sequence"])

    def test_sequence_length_matches_residues(self, structure):
        assert len(structure["sequence"]) == len(structure["residues"])

    def test_ca_coords_shape(self, structure):
        n = len(structure["sequence"])
        assert structure["ca_coords"].shape == (n, 3)

    def test_chain_id(self, structure):
        assert structure["chain_id"] == "A"

    def test_residue_has_position(self, structure):
        for res in structure["residues"]:
            assert "position" in res
            assert "aa" in res
            assert res["aa"] in AMINO_ACIDS

    def test_barnase_reasonable_size(self, structure):
        # Barnase is ~110 residues
        n = len(structure["sequence"])
        assert 90 < n < 130, f"Unexpected size: {n}"


class TestDistanceMatrix:
    def test_identity(self):
        coords = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
        dm = compute_distance_matrix(coords)
        assert dm.shape == (3, 3)
        np.testing.assert_allclose(dm[0, 0], 0.0)
        np.testing.assert_allclose(dm[0, 1], 1.0)
        np.testing.assert_allclose(dm[1, 0], 1.0)

    def test_symmetry(self):
        rng = np.random.RandomState(42)
        coords = rng.randn(10, 3).astype(np.float32)
        dm = compute_distance_matrix(coords)
        np.testing.assert_allclose(dm, dm.T)


class TestContactPairs:
    def test_all_close(self):
        coords = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]], dtype=np.float32)
        pairs = get_contact_pairs(coords, threshold=5.0)
        assert len(pairs) == 3  # All pairs within 5A

    def test_none_close(self):
        coords = np.array([[0, 0, 0], [100, 0, 0]], dtype=np.float32)
        pairs = get_contact_pairs(coords, threshold=5.0)
        assert len(pairs) == 0
