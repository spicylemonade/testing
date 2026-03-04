"""TM breeding: recombination of sub-components from high-scoring machines.

Decomposes TM transition tables into functional sub-modules and recombines
them to create novel machines.

Three recombination strategies:
1. Row swap: exchange the transitions for an entire state between two machines
2. Column swap: exchange all transitions for a given symbol
3. Block crossover: split the transition table at a random point and combine
"""

from __future__ import annotations

import json
import os
import random
from typing import Dict, List, Tuple

from src.tm_simulator import TuringMachine, HALT_STATE
from src.tm_accelerated import AcceleratedTuringMachine, _C_AVAILABLE


def decompose_into_modules(notation: str) -> Dict:
    """Decompose a TM into functional sub-components.

    Identifies:
    - Counter modules: states that increment/decrement a binary counter
    - Sweep modules: states that sweep left or right writing a fixed symbol
    - Shift modules: states that shift tape content left or right
    """
    tm = TuringMachine.from_compact(notation)
    modules = {
        "counter": [],   # States that read/write different symbols
        "sweep": [],     # States that always write the same and move same direction
        "mixed": [],     # States with heterogeneous behavior
    }

    for state in tm.states:
        if state not in tm.transitions:
            continue
        trans = tm.transitions[state]
        if len(trans) < 2:
            modules["mixed"].append(state)
            continue

        writes = set()
        dirs = set()
        for sym, (w, d, ns) in trans.items():
            writes.add(w)
            dirs.add(d)

        if len(writes) == 1 and len(dirs) == 1:
            modules["sweep"].append(state)
        elif len(writes) == 2:
            modules["counter"].append(state)
        else:
            modules["mixed"].append(state)

    return modules


def row_swap(parent1: str, parent2: str, state_idx: int) -> str:
    """Swap all transitions for a given state between two parents."""
    tm1 = TuringMachine.from_compact(parent1)
    tm2 = TuringMachine.from_compact(parent2)

    state = chr(ord("A") + state_idx)
    new_trans = {s: dict(syms) for s, syms in tm1.transitions.items()}

    if state in tm2.transitions:
        new_trans[state] = dict(tm2.transitions[state])

    child = TuringMachine(new_trans)
    return child.to_compact()


def column_swap(parent1: str, parent2: str, symbol: int) -> str:
    """Swap all transitions for a given symbol between two parents."""
    tm1 = TuringMachine.from_compact(parent1)
    tm2 = TuringMachine.from_compact(parent2)

    new_trans = {s: dict(syms) for s, syms in tm1.transitions.items()}

    for state in tm2.states:
        if state in tm2.transitions and symbol in tm2.transitions[state]:
            if state not in new_trans:
                new_trans[state] = {}
            new_trans[state][symbol] = tm2.transitions[state][symbol]

    child = TuringMachine(new_trans)
    return child.to_compact()


def block_crossover(parent1: str, parent2: str, crossover_point: int) -> str:
    """Split transition table at a point and combine.

    Transitions are ordered: (A,0), (A,1), (B,0), (B,1), ...
    Take first `crossover_point` from parent1, rest from parent2.
    """
    tm1 = TuringMachine.from_compact(parent1)
    tm2 = TuringMachine.from_compact(parent2)

    n = max(tm1.num_states, tm2.num_states)
    state_names = [chr(ord("A") + i) for i in range(n)]

    new_trans = {}
    idx = 0
    for state in state_names:
        new_trans[state] = {}
        for sym in range(2):
            source = tm1 if idx < crossover_point else tm2
            if state in source.transitions and sym in source.transitions[state]:
                new_trans[state][sym] = source.transitions[state][sym]
            elif state in tm1.transitions and sym in tm1.transitions[state]:
                new_trans[state][sym] = tm1.transitions[state][sym]
            else:
                new_trans[state][sym] = (0, "R", HALT_STATE)
            idx += 1

    child = TuringMachine(new_trans)
    return child.to_compact()


