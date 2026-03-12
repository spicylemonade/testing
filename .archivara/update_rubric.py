#!/usr/bin/env python3
"""Small helper to update Archivara rubric item state reproducibly."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("item_id")
    parser.add_argument("status")
    parser.add_argument("--notes")
    parser.add_argument("--error")
    parser.add_argument(
        "--path",
        default="research_rubric.json",
        help="Path to the rubric JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    data: dict[str, Any] = json.loads(path.read_text())
    found = False
    for phase in data.get("phases", []):
        for item in phase.get("items", []):
            if item.get("id") == args.item_id:
                item["status"] = args.status
                item["notes"] = args.notes
                item["error"] = args.error
                found = True
                break
        if found:
            break
    if not found:
        raise SystemExit(f"item not found: {args.item_id}")

    data["updated_at"] = utc_now()
    path.write_text(json.dumps(data, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
