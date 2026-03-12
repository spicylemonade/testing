#!/usr/bin/env python3
"""Small helper for disciplined research_rubric.json maintenance."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


RUBRIC_PATH = Path(__file__).resolve().parent.parent / "research_rubric.json"
VALID_STATUSES = {"pending", "in_progress", "completed", "failed"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_rubric() -> dict:
    return json.loads(RUBRIC_PATH.read_text())


def save_rubric(payload: dict) -> None:
    summary = status_summary(payload)
    payload["summary"] = {
        "total_items": sum(summary.values()),
        "completed": summary["completed"],
        "in_progress": summary["in_progress"],
        "failed": summary["failed"],
        "pending": summary["pending"],
    }
    payload["updated_at"] = now()
    RUBRIC_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def find_item(payload: dict, item_id: str) -> dict:
    for phase in payload.get("phases", []):
        for item in phase.get("items", []):
            if item.get("id") == item_id:
                return item
    raise SystemExit(f"unknown rubric item: {item_id}")


def status_summary(payload: dict) -> dict[str, int]:
    counts = {key: 0 for key in VALID_STATUSES}
    for phase in payload.get("phases", []):
        for item in phase.get("items", []):
            status = item.get("status")
            if status in counts:
                counts[status] += 1
    return counts


def cmd_set(args: argparse.Namespace) -> int:
    if args.status not in VALID_STATUSES:
        raise SystemExit(f"invalid status: {args.status}")
    payload = load_rubric()
    item = find_item(payload, args.item_id)
    item["status"] = args.status
    if args.notes is not None:
        item["notes"] = args.notes
    if args.error is not None:
        item["error"] = args.error
    elif args.status != "failed":
        item["error"] = None
    save_rubric(payload)
    summary = status_summary(payload)
    print(
        json.dumps(
            {
                "item_id": args.item_id,
                "status": item["status"],
                "summary": summary,
            },
            indent=2,
        )
    )
    return 0


def cmd_summary(_: argparse.Namespace) -> int:
    payload = load_rubric()
    print(json.dumps(status_summary(payload), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    set_p = sub.add_parser("set", help="set item status/notes/error")
    set_p.add_argument("item_id")
    set_p.add_argument("status")
    set_p.add_argument("--notes")
    set_p.add_argument("--error")
    set_p.set_defaults(func=cmd_set)

    summary_p = sub.add_parser("summary", help="print rubric status counts")
    summary_p.set_defaults(func=cmd_summary)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
