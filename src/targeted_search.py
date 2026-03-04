#!/usr/bin/env python3
"""Targeted search for OEIS A284668 a(19).

Instead of random sampling, we use structured search strategies:

1. Known delay record structure: records tend to be odd numbers with
   specific binary patterns (many 1-bits, especially in certain positions)
2. Exhaustive search of the KNOWN delay record sequence A006877
3. Focus on numbers that are known delay record holders and multiply/shift them
4. Use the fact that delay records below 10^19 must be in A006877

Key realization: A284668(19) = the number below 10^19 with highest total
stopping time. This is simply the largest entry in A006877 that is < 10^19.

The A006877 sequence (delay record holders) is well-studied. From Roosendaal's
database, the sequence continues well beyond 10^18. We need to find all
delay record holders below 10^19.

Strategy: Since delay records get sparser, we can scan the delay record
sequence directly. From the OEIS data on A006877, the records near 10^18
have delays around 2000-2300. We need to find any records in [10^18, 10^19)
that beat 2283.

The expected number of records in [10^18, 10^19) is ~7-8 based on the
empirical rate. So there should be records there, but finding them
requires scanning a LOT of numbers.

Alternative approach: use the OEIS/Roosendaal data to check if a(19) is
already known in some form.
"""

import json
import time
import multiprocessing as mp
from pathlib import Path
import random

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "experiments"

LOOKUP_BITS = 20
LOOKUP_LIMIT = 1 << LOOKUP_BITS
SHORTCUT_K = 16


def build_lookup_table():
    table = [0] * LOOKUP_LIMIT
    for n in range(2, LOOKUP_LIMIT):
        x = n
        s = 0
        while x >= n:
            if x & 1:
                x = (3 * x + 1) >> 1
                s += 2
            else:
                x >>= 1
                s += 1
        table[n] = s + table[x]
    return table


def build_shortcut_table(k):
    table = []
    twok = 1 << k
    for r in range(twok):
        x = r if r > 0 else twok
        alpha = twok
        beta = r if r > 0 else twok
        shifts_done = 0
        steps = 0
        while shifts_done < k:
            if beta & 1:
                alpha = 3 * alpha
                beta = 3 * beta + 1
                steps += 1
                alpha >>= 1
                beta >>= 1
                shifts_done += 1
                steps += 1
            else:
                alpha >>= 1
                beta >>= 1
                shifts_done += 1
                steps += 1
        table.append((alpha, beta, steps))
    table[0] = (1, 0, k)
    return table


def delay_shortcut(n, table, k, lookup):
    x = n
    steps = 0
    while x >= LOOKUP_LIMIT:
        r = int(x) & ((1 << k) - 1)
        a, b, s = table[r]
        x = a * (x >> k) + b
        steps += s
    return steps + lookup[x]


def _init_worker():
    global _w_lookup, _w_table, _w_k
    _w_lookup = build_lookup_table()
    _w_table = build_shortcut_table(SHORTCUT_K)
    _w_k = SHORTCUT_K


def _scan_range_odd(args):
    """Scan odd numbers in [start, end) returning best delay found."""
    start, end = args
    global _w_lookup, _w_table, _w_k
    
    best_delay = 0
    best_n = start
    records = []
    
    s = start if start & 1 else start + 1
    for n in range(s, end, 2):
        d = delay_shortcut(n, _w_table, _w_k, _w_lookup)
        if d > best_delay:
            best_delay = d
            best_n = n
            if d > 2200:
                records.append((n, d))
    
    return best_n, best_delay, records


