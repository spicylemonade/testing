#!/usr/bin/env python3
"""k-step shortcut engine for Collatz computation.

Correct formulation: We process k bits of the binary representation of n.
For each residue r = n mod 2^k, we know the exact parity sequence of the 
next operations. After processing these k decisions, n transforms via:
    n' = (3^odd_count * n + C_r) / 2^k
where odd_count and C_r depend only on r.

This is Crandall/Barina style: the key is that among the k parity bits
of n, some are 1 (odd -> multiply by 3, add 1) and some are 0 (even -> divide by 2).
We always divide by 2 exactly k times total, but the multiply-by-3 happens
for each odd step.
"""

import json
import time
import random
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "experiments"

LOOKUP_BITS = 20
LOOKUP_LIMIT = 1 << LOOKUP_BITS


def build_lookup_table():
    """Build delay lookup table for n < 2^LOOKUP_BITS."""
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
    """Build shortcut table for k-step lookahead.
    
    For the Syracuse/Collatz iteration using the compressed map:
        T(n) = (3n+1)/2 if n odd, n/2 if n even
    
    We process exactly k of these steps. The parity at each step
    is determined by the current value, not just the initial residue.
    
    But the standard trick works differently: we look at the k LOWEST
    bits of n. These k bits determine the parity of the first k 
    division-by-2 operations. Between divisions we may multiply by 3.
    
    Standard formulation (as in Barina): process n in the "3n+1" form:
        if n odd: n -> 3n+1 (always even after)
        if n even: n -> n/2
    
    The number of times we divide by 2 among k "raw" steps is k - odd_count.
    But this isn't quite right either.
    
    Let me use the simplest correct formulation:
    Simulate k COMBINED steps (T(n) = (3n+1)/2 if odd, n/2 if even) starting
    from n. Use two probe values to extract linear coefficients.
    
    The catch: after k combined steps, the result IS determined linearly by n,
    BUT only if the parity sequence of those k steps is the same. And the
    parity sequence depends on intermediate values, not just n mod 2^k.
    
    Solution: use a DIFFERENT decomposition. Process k EVEN-steps specifically.
    That is, we count only the /2 operations, and between them we do all the
    3n+1 operations. After consuming k bits of n (= k right-shifts), the result
    is 3^(odd_count) * (n >> k) + C_r where C_r depends on r = n & ((1<<k)-1).
    
    This is the Sieve approach: we iterate until we've shifted out k bits.
    """
    table = []
    twok = 1 << k
    
    for r in range(twok):
        # Process k bits: iterate until k right-shifts have been done
        x = r if r > 0 else twok  # avoid 0
        mult = twok  # track what the "high bits" above k are multiplied by
        # We're computing: starting with full n, after processing low k bits,
        # result = mult * (n >> k) + x_residual
        # Initially: n = (n >> k) * 2^k + r, so x = r, mult = 2^k
        
        shifts_done = 0
        steps = 0
        x_val = r if r > 0 else twok
        
        # Track symbolically: value = alpha * n_high + beta
        # where n_high = n >> k, initially value = n_high * 2^k + r
        alpha = twok  # coefficient of n_high
        beta = r if r > 0 else twok  # constant term
        
        while shifts_done < k:
            if beta & 1:  # odd (depends on beta parity = current value parity for same residue)
                # Actually this is wrong: the parity depends on the full value,
                # not just beta. alpha * n_high + beta is odd iff (alpha * n_high + beta) is odd.
                # If alpha is even (it starts as 2^k which is even), then parity = parity of beta.
                # After a 3x+1 step: alpha' = 3*alpha, beta' = 3*beta + 1 (alpha' is even*3 = even if alpha even)
                # Hmm, 3 * (even) = even. So alpha stays even? Let's check:
                # Start: alpha = 2^k (even). After odd step: alpha = 3 * 2^k (even).
                # After even step: alpha = 3 * 2^k / 2 = 3 * 2^(k-1) (even if k>1).
                # After another even step: alpha = 3 * 2^(k-2)... eventually alpha could become odd.
                # 
                # Actually the standard trick is: the PARITY of the full value
                # alpha * n_high + beta depends on n_high, which we don't know!
                # So this symbolic approach only works if alpha is even,
                # meaning parity = parity(beta).
                # alpha starts even (2^k) and:
                #   odd step: alpha -> 3*alpha (still even if alpha even)
                #   even step (shift): alpha -> alpha/2 
                # After k shifts, alpha = (3^odd_count * 2^k) / 2^k = 3^odd_count
                # So alpha loses one factor of 2 per shift. It stays even as long as 
                # shifts_done < k. Which is exactly our loop condition!
                # 
                # So: while shifts_done < k, alpha has at least one factor of 2,
                # meaning parity of (alpha * n_high + beta) = parity of beta. 
                
                alpha = 3 * alpha
                beta = 3 * beta + 1
                steps += 1  # 3n+1 step
                # Now alpha*n_high + beta is always even (since 3n+1 makes it even)
                # So we immediately shift
                alpha >>= 1
                beta >>= 1
                shifts_done += 1
                steps += 1  # /2 step
            else:
                alpha >>= 1
                beta >>= 1
                shifts_done += 1
                steps += 1
        
        # Now: value = alpha * n_high + beta = (3^odd_count) * (n >> k) + beta
        # Correct the beta for the r=0 case
        if r == 0:
            # We used twok instead of 0, so beta is off by the transformation of twok
            # Let's just recompute for r=0 specially
            a0 = alpha  # same as other residues
            # For r=0, the low k bits are all 0, so all k steps are even
            # alpha = 2^k / 2^k = 1, beta = 0
            # Actually no, let's just redo it:
            pass
        
        table.append((alpha, beta, steps))
    
    # Fix r=0: simulate directly
    alpha_0 = 1  # all even steps: 2^k / 2^k = 1
    beta_0 = 0
    steps_0 = k  # k even steps
    table[0] = (alpha_0, beta_0, steps_0)
    
    return table


