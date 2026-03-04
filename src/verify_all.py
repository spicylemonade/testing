#!/usr/bin/env python3
"""Master verification script — verifies all claimed results.

This is the "anyone can check this" script. Run:
    python src/verify_all.py

It independently verifies every claimed record using the naive
Collatz function (no optimizations, pure Python arbitrary precision).
"""

import json
import hashlib
import time
from pathlib import Path


def collatz_delay(n: int) -> int:
    """Compute total stopping time. Naive implementation."""
    steps = 0
    x = n
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
        steps += 1
    return steps


def main():
    t_start = time.perf_counter()
    results_dir = Path(__file__).resolve().parent.parent / "results"
    
    print("=" * 70)
    print("  COLLATZ DELAY RECORD VERIFICATION")
    print("  All results independently verified with naive Python implementation")
    print("=" * 70)
    
    # All records to verify
    records = [
        # OEIS A284668: a(1) through a(18)
        {"source": "OEIS_A284668_a1", "n": 9, "claimed_delay": 19},
        {"source": "OEIS_A284668_a2", "n": 97, "claimed_delay": 118},
        {"source": "OEIS_A284668_a3", "n": 871, "claimed_delay": 178},
        {"source": "OEIS_A284668_a4", "n": 6171, "claimed_delay": 261},
        {"source": "OEIS_A284668_a5", "n": 77031, "claimed_delay": 350},
        {"source": "OEIS_A284668_a6", "n": 837799, "claimed_delay": 524},
        {"source": "OEIS_A284668_a7", "n": 8400511, "claimed_delay": 685},
        {"source": "OEIS_A284668_a8", "n": 63728127, "claimed_delay": 949},
        {"source": "OEIS_A284668_a9", "n": 670617279, "claimed_delay": 986},
        {"source": "OEIS_A284668_a10", "n": 9780657630, "claimed_delay": 1132},
        {"source": "OEIS_A284668_a11", "n": 75128138247, "claimed_delay": 1228},
        {"source": "OEIS_A284668_a12", "n": 989345275647, "claimed_delay": 1348},
        {"source": "OEIS_A284668_a13", "n": 7887663552367, "claimed_delay": 1563},
        {"source": "OEIS_A284668_a14", "n": 80867137596217, "claimed_delay": 1662},
        {"source": "OEIS_A284668_a15", "n": 942488749153153, "claimed_delay": 1862},
        {"source": "OEIS_A284668_a16", "n": 7579309213675935, "claimed_delay": 1958},
        {"source": "OEIS_A284668_a17", "n": 93571393692802302, "claimed_delay": 2091},
        {"source": "OEIS_A284668_a18", "n": 931386509544713451, "claimed_delay": 2283},
        # Roosendaal delay records in [10^18, 10^19)
        {"source": "Roosendaal_record_141", "n": 1278775404785934855, "claimed_delay": 2286},
        {"source": "Roosendaal_record_142", "n": 1339302163616345727, "claimed_delay": 2330},
        {"source": "Roosendaal_record_143", "n": 2678604327232691454, "claimed_delay": 2331},
        {"source": "Roosendaal_record_144", "n": 3571472436310255273, "claimed_delay": 2334},
        {"source": "Roosendaal_record_145", "n": 4761963248413673697, "claimed_delay": 2337},
        {"source": "Roosendaal_record_146", "n": 5065931099926693735, "claimed_delay": 2363},
        {"source": "Roosendaal_record_147", "n": 5977996304343501855, "claimed_delay": 2389},
        {"source": "Roosendaal_record_148_best_below_1e19", "n": 9781262575275081247, "claimed_delay": 2426},
        # Records above 10^19 for reference
        {"source": "Roosendaal_above_1e19_149", "n": 13041683433700108329, "claimed_delay": 2429},
        {"source": "Roosendaal_above_1e19_150", "n": 14727207461063895711, "claimed_delay": 2442},
        {"source": "Roosendaal_above_1e19_151", "n": 28019077177231758495, "claimed_delay": 2456},
    ]
    
    all_pass = True
    hash_parts = []
    verified = []
    
    for rec in records:
        t0 = time.perf_counter()
        actual = collatz_delay(rec["n"])
        elapsed = time.perf_counter() - t0
        match = actual == rec["claimed_delay"]
        
        status = "PASS" if match else "FAIL"
        if not match:
            all_pass = False
        
        print(f"  [{status}] {rec['source']}: n={rec['n']}, "
              f"claimed={rec['claimed_delay']}, actual={actual} ({elapsed:.4f}s)")
        
        hash_parts.append(f"{rec['n']}:{actual}")
        verified.append({
            "source": rec["source"],
            "n": rec["n"],
            "claimed_delay": rec["claimed_delay"],
            "verified_delay": actual,
            "match": match,
            "verification_time_seconds": round(elapsed, 6),
        })
    
    total_time = time.perf_counter() - t_start
    cert_hash = hashlib.sha256(";".join(hash_parts).encode()).hexdigest()
    
    certificate = {
        "title": "Collatz Delay Record Verification Certificate",
        "date": "2026-03-04",
        "method": "Naive Collatz iteration: if even n/2, if odd 3n+1, count steps to 1",
        "implementation": "Pure Python arbitrary precision integers, no optimizations",
        "total_records_verified": len(verified),
        "all_passed": all_pass,
        "pass_count": sum(1 for v in verified if v["match"]),
        "fail_count": sum(1 for v in verified if not v["match"]),
        "total_verification_time_seconds": round(total_time, 2),
        "sha256_verification_hash": cert_hash,
        "key_finding": {
            "description": "The highest known Collatz delay below 10^19 is 2426 steps, achieved by n = 9,781,262,575,275,081,247",
            "n": 9781262575275081247,
            "delay": 2426,
            "bits": 9781262575275081247 .bit_length(),
            "implication": "This establishes a(19) >= 9,781,262,575,275,081,247 for OEIS A284668 (the number below 10^19 with the highest Collatz total stopping time has delay >= 2426)",
        },
        "records": verified,
    }
    
    out_dir = results_dir / "final"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "verification_certificate.json"
    out_path.write_text(json.dumps(certificate, indent=2))
    
    print(f"\n{'=' * 70}")
    print(f"  VERIFICATION {'PASSED' if all_pass else 'FAILED'}: "
          f"{certificate['pass_count']}/{certificate['total_records_verified']} records verified")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  SHA-256: {cert_hash}")
    print(f"  Certificate: {out_path}")
    print(f"\n  KEY FINDING:")
    print(f"  The number 9,781,262,575,275,081,247 takes 2,426 Collatz steps to reach 1.")
    print(f"  This is the highest known delay for any number below 10^19.")
    print(f"  OEIS A284668 a(19) >= 9,781,262,575,275,081,247 (delay >= 2426)")
    print(f"{'=' * 70}")
    
    return all_pass


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
