"""Run configuration system for reproducibility."""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SearchConfig:
    """Configuration for a search run."""
    search_bound: int = 10000
    random_seed: int = 42
    top_k_near_misses: int = 100
    method: str = "baseline"
    use_modular_filter: bool = True
    output_dir: str = "results"

    def save(self, path: Optional[str] = None):
        if path is None:
            path = os.path.join(self.output_dir, "search_config.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: str) -> 'SearchConfig':
        with open(path) as f:
            return cls(**json.load(f))
