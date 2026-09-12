#!/usr/bin/env python3
"""Fill missing image-extracted vocabulary fields from repository CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


HEADERS = ("từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ")


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


def load_input(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and set(payload) == {"rows"}:
        payload = payload["rows"]
    if not isinstance(payload, list) or not payload:
        raise ValueError("Input must be a non-empty JSON array or an object containing only 'rows'")

    rows: list[dict[str, str]] = []
    for number, item in enumerate(payload, start=1):
        if isinstance(item, str):
            row = {header: "" for header in HEADERS}
            row["từ mới"] = normalize(item)
        elif isinstance(item, dict):
            extra = set(item) - set(HEADERS)
            if extra:
                raise ValueError(f"Input row {number} has extra columns: {', '.join(sorted(extra))}")
            row = {header: "" for header in HEADERS}
            for header, value in item.items():
                if not isinstance(value, str):
                    raise ValueError(f"Input row {number}, column {header!r} must be a string")
                row[header] = normalize(value)
        else:
            raise ValueError(f"Input row {number} must be a kanji string or object")
        if not row["từ mới"]:
            raise ValueError(f"Input row {number} has no 'từ mới'")
        rows.append(row)
    return rows


def build_index(resources: Path) -> dict[str, list[tuple[dict[str, str], Path, int]]]:
    index: dict[str, list[tuple[dict[str, str], Path, int]]] = defaultdict(list)
    paths = sorted(resources.glob("**/goi/*.csv"))
    if not paths:
        raise ValueError(f"No vocabulary CSV found under {resources}")
    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != HEADERS:
                raise ValueError(f"Invalid header in {path}: {reader.fieldnames!r}")
            for line, raw in enumerate(reader, start=2):
                row = {header: normalize(raw[header]) for header in HEADERS}
                index[row["từ mới"]].append((row, path, line))
    return index


def enrich(
    rows: list[dict[str, str]],
    index: dict[str, list[tuple[dict[str, str], Path, int]]],
) -> tuple[list[dict[str, str]], list[str]]:
    issues: list[str] = []
    for number, row in enumerate(rows, start=1):
        matches = index.get(row["từ mới"], [])
        if not matches:
            issues.append(f"row {number} {row['từ mới']!r}: not found in resources")
            continue
        sources = ", ".join(f"{path}:{line}" for _, path, line in matches)
        for header in HEADERS[1:]:
            if row[header]:
                continue
            values = {match[header] for match, _, _ in matches if match[header]}
            if len(values) == 1:
                row[header] = values.pop()
            elif not values:
                issues.append(f"row {number} {row['từ mới']!r}, {header!r}: empty in {sources}")
            else:
                rendered = " | ".join(sorted(values))
                issues.append(
                    f"row {number} {row['từ mới']!r}, {header!r}: conflict [{rendered}] from {sources}"
                )
    return rows, issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON with kanji strings or partial rows")
    parser.add_argument("--resources", type=Path, required=True, help="Repository resources directory")
    parser.add_argument("--output", type=Path, required=True, help="Destination enriched JSON draft")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = load_input(args.input)
        index = build_index(args.resources)
        rows, issues = enrich(rows, index)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"OK: {args.output} ({len(rows)} rows, {len(issues)} unresolved)")
        for issue in issues:
            print(f"WARNING: {issue}", file=sys.stderr)
        return 2 if issues else 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
