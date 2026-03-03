#!/usr/bin/env python3
"""Update research rubric item status and summary counts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def update_item(rubric_path: Path, item_id: str, status: str, notes: str | None, error: str | None) -> None:
    payload = json.loads(rubric_path.read_text())

    item_found = None
    for phase in payload.get("phases", []):
        for item in phase.get("items", []):
            if item.get("id") == item_id:
                item["status"] = status
                item["notes"] = notes
                item["error"] = error
                item_found = item
                break
        if item_found is not None:
            break

    if item_found is None:
        raise SystemExit(f"Item id not found: {item_id}")

    counts: Counter[str] = Counter()
    total = 0
    for phase in payload.get("phases", []):
        for item in phase.get("items", []):
            total += 1
            counts[item.get("status", "pending")] += 1

    payload["summary"] = {
        "total_items": total,
        "completed": counts.get("completed", 0),
        "in_progress": counts.get("in_progress", 0),
        "failed": counts.get("failed", 0),
        "pending": counts.get("pending", 0),
    }
    payload["updated_at"] = now_iso()

    rubric_path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a rubric item status")
    parser.add_argument("item_id")
    parser.add_argument("status", choices=["pending", "in_progress", "completed", "failed"])
    parser.add_argument("--notes", default=None)
    parser.add_argument("--error", default=None)
    parser.add_argument("--rubric", default="research_rubric.json")
    args = parser.parse_args()

    update_item(
        rubric_path=Path(args.rubric),
        item_id=args.item_id,
        status=args.status,
        notes=args.notes,
        error=args.error,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
