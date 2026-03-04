#!/usr/bin/env python3
"""Parallel delay record search engine for OEIS A284668.

Uses the k-step shortcut engine with multiprocessing to search for the
number below 10^19 with the highest Collatz total stopping time.

Strategy:
1. Build shortcut table (k=16) and lookup table (2^20)
2. Partition range [1, 10^19) into chunks 
3. Use multiprocessing to scan chunks in parallel
4. Each worker tracks local max delay and returns it
5. Merge results to find global maximum

Key optimization: we already know a(18) = 931386509544713451 with delay 2283.
So we only need to find numbers with delay > 2283 (or find that no such number
exists below 10^19, in which case a(19) = a(18)).

Wait - a(19) is the number below 10^19 with highest delay. Since a(18) < 10^18 < 10^19,
a(19) >= a(18) in delay. But a(19) could be a(18) itself if no number in 
[10^18, 10^19) has delay > 2283.

Actually, a(n) is defined as the number below 10^n with the LARGEST stopping time.
So a(19) = the number below 10^19 with the largest stopping time. This includes
all numbers below 10^18 too. So a(19) is at least as good as a(18).

To find a(19), we need to:
1. Scan all numbers in [1, 10^19) - but we can skip [1, 10^18) since we know
   the best there is a(18) with delay 2283.
2. Find any number in [10^18, 10^19) with delay > 2283.
3. If found, a(19) = that number. If not, a(19) = a(18).

The search space is 9 * 10^18 numbers. At 274K/s single-core, that's
9e18 / 274000 = 3.28e13 seconds per core. Way too slow for brute force!

We need the sieve to eliminate most candidates.
"""

import json
import time
import random
import multiprocessing as mp
from pathlib import Path
from functools import partial

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "experiments"

LOOKUP_BITS = 20
LOOKUP_LIMIT = 1 << LOOKUP_BITS
SHORTCUT_K = 16


def build_lookup_table():
    """Build delay lookup table."""
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


def build_shortcut_table(k: int):
    """Build shortcut table for k-step lookahead."""
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
    """Compute delay using k-step shortcut + small lookup."""
    x = n
    steps = 0
    while x >= LOOKUP_LIMIT:
        r = int(x) & ((1 << k) - 1)
        a, b, s = table[r]
        x = a * (x >> k) + b
        steps += s
    return steps + lookup[x]


# ---- Sieve: identify residue classes with guaranteed short delays ----

def build_sieve_table(sieve_bits: int, shortcut_table, k, lookup, threshold: int):
    """For each residue r mod 2^sieve_bits, compute delay of r.
    
    If delay(r) < threshold, then for any n ≡ r (mod 2^sieve_bits),
    the trajectory will follow the same initial pattern and likely
    have similar delay. But this isn't quite right for arbitrary n.
    
    Better approach: for each residue class, compute the delay of just
    the residue value itself. Classes where even the residue has high
    delay are more likely to contain record-holders.
    
    Actually, the correct sieve approach for Collatz is:
    For residue r mod 2^sieve_bits, simulate sieve_bits steps.
    If the result is < r (trajectory decreased), this residue class
    will likely converge quickly. If result > r, it might take longer.
    
    For our purposes, we just compute delay of each residue and keep
    those with delay > some fraction of the threshold.
    """
    sieve = []
    mod = 1 << sieve_bits
    for r in range(mod):
        if r < 2:
            sieve.append(False)
            continue
        d = delay_shortcut(r, shortcut_table, k, lookup)
        # Keep residues whose delay is at least threshold * (sieve_bits / 64)
        # This is a rough heuristic
        sieve.append(d >= threshold * sieve_bits / 64)
    return sieve


# ---- Worker function for parallel search ----

def _init_worker():
    """Initialize worker process with lookup and shortcut tables."""
    global _w_lookup, _w_table, _w_k
    _w_lookup = build_lookup_table()
    _w_table = build_shortcut_table(SHORTCUT_K)
    _w_k = SHORTCUT_K


def _scan_chunk(args):
    """Scan a range of numbers and return the one with highest delay."""
    start, end, threshold = args
    global _w_lookup, _w_table, _w_k
    
    best_delay = 0
    best_n = start
    
    for n in range(start, end):
        d = delay_shortcut(n, _w_table, _w_k, _w_lookup)
        if d > best_delay:
            best_delay = d
            best_n = n
    
    # Only return results exceeding threshold
    if best_delay > threshold:
        return (best_n, best_delay)
    return (best_n, best_delay)


def _scan_chunk_with_sieve(args):
    """Scan with odd-only filter and basic optimizations."""
    start, end, threshold = args
    global _w_lookup, _w_table, _w_k
    
    best_delay = 0
    best_n = start
    count = 0
    
    # Only check odd numbers (even numbers have delay = 1 + delay(n/2))
    s = start if start & 1 else start + 1
    
    for n in range(s, end, 2):
        d = delay_shortcut(n, _w_table, _w_k, _w_lookup)
        count += 1
        if d > best_delay:
            best_delay = d
            best_n = n
    
    return (best_n, best_delay, count)


