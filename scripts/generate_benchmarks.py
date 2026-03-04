#!/usr/bin/env python3
"""Generate benchmark CSV datasets for SIMD parser evaluation.

Each dataset is designed to stress different aspects of CSV parsing:
- simple_uniform: pure numeric, no quoting (best case for any parser)
- mixed_quoting: 30% quoted fields with embedded commas (tests quote-state tracking)
- embedded_newlines: 10% fields with embedded CR/LF (hardest case for parallel parsing)
- wide_table: 200 columns, variable widths (tests field-extraction throughput)
- utf8_heavy: CJK/emoji content with mixed quoting (tests UTF-8 + structural detection)

Uses deterministic seed (42) for reproducibility.
"""

import json
import os
import random
import sys
import time

SEED = 42
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "benchmarks", "data")

# CJK + emoji characters for utf8_heavy dataset
CJK_CHARS = "".join(chr(c) for c in range(0x4E00, 0x4E00 + 200))
EMOJI_CHARS = "".join(chr(c) for c in [0x1F600, 0x1F601, 0x1F602, 0x1F603, 0x1F604,
                                         0x1F60A, 0x1F60D, 0x1F60E, 0x1F60F,
                                         0x1F618, 0x1F61C, 0x1F62D, 0x1F637,
                                         0x2764, 0x2B50, 0x1F525, 0x1F4A9])


def write_csv_line(f, fields, newline="\r\n"):
    """Write a CSV record, quoting fields that need it."""
    parts = []
    for field in fields:
        s = str(field)
        if '"' in s or ',' in s or '\n' in s or '\r' in s:
            s = '"' + s.replace('"', '""') + '"'
        parts.append(s)
    f.write(",".join(parts) + newline)


def generate_simple_uniform(rng):
    """1M rows, 10 numeric columns, no quoting needed. Target >= 50MB."""
    path = os.path.join(DATA_DIR, "simple_uniform.csv")
    print(f"Generating simple_uniform.csv ...")
    t0 = time.time()
    rows = 1_000_000
    cols = 10
    with open(path, "w", newline="") as f:
        # Header
        f.write(",".join(f"col_{i}" for i in range(cols)) + "\r\n")
        for _ in range(rows):
            values = [str(rng.randint(100000, 9999999)) for _ in range(cols)]
            f.write(",".join(values) + "\r\n")
    size = os.path.getsize(path)
    elapsed = time.time() - t0
    print(f"  -> {size / 1e6:.1f} MB, {rows} rows, {elapsed:.1f}s")
    return {"file": "simple_uniform.csv", "rows": rows, "columns": cols,
            "size_bytes": size, "quoting_pct": 0, "embedded_newlines": False,
            "description": "1M rows x 10 numeric columns, no quoting"}


def generate_mixed_quoting(rng):
    """500K rows, 10 columns, 30% quoted fields with embedded commas."""
    path = os.path.join(DATA_DIR, "mixed_quoting.csv")
    print(f"Generating mixed_quoting.csv ...")
    t0 = time.time()
    rows = 500_000
    cols = 10
    words = ["hello", "world", "data", "test", "value", "sample", "record",
             "field", "column", "entry", "item", "result", "output", "input"]

    with open(path, "w", newline="") as f:
        f.write(",".join(f"col_{i}" for i in range(cols)) + "\r\n")
        for _ in range(rows):
            fields = []
            for _ in range(cols):
                if rng.random() < 0.30:  # 30% quoted with embedded commas
                    w1 = rng.choice(words)
                    w2 = rng.choice(words)
                    w3 = rng.choice(words)
                    field = f"{w1}, {w2} and {w3}"
                    if rng.random() < 0.1:  # some with quotes inside
                        field = f'{w1} said "{w2}", then {w3}'
                    fields.append(field)
                else:
                    fields.append(rng.choice(words) + str(rng.randint(0, 9999)))
            write_csv_line(f, fields)
    size = os.path.getsize(path)
    elapsed = time.time() - t0
    print(f"  -> {size / 1e6:.1f} MB, {rows} rows, {elapsed:.1f}s")
    return {"file": "mixed_quoting.csv", "rows": rows, "columns": cols,
            "size_bytes": size, "quoting_pct": 30, "embedded_newlines": False,
            "description": "500K rows x 10 columns, 30% quoted fields with embedded commas"}


