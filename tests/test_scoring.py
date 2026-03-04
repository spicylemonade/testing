"""Tests for single-mutation scoring modules (ESM-2 and ProteinMPNN)."""

import os
import time
import pytest
import numpy as np
import pandas as pd

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
PDB_1BNI = os.path.join(FIXTURES, "1BNI.pdb")

# Skip GPU tests if CUDA not available
try:
    import torch
    HAS_CUDA = torch.cuda.is_available()
except ImportError:
    HAS_CUDA = False


class TestESM2Scoring:
    """Tests for ESM-2 masked marginal scoring."""

    @pytest.fixture(scope="class")
    def barnase_structure(self):
        from stabopt.utils.pdb_utils import parse_pdb
        return parse_pdb(PDB_1BNI, "A")

    @pytest.mark.skipif(not HAS_CUDA, reason="CUDA not available")
    def test_esm2_produces_dataframe(self, barnase_structure):
        from stabopt.scoring.esm2 import score_single_mutations
        df = score_single_mutations(
            barnase_structure["sequence"],
            device="cuda",
            batch_size=16,
        )
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) >= {"position", "wildtype", "mutant", "score"}

    @pytest.mark.skipif(not HAS_CUDA, reason="CUDA not available")
    def test_esm2_correct_count(self, barnase_structure):
        from stabopt.scoring.esm2 import score_single_mutations
        seq = barnase_structure["sequence"]
        df = score_single_mutations(seq, device="cuda", batch_size=16)
        # Each position has 19 possible mutations (exclude wildtype)
        expected = len(seq) * 19
        assert len(df) == expected, f"Expected {expected}, got {len(df)}"

    @pytest.mark.skipif(not HAS_CUDA, reason="CUDA not available")
    def test_esm2_no_self_mutations(self, barnase_structure):
        from stabopt.scoring.esm2 import score_single_mutations
        df = score_single_mutations(
            barnase_structure["sequence"], device="cuda", batch_size=16
        )
        # No row should have wildtype == mutant
        self_muts = df[df["wildtype"] == df["mutant"]]
        assert len(self_muts) == 0

    @pytest.mark.skipif(not HAS_CUDA, reason="CUDA not available")
    def test_esm2_timing(self, barnase_structure):
        """ESM-2 should score 108-residue protein in under 60s."""
        from stabopt.scoring.esm2 import score_single_mutations
        start = time.time()
        df = score_single_mutations(
            barnase_structure["sequence"], device="cuda", batch_size=16
        )
        elapsed = time.time() - start
        assert elapsed < 60, f"Took {elapsed:.1f}s (expected < 60s)"

    @pytest.mark.skipif(not HAS_CUDA, reason="CUDA not available")
    def test_esm2_score_range(self, barnase_structure):
        from stabopt.scoring.esm2 import score_single_mutations
        df = score_single_mutations(
            barnase_structure["sequence"], device="cuda", batch_size=16
        )
        # Scores should be finite
        assert df["score"].notna().all()
        assert np.isfinite(df["score"].values).all()
        # Should have both positive and negative scores
        assert df["score"].min() < 0
        assert df["score"].max() > 0


class TestProteinMPNNScoring:
    """Tests for ProteinMPNN / inverse-folding scoring."""

    def test_proteinmpnn_produces_dataframe(self):
        from stabopt.scoring.proteinmpnn import score_single_mutations
        df = score_single_mutations(PDB_1BNI, "A", device="cpu")
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) >= {"position", "wildtype", "mutant", "score"}

    def test_proteinmpnn_correct_count(self):
        from stabopt.scoring.proteinmpnn import score_single_mutations
        from stabopt.utils.pdb_utils import parse_pdb
        struct = parse_pdb(PDB_1BNI, "A")
        n = len(struct["sequence"])
        df = score_single_mutations(PDB_1BNI, "A", device="cpu")
        expected = n * 19
        assert len(df) == expected

    def test_proteinmpnn_no_self_mutations(self):
        from stabopt.scoring.proteinmpnn import score_single_mutations
        df = score_single_mutations(PDB_1BNI, "A", device="cpu")
        self_muts = df[df["wildtype"] == df["mutant"]]
        assert len(self_muts) == 0

    def test_proteinmpnn_score_sequence(self):
        from stabopt.scoring.proteinmpnn import score_sequence
        from stabopt.utils.pdb_utils import parse_pdb
        struct = parse_pdb(PDB_1BNI, "A")
        wt_score = score_sequence(struct["sequence"], PDB_1BNI, "A", device="cpu")
        assert isinstance(wt_score, float)


class TestScoringConsistency:
    """Cross-scorer consistency checks."""

    def test_both_scorers_same_positions(self):
        from stabopt.scoring.proteinmpnn import score_single_mutations as mpnn_score
        from stabopt.utils.pdb_utils import parse_pdb
        struct = parse_pdb(PDB_1BNI, "A")
        mpnn_df = mpnn_score(PDB_1BNI, "A", device="cpu")
        positions = sorted(mpnn_df["position"].unique())
        expected_positions = list(range(len(struct["sequence"])))
        assert positions == expected_positions
