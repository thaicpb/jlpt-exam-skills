#!/usr/bin/env python3
"""Load JLPT vocabulary from the repository's local CSV corpus only."""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import secrets
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
RESOURCE_ROOT = (SKILL_DIR / "../../resources").resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True, help="JLPT level, for example N2")
    parser.add_argument("--lesson", help="Lesson filename without .csv, for example dai1")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--limit", type=int, help="Take the first N matching rows")
    selection.add_argument("--sample", type=int, help="Randomly sample N matching rows")
    parser.add_argument("--seed", type=int, help="Seed used with --sample")
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(message)


def load_examples(path):
    notes_path = path.with_suffix('.examples.json')
    if not notes_path.exists():
        return {}, None
    data = json.loads(notes_path.read_text(encoding='utf-8'))
    if data.get('version') != 1:
        fail(f'Unsupported examples version: {notes_path}')
    notes = {}
    for note in data['items']:
        key = (note['word'], note['example'])
        if key in notes:
            fail(f'Duplicate example: {key[0]} in {notes_path}')
        segments = note['example_segments']
        if not note['example_vi'].strip() or not segments:
            fail(f'Incomplete example: {key[0]}')
        if ''.join(s['text'] for s in segments) != note['example']:
            fail(f'Example text mismatch: {key[0]}')
        for segment in segments:
            reading = segment.get('reading')
            if reading is not None:
                if not re.fullmatch(r'[ぁ-ゖァ-ヺー・ ]+', reading) or key[0] in segment['text']:
                    fail(f'Invalid furigana or target word annotated: {key[0]}')
            elif re.search(r'[一-龯々]', segment['text'].replace(key[0], '')):
                fail(f'Missing furigana: {key[0]} / {segment["text"]}')
        notes[key] = note
    return notes, str(notes_path.relative_to(RESOURCE_ROOT.parent))


def main() -> None:
    args = parse_args()
    level = args.level.upper()
    if not re.fullmatch(r"N[1-5]", level):
        fail("--level must be one of N1, N2, N3, N4, N5")
    if args.lesson and not re.fullmatch(r"[A-Za-z0-9_-]+", args.lesson):
        fail("--lesson may contain only letters, numbers, underscores, and hyphens")
    if args.limit is not None and args.limit < 1:
        fail("--limit must be at least 1")
    if args.sample is not None and args.sample < 1:
        fail("--sample must be at least 1")

    goi_dir = RESOURCE_ROOT / level / "goi"
    if not goi_dir.is_dir():
        available = sorted(path.parent.name for path in RESOURCE_ROOT.glob("N[1-5]/goi"))
        fail(f"No vocabulary data for {level}. Available levels: {', '.join(available) or 'none'}")

    files = [goi_dir / f"{args.lesson}.csv"] if args.lesson else sorted(goi_dir.glob("*.csv"))
    if any(not path.is_file() for path in files):
        available = ", ".join(path.stem for path in sorted(goi_dir.glob("*.csv")))
        fail(f"Lesson not found. Available lessons for {level}: {available or 'none'}")

    required = ["từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ"]
    rows: list[dict[str, object]] = []
    for path in files:
        notes, notes_source = load_examples(path)
        used = set()
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != required:
                fail(f"Unexpected columns in {path}: {reader.fieldnames}")
            for line_number, row in enumerate(reader, start=2):
                rows.append({
                    "word": row[required[0]],
                    "reading": row[required[1]],
                    "meaning_vi": row[required[2]],
                    "example": row[required[3]],
                    "source_file": str(path.relative_to(RESOURCE_ROOT.parent)),
                    "source_line": line_number,
                })
                key = (row[required[0]], row[required[3]])
                if key in notes:
                    note = notes[key]
                    rows[-1].update({name: note[name] for name in ('example_vi', 'example_segments')})
                    rows[-1]['example_notes_source'] = notes_source
                    used.add(key)
        if set(notes) != used:
            fail(f'Stale example annotations in {notes_source}; update them to match the CSV')

    seed = None
    if args.sample is not None:
        seed = args.seed if args.seed is not None else secrets.randbits(32)
        rows = random.Random(seed).sample(rows, min(args.sample, len(rows)))
    elif args.limit is not None:
        rows = rows[:args.limit]

    print(json.dumps({"level": level, "count": len(rows), "seed": seed, "items": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