def breed_population(
    parents: List[str],
    num_offspring: int = 1000,
    step_limit: int = 10**6,
    seed: int = 42,
) -> Dict:
    """Breed a population of TMs from parent machines.

    Uses all three recombination strategies.
    """
    rng = random.Random(seed)
    offspring = []
    seen = set(parents)

    for _ in range(num_offspring):
        p1, p2 = rng.sample(parents, 2)
        n_states = 6

        strategy = rng.choice(["row_swap", "column_swap", "block_crossover"])

        if strategy == "row_swap":
            state_idx = rng.randint(0, n_states - 1)
            child = row_swap(p1, p2, state_idx)
        elif strategy == "column_swap":
            symbol = rng.randint(0, 1)
            child = column_swap(p1, p2, symbol)
        else:
            crossover_point = rng.randint(1, n_states * 2 - 1)
            child = block_crossover(p1, p2, crossover_point)

        if child not in seen:
            seen.add(child)
            offspring.append((child, strategy))

    # Simulate all offspring
    results = []
    for notation, strategy in offspring:
        if _C_AVAILABLE:
            atm = AcceleratedTuringMachine.from_compact(notation)
            steps, ones, halted, _ = atm.simulate_c(max_steps=step_limit)
        else:
            atm = AcceleratedTuringMachine.from_compact(notation)
            steps, ones, halted, _ = atm.simulate(max_steps=step_limit)

        if halted:
            results.append({
                "notation": notation,
                "steps": steps,
                "sigma": ones,
                "strategy": strategy,
            })

    results.sort(key=lambda x: x["sigma"], reverse=True)

    return {
        "strategy": "tm_breeding",
        "num_parents": len(parents),
        "num_offspring_attempted": num_offspring,
        "num_unique_offspring": len(offspring),
        "num_halting": len(results),
        "step_limit": step_limit,
        "top_candidates": results[:100],
        "best_sigma": results[0]["sigma"] if results else 0,
        "best_steps": max((r["steps"] for r in results), default=0),
        "strategy_breakdown": {
            s: sum(1 for r in results if r["strategy"] == s)
            for s in ["row_swap", "column_swap", "block_crossover"]
        },
    }


if __name__ == "__main__":
    parents = [
        "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE",  # Kropitz t15
        "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE",  # mxdys
        "1RB1LE_1RC1RF_1LD0RB_1RE1LA_0LA1RZ_1RC0RE",  # Kropitz e1B
        "1RB1LE_1RC1RF_1LD0RB_1RE0LC_1LA1RZ_1LD1RC",  # Kropitz 2010
    ]

    print("Breeding TMs from champion parents...")

    # Document decomposition
    print("\nModule decomposition of parents:")
    for p in parents:
        modules = decompose_into_modules(p)
        print(f"  {p[:30]}...: counter={modules['counter']}, sweep={modules['sweep']}, mixed={modules['mixed']}")

    results = breed_population(parents, num_offspring=5000, step_limit=10**6, seed=42)

    print(f"\nBreeding results:")
    print(f"  Unique offspring: {results['num_unique_offspring']}")
    print(f"  Halting: {results['num_halting']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Strategy breakdown: {results['strategy_breakdown']}")

    if results['top_candidates']:
        print(f"\n  Top 5:")
        for c in results['top_candidates'][:5]:
            print(f"    {c['notation']}: sigma={c['sigma']}, steps={c['steps']} ({c['strategy']})")

    os.makedirs("results", exist_ok=True)
    with open("results/breeding_design.md", "w") as f:
        f.write("# TM Breeding Design\n\n")
        f.write("## Decomposition Scheme\n\n")
        f.write("Each TM transition table is decomposed into functional modules:\n")
        f.write("- **Counter modules**: States that read/write different symbols (binary counter behavior)\n")
        f.write("- **Sweep modules**: States that always write the same symbol and move in the same direction\n")
        f.write("- **Mixed modules**: States with heterogeneous behavior\n\n")
        f.write("## Recombination Strategies\n\n")
        f.write("1. **Row swap**: Exchange all transitions for a given state between parents\n")
        f.write("2. **Column swap**: Exchange all transitions for a given symbol\n")
        f.write("3. **Block crossover**: Split the transition table at a random point\n\n")
        f.write(f"## Results\n\n")
        f.write(f"- Parents: {len(parents)}\n")
        f.write(f"- Offspring: {results['num_unique_offspring']}\n")
        f.write(f"- Halting: {results['num_halting']}\n")
        f.write(f"- Best sigma: {results['best_sigma']}\n")
        f.write(f"- Strategy breakdown: {results['strategy_breakdown']}\n")

    print("\nSaved design to results/breeding_design.md")
