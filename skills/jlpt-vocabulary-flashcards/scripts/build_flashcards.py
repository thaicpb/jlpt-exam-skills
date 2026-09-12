#!/usr/bin/env python3
"""Render source-faithful flashcards without exercises or scoring."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True)
    parser.add_argument("--lesson")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--limit", type=int)
    group.add_argument("--sample", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--word", action="append")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.word and (args.limit is not None or args.sample is not None):
        parser.error("--word cannot be combined with --limit or --sample")
    command = [sys.executable, str(ROOT / "scripts/load_vocabulary.py"), "--level", args.level]
    for key in ("lesson", "limit", "sample", "seed"):
        value = getattr(args, key)
        if value is not None:
            command.extend(["--" + key, str(value)])
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        payload = json.loads(result.stdout)
        if args.word:
            available = {item["word"] for item in payload["items"]}
            missing = set(args.word) - available
            if missing:
                parser.error("Words not found in selected CSV scope: " + ", ".join(sorted(missing)))
            payload["items"] = [item for item in payload["items"] if item["word"] in args.word]
            payload["count"] = len(payload["items"])
        if not payload["items"]:
            parser.error("No vocabulary matched")
        encoded = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
        template = (ROOT / "assets/flashcards.html").read_text(encoding="utf-8")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(template.replace("__DATA__", encoded), encoding="utf-8")
        print(args.output.resolve())
    except subprocess.CalledProcessError as error:
        parser.exit(2, error.stderr)


if __name__ == "__main__":
    main()
