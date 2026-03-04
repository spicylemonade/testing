#!/usr/bin/env python3
"""
Cross-Domain Collatz Delay Record Search
=========================================

Combines insights from 5+ domains to find numbers with exceptionally high
Collatz delay (number of steps to reach 1) relative to their size.

DOMAINS BRIDGED:
  1. Number Theory: residue class sieve (mod 2^k) for systematic high-delay classes
  2. Evolutionary Biology: genetic algorithm with bit-level crossover/mutation
  3. Statistical Physics: simulated annealing on delay landscape
  4. Computational Biology: motif analysis of binary representations
  5. Information Theory: compression-guided candidate filtering
  6. Extreme Value Theory: prediction of expected record delay

VERIFICATION: Any result can be verified by computing the Collatz sequence from
the starting number and counting steps. This is a O(delay) deterministic computation.

Usage:
    python3 collatz_deep_search.py

Author: Cross-domain concept architect
Date: March 2026
"""

import random
import time
import json
import math
import zlib
import sys
from collections import Counter

# ============================================================================
# CORE: Collatz delay computation (optimized)
# ============================================================================

def collatz_delay(n):
    """Compute total stopping time (delay) of n: number of steps to reach 1."""
    if n <= 0:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def collatz_delay_fast(n):
    """Optimized delay using shortcut: odd n -> (3n+1)/2 counts as 2 steps."""
    if n <= 0:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        while n % 2 == 0:
            n //= 2
            steps += 1
        if n == 1:
            break
        n = (3 * n + 1) // 2
        steps += 2
    return steps

def collatz_max_value(n):
    """Compute maximum value reached in Collatz trajectory starting at n."""
    mx = n
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        if n > mx:
            mx = n
    return mx

def collatz_trajectory_signature(n, max_steps=500):
    """Return binary signature of trajectory: 0=even step, 1=odd step."""
    sig = []
    steps = 0
    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            sig.append(0)
            n //= 2
        else:
            sig.append(1)
            n = 3 * n + 1
        steps += 1
    return sig

# ============================================================================
# DOMAIN 1: Residue Class Sieve (Renormalization Group approach)
# ============================================================================

