import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class NoveltyDeepeningTest(unittest.TestCase):
    def test_independent_checker_matches_baseline_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "checker.json"
            subprocess.run(
                [
                    "python3",
                    "scripts/novelty_deepening.py",
                    "checker",
                    "--steps",
                    "200",
                    "--out",
                    str(out_path),
                ],
                check=True,
            )
            payload = json.loads(out_path.read_text())
        self.assertTrue(payload["row_terms_match"])
        self.assertTrue(payload["column_terms_match"])

    def test_shared_corpus_contains_record_and_control_windows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir) / "corpus"
            subprocess.run(
                [
                    "python3",
                    "scripts/novelty_deepening.py",
                    "build-corpus",
                    "--base-dir",
                    "results/experiments/run_1000000",
                    "--out-dir",
                    str(out_dir),
                    "--min-record-gap",
                    "20",
                    "--modulus-limit",
                    "8",
                ],
                check=True,
            )
            payload = json.loads((out_dir / "shared_corpus.json").read_text())

        self.assertEqual(payload["record_window_count"], 5)
        self.assertGreater(payload["control_window_count"], 0)
        self.assertGreater(payload["surrogate_window_count"], 0)


if __name__ == "__main__":
    unittest.main()
