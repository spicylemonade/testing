"""Genetic algorithm / evolutionary search for combinatorial mutation optimization.

Evolves a population of mutation sets through crossover, mutation, and
selection to find near-optimal combinations.
"""

from __future__ import annotations

import time
import random
from typing import List, Dict, Any, Tuple

import pandas as pd
import numpy as np


def evolutionary_search(
    energy_model: "EnergyModel",
    candidates: pd.DataFrame,
    k: int,
    population_size: int = 200,
    generations: int = 100,
    mutation_rate: float = 0.3,
    crossover_rate: float = 0.7,
    elitism_fraction: float = 0.1,
    top_results: int = 50,
    seed: int = 42,
) -> List[Dict[str, Any]]:
    """Evolutionary search over mutation combinations.

    Maintains a population of k-mutation sets that evolves through:
    - Crossover: swap mutations between two parent sets
    - Mutation: randomly replace a mutation in a set
    - Selection: keep the fittest individuals
    - Elitism: preserve top fraction across generations

    Args:
        energy_model: EnergyModel instance for scoring
        candidates: DataFrame of candidate single mutations
        k: Number of simultaneous mutations
        population_size: Number of individuals in population
        generations: Number of evolutionary generations
        mutation_rate: Probability of mutating each individual
        crossover_rate: Probability of crossover between pairs
        elitism_fraction: Fraction of top individuals to preserve
        top_results: Number of top results to return
        seed: Random seed

    Returns:
        List of result dicts sorted by score
    """
    start = time.time()
    rng = random.Random(seed)
    np_rng = np.random.RandomState(seed)

    N = energy_model.n_candidates
    positions = candidates["position"].values

    # Initialize population with random valid k-mutation sets
    population = _initialize_population(
        N, k, positions, population_size, rng
    )

    # Score initial population
    fitness = [energy_model.score(ind) for ind in population]

    n_elite = max(1, int(population_size * elitism_fraction))

    best_ever_score = max(fitness)
    best_ever_idx = fitness.index(best_ever_score)
    best_ever = population[best_ever_idx]

    for gen in range(generations):
        # Sort by fitness
        sorted_pairs = sorted(
            zip(fitness, population), key=lambda x: x[0], reverse=True
        )
        fitness = [f for f, _ in sorted_pairs]
        population = [ind for _, ind in sorted_pairs]

        # Track best
        if fitness[0] > best_ever_score:
            best_ever_score = fitness[0]
            best_ever = population[0]

        # Elitism: preserve top individuals
        new_population = [ind[:] for ind in population[:n_elite]]

        # Fill rest of population with offspring
        while len(new_population) < population_size:
            # Select parents via tournament selection
            parent1 = _tournament_select(population, fitness, rng)
            parent2 = _tournament_select(population, fitness, rng)

            # Crossover
            if rng.random() < crossover_rate:
                child = _crossover(parent1, parent2, positions, rng)
            else:
                child = parent1[:]

            # Mutation
            if rng.random() < mutation_rate:
                child = _mutate(child, N, positions, rng)

            if _is_valid(child, positions):
                new_population.append(child)

        population = new_population[:population_size]
        fitness = [energy_model.score(ind) for ind in population]

        if (gen + 1) % 20 == 0 or gen == 0:
            elapsed = time.time() - start
            print(
                f"  Gen {gen + 1}/{generations}: "
                f"best={max(fitness):.4f}, "
                f"mean={np.mean(fitness):.4f}, "
                f"best_ever={best_ever_score:.4f}, "
                f"t={elapsed:.2f}s"
            )

    elapsed = time.time() - start

    # Collect unique top solutions
    all_solutions = {}
    for ind, fit in zip(population, fitness):
        key = tuple(sorted(ind))
        if key not in all_solutions or fit > all_solutions[key][0]:
            all_solutions[key] = (fit, ind)

    # Sort and convert
    sorted_solutions = sorted(
        all_solutions.values(), key=lambda x: x[0], reverse=True
    )

    results = []
    for score, indices in sorted_solutions[:top_results]:
        mutations_str = energy_model.format_mutations(indices)
        results.append({
            "mutations": mutations_str,
            "predicted_ddG": score,
            "confidence": 0.7,  # Heuristic confidence
            "indices": indices,
        })

    print(
        f"Evolutionary search complete: {len(results)} unique solutions "
        f"in {elapsed:.2f}s"
    )
    if results:
        print(f"Best: {results[0]['mutations']} = {results[0]['predicted_ddG']:.4f}")

    return results


def _initialize_population(
    N: int, k: int, positions: np.ndarray, size: int, rng: random.Random
) -> List[List[int]]:
    """Create initial population of valid k-mutation sets."""
    population = []
    attempts = 0
    max_attempts = size * 100

    while len(population) < size and attempts < max_attempts:
        attempts += 1
        indices = rng.sample(range(N), k)
        if _is_valid(indices, positions):
            population.append(indices)

    # If not enough valid individuals, relax constraint
    while len(population) < size:
        population.append(population[rng.randint(0, len(population) - 1)][:])

    return population


def _is_valid(indices: List[int], positions: np.ndarray) -> bool:
    """Check that no two mutations are at the same position."""
    pos_set = set()
    for idx in indices:
        if idx < 0 or idx >= len(positions):
            return False
        p = positions[idx]
        if p in pos_set:
            return False
        pos_set.add(p)
    return True


def _tournament_select(
    population: List[List[int]],
    fitness: List[float],
    rng: random.Random,
    tournament_size: int = 3,
) -> List[int]:
    """Select an individual via tournament selection."""
    candidates = rng.sample(range(len(population)), min(tournament_size, len(population)))
    best = max(candidates, key=lambda i: fitness[i])
    return population[best]


def _crossover(
    parent1: List[int],
    parent2: List[int],
    positions: np.ndarray,
    rng: random.Random,
) -> List[int]:
    """Uniform crossover: randomly select each mutation from either parent."""
    k = len(parent1)
    child = []
    used_positions = set()

    for i in range(k):
        # Try from random parent
        if rng.random() < 0.5:
            candidates = [parent1[i], parent2[i]]
        else:
            candidates = [parent2[i], parent1[i]]

        added = False
        for c in candidates:
            if c < len(positions) and positions[c] not in used_positions:
                child.append(c)
                used_positions.add(positions[c])
                added = True
                break

        if not added:
            # Fallback: use any available from parent1
            for c in parent1:
                if c < len(positions) and positions[c] not in used_positions:
                    child.append(c)
                    used_positions.add(positions[c])
                    break

    return child[:k]


def _mutate(
    individual: List[int],
    N: int,
    positions: np.ndarray,
    rng: random.Random,
) -> List[int]:
    """Replace a random mutation with a different one."""
    if not individual:
        return individual

    child = individual[:]
    idx_to_replace = rng.randint(0, len(child) - 1)
    used_positions = {positions[i] for i in child if i != child[idx_to_replace]}

    # Try to find a valid replacement
    for _ in range(50):
        new_idx = rng.randint(0, N - 1)
        if new_idx < len(positions) and positions[new_idx] not in used_positions:
            child[idx_to_replace] = new_idx
            break

    return child
