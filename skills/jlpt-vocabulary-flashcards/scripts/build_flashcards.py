#!/usr/bin/env python3
"""Render source-faithful flashcards without exercises or scoring."""
import argparse
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render_example(item):
    parts = []
    for segment in item.get("example_segments") or [{"text": item["example"]}]:
        text = html.escape(segment["text"])
        if segment.get("target") is True:
            parts.append(f'<span class="fc-target">{text}</span>')
        elif segment.get("reading"):
            reading = html.escape(segment["reading"])
            parts.append(f'<ruby>{text}<rp>(</rp><rt>{reading}</rt><rp>)</rp></ruby>')
        else:
            parts.append(text)
    return "".join(parts)


def render_static_cards(items):
    cards = []
    for index, item in enumerate(items, start=1):
        word = html.escape(item["word"])
        reading = html.escape(item["reading"])
        meaning = html.escape(item["meaning_vi"])
        translation = html.escape(item.get("example_vi") or "Chưa có bản dịch câu mẫu.")
        source = html.escape(f'{item["source_file"]}:{item["source_line"]}')
        notes = item.get("example_notes_source")
        notes_html = f'<p>Bản dịch và furigana bổ sung: {html.escape(notes)}</p>' if notes else ""
        cards.append(
            f'<details class="fc-static-card" data-card-index="{index}">'
            f'<summary><span class="fc-static-number">{index}</span>'
            f'<span lang="ja" class="fc-static-word">{word}</span></summary>'
            '<div class="fc-static-answer">'
            f'<div class="fc-info"><div><div class="fc-label">Cách đọc</div><div lang="ja" class="fc-reading">{reading}</div></div>'
            f'<div><div class="fc-label">Ý nghĩa</div><div class="fc-meaning">{meaning}</div></div></div>'
            f'<section class="fc-example"><div class="fc-label">Câu mẫu</div><p lang="ja" class="fc-japanese">{render_example(item)}</p>'
            f'<p class="fc-translation">{translation}</p></section>'
            f'<div class="fc-source"><p>Nguồn dữ liệu: {source}</p>{notes_html}</div>'
            '</div></details>'
        )
    return "\n".join(cards)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True)
    parser.add_argument("--lesson")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--limit", type=int)
    group.add_argument("--sample", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--word", action="append")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.word and (args.limit is not None or args.sample is not None or args.offset):
        parser.error("--word cannot be combined with --limit, --sample, or --offset")
    command = [sys.executable, str(ROOT / "scripts/load_vocabulary.py"), "--level", args.level]
    for key in ("lesson", "limit", "sample", "seed", "offset"):
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
        lessons = sorted({
            Path(item["source_file"]).stem.removeprefix("dai")
            for item in payload["items"]
        })
        title = payload["level"] + (f" · Bài {lessons[0]}" if len(lessons) == 1 else " · Từ vựng")
        document = (template
                    .replace("__TITLE__", html.escape(title))
                    .replace("__STATIC_META__", f'{len(payload["items"])} thẻ · Chạm vào từ để xem đáp án')
                    .replace("__STATIC_CARDS__", render_static_cards(payload["items"]))
                    .replace("__DATA__", encoded))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(document, encoding="utf-8")
        print(args.output.resolve())
    except subprocess.CalledProcessError as error:
        parser.exit(2, error.stderr)


if __name__ == "__main__":
    main()
