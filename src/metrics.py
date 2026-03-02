"""Search metrics framework for tracking and reporting."""

import json
import time
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SearchMetrics:
    """Tracks all metrics for a search run."""
    total_candidates: int = 0
    passed_modular_filter: int = 0
    passed_face_diagonal: int = 0
    euler_bricks_found: int = 0
    perfect_cuboids_found: int = 0
    near_misses_found: int = 0
    wall_clock_seconds: float = 0.0
    candidates_per_second: float = 0.0
    method: str = ""
    search_bound: int = 0
    filter_stages: dict = field(default_factory=dict)

    _start_time: float = field(default=0.0, repr=False)

    def start_timer(self):
        self._start_time = time.time()

    def stop_timer(self):
        self.wall_clock_seconds = time.time() - self._start_time
        if self.wall_clock_seconds > 0:
            self.candidates_per_second = self.total_candidates / self.wall_clock_seconds

    def to_dict(self):
        d = asdict(self)
        d.pop('_start_time', None)
        return d

    def save(self, path: str = "results/metrics.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def report(self) -> str:
        lines = [
            f"Search Method: {self.method}",
            f"Search Bound: {self.search_bound:,}",
            f"Total Candidates Tested: {self.total_candidates:,}",
            f"Passed Modular Filter: {self.passed_modular_filter:,}",
            f"Passed Face Diagonal Check: {self.passed_face_diagonal:,}",
            f"Euler Bricks Found: {self.euler_bricks_found:,}",
            f"Perfect Cuboids Found: {self.perfect_cuboids_found:,}",
            f"Near-Misses Found: {self.near_misses_found:,}",
            f"Wall Clock Time: {self.wall_clock_seconds:.2f}s",
            f"Throughput: {self.candidates_per_second:,.0f} candidates/sec",
        ]
        if self.filter_stages:
            lines.append("Filter Stage Counts:")
            for stage, count in self.filter_stages.items():
                lines.append(f"  {stage}: {count:,}")
        return "\n".join(lines)
