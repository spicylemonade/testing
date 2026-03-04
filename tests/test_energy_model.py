"""Tests for the energy model and optimization modules."""

import pytest
import numpy as np
import pandas as pd
from stabopt.scoring.energy_model import EnergyModel
from stabopt.optimization.brute_force import brute_force_search, estimate_brute_force_time
from stabopt.optimization.greedy import greedy_search
from stabopt.optimization.beam_search import beam_search
from stabopt.optimization.evolutionary import evolutionary_search


@pytest.fixture
def mock_candidates():
    """Create mock single-mutation candidates for testing."""
    rng = np.random.RandomState(42)
    n = 20
    rows = []
    for i in range(n):
        rows.append({
            "position": i,
            "wildtype": "A",
            "mutant": "G" if i % 2 == 0 else "L",
            "score": rng.uniform(-1.0, 2.0),
        })
    return pd.DataFrame(rows)


@pytest.fixture
def mock_epistasis(mock_candidates):
    """Create mock epistasis matrix."""
    K = len(mock_candidates)
    rng = np.random.RandomState(42)
    eps = rng.uniform(-0.2, 0.2, (K, K)).astype(np.float32)
    eps = (eps + eps.T) / 2  # Symmetrize
    np.fill_diagonal(eps, 0.0)
    return eps


@pytest.fixture
def energy_additive(mock_candidates):
    return EnergyModel(mock_candidates, mode="additive_only")


@pytest.fixture
def energy_pairwise(mock_candidates, mock_epistasis):
    return EnergyModel(mock_candidates, mock_epistasis, mode="additive_pairwise")


class TestEnergyModel:
    def test_additive_score(self, energy_additive, mock_candidates):
        indices = [0, 1, 2]
        expected = sum(mock_candidates.iloc[i]["score"] for i in indices)
        assert abs(energy_additive.score(indices) - expected) < 1e-6

    def test_pairwise_score(self, energy_pairwise, mock_candidates, mock_epistasis):
        indices = [0, 1]
        additive = sum(mock_candidates.iloc[i]["score"] for i in indices)
        pairwise = mock_epistasis[0, 1]
        expected = additive + pairwise
        assert abs(energy_pairwise.score(indices) - expected) < 1e-6

    def test_marginal_gain_additive(self, energy_additive, mock_candidates):
        gain = energy_additive.marginal_gain([], 0)
        assert abs(gain - mock_candidates.iloc[0]["score"]) < 1e-6

    def test_marginal_gain_with_epistasis(self, energy_pairwise, mock_candidates, mock_epistasis):
        gain = energy_pairwise.marginal_gain([0], 1)
        expected = mock_candidates.iloc[1]["score"] + mock_epistasis[0, 1]
        assert abs(gain - expected) < 1e-6

    def test_n_candidates(self, energy_additive, mock_candidates):
        assert energy_additive.n_candidates == len(mock_candidates)

    def test_format_mutations(self, energy_additive):
        result = energy_additive.format_mutations([0, 2])
        assert "A0G" in result
        assert "A2G" in result

    def test_empty_score(self, energy_additive):
        assert energy_additive.score([]) == 0.0


class TestBruteForce:
    def test_small_enumeration(self, energy_additive, mock_candidates):
        results = brute_force_search(energy_additive, mock_candidates, k=3)
        assert len(results) > 0
        # Should be sorted by score descending
        for i in range(len(results) - 1):
            assert results[i]["predicted_ddG"] >= results[i + 1]["predicted_ddG"]

    def test_k2_enumeration(self, energy_additive, mock_candidates):
        results = brute_force_search(energy_additive, mock_candidates, k=2)
        assert len(results) > 0

    def test_estimate_time(self):
        est = estimate_brute_force_time(20, 4)
        assert est["n_combinations"] == 4845
        assert est["feasible_15min"] is True

        est2 = estimate_brute_force_time(50, 8)
        assert est2["n_combinations"] > 500_000_000
        assert est2["feasible_15min"] is False


class TestGreedy:
    def test_greedy_returns_result(self, energy_additive, mock_candidates):
        results = greedy_search(energy_additive, mock_candidates, k=4)
        assert len(results) == 1
        assert "mutations" in results[0]
        assert "predicted_ddG" in results[0]

    def test_greedy_step_log(self, energy_additive, mock_candidates):
        results = greedy_search(energy_additive, mock_candidates, k=3)
        assert "step_log" in results[0]
        assert len(results[0]["step_log"]) == 3


class TestBeamSearch:
    def test_beam_returns_results(self, energy_additive, mock_candidates):
        results = beam_search(
            energy_additive, mock_candidates, k=3, beam_width=10
        )
        assert len(results) > 0
        assert results[0]["predicted_ddG"] >= results[-1]["predicted_ddG"]

    def test_beam_width_affects_results(self, energy_additive, mock_candidates):
        results_narrow = beam_search(
            energy_additive, mock_candidates, k=3, beam_width=5
        )
        results_wide = beam_search(
            energy_additive, mock_candidates, k=3, beam_width=50
        )
        # Wider beam should find equal or better solution
        assert results_wide[0]["predicted_ddG"] >= results_narrow[0]["predicted_ddG"] - 0.01

    def test_beam_vs_brute_force_quality(self, energy_additive, mock_candidates):
        """Beam search should find a solution close to brute-force optimal for small k."""
        bf_results = brute_force_search(energy_additive, mock_candidates, k=3)
        beam_results = beam_search(
            energy_additive, mock_candidates, k=3, beam_width=50
        )
        bf_best = bf_results[0]["predicted_ddG"]
        beam_best = beam_results[0]["predicted_ddG"]
        # Beam should be within 5% of brute-force
        assert beam_best >= bf_best * 0.95 or abs(beam_best - bf_best) < 0.1


class TestEvolutionary:
    def test_evolutionary_returns_results(self, energy_additive, mock_candidates):
        results = evolutionary_search(
            energy_additive, mock_candidates, k=4,
            population_size=50, generations=20, seed=42
        )
        assert len(results) > 0
        assert results[0]["predicted_ddG"] >= results[-1]["predicted_ddG"]

    def test_evolutionary_deterministic(self, energy_additive, mock_candidates):
        r1 = evolutionary_search(
            energy_additive, mock_candidates, k=3,
            population_size=30, generations=10, seed=42
        )
        r2 = evolutionary_search(
            energy_additive, mock_candidates, k=3,
            population_size=30, generations=10, seed=42
        )
        assert r1[0]["predicted_ddG"] == r2[0]["predicted_ddG"]


class TestCLI:
    def test_help_output(self):
        from stabopt.cli import parse_args
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["--help"])
        assert exc_info.value.code == 0

    def test_parse_basic_args(self):
        from stabopt.cli import parse_args
        args = parse_args(["--pdb", "test.pdb", "--k", "4", "--output", "out.csv"])
        assert args.pdb == "test.pdb"
        assert args.k == 4
        assert args.output == "out.csv"

    def test_parse_defaults(self):
        from stabopt.cli import parse_args
        args = parse_args(["--pdb", "test.pdb"])
        assert args.k == 4
        assert args.beam_width == 100
        assert args.scorer == "esm2"
        assert args.optimizer == "beam"
        assert args.epistasis is True
        assert args.rerank is True
        assert args.seed == 42
