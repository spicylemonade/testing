from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import write_canonical_json
from .scenarios import random_n_body, three_body, two_body
from .simulator import SimConfig, simulate


def build_scenario(name: str, n: int, seed: int) -> dict:
    if name == "two_body":
        return two_body(seed=seed)
    if name == "three_body":
        return three_body(seed=seed)
    if name == "random":
        return random_n_body(n=n, seed=seed)
    raise ValueError(f"Unsupported scenario: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal gravity simulator CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--method", default="baseline", choices=["baseline", "symplectic"])
    run.add_argument("--scenario", default="two_body", choices=["two_body", "three_body", "random"])
    run.add_argument("--n", type=int, default=16)
    run.add_argument("--steps", type=int, default=1000)
    run.add_argument("--dt", type=float, default=0.005)
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--softening", type=float, default=1e-3)
    run.add_argument("--snapshot-every", type=int, default=1)
    run.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.cmd == "run":
        scenario = build_scenario(name=args.scenario, n=args.n, seed=args.seed)
        result = simulate(
            scenario["positions"],
            scenario["velocities"],
            scenario["masses"],
            SimConfig(
                dt=args.dt,
                steps=args.steps,
                softening=args.softening,
                method=args.method,
                snapshot_every=max(1, args.snapshot_every),
            ),
        )
        payload = {
            "metadata": {
                "method": args.method,
                "scenario": args.scenario,
                "n": int(result["n_bodies"]),
                "steps": args.steps,
                "dt": args.dt,
                "seed": args.seed,
                "softening": args.softening,
            },
            "trajectory": result,
        }
        out_path = Path(args.out)
        write_canonical_json(out_path, payload)
        print(json.dumps({"output": str(out_path), "frames": len(result["frames"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