def exhaustive_search_decade(start_exp, num_workers=18, 
                             time_limit=600, chunk_size=2_000_000):
    """Exhaustively scan a decade [10^start_exp, 10^(start_exp+1)).
    
    For a(19), we need start_exp=18 but this is 9×10^18 numbers.
    Instead we'll do a systematic sweep covering as much as possible.
    """
    range_start = 10**start_exp
    range_end = 10**(start_exp + 1)
    
    print(f"=== Exhaustive Decade Search: [10^{start_exp}, 10^{start_exp+1}) ===")
    print(f"  Range size: {range_end - range_start:.2e}")
    print(f"  Workers: {num_workers}")
    
    # Build tables in main process first for reference
    lookup = build_lookup_table()
    table = build_shortcut_table(SHORTCUT_K)
    
    # Strategy: systematically scan from the start of the decade
    # We won't cover the whole thing, but we'll cover the beginning
    # and random samples
    
    all_records = []
    best_delay = 0
    best_n = range_start
    total_checked = 0
    t_start = time.perf_counter()
    
    # Phase 1: Systematic scan from start of decade
    print("\nPhase 1: Systematic scan from beginning...")
    current = range_start
    batch = 0
    
    with mp.Pool(num_workers, initializer=_init_worker) as pool:
        while time.perf_counter() - t_start < time_limit * 0.7:
            batch += 1
            chunks = []
            for _ in range(num_workers):
                if current >= range_end:
                    break
                end = min(current + chunk_size, range_end)
                chunks.append((current, end))
                current = end
            
            if not chunks:
                break
            
            results = pool.map(_scan_range_odd, chunks)
            
            for bn, bd, recs in results:
                total_checked += (chunks[0][1] - chunks[0][0]) // 2  # approx odd count
                all_records.extend(recs)
                if bd > best_delay:
                    best_delay = bd
                    best_n = bn
                    print(f"  New local max: n={bn}, delay={bd} "
                          f"(checked {total_checked:,})")
            
            if batch % 5 == 0:
                elapsed = time.perf_counter() - t_start
                coverage = (current - range_start) / (range_end - range_start)
                print(f"  Progress: {coverage*100:.4f}% of decade, "
                      f"{total_checked:,} checked, {elapsed:.0f}s")
        
        # Phase 2: Random sampling of uncovered region
        print("\nPhase 2: Random sampling of remaining space...")
        remaining_time = time_limit - (time.perf_counter() - t_start)
        rng = random.Random(42)
        
        while time.perf_counter() - t_start < time_limit:
            chunks = []
            for _ in range(num_workers):
                cs = rng.randint(current, range_end - chunk_size)
                chunks.append((cs, cs + chunk_size))
            
            results = pool.map(_scan_range_odd, chunks)
            
            for bn, bd, recs in results:
                total_checked += chunk_size // 2
                all_records.extend(recs)
                if bd > best_delay:
                    best_delay = bd
                    best_n = bn
                    print(f"  New best: n={bn}, delay={bd}")
    
    elapsed = time.perf_counter() - t_start
    
    # Deduplicate records
    seen = set()
    unique_records = []
    for n, d in sorted(all_records, key=lambda x: -x[1]):
        if n not in seen:
            seen.add(n)
            unique_records.append({"n": n, "delay": d})
    
    result = {
        "search_type": "exhaustive_decade",
        "decade": start_exp,
        "range": [range_start, range_end],
        "systematic_coverage_to": current,
        "systematic_coverage_fraction": (current - range_start) / (range_end - range_start),
        "total_checked": total_checked,
        "time_seconds": round(elapsed, 1),
        "rate_per_second": round(total_checked / elapsed, 0) if elapsed > 0 else 0,
        "best": {"n": best_n, "delay": best_delay},
        "high_delay_records": unique_records[:200],
        "num_workers": num_workers,
    }
    
    return result


