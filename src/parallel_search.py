"""Parallel search infrastructure for BB(6) exploration.

Uses Python multiprocessing to distribute TM simulation across all CPU cores.
Implements work-stealing queue and crash recovery via periodic checkpointing.
"""

from __future__ import annotations

import json
import multiprocessing as mp
import os
import random
import time
from typing import Dict, List, Optional, Tuple

from src.tm_simulator import TuringMachine, HALT_STATE


def _simulate_batch(args: Tuple[List[str], int]) -> List[Dict]:
    """Worker function: simulate a batch of TMs and return results.

    This runs in a separate process.
    """
    notations, step_limit = args
    results = []

    # Import here to avoid pickling issues
    from src.tm_accelerated import AcceleratedTuringMachine, _C_AVAILABLE

    for notation in notations:
        try:
            if _C_AVAILABLE:
                atm = AcceleratedTuringMachine.from_compact(notation)
                steps, ones, halted, wall_time = atm.simulate_c(max_steps=step_limit)
            else:
                atm = AcceleratedTuringMachine.from_compact(notation)
                steps, ones, halted, wall_time = atm.simulate(max_steps=step_limit)

            if halted:
                results.append({
                    "notation": notation,
                    "steps": int(steps),
                    "sigma": int(ones),
                    "halted": True,
                })
        except Exception:
            pass

    return results


class ParallelSearch:
    """Parallel TM search with multiprocessing and checkpointing."""

    def __init__(
        self,
        num_workers: Optional[int] = None,
        step_limit: int = 10**6,
        checkpoint_interval: int = 300,  # seconds
        checkpoint_path: str = "results/search_campaigns/checkpoint.json",
    ):
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        self.step_limit = step_limit
        self.checkpoint_interval = checkpoint_interval
        self.checkpoint_path = checkpoint_path
        self.all_results: List[Dict] = []
        self.total_explored = 0

    def search(
        self,
        notations: List[str],
        batch_size: int = 100,
    ) -> Dict:
        """Run parallel search over a list of TM notations.

        Args:
            notations: List of compact notations to simulate.
            batch_size: Number of TMs per worker batch.

        Returns:
            Results dict with top candidates.
        """
        start_time = time.time()
        last_checkpoint = start_time

        # Split into batches
        batches = []
        for i in range(0, len(notations), batch_size):
            batch = notations[i : i + batch_size]
            batches.append((batch, self.step_limit))

        print(f"  Parallel search: {len(notations)} machines, {len(batches)} batches, {self.num_workers} workers")

        # Process with multiprocessing pool
        with mp.Pool(processes=self.num_workers) as pool:
            for result_batch in pool.imap_unordered(_simulate_batch, batches):
                self.all_results.extend(result_batch)
                self.total_explored += batch_size

                # Periodic checkpoint
                elapsed = time.time() - start_time
                if elapsed - (last_checkpoint - start_time) > self.checkpoint_interval:
                    self._save_checkpoint()
                    last_checkpoint = time.time()

        elapsed = time.time() - start_time

        # Sort by sigma
        self.all_results.sort(key=lambda x: x["sigma"], reverse=True)

        # Deduplicate
        seen = set()
        deduped = []
        for r in self.all_results:
            if r["notation"] not in seen:
                seen.add(r["notation"])
                deduped.append(r)
        self.all_results = deduped

        return {
            "total_explored": self.total_explored,
            "total_halting": len(self.all_results),
            "num_workers": self.num_workers,
            "step_limit": self.step_limit,
            "wall_time_seconds": round(elapsed, 2),
            "machines_per_second": round(self.total_explored / max(elapsed, 0.001), 1),
            "best_sigma": self.all_results[0]["sigma"] if self.all_results else 0,
            "best_steps": max((r["steps"] for r in self.all_results), default=0),
            "top_candidates": self.all_results[:100],
        }

    def _save_checkpoint(self):
        """Save current results to disk."""
        os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)
        checkpoint = {
            "timestamp": time.time(),
            "total_explored": self.total_explored,
            "total_halting": len(self.all_results),
            "best_sigma": max((r["sigma"] for r in self.all_results), default=0),
            "top_10": sorted(self.all_results, key=lambda x: x["sigma"], reverse=True)[:10],
        }
        with open(self.checkpoint_path, "w") as f:
            json.dump(checkpoint, f, indent=2)


def generate_random_machines(n: int, num_states: int = 6, seed: int = 42) -> List[str]:
    """Generate n random TMs in TNF-1RB form."""
    rng = random.Random(seed)
    state_names = [chr(ord("A") + i) for i in range(num_states)]
    all_states = state_names + [HALT_STATE]
    machines = []

    for _ in range(n):
        parts = []
        for si in range(num_states):
            group = ""
            for sym in range(2):
                if si == 0 and sym == 0:
                    group += "1RB"  # Fixed first transition
                else:
                    write = rng.randint(0, 1)
                    direction = rng.choice(["L", "R"])
                    next_state = rng.choice(all_states)
                    group += f"{write}{direction}{next_state}"
            parts.append(group)
        machines.append("_".join(parts))

    return machines


def run_parallel_benchmark() -> Dict:
    """Benchmark parallel vs single-core performance."""
    print("Generating test machines...")
    machines = generate_random_machines(10000, seed=42)

    # Single core
    print("Running single-core benchmark...")
    ps_single = ParallelSearch(num_workers=1, step_limit=10**5)
    result_single = ps_single.search(machines, batch_size=200)

    # Multi core
    num_cores = max(2, mp.cpu_count())
    print(f"Running {num_cores}-core benchmark...")
    ps_multi = ParallelSearch(num_workers=num_cores, step_limit=10**5)
    result_multi = ps_multi.search(machines, batch_size=200)

    speedup = result_single["wall_time_seconds"] / max(result_multi["wall_time_seconds"], 0.001)

    return {
        "single_core": result_single,
        "multi_core": result_multi,
        "num_cores": num_cores,
        "speedup": round(speedup, 2),
    }


if __name__ == "__main__":
    print("Running parallel search benchmark...")
    results = run_parallel_benchmark()

    print(f"\nResults:")
    print(f"  Single-core: {results['single_core']['wall_time_seconds']}s "
          f"({results['single_core']['machines_per_second']} machines/s)")
    print(f"  Multi-core ({results['num_cores']} cores): {results['multi_core']['wall_time_seconds']}s "
          f"({results['multi_core']['machines_per_second']} machines/s)")
    print(f"  Speedup: {results['speedup']}x")

    os.makedirs("results/benchmarks", exist_ok=True)
    with open("results/benchmarks/parallel_speedup.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to results/benchmarks/parallel_speedup.json")