def generate_embedded_newlines(rng):
    """100K rows, 8 columns, 10% fields with embedded CR/LF."""
    path = os.path.join(DATA_DIR, "embedded_newlines.csv")
    print(f"Generating embedded_newlines.csv ...")
    t0 = time.time()
    rows = 100_000
    cols = 8
    sentences = [
        "The quick brown fox\njumps over the lazy dog",
        "First line\r\nSecond line\r\nThird line",
        "Hello\nworld",
        "Multi\nline\nfield\nwith\nseveral\nbreaks",
        "Line one.\r\nLine two.\r\nLine three.",
        "Data with\nnewlines inside",
        "A field\r\nthat spans\r\nmultiple lines",
        "Embedded\nnewline\ncharacters\nare\ntricky",
    ]
    words = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]

    # Need >= 50MB -> make rows contain longer content
    with open(path, "w", newline="") as f:
        f.write(",".join(f"col_{i}" for i in range(cols)) + "\r\n")
        for _ in range(rows):
            fields = []
            for _ in range(cols):
                if rng.random() < 0.10:  # 10% embedded newlines
                    fields.append(rng.choice(sentences) + " " + str(rng.randint(0, 99999)))
                else:
                    # Generate longer content to reach 50MB target
                    parts = [rng.choice(words) + str(rng.randint(0, 9999)) for _ in range(8)]
                    fields.append(" ".join(parts))
            write_csv_line(f, fields)
    size = os.path.getsize(path)
    elapsed = time.time() - t0
    print(f"  -> {size / 1e6:.1f} MB, {rows} rows, {elapsed:.1f}s")
    return {"file": "embedded_newlines.csv", "rows": rows, "columns": cols,
            "size_bytes": size, "quoting_pct": 10, "embedded_newlines": True,
            "description": "100K rows x 8 columns, 10% fields with embedded CR/LF"}


def generate_wide_table(rng):
    """100K rows, 200 columns, variable widths."""
    path = os.path.join(DATA_DIR, "wide_table.csv")
    print(f"Generating wide_table.csv ...")
    t0 = time.time()
    rows = 100_000
    cols = 200

    with open(path, "w", newline="") as f:
        f.write(",".join(f"c{i:03d}" for i in range(cols)) + "\r\n")
        for _ in range(rows):
            fields = []
            for c in range(cols):
                width_class = c % 5
                if width_class == 0:  # short numeric
                    fields.append(str(rng.randint(0, 99)))
                elif width_class == 1:  # medium numeric
                    fields.append(str(rng.randint(10000, 99999)))
                elif width_class == 2:  # short string
                    fields.append("".join(rng.choices("abcdefghij", k=rng.randint(3, 8))))
                elif width_class == 3:  # medium string
                    fields.append("".join(rng.choices("abcdefghijklmnopqrstuvwxyz", k=rng.randint(10, 30))))
                else:  # long string, sometimes quoted
                    s = "".join(rng.choices("abcdefghijklmnopqrstuvwxyz0123456789 ", k=rng.randint(20, 60)))
                    if rng.random() < 0.05:
                        s = s + ", extra"
                    fields.append(s)
            write_csv_line(f, fields)
    size = os.path.getsize(path)
    elapsed = time.time() - t0
    print(f"  -> {size / 1e6:.1f} MB, {rows} rows, {elapsed:.1f}s")
    return {"file": "wide_table.csv", "rows": rows, "columns": cols,
            "size_bytes": size, "quoting_pct": 1, "embedded_newlines": False,
            "description": "100K rows x 200 columns, variable field widths"}


def generate_utf8_heavy(rng):
    """500K rows, 8 columns, CJK/emoji content with mixed quoting."""
    path = os.path.join(DATA_DIR, "utf8_heavy.csv")
    print(f"Generating utf8_heavy.csv ...")
    t0 = time.time()
    rows = 500_000
    cols = 8

    with open(path, "w", newline="") as f:
        f.write(",".join(f"col_{i}" for i in range(cols)) + "\r\n")
        for _ in range(rows):
            fields = []
            for _ in range(cols):
                content_type = rng.random()
                if content_type < 0.3:  # CJK content
                    chars = [rng.choice(CJK_CHARS) for _ in range(rng.randint(5, 20))]
                    s = "".join(chars)
                elif content_type < 0.5:  # emoji content
                    emojis = [rng.choice(EMOJI_CHARS) for _ in range(rng.randint(2, 6))]
                    s = " ".join(emojis) + " text" + str(rng.randint(0, 999))
                elif content_type < 0.7:  # mixed CJK + ASCII
                    cjk = "".join(rng.choice(CJK_CHARS) for _ in range(5))
                    s = f"name_{rng.randint(0,999)} {cjk}"
                else:  # ASCII with occasional quoting
                    s = "word" + str(rng.randint(0, 99999))
                    if rng.random() < 0.15:
                        s = f"{s}, extra, data"
                fields.append(s)
            write_csv_line(f, fields)
    size = os.path.getsize(path)
    elapsed = time.time() - t0
    print(f"  -> {size / 1e6:.1f} MB, {rows} rows, {elapsed:.1f}s")
    return {"file": "utf8_heavy.csv", "rows": rows, "columns": cols,
            "size_bytes": size, "quoting_pct": 15, "embedded_newlines": False,
            "description": "500K rows x 8 columns, CJK/emoji content with mixed quoting"}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    rng = random.Random(SEED)

    manifests = []
    manifests.append(generate_simple_uniform(rng))
    manifests.append(generate_mixed_quoting(rng))
    manifests.append(generate_embedded_newlines(rng))
    manifests.append(generate_wide_table(rng))
    manifests.append(generate_utf8_heavy(rng))

    manifest = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed": SEED,
        "datasets": manifests,
        "total_size_bytes": sum(m["size_bytes"] for m in manifests),
        "total_rows": sum(m["rows"] for m in manifests),
    }

    manifest_path = os.path.join(DATA_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest written to {manifest_path}")
    print(f"Total: {manifest['total_size_bytes'] / 1e6:.1f} MB across {len(manifests)} datasets")


if __name__ == "__main__":
    main()
