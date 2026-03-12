import json
import subprocess
import tempfile
import unittest
from pathlib import Path


def reversed_axis_choice_terms(steps: int) -> tuple[list[int], list[int]]:
    row_terms = [1]
    column_terms = [1]
    covered = {1}
    while len(row_terms) < steps:
        next_column = 1
        while next_column in covered:
            next_column += 1
        column_terms.append(next_column)
        next_row = 1
        while next_row in covered or next_row == next_column:
            next_row += 1
        row_terms.append(next_row)
        for row_term in row_terms:
            covered.add(next_column * row_term)
        for column_term in column_terms[:-1]:
            covered.add(next_row * column_term)
    return row_terms, column_terms


class PrimeSeparatorTest(unittest.TestCase):
    def _run_generator(self, command: list[str]) -> tuple[list[int], list[int]]:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            subprocess.run(command + ["--out-dir", str(out_dir)], check=True)
            row_terms = json.loads((out_dir / "row_terms.json").read_text())
            column_terms = json.loads((out_dir / "column_terms.json").read_text())
        return row_terms, column_terms

    def test_baseline_prefix(self) -> None:
        out_dir = Path("results/baseline/test_11")
        if out_dir.exists():
            for child in out_dir.iterdir():
                child.unlink()
        else:
            out_dir.mkdir(parents=True)

        subprocess.run(
            [
                "python3",
                "scripts/prime_separator.py",
                "--steps",
                "11",
                "--out-dir",
                str(out_dir),
            ],
            check=True,
        )
        contract = json.loads((out_dir / "contract.json").read_text())
        self.assertTrue(contract["validation"]["row_prefix_matches"])
        self.assertTrue(contract["validation"]["column_prefix_matches"])
        self.assertTrue(contract["validation"]["table_prefix_matches"])

    def test_structural_digest_is_repeatable(self) -> None:
        out_a = Path("results/baseline/test_repeat_a")
        out_b = Path("results/baseline/test_repeat_b")
        for out_dir in (out_a, out_b):
            if out_dir.exists():
                for child in out_dir.iterdir():
                    child.unlink()
            else:
                out_dir.mkdir(parents=True)
            subprocess.run(
                [
                    "python3",
                    "scripts/prime_separator.py",
                    "--steps",
                    "30000",
                    "--out-dir",
                    str(out_dir),
                ],
                check=True,
            )
        contract_a = json.loads((out_a / "contract.json").read_text())
        contract_b = json.loads((out_b / "contract.json").read_text())
        self.assertEqual(
            contract_a["structural_digest_sha256"],
            contract_b["structural_digest_sha256"],
        )
        self.assertEqual(contract_a["gap_locations"], contract_b["gap_locations"])

    def test_wrong_update_order_is_detectable(self) -> None:
        wrong_rows, wrong_cols = reversed_axis_choice_terms(11)
        self.assertNotEqual(wrong_rows[:11], [1, 2, 4, 7, 9, 13, 15, 18, 23, 25, 29])
        self.assertNotEqual(wrong_cols[:5], [1, 3, 5, 8, 11])

    def test_row_immediate_matches_baseline(self) -> None:
        baseline_rows, baseline_cols = self._run_generator(
            ["python3", "scripts/prime_separator.py", "--steps", "200"]
        )
        variant_rows, variant_cols = self._run_generator(
            [
                "python3",
                "scripts/prime_separator_variants.py",
                "--variant",
                "row_immediate",
                "--steps",
                "200",
            ]
        )
        self.assertEqual(variant_rows, baseline_rows)
        self.assertEqual(variant_cols, baseline_cols)

    def test_column_immediate_swaps_axes(self) -> None:
        baseline_rows, baseline_cols = self._run_generator(
            ["python3", "scripts/prime_separator.py", "--steps", "200"]
        )
        variant_rows, variant_cols = self._run_generator(
            [
                "python3",
                "scripts/prime_separator_variants.py",
                "--variant",
                "column_immediate",
                "--steps",
                "200",
            ]
        )
        self.assertEqual(variant_rows, baseline_cols)
        self.assertEqual(variant_cols, baseline_rows)


if __name__ == "__main__":
    unittest.main()