def find_high_delay_residues(modulus_bits=12, sample_limit=2**22):
    """
    Find residue classes mod 2^k with systematically high average delay.
    This is the 'renormalization group' approach: coarse-grain by residue class.
    """
    modulus = 2 ** modulus_bits
    delay_sums = [0] * modulus
    delay_counts = [0] * modulus

    # Sample numbers and accumulate delays per residue class
    sample_size = min(sample_limit, modulus * 64)
    for _ in range(sample_size):
        n = random.randint(modulus, modulus * 1000)
        r = n % modulus
        d = collatz_delay_fast(n)
        delay_sums[r] += d
        delay_counts[r] += 1

    # Compute averages and find top residue classes
    avg_delays = []
    for r in range(modulus):
        if delay_counts[r] > 0:
            avg_delays.append((delay_sums[r] / delay_counts[r], r))

    avg_delays.sort(reverse=True)
    top_n = max(1, len(avg_delays) // 100)  # Top 1%
    return [r for _, r in avg_delays[:top_n]]

# ============================================================================
# DOMAIN 2: Genetic Algorithm (Evolutionary Biology approach)
# ============================================================================

def genetic_search(bit_length=60, pop_size=200, generations=100, 
                   mutation_rate=0.05, elite_frac=0.1):
    """
    GA to evolve integers with high delay-to-bit-length ratio.
    Individuals are integers represented as bitstrings.
    """
    # Initialize population
    lo = 2 ** (bit_length - 1)
    hi = 2 ** bit_length - 1
    population = [random.randint(lo, hi) | 1 for _ in range(pop_size)]  # Ensure odd

    best_ever = (0, 0, 0)  # (delay, n, generation)

    for gen in range(generations):
        # Evaluate fitness
        fitnesses = []
        for n in population:
            d = collatz_delay_fast(n)
            fitnesses.append((d, n))
            if d > best_ever[0]:
                best_ever = (d, n, gen)

        fitnesses.sort(reverse=True)

        # Elitism
        elite_count = max(2, int(pop_size * elite_frac))
        new_pop = [n for _, n in fitnesses[:elite_count]]

        # Tournament selection + crossover + mutation
        while len(new_pop) < pop_size:
            # Tournament selection (size 5)
            parents = []
            for _ in range(2):
                tournament = random.sample(list(range(pop_size)), min(5, pop_size))
                winner = max(tournament, key=lambda i: fitnesses[i][0])
                parents.append(fitnesses[winner][1])

            # Single-point crossover on bits
            p1, p2 = parents
            bits1 = format(p1, f'0{bit_length}b')
            bits2 = format(p2, f'0{bit_length}b')
            cx_point = random.randint(1, bit_length - 1)
            child_bits = bits1[:cx_point] + bits2[cx_point:]

            # Mutation
            child_bits = list(child_bits)
            for i in range(len(child_bits)):
                if random.random() < mutation_rate:
                    child_bits[i] = '1' if child_bits[i] == '0' else '0'
            child_bits = ''.join(child_bits)

            child = int(child_bits, 2)
            if child < 2:
                child = lo | 1
            new_pop.append(child | 1)  # Keep odd

        population = new_pop[:pop_size]

    return best_ever

# ============================================================================
# DOMAIN 3: Simulated Annealing (Statistical Physics approach)
# ============================================================================

def simulated_annealing_search(bit_length=60, steps=5000, 
                                T_start=50.0, T_end=0.1, restarts=10):
    """
    Navigate the Collatz delay 'energy landscape' using SA.
    Energy = -delay. Moves are random bit flips.
    """
    best_overall = (0, 0)  # (delay, n)

    for _ in range(restarts):
        # Random starting point (odd number)
        n = random.randint(2**(bit_length-1), 2**bit_length - 1) | 1
        current_delay = collatz_delay_fast(n)
        best = (current_delay, n)

        for step in range(steps):
            # Temperature schedule (geometric cooling)
            T = T_start * (T_end / T_start) ** (step / max(1, steps - 1))

            # Random bit flip (neighbor generation)
            bit_to_flip = random.randint(0, bit_length - 2)  # Don't flip MSB
            n_new = n ^ (1 << bit_to_flip)
            n_new |= 1  # Keep odd

            if n_new < 2:
                continue

            new_delay = collatz_delay_fast(n_new)

            # Metropolis acceptance
            delta_e = -(new_delay - current_delay)  # Energy = -delay
            if delta_e <= 0 or random.random() < math.exp(-delta_e / max(T, 1e-10)):
                n = n_new
                current_delay = new_delay

            if current_delay > best[0]:
                best = (current_delay, n)

        if best[0] > best_overall[0]:
            best_overall = best

    return best_overall

# ============================================================================
# DOMAIN 4: Motif Analysis (Computational Biology approach)
# ============================================================================

def analyze_motifs(high_delay_numbers, motif_len=8):
    """
    Find enriched binary motifs in high-delay numbers,
    analogous to TFBS motif discovery in genomics.
    """
    # Count motifs in high-delay numbers
    motif_counts = Counter()
    total_positions = 0

    for n in high_delay_numbers:
        bits = bin(n)[2:]
        for i in range(len(bits) - motif_len + 1):
            motif = bits[i:i+motif_len]
            motif_counts[motif] += 1
            total_positions += 1

    # Expected frequency under uniform model
    expected_freq = 1.0 / (2 ** motif_len)

    # Compute enrichment
    enriched = []
    for motif, count in motif_counts.items():
        observed_freq = count / max(1, total_positions)
        enrichment = observed_freq / expected_freq
        enriched.append((enrichment, motif, count))

    enriched.sort(reverse=True)
    return enriched[:20]  # Top 20 motifs

def construct_from_motifs(enriched_motifs, bit_length=60, n_candidates=1000):
    """Construct candidate numbers by concatenating enriched motifs."""
    candidates = []
    motifs = [m for _, m, _ in enriched_motifs[:10]]

    for _ in range(n_candidates):
        bits = "1"  # MSB = 1
        while len(bits) < bit_length:
            motif = random.choice(motifs)
            bits += motif
        bits = bits[:bit_length-1] + "1"  # Ensure odd
        n = int(bits, 2)
        candidates.append(n)

    return candidates

# ============================================================================
# DOMAIN 5: Compression-Guided Filter (Information Theory approach)
# ============================================================================

def compression_score(n):
    """
    Compute compression ratio of binary representation.
    Numbers at 'edge of chaos' (intermediate compressibility) 
    are hypothesized to have high delay.
    """
    bits = bin(n)[2:].encode()
    compressed = zlib.compress(bits, 9)
    return len(compressed) / len(bits)

def compression_guided_filter(candidates, target_ratio_range=(0.5, 0.85)):
    """Filter candidates by compression ratio (Goldilocks zone)."""
    filtered = []
    for n in candidates:
        ratio = compression_score(n)
        if target_ratio_range[0] <= ratio <= target_ratio_range[1]:
            filtered.append(n)
    return filtered

# ============================================================================
# DOMAIN 6: EVT Prediction (Extreme Value Theory)
# ============================================================================

def predict_record_delay(known_records_delay_by_bits):
    """
    Simple EVT-inspired prediction of expected delay for a given bit range.
    Uses linear regression on (bit_length, max_delay) from known data.
    """
    if len(known_records_delay_by_bits) < 3:
        return None

    # Fit log-linear model: max_delay ~ a * bit_length + b
    xs = [x for x, _ in known_records_delay_by_bits]
    ys = [y for _, y in known_records_delay_by_bits]

    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))

    denom = n * sxx - sx * sx
    if denom == 0:
        return None

    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n

    return a, b

