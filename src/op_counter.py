"""Operation-counting framework for the comparison-addition model.

Tracks comparisons, additions, and heap operations (insert, extract-min,
decrease-key) to measure algorithmic complexity in the comparison-addition
model used by Fredman-Tarjan 1987, Duan et al. 2025, etc.
"""

import csv
import io
from dataclasses import dataclass, field


@dataclass
class OpCounter:
    """Counts operations in the comparison-addition model."""

    comparisons: int = 0
    additions: int = 0
    heap_inserts: int = 0
    extract_mins: int = 0
    decrease_keys: int = 0

    @property
    def heap_ops(self):
        return self.heap_inserts + self.extract_mins + self.decrease_keys

    @property
    def total_ops(self):
        return self.comparisons + self.additions + self.heap_ops

    def compare(self, a, b):
        """Perform a comparison, return -1, 0, or 1."""
        self.comparisons += 1
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0

    def less_than(self, a, b):
        """Perform a < comparison, return bool."""
        self.comparisons += 1
        return a < b

    def add(self, a, b):
        """Perform an addition, return result."""
        self.additions += 1
        return a + b

    def record_insert(self):
        self.heap_inserts += 1

    def record_extract_min(self):
        self.extract_mins += 1

    def record_decrease_key(self):
        self.decrease_keys += 1

    def reset(self):
        self.comparisons = 0
        self.additions = 0
        self.heap_inserts = 0
        self.extract_mins = 0
        self.decrease_keys = 0

    def to_dict(self):
        return {
            "comparisons": self.comparisons,
            "additions": self.additions,
            "heap_inserts": self.heap_inserts,
            "extract_mins": self.extract_mins,
            "decrease_keys": self.decrease_keys,
            "heap_ops": self.heap_ops,
            "total_ops": self.total_ops,
        }

    def __repr__(self):
        return (
            f"OpCounter(cmp={self.comparisons}, add={self.additions}, "
            f"ins={self.heap_inserts}, ext={self.extract_mins}, "
            f"dec={self.decrease_keys}, total={self.total_ops})"
        )


CSV_COLUMNS = [
    "algorithm", "graph_type", "n", "m", "trial",
    "total_ops", "comparisons", "additions",
    "heap_ops", "heap_inserts", "extract_mins", "decrease_keys",
    "wall_time_ms", "nodes_expanded",
]


def write_csv_header(filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)


def append_csv_row(filepath, row_dict):
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writerow(row_dict)


def format_csv_row(row_dict):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS)
    writer.writerow(row_dict)
    return buf.getvalue().strip()