def delay_shortcut(n: int, table: list, k: int, lookup: list) -> int:
    """Compute delay using k-step shortcut + small lookup."""
    x = n
    steps = 0
    mask = (1 << k) - 1
    
    while x >= LOOKUP_LIMIT:
        r = int(x & mask)
        a, b, s = table[r]
        x = a * x + b  # This is wrong! Should be a * (x >> k) + b
        steps += s
    
    return steps + lookup[x]


def delay_shortcut_v2(n: int, table: list, k: int, lookup: list) -> int:
    """Correct version: result = a * (n >> k) + b after processing k low bits."""
    x = n
    steps = 0
    
    while x >= LOOKUP_LIMIT:
        r = int(x) & ((1 << k) - 1)
        a, b, s = table[r]
        x = a * (x >> k) + b
        steps += s
    
    return steps + lookup[x]


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=== Shortcut Engine Benchmark ===\n")
    
    print(f"Building lookup table (2^{LOOKUP_BITS})...")
    t0 = time.perf_counter()
    lookup = build_lookup_table()
    print(f"  Done in {time.perf_counter() - t0:.3f}s")
    
    from baseline import A284668_KNOWN
    
    results = {}
    
    for k in [4, 8, 12, 16]:
        entries = 1 << k
        print(f"\n--- k={k} ({entries} entries) ---")
        t0 = time.perf_counter()
        table = build_shortcut_table(k)
        build_time = time.perf_counter() - t0
        print(f"  Table built in {build_time:.4f}s")
        
        # Verify against known A284668 records
        errors = 0
        for idx in range(1, 19):
            n, expected = A284668_KNOWN[idx]
            actual = delay_shortcut_v2(n, table, k, lookup)
            if actual != expected:
                errors += 1
                if errors <= 3:
                    print(f"  MISMATCH a({idx}): n={n}, expected={expected}, got={actual}")
        
        # Also verify small random numbers
        rng = random.Random(42)
        from baseline import delay_time as naive_delay
        small_errors = 0
        for _ in range(1000):
            n = rng.randint(2, 10**6)
            fast = delay_shortcut_v2(n, table, k, lookup)
            ref = naive_delay(n)
            if fast != ref:
                small_errors += 1
        
        total_errors = errors + small_errors
        print(f"  A284668: {18 - errors}/18 OK, Small random: {1000 - small_errors}/1000 OK")
        
        if total_errors == 0:
            # Benchmark: scan chunk at 10^18
            start = 10**18
            chunk = 100000
            t0 = time.perf_counter()
            max_d = 0
            max_n = start
            for n in range(start, start + chunk):
                d = delay_shortcut_v2(n, table, k, lookup)
                if d > max_d:
                    max_d = d
                    max_n = n
            scan_time = time.perf_counter() - t0
            nps = chunk / scan_time
            
            print(f"  100K scan at 10^18: {scan_time:.3f}s = {nps:.0f}/s")
            print(f"  Max delay in chunk: {max_d} at n={max_n}")
            
            results[f"k={k}"] = {
                "k": k,
                "table_entries": entries,
                "build_time_seconds": round(build_time, 4),
                "total_errors": total_errors,
                "scan_100k_time": round(scan_time, 3),
                "numbers_per_second": round(nps, 0),
                "max_delay_in_chunk": max_d,
                "max_n_in_chunk": max_n,
            }
        else:
            results[f"k={k}"] = {"k": k, "total_errors": total_errors, "status": "FAILED"}
    
    out_path = RESULTS_DIR / "shortcut_engine_benchmark.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
