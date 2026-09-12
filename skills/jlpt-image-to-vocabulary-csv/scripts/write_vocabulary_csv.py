#!/usr/bin/env python3
"""Validate extracted JLPT vocabulary rows and write the repository CSV format."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any


HEADERS = ("từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ")


def normalize_cell(value: Any, *, row_number: int, header: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Row {row_number}, column {header!r} must be a string")
    return " ".join(unicodedata.normalize("NFC", value).split())


def validate_rows(raw_rows: Any, *, allow_empty: bool) -> list[dict[str, str]]:
    if isinstance(raw_rows, dict) and set(raw_rows) == {"rows"}:
        raw_rows = raw_rows["rows"]
    if not isinstance(raw_rows, list) or not raw_rows:
        raise ValueError("Input must be a non-empty JSON array or an object containing only 'rows'")

    rows: list[dict[str, str]] = []
    expected = set(HEADERS)
    for row_number, raw_row in enumerate(raw_rows, start=1):
        if not isinstance(raw_row, dict):
            raise ValueError(f"Row {row_number} must be an object")
        missing = expected - set(raw_row)
        extra = set(raw_row) - expected
        if missing or extra:
            details = []
            if missing:
                details.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                details.append(f"extra: {', '.join(sorted(extra))}")
            raise ValueError(f"Row {row_number} has invalid columns ({'; '.join(details)})")
        row = {
            header: normalize_cell(raw_row[header], row_number=row_number, header=header)
            for header in HEADERS
        }
        if not allow_empty:
            empty = [header for header in HEADERS if not row[header]]
            if empty:
                raise ValueError(f"Row {row_number} has empty columns: {', '.join(empty)}")
        rows.append(row)
    return rows


def duplicate_rows(rows: list[dict[str, str]]) -> list[tuple[int, int]]:
    first_seen: dict[tuple[str, ...], int] = {}
    duplicates: list[tuple[int, int]] = []
    for index, row in enumerate(rows, start=1):
        key = tuple(row[header] for header in HEADERS)
        if key in first_seen:
            duplicates.append((index, first_seen[key]))
        else:
            first_seen[key] = index
    return duplicates


def read_csv(path: Path, *, allow_empty: bool) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != HEADERS:
            raise ValueError(f"Invalid CSV header: {reader.fieldnames!r}")
        return validate_rows(list(reader), allow_empty=allow_empty)


def write_csv(path: Path, rows: list[dict[str, str]], *, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Output already exists: {path}. Use --force only when replacement is intended")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, help="JSON file containing extracted rows")
    mode.add_argument("--check", type=Path, help="Validate an existing CSV without changing it")
    parser.add_argument("--output", type=Path, help="Destination CSV; required with --input")
    parser.add_argument("--allow-empty", action="store_true", help="Allow empty cells after explicit review")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.check:
            if args.output or args.force:
                raise ValueError("--output and --force cannot be used with --check")
            rows = read_csv(args.check, allow_empty=args.allow_empty)
            target = args.check
        else:
            if not args.output:
                raise ValueError("--output is required with --input")
            with args.input.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            rows = validate_rows(payload, allow_empty=args.allow_empty)
            write_csv(args.output, rows, force=args.force)
            target = args.output
        duplicates = duplicate_rows(rows)
        print(f"OK: {target} ({len(rows)} rows)")
        for duplicate, original in duplicates:
            print(f"WARNING: row {duplicate} duplicates row {original}", file=sys.stderr)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