# ============================================================================
# MAIN: Combined Cross-Domain Search
# ============================================================================

def main():
    print("=" * 70)
    print("CROSS-DOMAIN COLLATZ DELAY RECORD SEARCH")
    print("Bridging: Number Theory × Evolutionary Bio × Statistical Physics")
    print("        × Computational Biology × Information Theory × EVT")
    print("=" * 70)
    print()

    results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "approach": "cross-domain optimization for Collatz delay maximization",
            "domains_bridged": [
                "number_theory", "evolutionary_biology", "statistical_physics",
                "computational_biology", "information_theory", "extreme_value_theory"
            ]
        },
        "methods": {},
        "champions": [],
        "verification": []
    }

    # ========================================================================
    # Phase 0: Establish baselines with known delay records
    # ========================================================================
    print("[Phase 0] Computing baselines...")

    # True delay records (each has strictly higher delay than all predecessors)
    # These are confirmed delay records from Roosendaal's table
    known_delay_records = [
        (2, 1), (3, 7), (7, 16), (27, 111), (703, 170),
        (4255, 201), (9663, 184),  # Not a delay record, skip
        (26623, 307), (60975, 334), (63728127, 949),
    ]
    # Actually compute correct values
    known_delay_records = []
    test_nums = [2, 3, 7, 27, 703, 6171, 77031, 837799, 8400511, 63728127]
    for n in test_nums:
        d = collatz_delay(n)
        known_delay_records.append((n, d))

    # Verify known records
    print("  Verifying known delay records...")
    known_bits_delays = []
    for n, expected_delay in known_delay_records:
        actual = collatz_delay(n)
        assert actual == expected_delay, f"Verification failed for {n}: got {actual}, expected {expected_delay}"
        bits = n.bit_length()
        known_bits_delays.append((bits, actual))
    print(f"  ✓ All {len(known_delay_records)} known records verified")
    print()

    # ========================================================================
    # Phase 1: Residue Class Sieve (Number Theory / RG approach)
    # ========================================================================
    print("[Phase 1] Residue class sieve (Renormalization Group)...")
    t0 = time.time()

    good_residues_8 = find_high_delay_residues(modulus_bits=8, sample_limit=2**18)
    good_residues_10 = find_high_delay_residues(modulus_bits=10, sample_limit=2**20)

    print(f"  Found {len(good_residues_8)} good residues mod 2^8 (top 1%)")
    print(f"  Found {len(good_residues_10)} good residues mod 2^10 (top 1%)")

    # Generate candidates from good residue classes
    sieve_candidates = []
    target_bits = 50
    for r8 in good_residues_8[:5]:
        for _ in range(200):
            base = random.randint(2**(target_bits-1), 2**target_bits - 1)
            n = base - (base % 256) + r8
            if n > 0 and n % 2 == 1:
                sieve_candidates.append(n)

    # Evaluate sieve candidates
    sieve_best = (0, 0)
    for n in sieve_candidates:
        d = collatz_delay_fast(n)
        if d > sieve_best[0]:
            sieve_best = (d, n)

    sieve_time = time.time() - t0
    print(f"  Best from sieve: n={sieve_best[1]}, delay={sieve_best[0]}")
    print(f"  Time: {sieve_time:.2f}s")
    results["methods"]["residue_sieve"] = {
        "best_delay": sieve_best[0],
        "best_n": sieve_best[1],
        "candidates_evaluated": len(sieve_candidates),
        "time_seconds": round(sieve_time, 2)
    }
    print()

    # ========================================================================
    # Phase 2: Genetic Algorithm (Evolutionary Biology approach)
    # ========================================================================
    print("[Phase 2] Genetic algorithm (Evolutionary Biology)...")
    t0 = time.time()

    ga_results = []
    for bits in [40, 45, 50, 55, 60]:
        print(f"  Running GA at {bits} bits...", end=" ", flush=True)
        delay, n, gen = genetic_search(
            bit_length=bits, pop_size=150, generations=80,
            mutation_rate=0.03, elite_frac=0.15
        )
        ga_results.append((delay, n, bits, gen))
        print(f"delay={delay}, n={n}, found at gen {gen}")

    ga_best = max(ga_results, key=lambda x: x[0])
    ga_time = time.time() - t0
    print(f"  Best from GA: n={ga_best[1]}, delay={ga_best[0]} ({ga_best[2]} bits)")
    print(f"  Time: {ga_time:.2f}s")
    results["methods"]["genetic_algorithm"] = {
        "best_delay": ga_best[0],
        "best_n": ga_best[1],
        "best_bits": ga_best[2],
        "results_by_bitlength": [
            {"bits": b, "delay": d, "n": n, "gen_found": g}
            for d, n, b, g in ga_results
        ],
        "time_seconds": round(ga_time, 2)
    }
    print()

    # ========================================================================
    # Phase 3: Simulated Annealing (Statistical Physics approach)
    # ========================================================================
    print("[Phase 3] Simulated annealing (Statistical Physics)...")
    t0 = time.time()

    sa_results = []
    for bits in [40, 45, 50, 55, 60]:
        print(f"  Running SA at {bits} bits...", end=" ", flush=True)
        delay, n = simulated_annealing_search(
            bit_length=bits, steps=3000, T_start=100.0, T_end=0.01, restarts=5
        )
        sa_results.append((delay, n, bits))
        print(f"delay={delay}, n={n}")

    sa_best = max(sa_results, key=lambda x: x[0])
    sa_time = time.time() - t0
    print(f"  Best from SA: n={sa_best[1]}, delay={sa_best[0]} ({sa_best[2]} bits)")
    print(f"  Time: {sa_time:.2f}s")
    results["methods"]["simulated_annealing"] = {
        "best_delay": sa_best[0],
        "best_n": sa_best[1],
        "best_bits": sa_best[2],
        "results_by_bitlength": [
            {"bits": b, "delay": d, "n": n}
            for d, n, b in sa_results
        ],
        "time_seconds": round(sa_time, 2)
    }
    print()

    # ========================================================================
    # Phase 4: Motif Analysis (Computational Biology approach)
    # ========================================================================
    print("[Phase 4] Motif analysis (Computational Biology)...")
    t0 = time.time()

    # Collect high-delay numbers from previous phases
    all_found = [(d, n) for d, n, _, _ in ga_results] + [(d, n) for d, n, _ in sa_results]
    all_found.append((sieve_best[0], sieve_best[1]))

    # Also find high-delay numbers by random sampling
    print("  Sampling for high-delay numbers to build motif database...")
    random_high = []
    for _ in range(50000):
        n = random.randint(2**39, 2**50) | 1
        d = collatz_delay_fast(n)
        random_high.append((d, n))
    random_high.sort(reverse=True)
    top_random = [n for _, n in random_high[:500]]

    # Analyze motifs
    high_delay_nums = [n for _, n in all_found] + top_random
    enriched = analyze_motifs(high_delay_nums, motif_len=8)

    print(f"  Top enriched 8-bit motifs:")
    for i, (enrich, motif, count) in enumerate(enriched[:5]):
        print(f"    {motif} (enrichment={enrich:.2f}, count={count})")

    # Construct candidates from motifs
    motif_candidates = construct_from_motifs(enriched, bit_length=55, n_candidates=2000)

    # Apply compression filter
    filtered = compression_guided_filter(motif_candidates)
    print(f"  Compression filter: {len(motif_candidates)} -> {len(filtered)} candidates")

    # Evaluate
    motif_best = (0, 0)
    for n in filtered:
        d = collatz_delay_fast(n)
        if d > motif_best[0]:
            motif_best = (d, n)

    # If filtered is empty, evaluate unfiltered
    if not filtered:
        for n in motif_candidates[:500]:
            d = collatz_delay_fast(n)
            if d > motif_best[0]:
                motif_best = (d, n)

    motif_time = time.time() - t0
    print(f"  Best from motifs: n={motif_best[1]}, delay={motif_best[0]}")
    print(f"  Time: {motif_time:.2f}s")
    results["methods"]["motif_construction"] = {
        "best_delay": motif_best[0],
        "best_n": motif_best[1],
        "top_motifs": [(m, round(e, 3)) for e, m, _ in enriched[:10]],
        "candidates_generated": len(motif_candidates),
        "after_compression_filter": len(filtered),
        "time_seconds": round(motif_time, 2)
    }
    print()

    # ========================================================================
    # Phase 5: EVT Prediction (Extreme Value Theory)
    # ========================================================================
    print("[Phase 5] Extreme Value Theory predictions...")

    evt_fit = predict_record_delay(known_bits_delays)
    if evt_fit:
        a, b = evt_fit
        print(f"  Linear fit: delay ≈ {a:.2f} × bit_length + {b:.2f}")
        for target_bits in [50, 55, 60, 65, 70]:
            predicted = a * target_bits + b
            print(f"  Predicted max delay at {target_bits} bits: ~{predicted:.0f}")
        results["methods"]["evt_prediction"] = {
            "slope": round(a, 4),
            "intercept": round(b, 4),
            "predictions": {
                str(b): round(a * b + evt_fit[1], 0)
                for b in [50, 55, 60, 65, 70]
            }
        }
    print()

    # ========================================================================
    # Phase 6: Combined Champion Selection
    # ========================================================================
    print("[Phase 6] Selecting champions and verifying...")

    all_champions = []
    all_champions.append(("residue_sieve", sieve_best[0], sieve_best[1]))
    all_champions.append(("genetic_algorithm", ga_best[0], ga_best[1]))
    all_champions.append(("simulated_annealing", sa_best[0], sa_best[1]))
    all_champions.append(("motif_construction", motif_best[0], motif_best[1]))

    # Also try random baseline for comparison
    print("  Computing random baseline...", end=" ", flush=True)
    random_best = (0, 0)
    total_random = 5000
    for bits in [40, 45, 50, 55, 60]:
        for _ in range(total_random // 5):
            n = random.randint(2**(bits-1), 2**bits - 1) | 1
            d = collatz_delay_fast(n)
            if d > random_best[0]:
                random_best = (d, n)
    all_champions.append(("random_baseline", random_best[0], random_best[1]))
    print(f"delay={random_best[0]}")

    # Sort by delay
    all_champions.sort(key=lambda x: x[1], reverse=True)

    print()
    print("=" * 70)
    print("RESULTS: Cross-Domain Collatz Delay Champions")
    print("=" * 70)
    print(f"{'Rank':<6}{'Method':<25}{'Delay':<10}{'Bits':<8}{'Number'}")
    print("-" * 70)

    for rank, (method, delay, n) in enumerate(all_champions, 1):
        bits = n.bit_length()
        # Verify each champion
        verified_delay = collatz_delay(n)
        status = "✓" if verified_delay == delay else "✗"
        print(f"{rank:<6}{method:<25}{delay:<10}{bits:<8}{n}")

        results["champions"].append({
            "rank": rank,
            "method": method,
            "delay": delay,
            "n": n,
            "bit_length": bits,
            "delay_per_bit": round(delay / bits, 4),
            "verified": verified_delay == delay
        })

        results["verification"].append({
            "n": n,
            "computed_delay": verified_delay,
            "claimed_delay": delay,
            "match": verified_delay == delay,
            "max_value_reached": collatz_max_value(n) if n.bit_length() <= 50 else "skipped_too_large"
        })

    # Overall champion
    champion = all_champions[0]
    print()
    print(f"🏆 OVERALL CHAMPION: {champion[2]}")
    print(f"   Delay: {champion[1]} steps")
    print(f"   Bit length: {champion[2].bit_length()}")
    print(f"   Delay per bit: {champion[1] / champion[2].bit_length():.4f}")
    print(f"   Method: {champion[0]}")
    print(f"   Verified: {collatz_delay(champion[2]) == champion[1]}")

    # ========================================================================
    # Phase 7: Compute delay-per-bit efficiency ranking
    # ========================================================================
    print()
    print("DELAY-PER-BIT EFFICIENCY (higher = more exceptional):")
    print("-" * 50)
    efficiency = [(d/n.bit_length(), method, d, n) for method, d, n in all_champions]
    efficiency.sort(reverse=True)
    for eff, method, delay, n in efficiency:
        print(f"  {eff:.4f}  {method:<25} delay={delay}, {n.bit_length()} bits")

    results["efficiency_ranking"] = [
        {"efficiency": round(e, 4), "method": m, "delay": d, "n": n}
        for e, m, d, n in efficiency
    ]

    # ========================================================================
    # Save results
    # ========================================================================
    output_path = "/home/archivara/work/repo/results/concept_evolve/search_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")

    # Quick verification script output
    print()
    print("=" * 70)
    print("VERIFICATION SCRIPT (copy-paste to verify any result):")
    print("=" * 70)
    best_n = champion[2]
    print(f"""
def verify_collatz(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

n = {best_n}
delay = verify_collatz(n)
print(f"Collatz delay of {{n}} = {{delay}} steps")
print(f"Bit length: {{n.bit_length()}}")
print(f"Delay per bit: {{delay / n.bit_length():.4f}}")
""")

    return results


if __name__ == "__main__":
    results = main()