def search_a284668_19(num_workers=None, time_limit_seconds=3600, 
                      chunk_size=1_000_000, sample_strategy="random"):
    """Search for a(19) of OEIS A284668.
    
    Since brute-force scanning 9*10^18 numbers is infeasible,
    we use a sampling strategy: randomly sample chunks of numbers
    in [10^18, 10^19) and check for high delays.
    
    The known record to beat is a(18) = 931386509544713451 with delay 2283.
    
    Strategy: Use the known pattern that delay records tend to have
    specific binary structure. Search randomly but with bias toward
    numbers with binary patterns similar to known records.
    """
    if num_workers is None:
        num_workers = min(mp.cpu_count(), 20)
    
    print(f"=== A284668 a(19) Search ===")
    print(f"  Workers: {num_workers}")
    print(f"  Time limit: {time_limit_seconds}s")
    print(f"  Target: beat delay 2283 (a(18))")
    print(f"  Search range: [10^18, 10^19)\n")
    
    # Phase 1: Build tables (in main process for timing)
    print("Building tables...")
    t0 = time.perf_counter()
    lookup = build_lookup_table()
    table = build_shortcut_table(SHORTCUT_K)
    print(f"  Tables built in {time.perf_counter() - t0:.2f}s")
    
    # Phase 2: Quick scan of known record neighborhoods
    print("\nPhase 1: Scanning neighborhoods of known records...")
    from baseline import A284668_KNOWN
    
    neighborhood_records = []
    for idx in range(15, 19):
        n_rec, d_rec = A284668_KNOWN[idx]
        # Scan ±50000 around each record
        for offset in range(-50000, 50001):
            n = n_rec + offset
            if n < 2:
                continue
            d = delay_shortcut(n, table, SHORTCUT_K, lookup)
            if d > 2200:
                neighborhood_records.append((n, d))
    
    neighborhood_records.sort(key=lambda x: -x[1])
    print(f"  Found {len(neighborhood_records)} numbers with delay > 2200 near known records")
    if neighborhood_records:
        print(f"  Best: n={neighborhood_records[0][0]}, delay={neighborhood_records[0][1]}")
    
    # Phase 3: Random sampling search with parallel workers
    print(f"\nPhase 2: Random chunk sampling with {num_workers} workers...")
    
    range_start = 10**18
    range_end = 10**19
    current_best_delay = 2283  # a(18) delay
    current_best_n = 931386509544713451
    
    all_high_delay = list(neighborhood_records)
    
    start_time = time.perf_counter()
    total_checked = 0
    batch_num = 0
    
    rng = random.Random(42)
    
    with mp.Pool(num_workers, initializer=_init_worker) as pool:
        while time.perf_counter() - start_time < time_limit_seconds:
            batch_num += 1
            
            # Generate random chunk starts
            chunks = []
            for _ in range(num_workers * 2):
                # Random start point in [10^18, 10^19 - chunk_size)
                cs = rng.randint(range_start, range_end - chunk_size)
                chunks.append((cs, cs + chunk_size, current_best_delay - 100))
            
            # Also add some structured searches: 
            # numbers of form 2^k - 1 (Mersenne-like) tend to have high delays
            for bits in range(60, 64):
                base = (1 << bits) - 1
                cs = max(range_start, base - chunk_size // 2)
                if cs < range_end - chunk_size:
                    chunks.append((cs, cs + chunk_size, current_best_delay - 100))
            
            results = pool.map(_scan_chunk_with_sieve, chunks)
            
            for best_n, best_delay, count in results:
                total_checked += count
                if best_delay > current_best_delay:
                    current_best_delay = best_delay
                    current_best_n = best_n
                    print(f"  NEW RECORD! n={best_n}, delay={best_delay} "
                          f"(batch {batch_num}, {total_checked:,} checked)")
                if best_delay > 2200:
                    all_high_delay.append((best_n, best_delay))
            
            elapsed = time.perf_counter() - start_time
            rate = total_checked / elapsed if elapsed > 0 else 0
            if batch_num % 10 == 0:
                print(f"  Batch {batch_num}: {total_checked:,} checked, "
                      f"{rate:,.0f}/s, best delay={current_best_delay}, "
                      f"elapsed={elapsed:.0f}s")
    
    elapsed = time.perf_counter() - start_time
    
    # Deduplicate and sort high-delay records
    seen = set()
    unique_records = []
    for n, d in sorted(all_high_delay, key=lambda x: -x[1]):
        if n not in seen:
            seen.add(n)
            unique_records.append({"n": n, "delay": d})
    
    result = {
        "target": "a(19) of OEIS A284668",
        "search_range": [range_start, range_end],
        "time_seconds": round(elapsed, 1),
        "total_numbers_checked": total_checked,
        "rate_per_second": round(total_checked / elapsed, 0) if elapsed > 0 else 0,
        "num_workers": num_workers,
        "shortcut_k": SHORTCUT_K,
        "chunk_size": chunk_size,
        "current_best": {
            "n": current_best_n,
            "delay": current_best_delay,
            "is_new_record": current_best_delay > 2283,
        },
        "high_delay_numbers": unique_records[:100],
        "known_a18": {"n": 931386509544713451, "delay": 2283},
    }
    
    return result


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run search with time limit
    result = search_a284668_19(
        num_workers=18,  # Leave 2 cores for OS
        time_limit_seconds=300,  # 5 minutes for initial run
        chunk_size=500_000,
    )
    
    print(f"\n=== Search Complete ===")
    print(f"Total checked: {result['total_numbers_checked']:,}")
    print(f"Rate: {result['rate_per_second']:,.0f}/s")
    print(f"Best found: n={result['current_best']['n']}, "
          f"delay={result['current_best']['delay']}")
    print(f"Is new record: {result['current_best']['is_new_record']}")
    
    out_path = RESULTS_DIR / "delay_records.json"
    out_path.write_text(json.dumps(result, indent=2, default=str))
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