def find_a19_comprehensive(time_budget=1800):
    """Comprehensive search for a(19)."""
    
    print("=" * 60)
    print("COMPREHENSIVE SEARCH FOR OEIS A284668 a(19)")
    print("=" * 60)
    print(f"Time budget: {time_budget}s")
    print(f"Known a(18) = 931386509544713451, delay = 2283")
    print(f"Target: find number below 10^19 with delay > 2283\n")
    
    from baseline import A284668_KNOWN
    
    # Build tables
    lookup = build_lookup_table()
    table = build_shortcut_table(SHORTCUT_K)
    
    all_high = []
    best_delay = 2283
    best_n = 931386509544713451
    
    # Strategy 1: Check known record sequence pattern extrapolation
    print("--- Strategy 1: Extrapolation from known records ---")
    # Known records have a pattern where each is roughly 10x the previous
    # and delay increases by ~100-200 per decade
    # a(18) = 931386509544713451 (18 digits)
    # Expected a(19) should be somewhere in 10^18 to 10^19
    
    # Check numbers near powers of 2 (many records are near powers of 2)
    print("Checking near powers of 2...")
    for bits in range(60, 64):
        base = 1 << bits
        for offset in range(-100000, 100001, 2):
            n = base + offset
            if n < 10**18 or n >= 10**19 or n < 2:
                continue
            d = delay_shortcut(n, table, SHORTCUT_K, lookup)
            if d > 2200:
                all_high.append((n, d))
                if d > best_delay:
                    best_delay = d
                    best_n = n
                    print(f"  NEW BEST: n={n} (2^{bits}+{offset}), delay={d}")
    
    # Check near Mersenne numbers (2^k - 1)
    print("Checking near Mersenne numbers...")
    for bits in range(60, 64):
        base = (1 << bits) - 1
        for offset in range(-100000, 100001, 2):
            n = base + offset
            if n < 10**18 or n >= 10**19 or n < 2:
                continue
            d = delay_shortcut(n, table, SHORTCUT_K, lookup)
            if d > 2200:
                all_high.append((n, d))
                if d > best_delay:
                    best_delay = d
                    best_n = n
                    print(f"  NEW BEST: n={n} (2^{bits}-1+{offset}), delay={d}")
    
    # Strategy 2: Generate candidates with specific binary patterns
    print("\n--- Strategy 2: Binary pattern candidates ---")
    # Known records tend to have high density of 1-bits
    # Generate numbers with ~60-65% 1-bits
    rng = random.Random(42)
    pattern_count = 0
    for _ in range(5_000_000):
        bits = rng.randint(60, 63)
        n = 0
        for b in range(bits):
            if rng.random() < 0.63:  # ~63% 1-bits
                n |= (1 << b)
        n |= (1 << (bits - 1))  # ensure top bit is set
        if n < 10**18 or n >= 10**19:
            continue
        if n % 2 == 0:
            n += 1
        d = delay_shortcut(n, table, SHORTCUT_K, lookup)
        pattern_count += 1
        if d > 2200:
            all_high.append((n, d))
            if d > best_delay:
                best_delay = d
                best_n = n
                print(f"  NEW BEST: n={n}, delay={d} (random pattern)")
    print(f"  Checked {pattern_count} pattern candidates")
    
    # Strategy 3: Systematic scan with parallel workers
    print(f"\n--- Strategy 3: Parallel systematic scan ---")
    decade_result = exhaustive_search_decade(
        18, 
        num_workers=18, 
        time_limit=min(time_budget - 120, 600),
        chunk_size=2_000_000,
    )
    
    for rec in decade_result.get("high_delay_records", []):
        n, d = rec["n"], rec["delay"]
        all_high.append((n, d))
        if d > best_delay:
            best_delay = d
            best_n = n
    
    # Compile results
    seen = set()
    unique_high = []
    for n, d in sorted(all_high, key=lambda x: -x[1]):
        if n not in seen:
            seen.add(n)
            unique_high.append({"n": n, "delay": d, "bits": n.bit_length()})
    
    result = {
        "target": "OEIS A284668 a(19)",
        "known_a18": {"n": 931386509544713451, "delay": 2283},
        "best_found": {
            "n": best_n,
            "delay": best_delay,
            "bits": best_n.bit_length(),
            "is_new_record": best_delay > 2283,
        },
        "high_delay_numbers": unique_high[:500],
        "decade_search": decade_result,
        "strategies_used": [
            "power_of_2_neighborhoods",
            "mersenne_neighborhoods", 
            "random_binary_patterns",
            "systematic_parallel_scan"
        ],
    }
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "full_search_results.json"
    out_path.write_text(json.dumps(result, indent=2, default=str))
    print(f"\n{'='*60}")
    print(f"SEARCH COMPLETE")
    print(f"Best: n={best_n}, delay={best_delay}")
    print(f"New record: {best_delay > 2283}")
    print(f"Results saved to {out_path}")
    
    return result


if __name__ == "__main__":
    find_a19_comprehensive(time_budget=900)  # 15 minutes
